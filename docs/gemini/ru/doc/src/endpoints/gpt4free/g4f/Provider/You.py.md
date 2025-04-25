# Модуль You.py

## Обзор

Этот модуль предоставляет класс `You`, который реализует асинхронный генератор для работы с сервисом You.com. 

**Назначение**: 

- Обеспечивает взаимодействие с You.com API для генерации текста и изображений.
- Поддерживает различные модели, включая GPT-4, GPT-4o-Mini, GPT-4-Turbo, Dall-E и другие.
- Предоставляет возможность работы в режиме диалога или создания изображений.
- Обеспечивает обработку изображений с помощью модели `agent`.

**Использование**:

Класс `You` позволяет использовать различные функции:

- `create_async_generator()`: Создание асинхронного генератора для работы с You.com.
- `upload_file()`: Загрузка файла (изображения) на You.com.


## Классы

### `class You`

**Описание**: Класс `You` реализует асинхронный генератор для работы с сервисом You.com.

**Наследует**: 
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию результатов.
- `ProviderModelMixin`: Предоставляет функции для работы с различными моделями.

**Атрибуты**:

- `label (str)`:  Название провайдера (You.com).
- `url (str)`: URL-адрес You.com.
- `working (bool)`: Флаг, указывающий, доступен ли провайдер.
- `default_model (str)`:  Название модели по умолчанию (`gpt-4o-mini`).
- `default_vision_model (str)`: Название модели для обработки изображений (`agent`).
- `image_models (List[str])`: Список моделей, которые поддерживают генерацию изображений.
- `models (List[str])`: Список всех доступных моделей.
- `_cookies (Cookies)`:  Cookies, используемые для аутентификации.
- `_cookies_used (int)`: Количество использований cookies.
- `_telemetry_ids (List[str])`: Список ID для отслеживания телеметрии.


**Методы**:

- `create_async_generator()`: Создает асинхронный генератор, который позволяет получать результаты от You.com.
- `upload_file()`: Загружает файл (изображение) на You.com.

#### `async def create_async_generator(cls, model: str, messages: Messages, stream: bool = True, image: ImageType = None, image_name: str = None, proxy: str = None, timeout: int = 240, chat_mode: str = "default", cookies: Cookies = None, **kwargs) -> AsyncResult:`

**Назначение**: Создает асинхронный генератор, который позволяет получать результаты от You.com.

**Параметры**:

- `model (str)`: Название модели, которую необходимо использовать (например, `gpt-4o-mini`, `dall-e`).
- `messages (Messages)`: Список сообщений для диалога.
- `stream (bool)`: Флаг, указывающий, нужно ли использовать потоковую передачу данных.
- `image (ImageType)`: Изображение для обработки.
- `image_name (str)`:  Имя файла изображения.
- `proxy (str)`:  Прокси-сервер для подключения.
- `timeout (int)`:  Тайм-аут в секундах.
- `chat_mode (str)`:  Режим диалога (`default`, `agent`, `create`).
- `cookies (Cookies)`: Cookies для аутентификации.
- `kwargs (dict)`: Дополнительные параметры.

**Возвращает**:

- `AsyncResult`: Асинхронный результат, который является генератором строк, содержащих ответы от You.com.

**Как работает функция**:

1. Проверяет, нужно ли использовать модель для обработки изображений (`agent`) или создавать изображение с помощью Dall-E (`dall-e`).
2. Устанавливает режим диалога (`chat_mode`) в зависимости от выбранной модели и наличия изображения.
3. Получает cookies, если они не указаны, используя функцию `get_cookies()`.
4. Если cookies отсутствуют, открывает браузер и извлекает cookies с You.com.
5. Создает асинхронную сессию (`StreamSession`) для подключения к You.com.
6. Загружает изображение на You.com, если оно присутствует, используя функцию `upload_file()`.
7. Формирует запрос с использованием параметров `model`, `messages`, `chat_mode`, `upload` и других.
8. Отправляет GET-запрос на API You.com с помощью сессии и получает ответ в потоковом режиме.
9. Выполняет обработку ответа, извлекая текст или изображения.
10. Возвращает асинхронный результат (`AsyncResult`), который является генератором для получения ответов от You.com.


**Примеры**:

```python
# Пример использования модели GPT-4o-Mini для генерации текста
async def generate_text(messages: Messages):
    async for response in You.create_async_generator(model="gpt-4o-mini", messages=messages):
        print(response)

# Пример использования Dall-E для создания изображения
async def create_image(image_prompt: str):
    async for response in You.create_async_generator(model="dall-e", messages=[{"role": "user", "content": image_prompt}]):
        print(response)

```

#### `async def upload_file(cls, client: StreamSession, cookies: Cookies, file: bytes, filename: str = None) -> dict:`

**Назначение**: Загружает файл (изображение) на You.com.

**Параметры**:

- `client (StreamSession)`:  Асинхронная сессия для подключения к You.com.
- `cookies (Cookies)`: Cookies для аутентификации.
- `file (bytes)`:  Файл (изображение) в виде байтов.
- `filename (str)`:  Имя файла (опционально).

**Возвращает**:

- `dict`:  Словарь с информацией о загруженном файле.

**Как работает функция**:

1. Получает nonce (случайное значение) для загрузки файлов с You.com.
2. Создает объект `FormData` и добавляет к нему файл.
3. Отправляет POST-запрос на API You.com для загрузки файла.
4. Извлекает информацию о загруженном файле (имя, размер) из ответа.
5. Возвращает словарь с информацией о файле.


**Примеры**:

```python
# Загрузка изображения на You.com
async def upload_image(image_path: str):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    upload_result = await You.upload_file(client=StreamSession(), cookies=get_cookies(), file=image_bytes, filename="my_image.jpg")
    print(f"Uploaded image: {upload_result}")

```

## Внутренние функции

- **`def get_model(model: str) -> str:`**: Проверяет, существует ли модель в списке доступных моделей. Если модель не найдена, возвращает `None`.


## Параметры класса

- `default_model (str)`:  Название модели по умолчанию (`gpt-4o-mini`).
- `default_vision_model (str)`: Название модели для обработки изображений (`agent`).
- `image_models (List[str])`: Список моделей, которые поддерживают генерацию изображений.
- `models (List[str])`: Список всех доступных моделей.
- `_cookies (Cookies)`:  Cookies, используемые для аутентификации.
- `_cookies_used (int)`: Количество использований cookies.
- `_telemetry_ids (List[str])`: Список ID для отслеживания телеметрии.

## Примеры

```python
# Пример использования модели GPT-4o-Mini для генерации текста
async def generate_text(messages: Messages):
    async for response in You.create_async_generator(model="gpt-4o-mini", messages=messages):
        print(response)

# Пример использования Dall-E для создания изображения
async def create_image(image_prompt: str):
    async for response in You.create_async_generator(model="dall-e", messages=[{"role": "user", "content": image_prompt}]):
        print(response)

# Загрузка изображения на You.com
async def upload_image(image_path: str):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    upload_result = await You.upload_file(client=StreamSession(), cookies=get_cookies(), file=image_bytes, filename="my_image.jpg")
    print(f"Uploaded image: {upload_result}")

```