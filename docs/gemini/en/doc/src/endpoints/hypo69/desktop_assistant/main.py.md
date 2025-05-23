# Модуль Desktop Assistant API
## Обзор

Этот модуль предоставляет API для взаимодействия с  desktop assistant. Он использует Google Gemini для обработки запросов пользователей.

## Детали

Модуль создает приложение FastAPI, которое обрабатывает запросы на маршрутах `/` (корневой маршрут) и `/api/chat`. Корневой маршрут отображает HTML-страницу с интерфейсом чата. Маршрут `/api/chat` обрабатывает текстовые запросы пользователя и отправляет их в модель Google Gemini для получения ответов.

## Классы

### `ChatRequest`
**Описание**: Класс, представляющий модель запроса чата.
**Атрибуты**:
- `message` (str): Текстовый запрос пользователя.

## Функции

### `get_locale_file`
**Назначение**: Извлекает локальный файл для заданного языка.

**Параметры**:
- `lang` (str): Код языка (например, `ru`, `en`).

**Возвращает**:
- `dict`: Содержимое файла локализации в виде словаря.

**Возможные исключения**:
- `FileNotFoundError`: Если файл локализации не найден.
- `json.JSONDecodeError`: Если файл локализации некорректный JSON.
- `Exception`: При возникновении любой другой ошибки при чтении файла.

**Как работает**:
- Функция получает код языка в качестве параметра.
- Она пытается открыть файл локализации с именем `lang.json` в директории `locales_path`.
- Если файл найден, он читается, преобразуется в JSON и возвращается.
- В случае ошибок возвращается соответствующее исключение.

### `root`
**Назначение**: Обрабатывает корневой маршрут API и отображает HTML-страницу с интерфейсом чата.

**Параметры**:
- Нет.

**Возвращает**:
- `HTMLResponse`:  HTML-страница с интерфейсом чата.

**Возможные исключения**:
- `FileNotFoundError`: Если файл `index.html` не найден в директории `templates_path`.
- `Exception`: При возникновении любой другой ошибки при чтении HTML-файла.

**Как работает**:
- Функция пытается открыть файл `index.html` в директории `templates_path`.
- Если файл найден, он читается и возвращается в виде HTMLResponse.
- В случае ошибок возвращается исключение HTTPException с кодом 500.

### `chat`
**Назначение**: Обрабатывает запросы на чат, отправляет их в модель Google Gemini и возвращает ответ.

**Параметры**:
- `request` (ChatRequest): Запрос пользователя.

**Возвращает**:
- `dict`: Ответ от Google Gemini.

**Возможные исключения**:
- `Exception`: При возникновении ошибки во время обработки запроса или получения ответа.

**Как работает**:
- Функция получает объект `ChatRequest` с текстовым сообщением пользователя.
- Она создает объект `GoogleGenerativeAi`, если он не существует.
- Она отправляет текст пользователя в модель Google Gemini с помощью метода `chat`.
- Она возвращает полученный ответ.
- В случае ошибки возвращает исключение HTTPException с кодом 500.

## Примеры

```python
# Запрос к маршруту /api/chat
from fastapi.testclient import TestClient

client = TestClient(app)

response = client.post("/api/chat", json={"message": "Привет, как дела?"})

assert response.status_code == 200
print(response.json())

# Ожидаемый вывод:
# {"response": "Привет! У меня все хорошо. Как дела у тебя?"}

# Запрос к корневому маршруту /
response = client.get("/")

assert response.status_code == 200
print(response.text)

# Ожидаемый вывод:
# HTML-код с интерфейсом чата
```
```markdown