# Модуль провайдера Bard

## Обзор

Модуль `src.endpoints.freegpt-webui-ru/g4f/Provider/Providers/Bard.py` предоставляет реализацию провайдера Bard для взаимодействия с моделью Palm2 от Google.

## Подробней

Модуль содержит функции для создания завершений (completions) с использованием API Bard.

## Переменные

*   `url` (str): URL API Bard (значение: `'https://bard.google.com'` ).
*   `model` (list): Список поддерживаемых моделей (значение: `['Palm2']`).
*   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (значение: `False`).
*   `needs_auth` (bool): Указывает, требует ли провайдер аутентификацию (значение: `True`).

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, temperature: float = 0.6, stream: bool = False, **kwargs):
```

**Назначение**: Функция для создания завершения (completion).

**Параметры**:

*   `model` (str): Имя модели.
*   `messages` (list): Список сообщений.
*   `temperature` (float, optional): Температура. Defaults to 0.6.
*   `stream` (bool, optional): Указывает, использовать ли потоковую передачу. Defaults to `False`.
*   `**kwargs`: Дополнительные аргументы.

**Как работает функция**:

1.  Извлекает PSID из куки браузера Chrome для домена `.google.com`.
2.  Форматирует сообщения в строку.
3.  Определяет заголовки для HTTP-запроса.
4.  Получает значение `SNlM0e` из ответа на GET-запрос к `https://bard.google.com/`.
5.  Формирует параметры запроса.
6.  Формирует данные в формате JSON для отправки в API.
7.  Выполняет POST-запрос к API Bard.
8.  Извлекает данные чата из ответа JSON и возвращает их.