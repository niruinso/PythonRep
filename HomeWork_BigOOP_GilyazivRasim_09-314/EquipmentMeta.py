import Logger

logger = Logger.logger

class EquipmentMeta(type):
    '''Метакласс для контроля создания классов оборудования'''
    registry = {}

    def __new__(cls, name, bases, namespace):
        '''Авторегистрация классов оборудования'''
        new_class = super().__new__(cls, name, bases, namespace)
        if name != 'SportEquipment':
            cls.registry[name.lower()] = new_class
            logger.debug(f"Зарегистрирован класс оборудования: {name}")
        return new_class