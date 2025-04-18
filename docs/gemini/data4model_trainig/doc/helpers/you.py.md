# Модуль-помощник для провайдера You

## Обзор

Модуль `src.endpoints.freegpt-webui-ru/g4f/Provider/Providers/helpers/you.py` представляет собой скрипт-помощник для взаимодействия с API You.

## Подробней

Модуль содержит код для отправки запроса к API You и обработки потокового ответа. Он используется провайдером You для получения завершений (completions).

## Переменные

*   `config` (dict): Конфигурация, загруженная из аргументов командной строки.
*   `messages` (list): Список сообщений, извлеченный из конфигурации.
*   `prompt` (str): Текст запроса, извлеченный из конфигурации.

## Функции

### `transform`

```python
def transform(messages: list) -> list:
```

**Назначение**: Преобразует список сообщений в формат, ожидаемый API You.

**Параметры**:

*   `messages` (list): Список сообщений в формате `[{'role': 'user' | 'assistant', 'content': str}]`.

**Возвращает**:

*   `list`: Список сообщений в формате `[{'question': str, 'answer': str}]`.

**Как работает функция**:

1.  Итерируется по списку сообщений.
2.  Соединяет сообщения пользователя и ассистента в пары вопрос-ответ.
3.  Добавляет сообщения системы в список результатов.

### `output`

```python
def output(chunk):
```

**Назначение**: Обрабатывает и выводит полученные чанки данных.

**Параметры**:

*   `chunk`: Блок данных для обработки.

**Как работает функция**:

1.  Пытается декодировать чанк из байтов в строку UTF-8.
2.  Извлекает значение `youChatToken` из JSON-объекта.
3.  Выводит извлеченный токен в консоль.

### Основной цикл

```python
while True:
```

**Назначение**: Основной цикл для отправки запроса и обработки ответа.

**Как работает цикл**:

1.  Формирует строку параметров запроса.
2.  Выполняет GET-запрос к API You.
3.  В случае успеха вызывает функцию `output` для обработки каждого чанка ответа.
4.  В случае ошибки выводит сообщение об ошибке и повторяет попытку.