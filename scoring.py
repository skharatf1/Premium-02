import pandas as pd
import os
import numpy as np
from pathlib import Path

def normalize_scores(scores):
    """Normalize scores to sum to 1 and round to 2 decimal places"""
    total = sum(scores)
    if total == 0:
        return [0.00] * len(scores)
    normalized = [round(score/total, 2) for score in scores]
    # Ensure the sum is exactly 1.00 by adjusting the last score
    if len(normalized) > 0:
        normalized[-1] = round(1.00 - sum(normalized[:-1]), 2)
    return normalized

def calculate_plan_scores(plan_data, composition, current_plan_levels):
    """Calculate scores for a single plan based on the scoring criteria"""
    scores = []
    
    # Deductible Score (lower is better)
    deductible_col = 'individual_medical_deductible' if composition == 'Employee Only' else 'family_medical_deductible'
    deductible_scores = plan_data[deductible_col].astype(float)
    deductible_scores = 1 - (deductible_scores - deductible_scores.min()) / (deductible_scores.max() - deductible_scores.min())
    scores.append(deductible_scores * 0.25)
    
    # HSA Eligibility Bonus
    hsa_scores = plan_data['hsa_eligible'].astype(float) * 0.15
    scores.append(hsa_scores)
    
    # Child Benefits Score
    child_benefits = (plan_data['child_eyewear'].astype(float) + 
                     plan_data['child_eye_exam'].astype(float) + 
                     plan_data['child_dental'].astype(float)) / 3
    child_benefits = (child_benefits - child_benefits.min()) / (child_benefits.max() - child_benefits.min())
    scores.append(child_benefits * 0.20)
    
    # Coinsurance Score
    coinsurance = plan_data['plan_coinsurance'].astype(float)
    coinsurance = (coinsurance - coinsurance.min()) / (coinsurance.max() - coinsurance.min())
    scores.append(coinsurance * 0.25)
    
    # Plan Match Bonus
    plan_match = (plan_data['plan_levels'].astype(float) == current_plan_levels).astype(float) * 0.15
    scores.append(plan_match)
    
    # Combine all scores
    final_scores = sum(scores)
    return final_scores

def main():
    # Read the main CSV file
    df = pd.read_csv('merged_employee_plans.csv')
    
    # Initialize all score columns (s1 through s6) with NaN
    for i in range(1, 7):
        df[f's{i}'] = np.nan
    
    # Directory containing individual employee CSV files
    csv_dir = Path('Final_Cleaned_CSV_Output')
    
    # Process each employee
    for idx, row in df.iterrows():
        first_name = row['firstName']
        composition = row['composition']
        current_plan_levels = row['current_plan_levels']
        
        # Find the matching CSV file
        employee_file = None
        for file in csv_dir.glob('final_cleaned_*.csv'):
            if first_name.lower() in file.name.lower():
                employee_file = file
                break
        
        if not employee_file:
            print(f"Warning: No matching CSV file found for employee {first_name}")
            continue
        
        # Read employee's plan data
        employee_plans = pd.read_csv(employee_file)
        
        # Get plan IDs for this employee
        plan_ids = [row[f'p{i}'] for i in range(1, 7) if pd.notna(row[f'p{i}'])]
        
        # Find matching plans
        matching_plans = employee_plans[employee_plans['id'].isin(plan_ids)]
        
        # Check for missing plans
        missing_plans = set(plan_ids) - set(matching_plans['id'])
        if missing_plans:
            print(f"Warning: Missing plans for employee {first_name}")
            print(f"Expected: {plan_ids}")
            print(f"Found: {list(matching_plans['id'])}")
        
        if len(matching_plans) == 0:
            print(f"Warning: No matching plans found for employee {first_name}")
            continue
        
        # Calculate scores for each plan
        plan_scores = calculate_plan_scores(matching_plans, composition, current_plan_levels)
        
        # Normalize scores to sum to 1 and round to 2 decimal places
        normalized_scores = normalize_scores(plan_scores)
        
        # Update the original dataframe with scores
        for i in range(6):  # Always process all 6 score columns
            if i < len(normalized_scores):
                df.at[idx, f's{i+1}'] = normalized_scores[i]
            else:
                df.at[idx, f's{i+1}'] = 0.00  # Set remaining scores to 0.00
    
    # Save the updated dataframe
    df.to_csv('scored_employee_plans.csv', index=False)
    print("Analysis complete. Results saved to scored_employee_plans.csv")

if __name__ == "__main__":
    main()
