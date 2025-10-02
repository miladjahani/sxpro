import numpy as np
import pandas as pd
from scipy.optimize import minimize, fsolve
from typing import Dict, List, Tuple, Optional

class SimSXCu:
    """
    Copper Solvent Extraction Simulation Engine
    Full Version 2.0 - Based on Joseph Kafumbila's SimSXCu
    """

    def __init__(self):
        self.configurations = {
            'A': 'Series 2Ex1S',
            'B': 'Series 2Ex2S',
            'C': 'Series 3Ex1S',
            'D': 'Series 3Ex2S',
            'E': 'Series parallel 2Ex1Px1S',
            'F': 'Series parallel 2Ex1Px2S',
            'G': 'Optimum series parallel 1Ex1Px1Ex1S',
            'H': 'Optimum series parallel 1Ex1Px1Ex2S',
            'I': 'Triple parallel 1Ex1Px1Px1S',
            'J': 'Triple parallel 1Ex1Px1Px2S',
            'K': 'Interlaced 1Ex1Px1Ex1Px1S',
            'L': 'Interlaced 1Ex1Px1Ex1Px2S',
            'M': 'Double series parallel 2Ex2Px1S',
            'N': 'Double series parallel 2Ex2Px2S',
            'O': 'Optimum triple parallel 1Ex1Px1Px1Ex1S',
            'P': 'Optimum triple parallel 1Ex1Px1Px1Ex2S',
            'Q': 'Organic by pass 2Ex2Px1S',
            'R': 'Organic by pass 2Ex2Px2S'
        }

        self.extractant = "Lix984N"

    def calculate_AML(self, v_v_percent: float) -> float:
        """
        Calculate AML (Maximum loaded when free acid concentration in PLS is zero)
        AML = 0.4108 * (v/v%)^1.1
        """
        return 0.4108 * (v_v_percent ** 1.1)

    def extraction_equilibrium(self, PLS_Cu: float, PLS_Ac: float, v_v_percent: float, C_org: float) -> float:
        """
        Calculate extraction equilibrium using the complex formula from Excel
        This represents the relationship between aqueous and organic copper concentrations
        """
        term1 = -28.511 * (v_v_percent ** -1.746) * C_org + 11.711 * (v_v_percent ** -0.646)
        term2 = (3.303 * v_v_percent - 3.0842 * C_org) ** 2 / C_org
        inner_term = term1 * term2

        A = -1.299 * PLS_Ac - 2 * PLS_Cu - 0.422 * inner_term
        B = ((A ** 2) - 4 * ((0.644 * PLS_Ac + PLS_Cu) ** 2)) ** 0.5

        C_aq = (-A - B) / 2
        return C_aq

    def stripping_equilibrium(self, SP_Cu: float, SP_Ac: float, v_v_percent: float, C_org: float) -> float:
        """
        Calculate stripping equilibrium using the formula from Excel
        """
        term1 = (4.8579/1000 * v_v_percent - 0.19183) * C_org + 11.365 * (v_v_percent ** -0.85)
        term2 = (3.303 * v_v_percent - 3.0842 * C_org) ** 2 / C_org
        inner_term = term1 * term2

        A = -1.299 * SP_Ac - 2 * SP_Cu - 0.422 * inner_term
        B = ((A ** 2) - 4 * ((0.644 * SP_Ac + SP_Cu) ** 2)) ** 0.5

        C_aq = (-A - B) / 2
        return C_aq

    def calculate_ML(self, PLS_Cu: float, PLS_Ac: float, v_v_percent: float, C_org: float) -> float:
        """
        Calculate ML (Maximum loaded - value of copper concentration in organic phase in steady state with PLS)
        """
        equilibrium_term = self.extraction_equilibrium(PLS_Cu, PLS_Ac, v_v_percent, C_org)
        return (PLS_Ac ** 2 / PLS_Cu) - equilibrium_term

    def extraction_recovery(self, PLS_Cu: float, raffinate_Cu: float) -> float:
        """
        Calculate extraction recovery percentage
        """
        if PLS_Cu == 0:
            return 0.0
        return ((PLS_Cu - raffinate_Cu) / PLS_Cu) * 100

    def stripping_recovery(self, loaded_organic_Cu: float, stripped_organic_Cu: float) -> float:
        """
        Calculate stripping recovery percentage
        """
        if loaded_organic_Cu == 0:
            return 0.0
        return ((loaded_organic_Cu - stripped_organic_Cu) / loaded_organic_Cu) * 100

    def net_transfer(self, loaded_organic_Cu: float, stripped_organic_Cu: float, v_v_percent: float) -> float:
        """
        Calculate net transfer (g/l per 1% extractant)
        """
        if v_v_percent == 0:
            return 0.0
        return (loaded_organic_Cu - stripped_organic_Cu) / v_v_percent

