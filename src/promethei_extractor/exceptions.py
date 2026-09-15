class ExtractorError(Exception):
    """Базовое исключение"""


class AuthenticationError(ExtractorError):
    """Исключение аутентификации во время парсинга"""


class PrometheiApiError(ExtractorError):
    """Прометей недоступен или ответил сетевой ошибкой"""


class MalformedResponseError(ExtractorError):
    """Ответ Прометея не удалось разобрать даже с recover=True"""


class ConfigurationError(ExtractorError):
    """Некорректная конфигурация: не заданы логин/пароль, некорректный .env или его отсутствие и т.п."""


class OutputWriteError(ExtractorError):
    """Не удалось записать результат на диск: нет прав, не существует путь, диск заполнен"""

