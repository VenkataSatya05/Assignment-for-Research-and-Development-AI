"""Basic unit tests for forward model and loss using synthetic parameters."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from model import forward
from loss import l1_loss


def test_forward_and_loss():
    """
    Test forward model and L1 loss functions using synthetic parameters.
    Ensures that comparing predictions to themselves gives zero loss.
    """
    t = np.array([6.0, 10.0, 30.0])
    theta_deg = 20.0
    M = 0.01
    X = 5.0

    # Generate synthetic predictions
    x, y = forward(t, theta_deg, M, X)

    # Compute L1 loss when comparing predictions to themselves (should be 0)
    l = l1_loss(x, y, x, y)
    assert l == 0.0, f"L1 loss expected 0.0, got {l}"


if __name__ == "__main__":
    test_forward_and_loss()
    print("Tests passed.")