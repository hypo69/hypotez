# Модуль ChatgptDuo

## Обзор

Модуль `ChatgptDuo` предоставляет асинхронный класс `ChatgptDuo` для взаимодействия с моделью ChatgptDuo. 

## Подробней

`ChatgptDuo` - это асинхронный провайдер, который позволяет взаимодействовать с моделью ChatgptDuo и получать ответы на запросы в виде текста.

## Классы

### `class ChatgptDuo`

**Описание**: Класс `ChatgptDuo` реализует асинхронный провайдер для работы с ChatgptDuo.

**Наследует**: `AsyncProvider`

**Атрибуты**:

- `url` (str): URL-адрес API ChatgptDuo.
- `supports_gpt_35_turbo` (bool):  Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo.
- `working` (bool): Указывает, доступен ли провайдер для работы.

**Методы**:

- `create_async`: Создает асинхронный сеанс с ChatgptDuo и возвращает ответ на запрос.
- `get_sources`: Возвращает список источников, найденных ChatgptDuo.

#### `create_async(model: str, messages: Messages, proxy: str = None, timeout: int = 120, **kwargs) -> str`

**Назначение**: Создает асинхронный сеанс с ChatgptDuo и отправляет запрос.

**Параметры**:

- `model` (str): Название модели ChatgptDuo.
- `messages` (Messages): Список сообщений для отправки в ChatgptDuo.
- `proxy` (str, optional):  Прокси-сервер для подключения.
- `timeout` (int, optional): Время ожидания ответа.
- `kwargs`: Дополнительные аргументы.

**Возвращает**:

- `str`:  Ответ модели ChatgptDuo в виде текста.

**Как работает функция**:

- Метод `create_async` создает асинхронный сеанс с использованием библиотеки `StreamSession` для обработки запросов.
- Он формирует запрос к ChatgptDuo, используя URL-адрес API и отправляет его через HTTP POST-запрос.
- После получения ответа метод проверяет статус запроса.
- Если запрос был успешным, метод извлекает ответ из JSON-данных и возвращает его.

**Примеры**:

```python
async def main():
    messages = [
        {"role": "user", "content": "Привет, как дела?"},
    ]
    response = await ChatgptDuo.create_async(model="gpt-3.5-turbo", messages=messages)
    print(response)
```


#### `get_sources() -> list`

**Назначение**:  Возвращает список источников, найденных ChatgptDuo.

**Параметры**: 

- Отсутствуют.

**Возвращает**:

- `list`: Список источников в виде словаря, содержащего название, URL и фрагмент текста из источника.

**Как работает функция**:

- Метод `get_sources` возвращает список источников, который был получен в предыдущем запросе к ChatgptDuo.


## Параметры класса

- `url` (str): URL-адрес API ChatgptDuo.
- `supports_gpt_35_turbo` (bool):  Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo.
- `working` (bool): Указывает, доступен ли провайдер для работы.



```markdown