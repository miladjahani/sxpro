from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Union

from .sim_engine import SimSXCu, ConfigurationA_2Ex1S
from .solver import SolverEngine
from .models import DesignerModeInput, PlantModeInput, SimulationResult

# --- Application Setup ---
app = FastAPI(
    title="SimSXCu API",
    description="API for running copper solvent extraction simulations.",
    version="2.0.0"
)

# --- CORS Middleware ---
# This allows the React frontend (running on a different port) to communicate with the API.
origins = [
    "http://localhost:3000",  # React default dev server
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global Objects ---
# Instantiate the core simulation and solver engines once to be reused across requests.
sim_engine = SimSXCu()
solver = SolverEngine()
# For now, we only have Configuration A. This can be extended later.
config_A = ConfigurationA_2Ex1S(sim_engine)


# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the SimSXCu API. Go to /docs for interactive documentation."}

@app.post("/api/simulate", response_model=SimulationResult)
def run_simulation(data: Union[DesignerModeInput, PlantModeInput] = Body(...)):
    """
    Main endpoint to run a simulation.
    It accepts data for either "Designer Mode" or "Plant Metallurgist Mode".
    """
    params = data.dict()

    try:
        if data.mode == 'designer':
            # --- Designer Mode Logic ---
            objective_func = config_A.option1_objective
            optimization_result = solver.solve_designer_mode(objective_func, params)

            if not optimization_result['success']:
                return SimulationResult(success=False, message=f"Optimization failed: {optimization_result['message']}")

            # Combine initial params with optimized results for final calculation
            full_params = {**params, **optimization_result}
            detailed_results = config_A.calculate_full_results(full_params, mode='designer')

            return SimulationResult(
                **optimization_result,
                **detailed_results
            )

        elif data.mode == 'plant':
            # --- Plant Metallurgist Mode Logic ---
            objective_func = config_A.option2_objective
            optimization_result = solver.solve_plant_mode(objective_func, params)

            if not optimization_result['success']:
                return SimulationResult(success=False, message=f"Optimization failed: {optimization_result['message']}")

            full_params = {**params, **optimization_result}
            detailed_results = config_A.calculate_full_results(full_params, mode='plant')

            return SimulationResult(
                **optimization_result,
                **detailed_results
            )

        else:
            raise HTTPException(status_code=400, detail="Invalid simulation mode specified.")

    except Exception as e:
        # Catch any unexpected errors during simulation
        # In a production environment, you would log this error.
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred during simulation: {e}")