# Модуль провайдера Forefront

## Обзор

Модуль `src.endpoints.freegpt-webui-ru/g4f/Provider/Providers/Forefront.py` предоставляет реализацию провайдера Forefront для взаимодействия с языковой моделью.

## Подробней

Модуль содержит функции для создания завершений (completions) с использованием API Forefront.

## Переменные

*   `url` (str): URL API Forefront (значение: `'https://forefront.com'` ).
*   `model` (list): Список поддерживаемых моделей (значение: `['gpt-3.5-turbo']`).
*   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (значение: `True`).
*   `needs_auth` (bool): Указывает, требует ли провайдер аутентификацию (значение: `False`).

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
```

**Назначение**: Функция для создания завершения (completion).

**Параметры**:

*   `model` (str): Имя модели.
*   `messages` (list): Список сообщений.
*   `stream` (bool): Указывает, использовать ли потоковую передачу.
*   `**kwargs`: Дополнительные аргументы.

**Как работает функция**:

1.  Формирует данные в формате JSON для отправки в API.
2.  Выполняет POST-запрос к API Forefront.
3.  Итерируется по токенам в потоке ответа и возвращает их.