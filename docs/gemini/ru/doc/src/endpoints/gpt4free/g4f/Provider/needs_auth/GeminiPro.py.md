# Модуль `GeminiPro`

## Обзор

Модуль `GeminiPro` предоставляет реализацию класса `GeminiPro`, который представляет собой асинхронный генератор ответов с использованием API Google Gemini Pro.  

Этот класс наследует функции `AsyncGeneratorProvider` и `ProviderModelMixin`, предоставляя возможности для генерации текста, перевода и других задач, связанных с обработкой естественного языка. 

## Классы

### `class GeminiPro`

**Описание**: Класс `GeminiPro` реализует асинхронный генератор ответов с использованием API Google Gemini Pro.

**Наследует**:
 - `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов ответов.
 - `ProviderModelMixin`: Предоставляет функции для работы с моделями.

**Атрибуты**:

 - `label`: Текстовая метка для идентификации провайдера ("Google Gemini API").
 - `url`: Базовый URL для API Google Gemini Pro.
 - `login_url`: URL для авторизации.
 - `api_base`: Базовый URL для API Google Gemini Pro.
 - `working`: Флаг, указывающий, что провайдер работает.
 - `supports_message_history`: Флаг, указывающий, что провайдер поддерживает историю сообщений.
 - `supports_system_message`: Флаг, указывающий, что провайдер поддерживает системные сообщения.
 - `needs_auth`: Флаг, указывающий, что провайдер требует авторизации.
 - `default_model`: Имя модели по умолчанию ("gemini-1.5-pro").
 - `default_vision_model`: Имя модели по умолчанию для задач обработки изображений.
 - `fallback_models`: Список резервных моделей.
 - `model_aliases`: Словарь псевдонимов для моделей.

**Методы**:

 - `get_models(api_key: str = None, api_base: str = api_base) -> list[str]`: Возвращает список доступных моделей. 
 - `create_async_generator(model: str, messages: Messages, stream: bool = False, proxy: str = None, api_key: str = None, api_base: str = api_base, use_auth_header: bool = False, media: MediaListType = None, tools: Optional[list] = None, connector: BaseConnector = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор ответов.

####  `get_models(api_key: str = None, api_base: str = api_base) -> list[str]`

**Назначение**: Функция извлекает список доступных моделей из API Google Gemini Pro. 

**Параметры**:

 - `api_key` (str): Ключ API для доступа к API Google Gemini Pro.
 - `api_base` (str): Базовый URL для API Google Gemini Pro.

**Возвращает**:

 - `list[str]`: Список доступных моделей. 

**Вызывает исключения**:

 - `MissingAuthError`: Возникает, если не указан ключ API.

**Как работает функция**:

 - Извлекает список доступных моделей из API Google Gemini Pro, используя URL `api_base/models`.
 - Проверяет, есть ли ключ API. 
 - Если ключ API не задан, возвращает список резервных моделей.
 - Если ключ API задан, отправляет запрос GET к API Google Gemini Pro с ключом API в качестве параметра.
 - Проверяет статус ответа и, если он успешен, извлекает список моделей из ответа.
 - Сортирует список моделей.
 - Возвращает список доступных моделей.

####  `create_async_generator(model: str, messages: Messages, stream: bool = False, proxy: str = None, api_key: str = None, api_base: str = api_base, use_auth_header: bool = False, media: MediaListType = None, tools: Optional[list] = None, connector: BaseConnector = None, **kwargs) -> AsyncResult`

**Назначение**: Создает асинхронный генератор ответов с использованием API Google Gemini Pro. 

**Параметры**:

 - `model` (str): Имя модели, которую нужно использовать.
 - `messages` (Messages): Список сообщений для обработки.
 - `stream` (bool): Флаг, указывающий, нужно ли использовать потоковую передачу.
 - `proxy` (str): URL-адрес прокси-сервера.
 - `api_key` (str): Ключ API для доступа к API Google Gemini Pro.
 - `api_base` (str): Базовый URL для API Google Gemini Pro.
 - `use_auth_header` (bool): Флаг, указывающий, нужно ли использовать заголовок авторизации.
 - `media` (MediaListType): Список медиа-файлов для обработки.
 - `tools` (Optional[list]): Список инструментов для использования.
 - `connector` (BaseConnector): Объект `BaseConnector` для настройки сетевого соединения.
 - `**kwargs`: Дополнительные параметры.

**Возвращает**:

 - `AsyncResult`: Асинхронный объект, представляющий результат генерации.

**Вызывает исключения**:

 - `MissingAuthError`: Возникает, если не указан ключ API.

**Как работает функция**:

 - Проверяет, задан ли ключ API.
 - Выбирает модель для использования.
 - Устанавливает заголовки и параметры запроса.
 - Определяет метод API (`streamGenerateContent` для потоковой передачи или `generateContent` для обычного запроса).
 - Создает объект `ClientSession` с использованием прокси-сервера, если он задан.
 - Преобразует список сообщений в формат, необходимый для API Google Gemini Pro.
 - Добавляет медиа-файлы к запросу, если они заданы.
 - Формирует данные запроса, включающие настройки генерации, инструменты и системные сообщения.
 - Отправляет запрос POST к API Google Gemini Pro.
 - Проверяет статус ответа. 
 - Если ответ успешен, обрабатывает данные ответа, возвращая текстовую часть ответа, информацию о завершении и информацию об использовании токенов.
 - Если ответ не успешен, генерирует исключение.

##  Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GeminiPro import GeminiPro
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание объекта GeminiPro
provider = GeminiPro()

# Список сообщений для обработки
messages = Messages(
    [
        {
            "role": "user",
            "content": "Привет, напиши мне короткий стих про летний дождь.",
        }
    ]
)

# Генерация ответа
async def generate_response():
    async for response in provider.create_async_generator(model="gemini-1.5-pro", messages=messages, api_key="YOUR_API_KEY"):
        print(response)

# Вызов функции для генерации ответа
generate_response()