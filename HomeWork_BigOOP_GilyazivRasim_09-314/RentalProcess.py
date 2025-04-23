import Logger
from abc import abstractmethod
from Mixins import *
from SportsEquipment import Rentable, Reportable
from SportsEquipment import SportEquipment
from Customer import Customer
from Request import Request
from typing import Optional
from datetime import datetime
from Chain_of_Responsibilities import *
from Rental import Rental
from typing import Dict
from Errors import *

logger = Logger.logger

class RentalProcess(Rental, Rentable, Reportable, LoggingMixin):
    '''Абстрактный класс процесса аренды'''
    def __init__(self, rental_id: str, customer: Customer, equipment: SportEquipment
                 , start_time: datetime, end_time: Optional[datetime] = None, extras: Optional[Dict[str, float]] = None) -> None:
        '''Конструктор процесса аренды'''
        super().__init__(rental_id, customer, equipment, start_time, end_time, extras)

    def rent_equipment(self, request: Optional[Request] = None) -> 'Rental':
        '''Метод аренды оборудования'''
        if self.check():
            rent = self.create()
            price = rent.total_cost
            rent.total_cost_approved = self.confirm(price, request)
            return rent
        else:
            logger.error("Попытка арендовать недоступное оборудование")
            raise RentalNotFoundError("Инвентарь недоступен")

    @abstractmethod
    def check(self):
        '''Абстрактный метод проверки'''
        pass

    @abstractmethod
    def create(self):
        '''Абстрактный метод создания аренды'''
        pass

    @abstractmethod
    def confirm(self):
        '''Абстрактный метод подтверждения'''
        pass

class OnlineRentalProcess(RentalProcess):
    '''Класс онлайн процесса аренды'''
    def __init__(self, rental_id: str, customer: Customer, equipment: SportEquipment
                 , start_time: datetime, end_time: Optional[datetime] = None, extras: Optional[Dict[str, float]] = None) -> None:
        '''Конструктор онлайн процесса'''
        super().__init__(rental_id, customer, equipment, start_time, end_time, extras)

    def rent_equipment(self, request: Optional[Request] = None) -> 'Rental':
        '''Метод онлайн аренды'''
        logger.info("Начало онлайн процесса аренды")
        rent = super().rent_equipment(request)
        print(rent.generate_report())
        return rent

    def check(self):
        '''Метод проверки для онлайн аренды'''
        logger.debug("Онлайн проверка доступности оборудования")
        return self.equipment.is_available

    def create(self):
        '''Метод создания онлайн аренды'''
        logger.debug("Подсчет базовой стоимости онлайн")
        rent = self.equipment.rent_equipment(self.customer_info, self.start_time, self.end_time, self.extras)
        return rent

    def confirm(self, price, request):
        '''Метод подтверждения для онлайн аренды'''
        logger.debug("Согласование цены с персоналом онлайн")
        if request:
            price = request.newprice if Operator(Manager(Admin())).handle_request(request) else price
        return price

class OfflineRentalProcess(RentalProcess):
    '''Класс оффлайн процесса аренды'''
    def __init__(self, rental_id: str, customer: Customer, equipment: SportEquipment
                 , start_time: datetime, end_time: Optional[datetime] = None, extras: Optional[Dict[str, float]] = None) -> None:
        '''Конструктор онлайн процесса'''
        super().__init__(rental_id, customer, equipment, start_time, end_time, extras)

    def rent_equipment(self, request: Optional[Request] = None) -> 'Rental':
        '''Метод оффлайн аренды'''
        logger.info("Начало оффлайн процесса аренды")
        rent = super().rent_equipment(request)
        print(rent.generate_report())
        return rent

    def check(self):
        '''Метод проверки для оффлайн аренды'''
        logger.debug("Оффлайн проверка доступности оборудования")
        return self.equipment.is_available

    def create(self):
        '''Метод создания оффлайн аренды'''
        logger.debug("Подсчет базовой стоимости оффлайн")
        rent = self.equipment.rent_equipment(self.customer_info, self.start_time, self.end_time, self.extras)
        return rent

    def confirm(self, price, request):
        '''Метод подтверждения для оффлайн аренды'''
        logger.debug("Согласование цены с персоналом оффлайн")
        if request:
            price = request.newprice if Operator(Manager(Admin())).handle_request(request) else price
        return price
