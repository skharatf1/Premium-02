import pandas as pd
import os

# List of specific files to process
files_to_process = [
    'final_cleaned_3_Katherine.csv',
    'final_cleaned_7_Jessica.csv',
    'final_cleaned_9_Robert.csv',
    'final_cleaned_10_Valerie.csv',
    'final_cleaned_16_Debra.csv',
    'final_cleaned_17_Catherine.csv',
    'final_cleaned_18_Heather.csv',
    'final_cleaned_19_Ruth.csv',
    'final_cleaned_30_Melissa.csv',
    'final_cleaned_31_Steven.csv',
    'final_cleaned_40_Christopher.csv',
    'final_cleaned_51_John.csv',
    'final_cleaned_52_Emily.csv',
    'final_cleaned_53_Mark.csv',
    'final_cleaned_55_David.csv',
    'final_cleaned_56_Laura.csv',
    'final_cleaned_57_Alex.csv'
]

# Directory containing the CSV files
input_dir = 'Final_Cleaned_CSV_Output'

# Read the assignment file to get age information
assignment_df = pd.read_csv('Assignment_2.csv')

# Initialize an empty list to store results
results = []

# Process each file
for file_name in files_to_process:
    file_path = os.path.join(input_dir, file_name)
    
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Extract employee ID from filename
        employee_id = int(file_name.split('_')[2])
        
        # Get employee's age from assignment file
        employee_age = assignment_df[assignment_df['employeeId'] == employee_id]['age'].iloc[0]
        
        # Initialize a dictionary to store the results for this file
        file_result = {'file_name': file_name}
        
        # Process each plan level (1-5)
        for level in range(1, 6):
            # Filter data for current level
            level_data = df[df['plan_levels'] == level]
            
            if not level_data.empty:
                # Find the plan with lowest premium
                min_premium_row = level_data.loc[level_data['premium'].idxmin()]
                file_result[f'plan_level_{level}_id'] = min_premium_row['id']
            else:
                # If no plans exist for this level, leave it blank
                file_result[f'plan_level_{level}_id'] = ''
        
        # Add p6 column based on age and HSA eligibility
        if employee_age < 40:
            # Find HSA eligible plans with lowest premium
            hsa_eligible_plans = df[df['hsa_eligible'] == True]
            if not hsa_eligible_plans.empty:
                min_premium_hsa = hsa_eligible_plans.loc[hsa_eligible_plans['premium'].idxmin()]
                file_result['p6'] = min_premium_hsa['id']
            else:
                file_result['p6'] = ''
        else:
            file_result['p6'] = ''
        
        # Add the results for this file to our list
        results.append(file_result)
        
    except Exception as e:
        print(f"Error processing {file_name}: {str(e)}")

# Convert results to DataFrame
summary_df = pd.DataFrame(results)

# Ensure all columns exist (in case some files are missing certain levels)
for level in range(1, 6):
    col_name = f'plan_level_{level}_id'
    if col_name not in summary_df.columns:
        summary_df[col_name] = ''

# Save the summary to CSV
output_file = 'lowest_premium_plan_ids_summary.csv'
summary_df.to_csv(output_file, index=False)
print(f"Summary saved to {output_file}")

# Merge with Assignment_2.csv
try:
    # Read the lowest premium summary file
    premium_summary_df = pd.read_csv('lowest_premium_plan_ids_summary.csv')
    
    # Extract employeeId from file_name in premium_summary_df
    premium_summary_df['employeeId'] = premium_summary_df['file_name'].str.extract(r'final_cleaned_(\d+)_').astype(int)
    
    # Merge the dataframes on employeeId
    merged_df = pd.merge(assignment_df, premium_summary_df, on='employeeId', how='left')
    
    # Save the merged result to a new CSV file
    merged_output_file = 'merged_employee_plans.csv'
    merged_df.to_csv(merged_output_file, index=False)
    print(f"Merged data saved to {merged_output_file}")
except Exception as e:
    print(f"Error during merge operation: {str(e)}")
