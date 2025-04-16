# Модуль провайдера Lockchat

## Обзор

Модуль `src.endpoints.freegpt-webui-ru/g4f/Provider/Providers/Lockchat.py` предоставляет реализацию провайдера Lockchat для взаимодействия с языковыми моделями.

## Подробней

Модуль содержит функции для создания завершений (completions) с использованием API Lockchat.

## Переменные

*   `url` (str): URL API Lockchat (значение: `'http://super.lockchat.app'` ).
*   `model` (list): Список поддерживаемых моделей (значение: `['gpt-4', 'gpt-3.5-turbo']`).
*   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (значение: `True`).
*   `needs_auth` (bool): Указывает, требует ли провайдер аутентификацию (значение: `False`).

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, temperature: float = 0.7, **kwargs):
```

**Назначение**: Функция для создания завершения (completion).

**Параметры**:

*   `model` (str): Имя модели.
*   `messages` (list): Список сообщений.
*   `stream` (bool): Указывает, использовать ли потоковую передачу.
*   `temperature` (float, optional): Температура. Defaults to 0.7.
*   `**kwargs`: Дополнительные аргументы.

**Как работает функция**:

1.  Формирует данные в формате JSON для отправки в API, включая модель, температуру и сообщения.
2.  Определяет заголовки для HTTP-запроса.
3.  Выполняет POST-запрос к API Lockchat.
4.  Итерируется по строкам ответа:

    *   Проверяет наличие ошибки "The model: `gpt-4` does not exist" и, в случае обнаружения, повторяет попытку запроса.
    *   Извлекает содержимое из JSON и возвращает его.