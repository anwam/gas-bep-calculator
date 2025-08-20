# -*- coding: utf-8 -*-
"""
This program calculates the break-even point for a hybrid car compared to a gasoline car.
It also provides an equation to help you determine the monthly mileage needed to justify the purchase of a hybrid or EV.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

def load_fuel_data():
    """Loads historical fuel price data from CSV files for all fuel types."""
    data_dir = 'fuel_data'
    fuel_types = ['diesel', 'gasohol_91', 'gasohol_95', 'gasohol_e20', 'gasohol_e85']
    all_fuel_data = {}
    
    for fuel_type in fuel_types:
        fuel_type_data = []
        fuel_type_dir = os.path.join(data_dir, fuel_type)
        
        if os.path.exists(fuel_type_dir):
            # Load data from 2020 to 2024
            for year in range(2020, 2025):
                file_path = os.path.join(fuel_type_dir, f'{year}.csv')
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path)
                    fuel_type_data.append(df)
        
        if fuel_type_data:
            fuel_df = pd.concat(fuel_type_data, ignore_index=True)
            fuel_df['date'] = pd.to_datetime(fuel_df['date'])
            fuel_df = fuel_df.sort_values('date').reset_index(drop=True)
            fuel_df['time'] = (fuel_df['date'] - fuel_df['date'].min()).dt.days
            fuel_df['fuel_type'] = fuel_type
            all_fuel_data[fuel_type] = fuel_df
    
    return all_fuel_data

def visualize_fuel_prices_and_breakeven(all_fuel_data, break_even_results):
    """Visualizes historical fuel prices and break-even analysis in a comprehensive dashboard."""
    if not all_fuel_data:
        print("No fuel price data to visualize.")
        return
        
    # Create a figure with subplots - adjusted layout for more charts
    fig = plt.figure(figsize=(20, 16))
    
    # Create a grid layout: 4 rows, 2 columns for better spacing
    gs = fig.add_gridspec(4, 2, height_ratios=[2, 1, 1, 1.2], width_ratios=[1, 1], 
                         hspace=0.4, wspace=0.3)
    
    # Main fuel price chart (top row, spanning both columns)
    ax1 = fig.add_subplot(gs[0, :])
    
    # Define colors for each fuel type
    colors = {
        'diesel': '#1f77b4',
        'gasohol_91': '#ff7f0e', 
        'gasohol_95': '#2ca02c',
        'gasohol_e20': '#d62728',
        'gasohol_e85': '#9467bd'
    }
    
    # Define labels for better readability
    labels = {
        'diesel': 'Diesel',
        'gasohol_91': 'Gasohol 91',
        'gasohol_95': 'Gasohol 95', 
        'gasohol_e20': 'Gasohol E20',
        'gasohol_e85': 'Gasohol E85'
    }
    
    for fuel_type, df in all_fuel_data.items():
        ax1.plot(df['date'], df['price'], 
                label=labels.get(fuel_type, fuel_type),
                color=colors.get(fuel_type, 'black'),
                linewidth=2)
    
    ax1.set_title('Thai Fuel Prices by Type (2020-2024)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Year', fontsize=10)
    ax1.set_ylabel('Price (THB per Liter)', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left', fontsize=9)
    
    # Break-even summary chart (second row, left)
    ax2 = fig.add_subplot(gs[1, 0])
    
    vehicles = ['Hybrid', 'EV']
    break_even_years = [
        break_even_results['break_even']['hybrid_years'],
        break_even_results['break_even']['ev_years']
    ]
    
    # Cap the years for better visualization
    capped_years = [min(year, 15) for year in break_even_years]
    colors_bar = ['#2ca02c', '#1f77b4']
    
    bars = ax2.bar(vehicles, capped_years, color=colors_bar, alpha=0.7)
    ax2.set_title(f'Break-Even Analysis ({break_even_results["assumptions"]["km_per_year"]:,} km/year)', 
                  fontsize=12, fontweight='bold')
    ax2.set_ylabel('Years to Break Even', fontsize=9)
    ax2.set_ylim(0, max(capped_years) * 1.2)
    
    # Add value labels on bars
    for i, (bar, year) in enumerate(zip(bars, break_even_years)):
        height = bar.get_height()
        label = f'{year:.1f}' if year < 100 else '15+'
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                label, ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Cost comparison chart (second row, right)
    ax4 = fig.add_subplot(gs[1, 1])
    
    cost_categories = ['Gasoline', 'Hybrid', 'EV']
    costs_per_km = [
        break_even_results['costs']['gasoline_cost_per_km'],
        break_even_results['costs']['hybrid_cost_per_km'],
        break_even_results['costs']['ev_cost_per_km']
    ]
    
    bars_cost = ax4.bar(cost_categories, costs_per_km, color=['#ff7f0e', '#2ca02c', '#1f77b4'], alpha=0.7)
    ax4.set_title('Fuel/Energy Cost per KM', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Cost (THB/km)', fontsize=9)
    
    # Add value labels on bars
    for bar, cost in zip(bars_cost, costs_per_km):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'฿{cost:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=8)
    
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Monthly KM needed chart (third row, left)
    ax5 = fig.add_subplot(gs[2, 0])
    
    km_categories = ['Hybrid', 'EV']
    monthly_km_needed = [
        break_even_results['break_even']['hybrid_monthly_km_needed'],
        break_even_results['break_even']['ev_monthly_km_needed']
    ]
    
    bars_km = ax5.bar(km_categories, monthly_km_needed, color=['#2ca02c', '#1f77b4'], alpha=0.7)
    ax5.set_title('Monthly KM Needed (5-year plan)', fontsize=12, fontweight='bold')
    ax5.set_ylabel('KM per Month', fontsize=9)
    
    # Add value labels on bars
    for bar, km in zip(bars_km, monthly_km_needed):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height + max(monthly_km_needed) * 0.02,
                f'{km:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    ax5.grid(True, alpha=0.3, axis='y')
    
    # Annual savings chart (third row, right)
    ax6 = fig.add_subplot(gs[2, 1])
    
    savings_categories = ['Hybrid', 'EV']
    annual_savings = [
        break_even_results['break_even']['hybrid_annual_savings'],
        break_even_results['break_even']['ev_annual_savings']
    ]
    
    bars_savings = ax6.bar(savings_categories, annual_savings, color=['#2ca02c', '#1f77b4'], alpha=0.7)
    ax6.set_title('Annual Savings vs Gasoline', fontsize=12, fontweight='bold')
    ax6.set_ylabel('Savings (THB/year)', fontsize=9)
    
    # Add value labels on bars
    for bar, savings in zip(bars_savings, annual_savings):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height + max(annual_savings) * 0.02,
                f'฿{savings:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=8)
    
    ax6.grid(True, alpha=0.3, axis='y')
    
    # Summary text (bottom row, spanning both columns)
    ax3 = fig.add_subplot(gs[3, :])
    ax3.axis('off')
    
    # Create more compact summary text in two columns
    summary_left = f"""ASSUMPTIONS & COSTS:
