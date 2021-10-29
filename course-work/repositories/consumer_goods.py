from repository import Repository

from models.models import ConsumerGoods


class ConsumerGoodsRepository(Repository):

    _QUERIES = {
        'get_consumers_goods': ("SELECT * FROM consumers_goods"),

        'get_consumer_goods': ("SELECT FROM consumers_goods"
                               "WHERE id = %s"),

        'insert_consumer_goods': ("INSERT INTO consumers_goods"
                                  "(name, price, sold)"
                                  "VALUES (%(name)s, %(price)s, %(sold)s)")
    }

    def get_consumers_goods(self):
        query_result = self.__execute_query(
            self, self._QUERIES['get_customers_good'])

        consumer_goods = [ConsumerGoods(**consumer_goods)
                          for consumer_goods in query_result]

        return consumer_goods

    def get_consumer_goods(self, id: int):
        query_result = self.__execute_query(
            self, self._QUERIES['get_customer_goods'], (id))

        consumer_goods = ConsumerGoods(**query_result)
        return consumer_goods

    def insert_consumer_goods(self, consumer_goods: ConsumerGoods):
        self.__execute_query(
            self, self._QUERIES['insert_consumer_goods'], consumer_goods.dict())
