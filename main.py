import sys
import os
import json
import numpy as np

# Add the src directory to the path so we can import from it
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Import the modules directly
import io_module
import optimize
import model
import visualize
import loss

def main():
    """
    Main entry point for running the curve fitting analysis.
    """
    # Define paths relative to the current directory
    data_path = os.path.join('data', 'xy_data.csv')
    results_path = os.path.join('results', 'final_params.json')
    plot_path = os.path.join('examples', 'overlay_plot.png')
    error_dist_path = os.path.join('examples', 'error_distribution.png')
    error_heatmap_path = os.path.join('examples', 'error_heatmap.png')
    obs_vs_pred_x_path = os.path.join('examples', 'observed_vs_predicted_x.png')
    obs_vs_pred_y_path = os.path.join('examples', 'observed_vs_predicted_y.png')
    
    print("Loading data...")
    df = io_module.load_xy(data_path)
    
    print("Running optimization...")
    results = optimize.run_full_optimization(df, seed=42)
    
    # Save results
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate predictions
    x_pred, y_pred = model.predict_dataframe(df, results["theta_deg"], results["M"], results["X"])
    
    # Create overlay plot
    visualize.overlay_plot(df, x_pred, y_pred, plot_path, 
                          theta_deg=results["theta_deg"], 
                          M=results["M"], 
                          X=results["X"])
    
    # Calculate errors for additional visualizations
    x_obs = df["x"].values
    y_obs = df["y"].values
    
    # Calculate point-wise L1 errors
    errors = np.abs(x_obs - x_pred) + np.abs(y_obs - y_pred)
    
    # Create error distribution plot
    visualize.error_distribution_plot(errors, error_dist_path)
    
    # Create error heatmap
    visualize.error_heatmap_plot(df, x_pred, y_pred, error_heatmap_path)
    
    # Create observed vs predicted scatter plots
    visualize.observed_vs_predicted_scatter_plots(df, x_pred, y_pred, 
                                                 obs_vs_pred_x_path, obs_vs_pred_y_path)
    
    # Print results
    print(f"\nOptimized Parameters:")
    print(f"θ = {results['theta_deg']:.6f}°")
    print(f"M = {results['M']:.6f}")
    print(f"X = {results['X']:.6f}")
    print(f"Total L1 Loss: {results['l1']:.6f}")
    print(f"Success: {results['success']}")
    
    # Print error statistics
    mean_error = np.mean(errors)
    median_error = np.median(errors)
    std_error = np.std(errors)
    min_error = np.min(errors)
    max_error = np.max(errors)
    
    print(f"\nError Statistics:")
    print(f"Mean L1 Error: {mean_error:.6f}")
    print(f"Median L1 Error: {median_error:.6f}")
    print(f"Standard Deviation: {std_error:.6f}")
    print(f"Min Error: {min_error:.6f}")
    print(f"Max Error: {max_error:.6f}")
    
    # Calculate R² score
    ss_res = np.sum(errors**2)
    ss_tot = np.sum((np.concatenate([x_obs, y_obs]) - np.mean(np.concatenate([x_obs, y_obs])))**2)
    r2 = 1 - (ss_res / ss_tot)
    print(f"R² Score: {r2:.6f}")
    
    print(f"\nResults saved to: {results_path}")
    print(f"lots saved to:")
    print(f"   - Overlay plot: {plot_path}")
    print(f"   - Error distribution: {error_dist_path}")
    print(f"   - Error heatmap: {error_heatmap_path}")
    print(f"   - Observed vs Predicted (x): {obs_vs_pred_x_path}")
    print(f"   - Observed vs Predicted (y): {obs_vs_pred_y_path}")

if __name__ == "__main__":
    main()