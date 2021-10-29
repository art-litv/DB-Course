from abc import ABC, abstractmethod
from mysql.connector import Error


class Repository(ABC):

    @abstractmethod
    def __init__(self, connection):
        self.__connection = connection

    def __execute_query(self, query, params=[]):
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query, params=params)
            self.__connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
