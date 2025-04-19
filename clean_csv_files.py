import pandas as pd
import os
from pathlib import Path
import re

# Define input and output directories
input_dir = "Cleaned_CSV_Output"  # Changed to read from Cleaned_CSV_Output
output_dir = "Final_Cleaned_CSV_Output"  # New output directory for final cleaned files

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def extract_dollar_amount(value):
    """
    Extracts the dollar amount from a given string.
    Returns 0 if no match is found or if the input is null/empty.
    """
    if pd.isna(value) or not value:
        return 0
    match = re.search(r'\$?([\d,]+)', str(value))
    if match:
        amount_str = match.group(1).replace(',', '')
        try:
            return int(amount_str)
        except ValueError:
            return 0
    return 0

def extract_percentage(value):
    """
    Extracts the percentage from a given string.
    Returns 0 if no match is found or if the input is null/empty.
    """
    if pd.isna(value) or not value:
        return 0
    match = re.search(r'(\d+)%', str(value))
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return 0
    return 0

def clean_csv_file(input_file):
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # Process dollar amount columns
        dollar_columns = ['individual_medical_deductible', 'family_medical_deductible', 
                         'child_eyewear', 'child_eye_exam', 'child_dental']
        for col in dollar_columns:
            if col in df.columns:
                df[col] = df[col].apply(extract_dollar_amount)
        
        # Process percentage column
        if 'plan_coinsurance' in df.columns:
            df['plan_coinsurance'] = df['plan_coinsurance'].apply(extract_percentage)
        
        # Create output filename
        output_file = os.path.join(output_dir, f"final_{os.path.basename(input_file)}")
        
        # Save the cleaned data
        df.to_csv(output_file, index=False)
        print(f"Processed {input_file} -> {output_file}")
        print(f"Rows in output file: {len(df)}")
        
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")

def main():
    # Get all CSV files from input directory
    csv_files = list(Path(input_dir).glob("*.csv"))
    print(f"Found {len(csv_files)} CSV files to process")
    
    # Process each file
    for csv_file in csv_files:
        clean_csv_file(str(csv_file))
    
    print("Processing complete!")

if __name__ == "__main__":
    main() 