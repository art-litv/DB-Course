from logger import Logger


class View():

    @staticmethod
    def show_bullet_point_list(item_type, items):
        print('--- {} LIST ---'.format(item_type.upper()))
        for item in items:
            print('* {}'.format(item))

    @staticmethod
    def show_number_point_list(item_type, items):
        print('--- {} LIST ---'.format(item_type.upper()))
        for i, item in enumerate(items):
            print('{}. {}'.format(i+1, item))

    @staticmethod
    def show_item(item, item_name):
        print(f'Item from {item_name} found')
        Logger.log_info(item)

    @staticmethod
    def display_missing_item_error(item_type, id, err):
        print('Error. Item {} with id {} not found'.format(item_type, id))
        Logger.log_error(err)

    @staticmethod
    def display_insert_item_error(item, err):
        print('Error. Could not insert {} into database'
              .format(item))
        Logger.log_error(err)

    @staticmethod
    def display_item_updated(item_type, item_id):
        Logger.log_info(f'Updated item {item_type} with id {item_id}')

    @staticmethod
    def display_item_deletion(item_name, item_id):
        Logger.log_info(
            f'{item_name} with id {item_id} has been removed from database'
        )

    @staticmethod
    def display_item_insertion(item_type):
        Logger.log_info(f'{item_type} has been inserted to database')

    @staticmethod
    def display_items_generated(count, item_type):
        Logger.log_info(
            f'{count} of {item_type} has been generated'
        )
