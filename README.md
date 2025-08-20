# Gas Break-Even Point Calculator

A comprehensive tool for analyzing the financial break-even points of hybrid and electric vehicles compared to gasoline cars in the Thai market. The calculator uses historical fuel price data, time-series forecasting, and interactive visualizations to provide data-driven vehicle purchase recommendations.

## 🚗 Features

- **Multi-Fuel Analysis**: Tracks prices for diesel, gasohol 91/95/E20/E85 from 2020-2024
- **Time-Series Forecasting**: Uses linear regression to predict future fuel prices
- **Break-Even Calculations**: Determines payback periods for hybrid and EV investments
- **Interactive Dashboard**: Comprehensive visualizations showing:
  - Historical fuel price trends
  - Break-even analysis charts
  - Operating cost comparisons
  - Monthly driving requirements
  - Annual savings projections
- **Data Scraping**: Automated collection of historical fuel prices from Bangchak website

## 📊 Sample Output

The tool generates a multi-panel dashboard showing:
- Fuel price trends across all types
- Break-even years for hybrid/EV vs gasoline
- Cost per kilometer comparisons
- Monthly driving requirements for 5-year payback
- Annual savings potential

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd gas-bep-calculator

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Dependencies
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib
- **Machine Learning**: scikit-learn
- **Web Scraping**: beautifulsoup4, requests

## 🚀 Usage

### Basic Analysis
```bash
# Activate virtual environment
source venv/bin/activate

# Run the analysis
python main.py
```

This will:
1. Load historical fuel data from `fuel_data/` directory
2. Display fuel price statistics (2020-2024)
3. Calculate break-even points using current assumptions
4. Generate an interactive dashboard

### Updating Fuel Data
```bash
# Run the scraper to get latest prices
python scraper.py
```

## 📈 Current Assumptions

The calculator uses the following default assumptions (easily modifiable in `calculate_break_even()`):

### Vehicle Prices (THB)
- Gasoline car: ฿990,000
- Hybrid car: ฿1,290,000  
- Electric car: ฿1,590,000

### Efficiency Ratings
- Gasoline: 12 km/L
- Hybrid: 25 km/L
- EV: 0.15 kWh/km

### Operating Costs
- Annual driving: 50,000 km
- Electricity rate: ฿4.30/kWh
- Maintenance (gasoline/hybrid): ฿10,000/year
- Maintenance (EV): ฿4,000/year

## 📁 Project Structure

```
gas-bep-calculator/
├── main.py              # Main analysis pipeline
├── scraper.py           # Fuel price data scraper
├── requirements.txt     # Python dependencies
├── fuel_data/          # Historical price data
│   ├── diesel/         # Diesel prices by year
│   ├── gasohol_91/     # Gasohol 91 prices
│   ├── gasohol_95/     # Gasohol 95 prices
│   ├── gasohol_e20/    # Gasohol E20 prices
│   └── gasohol_e85/    # Gasohol E85 prices
└── .github/
    └── copilot-instructions.md
```

## 🔧 Customization

### Modifying Assumptions
Edit the variables in `calculate_break_even()` function:

```python
# Car prices
gasoline_car_price = 990_000  # Your gasoline car price
hybrid_car_price = 1_290_000  # Your hybrid car price
ev_car_price = 1_590_000      # Your EV price

# Efficiency
gasoline_car_kpl = 12         # Your car's fuel efficiency
hybrid_car_kpl = 25          # Target hybrid efficiency
ev_car_kwh_per_km = 0.15     # Target EV efficiency

# Annual driving
km_per_year = 50000          # Your annual driving distance
```

### Adding New Fuel Types
1. Add fuel type to `oil_type_index` in `scraper.py`
2. Update `fuel_types` list in `load_fuel_data()`
3. Add color mapping in `visualize_fuel_prices_and_breakeven()`

## 📊 Data Sources

- **Fuel Prices**: [Bangchak Corporation](https://www.bangchak.co.th/en/oilprice/historical)
- **Price Range**: 2020-2024 historical data
- **Update Frequency**: Run scraper as needed for latest prices

## 🧮 Calculation Methodology

### Break-Even Formula
```
Break-even Years = Initial Price Difference / Annual Total Savings

Where:
Annual Total Savings = Fuel Savings + Maintenance Savings
Fuel Savings = (Gas Cost/km - Alternative Cost/km) × Annual KM
```

### Forecasting
- Uses linear regression on historical price data
- Predicts prices 365 days into the future
- Based on `time` feature (days since first data point)

## 📋 Requirements

See `requirements.txt` for full dependency list. Key packages:
- pandas==2.3.1
- matplotlib==3.10.5
- scikit-learn==1.7.1
- beautifulsoup4==4.13.4
- requests==2.32.5

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Update assumptions documentation
5. Submit a pull request

## 📄 License

This project is open source. See the LICENSE file for details.

## ⚠️ Disclaimers

- **Financial Advice**: This tool provides estimates only. Consult financial advisors for investment decisions.
- **Data Accuracy**: Fuel prices are scraped from public sources. Verify critical data independently.
- **Market Changes**: Calculations are based on current market conditions and may not reflect future changes.
- **Regional Variations**: Focused on Thai market conditions and fuel types.

## 📞 Support

For questions about:
- **Calculation methodology**: See code comments in `main.py`
- **Data sources**: Check scraper configuration in `scraper.py`
- **Technical issues**: Review error messages and check data file integrity

---

*Last updated: August 20, 2025*