• Annual driving: {break_even_results['assumptions']['km_per_year']:,} km/year
• Gasoline car: {break_even_results['assumptions']['gasoline_car_kpl']} km/L
• Hybrid car: {break_even_results['assumptions']['hybrid_car_kpl']} km/L  
• EV: {break_even_results['assumptions']['ev_kwh_per_km']} kWh/km
• Electricity: ฿{break_even_results['assumptions']['electricity_price_per_kwh']:.2f}/kWh

ADDITIONAL INITIAL COSTS:
• Hybrid: ฿{break_even_results['costs']['hybrid_price_difference']:,.0f}
• EV: ฿{break_even_results['costs']['ev_price_difference']:,.0f}"""
    
    summary_right = f"""BREAK-EVEN ANALYSIS ({break_even_results['assumptions']['km_per_year']:,} km/year):
• Hybrid break-even: {break_even_results['break_even']['hybrid_years']:.1f} years
• EV break-even: {break_even_results['break_even']['ev_years']:.1f} years
• Hybrid annual savings: ฿{break_even_results['break_even']['hybrid_annual_savings']:,.0f}
• EV annual savings: ฿{break_even_results['break_even']['ev_annual_savings']:,.0f}

MONTHLY DRIVING NEEDED (5-year plan):
• Hybrid: {break_even_results['break_even']['hybrid_monthly_km_needed']:,.0f} km/month
• EV: {break_even_results['break_even']['ev_monthly_km_needed']:,.0f} km/month"""
    
    # Place text in two columns
    ax3.text(0.02, 0.95, summary_left, transform=ax3.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", 
             facecolor="lightblue", alpha=0.3))
    
    ax3.text(0.52, 0.95, summary_right, transform=ax3.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", 
             facecolor="lightgreen", alpha=0.3))
    
    # Use subplots_adjust instead of tight_layout to avoid the warning
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, hspace=0.3, wspace=0.3)
    plt.show()

def display_fuel_statistics(all_fuel_data):
    """Display statistics for all fuel types."""
    print("--- Fuel Price Statistics (2020-2024) ---")
    for fuel_type, df in all_fuel_data.items():
        if not df.empty:
            avg_price = df['price'].mean()
            min_price = df['price'].min()
            max_price = df['price'].max()
            latest_price = df.iloc[-1]['price']
            
            fuel_name = fuel_type.replace('_', ' ').title()
            print(f"{fuel_name}:")
            print(f"  Latest Price: ฿{latest_price:.2f}/L")
            print(f"  Average: ฿{avg_price:.2f}/L")
            print(f"  Range: ฿{min_price:.2f} - ฿{max_price:.2f}/L")
            print()

def forecast_fuel_price(all_fuel_data, fuel_type='gasohol_95'):
    """Forecasts fuel price for the next year for a specific fuel type."""
    if not all_fuel_data or fuel_type not in all_fuel_data:
        print(f"Not enough data to forecast fuel price for {fuel_type}. Returning default price.")
        return 32.55

    df = all_fuel_data[fuel_type]
    if df.empty or len(df) < 2:
        print(f"Not enough data to forecast fuel price for {fuel_type}. Returning current average.")
        return df['price'].mean() if not df.empty else 32.55

    X = df[['time']]
    y = df['price']
    
    model = LinearRegression()
    model.fit(X, y)
    
    future_time = df['time'].max() + 365
    # Use pandas DataFrame to maintain feature names consistency
    future_df = pd.DataFrame([[future_time]], columns=['time'])
    forecasted_price = model.predict(future_df)[0]
    return forecasted_price

def forecast_car_price(current_price, years=1, depreciation_rate=0.05):
    """Forecasts car price based on a simple depreciation model."""
    return current_price * ((1 - depreciation_rate) ** years)

def calculate_break_even(all_fuel_data):
    """
    Calculates the break-even point for a hybrid car.
    Returns a dictionary with all calculation results.
    """

    # --- User Input ---
    # Car Prices (in Thai Baht)
    gasoline_car_price = 990_000  # Example price for a new gasoline car
    hybrid_car_price = 1_290_000   # Example price for a new hybrid car
    ev_car_price = 1_590_000       # Example price for a new electric car

    # Fuel & Energy Prices
    forecasted_gasoline_price = forecast_fuel_price(all_fuel_data, 'gasohol_95')
    electricity_price_per_kwh = 4.30    # Average household electricity rate in Thailand

    # Forecasted Car Prices for next year
    gasoline_car_price_future = forecast_car_price(gasoline_car_price)
    hybrid_car_price_future = forecast_car_price(hybrid_car_price)
    ev_car_price_future = forecast_car_price(ev_car_price)


    # Fuel & Energy Efficiency
    gasoline_car_kpl = 12  # Kilometers per liter for the gasoline car
    hybrid_car_kpl = 25   # Kilometers per liter for the hybrid car
    ev_car_kwh_per_km = 0.15 # Kilowatt-hours per kilometer for the EV

    # Annual Maintenance Cost
    gasoline_car_maintenance_annual = 10_000
    hybrid_car_maintenance_annual = 10_000
    ev_car_maintenance_annual = 4_000

    # --- Calculations ---

    # Price Differences
    hybrid_price_difference = hybrid_car_price_future - gasoline_car_price_future
    ev_price_difference = ev_car_price_future - gasoline_car_price_future

    # Cost per Kilometer (Fuel/Energy)
    gasoline_cost_per_km_fuel = forecasted_gasoline_price / gasoline_car_kpl
    hybrid_cost_per_km_fuel = forecasted_gasoline_price / hybrid_car_kpl
    ev_cost_per_km_energy = electricity_price_per_kwh * ev_car_kwh_per_km

    # Savings per kilometer (vs. gasoline car)
    hybrid_savings_per_km = gasoline_cost_per_km_fuel - hybrid_cost_per_km_fuel
    ev_savings_per_km = gasoline_cost_per_km_fuel - ev_cost_per_km_energy

    # Annual cost savings (vs. gasoline car)
    hybrid_annual_maintenance_savings = gasoline_car_maintenance_annual - hybrid_car_maintenance_annual
    ev_annual_maintenance_savings = gasoline_car_maintenance_annual - ev_car_maintenance_annual

    # Break-Even Point (in Kilometers)
    # BEP_km = (Price_Diff) / (Savings_per_km + Annual_Maintenance_Savings / Annual_KM)
    # This can be simplified by looking at total cost over time.
    # Let's adjust the logic to be clearer.
    # Total cost = Car Price + (Cost_per_km * Total_KM) + (Annual_Maintenance * Years)
    # We are looking for the Total_KM where costs are equal.
    # Let's consider the total cost over the car's lifetime.
    # A simpler approach is to find the annual mileage needed to make up for the price difference.

    # Let's calculate the break-even point in years, assuming a certain annual mileage.
    km_per_year = 50000 # Assumed annual driving distance

    hybrid_annual_fuel_savings = hybrid_savings_per_km * km_per_year
    hybrid_total_annual_savings = hybrid_annual_fuel_savings + hybrid_annual_maintenance_savings
    hybrid_break_even_years = hybrid_price_difference / hybrid_total_annual_savings if hybrid_total_annual_savings > 0 else float('inf')

    ev_annual_fuel_savings = ev_savings_per_km * km_per_year
    ev_total_annual_savings = ev_annual_fuel_savings + ev_annual_maintenance_savings
    ev_break_even_years = ev_price_difference / ev_total_annual_savings if ev_total_annual_savings > 0 else float('inf')


    # --- Output ---
    print("--- Forecasts ---")
    # Show forecasts for all fuel types
    for fuel_type in all_fuel_data.keys():
        forecasted_price = forecast_fuel_price(all_fuel_data, fuel_type)
        fuel_name = fuel_type.replace('_', ' ').title()
        print(f"Forecasted {fuel_name} Price next year: ฿{forecasted_price:,.2f} / liter")
    
    print(f"\nForecasted Gasoline Car Price next year: ฿{gasoline_car_price_future:,.2f}")
    print(f"Forecasted Hybrid Car Price next year: ฿{hybrid_car_price_future:,.2f}")
    print(f"Forecasted EV Car Price next year: ฿{ev_car_price_future:,.2f}\n")


    print(f"--- Break-Even Analysis (Based on Forecasts & {km_per_year:,} km/year) ---")
    print(f"Initial additional cost for Hybrid: ฿{hybrid_price_difference:,.2f}")
    print(f"Initial additional cost for EV: ฿{ev_price_difference:,.2f}\n")

    print(f"Gasoline Car Cost per KM (Fuel only): ฿{gasoline_cost_per_km_fuel:.2f}")
    print(f"Hybrid Car Cost per KM (Fuel only): ฿{hybrid_cost_per_km_fuel:.2f}")
    print(f"EV Car Cost per KM (Energy only): ฿{ev_cost_per_km_energy:.2f}\n")

    print(f"Hybrid total annual savings (fuel + maintenance): ฿{hybrid_total_annual_savings:,.2f}")
    print(f"EV total annual savings (fuel + maintenance): ฿{ev_total_annual_savings:,.2f}\n")

    print(f"You need to own the Hybrid for approximately {hybrid_break_even_years:.1f} years to break even.")
    print(f"You need to own the EV for approximately {ev_break_even_years:.1f} years to break even.\n")

    # --- Monthly Mileage Suggestion ---
    print("--- Monthly Mileage Equation & Suggestion ---")
    print("To determine if a hybrid or EV is worth it for you, consider how many years you are willing to wait to break even.\n")

    years_to_own = 5 # Example: You plan to own the car for 5 years
    
    # Calculate the required annual savings to break even in `years_to_own`
    hybrid_required_annual_savings = hybrid_price_difference / years_to_own
    ev_required_annual_savings = ev_price_difference / years_to_own

    # Calculate the required annual mileage
    hybrid_required_annual_km = (hybrid_required_annual_savings - hybrid_annual_maintenance_savings) / hybrid_savings_per_km if hybrid_savings_per_km > 0 else float('inf')
    ev_required_annual_km = (ev_required_annual_savings - ev_annual_maintenance_savings) / ev_savings_per_km if ev_savings_per_km > 0 else float('inf')

    print(f"To break even on a Hybrid in {years_to_own} years, you should drive at least: {hybrid_required_annual_km / 12:,.0f} km/month")
    print(f"To break even on an EV in {years_to_own} years, you should drive at least: {ev_required_annual_km / 12:,.0f} km/month")

    # Return all calculation results for visualization
    return {
        'forecasts': {
            'fuel_prices': {fuel_type: forecast_fuel_price(all_fuel_data, fuel_type) 
                           for fuel_type in all_fuel_data.keys()},
            'gasoline_car_price': gasoline_car_price_future,
            'hybrid_car_price': hybrid_car_price_future,
            'ev_car_price': ev_car_price_future,
            'gasoline_fuel_price': forecasted_gasoline_price
        },
        'costs': {
            'hybrid_price_difference': hybrid_price_difference,
            'ev_price_difference': ev_price_difference,
            'gasoline_cost_per_km': gasoline_cost_per_km_fuel,
            'hybrid_cost_per_km': hybrid_cost_per_km_fuel,
            'ev_cost_per_km': ev_cost_per_km_energy,
            'hybrid_savings_per_km': hybrid_savings_per_km,
            'ev_savings_per_km': ev_savings_per_km
        },
        'break_even': {
            'hybrid_years': hybrid_break_even_years,
            'ev_years': ev_break_even_years,
            'hybrid_annual_savings': hybrid_total_annual_savings,
            'ev_annual_savings': ev_total_annual_savings,
            'hybrid_monthly_km_needed': hybrid_required_annual_km / 12,
            'ev_monthly_km_needed': ev_required_annual_km / 12,
            'years_to_own': years_to_own
        },
        'assumptions': {
            'km_per_year': km_per_year,
            'gasoline_car_kpl': gasoline_car_kpl,
            'hybrid_car_kpl': hybrid_car_kpl,
            'ev_kwh_per_km': ev_car_kwh_per_km,
            'electricity_price_per_kwh': electricity_price_per_kwh
        }
    }


if __name__ == '__main__':
    all_fuel_data = load_fuel_data()
    display_fuel_statistics(all_fuel_data)
    break_even_results = calculate_break_even(all_fuel_data)
    visualize_fuel_prices_and_breakeven(all_fuel_data, break_even_results)
