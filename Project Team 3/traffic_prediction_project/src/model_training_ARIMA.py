
from statsmodels.tsa.arima_model import ARIMA

def train_traffic_model(train_data):
    model = ARIMA(train_data, order=(5, 1, 0))
    model_fit = model.fit(disp=0)
    return model_fit
