import pandas as pd
import requests

from models import *


class ItemsImporter:

    @staticmethod
    def get_items_from_csv(model, dataset_path):
        data_set = pd.read_csv(dataset_path)
        data_tuples = data_set.to_dict('records')
        return [model(**data_tuple) for data_tuple in data_tuples]

    @staticmethod
    def get_items_from_network(model, url):
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        non_id_dicts = [{key: data[key]
                         for key in data.keys() if key != "id"} for data in data]
        data_tuples = [model(**data) for data in non_id_dicts]
        return data_tuples
