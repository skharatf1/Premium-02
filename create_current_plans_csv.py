import pandas as pd
import re

def extract_dollar_amount(value):
    """
    Extracts dollar amount from a string, handling various formats including those with '~'.
    Returns 0 if no match is found or if the input is null/empty.
    """
    if not value or pd.isna(value):
        return 0
    # Remove '~' if present and find dollar amount
    value = str(value).replace('~', '')
    match = re.search(r'\$(\d+,?\d*)', value)
    if match:
        # Remove commas and convert to integer
        amount_str = match.group(1).replace(',', '')
        try:
            return int(amount_str)
        except ValueError:
            return 0
    return 0

def extract_percentage(value):
    """
    Extracts percentage from a string.
    Returns 0 if no match is found or if the input is null/empty.
    """
    if not value or pd.isna(value):
        return 0
    match = re.search(r'(\d+)%', value)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return 0
    return 0

def assign_individual_level(deductible):
    """
    Assigns individual level based on deductible amount
    """
    if deductible >= 4999:
        return 1
    elif 0 <= deductible <= 499:
        return 3
    elif 500 <= deductible <= 1499:
        return 4
    return 0

def assign_family_level(deductible):
    """
    Assigns family level based on deductible amount
    """
    if deductible >= 4999:
        return 1
    elif 0 <= deductible <= 499:
        return 3
    elif 500 <= deductible <= 1499:
        return 4
    return 0

# Define the plan data
plans_data = {
    "P001": {
        "id": "P001",
        "name": "Oscar HMO",
        "planType": "HMO",
        "carrierName": "Oscar Silver 5000 Off Exchange Plan",
        "level": "silver",
        "hsaEligible": False,
        "individualMedicalDeductibleInNetwork": "$5000",
        "familyMedicalDeductibleInNetwork": "$10000",
        "individualMedicalMoopInNetwork": "$9200",
        "familyMedicalMoopInNetwork": "$18400",
        "planCoinsuranceInNetwork": "Certain diagnostic tests (e.g. x-ray): 30% coinsurance",
        "primaryCarePhysicianInNetwork": "$55/visit",
        "specialistInNetwork": "$100/visit"
    },
    "P002": {
        "id": "P002",
        "name": "UnitedHealthcare HMO",
        "planType": "HMO",
        "carrierName": "UHC Silver‑X Copay Focus $0 Indiv Med Ded (Off‑Exchange Only)",
        "level": "silver",
        "hsaEligible": False,
        "individualMedicalDeductibleInNetwork": "$0",
        "familyMedicalDeductibleInNetwork": "$0",
        "individualMedicalMoopInNetwork": "$9200",
        "familyMedicalMoopInNetwork": "$18400",
        "planCoinsuranceInNetwork": "For durable medical equipment and home health care: 30%",
        "primaryCarePhysicianInNetwork": "$35/visit",
        "specialistInNetwork": "$90/visit"
    },
    "P003": {
        "id": "P003",
        "name": "KP GA Signature Gold 500 Ded/500 Rx Ded",
        "planType": "HMO",
        "carrierName": "Kaiser Permanente HMO network",
        "level": "silver",
        "hsaEligible": False,
        "individualMedicalDeductibleInNetwork": "$500",
        "familyMedicalDeductibleInNetwork": "$1000",
        "individualMedicalMoopInNetwork": "$8000",
        "familyMedicalMoopInNetwork": "$16000",
        "planCoinsuranceInNetwork": "30% coinsurance applies for lab testing",
        "primaryCarePhysicianInNetwork": "~$20/visit",
        "specialistInNetwork": "~$40/visit"
    }
}

# Create DataFrame from the plans data
df = pd.DataFrame.from_dict(plans_data, orient='index')

# Extract numeric values from columns
columns_to_process = [
    'individualMedicalDeductibleInNetwork',
    'familyMedicalDeductibleInNetwork',
    'individualMedicalMoopInNetwork',
    'familyMedicalMoopInNetwork',
    'primaryCarePhysicianInNetwork',
    'specialistInNetwork'
]

for column in columns_to_process:
    df[column] = df[column].apply(extract_dollar_amount)

# Handle planCoinsuranceInNetwork separately as it contains percentages
df['planCoinsuranceInNetwork'] = df['planCoinsuranceInNetwork'].apply(extract_percentage)

# Add new columns for individual and family levels
df['individual_levels'] = df['individualMedicalDeductibleInNetwork'].apply(assign_individual_level)
df['family_levels'] = df['familyMedicalDeductibleInNetwork'].apply(assign_family_level)

# Save DataFrame to CSV
df.to_csv('current_plans_new.csv', index=False)

print("CSV file 'current_plans_new.csv' has been created successfully!") 