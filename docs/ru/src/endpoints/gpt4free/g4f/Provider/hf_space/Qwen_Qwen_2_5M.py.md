# Модуль `Qwen_Qwen_2_5M`

## Обзор

Модуль `Qwen_Qwen_2_5M` предоставляет асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.5M, размещенной на платформе Hugging Face Space. Он поддерживает потоковую передачу данных и системные сообщения, но не поддерживает историю сообщений.

## Подробнее

Этот модуль позволяет взаимодействовать с моделью Qwen Qwen-2.5M через API Hugging Face Space. Он использует асинхронные запросы для получения ответов модели в режиме реального времени. Модуль также предоставляет возможность отслеживать этапы генерации ответа модели.

## Классы

### `Qwen_Qwen_2_5M`

**Описание**: Класс для взаимодействия с моделью Qwen Qwen-2.5M через API Hugging Face Space.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("Qwen Qwen-2.5M").
- `url` (str): URL Hugging Face Space ("https://qwen-qwen2-5-1m-demo.hf.space").
- `api_endpoint` (str): URL API для предсказаний ("https://qwen-qwen2-5-1m-demo.hf.space/run/predict?__theme=light").
- `working` (bool): Флаг, указывающий, что провайдер работает (True).
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу (True).
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения (True).
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений (False).
- `default_model` (str): Модель по умолчанию ("qwen-2.5-1m-demo").
- `model_aliases` (dict): Псевдонимы моделей ({"qwen-2.5-1m": "qwen-2.5-1m-demo"}).
- `models` (list): Список доступных моделей (["qwen-2.5-1m"]).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от модели.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    return_conversation: bool = False,
    conversation: JsonConversation = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от модели.

    Args:
        model (str): Имя модели.
        messages (Messages): Список сообщений для отправки модели.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать объект JsonConversation. По умолчанию `False`.
        conversation (JsonConversation, optional): Объект JsonConversation для поддержания состояния разговора. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

    Raises:
        aiohttp.ClientError: Если возникает ошибка при выполнении HTTP-запроса.
        json.JSONDecodeError: Если не удается декодировать JSON-ответ.

    **Внутренние функции**:

    ### `generate_session_hash`

    ```python
    def generate_session_hash():
        """Генерирует уникальный hash сессии."""
        return str(uuid.uuid4()).replace('-', '')[:12]
    ```

    **Как работает функция**:
    - Функция генерирует UUID, удаляет дефисы и берет первые 12 символов.
    - Возвращает уникальный идентификатор сессии.

    """
    ```

**Назначение**: Создает асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.5M.

**Параметры**:
- `model` (str): Имя модели, которую нужно использовать.
- `messages` (Messages): Список сообщений, которые нужно отправить модели.
- `proxy` (str, optional): URL прокси-сервера, если необходимо использовать прокси. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг, указывающий, нужно ли возвращать объект `JsonConversation`. По умолчанию `False`.
- `conversation` (JsonConversation, optional): Объект `JsonConversation` для поддержания состояния разговора. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от модели.

**Вызывает исключения**:
- `aiohttp.ClientError`: Если возникает ошибка при выполнении HTTP-запроса.
- `json.JSONDecodeError`: Если не удается декодировать JSON-ответ.

**Как работает функция**:
1. **Генерация уникального хеша сессии**: Если объект `conversation` не передан, генерируется уникальный хеш сессии с использованием внутренней функции `generate_session_hash`.
2. **Возврат объекта `JsonConversation`**: Если `return_conversation` имеет значение `True`, функция возвращает объект `JsonConversation` с хешем сессии.
3. **Форматирование промпта**: Если объект `conversation` не передан, промпт форматируется из списка сообщений с помощью функции `format_prompt`. В противном случае извлекается последнее сообщение пользователя из списка сообщений с помощью функции `get_last_user_message`.
4. **Формирование заголовков и полезной нагрузки**: Формируются заголовки HTTP-запроса и полезная нагрузка для отправки запроса к API Hugging Face Space.
5. **Отправка запроса к API**: С использованием асинхронной сессии `aiohttp` отправляется POST-запрос к API Hugging Face Space для получения ответа от модели.
6. **Обработка потока данных**: Полученный ответ обрабатывается построчно. Каждая строка декодируется из UTF-8. Если строка начинается с "data: ", то извлекается JSON-данные и обрабатываются.
7. **Анализ этапов генерации**: Если в JSON-данных содержится сообщение "process_generating", то извлекается текст ответа модели и возвращается генератором.
8. **Проверка завершения**: Если в JSON-данных содержится сообщение "process_completed", то извлекается окончательный ответ модели и возвращается генератором.
9. **Обработка ошибок**: Если не удается декодировать JSON-данные, то в журнал записывается сообщение об ошибке.

**Примеры**:

```python
# Пример использования с минимальными параметрами
async for response in Qwen_Qwen_2_5M.create_async_generator(model="qwen-2.5-1m", messages=[{"role": "user", "content": "Hello"}]):
    print(response)

# Пример использования с прокси-сервером
async for response in Qwen_Qwen_2_5M.create_async_generator(model="qwen-2.5-1m", messages=[{"role": "user", "content": "Hello"}], proxy="http://proxy.example.com"):
    print(response)

# Пример использования с возвратом объекта JsonConversation
async for response in Qwen_Qwen_2_5M.create_async_generator(model="qwen-2.5-1m", messages=[{"role": "user", "content": "Hello"}], return_conversation=True):
    if isinstance(response, JsonConversation):
        print(f"Session hash: {response.session_hash}")
    else:
        print(response)