import json
import csv
import os
import sys
from pathlib import Path

def flatten_json(nested_json, parent_key='', sep='/'):
    """Flatten nested JSON structure with special handling for lists of dictionaries"""
    items = []
    
    for key, value in nested_json.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        
        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key, sep=sep).items())
        elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
            # Handle list of dictionaries
            for i, item in enumerate(value):
                dict_num_key = f"{new_key}{sep}{i+1}"
                items.extend(flatten_json(item, dict_num_key, sep=sep).items())
        else:
            items.append((new_key, value))
            
    return dict(items)

def json_to_csv(json_file_path, csv_file_path):
    """Convert a single JSON file to CSV"""
    try:
        # Load JSON data
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        plans = data.get('plans', [])
        if not plans:
            print(f"No 'plans' key found or it's empty in {json_file_path}")
            return False
        
        # Flatten each plan
        flattened_plans = [flatten_json(plan) for plan in plans]
        
        # Get all unique keys
        all_keys = []
        for plan in flattened_plans:
            for key in plan.keys():
                if key not in all_keys:
                    all_keys.append(key)
        
        # Write to CSV
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=all_keys)
            writer.writeheader()
            writer.writerows(flattened_plans)
        
        print(f"Successfully converted {json_file_path} to {csv_file_path}")
        return True
    
    except Exception as e:
        print(f"Error processing {json_file_path}: {str(e)}")
        return False

def process_all_json_files():
    """Process all JSON files in the ResponseJSON folder"""
    # Create output directory if it doesn't exist
    output_dir = Path("CSV_Output")
    output_dir.mkdir(exist_ok=True)
    
    # Get all JSON files from ResponseJSON folder
    json_dir = Path("ResponseJSON")
    if not json_dir.exists():
        print("ResponseJSON folder not found!")
        return
    
    json_files = list(json_dir.glob("*.json"))
    if not json_files:
        print("No JSON files found in ResponseJSON folder!")
        return
    
    print(f"Found {len(json_files)} JSON files to process...")
    
    successful = 0
    failed = 0
    
    for json_file in json_files:
        # Create corresponding CSV filename
        csv_filename = json_file.stem + ".csv"
        csv_path = output_dir / csv_filename
        
        # Convert the file
        if json_to_csv(str(json_file), str(csv_path)):
            successful += 1
        else:
            failed += 1
    
    print("\nConversion Summary:")
    print(f"Successfully converted: {successful} files")
    print(f"Failed conversions: {failed} files")
    print(f"CSV files have been saved to the {output_dir} folder")

if __name__ == "__main__":
    process_all_json_files() 