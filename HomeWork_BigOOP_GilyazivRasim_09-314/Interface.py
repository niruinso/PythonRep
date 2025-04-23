from EquipmentMeta import EquipmentMeta
from Customer import Customer
from abc import abstractmethod
from datetime import datetime

class Rentable(metaclass=EquipmentMeta):
    '''Интерфейс для арендуемых объектов'''
    @abstractmethod
    def rent_equipment(self, customer: 'Customer', start_time: datetime):
        '''Абстрактный метод для аренды оборудования'''
        pass

class Reportable(metaclass=EquipmentMeta):
    '''Интерфейс для генерации отчетов'''
    @abstractmethod
    def generate_report(self) -> str:
        '''Абстрактный метод для генерации отчета'''
        pass
    