# All the python libraries to perform different task.
import requests
import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# API key and airport details
api_key = '656644a20b44d4dd7a76c5f2'
origin_airport = 'IAH'
destination_airport = 'DFW'
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
all_flight_data = pd.DataFrame()


# Executing code for fetching flight data for each and every dates till the creating range betweent start_date and end_date  
while start_date <= end_date:
    # Date formating using strftime() function in 'YYYYMMDD' format.
    date = start_date.strftime('%Y%m%d')
    # Creating the API url using different parameters such as api_key, date, origin_airport and destination_airport.
    url = f'https://api.flightapi.io/trackbyroute/{api_key}?date={date}&airport1={origin_airport}&airport2={destination_airport}'
    # Sending an HTTP request to the API using requests.get() function of request library of python by providing url parameter.
    resp = requests.get(url)
    # Checking the status code of response for futher execution. If status is 200 then it will execute the body part of if condition.
    if resp.status_code == 200:
        # Parsing of JSON response json() function and collected into the flight_data variable.
        flight_data = resp.json()
        # Here parsed json response is converted into dataFrame using DataFrame() function by python library call pandas.
        df = pd.DataFrame(flight_data)
        # Here current data and previously collected data are being concatenated using pandas function call concat().
        all_flight_data = pd.concat([all_flight_data, df], ignore_index=True)
    # Display of fetched data for the current date.
    print(f"Fetched data for {date}")
    # Increse the date or move to the next date.
    start_date += timedelta(days=1)


###################################################
# Data cleaning part
###################################################

# Get the number of missing value in the 'Operated By' column.
missing_values = all_flight_data['Operated By'].apply(lambda x: str(x).strip() == '').sum()


# Display of number of missing valuse in 'Operated By' column.
print("Missing Values in 'Operated By' Column:", missing_values)


# Replacing missing value '-' with 'NaN' in the 'operated By' column.
all_flight_data['Operated By'].replace('-', np.nan, inplace=True)


# Format date columns
all_flight_data['DepartureDate'] = pd.to_datetime(all_flight_data['DepartureTime']).dt.date
all_flight_data['DepartureTime'] = pd.to_datetime(all_flight_data['DepartureTime']).dt.time
all_flight_data['ArrivalDate'] = pd.to_datetime(all_flight_data['ArrivalTime']).dt.date
all_flight_data['ArrivalTime'] = pd.to_datetime(all_flight_data['ArrivalTime']).dt.time

# Displaying the formatted data
print(all_flight_data)

# Data storing
conn = pyodbc.connect('Driver={SQL Server};Server=Nilay;Database=flight_analysis;Trusted_Connection=yes;')
cursor = conn.cursor()
table_name = 'schedule'

# Error handling using try, exception, and finally.
try:
    # Iterate through the rows of the DataFrame and insert data into the SQL Server database
    for index, row in all_flight_data.iterrows():
        # Extract the 'Airline' value from the current row and convert it to a string
        airline = str(row["Airline"])
        # Extract the 'FlightNumber' value from the current row and convert it to a string
        flight_number = str(row["FlightNumber"])
        # Extract the 'Status' value from the current row and convert it to a string
        status = str(row["Status"])
        # Extract the 'Operated By' value from the current row and convert it to a string, or set it to None if it's missing
        operated_by = str(row["Operated By"]) if row["Operated By"] is not None else None
        # Date formating using strftime() function.
        departure_date = row["DepartureDate"].strftime('%Y-%m-%d')
        # Date formating using strftime() function.
        departure_time = row["DepartureTime"].strftime('%H:%M:%S')
        # Time formating using strftime() function.
        arrival_date = row["ArrivalDate"].strftime('%Y-%m-%d')
        # Time formating using strftime() function.
        arrival_time = row["ArrivalTime"].strftime('%H:%M:%S')
        # Create SQL Insert query to store data into database.
        sql_insert = f"INSERT INTO {table_name} (Airline, FlightNumber, Status, OperatedBy, DepartureDate, DepartureTime, ArrivalDate, ArrivalTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        # Execute the SQL command using execute() function.
        cursor.execute(sql_insert, airline, flight_number, status, operated_by, departure_date, departure_time,
                       arrival_date, arrival_time)
    # Commit the change in the database.
    conn.commit()
    print(f"Data has been successfully inserted into the '{table_name}' table.")
except Exception as e:
    print(f"An error occurred while inserting data: {str(e)}")
finally:
    conn.close()