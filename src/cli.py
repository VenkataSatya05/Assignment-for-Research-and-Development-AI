"""Command-line wrapper for full optimization run."""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import io_module
import optimize
import model
import visualize

def main(argv=None):
    """
    Entry point for running the full optimization pipeline from the command line.

    Parameters
    ----------
    argv : list, optional
        Command-line arguments (used mainly for testing). Defaults to None.

    Workflow
    --------
    1. Load observed (x, y) data.
    2. Run full optimization (global + local refinement).
    3. Save optimized parameters to a JSON file.
    4. Generate and save overlay plot of observed vs predicted data.
    """
    parser = argparse.ArgumentParser(description="Run full optimization and generate results.")
    parser.add_argument("--data", required=True, help="Path to input CSV file containing x, y (and optionally t) columns.")
    parser.add_argument("--out", default="results/final_params.json", help="Path to save optimized parameters (JSON).")
    parser.add_argument("--plot", default="examples/overlay_plot.png", help="Path to save overlay plot (PNG).")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for reproducibility.")
    args = parser.parse_args(argv)

    # Load data
    df = io_module.load_xy(args.data)

    # Run optimization
    results = optimize.run_full_optimization(df, seed=args.seed)

    # Save results
    io_module.save_results(results, args.out)

    # Generate predictions
    x_pred, y_pred = model.predict_dataframe(df, results["theta_deg"], results["M"], results["X"])

    # Create overlay plot with parameters
    visualize.overlay_plot(df, x_pred, y_pred, args.plot, 
                theta_deg=results["theta_deg"], 
                M=results["M"], 
                X=results["X"])

    print("✅ Done. Results saved to", args.out)
    print("📈 Plot saved to", args.plot)


if __name__ == "__main__":
    main()