from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class SimulationInputBase(BaseModel):
    # Common parameters for both modes
    PLS_flow: float = Field(..., gt=0, description="Pregnant Leach Solution Flow Rate (m³/h)")
    PLS_Cu: float = Field(..., gt=0, description="PLS Copper Concentration (g/l)")
    PLS_Ac: float = Field(..., gt=0, description="PLS Acid Concentration (g/l)")
    O_A_Ext: float = Field(..., gt=0, description="Extraction O/A Ratio")
    SP_Cu: float = Field(..., gt=0, description="Spent Electrolyte Copper (g/l)")
    SP_Ac: float = Field(..., gt=0, description="Spent Electrolyte Acid (g/l)")
    AD_Cu: float = Field(..., gt=0, description="Advanced Electrolyte Copper (g/l)")
    Mef1s: float = Field(..., gt=0, le=100, description="Stripping Mixer Efficiency 1 (%)")

class DesignerModeInput(SimulationInputBase):
    mode: str = "designer"
    SR: float = Field(..., gt=0, le=100, description="Saturation Ratio (%)")
    Mef1e: float = Field(..., gt=0, le=100, description="Extraction Mixer Efficiency 1 (%)")
    Mef2e: float = Field(..., gt=0, le=100, description="Extraction Mixer Efficiency 2 (%)")

class PlantModeInput(SimulationInputBase):
    mode: str = "plant"
    ML_plant: float = Field(..., gt=0, description="Loaded Organic from Plant Lab (g/l)")
    raffinate_Cu_target: float = Field(..., ge=0, description="Target Raffinate Copper (g/l)")
    stripped_organic_Cu_target: float = Field(..., ge=0, description="Target Stripped Organic Copper (g/l)")

class McCabeThieleData(BaseModel):
    eq_x: List[float]
    eq_y: List[float]
    op_x: List[float]
    op_y: List[float]

class SimulationResult(BaseModel):
    success: bool
    message: str
    v_v_percent_opt: Optional[float] = None
    SR_opt: Optional[float] = None
    Mef1e_opt: Optional[float] = None
    Mef2e_opt: Optional[float] = None
    objective_value: Optional[float] = None

    # Detailed results
    C1Cuor_Ext: Optional[float] = None
    raffinate_E1: Optional[float] = None
    C2Cuor_Ext: Optional[float] = None
    raffinate_E2: Optional[float] = None
    O_A_str: Optional[float] = None
    C1Cuor_Str: Optional[float] = None
    extraction_recovery: Optional[float] = None
    stripping_recovery: Optional[float] = None
    net_transfer: Optional[float] = None

    mccabe_thiele_extraction: Optional[McCabeThieleData] = None
    mccabe_thiele_stripping: Optional[McCabeThieleData] = None