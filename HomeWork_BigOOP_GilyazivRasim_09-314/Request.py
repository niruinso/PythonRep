import Logger

logger = Logger.logger

class Request:
    '''Класс запроса на изменение'''
    def __init__(self, type: str, newprice: float, approved: bool = False):
        '''Конструктор запроса'''
        self.__type = type
        self.__approved = approved
        self.newprice = newprice
        logger.debug(f"Создан запрос типа {type} на сумму {newprice}")

    @property
    def type(self) -> str:
        '''Геттер для типа запроса'''
        return self.__type

    @type.setter
    def type(self, type: str) -> None:
        '''Сеттер для типа запроса'''
        logger.debug(f"Изменение типа запроса с {self.__type} на {type}")
        self.__type = type

    @property
    def approved(self) -> bool:
        '''Геттер для статуса одобрения'''
        return self.__approved

    @approved.setter
    def approved(self, approved: bool) -> None:
        '''Сеттер для статуса одобрения'''
        if not self.__approved:
            logger.info(f"Изменение статуса одобрения запроса с {self.__approved} на {approved}")
            self.__approved = approved