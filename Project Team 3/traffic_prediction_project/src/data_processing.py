
import pandas as pd

def load_traffic_data(data_path):
    data = pd.read_csv(data_path)  # Load your historical traffic data here
    # Add data preprocessing steps here
    return data
