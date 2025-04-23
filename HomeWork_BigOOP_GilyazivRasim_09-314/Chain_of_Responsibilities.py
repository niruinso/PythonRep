import Logger
from abc import ABC, abstractmethod
from Errors import PermissionDeniedError

logger = Logger.logger

def check_permissions(required_permission):
    '''Декоратор для проверки прав доступа'''
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if required_permission > self.access:
                logger.warning(f"Попытка выполнить действие без достаточных прав (Требуется: {required_permission}, Имеется: {self.access})")
                raise PermissionDeniedError
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

class ChangeHandler(ABC):
    '''Абстрактный класс обработчика запросов'''
    def __init__(self, next=None):
        '''Конструктор обработчика'''
        self._next = next

    @abstractmethod
    def handle_request(self, request):
        '''Абстрактный метод обработки запроса'''
        pass

class Operator(ChangeHandler):
    '''Класс оператора'''
    def handle_request(self, request):
        '''Обработка запроса оператором'''
        if request.type == 'easy':
            logger.info(f"Оператор одобрил запрос типа {request.type}")
            request.approved = True
            return True
        elif self._next:
            return self._next.handle_request(request)
        logger.warning(f"Оператор не смог обработать запрос типа {request.type}")
        return False

class Manager(ChangeHandler):
    '''Класс менеджера'''
    def handle_request(self, request):
        '''Обработка запроса менеджером'''
        if (request.type == 'easy' or request.type == 'average'):
            logger.info(f"Менеджер одобрил запрос типа {request.type}")
            request.approved = True
            return True
        elif self._next:
            return self._next.handle_request(request)
        logger.warning(f"Менеджер не смог обработать запрос типа {request.type}")
        return False

class Admin(ChangeHandler):
    '''Класс администратора'''
    def handle_request(self, request):
        '''Обработка запроса администратором'''
        logger.info(f"Администратор одобрил запрос типа {request.type}")
        request.approved = True
        return True

class Salesman:
    '''Класс продавца'''
    def __init__(self, access: int) -> None:
        '''Конструктор продавца'''
        self.access = access
        logger.info(f"Создан продавец с уровнем доступа {access}")

    @check_permissions(3)
    def makesale(self, rentalprocess, request=None):
        '''Метод оформления продажи'''
        logger.info(f"Продавец с уровнем доступа {self.access} оформляет аренду")
        return rentalprocess.rent_equipment(request)
