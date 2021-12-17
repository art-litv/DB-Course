import numpy as np
from datetime import datetime

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import normalize


class DataPrediction:

    @staticmethod
    def __price_date_to_datetime(price_date):
        return datetime(price_date.year, price_date.month, price_date.day)

    @staticmethod
    def predict_price(prices, prediction_date):
        normalization_date_k = 1000000000
        normalization_price_k = 100
        price_values = list(
            map(lambda price: price.price / normalization_price_k, prices))
        price_dates = list(map(lambda price: DataPrediction.__price_date_to_datetime(price.created_at).timestamp() / normalization_date_k,
                               prices))

        model = Sequential([Dense(units=1, input_shape=[1])])
        model.compile(optimizer='sgd', loss='mean_squared_error')

        xs = np.array(price_dates, dtype=float)
        ys = np.array(price_values, dtype=float)

        model.fit(xs, ys, epochs=100)

        results = model.predict(
            [DataPrediction.__price_date_to_datetime(prediction_date).timestamp() / normalization_date_k])

        return results[0][0] * normalization_price_k
