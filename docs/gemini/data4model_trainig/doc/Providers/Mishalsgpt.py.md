# Модуль провайдера Mishalsgpt

## Обзор

Модуль `src.endpoints.freegpt-webui-ru/g4f/Provider/Providers/Mishalsgpt.py` предоставляет реализацию провайдера Mishalsgpt для взаимодействия с языковой моделью.

## Подробней

Модуль содержит функции для создания завершений (completions) с использованием API Mishalsgpt.

## Переменные

*   `url` (str): URL API Mishalsgpt (значение: `'https://mishalsgpt.vercel.app'` ).
*   `model` (list): Список поддерживаемых моделей (значение: `['gpt-3.5-turbo-16k-0613', 'gpt-3.5-turbo']`).
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

1.  Определяет заголовки для HTTP-запроса.
2.  Формирует данные в формате JSON для отправки в API, включая модель, температуру и сообщения.
3.  Выполняет POST-запрос к API Mishalsgpt.
4.  Извлекает сообщение из ответа JSON и возвращает его.