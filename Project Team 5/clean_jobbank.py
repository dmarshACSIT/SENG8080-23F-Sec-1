import pandas as pd
import numpy as np
input_csv_filename = r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + "jobbank_2023-11-15.csv"

df = pd.read_csv(input_csv_filename)

# 1. Clean "Job Title" column
df["Job Title"] = df["Job Title"].str.replace("developer, software", "software developer")
df["Job Title"] = df["Job Title"].str.replace("senior software developer Verified", "senior software developer")
df["Job Title"] = df["Job Title"].str.replace("software developer Verified", "software developer")

# 2. Clean "Location" column
df["Location"] = df["Location"].apply(lambda x: x.replace(' (', ', ').replace(')', ''))
df["Location"] = df["Location"].str.replace('Location ', '').str.strip('"')

# 3. Split "Estimated Salary" into Min Salary and Max Salary
def extract_salary(salary):
    if "Salary not available" in salary:
        return np.nan, np.nan
    
    if "annually" in salary.lower():
        parts = salary.split(": ")[1].split(" to ")
        min_value = parts[0].replace("$", "").replace(",", "")
        max_value = parts[-1].split(" ")[0].replace("$", "").replace(",", "")
    elif "hourly" in salary.lower():
        hourly_rate = float(salary.split(": $")[1].split(" hourly")[0])
        min_value = str(hourly_rate * 40 * 52)
        max_value = min_value
    
    min_value = min_value.replace(" annually", "")
    return min_value, max_value

df[["Min Salary", "Max Salary"]] = df["Estimated Salary"].apply(lambda x: pd.Series(extract_salary(x)))

# Drop the original "Estimated Salary" column
df.drop(columns=["Estimated Salary"], inplace=True)

# Display the cleaned data
#print(input_csv_filename,"\n",df)

# Extract the date from the input CSV file's name
date_from_filename = input_csv_filename.split("_")[1].split(".csv")[0]

# Define the filename for the cleaned data
output_csv_filename = f"cleaned_jobbank_{date_from_filename}.csv"

# Save the cleaned data to a CSV file
df.to_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + output_csv_filename, index=False)