# Data Documentation

## xy_data.csv

This file contains the observed (x, y) data points used for parameter estimation.

### Format

The CSV file contains two columns:
- `x`: X-coordinate values
- `y`: Y-coordinate values

### Provenance

The data represents a 2D trajectory with 1501 observations. When a 't' column is not present, the implementation assumes uniform spacing of t values between 6 and 60.

### Preprocessing

The data has been validated for:
- Missing values: None found
- Duplicates: None found
- Outliers: None removed

All data points are used in the optimization process.