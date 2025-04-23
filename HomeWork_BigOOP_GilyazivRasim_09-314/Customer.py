import Logger
from typing import Dict, Any

logger = Logger.logger

class Customer:
    '''Класс клиента'''
    def __init__(self, customer_id: str, name: str) -> None:
        '''Конструктор клиента'''
        self.__customer_id = customer_id
        self.__name = name
        logger.info(f"Создан клиент: {name} (ID: {customer_id})")

    @property
    def customer_id(self) -> str:
        '''Геттер для ID клиента'''
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, customer_id: str) -> None:
        '''Сеттер для ID клиента'''
        logger.debug(f"Изменение ID клиента с {self.__customer_id} на {customer_id}")
        self.__customer_id = customer_id

    @property
    def name(self) -> str:
        '''Геттер для имени клиента'''
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        '''Сеттер для имени клиента'''
        logger.debug(f"Изменение имени клиента с {self.__name} на {name}")
        self.__name = name

    def __str__(self) -> str:
        '''Строковое представление клиента'''
        return f"Клиент {self.name} ID: {self.customer_id}"

    def to_dict(self) -> Dict[str, Any]:
        '''Преобразование клиента в словарь'''
        return {
            'cutstomer_id': self.customer_id,
            'name': self.name,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Customer':
        '''Создание клиента из словаря'''
        logger.debug(f"Создание Customer из словаря: {data}")
        return cls(*data.values())