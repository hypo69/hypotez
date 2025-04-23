### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Данный блок кода отвечает за настройку обработчика сообщений Telegram-бота в приложении. Он инициализирует класс `BotHandler` и назначает метод `handle_message` этого класса как обработчик сообщений Telegram.

Шаги выполнения
-------------------------
1. **Инициализация `BotHandler`**: Создается экземпляр класса `BotHandler`, который содержит логику обработки сообщений от Telegram.
2. **Назначение обработчика**: Метод `handle_message` из экземпляра `BotHandler` присваивается переменной `telega_message_handler`. Это подготавливает функцию для обработки входящих сообщений Telegram.

Пример использования
-------------------------

```python
from src.endpoints.bots.telegram.bot_handlers import BotHandler

class Routes:
    def tegram_message_handler(self):
        """ """
        bot_handlers = BotHandler()
        telega_message_handler = bot_handlers.handle_message

# Пример использования класса Routes:
routes = Routes()
routes.tegram_message_handler()
# Теперь telega_message_handler содержит функцию, готовую к обработке сообщений Telegram.
```