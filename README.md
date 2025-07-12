# Ukraine Support Gravity Analysis

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for analyzing and visualizing the gravitational center of European Union (EU) assistance to Ukraine. This project applies economic gravity models as a novel geopolitical analysis tool, using KMeans clustering to determine the optimal center of gravity for EU assistance distribution. The results are visualized on interactive maps using Matplotlib and Basemap.

## Features

- **Gravity Center Analysis**: Uses weighted KMeans clustering to find the optimal center of EU assistance
- **Concentricity Visualization**: Plots concentric circles around Moscow to analyze geographic relationships
- **Data Processing**: Automated extraction and processing of support tracker data
- **Professional Visualizations**: High-quality map plots with customizable parameters

## Project Structure

```
ukraine_support_gravity/
├── ukraine_support_gravity/          # Main package
│   ├── __init__.py                   # Package initialization
│   ├── gravity_analysis.py           # Core analysis functions
│   ├── data/                         # Data files
│   │   ├── ukrainesupporttracker.xlsx
│   │   ├── country-list.csv
│   │   └── data.parquet
│   └── plots/                        # Generated visualizations
├── main.py                           # Main entry point
├── requirements.txt                  # Dependencies
├── pyproject.toml                    # Package configuration
└── README.md                         # This file
```
## Installation

### Option 1: Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/ukraine-support-gravity.git
cd ukraine-support-gravity

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using conda

```bash
# Clone the repository
git clone https://github.com/your-username/ukraine-support-gravity.git
cd ukraine-support-gravity

# Create and activate conda environment
conda env create -f UkraineGravity.yml
conda activate ukraine-support-gravity
```

### Option 3: Development Installation

```bash
# Clone and install in development mode
git clone https://github.com/your-username/ukraine-support-gravity.git
cd ukraine-support-gravity
pip install -e .
```

## Quick Start

```python
from ukraine_support_gravity import run_concentricity, run_support_gravity_center

# Run concentricity analysis (default)
run_concentricity()

# Run gravity center analysis
run_support_gravity_center()
```

Or use the command line:

```bash
python main.py
```

## Usage

The package provides three main analysis functions:

### 1. Concentricity Analysis
```python
from ukraine_support_gravity import run_concentricity

# Run with default parameters (10 circles, 500km distance)
run_concentricity()

# Customize parameters
run_concentricity(num_circles=15, circle_distance=300.0)
```

### 2. Gravity Center Analysis
```python
from ukraine_support_gravity import run_support_gravity_center

run_support_gravity_center()
```

### 3. Data Extraction
```python
from ukraine_support_gravity import extract_support_gravity_center

# Extract and process data from Excel files
extract_support_gravity_center()
```

## Methodology

This project applies **economic gravity models** to geopolitical analysis - a novel approach to understanding international aid distribution patterns.

### Theoretical Foundation

The gravity model, originally developed for trade analysis, suggests that economic interactions between two entities are proportional to their economic sizes and inversely proportional to the distance between them. This project adapts this concept to analyze EU assistance patterns to Ukraine, treating aid as a form of economic "gravity" that can be spatially analyzed.

### Mathematical Approach

**Gravity Center Calculation:**
The optimal assistance center is computed using weighted K-means clustering where:
- **Features**: Normalized latitude and longitude coordinates (shifted by +90° and +180° respectively)
- **Weights**: Total assistance amounts as percentage of 2021 GDP
- **Algorithm**: K-means with k=1 to find the single optimal point
- **Output**: Geographic coordinates representing the "center of gravity" for EU assistance

**Distance Analysis:**
Concentric circle analysis around Moscow uses:
- **Base coordinates**: Moscow (55.7558°N, 37.6173°E)
- **Circle spacing**: Configurable distance (default 500km)
- **Calculation**: Great circle distance approximation using lat/lon conversion

### Processing Pipeline

1. **Data Extraction**: 
   - Parse Ukraine Support Tracker Excel data (Sheet: "Country Summary (€)")
   - Extract country names, assistance amounts, and GDP percentages
   - Geocode country locations using Nominatim API

2. **Data Cleaning**:
   - Remove entries with zero assistance
   - Filter out aggregate EU entries (no geographic location)
   - Manual correction for geocoding anomalies (e.g., Greece coordinates)

3. **Weighted Clustering**:
   - Apply coordinate normalization for KMeans compatibility
   - Use assistance amounts as sample weights
   - Extract optimal point and denormalize coordinates

4. **Visualization**:
   - Plot countries sized by assistance magnitude
   - Color-code by assistance ranking
   - Draw connections from countries to gravity center
   - Overlay concentric distance circles from reference points (Moscow, Kyiv)

### Novel Contributions

- **First application** of economic gravity models to geopolitical aid analysis
- **Spatial clustering** approach to understanding assistance distribution patterns
- **Quantitative framework** for analyzing geopolitical positioning through aid flows
- **Visual methodology** for comparing assistance patterns against geographic references

## Data Sources

- **Ukraine Support Tracker**: [Kiel Institute for the World Economy](https://www.ifw-kiel.de/topics/war-against-ukraine/ukraine-support-tracker/)
- **Country Capitals**: [Country List CSV](https://github.com/icyrockcom/country-capitals/blob/master/data/country-list.csv)
- **SIPRI Military Expenditure Data**: 1949-2022 data included in repository

## Output Files

The analysis generates several visualization files in `ukraine_support_gravity/plots/`:

- `CapitalsMoscowCircle.png`: Concentricity analysis showing EU capitals with concentric circles around Moscow
- `UkraineSupportGravityPlot.png`: Gravity center analysis with weighted clustering visualization

## Dependencies

- Python 3.9+
- numpy >= 1.26.4
- pandas >= 2.2.0
- matplotlib >= 3.8.0
- scikit-learn >= 1.5.2
- geopy >= 2.4.1
- basemap >= 1.3.6
- openpyxl >= 3.1.0

## Contributing

This project represents a novel application of economic gravity models to geopolitical analysis. Contributions and suggestions for improvements are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Kiel Institute for maintaining the Ukraine Support Tracker
- ChatGPT and Perplexity.ai assisted in documentation and development
- Basemap and matplotlib communities for excellent visualization tools

## Changelog

### Version 1.0.0
- ✅ **Security**: Updated scikit-learn and all dependencies to latest secure versions
- ✅ **Structure**: Reorganized into proper Python package structure
- ✅ **Documentation**: Comprehensive README with installation and usage instructions
- ✅ **Configuration**: Added pyproject.toml and proper .gitignore
- ✅ **Path Handling**: Fixed file paths using pathlib for cross-platform compatibility
- 📈 **Enhancement**: Added proper error handling and type hints
- 🎨 **Visualization**: Improved plot organization and output management