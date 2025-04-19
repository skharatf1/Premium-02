import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_lowest_premium_plan(employee_plans, employee_csv_path):
    """
    Find the plan ID with the lowest premium from the employee's CSV file.
    
    Args:
        employee_plans (list): List of plan IDs to check
        employee_csv_path (str): Path to the employee's CSV file
        
    Returns:
        str: Plan ID with the lowest premium, or None if no valid plans found
    """
    try:
        # Read the employee's CSV file
        df = pd.read_csv(employee_csv_path)
        
        # Filter for the plans we're interested in
        valid_plans = df[df['id'].isin(employee_plans)]
        
        if valid_plans.empty:
            logging.warning(f"No matching plans found in {employee_csv_path}")
            return None
            
        # Find the plan with the lowest premium
        lowest_premium_plan = valid_plans.loc[valid_plans['premium'].idxmin()]
        return lowest_premium_plan['id']
        
    except Exception as e:
        logging.error(f"Error processing {employee_csv_path}: {str(e)}")
        return None

def find_highest_score_plan(row):
    """
    Find the plan ID corresponding to the highest score among s1-s6.
    
    Args:
        row (pd.Series): Row from the main dataframe
        
    Returns:
        str: Plan ID with the highest score, or None if no valid scores found
    """
    try:
        # Get scores and corresponding plan IDs
        scores = {f's{i}': row[f's{i}'] for i in range(1, 7) if pd.notna(row[f's{i}'])}
        plans = {f's{i}': row[f'p{i}'] for i in range(1, 7) if pd.notna(row[f'p{i}'])}
        
        if not scores:
            logging.warning(f"No valid scores found for employee {row['firstName']}")
            return None
            
        # Find the highest score
        highest_score_key = max(scores, key=scores.get)
        
        # Get the corresponding plan ID
        return plans[highest_score_key]
        
    except Exception as e:
        logging.error(f"Error finding highest score plan: {str(e)}")
        return None

def process_employee_plans():
    """
    Main function to process employee plans and find:
    1. The plan with the lowest premium (fp1)
    2. The plan with the highest score (fp2)
    """
    try:
        # Read the main CSV file
        main_df = pd.read_csv('scored_employee_plans.csv')
        
        # Initialize the new columns
        main_df['fp1'] = None
        main_df['fp2'] = None
        
        # Process each employee
        for index, row in main_df.iterrows():
            first_name = row['firstName']
            
            # Get the plan IDs for premium check
            plan_ids = [row[f'p{i}'] for i in range(1, 7) if pd.notna(row[f'p{i}'])]
            
            # Find the matching CSV file
            employee_csv_path = None
            for file in os.listdir('Final_Cleaned_CSV_Output'):
                if file.startswith('final_cleaned_') and first_name in file:
                    employee_csv_path = os.path.join('Final_Cleaned_CSV_Output', file)
                    break
            
            if not employee_csv_path:
                logging.warning(f"No CSV file found for employee {first_name}")
                continue
                
            # Find the plan with lowest premium (fp1)
            lowest_premium_plan = find_lowest_premium_plan(plan_ids, employee_csv_path)
            
            if lowest_premium_plan:
                main_df.at[index, 'fp1'] = lowest_premium_plan
                logging.info(f"Found lowest premium plan for {first_name}: {lowest_premium_plan}")
            else:
                logging.warning(f"Could not determine lowest premium plan for {first_name}")
            
            # Find the plan with highest score (fp2)
            highest_score_plan = find_highest_score_plan(row)
            
            if highest_score_plan:
                main_df.at[index, 'fp2'] = highest_score_plan
                logging.info(f"Found highest score plan for {first_name}: {highest_score_plan}")
            else:
                logging.warning(f"Could not determine highest score plan for {first_name}")
        
        # Save the results back to the same file
        main_df.to_csv('scored_employee_plans.csv', index=False)
        logging.info("Successfully updated scored_employee_plans.csv")
        
    except Exception as e:
        logging.error(f"Error in main processing: {str(e)}")

if __name__ == "__main__":
    process_employee_plans()
