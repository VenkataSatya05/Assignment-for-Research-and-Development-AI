# RDE AI Curve Fitting

This repository contains code and results for estimating parameters θ, M, X in a parametric curve model using observed (x, y) data points.

## Project Overview

The goal of this project is to fit a parametric model to observed 2D trajectory data. The model is defined as:

```
x = t * cos(θ) - exp(M * |t|) * sin(0.3 * t) * sin(θ) + X
y = 42 + t * sin(θ) + exp(M * |t|) * sin(0.3 * t) * cos(θ)
```

Where:
- θ is an angle parameter (0° to 50°)
- M is an exponential parameter (-0.05 to 0.05)
- X is an offset parameter (0 to 100)
- t is a parameter that maps to data points

## Repository Structure

```
.
├── README.md
├── environment.yml
├── .gitignore
├── data/
│   └── xy_data.csv
├── notebooks/
├── src/
│   ├── __init__.py
│   ├── io_module.py
│   ├── model.py
│   ├── loss.py
│   ├── optimize.py
│   ├── visualize.py
│   ├── cli.py
│   ├── app.py
│   └── tests/
│       └── test_model.py
├── docs/
│   └── COMPREHENSIVE_REPORT.md
├── examples/
│   ├── overlay_plot.png
│   ├── error_distribution.png
│   ├── error_heatmap.png
│   ├── observed_vs_predicted_x.png
│   └── observed_vs_predicted_y.png
├── results/
│   ├── final_params.json
│   └── final_curve_equation.txt
├── main.py

```

## Installation

1. **Create the conda environment:**
   ```bash
   conda env create -f environment.yml
   ```

2. **Activate the environment:**
   ```bash
   conda activate rde_ai_curve_env
   ```

## Usage

### Running the Analysis

To run the complete optimization pipeline:

```bash
python main.py
```

This will:
1. Load the data from `data/xy_data.csv`
2. Run global and local optimization
3. Save the optimized parameters to `results/final_params.json`
4. Generate multiple visualizations at `examples/`:
   - `overlay_plot.png`: Observed data and fitted curve
   - `error_distribution.png`: Histogram of L1 errors
   - `error_heatmap.png`: Error magnitude visualization
   - `observed_vs_predicted_x.png`: X coordinate correlation
   - `observed_vs_predicted_y.png`: Y coordinate correlation

### Command-Line Options

The analysis script accepts several options:

```bash
python main.py
```

### Using the FastAPI Backend

To run the FastAPI server:

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

Endpoints:
- `/status` - Health check
- `/predict` - Generate predictions with given parameters
- `/final` - Get final optimized parameters

## Results

After running the analysis, you will find:

1. **Optimized Parameters**: `results/final_params.json` contains the estimated θ, M, and X values
2. **Visualizations**: Multiple plots in `examples/` directory showing various aspects of the fit
3. **Comprehensive Report**: Detailed documentation in `docs/COMPREHENSIVE_REPORT.md`

## Development

### Running Tests

```bash
python src/tests/test_model.py
```

### Project Structure Details

- `src/model.py`: Forward parametric model implementation
- `src/loss.py`: L1 cost function
- `src/optimize.py`: Global and local optimization routines
- `src/visualize.py`: Plotting utilities including error distribution, heatmap, and scatter plots
- `src/io_module.py`: Data loading and saving functions
- `src/cli.py`: Command-line interface
- `src/app.py`: FastAPI backend
- `src/tests/`: Unit and integration tests



## Contact

For questions about this repository, please contact the development team .
