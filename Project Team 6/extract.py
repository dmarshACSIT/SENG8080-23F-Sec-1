import pyodbc
import csv

def export_to_csv(server, database, table, csv_path):
    # Define the connection parameters
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    try:
        # Establish a connection
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Fetch data from the table
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        # Get the column names
        columns = [column[0] for column in cursor.description]

        # Write data to CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            
            # Write the header
            csv_writer.writerow(columns)

            # Write the data
            csv_writer.writerows(rows)

        print(f"Data exported to CSV successfully at: {csv_path}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        if conn:
            conn.close()

# Replace 'your_server_name', 'your_database_name', 'your_table_name', and 'your_csv_path' with your specific details
export_to_csv('RIZWI', 'USjob', 'job_data', 'ExctractedData.csv')
