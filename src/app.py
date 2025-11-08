"""Optional FastAPI endpoint to serve results and predicted points."""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import json
from pathlib import Path
import sys
import os

# Add the current directory to the path so we can import from it
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the modules directly
import io_module
from model import predict_dataframe

app = FastAPI()


class Params(BaseModel):
    """Pydantic model for prediction parameters."""
    theta_deg: float
    M: float
    X: float


@app.get("/status")
async def status() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns
    -------
    dict
        Dictionary containing API status.
    """
    return {"status": "ok"}


@app.post("/predict")
async def predict(params: Params, data_path: str = "data/xy_data.csv") -> Dict[str, list]:
    """
    Predict (x, y) coordinates based on given parameters.

    Parameters
    ----------
    params : Params
        Model parameters (theta_deg, M, X).
    data_path : str, optional
        Path to CSV file containing observed data (default: 'data/xy_data.csv').

    Returns
    -------
    dict
        Dictionary containing predicted x and y arrays.
    """
    df = io_module.load_xy(data_path)
    x_pred, y_pred = predict_dataframe(df, params.theta_deg, params.M, params.X)
    return {"x_pred": x_pred.tolist(), "y_pred": y_pred.tolist()}


@app.get("/final")
async def final(results_path: str = "results/final_params.json") -> Dict:
    """
    Return the final optimized parameters as JSON.

    Parameters
    ----------
    results_path : str, optional
        Path to saved JSON results file (default: 'results/final_params.json').

    Returns
    -------
    dict
        JSON object with optimized parameters or error message.
    """
    p = Path(results_path)
    if not p.exists():
        return {"error": "results not found"}
    return json.loads(p.read_text())