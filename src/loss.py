"""Loss utilities."""

import numpy as np


def l1_loss(x_obs, y_obs, x_pred, y_pred) -> float:
    """
    Compute the total L1 (Manhattan) distance between observed and predicted coordinates.

    Parameters
    ----------
    x_obs, y_obs : array-like
        Observed x and y values.
    x_pred, y_pred : array-like
        Predicted x and y values.

    Returns
    -------
    float
        Total L1 loss summing both coordinates.
    """
    return float(np.sum(np.abs(x_obs - x_pred) + np.abs(y_obs - y_pred)))


def mean_l1(x_obs, y_obs, x_pred, y_pred) -> float:
    """
    Compute the mean L1 (Manhattan) loss per observation.

    Parameters
    ----------
    x_obs, y_obs : array-like
        Observed x and y values.
    x_pred, y_pred : array-like
        Predicted x and y values.

    Returns
    -------
    float
        Mean L1 loss per sample.
    """
    n = len(x_obs)
    return l1_loss(x_obs, y_obs, x_pred, y_pred) / float(n)
