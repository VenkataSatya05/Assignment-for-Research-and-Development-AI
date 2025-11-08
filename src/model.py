"""
Parametric forward model for x(t) and y(t).

Model:
    x = t * cos(theta) - exp(M * |t|) * sin(0.3 * t) * sin(theta) + X
    y = 42 + t * sin(theta) + exp(M * |t|) * sin(0.3 * t) * cos(theta)

theta is provided in degrees by callers; convert internally to radians.
"""

import numpy as np
from typing import Tuple


def forward(t: np.ndarray, theta_deg: float, M: float, X: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute predicted (x, y) arrays for given parameters.

    Parameters
    ----------
    t : array-like
        Parameter t (same shape as x/y observations)
    theta_deg : float
        Theta in degrees; will be converted to radians internally.
    M : float
        Model parameter controlling exponential growth with |t|.
    X : float
        X offset value.

    Returns
    -------
    x, y : Tuple[np.ndarray, np.ndarray]
        Predicted arrays for x(t) and y(t).
    """
    theta = np.deg2rad(theta_deg)
    t = np.asarray(t)
    exp_term = np.exp(M * np.abs(t))
    s = np.sin(0.3 * t)

    x = t * np.cos(theta) - exp_term * s * np.sin(theta) + X
    y = 42 + t * np.sin(theta) + exp_term * s * np.cos(theta)

    return x, y


def predict_dataframe(df, theta_deg: float, M: float, X: float):
    """
    Compute predicted x and y based on a DataFrame containing t values.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with optional 't' column. If missing, t is generated uniformly.
    theta_deg : float
        Theta in degrees.
    M : float
        Exponential parameter.
    X : float
        Offset parameter.

    Returns
    -------
    x, y : Tuple[np.ndarray, np.ndarray]
        Predicted arrays corresponding to input DataFrame rows.
    """
    if "t" in df.columns:
        t = df["t"].values
    else:
        # assume uniform spacing between 6 and 60 for rows
        n = len(df)
        t = np.linspace(6, 60, n)

    x, y = forward(t, theta_deg, M, X)
    return x, y
