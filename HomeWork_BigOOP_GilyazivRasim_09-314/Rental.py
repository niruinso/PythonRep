import Logger
from Mixins import *
from typing import Dict, Any, Optional
from SportsEquipment import SportEquipment, Bicycle, Skis, TennisRacket
from Interface import Reportable
from Customer import Customer
from datetime import datetime

logger = Logger.logger

class Rental(Reportable, LoggingMixin, NotificationMixin):
    '''Класс аренды'''
    def __init__(self,rental_id: str, customer: Customer, equipment: SportEquipment
                 , start_time: datetime, end_time: Optional[datetime] = None, extras: Optional[Dict[str, float]] = None):
        '''Конструктор аренды'''
        self.__rental_id = rental_id
        self.__customer_info = customer
        self.__equipment = equipment
        self.__start_time = start_time
        self.__end_time = end_time
        self.__extras: Dict[str, float] = extras
        self.__total_cost: Optional[float] = None
        self.__total_cost_approved: Optional[float] = None
        logger.info(f"Создана аренда: {rental_id} для клиента {customer.name}")

    @property
    def rental_id(self) -> str:
        '''Геттер для ID аренды'''
        return self.__rental_id

    @rental_id.setter
    def rental_id(self, rental_id: str) -> None:
        '''Сеттер для ID аренды'''
        logger.debug(f"Изменение ID аренды с {self.__rental_id} на {rental_id}")
        self.__rental_id = rental_id

    @property
    def customer_info(self) -> Customer:
        '''Геттер для информации о клиенте'''
        return self.__customer_info

    @customer_info.setter
    def customer_info(self, customer_info: Customer) -> None:
        '''Сеттер для информации о клиенте'''
        logger.debug(f"Изменение информации о клиенте с {self.__customer_info.name} на {customer_info.name}")
        self.__customer_info = customer_info

    @property
    def equipment(self) -> SportEquipment:
        '''Геттер для информации об оборудовании'''
        return self.__equipment

    @equipment.setter
    def equipment(self, equipment: SportEquipment) -> None:
        '''Сеттер для информации об оборудовании'''
        logger.debug(f"Изменение оборудования с {self.__equipment.name} на {equipment.name}")
        self.__equipment = equipment

    @property
    def start_time(self) -> datetime:
        '''Геттер для времени начала аренды'''
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time: datetime) -> None:
        '''Сеттер для времени начала аренды'''
        logger.debug(f"Изменение времени начала аренды с {self.__start_time} на {start_time}")
        self.__start_time = start_time

    @property
    def end_time(self) -> datetime:
        '''Геттер для времени окончания аренды'''
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time: datetime) -> None:
        '''Сеттер для времени окончания аренды'''
        if self.__end_time is None:
            logger.debug(f"Установка времени окончания аренды: {end_time}")
            self.__end_time = end_time

    @property
    def total_cost(self) -> float:
        '''Геттер для общей стоимости аренды'''
        if self.__total_cost is None:
            self.calculate_total()
        return self.__total_cost

    @property
    def total_cost_approved(self) -> float:
        '''Геттер для утвержденной стоимости'''
        return self.__total_cost_approved
    
    @property
    def extras(self):
        '''Геттер для дополнительных элементов аренды'''
        return self.__extras

    @total_cost_approved.setter
    def total_cost_approved(self, total_cost: float) -> None:
        '''Сеттер для утвержденной стоимости'''
        if self.__total_cost_approved is None:
            logger.info(f"Утверждение стоимости аренды: {total_cost}")
            self.__total_cost_approved = total_cost

    def add_extra(self, service: str, price: float) -> None:
        '''Добавление дополнительной услуги'''
        logger.info(f"Добавление дополнительной услуги: {service} за {price}")
        self.__extras[service] = price
        self.__total_cost = None

    def remove_extra(self, service: str) -> None:
        '''Удаление дополнительной услуги'''
        if service in self.__extras:
            logger.info(f"Удаление дополнительной услуги: {service}")
            del self.__extras[service]
            self.__total_cost = self.calculate_total()

    def calculate_total(self) -> float:
        '''Расчет общей стоимости аренды'''
        logger.debug("Расчет общей стоимости аренды")
        if self.__total_cost is not None:
            return self.__total_cost

        hours = (self.end_time - self.start_time).total_seconds() / 3600
        base_cost = self.equipment.calculate_rental_cost(hours)
        extras_cost = 0
        if self.__extras is not None:
            extras_cost = sum(self.__extras.values())
        self.__total_cost = base_cost + extras_cost
        logger.debug(f"Общая стоимость аренды: {self.__total_cost}")
        return self.__total_cost

    def __str__(self):
        '''Строковое представление аренды'''
        self.total_cost_approved = self.calculate_total()
        duration = (self.end_time - self.start_time).total_seconds() / 3600 if self.end_time is not None else "не завершена"
        return (f"Отчет по аренде #{self.rental_id}\n" +
                f"Клиент: {self.customer_info}\n" +
                f"Инвентарь: {self.equipment}\n" +
                f"Длительность: {duration} ч\n" +
                f"Доп. услуги: {', '.join(self.__extras.keys()) if self.__extras else 'нет'}\n" +
                f"Общая стоимость: {self.total_cost_approved}.")

    def generate_report(self) -> str:
        '''Генерация отчета по аренде'''
        logger.info(f"Генерация отчета по аренде {self.rental_id}")
        return self.__str__()

    def to_dict(self) -> Dict[str, Any]:
        '''Преобразование аренды в словарь'''
        return {
            'rental_id': self.rental_id,
            'customer_info': self.customer_info.to_dict(),
            'equipment': self.equipment.to_dict(),
            'start_time': self.start_time.timestamp(),
            'end_time': self.end_time.timestamp() if self.end_time else None,
            'extras': self.__extras
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rental':
        '''Создание аренды из словаря'''
        logger.debug(f"Создание Rental из словаря: {data}")
        dict = list(data.values())
        eq = dict[2]
        res_dict = None
        if 'length' in eq.keys():
            res_dict = Skis.from_dict(eq)
        elif 'type' in eq.keys():
            res_dict = Bicycle.from_dict(eq)
        elif 'string_tension' in eq.keys():
            res_dict = TennisRacket.from_dict(eq)
        else:
            res_dict = SportEquipment.from_dict(eq)

        return cls(dict[0],
                 Customer.from_dict(dict[1]),
                 res_dict,
                 datetime.fromtimestamp(dict[3]),
                 datetime.fromtimestamp(dict[4]) if dict[4] else None)