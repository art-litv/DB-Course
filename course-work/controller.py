from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ast import literal_eval
import datetime

from items_import import ItemsImporter
from config import DATABASE_URI
from data_prediction import DataPrediction
from plot_builder import PlotBuilder

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


class Controller():

    def __init__(self, model, view, autocommit=True):
        self.model = model
        self.view = view
        self.session = Session(autocommit=autocommit)

    def show_items(self, page, bullet_points=False):
        items = self.session.query(self.model).all()
        paginated_items = self.__paginate_items(items)
        item_name = self.model.__tablename__
        total_pages = len(paginated_items)
        if int(page) > total_pages:
            try:
                raise IndexError(
                    f'Page out of range exception'
                )
            except IndexError as _ex:
                self.view.display_page_error(item_name, page, total_pages, _ex)
        if bullet_points:
            self.view.show_bullet_point_list(
                item_name, paginated_items[int(page) - 1], page, total_pages)
        else:
            self.view.show_number_point_list(
                item_name, paginated_items[int(page) - 1], page, total_pages)

    @staticmethod
    def __paginate_items(items, per_page=10):
        return [items[i:i+per_page] for i in range(0, len(items), per_page)]

    def show_item(self, item_id: int):
        item_name = self.model.__tablename__
        try:
            item = self.session.query(self.model).get(item_id)
            if not item:
                raise Exception('Item not found')
            self.view.show_item(item, item_name, item_id)
        except Exception as _ex:
            self.view.display_missing_item_error(item_name, item_id, _ex)

    def show_filtered_items(self, attrs, bullet_points=False):
        items = self.session.query(self.model).filter_by(**literal_eval(attrs))
        item_name = self.model.__tablename__
        if bullet_points:
            self.view.show_bullet_point_list(item_name, items)
        else:
            self.view.show_number_point_list(item_name, items)

    def insert_item(self, item_data):
        item_data = literal_eval(item_data)
        item = self.model(**item_data)
        item_name = self.model.__tablename__
        try:
            self.session.add(item)
            self.view.display_item_insertion(item_name)
        except Exception as _ex:
            self.view.display_insert_item_error(item, _ex)

    def update_item(self, item_data):
        item_data = literal_eval(item_data)
        item_id_dict = {}
        id_column_name = list(item_data.keys())[0]
        item_id_dict[id_column_name] = item_data[id_column_name]
        item = self.session.query(self.model).filter_by(**item_id_dict).first()
        item_type = self.model.__tablename__
        is_item_found = bool(item)
        try:
            if not is_item_found:
                raise Exception('Item not found exception')

            for key, value in item_data.items():
                setattr(item, key, value)

            self.view.display_item_updated(
                item_type, item_id_dict[id_column_name])
        except Exception as _ex:
            self.view.display_missing_item_error(
                item_type, item_id_dict[id_column_name], _ex)

    def delete_item(self, item_id: int):
        item_type = self.model.__tablename__
        id_column_name = self.model.__table__.columns.keys()[0]
        item = self.session.query(self.model).filter_by(
            **{id_column_name: item_id}
        )
        try:
            if not item:
                raise Exception('Item not found exception')

            item.delete()
            self.view.display_item_deletion(item_type, item_id)
        except Exception as _ex:
            self.view.display_missing_item_error(item_type, item_id, _ex)

    def generate_items_with_db(self, amount):
        item_type = self.model.__tablename__
        model_fields = self.model.__table__.columns.keys()
        is_foreign_key = len(list(filter(
            lambda field: field.endswith("_id"), model_fields
        ))) > 1
        items = []
        for _ in range(int(amount)):
            item = self.model.generate(
                self.session) if is_foreign_key else self.model.generate()
            items.append(item)

        self.session.bulk_save_objects(items)
        self.view.display_items_generated(amount, item_type)

    def generate_items_from_dataset(self, path):
        item_type = self.model.__tablename__
        items = ItemsImporter.get_items_from_csv(self.model, path)
        self.session.bulk_save_objects(items)
        self.view.display_items_generated(len(items), item_type)

    def generate_items_from_network(self, url):
        item_type = self.model.__tablename__
        items = ItemsImporter.get_items_from_network(
            self.model, url)
        self.session.bulk_save_objects(items)
        self.view.display_items_generated(len(items), item_type)

    def predict_item_price(self, product_id, prediction_date=datetime.datetime.now()):
        item_name = self.model.__tablename__
        try:
            prices = self.session.query(
                self.model).filter_by(product_id=product_id).order_by(self.model.created_at).all()
            if len(prices) == 0:
                raise Exception('Prices for product not found')

            predicted_price = DataPrediction.predict_price(
                prices, prediction_date)

            print(predicted_price)
        except Exception as _ex:
            self.view.display_missing_item_error(item_name, product_id, _ex)

    def build_product_price_plot(self, product_id):
        item_name = self.model.__tablename__
        try:
            prices = self.session.query(
                self.model).filter_by(product_id=product_id).order_by(self.model.created_at).all()
            if len(prices) == 0:
                raise Exception('Prices for product not found')

            PlotBuilder.build_price_plot(prices)
        except Exception as _ex:
            self.view.display_missing_item_error(item_name, product_id, _ex)

    def __del__(self):
        self.session.close()
