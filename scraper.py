import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import os

oil_type_index = {
    "gasohol_95": "Gasohol 95 S EVO",
    "gasohol_91": "Gasohol 91 S EVO",
    "diesel": "Hi Diesel S",
    "gasohol_e85": "Gasohol E85 S EVO",
    "gasohol_e20": "Gasohol E20 S EVO"
}

def scrape_fuel_prices(year, oil_types=None):
    """
    Scrapes historical fuel prices for a given year from the Bangchak website.
    
    Args:
        year (int): The year to scrape data for
        oil_types (list): List of oil types to scrape. If None, scrapes all available types.
    
    Returns:
        dict: Dictionary mapping oil_type to DataFrame
    """
    if oil_types is None:
        oil_types = list(oil_type_index.keys())
    
    url = f"https://www.bangchak.co.th/en/oilprice/historical?year={year}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for year {year}: {e}")
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table', {'class': 'table--historical-oilprice'})
    if not table:
        print(f"Could not find the price table for year {year}.")
        return {}

    if not isinstance(table, Tag):
        print(f"Could not find the price table for year {year}.")
        return {}

    thead = table.find('thead')
    if not isinstance(thead, Tag):
        print("Could not find the table head.")
        return {}
    
    header_rows = thead.find_all('tr')
    if len(header_rows) < 2:
        print("Unexpected header structure.")
        return {}

    headers = []
    # First header is 'Date' from the first row of thead
    first_header_row = header_rows[0]
    if isinstance(first_header_row, Tag):
        date_header = first_header_row.find('th')
        if isinstance(date_header, Tag):
            headers.append(date_header.text.strip())
        else:
            print("Could not find date header.")
            return {}
    else:
        print("First header row is not a Tag.")
        return {}

    # The rest of the headers are from the second row
    second_header_row = header_rows[1]
    if isinstance(second_header_row, Tag):
        price_headers = second_header_row.find_all('th')
        for th in price_headers:
            if isinstance(th, Tag):
                title_attr = th.get('title')
                if isinstance(title_attr, str):
                    headers.append(title_attr.strip())
                elif isinstance(title_attr, list):
                    headers.append(title_attr[0].strip())
    else:
        print("Second header row is not a Tag.")
        return {}

    # Find indices for all requested oil types
    oil_type_indices = {}
    for oil_type in oil_types:
        if oil_type not in oil_type_index:
            print(f"Unknown oil type: {oil_type}")
            continue
            
        header_name = oil_type_index[oil_type]
        try:
            price_index = headers.index(header_name)
            oil_type_indices[oil_type] = price_index
        except ValueError:
            print(f"'{header_name}' not found in table headers.")
            print(f"Available headers: {headers}")
            continue

    if not oil_type_indices:
        print("No valid oil types found in table headers.")
        return {}

    # Initialize data storage for each oil type
    oil_type_rows = {oil_type: [] for oil_type in oil_type_indices.keys()}
    
    tbody = table.find('tbody')
    if not isinstance(tbody, Tag):
        print("Could not find table body.")
        return {}

    for row in tbody.find_all('tr'):
        if not isinstance(row, Tag):
            continue
        
        date_col = row.find('th')
        if not isinstance(date_col, Tag):
            continue
        date = date_col.text.strip()

        cols = row.find_all('td')
        
        # Extract prices for each oil type
        for oil_type, price_index in oil_type_indices.items():
            if len(cols) > price_index - 1:
                price_col = cols[price_index - 1]
                if isinstance(price_col, Tag):
                    price = price_col.text.strip()
                    if price and price != '-':
                        try:
                            oil_type_rows[oil_type].append({'date': date, 'price': float(price)})
                        except ValueError:
                            # Skip invalid price values
                            continue

    # Create DataFrames and save files for each oil type
    results = {}
    for oil_type, rows in oil_type_rows.items():
        if not rows:
            print(f"No data found for {oil_type_index[oil_type]}.")
            results[oil_type] = pd.DataFrame()
            continue

        df = pd.DataFrame(rows)
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df = df.sort_values('date').reset_index(drop=True)
        
        # Create output directory for this oil type
        output_dir = f'fuel_data/{oil_type}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save to CSV
        df.to_csv(f'{output_dir}/{year}.csv', index=False)
        print(f"Successfully scraped and saved data for {oil_type} ({oil_type_index[oil_type]}) - {year}.")
        
        results[oil_type] = df
    
    return results

if __name__ == '__main__':
    years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    
    # You can specify which oil types to scrape, or leave as None to scrape all
    oil_types_to_scrape = None  # This will scrape all types
    # oil_types_to_scrape = ["gasohol_95", "gasohol_91", "diesel"]  # Or specify specific types
    
    for year in years:
        print(f"\nScraping data for year {year}...")
        results = scrape_fuel_prices(year, oil_types_to_scrape)
        print(f"Completed scraping for {year}. Found data for {len(results)} oil types.")
