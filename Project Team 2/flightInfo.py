import requests
import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

api_key = '653445bbfd8c895effa24fca'  

origin_airport = 'IAH'  
destination_airport = 'DFW' 

end_date = datetime.now()
start_date = end_date - timedelta(days=30)  

all_flight_data = pd.DataFrame()

while start_date <= end_date:
    date = start_date.strftime('%Y%m%d')
    url = f'https://api.flightapi.io/trackbyroute/{api_key}?date={date}&airport1={origin_airport}&airport2={destination_airport}'
    resp = requests.get(url)

    if resp.status_code == 200:
        flight_data = resp.json()
        df = pd.DataFrame(flight_data)
        all_flight_data = pd.concat([all_flight_data, df], ignore_index=True)

    print(f"Fetched data for {date}")
    start_date += timedelta(days=1)  
    

missing_values = all_flight_data['Operated By'].apply(lambda x: str(x).strip() == '').sum()
print("Missing Values in 'Operated By' Column:", missing_values)
all_flight_data['Operated By'].replace('-', np.nan, inplace=True)
print(all_flight_data)


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=Nilay;'
                      'Database=flight_analysis;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

table_name = 'schedules'

try:

    for index, row in all_flight_data.iterrows():
        airline = str(row["Airline"])  
        flight_number = str(row["FlightNumber"])  
        status = str(row["Status"])  
        operated_by = str(row["Operated By"]) if row["Operated By"] is not None else None  

        
        departure_time = datetime.strptime(row["DepartureTime"], "%I:%M %p, %b %d")
        arrival_time = datetime.strptime(row["ArrivalTime"], "%I:%M %p, %b %d")

        
        sql_insert = f"INSERT INTO {table_name} (Airline, FlightNumber, Status, OperatedBy, DepartureTime, ArrivalTime) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(sql_insert, airline, flight_number, status, operated_by, departure_time, arrival_time)

    conn.commit()
    print(f"Data has been successfully inserted into the '{table_name}' table.")
except Exception as e:
    print(f"An error occurred while inserting data: {str(e)}")
finally:
    conn.close()
