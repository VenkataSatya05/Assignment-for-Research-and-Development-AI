# AI-Driven Curve Fitting Project

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)


> Parametric curve fitting using optimization algorithms to estimate parameters from 2D trajectory data

## 📋 Table of Contents

- [Overview](#overview)
- [Mathematical Model](#mathematical-model)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Repository Structure](#repository-structure)
- [Documentation](#documentation)
- [Development](#development)
- [License](#license)
- [Contact](#contact)

## Overview

This project implements an AI-driven approach to fit a parametric mathematical model to observed 2D trajectory data. Using sophisticated optimization techniques (Differential Evolution for global search and Powell method for local refinement), the system estimates three critical parameters that best describe the curve.

**Key Objectives:**
- Estimate parameters θ (angle), M (exponential coefficient), and X (offset)
- Minimize L1 distance between observed and predicted trajectories
- Provide comprehensive visualization and analysis tools
- Deliver production-ready, well-documented code

## Mathematical Model

The parametric equations define the curve as:


$$
x(t) = t \cdot \cos\theta - e^{M \cdot |t|} \cdot \sin(0.3t) \cdot \sin\theta + X \qquad,
y(t) = 42 + t \cdot \sin\theta + e^{M \cdot |t|} \cdot \sin(0.3t) \cdot \cos\theta
$$


**Parameters:**
- **θ** (theta): Angle parameter, range [0°, 50°]
- **M**: Exponential modulation coefficient, range [-0.05, 0.05]
- **X**: Horizontal offset, range [0, 100]
- **t**: Independent parameter, range (6, 60)

**Model Components:**
- **Linear terms**: `t·cos(θ)` and `t·sin(θ)` create the base trajectory
- **Oscillatory component**: `sin(0.3t)` adds periodic variations
- **Exponential modulation**: `e^(M |t|)` controls oscillation amplitude
- **Translation**: X shifts horizontally, 42 shifts vertically

## Features

✨ **Core Capabilities:**
- Multi-stage optimization (global → local refinement)
- L1 distance minimization
- Automatic t-parameter estimation
- Comprehensive error analysis
- Multiple visualization outputs

📊 **Visualization Suite:**
- Overlay plots (observed vs. fitted)
- Error distribution histograms
- Error heatmaps
- Correlation scatter plots
- Q-Q plots for residual analysis

🔧 **Tools & Interfaces:**
- Command-line interface (CLI)
- FastAPI REST API backend
- Modular, testable codebase
- Reproducible results (seed control)

## Installation

### Prerequisites

- Python 3.8 or higher
- Conda (recommended) or pip

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-curve-fitting.git
   cd ai-curve-fitting
   ```

2. **Create and activate conda environment:**
   ```bash
   conda env create -f environment.yml
   conda activate rde_ai_curve_env
   ```

   **Alternative (pip):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python -c "import numpy, scipy, matplotlib; print('Setup successful!')"
   ```

## Usage

### Quick Start

Run the complete optimization pipeline:

```bash
python main.py
```

This executes all phases:
1. Data loading and validation
2. Global optimization (Differential Evolution)
3. Local refinement (Powell method)
4. Parameter extraction and saving
5. Comprehensive visualization generation

### Command-Line Interface

```bash
# Run with default settings
python src/cli.py

# Specify custom data file
python src/cli.py --data path/to/data.csv

# Custom output directory
python src/cli.py --output custom_results/

# Verbose mode
python src/cli.py --verbose
```

### API Server

Launch the FastAPI backend:

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

**Available Endpoints:**

- `GET /status` - Health check
- `POST /predict` - Generate predictions with custom parameters
  ```json
  {
    "theta_deg": 28.19,
    "M": 0.0216,
    "X": 54.92,
    "t_values": [10, 20, 30, 40, 50]
  }
  ```
- `GET /final` - Retrieve optimized parameters

**Interactive Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Python API

```python
from src.model import forward
from src.optimize import run_optimization
from src.io_module import load_data

# Load data
df = load_data('data/xy_data.csv')

# Run optimization
result = run_optimization(df)

# Access results
theta, M, X = result['theta_deg'], result['M'], result['X']
print(f"Optimized: θ={theta:.6f}°, M={M:.6f}, X={X:.6f}")

# Generate predictions
t_values = np.linspace(6, 60, 100)
x_pred, y_pred = forward(t_values, theta, M, X)
```

## Results

### Final Optimized Parameters

```
θ (theta) = 28.192715°  (0.492161 radians)
M         = 0.021583
X         = 54.916793
```

### Performance Metrics

- **Total L1 Distance**: 37,865.21
- **Mean L1 Error**: 25.24
- **Median L1 Error**: 22.29
- **Standard Deviation**: 17.10
- **R² Score**: -0.63

### LaTeX/Desmos Format

```latex
\left(t*\cos(0.492161)-e^{0.021583\left|t\right|}\cdot\sin(0.3t)\sin(0.492161)+54.916793,42+t*\sin(0.492161)+e^{0.021583\left|t\right|}\cdot\sin(0.3t)\cos(0.492161)\right)
```

### Output Files

After running the analysis:

- `results/final_params.json` - Optimized parameter values
- `results/final_curve_equation.txt` - LaTeX-formatted equation
- `examples/overlay_plot.png` - Main fitting visualization
- <img width="2000" height="1200" alt="image" src="https://github.com/user-attachments/assets/fede7b1c-29e4-4b2b-bf08-d66625d64c02" />
- `examples/error_distribution.png` - Error histogram
- <img width="3000" height="1800" alt="image" src="https://github.com/user-attachments/assets/d135efb2-b66d-458e-98e2-1fa3579a328f" />
- `examples/error_heatmap.png` - Spatial error distribution
- <img width="3600" height="1800" alt="image" src="https://github.com/user-attachments/assets/b42ca2fb-c1b8-4543-ac95-6c231a4bba51" />
- `examples/observed_vs_predicted_x.png` - X-coordinate correlation
- `examples/observed_vs_predicted_y.png` - Y-coordinate correlation

## Repository Structure

```
ai-curve-fitting/
├── README.md                      # This file
├── environment.yml                # Conda environment specification
├── requirements.txt               # Pip dependencies
├── .gitignore                     # Git ignore patterns
│
├── data/
│   └── xy_data.csv               # Input trajectory data (1501 points)
│
├── src/
│   ├── __init__.py               # Package initialization
│   ├── io_module.py              # Data I/O utilities
│   ├── model.py                  # Parametric model implementation
│   ├── loss.py                   # L1 loss function
│   ├── optimize.py               # Optimization routines
│   ├── visualize.py              # Plotting utilities
│   ├── cli.py                    # Command-line interface
│   ├── app.py                    # FastAPI backend
│   └── tests/
│       └── test_model.py         # Unit tests
│
├── results/
│   ├── final_params.json         # Optimized parameters
│   └── final_curve_equation.txt  # LaTeX equation
│
├── examples/
│   ├── overlay_plot.png          # Visualizations (300 DPI)
│   ├── error_distribution.png
│   ├── error_heatmap.png
│   ├── observed_vs_predicted_x.png
│   └── observed_vs_predicted_y.png
│
├── docs/
│   └── COMPREHENSIVE_REPORT.md   # Detailed technical documentation
│
├── main.py                       # Main execution script
└── deploy/                       # Deployment configurations
```

## Documentation

Comprehensive documentation is available in `docs/COMPREHENSIVE_REPORT.md`, covering:

- **Phase 1**: Data Analysis & Exploration
- **Phase 2**: Mathematical Model Setup
- **Phase 3**: Optimization Strategy
- **Phase 4**: Parameter Estimation
- **Phase 5**: Model Validation
- **Phase 6**: Visualization Suite
- **Phase 7**: Code Quality Standards
- **Phase 8**: Results & Submission Format
- **Phase 9**: Repository Organization

## Development

### Running Tests

```bash
# Run all tests
python -m pytest src/tests/

# Run specific test file
python src/tests/test_model.py

# With coverage
pytest --cov=src src/tests/
```

### Code Quality

This project follows:
- **PEP 8** style guidelines
- **Type hints** for function signatures
- **Comprehensive docstrings** (Google style)
- **Modular design** principles
- **Error handling** best practices

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Contact

**Project Maintainer**: Alajangi Venkata Satya
- Email: satyavenkata46@gmail.com
- GitHub: [@VenkataSatya05](https://github.com/VenkataSatya05)

**Issues & Support**: Please use the [GitHub Issues](https://github.com/yourusername/ai-curve-fitting/issues) page for bug reports and feature requests.

---

<div align="center">
Made with ❤️ for advancing AI-driven mathematical optimization
</div>
