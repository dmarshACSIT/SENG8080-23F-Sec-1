# src/visualization.py
import matplotlib.pyplot as plt

def visualize_traffic_predictions(test_data, predictions):
    plt.figure(figsize=(12, 6))
    plt.plot(test_data, label='Actual Traffic')
    plt.plot(predictions, color='red', label='Predicted Traffic')
    plt.xlabel('Time')
    plt.ylabel('Traffic')
    plt.title('Traffic Prediction')
    plt.legend()
    plt.show()
