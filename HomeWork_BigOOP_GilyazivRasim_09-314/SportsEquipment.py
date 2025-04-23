from Errors import *
from Mixins import *
from typing import Dict, Any
from EquipmentMeta import EquipmentMeta
from abc import abstractmethod
from datetime import datetime, timedelta
from Customer import Customer
from Interface import *
import Logger

logger = Logger.logger

class SportEquipment(Rentable, LoggingMixin, NotificationMixin, metaclass=EquipmentMeta):
    '''Абстрактный класс спортивного инвентаря'''
    def __init__(self, equipment_id: str, name: str, condition: str, hourly_rate: float, is_available: bool = True) -> None:
        '''Конструктор спортивного инвентаря'''
        self.__equipment_id = equipment_id
        self.__name = name
        self.__condition = condition
        self.__hourly_rate = hourly_rate
        self.__is_available = is_available
        logger.info(f"Создан инвентарь: {name} (ID: {equipment_id})")
        print(self.send_notification(f'Инвентарь {name} готов к выдаче'))

    @property
    def equipment_id(self) -> str:
        '''Геттер для ID оборудования'''
        return self.__equipment_id

    @equipment_id.setter
    def equipment_id(self, equipment_id: str) -> None:
        '''Сеттер для ID оборудования'''
        logger.debug(f"Изменение ID оборудования с {self.__equipment_id} на {equipment_id}")
        self.__equipment_id = equipment_id

    @property
    def name(self) -> str:
        '''Геттер для названия оборудования'''
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        '''Сеттер для названия оборудования'''
        logger.debug(f"Изменение названия оборудования с {self.__name} на {name}")
        self.__name = name

    @property
    def condition(self) -> str:
        '''Геттер для состояния оборудования'''
        return self.__condition

    @condition.setter
    def condition(self, condition: str) -> None:
        '''Сеттер для состояния оборудования'''
        logger.debug(f"Изменение состояния оборудования с {self.__condition} на {condition}")
        self.__condition = condition

    @property
    def hourly_rate(self) -> float:
        '''Геттер для почасовой ставки'''
        return self.__hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, hourly_rate: float) -> None:
        '''Сеттер для почасовой ставки'''
        if hourly_rate < 0:
            logger.error("Попытка установить отрицательную почасовую ставку")
            raise InvalidEquipmentError("Недопустимое значение для цены")
        logger.debug(f"Изменение почасовой ставки с {self.__hourly_rate} на {hourly_rate}")
        self.__hourly_rate = hourly_rate

    @property
    def is_available(self) -> bool:
        '''Геттер для статуса доступности'''
        return self.__is_available

    @is_available.setter
    def is_available(self, is_available: bool) -> None:
        '''Сеттер для статуса доступности'''
        logger.debug(f"Изменение статуса доступности с {self.__is_available} на {is_available}")
        self.__is_available = is_available

    @abstractmethod
    def calculate_rental_cost(self, hours: float) -> float:
        '''Абстрактный метод для расчета стоимости аренды'''
        pass

    def __str__(self) -> str:
        '''Строковое представление объекта'''
        return f"Инвентарь: {self.__name}, Состояние: {self.__condition}"

    def __lt__(self, other: Any) -> bool:
        '''Оператор сравнения "меньше"'''
        return (self.__hourly_rate, self.__condition) < (other.hourly_rate, other.condition)

    def __gt__(self, other: Any) -> bool:
        '''Оператор сравнения "больше"'''
        return (self.__hourly_rate, self.__condition) > (other.hourly_rate, other.condition)

    def rent_equipment(self, customer: 'Customer', start_time: datetime
                       , end_time: datetime = datetime.now() + timedelta(days=1), extras: Dict[str, float] = None):
        '''Метод для аренды оборудования'''
        if not self.is_available:
            logger.warning(f"Попытка арендовать недоступный инвентарь: {self.__name}")
            raise RentalNotFoundError("Инвентарь недоступен")
        from Rental import Rental
        logger.info(f"Инвентарь {self.name} арендован клиентом {customer.name}")
        print(self.log_action(f'Инвентарь {self.name} арендован'))
        self.is_available = False
        rental_id = f"rent_{self.equipment_id}"
        return Rental(rental_id, customer, self, start_time, end_time, extras)

    def to_dict(self) -> Dict[str, Any]:
        '''Преобразование объекта в словарь'''
        return {
            'equipment_id': self.equipment_id,
            'name': self.name,
            'condition': self.condition,
            'hourly_rate': self.hourly_rate,
            'is_available': self.is_available
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SportEquipment':
        '''Создание объекта из словаря'''
        logger.debug(f"Создание SportEquipment из словаря: {data}")
        return cls(*data.values())

class Bicycle(SportEquipment):
    '''Класс велосипеда'''
    def __init__(self, equipment_id: str, name: str, condition: str
                 , hourly_rate: float, bike_type: str, is_available: bool = True) -> None:
        '''Конструктор велосипеда'''
        super().__init__(equipment_id, name, condition, hourly_rate, is_available)
        self.__type = bike_type
        logger.info(f"Создан велосипед: {name} (Тип: {bike_type})")

    @property
    def type(self) -> str:
        '''Геттер для типа велосипеда'''
        return self.__type

    @type.setter
    def type(self, new: str) -> None:
        '''Сеттер для типа велосипеда'''
        logger.debug(f"Изменение типа велосипеда с {self.__type} на {type}")
        self.__type = type

    def calculate_rental_cost(self, hours: float) -> float:
        '''Расчет стоимости аренды велосипеда'''
        logger.debug(f"Расчет стоимости аренды велосипеда на {hours} часов")
        if hours >= 5:
            return self.hourly_rate * hours * 0.92
        return self.hourly_rate * hours

    def __str__(self) -> str:
        '''Строковое представление велосипеда'''
        return f"Велосипед: {self.name}, Тип: {self.__type}"

    def to_dict(self) -> Dict[str, Any]:
        '''Преобразование велосипеда в словарь'''
        return {
            'equipment_id': self.equipment_id,
            'name': self.name,
            'condition': self.condition,
            'hourly_rate': self.hourly_rate,
            'type': self.type,
            'is_available': self.is_available
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Bicycle':
        '''Создание велосипеда из словаря'''
        logger.debug(f"Создание Bicycle из словаря: {data}")
        return cls(*data.values())

class Skis(SportEquipment):
    '''Класс лыж'''
    def __init__(self, equipment_id: str, name: str, condition: str
                 , hourly_rate: float, length: float, is_available: bool = True) -> None:
        '''Конструктор лыж'''
        super().__init__(equipment_id, name, condition, hourly_rate, is_available)
        self.__length = length
        logger.info(f"Созданы лыжи: {name} (Длина: {length})")

    @property
    def length(self) -> float:
        '''Геттер для длины лыж'''
        return self.__length

    @length.setter
    def length(self, length: float) -> None:
        '''Сеттер для длины лыж'''
        if length < 0:
            logger.error("Попытка установить отрицательную длину лыж")
            raise InvalidEquipmentError
        logger.debug(f"Изменение длины лыж с {self.__length} на {length}")
        self.__length = length

    def calculate_rental_cost(self, hours: float) -> float:
        '''Расчет стоимости аренды лыж'''
        logger.debug(f"Расчет стоимости аренды лыж на {hours} часов")
        if hours >= 5:
            return self.hourly_rate * hours * 0.9
        return self.hourly_rate * hours

    def __str__(self) -> str:
        '''Строковое представление лыж'''
        return f"Лыжи: {self.name}, Длина: {self.__length}"

    def to_dict(self) -> Dict[str, Any]:
        '''Преобразование лыж в словарь'''
        return {
            'equipment_id': self.equipment_id,
            'name': self.name,
            'condition': self.condition,
            'hourly_rate': self.hourly_rate,
            'length': self.length,
            'is_available': self.is_available
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Skis':
        '''Создание лыж из словаря'''
        logger.debug(f"Создание Skis из словаря: {data}")
        return cls(*data.values())

class TennisRacket(SportEquipment):
    '''Класс теннисной ракетки'''
    def __init__(self, equipment_id: str, name: str,condition: str
                 , hourly_rate: float, string_tension: float, is_available: bool = True) -> None:
        '''Конструктор теннисной ракетки'''
        super().__init__(equipment_id, name, condition, hourly_rate, is_available)
        self.__string_tension = string_tension
        logger.info(f"Создана теннисная ракетка: {name} (Натяжение: {string_tension})")

    @property
    def string_tension(self) -> float:
        '''Геттер для натяжения струн'''
        return self.__string_tension

    @string_tension.setter
    def string_tension(self, string_tension: float) -> None:
        '''Сеттер для натяжения струн'''
        if string_tension < 0:
            logger.error("Попытка установить отрицательное натяжение струн")
            raise InvalidEquipmentError("Недопустимое значение для напряжения")
        logger.debug(f"Изменение натяжения струн с {self.__string_tension} на {string_tension}")
        self.__string_tension = string_tension

    def calculate_rental_cost(self, hours: float) -> float:
        '''Расчет стоимости аренды ракетки'''
        logger.debug(f"Расчет стоимости аренды ракетки на {hours} часов")
        if hours >= 5:
            return self.hourly_rate * hours * 0.88
        return self.hourly_rate * hours

    def __str__(self) -> str:
        '''Строковое представление ракетки'''
        return f"Теннисная ракетка: {self.name}, Натяжение: {self.__string_tension}"

    def to_dict(self) -> Dict[str, Any]:
        '''Преобразование ракетки в словарь'''
        return {
            'equipment_id': self.equipment_id,
            'name': self.name,
            'condition': self.condition,
            'hourly_rate': self.hourly_rate,
            'string_tension': self.string_tension,
            'is_available': self.is_available
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TennisRacket':
        '''Создание ракетки из словаря'''
        logger.debug(f"Создание TennisRacket из словаря: {data}")
        return cls(*data.values())
    

