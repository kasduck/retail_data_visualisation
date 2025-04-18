import pandas as pd
import numpy as np
import logging
from pathlib import Path
import sys
import psutil
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('data_cleanup.log')]
)

def check_system_resources():
    """Check available memory and log status."""
    memory = psutil.virtual_memory()
    available_gb = memory.available / (1024 ** 3)
    if available_gb < 0.5:  # Adjusted to 0.5GB for your 1.06GB system
        logging.warning(f"Very low memory available ({available_gb:.2f}GB). Proceeding with caution.")
    else:
        logging.info(f"Sufficient memory available ({available_gb:.2f}GB).")
    return available_gb

def load_and_validate_data(file_path):
    """Load Excel file with optimized memory usage."""
    try:
        logging.info(f"Loading data from {file_path}")
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        # Optimize dtypes to reduce memory usage
        dtypes = {'Quantity': 'int32', 'UnitPrice': 'float32', 'CustomerID': 'float64'}  # CustomerID as float to handle NA
        df = pd.read_excel(file_path, engine='openpyxl', dtype=dtypes)
        
        logging.info(f"Loaded data with shape: {df.shape}")
        if df.empty:
            raise ValueError("Loaded dataset is empty")
        if df.duplicated().any():
            logging.warning(f"Found {df.duplicated().sum()} duplicate rows; consider deduplication")
        
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise

def clean_data(df, remove_zero_price=True, deduplicate=True, outlier_cap=0.99):
    """Clean dataset with deduplication and outlier handling."""
    logging.info("Starting data cleaning process")
    initial_rows = len(df)
    
    # Deduplicate if enabled
    if deduplicate:
        initial_duplicates = df.duplicated().sum()
        df = df.drop_duplicates()
        logging.info(f"Removed {initial_duplicates} duplicate rows")
    
    # In-place filtering for valid quantities and prices
    mask = (df['Quantity'] >= 1) & (df['UnitPrice'] >= 0)
    df = df[mask].copy()
    
    # Drop rows with NA in key columns
    df = df.dropna(subset=['Quantity', 'UnitPrice'])
    
    if remove_zero_price:
        df = df[df['UnitPrice'] > 0]
        logging.info("Removed rows with zero UnitPrice")
    
    # Cap outliers at 99th percentile
    unitprice_cap = df['UnitPrice'].quantile(outlier_cap)
    df['UnitPrice'] = df['UnitPrice'].clip(upper=unitprice_cap)
    logging.info(f"Capped UnitPrice at {outlier_cap}th percentile: {unitprice_cap}")
    
    # Validate post-cleaning
    if (df['Quantity'] < 1).any() or (df['UnitPrice'] < 0).any():
        logging.warning("Invalid data detected post-cleaning")
    
    final_rows = len(df)
    logging.info(f"Removed {initial_rows - final_rows} rows during cleaning")
    logging.info(f"Cleaned data shape: {df.shape}")
    return df

def calculate_revenue(df):
    """Calculate revenue with vectorized operations and cap outliers."""
    logging.info("Calculating revenue")
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    
    revenue_cap = df['Revenue'].quantile(0.99)
    df['Revenue'] = df['Revenue'].clip(upper=revenue_cap)
    logging.info(f"Capped Revenue at 99th percentile: {revenue_cap}")
    
    if (df['Revenue'] < 0).any():
        logging.warning("Negative revenue detected")
    
    return df

def save_cleaned_data(df, output_path):
    """Save optimized CSV with compression and backup."""
    logging.info(f"Saving cleaned data to {output_path}")
    df['Quantity'] = df['Quantity'].astype('int32')
    df['UnitPrice'] = df['UnitPrice'].astype('float32')
    df['Revenue'] = df['Revenue'].astype('float32')
    
    backup_path = Path("backups") / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv.gz"
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(backup_path, index=False, compression='gzip')
    df.to_csv(output_path.with_suffix(''), index=False)  # Save as CSV without .gz for your Excel conversion
    logging.info(f"Data saved successfully with shape: {df.shape}")
    logging.info(f"Backup created at: {backup_path}")

def main():
    input_file = Path("Online_Retail_Data_Set.xlsx")
    output_file = Path("Online_Retail_Data_Set_Cleaned.csv")
    
    check_system_resources()
    
    try:
        df = load_and_validate_data(input_file)
        df_cleaned = clean_data(df, remove_zero_price=True, deduplicate=True, outlier_cap=0.99)
        df_with_revenue = calculate_revenue(df_cleaned)
        save_cleaned_data(df_with_revenue, output_file)
        
        logging.info("Validation check:")
        print(df_with_revenue.describe())
    except Exception as e:
        logging.error(f"Process failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
