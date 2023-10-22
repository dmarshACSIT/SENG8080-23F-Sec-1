import pandas as pd
import pyodbc
from datetime import datetime

csv_file_path = 'E:/case studies/flights.csv'

df = pd.read_csv(csv_file_path)

df['Date'] = pd.to_datetime(df[['Year', 'Month', 'DayofMonth', 'DayOfWeek']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%u')

df['DepTime'] = df['DepTime'].apply(lambda x: f"{int(x // 100):02d}:{int(x % 100):02d}" if not pd.isna(x) else pd.NA)
df['ArrTime'] = df['ArrTime'].apply(lambda x: f"{int(x // 100):02d}:{int(x % 100):02d}" if not pd.isna(x) else pd.NA)

columns_to_keep = ['Date', 'DepTime', 'ArrTime', 'UniqueCarrier', 'FlightNum']
df = df[columns_to_keep]

df = df.drop_duplicates()

print("Missing Values Before Handling:")
print(df.isnull().sum())

# Remove rows with missing values in 'DepTime' and 'ArrTime'
df.dropna(subset=['DepTime', 'ArrTime'], inplace=True)

# Check for missing values after handling
print("Missing Values After Handling:")
print(df.isnull().sum())

# Define the SQL Server connection string using Windows Authentication
connection_string = 'Driver={SQL Server};Server=Nilay;Database=flight_analysis;Trusted_Connection=yes;'

# Establish a connection to SQL Server
conn = pyodbc.connect(connection_string)

# Specify the table name in the database
table_name = 'HistoricalData'

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Define a regular expression pattern to match HH:MM format
time_pattern = r'^[0-2][0-9]:[0-5][0-9]$'

# Filter rows with 'DepTime' and 'ArrTime' in the correct format
valid_time_rows = df[df['DepTime'].str.match(time_pattern) & df['ArrTime'].str.match(time_pattern)]

# Loop through the DataFrame and insert each valid row into the SQL Server table
for index, row in valid_time_rows.iterrows():
    try:
        dep_time = row['DepTime']
        arr_time = row['ArrTime']

        # Handle time values greater than 23:59
        if dep_time > '23:59':
            dep_time = '00:00'
        if arr_time > '23:59':
            arr_time = '00:00'

        cursor.execute(f"INSERT INTO {table_name} (Date, DepTime, ArrTime, UniqueCarrier, FlightNum) VALUES (?, CAST(? AS TIME), CAST(? AS TIME), ?, ?)",
                       row['Date'], dep_time, arr_time, row['UniqueCarrier'], row['FlightNum'])
    except pyodbc.DataError as e:
        print(f"Error on index {index}: {e}")
        print(f"Row data: Date={row['Date']}, DepTime={row['DepTime']}, ArrTime={row['ArrTime']}, UniqueCarrier={row['UniqueCarrier']}, FlightNum={row['FlightNum']}")
        # Optionally, you can add additional handling logic here or skip problematic rows.

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()