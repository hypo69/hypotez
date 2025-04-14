# Модуль gemini_simplechat.main

## Обзор

Модуль `gemini_simplechat.main` предоставляет простой API для общения с Google Gemini. Он включает в себя настройку FastAPI приложения, CORS middleware, обработку запросов чата и запуск локального сервера.

## Подробнее

Этот модуль создает FastAPI приложение для обработки входящих запросов чата. Он использует модель Google Gemini для генерации ответов на сообщения пользователей. Модуль также настраивает CORS для разрешения запросов с разных доменов, что полезно при разработке веб-приложений.
Файл `main.py` отвечает за запуск веб-сервера, который будет принимать запросы к Gemini.
Расположение файла `hypotez/src/endpoints/gemini_simplechat/main.py` указывает на то, что это основной файл для endpoint `gemini_simplechat`, который предоставляет функциональность чата с использованием модели Gemini.

## Классы

### `ChatRequest`

**Описание**: Модель запроса чата, используемая для валидации входящих сообщений.

**Наследует**: `BaseModel` из `pydantic`

**Атрибуты**:

-   `message` (str): Сообщение от пользователя.

## Функции

### `root`

**Назначение**: Обрабатывает GET-запросы к корневому пути ("/").

```python
async def root():
    """
    Обрабатывает GET-запросы к корневому пути ("/").

    Args:
        Нет

    Returns:
        HTMLResponse: HTML-контент, прочитанный из файла index.html.

    Raises:
        HTTPException: Если возникает ошибка при чтении файла index.html.
    """
```

**Как работает функция**:

1.  Пытается прочитать содержимое файла `index.html`, путь к которому берется из конфигурации `gs.fast_api.index_path`.
2.  Возвращает HTML-контент в `HTMLResponse`.
3.  Если происходит ошибка при чтении файла, выбрасывает `HTTPException` с кодом состояния 500 и детальным сообщением об ошибке.

**Примеры**:

```python
# Пример вызова (непосредственно FastAPI вызывает эту функцию при запросе)
# GET /
```

### `chat`

**Назначение**: Обрабатывает POST-запросы к пути "/api/chat".

```python
async def chat(request: ChatRequest):
    """
    Обрабатывает POST-запросы к пути "/api/chat".

    Args:
        request (ChatRequest): Объект `ChatRequest`, содержащий сообщение пользователя.

    Returns:
        dict: Словарь с ответом от модели Gemini.

    Raises:
        HTTPException: Если возникает ошибка при взаимодействии с моделью Gemini.
    """
```

**Как работает функция**:

1.  Принимает объект `ChatRequest`, содержащий сообщение пользователя.
2.  Использует глобальную переменную `model` (экземпляр `GoogleGenerativeAI`) для генерации ответа на сообщение.
3.  Возвращает словарь, содержащий ответ от модели Gemini.
4.  В случае ошибки логирует её с использованием `logger.error` и выбрасывает `HTTPException` с кодом состояния 500 и детальным сообщением об ошибке.

**Примеры**:

```python
# Пример вызова (непосредственно FastAPI вызывает эту функцию при POST-запросе)
# POST /api/chat с JSON-телом {"message": "Hello, Gemini!"}
```

## Переменные

### `system_instruction`

```python
system_instruction: str = Path('instructions', 'system_instruction.md').read_text(encoding='UTF-8')
```

**Описание**: Содержит текст системной инструкции, прочитанный из файла `system_instruction.md`.
Файл расположен в директории `instructions`. Инструкция кодируется в формате UTF-8

### `model`

```python
model: GoogleGenerativeAI = GoogleGenerativeAI(api_key = gs.credentials.gemini.api_key, 
                                               model_name = gs.credentials.gemini.model_name, 
                                               system_instruction = system_instruction)
```

**Описание**: Экземпляр класса `GoogleGenerativeAI`, используемый для взаимодействия с моделью Gemini.
Инициализируется с использованием API-ключа, имени модели и системной инструкции, полученных из конфигурации `gs.credentials.gemini`.