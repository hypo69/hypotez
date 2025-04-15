# Модуль `Raycast.py`

## Обзор

Модуль предоставляет класс `Raycast`, который является провайдером для взаимодействия с моделями GPT через API Raycast. Raycast - это платформа, предоставляющая инструменты для автоматизации и улучшения рабочих процессов. Этот модуль позволяет использовать модели, такие как "gpt-3.5-turbo" и "gpt-4", через API Raycast для генерации текста и выполнения других задач, связанных с обработкой естественного языка.

## Подробнее

Модуль предназначен для интеграции с платформой Raycast и обеспечивает возможность использования моделей GPT для различных задач, таких как чат-боты, генерация контента и т.д. Он поддерживает потоковую передачу данных, что позволяет получать результаты в режиме реального времени. Для работы требуется аутентификация через токен.

## Классы

### `Raycast`

**Описание**: Класс `Raycast` является провайдером, который реализует взаимодействие с API Raycast для использования моделей GPT.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `url` (str): URL платформы Raycast (`https://raycast.com`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (значение `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с провайдером (значение `True`).
- `working` (bool): Указывает, работает ли провайдер в данный момент (значение `False`).
- `models` (list): Список поддерживаемых моделей (например, `gpt-3.5-turbo` и `gpt-4`).

**Методы**:
- `create_completion()`: Метод для создания завершения текста с использованием API Raycast.

## Методы класса

### `create_completion`

```python
@staticmethod
def create_completion(
    model: str,
    messages: Messages,
    stream: bool,
    proxy: str = None,
    **kwargs,
) -> CreateResult:
    """
    Создает завершение текста с использованием API Raycast.

    Args:
        model (str): Имя используемой модели (например, "gpt-3.5-turbo").
        messages (Messages): Список сообщений для передачи в модель.
        stream (bool): Указывает, использовать ли потоковую передачу данных.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы, такие как токен аутентификации.

    Returns:
        CreateResult: Результат завершения текста.

    Raises:
        ValueError: Если не предоставлен токен аутентификации.

    Внутренние функции:
        Отсутствуют.

    Как работает функция:
    - Проверяет наличие токена аутентификации в аргументах `kwargs`.
    - Формирует заголовки запроса, включая токен аутентификации.
    - Преобразует список сообщений в формат, ожидаемый API Raycast.
    - Формирует данные запроса, включая модель, сообщения и другие параметры.
    - Отправляет POST-запрос к API Raycast с использованием библиотеки `requests`.
    - Итерируется по ответу, извлекая токены завершения текста.
    - Возвращает токены завершения текста с использованием генератора.

    Примеры:
        Пример 1: Успешное создание ответа с использованием токена
        >>> Raycast.create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}], stream=True, auth='YOUR_API_KEY')
        <generator object AbstractProvider.create_completion at 0x...>

        Пример 2: Вызов исключения из-за отсутствия аутентификации
        >>> Raycast.create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}], stream=True)
        ValueError: Raycast needs an auth token, pass it with the `auth` parameter
    """
```

## Параметры класса

- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для передачи в модель.
- `stream` (bool): Указывает, использовать ли потоковую передачу данных.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, такие как токен аутентификации.

**Примеры**:

Пример 1:

```python
Raycast.create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}], stream=True, auth='YOUR_API_KEY')
```

Пример 2:

```python
try:
    Raycast.create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}], stream=True)
except ValueError as ex:
    print(f"Ошибка: {ex}")