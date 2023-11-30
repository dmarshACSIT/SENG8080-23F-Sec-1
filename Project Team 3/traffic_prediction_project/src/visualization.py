# src/visualization.py
import matplotlib.pyplot as plt
import folium
import pandas as pd

def visualize_traffic_predictions(test_data, predictions,incident_data):
    plt.figure(figsize=(12, 6))
    plt.plot(test_data, label='Actual Traffic')
    plt.plot(predictions, color='red', label='Predicted Traffic')
    plt.xlabel('Time')
    plt.ylabel('Traffic')
    plt.title('Traffic Prediction')
    plt.legend()
    plt.show()


    # Assuming your DataFrame is named 'incident_data'
    # 'point' column contains the latitude and longitude coordinates

    # Create a base map centered around the mean coordinates
    m = folium.Map(location=[incident_data['point'].mean()], zoom_start=12)

    # Iterate through incidents and add markers to the map
    for index, row in incident_data.iterrows():
        lat, lon = row['point']
        folium.Marker([lat, lon], popup=row['description']).add_to(m)

    # Display the map
    m






