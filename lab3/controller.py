from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ast import literal_eval

from config import DATABASE_URI

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


class Controller():

    def __init__(self, model, view, autocommit=True):
        self.model = model
        self.view = view
        self.session = Session(autocommit=autocommit)

    def show_items(self, bullet_points=False):
        items = self.session.query(self.model).all()
        item_name = self.model.__tablename__
        if bullet_points:
            self.view.show_bullet_point_list(item_name, items)
        else:
            self.view.show_number_point_list(item_name, items)

    def show_item(self, item_id: int):
        item_name = self.model.__tablename__
        try:
            item = self.session.query(self.model).get(item_id)
            self.view.show_item(item, item_name)
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

    def __del__(self):
        self.session.close()


