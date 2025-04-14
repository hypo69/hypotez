# Модуль для работы с провайдером Reka (space.reka.ai)
=========================================================

Модуль содержит класс `Reka`, который используется для взаимодействия с AI-моделью Reka.
Этот класс предоставляет методы для создания запросов к модели, загрузки изображений и получения токена доступа.

## Оглавление
- [Обзор](#обзор)
- [Подробнее](#подробнее)
- [Классы](#классы)
    - [Reka](#Reka)
        - [Метод `create_completion`](#create_completion)
        - [Метод `upload_image`](#upload_image)
        - [Метод `get_access_token`](#get_access_token)

## Обзор

Модуль `Reka` предоставляет функциональность для взаимодействия с AI-моделью, размещенной на платформе `space.reka.ai`.
Он включает в себя методы для отправки текстовых сообщений и изображений, а также для получения ответов от модели.
Модуль требует аутентификации через cookies или API-ключ.

## Подробнее

Класс `Reka` наследуется от `AbstractProvider` и реализует методы для создания запросов к AI-модели Reka, загрузки изображений и получения токена доступа.
Для работы с классом требуется либо действующий API-ключ, либо cookies аутентифицированной сессии на сайте `space.reka.ai`.
Если API-ключ не предоставлен, класс пытается получить его автоматически из cookies.

## Классы

### `Reka`

**Описание**: Класс для взаимодействия с AI-моделью Reka на платформе `space.reka.ai`.

**Наследует**:
- `AbstractProvider`: Абстрактный базовый класс для провайдеров AI-моделей.

**Атрибуты**:
- `domain` (str): Доменное имя платформы Reka ("space.reka.ai").
- `url` (str): URL платформы Reka (f"https://{domain}").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (True).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (True).
- `default_vision_model` (str): Название модели для работы с изображениями ("reka").
- `cookies` (dict): Словарь с cookies для аутентификации.

#### Метод `create_completion`

```python
    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: str = None,
        api_key: str = None,
        image: ImageType = None,
        **kwargs
    ) -> CreateResult:
        """
        Создает запрос к AI-модели Reka и возвращает результат.

        Args:
            model (str): Название используемой модели.
            messages (Messages): Список сообщений для отправки модели.
                                  Каждое сообщение должно содержать ключи "type" (human или assistant) и "text" (содержимое сообщения).
            stream (bool): Флаг, указывающий на необходимость потоковой передачи данных.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            api_key (str, optional): API-ключ для аутентификации. Если не указан, будет предпринята попытка получить его из cookies. По умолчанию `None`.
            image (ImageType, optional): Изображение для отправки модели. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Returns:
            CreateResult: Результат запроса к модели.

        Raises:
            ValueError: Если не найдены cookies или отсутствует appSession в cookies, а также если не указан api_key.

        Как работает функция:
        1. Функция принимает параметры запроса, включая модель, сообщения, флаг потоковой передачи, прокси, API-ключ и изображение.
        2. Если API-ключ не предоставлен, функция пытается получить его из cookies. Если cookies отсутствуют или не содержат appSession, выбрасывается исключение ValueError.
        3. Формируется структура conversation, содержащая сообщения для отправки модели.
        4. Если предоставлено изображение, оно загружается на сервер Reka, и в conversation добавляется информация об изображении.
        5. Формируются заголовки запроса, включая API-ключ.
        6. Отправляется POST-запрос к API Reka с использованием библиотеки requests.
        7. Полученные данные обрабатываются построчно, извлекаются текстовые фрагменты и возвращаются в виде потока.

        ASCII flowchart:

        Начало --> Проверка API-ключа
                 |
                 Нет API-ключа --> Получение API-ключа из Cookies --> Проверка наличия Cookies
                 |                                                    |
                 Да API-ключ   --> Формирование структуры Conversation <-- Нет Cookies --> Ошибка
                 |
                 Наличие изображения --> Загрузка изображения --> Добавление информации об изображении в Conversation
                 |
                 Формирование заголовков запроса
                 |
                 Отправка POST-запроса к API Reka
                 |
                 Обработка потока данных ответа
                 |
                 Извлечение текстовых фрагментов
                 |
                 Возврат результата в виде потока
                 ↓
                 Конец

        Примеры:
            Пример 1: Создание запроса с использованием API-ключа
            ```python
            result = Reka.create_completion(
                model="reka-core",
                messages=[{"role": "user", "content": "Hello, Reka!"}],
                stream=True,
                api_key="YOUR_API_KEY"
            )
            for token in result:
                print(token, end="")
            ```

            Пример 2: Создание запроса с использованием cookies (предполагается, что cookies уже установлены)
            ```python
            Reka.cookies = {"appSession": "YOUR_APP_SESSION_COOKIE"}
            result = Reka.create_completion(
                model="reka-core",
                messages=[{"role": "user", "content": "Hello, Reka!"}],
                stream=True
            )
            for token in result:
                print(token, end="")
            ```

            Пример 3: Создание запроса с изображением
            ```python
            with open("image.png", "rb") as image_file:
                image_data = image_file.read()

            result = Reka.create_completion(
                model="reka-core",
                messages=[{"role": "user", "content": "Describe this image."}],
                stream=True,
                api_key="YOUR_API_KEY",
                image=image_data
            )
            for token in result:
                print(token, end="")
            ```
        """
        cls.proxy = proxy

        if not api_key:
            cls.cookies = get_cookies(cls.domain)
            if not cls.cookies:
                raise ValueError(f"No cookies found for {cls.domain}")
            elif "appSession" not in cls.cookies:
                raise ValueError(f"No appSession found in cookies for {cls.domain}, log in or provide bearer_auth")
            api_key = cls.get_access_token(cls)

        conversation = []
        for message in messages:
            conversation.append({
                "type": "human",
                "text": message["content"],
            })

        if image:
            image_url = cls.upload_image(cls, api_key, image)
            conversation[-1]["image_url"] = image_url
            conversation[-1]["media_type"] = "image"

        headers = {
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'authorization': f'Bearer {api_key}',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': cls.url,
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        json_data = {
            'conversation_history': conversation,
            'stream': True,
            'use_search_engine': False,
            'use_code_interpreter': False,
            'model_name': 'reka-core',
            'random_seed': int(time.time() * 1000),
        }

        tokens = ''

        response = requests.post(f'{cls.url}/api/chat', 
                                cookies=cls.cookies, headers=headers, json=json_data, proxies=cls.proxy, stream=True)

        for completion in response.iter_lines():
            if b'data' in completion:
                token_data = json.loads(completion.decode('utf-8')[5:])['text']

                yield (token_data.replace(tokens, ''))

                tokens = token_data
```

#### Метод `upload_image`

```python
    def upload_image(cls, access_token: str, image: ImageType) -> str:
        """
        Загружает изображение на сервер Reka.

        Args:
            access_token (str): Токен доступа для аутентификации.
            image (ImageType): Изображение для загрузки.

        Returns:
            str: URL загруженного изображения.

        Как работает функция:
        1. Функция принимает токен доступа и изображение.
        2. Генерируется случайный токен boundary_token для формирования multipart/form-data запроса.
        3. Формируются заголовки запроса, включая токен доступа и Content-Type.
        4. Изображение преобразуется в байты с помощью функции to_bytes.
        5. Формируется тело запроса в формате multipart/form-data, включая данные изображения.
        6. Отправляется POST-запрос к API Reka для загрузки изображения.
        7. Полученный ответ преобразуется в JSON и возвращается URL загруженного изображения.

        ASCII flowchart:
        Начало --> Генерация boundary_token
                 |
                 Формирование заголовков запроса
                 |
                 Преобразование изображения в байты
                 |
                 Формирование тела запроса в формате multipart/form-data
                 |
                 Отправка POST-запроса к API Reka для загрузки изображения
                 |
                 Преобразование ответа в JSON
                 |
                 Возврат URL загруженного изображения
                 ↓
                 Конец
        Примеры:
            Пример: Загрузка изображения и получение URL
            ```python
            with open("image.png", "rb") as image_file:
                image_data = image_file.read()
            access_token = "YOUR_ACCESS_TOKEN"
            image_url = Reka.upload_image(access_token, image_data)
            print(f"Image URL: {image_url}")
            ```
        """
        boundary_token = os.urandom(8).hex()

        headers = {
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cache-control': 'no-cache',
            'authorization': f'Bearer {access_token}',
            'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary{boundary_token}',
            'origin': cls.url,
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'{cls.url}/chat/hPReZExtDOPvUfF8vCPC',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        image_data = to_bytes(image)

        boundary = f'----WebKitFormBoundary{boundary_token}'
        data = f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="image.png"\r\nContent-Type: image/png\r\n\r\n'
        data += image_data.decode('latin-1')
        data += f'\r\n--{boundary}--\r\n'

        response = requests.post(f'{cls.url}/api/upload-image', 
                                    cookies=cls.cookies, headers=headers, proxies=cls.proxy, data=data.encode('latin-1'))

        return response.json()['media_url']
```

#### Метод `get_access_token`

```python
    def get_access_token(cls) -> str:
        """
        Получает токен доступа для аутентификации.

        Returns:
            str: Токен доступа.

        Raises:
            ValueError: Если не удалось получить токен доступа.

        Как работает функция:
        1. Функция формирует заголовки запроса.
        2. Отправляется GET-запрос к API Reka для получения токена доступа.
        3. Полученный ответ преобразуется в JSON и извлекается токен доступа.
        4. Если получение токена не удалось, выбрасывается исключение ValueError.

        ASCII flowchart:

        Начало --> Формирование заголовков запроса
                 |
                 Отправка GET-запроса к API Reka для получения токена доступа
                 |
                 Преобразование ответа в JSON
                 |
                 Извлечение токена доступа
                 |
                 Успешно --> Возврат токена доступа
                 |
                 Неуспешно --> Выброс исключения ValueError
                 ↓
                 Конец

        Примеры:
            Пример: Получение токена доступа
            ```python
            Reka.cookies = {"appSession": "YOUR_APP_SESSION_COOKIE"}
            access_token = Reka.get_access_token()
            print(f"Access Token: {access_token}")
            ```
        """
        headers = {
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'{cls.url}/chat',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        try:
            response = requests.get(f'{cls.url}/bff/auth/access_token', 
                                    cookies=cls.cookies, headers=headers, proxies=cls.proxy)

            return response.json()['accessToken']

        except Exception as ex:
            raise ValueError(f"Failed to get access token: {ex}, refresh your cookies / log in into {cls.domain}")