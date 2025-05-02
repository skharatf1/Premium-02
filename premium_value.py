import pandas as pd
import os
import glob

def get_employee_filename(first_name):
    """Find the matching CSV file for an employee based on their first name."""
    pattern = f"Final_Cleaned_CSV_Output/final_cleaned_*_{first_name}.csv"
    matching_files = glob.glob(pattern)
    if not matching_files:
        raise FileNotFoundError(f"No matching file found for employee {first_name}")
    return matching_files[0]

def main():
    # Read the scored employee plans file
    scored_df = pd.read_csv('scored_employee_plans.csv')
    
    # Create new columns for premiums
    for i in range(1, 7):
        scored_df[f'p{i}_premium'] = None
    
    # Process each employee
    for idx, row in scored_df.iterrows():
        first_name = row['firstName']
        employee_file = get_employee_filename(first_name)
        
        # Read the employee's plan file
        employee_df = pd.read_csv(employee_file)
        
        # For each plan (p1 to p6)
        for i in range(1, 7):
            plan_id = row[f'p{i}']
            if pd.isna(plan_id):  # Skip if no plan is assigned
                continue
                
            # Find the matching plan and get its premium
            matching_plan = employee_df[employee_df['id'] == plan_id]
            if not matching_plan.empty:
                premium = matching_plan['premium'].iloc[0]
                scored_df.at[idx, f'p{i}_premium'] = premium
    
    # Save the updated dataframe with a different filename
    output_file = 'employee_plans_with_premiums_output.csv'
    scored_df.to_csv(output_file, index=False)
    print(f"Processing complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()
