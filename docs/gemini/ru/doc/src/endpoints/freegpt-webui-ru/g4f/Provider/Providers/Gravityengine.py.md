# Модуль Gravityengine 

## Обзор

Модуль Gravityengine предоставляет реализацию класса `_create_completion` для работы с API GravityEngine.  

## Подробнее

Модуль содержит набор функций и параметров, необходимых для взаимодействия с API GravityEngine для создания ответов от моделей искусственного интеллекта.  

## Классы

### `_create_completion`

**Описание**:  Функция для создания ответов от модели ИИ, доступной через API GravityEngine.

**Параметры**:

- `model` (str): Название модели ИИ, например, `gpt-3.5-turbo-16k`
- `messages` (list): Список сообщений, отправляемых модели для генерации ответа.
- `stream` (bool):  Флаг, указывающий, нужно ли возвращать ответ в виде потока.
- `kwargs`: Дополнительные параметры, передаваемые в API GravityEngine.

**Возвращает**: 

- `Generator[str, None, None]`:  Генератор,  возвращающий части ответа от модели в виде строк.

**Примеры**:
```python
from hypotez.src.endpoints.freegpt-webui-ru.g4f.Provider.Providers.Gravityengine import _create_completion

model = 'gpt-3.5-turbo-16k'
messages = [{'role': 'user', 'content': 'Привет, как дела?'}]

# Генерация ответа с использованием потока
for chunk in _create_completion(model, messages, stream=True):
    print(chunk)