# Модуль провайдера Liaobots

## Обзор

Модуль `src.endpoints.freegpt-webui-ru/g4f/Provider/Providers/Liaobots.py` предоставляет реализацию провайдера Liaobots для взаимодействия с языковыми моделями.

## Подробней

Модуль содержит функции для создания завершений (completions) с использованием API Liaobots.

## Переменные

*   `url` (str): URL API Liaobots (значение: `'https://liaobots.com'` ).
*   `model` (list): Список поддерживаемых моделей (значение: `['gpt-3.5-turbo', 'gpt-4']`).
*   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (значение: `True`).
*   `needs_auth` (bool): Указывает, требует ли провайдер аутентификацию (значение: `True`).
*   `models` (dict): Словарь, содержащий информацию о доступных моделях (id, name, maxLength, tokenLimit).

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

1.  Определяет заголовки для HTTP-запроса, включая ключ авторизации (`x-auth-code`).
2.  Формирует данные в формате JSON для отправки в API, включая conversationId, модель, сообщения и промпт.
3.  Выполняет POST-запрос к API Liaobots.
4.  Итерируется по частям ответа и возвращает их в кодировке UTF-8.