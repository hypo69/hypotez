## Модуль `Chatgpt4o.py`

### Обзор

Модуль предоставляет асинхронный класс `Chatgpt4o`, который является провайдером для взаимодействия с моделью `gpt-4o-mini-2024-07-18` через API `chatgpt4o.one`. Модуль предназначен для генерации текста на основе предоставленных сообщений. Он получает `post_id` и `nonce` со страницы `chatgpt4o.one`, необходимые для выполнения запросов.

### Подробнее

Модуль использует библиотеки `re`, `StreamSession` из `...requests`, `Messages` из `...typing`, а также `AsyncProvider` и `ProviderModelMixin` из `..base_provider` и `format_prompt` из `..helper`.
Он предназначен для асинхронного взаимодействия с API `chatgpt4o.one` для генерации ответов на основе предоставленных сообщений.

## Классы

### `Chatgpt4o`

**Описание**: Класс `Chatgpt4o` предоставляет асинхронный интерфейс для взаимодействия с моделью `gpt-4o-mini-2024-07-18` через API `chatgpt4o.one`.

**Наследует**:
- `AsyncProvider`: Обеспечивает асинхронную поддержку для провайдера.
- `ProviderModelMixin`: Добавляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL-адрес API `chatgpt4o.one`.
- `working` (bool): Указывает, работает ли провайдер (в данном случае `False`).
- `_post_id` (str | None): ID поста, необходимый для запросов.
- `_nonce` (str | None): Одноразовый токен, необходимый для запросов.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini-2024-07-18`).
- `models` (list[str]): Список поддерживаемых моделей (`gpt-4o-mini-2024-07-18`).
- `model_aliases` (dict[str, str]): Псевдонимы моделей (например, `"gpt-4o-mini": "gpt-4o-mini-2024-07-18"`).

**Методы**:
- `create_async()`: Асинхронно создает текст на основе предоставленных сообщений, используя API `chatgpt4o.one`.

#### `create_async`

```python
    @classmethod
    async def create_async(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        timeout: int = 120,
        cookies: dict = None,
        **kwargs
    ) -> str:
        """
        Асинхронно создает текст на основе предоставленных сообщений, используя API chatgpt4o.one.

        Args:
            model (str): Имя используемой модели.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            timeout (int, optional): Время ожидания запроса в секундах. По умолчанию `120`.
            cookies (dict, optional): Куки для отправки с запросом. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            str: Текст, сгенерированный API.

        Raises:
            RuntimeError: Если не удается получить `post_id` или `nonce`, или если структура ответа API неожиданная.

        
        - Функция отправляет запрос к API `chatgpt4o.one` с предоставленными сообщениями для генерации текста.
        - Если `_post_id` или `_nonce` не установлены, функция получает их со страницы `chatgpt4o.one`.
        - Форматирует сообщения с использованием `format_prompt`.
        - Отправляет POST-запрос с данными, включая `_wpnonce`, `post_id`, `url`, `action`, `message` и `bot_id`.
        - Возвращает текст, сгенерированный API.

        Примеры:
            >>> messages = [{"role": "user", "content": "Hello, world!"}]
            >>> Chatgpt4o.create_async(model="gpt-4o-mini-2024-07-18", messages=messages)
            'Hello, world!'
        """
```

##### Внутренние переменные `create_async`

- `headers` (dict): Заголовки HTTP-запроса, включающие информацию о браузере, referrer и типе контента.
- `session` (`StreamSession`): Асинхронная сессия для выполнения HTTP-запросов с поддержкой прокси и таймаутов.
- `response` (`aiohttp.ClientResponse`): Объект ответа от HTTP-запроса.
- `response_text` (str): Текст ответа от HTTP-запроса.
- `post_id_match` (`re.Match`): Результат поиска `post_id` в тексте ответа.
- `nonce_match` (`re.Match`): Результат поиска `nonce` в тексте ответа.
- `prompt` (str): Отформатированный промпт (сообщение) для отправки в API.
- `data` (dict): Данные, отправляемые в POST-запросе, включающие `_wpnonce`, `post_id`, `url`, `action`, `message` и `bot_id`.
- `response_json` (dict): JSON-ответ от API.

##### **Как работает функция**:

1. **Определение заголовков**:
   - Определяются необходимые HTTP-заголовки для запроса, такие как `authority`, `accept`, `accept-language`, `origin`, `referer`, `sec-ch-ua`, `sec-ch-ua-mobile`, `sec-ch-ua-platform`, `sec-fetch-dest`, `sec-fetch-mode`, `sec-fetch-site` и `user-agent`.

2. **Создание асинхронной сессии**:
   - Создается асинхронная сессия `StreamSession` с заданными заголовками, куками, имитацией браузера (`impersonate="chrome"`), прокси и таймаутом.

3. **Получение `post_id` и `nonce` (если необходимо)**:
   - Проверяется, установлены ли `cls._post_id` и `cls._nonce`. Если нет, выполняются следующие действия:
     - Отправляется GET-запрос на главную страницу `cls.url`.
     - Извлекается текст ответа.
     - Используются регулярные выражения для поиска `data-post-id` и `data-nonce` в тексте ответа.
     - Если `post_id` или `nonce` не найдены, вызывается исключение `RuntimeError`.
     - Полученные значения присваиваются `cls._post_id` и `cls._nonce`.

4. **Форматирование промпта**:
   - Форматируются входные сообщения `messages` с использованием функции `format_prompt`.

5. **Подготовка данных для POST-запроса**:
   - Создается словарь `data` с параметрами, необходимыми для POST-запроса, такими как `_wpnonce`, `post_id`, `url`, `action`, `message` и `bot_id`.

6. **Отправка POST-запроса и обработка ответа**:
   - Отправляется POST-запрос на URL `f"{cls.url}/wp-admin/admin-ajax.php"` с данными `data` и куками.
     - Проверяется статус ответа с помощью `raise_for_status`.
   - Извлекается JSON-ответ.
   - Проверяется наличие поля `"data"` в JSON-ответе. Если поле отсутствует, вызывается исключение `RuntimeError`.
   - Возвращается значение поля `"data"` из JSON-ответа.

#### **Примеры**

```python
messages = [{"role": "user", "content": "Hello, world!"}]
Chatgpt4o.create_async(model="gpt-4o-mini-2024-07-18", messages=messages)
# Вывод: 'Hello, world!'
```