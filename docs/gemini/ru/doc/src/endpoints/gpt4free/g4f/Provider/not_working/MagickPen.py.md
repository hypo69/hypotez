# Модуль MagickPen

## Обзор

Модуль `MagickPen` предоставляет класс `MagickPen`, который реализует асинхронный генератор ответов от модели `MagickPen.com`. 

## Подробности

`MagickPen.com` - это бесплатная платформа, предлагающая доступ к API-модели GPT-4. Модуль `MagickPen` предоставляет механизм для взаимодействия с этим API,  обходя ограничения бесплатного доступа.

## Классы

### `class MagickPen`

**Описание**: Класс `MagickPen` реализует асинхронный генератор ответов от модели `MagickPen.com`, наследуя от `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает общий интерфейс для асинхронных генераторов ответов.
- `ProviderModelMixin`: Добавляет поддержку различных моделей.

**Атрибуты**:
- `url` (str): Базовый URL для `MagickPen.com`.
- `api_endpoint` (str):  URL API-конца для запросов к модели.
- `working` (bool): Флаг, указывающий, доступен ли сервис.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли сервис потоковую передачу ответа.
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли сервис системные сообщения.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли сервис историю сообщений.
- `default_model` (str):  Название модели по умолчанию.
- `models` (list): Список доступных моделей.

**Методы**:
- `fetch_api_credentials()`: Асинхронная функция, извлекающая API-ключи из JavaScript-файла на `MagickPen.com`.
- `create_async_generator()`: Асинхронная функция, создающая генератор ответов от API.


## Методы класса

### `MagickPen.fetch_api_credentials()`

```python
    @classmethod
    async def fetch_api_credentials(cls) -> tuple:
        """
        Извлекает API-ключи из JavaScript-файла на MagickPen.com.
        
        Args:
            None
        
        Returns:
            tuple: Кортеж с API-ключами:
            - X_API_SECRET (str): API-ключ.
            - signature (str): Подпись.
            - timestamp (str): Метка времени.
            - nonce (str): Случайное число.
            - secret (str): Секретный ключ.
        
        Raises:
            Exception: Если не удалось извлечь все необходимые данные из JavaScript-файла.
        
        """
        url = "https://magickpen.com/_nuxt/bf709a9ce19f14e18116.js"
        async with ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
        
        pattern = r\'"X-API-Secret":"(\\w+)"\'\n        match = re.search(pattern, text)\n        X_API_SECRET = match.group(1) if match else None
        
        timestamp = str(int(time.time() * 1000))
        nonce = str(random.random())
        
        s = ["TGDBU9zCgM", timestamp, nonce]
        s.sort()
        signature_string = \'\'.join(s)
        signature = hashlib.md5(signature_string.encode()).hexdigest()
        
        pattern = r\'secret:"(\\w+)"\'\n        match = re.search(pattern, text)\n        secret = match.group(1) if match else None
        
        if X_API_SECRET and timestamp and nonce and secret:
            return X_API_SECRET, signature, timestamp, nonce, secret
        else:
            raise Exception("Unable to extract all the necessary data from the JavaScript file.")
```

**Назначение**: 
Извлекает API-ключи из JavaScript-файла на `MagickPen.com`, необходимых для  авторизации запросов к модели.

**Параметры**: 
-  Отсутствуют

**Возвращает**:
-  `tuple`: Кортеж, содержащий API-ключи `X_API_SECRET`, `signature`, `timestamp`, `nonce`, `secret`.

**Вызывает исключения**:
- `Exception`: Если не удалось извлечь все необходимые данные из JavaScript-файла.

**Как работает функция**:
1.  Функция отправляет запрос к `https://magickpen.com/_nuxt/bf709a9ce19f14e18116.js`  и извлекает содержимое файла.
2.  Из полученного текста с помощью регулярных выражений извлекаются следующие данные: 
    -  `X_API_SECRET`: API-ключ
    -  `secret`: Секретный ключ.
3.  Генерируются временная метка `timestamp`,  случайное число `nonce` и подпись `signature` на основе `X_API_SECRET` и `secret`.
4.  Если все данные извлечены, возвращается кортеж с ними.
5.  Если не удалось извлечь все данные, вызывается исключение `Exception`.

**Пример**:
```python
>>> from src.endpoints.gpt4free.g4f.Provider.not_working.MagickPen import MagickPen
>>> credentials = MagickPen.fetch_api_credentials()
>>> print(credentials)
('...', '...', '...', '...', '...')
```

### `MagickPen.create_async_generator()`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор ответов от API.
        
        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки модели.
            proxy (str, optional): Прокси-сервер для запросов. По умолчанию None.
            **kwargs: Дополнительные параметры.
        
        Returns:
            AsyncResult: Асинхронный результат с генератором ответов.
        
        Raises:
            Exception: Если произошла ошибка во время получения ответа от API.
        
        """
        model = cls.get_model(model)
        X_API_SECRET, signature, timestamp, nonce, secret = await cls.fetch_api_credentials()
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'nonce': nonce,
            'origin': cls.url,
            'referer': f"{cls.url}/",
            'secret': secret,
            'signature': signature,
            'timestamp': timestamp,
            'x-api-secret': X_API_SECRET,
        }
        
        async with ClientSession(headers=headers) as session:
            prompt = format_prompt(messages)
            payload = {
                'query': prompt,
                'turnstileResponse': '',
                'action': 'verify'
            }
            async with session.post(cls.api_endpoint, json=payload, proxy=proxy) as response:
                response.raise_for_status()
                async for chunk in response.content:
                    if chunk:
                        yield chunk.decode()
```

**Назначение**:
Создает асинхронный генератор ответов от API-модели `MagickPen.com`.

**Параметры**: 
- `model` (str): Название модели.
- `messages` (Messages): Список сообщений для отправки модели.
- `proxy` (str, optional): Прокси-сервер для запросов. По умолчанию `None`.
- `**kwargs`:  Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный результат с генератором ответов.

**Вызывает исключения**:
- `Exception`: Если произошла ошибка во время получения ответа от API.

**Как работает функция**:
1.  Функция получает модель из списка `models` и извлекает API-ключи с помощью `fetch_api_credentials()`.
2.  Создается заголовок запроса `headers`  с использованием полученных ключей.
3.  Сформирован запрос с `prompt`, содержащий историю сообщений.
4.  Отправляется POST-запрос к `api_endpoint` с использованием `session`.
5.  Обработка ответа от API:  
    -  Проверка статуса ответа.
    -  Генерация и отправка ответа по частям (chunked) для экономии памяти.

**Пример**:
```python
>>> from src.endpoints.gpt4free.g4f.Provider.not_working.MagickPen import MagickPen
>>> from ...typing import Messages
>>> messages:Messages = [
...     {'role': 'user', 'content': 'Привет! Как дела?'},
... ]
>>> generator = MagickPen.create_async_generator(model='gpt-4o-mini', messages=messages)
>>> async for chunk in generator:
...     print(chunk, end='')
Привет! У меня все отлично. Что насчет тебя?