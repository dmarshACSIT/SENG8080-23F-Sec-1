import pandas as pd

file1 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + "FinalJobData.csv")
file2 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + "mergedJobData_2023-11-22.csv")

# Concatenate the two files
merged_data = pd.concat([file1, file2])

# Convert 'Retrieved Date' column to datetime format
merged_data['Retrieved Date'] = pd.to_datetime(merged_data['Retrieved Date'])

# Sort by 'Retrieved Date' in ascending order
merged_data.sort_values('Retrieved Date', inplace=True)

# Keep the first occurrence of unique rows based on 'Job Title', 'Company', 'Location'
merged_data.drop_duplicates(subset=['Job Title', 'Company', 'Location'], keep='first', inplace=True)

# Display the resulting merged and filtered data
merged_data.to_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" +"FinalJobData.csv", index=False)