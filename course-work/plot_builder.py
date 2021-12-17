import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class PlotBuilder:

    @staticmethod
    def build_price_plot(prices):
        price_values = list(
            map(lambda price: price.price, prices))
        price_dates = list(map(lambda price: price.created_at,
                               prices))

        df = pd.DataFrame(dict(date=np.array(price_dates),
                               value=np.array(price_values)))

        plot = sns.relplot(x="date", y="value", kind="line", data=df)
        plot.figure.autofmt_xdate()

        plt.show()
