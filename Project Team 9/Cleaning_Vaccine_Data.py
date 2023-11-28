
import pandas as pd
import numpy as np
import re


df = pd.read_csv("C:/Users/chris/OneDrive/Documents/Education/Semester 2/CaseStudies/Case rates by vaccination status and age group.csv")

# Remove empty columns
df = df.dropna(axis=1, how='all')

# Replace empty values with 0
df = df.fillna(0)

# Drop dullicates
df = df.drop_duplicates()


# Function to clean and extract the highest age
def clean_age(agegroup):
    agegroup = agegroup.replace('+', '')  # Remove '+'
    agegroup = agegroup.replace('-', ' to ')  # Replace '-' with ' to '
    agegroup = agegroup.replace('yrs', '')  # Remove 'yrs'
    
    # Skip 'ALL' values
    if agegroup == 'ALL':
        return None
    
    ages = agegroup.split(' to ')
    if len(ages) == 2:
        return max(int(ages[0]), int(ages[1]))
    elif len(ages) == 1:
        return int(ages[0])
    else:
        return None

    
# Apply the cleaning function to the 'agegroup' column
df['highest_age'] = df['agegroup'].apply(clean_age)

# Drop the original 'agegroup' column if not needed
df = df.drop(columns=['agegroup'])

# Clean the date column and extract only the date part
df['date'] = pd.to_datetime(df['date']).dt.date

# Define a function to identify and handle outliers using IQR
def handle_outliers_iqr(df, column_name):
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter out the outliers
    filtered_data = df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]
    
    return filtered_data

# Apply the handle_outliers_iqr function to the columns where you want to handle outliers
columns_to_handle_outliers = ['cases_unvac_rate_per100K', 'cases_partial_vac_rate_per100K', 'cases_notfull_vac_rate_per100K', 'cases_full_vac_rate_per100K', 'cases_boost_vac_rate_per100K']
for column in columns_to_handle_outliers:
    df = handle_outliers_iqr(df, column)

# The df DataFrame now contains rows with outliers removed
# Save the cleaned data to a new CSV file if needed
df.to_csv('cleaned_dataset.csv',index=False, mode='w')


