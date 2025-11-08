"""Optimization routines: global search + local refinement."""

from typing import Tuple
import numpy as np
from scipy.optimize import differential_evolution, minimize
import sys
import os

# Add the current directory to the path so we can import from it
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the modules directly
import model
import loss

# Parameter bounds
THETA_BOUNDS = (1e-6, 50.0 - 1e-6)   # degrees, strict open interval
M_BOUNDS = (-0.05 + 1e-8, 0.05 - 1e-8)
X_BOUNDS = (1e-6, 100.0 - 1e-6)


def objective(params, df) -> float:
    """
    Compute L1 loss for given parameters.

    Parameters
    ----------
    params : tuple
        (theta, M, X) parameter tuple.
    df : pandas.DataFrame
        DataFrame with observed 'x', 'y', and optionally 't' values.

    Returns
    -------
    float
        L1 loss between observed and predicted (x, y).
    """
    theta, M, X = params
    x_pred, y_pred = model.predict_dataframe(df, theta, M, X)
    return loss.l1_loss(df["x"].values, df["y"].values, x_pred, y_pred)


def global_search(df, seed: int = 0, maxiter: int = 50) -> Tuple[float, Tuple[float, float, float]]:
    """
    Perform a global optimization using Differential Evolution.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing observed data.
    seed : int, optional
        Random seed for reproducibility.
    maxiter : int, optional
        Maximum number of iterations for the global search.

    Returns
    -------
    Tuple[float, Tuple[float, float, float]]
        Best objective value and corresponding parameters (theta, M, X).
    """
    bounds = [THETA_BOUNDS, M_BOUNDS, X_BOUNDS]

    def obj_wrapped(v):
        return objective(v, df)

    result = differential_evolution(
        obj_wrapped,
        bounds,
        maxiter=maxiter,
        seed=seed,
        polish=False
    )

    return result.fun, tuple(result.x)


def local_refine(df, x0, method: str = "Powell"):
    """
    Perform local optimization (refinement) from a given starting point.

    Parameters
    ----------
    df : pandas.DataFrame
        Observed data.
    x0 : array-like
        Initial parameter guess (theta, M, X).
    method : str, optional
        Optimization method (default: "Powell" for derivative-free optimization).

    Returns
    -------
    scipy.optimize.OptimizeResult
        Optimization result object.
    """
    bounds = [
        (THETA_BOUNDS[0], THETA_BOUNDS[1]),
        (M_BOUNDS[0], M_BOUNDS[1]),
        (X_BOUNDS[0], X_BOUNDS[1])
    ]

    res = minimize(
        lambda p: objective(p, df),
        x0,
        method=method,
        bounds=bounds,
        options={"maxiter": 10000}
    )

    return res


def run_full_optimization(df, seed: int = 0):
    """
    Run a full optimization pipeline:
    1. Global search using Differential Evolution.
    2. Local refinement using Powell method.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame with observed x, y, and optionally t.
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    dict
        Dictionary with optimized parameters and status.
    """
    # Step 1: Global search
    g_val, g_params = global_search(df, seed=seed)

    # Step 2: Local refinement
    res = local_refine(df, x0=np.array(g_params), method="Powell")

    # Step 3: Extract results
    final_params = res.x if res.success else np.array(g_params)
    final_val = float(res.fun) if res.success else float(g_val)

    return {
        "theta_deg": float(final_params[0]),
        "M": float(final_params[1]),
        "X": float(final_params[2]),
        "l1": float(final_val),
        "success": bool(res.success)
    }