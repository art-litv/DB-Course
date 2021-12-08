import pandas as pd
import requests
from datetime import datetime

from models import *


class ItemsImporter:

    @staticmethod
    def get_items_from_csv(model, dataset_path):
        data_set = pd.read_csv(dataset_path)
        data_tuples = list(data_set.itertuples(index=False, name=None))
        return [model.from_tuple(data_tuple) for data_tuple in data_tuples]

    @staticmethod
    def get_items_from_network(model, url):
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data_tuples = [model.parse_obj(data) for data in data]
        return data_tuples
