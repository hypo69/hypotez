# Модуль Grok

## Обзор

Модуль `Grok` предоставляет API-интерфейс для взаимодействия с моделью `Grok AI`.  Он реализует класс `Grok`, который позволяет аутентифицироваться, отправлять запросы и получать ответы от `Grok AI`. 

## Подробней

Модуль `Grok` - это провайдер для работы с моделью `Grok AI`, интегрированный в `hypotez`. Он обрабатывает аутентификацию, формирует запросы и анализирует ответы, предоставляя пользователям удобный доступ к функциональности `Grok AI`. 

## Классы

### `class Conversation`

**Описание**: Класс `Conversation` представляет собой контейнер для идентификатора беседы.

**Атрибуты**:

- `conversation_id` (str): Идентификатор беседы.

### `class Grok`

**Описание**:  Класс `Grok` реализует провайдер для работы с моделью `Grok AI`. 

**Наследует**:

- `AsyncAuthedProvider`:  Класс, который реализует асинхронную аутентификацию.
- `ProviderModelMixin`:  Класс, который предоставляет методы для работы с различными моделями.

**Атрибуты**:

- `label` (str): Название провайдера.
- `url` (str): Базовый URL-адрес `Grok AI`.
- `cookie_domain` (str): Домен, используемый для хранения cookie.
- `assets_url` (str): Базовый URL-адрес для получения ресурсов.
- `conversation_url` (str): URL-адрес для работы с беседами.
- `needs_auth` (bool):  Флаг, указывающий на необходимость аутентификации.
- `working` (bool): Флаг, указывающий на доступность провайдера.
- `default_model` (str): Название модели по умолчанию.
- `models` (List[str]):  Список доступных моделей.
- `model_aliases` (Dict[str, str]): Словарь для преобразования псевдонимов моделей.

**Методы**:

- `on_auth_async(cls, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncIterator`: 
   **Описание**: Метод, который управляет аутентификацией.  Он проверяет наличие cookie и, если их нет, выдает запрос на аутентификацию.
   **Параметры**:
      - `cookies` (Cookies, optional):  Cookie-файлы, которые необходимо использовать для аутентификации. По умолчанию `None`.
      - `proxy` (str, optional):  Прокси-сервер, который необходимо использовать. По умолчанию `None`.
   **Возвращает**:
      - `AsyncIterator`: Асинхронный итератор, который выдает результаты аутентификации.
   **Вызывает исключения**:
      - `Exception`: Возникает при ошибке аутентификации.

- `_prepare_payload(cls, model: str, message: str) -> Dict[str, Any]`: 
   **Описание**:  Метод, который формирует тело запроса для `Grok AI`.
   **Параметры**:
      - `model` (str): Название модели.
      - `message` (str): Текстовое сообщение, которое необходимо отправить.
   **Возвращает**:
      - `Dict[str, Any]`: Словарь с данными, которые необходимо отправить в запросе.

- `create_authed(cls, model: str, messages: Messages, auth_result: AuthResult, cookies: Cookies = None, return_conversation: bool = False, conversation: Conversation = None, **kwargs) -> AsyncResult`: 
   **Описание**:  Метод, который отправляет запрос к `Grok AI` и обрабатывает ответ.
   **Параметры**:
      - `model` (str): Название модели.
      - `messages` (Messages): Список сообщений в беседе.
      - `auth_result` (AuthResult): Результат аутентификации.
      - `cookies` (Cookies, optional): Cookie-файлы. По умолчанию `None`.
      - `return_conversation` (bool, optional): Флаг, указывающий на необходимость вернуть объект `Conversation`. По умолчанию `False`.
      - `conversation` (Conversation, optional): Объект `Conversation`. По умолчанию `None`.
   **Возвращает**:
      - `AsyncResult`: Асинхронный результат, который выдает ответы от `Grok AI`. 
   **Вызывает исключения**:
      - `Exception`: Возникает при ошибке отправки запроса или получения ответа. 

### **Внутренние функции**:
- `format_prompt(messages)`: Функция, которая форматирует список сообщений для отправки в запросе. 
- `get_last_user_message(messages)`: Функция, которая извлекает последнее сообщение пользователя из списка сообщений.
- `get_cookies(domain, use_cache, update_cache, ignore_cookie_exists, cache_dir=None, use_chrome_cookies=False, allow_insecure=False)`: Функция, которая загружает cookie из кеша или браузера. 
- `get_args_from_nodriver(url, proxy, wait_for, timeout=60, headless=True, use_chrome=True)`: Функция, которая запускает браузер без визуального интерфейса для сбора cookie.

## Методы класса

### `function_name`

```python
    def function(param1:str, param2:Optional[int] = 0) -> bool:
        """ Функция выполняет некоторое действия... <Тут Ты пишешь что именно делает функция> 
        Args:
            param1 (str): Описание параметра `param1`.
            param2 (Optional[int], optional): Описание параметра `param2`. По умолчанию 0.
        Returns:
            bool: Описание возвращаемого значения. Возвращает `True` или `False`.

        Raises:
            Ошибка выполнение

        Example:
            Примеры вызовов со всем спектром параметров. которы можно передать в функцию

        """
        - Не отдавай код функции. Только документацию и примеры вызова функции;
        - Все комментарии и docstring должны быть на русском языке в формате UTF-8
```

## Параметры класса

- `param` (str): Более подробное Описание параметра `param`.
- `param1` (Optional[str | dict | str], optional): Более подробное Описание параметра `param1`. По умолчанию `None`.

## Примеры

```python
# Создание инстанса класса Grok
grok = Grok()

# Аутентификация 
auth_result = await grok.on_auth_async()
print(auth_result)

# Отправка запроса к Grok AI
messages = [{"role": "user", "content": "Привет! Как дела?"}]
response = await grok.create_authed(model="grok-3", messages=messages, auth_result=auth_result)

# Вывод ответов
async for item in response:
    if isinstance(item, Reasoning):
        print(f"Reasoning: {item}")
    elif isinstance(item, str):
        print(f"Response: {item}")
    elif isinstance(item, ImagePreview):
        print(f"Image Preview: {item}")
    elif isinstance(item, ImageResponse):
        print(f"Image Response: {item}")
    elif isinstance(item, TitleGeneration):
        print(f"Title Generation: {item}")
    elif isinstance(item, Conversation):
        print(f"Conversation ID: {item.conversation_id}")