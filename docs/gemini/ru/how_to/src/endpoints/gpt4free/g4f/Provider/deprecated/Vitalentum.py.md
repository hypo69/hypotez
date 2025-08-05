## Как использовать этот блок кода
========================================================================================

Описание
-------------------------
Этот блок кода реализует класс `Vitalentum`, который является асинхронным генератором ответов для модели `GPT-3.5 Turbo` на платформе Vitalentum.io. 

Шаги выполнения
-------------------------
1. **Инициализация класса `Vitalentum`**: Класс создается с помощью метода `create_async_generator`, который принимает следующие аргументы:
    - `model`: название модели, например, "gpt-3.5-turbo".
    - `messages`: список сообщений в формате `Messages`.
    - `proxy`: (опционально) прокси-сервер для запросов.
    - `**kwargs`: (опционально) дополнительные параметры для запроса к API.
2. **Создание заголовков запроса**: Метод `create_async_generator` создает словарь `headers` с заголовками, необходимыми для запроса к API Vitalentum.io.
3. **Формирование тела запроса**: Создается JSON-объект `conversation` с историей сообщений и передается в словарь `data` вместе с параметрами `temperature` и `**kwargs`.
4. **Отправка запроса**: Используется `aiohttp.ClientSession` для отправки POST-запроса к API Vitalentum.io.
5. **Обработка ответа**: После получения ответа от API Vitalentum.io, код обрабатывает его, извлекая текст ответа и передавая его через генератор `yield`.
6. **Генерация ответа**: Генератор `yield` выдает текст ответа по частям, пока не будет достигнут конец ответа.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Vitalentum import Vitalentum
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание списка сообщений
messages: Messages = [
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Хорошо, спасибо! А у тебя?"},
]

# Создание экземпляра Vitalentum
async_generator = Vitalentum.create_async_generator(
    model="gpt-3.5-turbo",
    messages=messages,
)

# Получение ответа от генератора
async for chunk in async_generator:
    print(chunk)

```