import pandas as pd
import numpy as np

def load_data():
    # Load the CSV file
    df = pd.read_csv('scored_employee_plans_with_premiums.csv')
    return df

def get_user_input():
    # Get user input for score threshold and budget limit
    score_threshold = float(input("Enter the total score threshold: "))
    budget_limit = float(input("Enter the total budget limit: "))
    return score_threshold, budget_limit

def get_composition_multiplier(member_status, composition):
    # Define composition multipliers
    multipliers = {
        ('PT', 'Employee Only'): 0.5,
        ('PT', 'Employee + Spouse'): 0.6,
        ('PT', 'Employee + Family'): 0.7,
        ('FT', 'Employee Only'): 0.75,
        ('FT', 'Employee + Spouse'): 0.875,
        ('FT', 'Employee + Family'): 1.0
    }
    return multipliers.get((member_status, composition), 0)

def create_fp1_score(df):
    # Create fp1_Score DataFrame
    fp1_data = []
    total_company_cost = 0
    
    for _, row in df.iterrows():
        # Get all scores and corresponding plan IDs
        scores = []
        plan_ids = []
        premiums = []
        
        # Collect valid scores, plan IDs, and premiums
        for i in range(1, 7):
            if pd.notna(row[f's{i}']) and pd.notna(row[f'p{i}']) and pd.notna(row[f'p{i}_premium']):
                scores.append(float(row[f's{i}']))
                plan_ids.append(row[f'p{i}'])
                premiums.append(float(row[f'p{i}_premium']))
        
        if not scores:  # Skip if no valid plans found
            print(f"Warning: No valid plans found for employee {row['firstName']} {row['lastName']}")
            continue
            
        # Find the index of the highest score
        max_score_idx = scores.index(max(scores))
        
        # Get composition multiplier
        multiplier = get_composition_multiplier(row['memberStatus'], row['composition'])
        company_cost = premiums[max_score_idx] * multiplier
        total_company_cost += company_cost
        
        # Create employee data
        employee_data = {
            'employee_name': f"{row['firstName']} {row['lastName']}",
            'selected_plan_id': plan_ids[max_score_idx],
            'selected_score': scores[max_score_idx],
            'selected_premium': premiums[max_score_idx],
            'company_cost': company_cost
        }
        fp1_data.append(employee_data)
    
    return pd.DataFrame(fp1_data), total_company_cost

def create_fp2_budget(df, budget_limit):
    # Create fp2_Budget DataFrame
    fp2_data = []
    total_premium = 0
    total_company_cost = 0
    
    for _, row in df.iterrows():
        # Get all premiums and corresponding plan IDs and scores
        scores = []
        plan_ids = []
        premiums = []
        
        # Collect valid scores, plan IDs, and premiums
        for i in range(1, 7):
            if pd.notna(row[f's{i}']) and pd.notna(row[f'p{i}']) and pd.notna(row[f'p{i}_premium']):
                scores.append(float(row[f's{i}']))
                plan_ids.append(row[f'p{i}'])
                premiums.append(float(row[f'p{i}_premium']))
        
        if not premiums:  # Skip if no valid plans found
            print(f"Warning: No valid plans found for employee {row['firstName']} {row['lastName']}")
            continue
            
        # Find the index of the lowest premium
        min_premium_idx = premiums.index(min(premiums))
        
        # Get composition multiplier
        multiplier = get_composition_multiplier(row['memberStatus'], row['composition'])
        company_cost = premiums[min_premium_idx] * multiplier
        
        # Check if adding this premium would exceed the budget
        if total_premium + premiums[min_premium_idx] <= budget_limit:
            total_premium += premiums[min_premium_idx]
            total_company_cost += company_cost
            
            # Create employee data
            employee_data = {
                'employee_name': f"{row['firstName']} {row['lastName']}",
                'selected_plan_id': plan_ids[min_premium_idx],
                'selected_score': scores[min_premium_idx],
                'selected_premium': premiums[min_premium_idx],
                'company_cost': company_cost
            }
            fp2_data.append(employee_data)
        else:
            # If budget would be exceeded, skip this employee
            print(f"Warning: Budget limit reached. Skipping employee {row['firstName']} {row['lastName']}")
    
    return pd.DataFrame(fp2_data), total_company_cost

def main():
    # Load data
    df = load_data()
    
    # Get user input
    score_threshold, budget_limit = get_user_input()
    
    # Create fp1_Score DataFrame
    fp1_score, fp1_total_company_cost = create_fp1_score(df)
    
    # Calculate total score
    total_score = fp1_score['selected_score'].sum()
    
    # Check if total score meets threshold
    if total_score >= score_threshold:
        print("\nScore threshold met!")
        print(f"Total Score: {total_score}")
        print(f"Total Company Cost (fp1_Score): ${fp1_total_company_cost:.2f}")
        print("\nfp1_Score DataFrame:")
        print(fp1_score)
    else:
        print(f"\nScore threshold not met. Total Score: {total_score}")
    
    # Create fp2_Budget DataFrame
    fp2_budget, fp2_total_company_cost = create_fp2_budget(df, budget_limit)
    
    # Calculate total premium
    total_premium = fp2_budget['selected_premium'].sum()
    
    print(f"\nTotal Premium: ${total_premium:.2f}")
    print(f"Total Company Cost (fp2_Budget): ${fp2_total_company_cost:.2f}")
    print("\nfp2_Budget DataFrame:")
    print(fp2_budget)

if __name__ == "__main__":
    main()
