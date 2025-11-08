import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from matplotlib.colors import Normalize
import matplotlib.cm as cm


def overlay_plot(df, x_pred, y_pred, out_path: str, theta_deg=None, M=None, X=None):
    """
    Generate an overlay plot of observed vs predicted trajectories and save to file.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing observed 'x' and 'y' columns.
    x_pred, y_pred : array-like
        Predicted x and y arrays.
    out_path : str
        File path where the output image will be saved.
    theta_deg, M, X : float, optional
        Optimized parameters to display in title.

    Returns
    -------
    None
    """
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.scatter(df["x"].values, df["y"].values, label="Observed", s=10, alpha=0.7)
    plt.plot(x_pred, y_pred, label="Predicted", linewidth=2, color='red')
    plt.xlabel("x")
    plt.ylabel("y")
    
    # Add title with parameters if provided
    if theta_deg is not None and M is not None and X is not None:
        plt.title(f"Curve Fitting Results\nθ={theta_deg:.2f}°, M={M:.4f}, X={X:.2f}")
    else:
        plt.title("Curve Fitting Results")
    
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(p, dpi=200)
    plt.close()


def error_distribution_plot(errors, out_path: str):
    """
    Generate a histogram of L1 errors and save to file.

    Parameters
    ----------
    errors : array-like
        Array of L1 errors for each point.
    out_path : str
        File path where the output image will be saved.

    Returns
    -------
    None
    """
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.hist(errors, bins=50, alpha=0.7, color='skyblue', edgecolor='black', linewidth=0.5)
    plt.xlabel("L1 Error")
    plt.ylabel("Frequency")
    plt.title("Distribution of L1 Errors")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(p, dpi=300)
    plt.close()


def error_heatmap_plot(df, x_pred, y_pred, out_path: str):
    """
    Generate an error heatmap showing error magnitude along the curve.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing observed 'x' and 'y' columns.
    x_pred, y_pred : array-like
        Predicted x and y arrays.
    out_path : str
        File path where the output image will be saved.

    Returns
    -------
    None
    """
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    # Calculate errors
    errors = np.abs(df["x"].values - x_pred) + np.abs(df["y"].values - y_pred)
    
    plt.figure(figsize=(12, 6))
    
    # Create scatter plot with color mapping based on error
    scatter = plt.scatter(df["x"].values, df["y"].values, c=errors, cmap='viridis', 
                         s=20, alpha=0.7, edgecolors='black', linewidth=0.3)
    
    plt.colorbar(scatter, label='L1 Error')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Error Heatmap (Observed Points Colored by L1 Error)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(p, dpi=300)
    plt.close()


def observed_vs_predicted_scatter_plots(df, x_pred, y_pred, out_path_x: str, out_path_y: str):
    """
    Generate scatter plots of observed vs predicted values for x and y coordinates.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing observed 'x' and 'y' columns.
    x_pred, y_pred : array-like
        Predicted x and y arrays.
    out_path_x : str
        File path where the x scatter plot will be saved.
    out_path_y : str
        File path where the y scatter plot will be saved.

    Returns
    -------
    None
    """
    # X scatter plot
    p_x = Path(out_path_x)
    p_x.parent.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(df["x"].values, x_pred, alpha=0.7, color='blue')
    plt.plot([df["x"].min(), df["x"].max()], [df["x"].min(), df["x"].max()], 'r--', lw=2)
    plt.xlabel("Observed x")
    plt.ylabel("Predicted x")
    plt.title("Observed vs Predicted x Values")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(p_x, dpi=300)
    plt.close()
    
    # Y scatter plot
    p_y = Path(out_path_y)
    p_y.parent.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(df["y"].values, y_pred, alpha=0.7, color='green')
    plt.plot([df["y"].min(), df["y"].max()], [df["y"].min(), df["y"].max()], 'r--', lw=2)
    plt.xlabel("Observed y")
    plt.ylabel("Predicted y")
    plt.title("Observed vs Predicted y Values")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(p_y, dpi=300)
    plt.close()