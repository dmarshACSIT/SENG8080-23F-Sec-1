import pandas as pd
from datetime import datetime
import numpy as np

input_csv_filename = r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + "workopolis_2023-10-25.csv"

df = pd.read_csv(input_csv_filename)

df['Location'] = df['Location'].str.replace('— ', '').str.replace('Ontario', 'Various locations').str.replace('Canada', 'Various locations').str.replace('Kitchener-Waterloo', 'Kitchener')

# Convert 'N/A' in 'Estimated Salary' to 'NULL'
df['Estimated Salary'] = df['Estimated Salary'].replace('N/A', np.nan)

# Split and format 'Estimated Salary' into 'Min Salary' and 'Max Salary'
def extract_salary(salary):
    salary = str(salary)
    min_value, max_value = np.nan, np.nan
    
    if "N/A" not in salary:
        if "a year" in salary.lower():
            parts = salary.split("-")
            if len(parts) == 2:
                min_value = parts[0].replace("Estimated:", "").replace("$", "").strip().replace(",", "")
                max_value = parts[1].replace("$", "").strip().split(" ")[0].replace(",", "")
            else:
                min_value = max_value = salary.split(" a year")[0].replace('$', '').replace(',', '').strip()
        elif "an hour" in salary.lower():
            # Check if it's a range (e.g., '$70 - $80 an hour')
            if "-" in salary:
                hourly_rates = salary.split("-")
                min_hourly_rate = hourly_rates[0].replace("$", "").strip()
                max_hourly_rate = hourly_rates[1].replace("$", "").split(" ")[0].strip()
                if min_hourly_rate:
                    min_value = str(int(float(min_hourly_rate) * 40 * 52))  # Convert hourly to annual
                if max_hourly_rate:
                    max_value = str(int(float(max_hourly_rate) * 40 * 52))  # Convert hourly to annual
            else:
                hourly_rate = salary.split(" ")[0].replace("$", "").strip()
                if hourly_rate:  # Check for empty string
                    min_value = str(int(float(hourly_rate) * 40 * 52))  # Convert hourly to annual
                    max_value = min_value

    return pd.Series([min_value, max_value])

# Apply the extract_salary function
df[["Min Salary", "Max Salary"]] = df["Estimated Salary"].apply(extract_salary)

#def calculate_date(d):
#    if pd.notna(d) and d != np.nan:
#        result_date = datetime.now() - pd.DateOffset(days=int(d.split(" ")[0]))
#        return result_date.strftime('%Y-%m-%d')
#    return np.nan

#df['Job Age'] = df['Job Age'].apply(calculate_date)

column_order = ['Job Title', 'Company', 'Location', 'Min Salary', 'Max Salary']#, 'Job Age']

df = df[column_order]

# Extract the date from the input CSV file's name
date_from_filename = input_csv_filename.split("_")[1].split(".csv")[0]

# Define the filename for the cleaned data
output_csv_filename = f"cleaned_workopolis_{date_from_filename}.csv"

# Save the cleaned data to a CSV file
df.to_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + output_csv_filename, index=False)