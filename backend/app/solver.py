from scipy.optimize import minimize
from typing import Dict, List, Tuple, Callable

class SolverEngine:
    """
    Solver engine to optimize parameters for the SimSXCu simulation.
    """

    def __init__(self):
        self.method = 'SLSQP'  # Sequential Least Squares Programming

    def solve(self,
              objective_func: Callable,
              initial_guess: List[float],
              bounds: List[Tuple],
              params: Dict) -> Dict:
        """
        Generic solve method that runs the minimization.
        """
        result = minimize(
            objective_func,
            initial_guess,
            args=(params,),
            method=self.method,
            bounds=bounds,
            options={'ftol': 1e-9, 'disp': False} # disp=False for production
        )

        return result

    def solve_designer_mode(self, objective_func: Callable, params: Dict) -> Dict:
        """
        Solve for Option 1 (Designer Mode): Find optimum extractant volume percentage.
        """
        initial_guess = [15.0]  # Initial guess for v/v%
        bounds = [(5.0, 40.0)]    # Reasonable bounds for v/v%

        result = self.solve(objective_func, initial_guess, bounds, params)

        return {
            'success': result.success,
            'v_v_percent_opt': result.x[0] if result.success else None,
            'objective_value': result.fun if result.success else None,
            'message': result.message
        }

    def solve_plant_mode(self, objective_func: Callable, params: Dict) -> Dict:
        """
        Solve for Option 2 (Plant Metallurgist Mode): Find plant operating parameters.
        """
        # Initial guess: [v/v%, SR, Mef1e, Mef2e]
        initial_guess = [15.0, 90.0, 90.0, 90.0]
        bounds = [
            (5.0, 40.0),   # v/v%
            (70.0, 100.0), # SR %
            (70.0, 100.0), # Mef1e %
            (70.0, 100.0)  # Mef2e %
        ]

        result = self.solve(objective_func, initial_guess, bounds, params)

        if result.success:
            return {
                'success': True,
                'v_v_percent_opt': result.x[0],
                'SR_opt': result.x[1],
                'Mef1e_opt': result.x[2],
                'Mef2e_opt': result.x[3],
                'objective_value': result.fun,
                'message': result.message
            }
        else:
            return {
                'success': False,
                'message': result.message
            }