import pandas as pd
import os
import glob

# Directory containing the CSV files
input_dir = "Final_Cleaned_CSV_Output"

# List of specific files to process
target_files = [
    "final_cleaned_10_Valerie.csv",
    "final_cleaned_16_Debra.csv",
    "final_cleaned_17_Catherine.csv",
    "final_cleaned_18_Heather.csv",
    "final_cleaned_19_Ruth.csv",
    "final_cleaned_30_Melissa.csv",
    "final_cleaned_31_Steven.csv",
    "final_cleaned_40_Christopher.csv"
]

def determine_plan_level(row):
    """
    Determine the plan level based on the given conditions
    """
    plan_type = row['plan_type']
    level = row['level']
    deductible = row['family_medical_deductible']
    coinsurance = row['plan_coinsurance']
    
    # Condition 1: HMO Gold
    if plan_type == 'HMO' and level == 'gold':
        return 5
    
    # Conditions for HMO Silver
    if plan_type == 'HMO' and level == 'silver':
        # Condition 2: Deductible 0-499
        if 0 <= deductible <= 499:
            return 3
            
        # Condition 3: Deductible 500-1499
        if 500 <= deductible <= 1499:
            if coinsurance >= 40:
                return 3
            elif coinsurance >= 30:
                return 4
                
        # Condition 4: Deductible 1500-2999
        if 1500 <= deductible <= 2999:
            return 4
            
        # Condition 6: Deductible 5000+
        if deductible >= 5000:
            return 1
    
    # Condition 5: EPO or HMO Silver with deductible 3000-4999
    if (plan_type in ['EPO', 'HMO']) and level == 'silver':
        if 3000 <= deductible <= 4999:
            return 2
            
    return None  # Default return if no conditions match

def process_csv_file(file_path):
    """
    Process a single CSV file and add the plan_levels column
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Add plan_levels column
        df['plan_levels'] = df.apply(determine_plan_level, axis=1)
        
        # Save the modified DataFrame back to the same file
        df.to_csv(file_path, index=False)
        print(f"Successfully processed {os.path.basename(file_path)}")
        
    except Exception as e:
        print(f"Error processing {os.path.basename(file_path)}: {str(e)}")

def main():
    # Process each target file
    for filename in target_files:
        file_path = os.path.join(input_dir, filename)
        if os.path.exists(file_path):
            process_csv_file(file_path)
        else:
            print(f"File not found: {filename}")

if __name__ == "__main__":
    main() 