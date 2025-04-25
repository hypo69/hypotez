# Модуль `gemini_simplechat.main`

## Обзор

Этот модуль содержит реализацию простого чат-интерфейса на базе `fast_api`, использующего модель Google Gemini для обработки текстовых запросов. 

## Подробности

Модуль `gemini_simplechat.main` предоставляет API для взаимодействия с моделью Google Gemini через веб-интерфейс. В основе API лежит библиотека `fast_api`, которая обеспечивает обработку HTTP-запросов. 

## Классы

### `Config`

**Описание**: Класс `Config` содержит конфигурационные параметры для модуля, такие как хост, диапазон портов, API-ключ для доступа к Google Gemini, имя модели, путь к файлу с системными инструкциями и путь к каталогу с HTML-шаблонами.

**Атрибуты**:
- `ENDPOINT` (Path): Путь к каталогу модуля `gemini_simplechat`.
- `config` (SimpleNamespace): Объект, содержащий конфигурационные параметры, загруженные из файла `gemini_simplechat.json`.
- `HOST` (str): Хост для запуска сервера.
- `PORTS_RANGE` (list[int]): Диапазон портов для поиска свободного порта.
- `GEMINI_API_KEY` (str): API-ключ для доступа к Google Gemini.
- `GEMINI_MODEL_NAME` (str): Имя модели Google Gemini.
- `system_instruction_path` (Path): Путь к файлу с системными инструкциями для модели Gemini.
- `SYSTEM_INSTRUCTION` (str): Текст системных инструкций для модели Gemini, загруженный из файла `system_instruction_path`.

**Принцип работы**:
- Класс `Config` считывает конфигурационные параметры из файла `gemini_simplechat.json`, который находится в каталоге модуля `gemini_simplechat`.
- Загруженные параметры сохраняются в атрибуте `config`, который является объектом `SimpleNamespace` для удобного доступа к значениям.
- Также класс загружает текст системных инструкций для модели Gemini из файла `system_instruction_path`.

## Функции

### `root`

**Назначение**: Функция, отвечающая за обработку запроса к корневому маршруту API `/`.

**Параметры**:
- Нет.

**Возвращает**:
- `HTMLResponse`: Объект `HTMLResponse` с содержимым HTML-файла `index.html`, который находится в каталоге `html` модуля `gemini_simplechat`.

**Вызывает исключения**:
- `HTTPException`: В случае ошибки при чтении HTML-файла.

**Пример**:

```python
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.get("/")
assert response.status_code == 200
assert response.text == '<html> ... </html>' # содержимое HTML-файла
```

### `chat`

**Назначение**: Функция, отвечающая за обработку запроса к маршруту `api/chat` для отправки текстового запроса модели Google Gemini.

**Параметры**:
- `request` (ChatRequest): Объект, содержащий текстовый запрос пользователя.

**Возвращает**:
- `dict`: Словарь, содержащий ответ модели Gemini.

**Вызывает исключения**:
- `HTTPException`: В случае ошибки при выполнении запроса к модели Gemini.

**Пример**:

```python
from fastapi.testclient import TestClient
from gemini_simplechat.main import ChatRequest

client = TestClient(app)
request_data = {"message": "Привет, как дела?"}
response = client.post("/api/chat", json=request_data)
assert response.status_code == 200
assert response.json() == {"response": "Привет! У меня все хорошо, спасибо за вопрос. А как дела у тебя?"} # пример ответа модели
```


## Параметры класса

- `model` (GoogleGenerativeAi): Объект класса `GoogleGenerativeAi` из модуля `src.llm.gemini`, представляющий собой модель Google Gemini, инициализированную API-ключом, именем модели и системными инструкциями.

## Примеры

### Создание и запуск сервера:

```python
from gemini_simplechat.main import app, Config

# Загрузка конфигурационных параметров
config = Config()

# Запуск сервера на свободном порту
port = get_free_port(config.HOST, config.PORTS_RANGE)
uvicorn.run(app, host=config.HOST, port=port)
```

### Отправка текстового запроса:

```python
from fastapi.testclient import TestClient
from gemini_simplechat.main import ChatRequest

client = TestClient(app)
request_data = {"message": "Расскажи анекдот."}
response = client.post("/api/chat", json=request_data)
print(response.json())
```

## Основные функции:

- **Загрузка конфигурационных параметров**: Модуль считывает конфигурацию из файла `gemini_simplechat.json` и инициализирует класс `Config`.
- **Создание модели Google Gemini**:  Используется класс `GoogleGenerativeAi` из модуля `src.llm.gemini` для инициализации модели Google Gemini с указанными API-ключом, именем модели и системными инструкциями.
- **Обработка HTTP-запросов**: Модуль использует `fast_api` для обработки HTTP-запросов к корневому маршруту `/` и маршруту `api/chat`. 
- **Обработка текстовых запросов**:  Модуль передает текстовые запросы, полученные от пользователя, модели Google Gemini через метод `chat` класса `GoogleGenerativeAi`.
- **Возврат ответов**: Модуль возвращает ответы модели Google Gemini пользователю в виде JSON-объекта.
- **Логирование**: Модуль использует модуль `logger` из `src.logger` для записи информации о работе API в лог-файлы.

## Взаимодействие с другими частями проекта

- Модуль `gemini_simplechat.main` взаимодействует с модулем `src.llm.gemini` для работы с моделью Google Gemini.
- Модуль использует функции `get_free_port` и `j_loads_ns` из модуля `src.utils` для поиска свободного порта и загрузки конфигурационных параметров.
- Модуль `src.logger` используется для логирования. 

##  Важные моменты

- Модуль `gemini_simplechat.main`  включает в себя код, который используется для запуска веб-сервера.
- Для работы модуля требуется API-ключ Google Gemini, который должен быть указан в файле конфигурации `gemini_simplechat.json`.
- В файле `gemini_simplechat.json` также можно задать имя модели Gemini, а также путь к файлу с системными инструкциями. 
- Модуль обеспечивает поддержку CORS, что позволяет ему принимать запросы от веб-приложений, работающих на других доменах.
- Для использования API необходимо использовать HTTP-клиент, например `requests` или `curl`.

## Дополнительные сведения

- Дополнительная информация о модели Google Gemini доступна на сайте [https://developers.generativeai.google](https://developers.generativeai.google).
- Документация по библиотеке `fast_api` доступна на сайте [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/).
- Документация по модулю `src.utils` доступна в соответствующем файле `.md` в проекте `hypotez`.