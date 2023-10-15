
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

def train_lstm_traffic_model(train_data, seq_length, epochs, batch_size):
    # Normalize the data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(train_data)

    # Create sequences for LSTM
    def create_sequences(data, seq_length):
        sequences = []
        for i in range(len(data) - seq_length):
            sequences.append(data[i:i+seq_length])
        return np.array(sequences)

    sequences = create_sequences(scaled_data, seq_length)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(seq_length, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Split data into input and output
    X = sequences[:, :-1]
    y = sequences[:, -1]

    # Reshape the data for LSTM
    X = X.reshape(X.shape[0], X.shape[1], 1)

    # Train the model
    model.fit(X, y, epochs=epochs, batch_size=batch_size)

    return model
