## Как использовать блок кода `Routes.tegram_message_handler`
=========================================================================================

Описание
-------------------------
Блок кода `Routes.tegram_message_handler` инициализирует обработчик сообщений для Telegram-бота. Он создает экземпляр класса `BotHandler` и получает ссылку на метод `handle_message`, который обрабатывает входящие сообщения от Telegram.

Шаги выполнения
-------------------------
1. **Инициализация обработчика**: Создается экземпляр класса `BotHandler` с именем `bot_nahdlers`.
2. **Получение обработчика сообщений**: Из обработчика `bot_nahdlers` извлекается метод `handle_message` и присваивается переменной `telega_message_handler`.

Пример использования
-------------------------

```python
from src.fast_api.routes import Routes

# Создание экземпляра класса Routes
routes = Routes()

# Получение обработчика сообщений Telegram
telega_message_handler = routes.tegram_message_handler()

# Использование обработчика для обработки сообщений 
# (Пример - отправка сообщения в Telegram):
message = "Привет!"
telega_message_handler(message) 
```