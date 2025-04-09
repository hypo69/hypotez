# Модуль Yqcloud

## Обзор

Модуль `Yqcloud` предоставляет асинхронный интерфейс для взаимодействия с провайдером Yqcloud (https://chat9.yqcloud.top) через API https://api.binjie.fun/api/generateStream. 
Этот модуль позволяет генерировать текст на основе предоставленных сообщений, поддерживая потоковую передачу данных и работу с историей сообщений.

## Подробней

Модуль `Yqcloud` предназначен для асинхронной генерации текста с использованием API Yqcloud. Он включает в себя функциональность для управления историей сообщений, поддержки системных сообщений и потоковой передачи данных.
Этот модуль используется в проекте для интеграции с сервисом Yqcloud для предоставления пользователям возможности взаимодействия с моделью GPT-4 через API.

## Классы

### `Conversation`

**Описание**: Класс `Conversation` представляет собой контейнер для хранения истории сообщений и идентификатора пользователя в рамках диалога с моделью.

**Наследует**: `JsonConversation`

**Аттрибуты**:
- `userId` (str): Уникальный идентификатор пользователя в формате `#/chat/{timestamp}`.
- `message_history` (Messages): Список сообщений в формате `List[Dict[str, str]]`, представляющий историю диалога.
- `model` (str): Модель, используемая в разговоре.

**Методы**:
- `__init__(model: str)`: Инициализирует объект `Conversation`, устанавливая модель и генерируя уникальный `userId`.

### `Yqcloud`

**Описание**: Класс `Yqcloud` является провайдером для асинхронной генерации текста с использованием API Yqcloud.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Аттрибуты**:
- `url` (str): URL сервиса Yqcloud.
- `api_endpoint` (str): URL API для генерации текста.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4`).
- `models` (List[str]): Список поддерживаемых моделей (`[default_model]`).

**Методы**:
- `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: 
   Метод для создания асинхронного генератора текста.

## Функции

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        proxy: str = None,
        conversation: Conversation = None,
        return_conversation: bool = False,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения текстовых ответов от API Yqcloud.

        Args:
            model (str): Идентификатор используемой модели.
            messages (Messages): Список сообщений для передачи в API.
            stream (bool, optional): Флаг, указывающий на использование потоковой передачи данных. По умолчанию `True`.
            proxy (str, optional): URL прокси-сервера для использования при подключении к API. По умолчанию `None`.
            conversation (Conversation, optional): Объект `Conversation` для хранения истории сообщений. По умолчанию `None`.
            return_conversation (bool, optional): Флаг, указывающий на необходимость возврата объекта `Conversation` с обновленной историей. По умолчанию `False`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий текстовые ответы от API.

        Raises:
            Exception: Если возникает ошибка при взаимодействии с API.

        """
```

**Назначение**: Создание асинхронного генератора для взаимодействия с API Yqcloud и получения текстовых ответов.

**Параметры**:
- `model` (str): Идентификатор используемой модели.
- `messages` (Messages): Список сообщений для передачи в API.
- `stream` (bool, optional): Флаг, указывающий на использование потоковой передачи данных. По умолчанию `True`.
- `proxy` (str, optional): URL прокси-сервера для использования при подключении к API. По умолчанию `None`.
- `conversation` (Conversation, optional): Объект `Conversation` для хранения истории сообщений. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг, указывающий на необходимость возврата объекта `Conversation` с обновленной историей. По умолчанию `False`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий текстовые ответы от API.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при взаимодействии с API.

**Как работает функция**:

1. **Подготовка данных**:
   - Извлекает модель, устанавливает заголовки запроса.
   - Если объект `conversation` не предоставлен, создает новый экземпляр класса `Conversation` и инициализирует его историей сообщений. В противном случае добавляет последнее сообщение в существующую историю.
   - Извлекает системное сообщение (если есть) из истории сообщений.

2. **Взаимодействие с API**:
   - Отправляет POST-запрос к `cls.api_endpoint` с использованием `aiohttp.ClientSession`.
   - Формирует JSON-данные для запроса, включающие промпт, идентификатор пользователя, флаг сетевого подключения, системное сообщение и флаг потоковой передачи.

3. **Обработка ответа**:
   - Получает ответ от API и обрабатывает его по частям (chunks).
   - Декодирует каждую часть ответа и передает ее в генератор.
   - Если `return_conversation` установлен в `True`, добавляет ответ ассистента в историю сообщений и возвращает объект `conversation`.

4. **Завершение**:
   - После обработки всех частей ответа генерирует `FinishReason("stop")`, сигнализирующий о завершении работы генератора.

```
    Подготовка данных
    │
    ├───> Создание или обновление conversation
    │     │
    │     └───> Извлечение системного сообщения
    │
    │
    V
    Отправка POST-запроса к API
    │
    ├───> Формирование JSON-данных
    │     │
    │     └───> Отправка запроса
    │
    │
    V
    Обработка ответа
    │
    ├───> Потоковая обработка chunks
    │     │
    │     └───> Декодирование и передача в генератор
    │
    │
    V
    Завершение
    │
    └───> Возврат conversation (если необходимо)
    │
    V
    FinishReason("stop")
```

**Примеры**:

```python
# Пример использования без прокси и истории сообщений
async def example():
    model = "gpt-4"
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for message in Yqcloud.create_async_generator(model=model, messages=messages):
        print(message, end="")

# Пример использования с прокси и возвратом истории сообщений
async def example_with_proxy():
    model = "gpt-4"
    messages = [{"role": "user", "content": "Tell me a joke."}]
    proxy = "http://your-proxy-url:8080"
    async for item in Yqcloud.create_async_generator(model=model, messages=messages, proxy=proxy, return_conversation=True):
        if isinstance(item, Conversation):
            print("Conversation history:", item.message_history)
        else:
            print(item, end="")