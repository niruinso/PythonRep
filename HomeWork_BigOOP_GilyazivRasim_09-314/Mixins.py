import Logger

logger = Logger.logger

class LoggingMixin:
    '''Миксин для логирования действий'''
    def log_action(self, text: str) -> str:
        '''Метод для логирования действий'''
        logger.info(text)
        return f"[LOG] {text}"

class NotificationMixin:
    '''Миксин для уведомлений'''
    def send_notification(self, text) -> str:
        '''Метод для отправки уведомлений'''
        logger.info(f"Уведомление: {text}")
        return f"[NOTIFICATION] {text}"