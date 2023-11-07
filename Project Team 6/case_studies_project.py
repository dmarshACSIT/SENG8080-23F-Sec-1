import pandas as pd
import pyodbc

# Define the path to your CSV file
csv_file = "C:\\Users\\Himani\\Desktop\\dataset.csv"  # Replace with the actual path to your CSV file

# Read CSV data into a DataFrame
data = pd.read_csv(csv_file)

# SQL Server Database Configuration
server_name = 'HIMANISHARMA'
db_name = 'CaseStudiesProject'
table_name = 'JobTrend'  # Replace with your table name

# Create a connection to the SQL Server database using trusted connection (Windows Authentication)
driver_name = '{SQL Server}'
connection_string = f'Driver={driver_name};Server={server_name};Database={db_name};Trusted_Connection=yes;'
conn = pyodbc.connect(connection_string)

# Create a cursor for database operations
cursor = conn.cursor()

# Check if the table exists, and create it if it doesn't
table_exists_query = f"IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}') CREATE TABLE {table_name} (Year INT, Geography NVARCHAR(255), Immig NVARCHAR(255), Reason NVARCHAR(255), AgeGroup NVARCHAR(255), BothSexes FLOAT, Men FLOAT, Women FLOAT);"
cursor.execute(table_exists_query)

# Commit the transaction to create the table
conn.commit()

# Insert DataFrame records one by one
for index, row in data.iterrows():
    insert_query = f"""
    INSERT INTO {table_name} (Year, Geography, Immig, Reason, AgeGroup, BothSexes, Men, Women)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    cursor.execute(insert_query, tuple(row))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print(f"Data has been successfully inserted into the {table_name} table.")
