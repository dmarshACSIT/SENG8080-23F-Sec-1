from datetime import datetime
import pandas as pd

def convert_milliseconds_to_datetime(milliseconds):
    seconds = milliseconds / 1000.0
    return datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')

def load_traffic_data(data_path):
    df = pd.read_csv(data_path)  # Load your historical traffic data here


    # Assuming df is your DataFrame and 'start' is the column with date strings
    df['start'] = df['start'].apply(lambda x: convert_milliseconds_to_datetime(int(x[6:-2])))
    df['start'] = pd.to_datetime(df['start'])
    df['start'] = pd.to_datetime(df['start'])
    df['INCIDENT_DATE'] = df['start'].dt.date
    df['end'] = df['end'].apply(lambda x: convert_milliseconds_to_datetime(int(x[6:-2])))
    
    # Handle categorical variables using one-hot encoding or label encoding
    # For example, 'type' column can be encoded
    #df = pd.get_dummies(df, columns=['type'])  # One-hot encoding for 'type' column
    
    # Dropping unnecessary or deprecated columns
    columns_to_drop = [ 'verified', 'alertCCodes']
    df = df.drop(columns=columns_to_drop)
    
    # Handling missing values
    df = df.fillna(0)  # Fill NaN values with 0, adjust as needed
    
    return df

def load_traffic_volume_data(road_data_path):
    road_data = pd.read_csv(road_data_path)
    road_data['ACCIDENTDATE'] = pd.to_datetime(road_data['ACCIDENTDATE'])

    road_data['ACCIDENTDATE'] = road_data['ACCIDENTDATE'].dt.date
    return road_data
    

