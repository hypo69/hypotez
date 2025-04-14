# Модуль VoiGpt

## Обзор

Модуль `VoiGpt` предоставляет класс `VoiGpt`, который является провайдером для взаимодействия с сайтом VoiGpt.com.
Этот модуль позволяет генерировать ответы на основе предоставленных сообщений, используя модель `gpt-3.5-turbo` или другую указанную модель.
Для работы с этим провайдером необходимо получить `csrf token/cookie` с сайта voigpt.com.

## Подробней

Этот модуль предназначен для интеграции с API VoiGpt.com, предоставляя удобный интерфейс для отправки сообщений и получения ответов.
Он включает в себя автоматическое получение `access_token` (csrftoken) из cookies, если он не был предоставлен.

## Классы

### `VoiGpt`

**Описание**: Класс `VoiGpt` является провайдером для VoiGpt.com.

**Принцип работы**:
Класс наследуется от `AbstractProvider` и предоставляет метод `create_completion` для отправки сообщений и получения ответов от API VoiGpt.com.
Если `access_token` не предоставлен, он автоматически получает его из cookies сайта.

**Атрибуты**:

- `url` (str): URL сайта VoiGpt.com.
- `working` (bool): Флаг, указывающий, работает ли провайдер.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий, поддерживает ли провайдер модель `gpt-3.5-turbo`.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных.
- `_access_token` (str): Приватный атрибут для хранения `access_token`.

**Методы**:
- `create_completion`: Отправляет сообщения и получает ответы от API VoiGpt.com.

## Функции

### `create_completion`

```python
@classmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    proxy: str = None,
    access_token: str = None,
    **kwargs
) -> CreateResult:
    """
    Отправляет сообщения и получает ответы от API VoiGpt.com.

    Args:
        model (str): Модель для использования.
        messages (Messages): Сообщения для отправки.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу данных.
        proxy (str, optional): Прокси для использования. По умолчанию `None`.
        access_token (str, optional): Access token для использования. По умолчанию `None`.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        CreateResult: Объект CreateResult с результатом.

    Raises:
        RuntimeError: Если получен некорректный ответ от сервера.
    """
```

**Назначение**:
Метод `create_completion` отправляет сообщения в API VoiGpt.com и возвращает ответ.
Он автоматически получает `access_token` из cookies, если он не был предоставлен.

**Параметры**:

- `cls`: Ссылка на класс `VoiGpt`.
- `model` (str): Модель для использования. Если не указана, используется `gpt-3.5-turbo`.
- `messages` (Messages): Список сообщений для отправки.
- `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `access_token` (str, optional): Токен доступа для использования. Если не указан, пытается получить из cookies. По умолчанию `None`.
- `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**:
- `CreateResult`: Объект, содержащий результат запроса.

**Вызывает исключения**:
- `RuntimeError`: Если получен некорректный ответ от сервера.

**Как работает функция**:

1. **Инициализация**:
   - Если модель не указана, устанавливает `model` в `gpt-3.5-turbo`.
   - Если `access_token` не предоставлен, пытается получить его из cookies сайта VoiGpt.com.

2. **Получение `access_token`**:
   - Если `access_token` не был передан в аргументах и не был сохранен в `cls._access_token`, функция отправляет GET-запрос на главную страницу VoiGpt.com, чтобы получить `csrftoken` из cookies.
   - Полученный `csrftoken` сохраняется в `cls._access_token` для дальнейшего использования.

3. **Формирование заголовков**:
   - Формирует заголовки запроса, включая `csrftoken` из cookies.

4. **Формирование полезной нагрузки (payload)**:
   - Формирует JSON-payload с сообщениями для отправки.

5. **Отправка запроса**:
   - Отправляет POST-запрос на URL `https://voigpt.com/generate_response/` с заголовками и полезной нагрузкой.

6. **Обработка ответа**:
   - Пытается распарсить JSON-ответ от сервера.
   - Извлекает текст ответа из поля `"response"` и возвращает его.
   - Если происходит ошибка при парсинге JSON, вызывает исключение `RuntimeError` с текстом ответа от сервера.

```
    Начало
    │
    ├── Проверка model: model == None?
    │   └── Да: model = "gpt-3.5-turbo"
    │
    ├── Проверка access_token: access_token == None?
    │   └── Да: access_token = cls._access_token
    │
    ├── Проверка access_token: access_token == None?
    │   └── Да: 
    │       ├──  GET запрос на cls.url для получения csrftoken
    │       └──  Сохранение csrftoken в access_token и cls._access_token
    │
    ├── Формирование заголовков запроса с access_token
    │
    ├── Формирование payload с сообщениями
    │
    ├── POST запрос на f"{cls.url}/generate_response/"
    │
    ├── Обработка ответа
    │   └── Попытка парсинга JSON ответа
    │       ├── Успех: Извлечение текста ответа из поля "response"
    │       └── Неудача: Вызов исключения RuntimeError с текстом ответа
    │
    └── Конец
```

**Примеры**:

```python
from typing import List, Dict

# Пример 1: Использование с минимальными параметрами
messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, VoiGpt!"}]
result = VoiGpt.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)
print(next(result))

# Пример 2: Использование с указанием access_token
access_token = "your_access_token"  # Замените на ваш actual access token
messages: List[Dict[str, str]] = [{"role": "user", "content": "Как дела?"}]
result = VoiGpt.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False, access_token=access_token)
print(next(result))

# Пример 3: Использование с указанием прокси
messages: List[Dict[str, str]] = [{"role": "user", "content": "Tell me a joke."}]
result = VoiGpt.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False, proxy="http://your_proxy:8080")
print(next(result))