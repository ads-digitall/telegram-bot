"""
modules/bot/handler_registry.py

Модуль для централизованного хранения и управления обработчиками Telegram-бота.
Предоставляет класс HandlerRegistry, который позволяет регистрировать обработчики,
получать список зарегистрированных обработчиков и производить их очистку.
"""

import logging

logger = logging.getLogger(__name__)

class HandlerRegistry:
    def __init__(self):
        # Словарь для хранения обработчиков: ключ — уникальное имя, значение — обработчик.
        self._handlers = {}

    def register(self, name: str, handler):
        """
        Регистрирует обработчик с заданным именем.

        Args:
            name (str): Уникальное имя обработчика.
            handler: Функция или объект, представляющий обработчик.
        """
        if name in self._handlers:
            logger.warning(f"Обработчик с именем '{name}' уже зарегистрирован. Он будет перезаписан.")
        self._handlers[name] = handler
        logger.info(f"Обработчик '{name}' успешно зарегистрирован.")

    def get_handler(self, name: str):
        """
        Возвращает обработчик по его имени.

        Args:
            name (str): Имя обработчика.

        Returns:
            Обработчик, либо None если обработчик не найден.
        """
        return self._handlers.get(name)

    def get_all_handlers(self):
        """
        Возвращает копию словаря всех зарегистрированных обработчиков.

        Returns:
            dict: Словарь, где ключи — имена обработчиков, а значения — сами обработчики.
        """
        return self._handlers.copy()

    def clear(self):
        """
        Очищает реестр обработчиков.
        """
        self._handlers.clear()
        logger.info("Реестр обработчиков очищен.")

# Глобальный экземпляр реестра, который можно импортировать и использовать в других модулях
handler_registry = HandlerRegistry()

__all__ = ["HandlerRegistry", "handler_registry"]
