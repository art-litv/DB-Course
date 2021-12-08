from ast import literal_eval
from items_import import ItemsImporter


class Controller():

    def __init__(self, repository, view):
        self.repository = repository  # crud api for existing model
        self.view = view

    def show_items(self, page, bullet_points=False):
        items = self.repository.get_items()
        paginated_items = self.__paginate_items(items)
        item_name = self.repository.model.__name__
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
        item_name = self.repository.model.__name__
        try:
            item = self.repository.get_item_by_id(item_id)
            self.view.show_item(item, item_name)
        except Exception as _ex:
            self.view.display_missing_item_error(item_name, item_id, _ex)

    def show_filtered_items(self, attrs, bullet_points=False):
        items = self.repository.get_filtered_items(literal_eval(attrs))
        item_name = self.repository.model.__name__
        if bullet_points:
            self.view.show_bullet_point_list(item_name, items)
        else:
            self.view.show_number_point_list(item_name, items)

    def insert_item(self, item_data_tuple):
        item = self.repository.model.from_tuple(literal_eval(item_data_tuple))
        try:
            self.repository.create_item(item)
            self.view.display_item_insertion(self.repository.model.__name__)
        except Exception as _ex:
            self.view.display_insert_item_error(item, _ex)

    def update_item(self, item_data_tuple):
        item_type = self.repository.model.__name__
        item = self.repository.model.from_tuple(literal_eval(item_data_tuple))
        try:
            is_updated = self.repository.update_item(item)
            if not is_updated:
                raise Exception('Item not found exception')

            self.view.display_item_updated(item_type, item.id)
        except Exception as _ex:
            self.view.display_missing_item_error(item_type, item.id, _ex)

    def delete_item(self, item_id: int):
        item_type = self.repository.model.__name__
        try:
            is_deleted = self.repository.delete_item(item_id)
            if not is_deleted:
                raise Exception('Item not found exception')

            self.view.display_item_deletion(item_type, item_id)
        except Exception as _ex:
            self.view.display_missing_item_error(item_type, item_id, _ex)

    def generate_items_with_db(self, amount):
        item_type = self.repository.model.__name__
        self.repository.generate_items(int(amount))
        self.view.display_items_generated(amount, item_type)

    def generate_items_from_dataset(self, path):
        item_type = self.repository.model.__name__
        items = ItemsImporter.get_items_from_csv(self.repository.model, path)
        self.repository.create_items(items)
        self.view.display_items_generated(int(items), item_type)

    def generate_items_from_network(self, url):
        item_type = self.repository.model.__name__
        items = ItemsImporter.get_items_from_network(
            self.repository.model, url)
        self.repository.create_items(items)
        self.view.display_items_generated(int(items), item_type)