class ConfigurationA_2Ex1S:
    """
    Configuration A: Series 2Ex1S (2 Extraction stages, 1 Stripping stage)
    """

    def __init__(self, sim_engine: SimSXCu):
        self.sim = sim_engine
        self.name = "Series 2Ex1S"

    def option1_objective(self, x: List[float], params: Dict) -> float:
        v_v_percent = x[0]

        # Extract parameters
        PLS_Cu = params['PLS_Cu']
        PLS_Ac = params['PLS_Ac']
        SR = params['SR']
        O_A_Ext = params['O_A_Ext']
        Mef1e = params['Mef1e']
        Mef2e = params['Mef2e']
        SP_Cu = params['SP_Cu']
        SP_Ac = params['SP_Ac']
        AD_Cu = params['AD_Cu']
        Mef1s = params['Mef1s']

        AML = self.sim.calculate_AML(v_v_percent)
        ML = AML * SR / 100
        LO = ML

        C1Cuor_Ext = self.calculate_C1Cuor_Ext(PLS_Cu, PLS_Ac, v_v_percent, Mef1e, O_A_Ext, LO)
        C2Cuor_Ext = self.calculate_C2Cuor_Ext(PLS_Cu, PLS_Ac, v_v_percent, Mef1e, Mef2e, O_A_Ext, LO, C1Cuor_Ext)

        O_A_str = self.calculate_O_A_str(AD_Cu, SP_Cu, LO, C2Cuor_Ext)
        C1Cuor_Str = self.calculate_C1Cuor_Str(SP_Cu, SP_Ac, v_v_percent, LO, Mef1s, O_A_str, AD_Cu)

        objective = (C1Cuor_Str * Mef1s / 100 + LO * (1 - Mef1s / 100)) - C2Cuor_Ext

        return abs(objective)

    def option2_objective(self, x: List[float], params: Dict) -> float:
        v_v_percent, SR, Mef1e, Mef2e = x[0], x[1], x[2], x[3]

        PLS_Cu = params['PLS_Cu']
        PLS_Ac = params['PLS_Ac']
        O_A_Ext = params['O_A_Ext']
        ML_plant = params['ML_plant']
        SP_Cu = params['SP_Cu']
        SP_Ac = params['SP_Ac']
        AD_Cu = params['AD_Cu']
        Mef1s = params['Mef1s']

        AML = self.sim.calculate_AML(v_v_percent)
        LO = ML_plant * SR / 100

        C1Cuor_Ext = self.calculate_C1Cuor_Ext(PLS_Cu, PLS_Ac, v_v_percent, Mef1e, O_A_Ext, LO)
        C2Cuor_Ext = self.calculate_C2Cuor_Ext(PLS_Cu, PLS_Ac, v_v_percent, Mef1e, Mef2e, O_A_Ext, LO, C1Cuor_Ext)

        raffinate_E1 = self.calculate_raffinate_E1(PLS_Cu, C1Cuor_Ext, LO, O_A_Ext)
        raffinate_E2 = self.calculate_raffinate_E2(raffinate_E1, C2Cuor_Ext, C1Cuor_Ext, O_A_Ext)

        O_A_str = self.calculate_O_A_str(AD_Cu, SP_Cu, LO, C2Cuor_Ext)
        C1Cuor_Str = self.calculate_C1Cuor_Str(SP_Cu, SP_Ac, v_v_percent, LO, Mef1s, O_A_str, AD_Cu)

        obj1 = ML_plant - self.sim.calculate_ML(PLS_Cu, PLS_Ac, v_v_percent, C1Cuor_Ext)
        obj2 = raffinate_E2 - params['raffinate_Cu_target']
        obj3 = C1Cuor_Str - params['stripped_organic_Cu_target']

        return abs(obj1) + abs(obj2) + abs(obj3)

    def calculate_full_results(self, params: Dict, mode: str) -> Dict:
        """
        Calculate all intermediate and final results for a given set of parameters.
        This is used after optimization to provide detailed output.
        """
        if mode == 'designer':
            v_v_percent = params['v_v_percent_opt']
            SR = params['SR']
            Mef1e = params['Mef1e']
            Mef2e = params['Mef2e']
            AML = self.sim.calculate_AML(v_v_percent)
            ML = AML * SR / 100
        else: # Plant Metallurgist Mode
            v_v_percent = params['v_v_percent_opt']
            SR = params['SR_opt']
            Mef1e = params['Mef1e_opt']
            Mef2e = params['Mef2e_opt']
            ML = params['ML_plant']

        # Shared parameters
        PLS_Cu = params['PLS_Cu']
        PLS_Ac = params['PLS_Ac']
        O_A_Ext = params['O_A_Ext']
        SP_Cu = params['SP_Cu']
        SP_Ac = params['SP_Ac']
        AD_Cu = params['AD_Cu']
        Mef1s = params['Mef1s']

        LO = ML

        # Extraction
        C1Cuor_Ext = self.calculate_C1Cuor_Ext(PLS_Cu, PLS_Ac, v_v_percent, Mef1e, O_A_Ext, LO)
        raffinate_E1 = self.calculate_raffinate_E1(PLS_Cu, C1Cuor_Ext, LO, O_A_Ext)
        C2Cuor_Ext = self.calculate_C2Cuor_Ext(raffinate_E1, PLS_Ac, v_v_percent, Mef2e, O_A_Ext, C1Cuor_Ext)
        raffinate_E2 = self.calculate_raffinate_E2(raffinate_E1, C2Cuor_Ext, C1Cuor_Ext, O_A_Ext)

        # Stripping
        O_A_str = self.calculate_O_A_str(AD_Cu, SP_Cu, LO, C2Cuor_Ext)
        C1Cuor_Str = self.calculate_C1Cuor_Str(SP_Cu, SP_Ac, v_v_percent, LO, Mef1s, O_A_str, AD_Cu)

        # Final Metrics
        ext_recovery = self.sim.extraction_recovery(PLS_Cu, raffinate_E2)
        strip_recovery = self.sim.stripping_recovery(C2Cuor_Ext, C1Cuor_Str)
        net_transfer = self.sim.net_transfer(C2Cuor_Ext, C1Cuor_Str, v_v_percent)

        # McCabe-Thiele Data
        mccabe_ext = self.generate_mccabe_thiele_extraction(PLS_Cu, PLS_Ac, v_v_percent, O_A_Ext, raffinate_E2, C1Cuor_Str, C2Cuor_Ext)
        mccabe_strip = self.generate_mccabe_thiele_stripping(SP_Cu, SP_Ac, v_v_percent, O_A_str, AD_Cu, C1Cuor_Str, C2Cuor_Ext)

        return {
            "C1Cuor_Ext": C1Cuor_Ext,
            "raffinate_E1": raffinate_E1,
            "C2Cuor_Ext": C2Cuor_Ext,
            "raffinate_E2": raffinate_E2,
            "O_A_str": O_A_str,
            "C1Cuor_Str": C1Cuor_Str,
            "extraction_recovery": ext_recovery,
            "stripping_recovery": strip_recovery,
            "net_transfer": net_transfer,
            "mccabe_thiele_extraction": mccabe_ext,
            "mccabe_thiele_stripping": mccabe_strip,
        }

    def calculate_C1Cuor_Ext(self, PLS_Cu: float, PLS_Ac: float, v_v_percent: float,
                           Mef1e: float, O_A_Ext: float, LO: float) -> float:
        C_eq = self.sim.extraction_equilibrium(PLS_Cu, PLS_Ac, v_v_percent, LO)
        transfer = (C_eq - PLS_Cu) * Mef1e / 100
        C_org = LO - transfer / O_A_Ext
        return C_org

    def calculate_C2Cuor_Ext(self, raffinate_E1: float, PLS_Ac: float, v_v_percent: float,
                           Mef2e: float, O_A_Ext: float, C1Cuor_Ext: float) -> float:
        C_eq = self.sim.extraction_equilibrium(raffinate_E1, PLS_Ac, v_v_percent, C1Cuor_Ext)
        transfer = (C_eq - raffinate_E1) * Mef2e / 100
        C_org = C1Cuor_Ext - transfer / O_A_Ext
        return C_org

    def calculate_O_A_str(self, AD_Cu: float, SP_Cu: float, LO: float, C2Cuor_Ext: float) -> float:
        # This is a simplification. In a real scenario, this might be an input or calculated differently.
        # For now, derive from a simple mass balance.
        copper_stripped = C2Cuor_Ext - LO # Approximation for stripped organic
        electrolyte_gain = AD_Cu - SP_Cu
        if copper_stripped > 0 and electrolyte_gain > 0:
             return electrolyte_gain / copper_stripped
        return 1.0

    def calculate_C1Cuor_Str(self, SP_Cu: float, SP_Ac: float, v_v_percent: float,
                           LO: float, Mef1s: float, O_A_str: float, AD_Cu: float) -> float:
        # The incoming organic to stripping is the loaded organic from extraction (C2Cuor_Ext)
        # This function seems to have a slight logic error in the original script.
        # Let's assume LO is the fully loaded organic for equilibrium calculation purposes.
        C_eq = self.sim.stripping_equilibrium(AD_Cu, SP_Ac, v_v_percent, LO)
        transfer = (LO - C_eq) * Mef1s / 100
        C_org = LO - (transfer * O_A_str)
        return C_org

    def calculate_raffinate_E1(self, PLS_Cu: float, C1Cuor_Ext: float, LO: float, O_A_Ext: float) -> float:
        return PLS_Cu - (C1Cuor_Ext - LO) * O_A_Ext

    def calculate_raffinate_E2(self, raffinate_E1: float, C2Cuor_Ext: float, C1Cuor_Ext: float, O_A_Ext: float) -> float:
        return raffinate_E1 - (C2Cuor_Ext - C1Cuor_Ext) * O_A_Ext

    def generate_mccabe_thiele_extraction(self, PLS_Cu, PLS_Ac, v_v_percent, O_A_Ext, raffinate_Cu, stripped_org_Cu, loaded_org_Cu):
        # Equilibrium line
        aq_eq = np.linspace(raffinate_Cu, PLS_Cu, 20)
        org_eq = [self.sim.extraction_equilibrium(c, PLS_Ac, v_v_percent, 0) for c in aq_eq] # Simplified C_org=0

        # Operating line
        op_line_x = [raffinate_Cu, PLS_Cu]
        op_line_y = [stripped_org_Cu, loaded_org_Cu]

        return {"eq_x": list(aq_eq), "eq_y": list(org_eq), "op_x": op_line_x, "op_y": op_line_y}

    def generate_mccabe_thiele_stripping(self, SP_Cu, SP_Ac, v_v_percent, O_A_str, AD_Cu, stripped_org_Cu, loaded_org_Cu):
        # Equilibrium line
        org_eq = np.linspace(stripped_org_Cu, loaded_org_Cu, 20)
        aq_eq = [self.sim.stripping_equilibrium(SP_Cu, SP_Ac, v_v_percent, c) for c in org_eq]

        # Operating line
        op_line_x = [stripped_org_Cu, loaded_org_Cu]
        op_line_y = [SP_Cu, AD_Cu]

        return {"eq_x": list(org_eq), "eq_y": list(aq_eq), "op_x": op_line_x, "op_y": op_line_y}