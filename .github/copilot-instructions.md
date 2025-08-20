# Copilot Instructions for gas-bep-calculator

This project calculates break-even points for hybrid and electric vehicles vs gasoline cars using Thai historical fuel price data. It combines data scraping, time-series forecasting, and comprehensive visualization in a scientific computing workflow.

## Project Architecture

### Core Components
- `main.py`: Main analysis pipeline with data loading, forecasting, calculations, and visualization
- `scraper.py`: Web scraping tool for historical fuel prices from Bangchak website
- `fuel_data/`: Organized CSV storage with subdirectories for each fuel type (diesel, gasohol_91, gasohol_95, gasohol_e20, gasohol_e85)
- `requirements.txt`: Scientific Python stack (pandas, matplotlib, scikit-learn) + web scraping (beautifulsoup4, requests)

### Data Flow Pattern
1. **Load** → `load_fuel_data()` reads all fuel types from `fuel_data/{fuel_type}/{year}.csv`
2. **Analyze** → `calculate_break_even()` performs forecasting and financial calculations
3. **Visualize** → `visualize_fuel_prices_and_breakeven()` creates comprehensive dashboard

## Key Patterns & Conventions

### Fuel Data Structure
- Data organized by fuel type in separate directories: `fuel_data/{fuel_type}/{year}.csv`
- Each CSV has `date,price` columns with prices in Thai Baht per liter
- Time series spans 2020-2024, loaded via `range(2020, 2025)` in `load_fuel_data()`
- Data processing adds `time` column (days since first date) for linear regression

### Forecasting Approach
- Uses scikit-learn `LinearRegression` on time series data
- **Critical**: Always pass pandas DataFrame to `model.predict()`, not numpy arrays (avoids feature name warnings)
- Default fuel type for calculations: `gasohol_e20` (set in `calculate_break_even()`)

### Visualization Architecture
- Multi-panel dashboard using `matplotlib.gridspec` (3x2 grid layout)
- **Layout fix**: Use `plt.subplots_adjust()` instead of `plt.tight_layout()` to avoid axis compatibility warnings
- Color scheme consistently maps fuel types: diesel=#1f77b4, gasohol_91=#ff7f0e, etc.

## Development Workflow

### Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate  # Required on macOS due to externally-managed-environment
pip install -r requirements.txt
```

### Running Analysis
```bash
source venv/bin/activate && python main.py
```

### Key Assumptions to Modify
- Annual driving distance: `km_per_year = 30000` in `calculate_break_even()`
- Car prices: gasoline=800k, hybrid=1.2M, EV=1.5M THB
- Efficiency: gasoline=15 km/L, hybrid=25 km/L, EV=0.15 kWh/km
- Maintenance costs: defined in `calculate_break_even()` function

## Data Scraping Notes
- `scraper.py` targets Bangchak website with oil_type_index mapping
- Historical data URL pattern: `https://www.bangchak.co.th/en/oilprice/historical?year={year}`
- Run scraper separately to update fuel_data before analysis

---
_Last updated: August 20, 2025_
