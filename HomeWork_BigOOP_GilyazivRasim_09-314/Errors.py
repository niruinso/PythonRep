class PermissionDeniedError(Exception):
    '''Класс для определения ошибки недостаточных прав'''
    def __init__(self, msg="Нет прав доступа"):
        self.msg = msg


class InvalidEquipmentError(Exception):
    '''Класс для определения ошибки некорректных данных инвентаря'''
    def __init__(self, msg="Инвентарь содержит некорректные данные"):
        self.msg = msg
        super().__init__(msg)


class RentalNotFoundError(Exception):
    '''Класс для определения ошибки отсутствия аренды'''
    def __init__(self, msg="Аренда не найдена"):
        self.msg = msg
        super().__init__(msg)