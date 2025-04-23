import Logger
from EquipmentMeta import EquipmentMeta
from Errors import *

logger = Logger.logger

class EquipmentFactory:
    '''Фабрика для создания оборудования'''
    @staticmethod
    def create_equipment(equipment_type: str, *args, **kwargs):
        '''Статический метод для создания оборудования'''
        equipment = EquipmentMeta.registry.get(equipment_type.lower())
        if not equipment:
            logger.error(f"Неизвестный тип инвентаря: {equipment_type}")
            raise InvalidEquipmentError(f'Неизвестный тип инвентаря: {equipment_type}')
        logger.info(f"Создание оборудования типа {equipment_type}")
        return equipment(*args, **kwargs)
