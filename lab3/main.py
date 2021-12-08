import inspect
from pprint import pprint
from time import time
import os

import models
from logger import Logger

from controller import Controller
from view import View


class Session:

    def start(self):
        while True:
            try:
                model_type = input('Input model type: ')
                model = self.search_model(model_type)
                controller = Controller(model, View())
                while True:
                    command = input(
                        'Enter a command (\'help\' for all commands): ')
                    if command == 'switch_model':
                        break
                    try:
                        self.dispatch_command(controller, command)
                    except Exception as _ex:
                        #raise _ex
                        Logger.log_error(_ex)
                    continue
            except Exception as _ex:
                #raise _ex
                Logger.log_error(_ex)
                continue

    def exit(self):
        self.__connection.close()
        Logger.log_info("PostgreSQL connection closed")
        quit()

    def switch_model(self):
        self.__connection.close()
        self.start()

    def get_commands(self, controller):
        commands = {
            'exit': self.exit,
            'show_items': controller.show_items,
            'show_item': controller.show_item,
            'show_filtered_items': controller.show_filtered_items,
            'insert_item': controller.insert_item,
            'update_item': controller.update_item,
            'delete_item': controller.delete_item,
            'switch_model': '',
        }
        commands['help'] = pprint
        return commands

    def dispatch_command(self, controller, command):
        command_parts = command.split(' ')
        command = command_parts[0]
        command_param = ''.join(command_parts[1:])
        commands = self.get_commands(controller)
        if command == 'help':
            commands[command](tuple(commands.keys()))
        elif command == 'cls':
            os.system('cls')
        elif command == 'show_filtered_items':
            start_time = time()
            commands[command](command_param)
            end_time = time()
            Logger.log_info(f'Filtration time: {end_time - start_time}')
        else:
            commands[command](command_param)

    def search_model(self, model_name):
        for _, model in inspect.getmembers(models, inspect.isclass):
            if model.__name__.lower() == model_name.lower():
                return model
        raise Exception('Model not found')


if __name__ == '__main__':
    session = Session()
    session.start()
