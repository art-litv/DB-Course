import inspect

import models
from models import Model
from pprint import pprint


class Repository():

    def __init__(self, connection, model, autocommit=True):
        connection.autocommit = autocommit
        self.__connection = connection
        self.model = model  # __table__, __name__, __fields__

    def __get_queries(self):
        return {
            'get_items': """
                SELECT * FROM {0}
            """.format(self.model.__table__),
            'get_item_by_id': """
                SELECT * FROM {0} WHERE {1}_id = %(id)s
            """
            .format(self.model.__table__, self.model.__name__.lower()),
            'insert_items': """
              INSERT INTO {0} {1}
              VALUES {2}
            """,
            'update_item': """
              UPDATE {0} SET {1}
              WHERE {2}_id = %(id)s
            """.format(self.model.__table__, ', '.join([f"{field} = %({field})s" for field in tuple(self.model.__fields__)[1:]]), self.model.__name__.lower()),
            'delete_item': """
                DELETE FROM {0} WHERE {1}_id = %(id)s
            """.format(self.model.__table__, self.model.__name__.lower()),
            'generate_random_name_series': """
                SELECT chr(trunc(65+random() * 25)::int)
                || chr(trunc(97+random() * 25)::int)
                || chr(trunc(97+random() * 25)::int)
                || chr(trunc(97+random() * 25)::int)
                || chr(trunc(97+random() * 25)::int)
                || chr(trunc(97+random() * 25)::int)
                FROM generate_series(1, %(amount)s)
            """,
            'generate_random_integer_series': """
                SELECT trunc(random() * 100)::int
                FROM generate_series(1, %(amount)s)
            """,
            'get_random_id': """
                SELECT {0}_id FROM {1}
                ORDER BY RANDOM()
                LIMIT 1
            """.format(self.model.__name__, self.model.__table__),
            'filter_by_attribute': """
                SELECT * FROM {0}
                WHERE {1}
            """
        }

    def get_items(self):
        cursor = self.__connection.cursor()
        cursor.execute(self.__get_queries()['get_items'])

        items_data = cursor.fetchall()
        items = [self.model.from_tuple(item_data)
                 for item_data in items_data]

        cursor.close()
        return items

    def get_item_by_id(self, id: int):
        cursor = self.__connection.cursor()
        cursor.execute(
            self.__get_queries()['get_item_by_id'], {'id': str(id)}
        )

        items_data = cursor.fetchone()
        item = self.model.from_tuple(items_data)

        cursor.close()
        return item

    def create_item(self, item: Model):
        cursor = self.__connection.cursor()
        cursor.execute(
            self.__get_queries()['insert_item'], item.dict()
        )

        cursor.close()

    def create_items(self, items: list[Model]):
        cursor = self.__connection.cursor()
        values = [str(tuple(item.dict().values())[1:]) for item in items]
        cursor.execute(
            self.__get_queries()['insert_items']
                .format(self.model.__table__, str(tuple(self.model.__fields__)[1:]).replace("'", ""),
                        ','.join(values))
        )

        cursor.close()

    def update_item(self, item: Model):
        cursor = self.__connection.cursor()
        item_dict = item.dict()
        cursor.execute(
            self.__get_queries()['update_item'], item_dict
        )

        rows_updated = cursor.rowcount
        cursor.close()

        return bool(rows_updated)

    def delete_item(self, id: int):
        cursor = self.__connection.cursor()
        cursor.execute(
            self.__get_queries()['delete_item'], {'id': str(id)}
        )

        rows_deleted = cursor.rowcount
        cursor.close()

        return bool(rows_deleted)

    def get_random_id(self):
        cursor = self.__connection.cursor()
        cursor.execute(
            self.__get_queries()['get_random_id']
        )

        random_id = cursor.fetchone()
        cursor.close()

        return random_id

    def generate_random_id_series(self, amount: int):
        random_ids = []
        for _ in range(int(amount)):
            random_ids.append(self.get_random_id())

        return random_ids

    def __get_model_of_foreign_key(self, field):
        model_name = field.split('_')[0]
        for _, model in inspect.getmembers(models, inspect.isclass):
            if model.__name__.lower() == model_name:
                return model
        return None

    def __get_tuples_from_fields_series(self, fields_series):
        return [
            tuple([field_series[j][0] for field_series in fields_series]) for j in range(len(fields_series[0]))
        ]

    def generate_items(self, amount: int):
        cursor = self.__connection.cursor()

        fields_series = []
        for field in list(self.model.__fields__):
            if (field.endswith('id') and field != 'id'):
                model = self.__get_model_of_foreign_key(field)
                modelRepo = Repository(self.__connection, model)
                fields_series.append(
                    modelRepo.generate_random_id_series(amount))
                continue

            is_int = self.model.__annotations__[field] == int
            query_type = 'generate_random_integer_series' if is_int else 'generate_random_name_series'

            cursor.execute(
                self.__get_queries()[query_type],
                {
                    'amount': str(amount)
                }
            )

            random_data = cursor.fetchall()
            fields_series.append(random_data)

        items = [self.model.from_tuple(item_data)
                 for item_data in self.__get_tuples_from_fields_series(fields_series)]
        self.create_items(items)

        cursor.close()

    def get_filtered_items(self, attrs: dict):
        cursor = self.__connection.cursor()

        cursor.execute(
            self.__get_queries()['filter_by_attribute']
                .format(self.model.__table__, ' AND '.join([f'{key} = %({key})s' for key in attrs])),
            attrs
        )

        items_data = cursor.fetchall()
        items = [self.model.from_tuple(item_data)
                 for item_data in items_data]

        cursor.close()
        return items
