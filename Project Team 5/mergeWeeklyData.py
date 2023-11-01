import pandas as pd

# Read the first CSV file into a DataFrame
file1 = "cleaned_jobbank_2023-11-01.csv"
file2 = "cleaned_workopolis_2023-11-01.csv"
df1 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + file1)
df2 = pd.read_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + file2)
date_from_filename1 = file1.split("_")[2].split(".csv")[0]
date_from_filename2 = file2.split("_")[2].split(".csv")[0]

print(date_from_filename1,date_from_filename2)

if date_from_filename1 == date_from_filename2:    
    # Merge the two DataFrames vertically
    merged_df = pd.concat([df1, df2], ignore_index=True)

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + "mergedJobData_" + date_from_filename1 + ".csv", index=False)