## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода реализует класс `Acytoo`, который представляет собой провайдера для асинхронного взаимодействия с API чат-бота `Acytoo`. Класс `Acytoo`  является подклассом `AsyncGeneratorProvider`, определяющим базовую функциональность для работы с асинхронными генераторами ответов.


Шаги выполнения
-------------------------
1. **Инициализация класса:**  
    - Создается экземпляр класса `Acytoo`. 
    - Задаются базовые параметры: `url`, `working`, `supports_message_history`, `supports_gpt_35_turbo`.
2. **Создание асинхронного генератора:**
    - Вызывается метод `create_async_generator` класса `Acytoo`.
    - Передаются следующие аргументы:
        - `model`:  имя модели (например, `gpt-3.5-turbo`).
        - `messages`: список сообщений в формате `Messages`.
        - `proxy`:  (опционально) прокси для подключения к API.
        - `kwargs`: дополнительные аргументы (например, `temperature`).
3. **Отправка запроса к API:**
    - Создается асинхронный клиент `ClientSession`.
    - Отправляется POST-запрос на `/api/completions` API `Acytoo`.
    - Формируется заголовок запроса (`_create_header`).
    - Формируется JSON-payload запроса (`_create_payload`).
    - Обрабатываются ошибки (с помощью `response.raise_for_status`).
4. **Получение ответа в виде потока:**
    - Используется `response.content.iter_any()` для итерации по потоку ответов.
    - Декодируется и возвращается каждый полученный блок.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Acytoo import Acytoo
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание экземпляра класса Acytoo
acytoo_provider = Acytoo()

# Формирование списка сообщений
messages: Messages = [
    {"role": "user", "content": "Привет, как дела?"},
]

# Получение ответа от API Acytoo
async for stream in acytoo_provider.create_async_generator(model='gpt-3.5-turbo', messages=messages):
    print(stream)
```