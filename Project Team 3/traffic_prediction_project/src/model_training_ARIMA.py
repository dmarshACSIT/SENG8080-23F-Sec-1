import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

def train_arima_model(merged_df):
    # Extract the time series data
    time_series_data = merged_df[['Year', 'AADT']].copy()

    # Train-test split for time series data
    train_size = int(len(time_series_data) * 0.8)
    train, test = time_series_data.iloc[:train_size], time_series_data.iloc[train_size:]

    # Fit ARIMA model
    order = (5, 1, 0)  # Adjust order based on your data
    model = ARIMA(train['AADT'], order=order)
    model_fit = model.fit()
    # Predictions
    start_year = test['Year'].min()
    end_year = test['Year'].max()
    predictions = model_fit.predict(start=start_year, end=end_year)

    # Evaluate model (e.g., Mean Absolute Error)
    mae = np.mean(np.abs(predictions - test['AADT']))
    print(f'Mean Absolute Error: {mae}')
    return predictions

    

   


