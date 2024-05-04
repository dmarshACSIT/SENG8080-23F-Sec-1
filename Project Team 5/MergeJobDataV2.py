import pandas as pd

file1 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + 'mergedJobData_2023-10-04.csv')
file2 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + 'mergedJobData_2023-10-11.csv')
file3 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + 'mergedJobData_2023-10-18.csv')
file4 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" +'mergedJobData_2023-10-25.csv')
file5 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + 'mergedJobData_2023-11-01.csv')
file6 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + 'mergedJobData_2023-11-08.csv')
file7 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + 'mergedJobData_2023-11-15.csv')
file8 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + 'mergedJobData_2023-11-22.csv')

# Concatenate the two files
merged_data = pd.concat([file1, file2, file3, file4, file5, file6, file7, file8])

# Convert 'Retrieved Date' column to datetime format
merged_data['Retrieved Date'] = pd.to_datetime(merged_data['Retrieved Date'])

merged_data['Last Appearance'] = merged_data.groupby(['Job Title', 'Company', 'Location'])['Retrieved Date'].transform('max')

# Sort by 'Retrieved Date' in ascending order
merged_data.sort_values('Retrieved Date', inplace=True)

# Keep the first occurrence of unique rows based on 'Job Title', 'Company', 'Location'
merged_data.drop_duplicates(subset=['Job Title', 'Company', 'Location'], keep='first', inplace=True)

# Display the resulting merged and filtered data
merged_data.to_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + "FinalJobDataV2.csv", index=False)