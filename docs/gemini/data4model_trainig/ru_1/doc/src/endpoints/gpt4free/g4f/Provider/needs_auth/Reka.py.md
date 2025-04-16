# Модуль для работы с провайдером Reka для gpt4free
=================================================

Модуль содержит класс `Reka`, который используется для взаимодействия с Reka AI.
Он поддерживает как текстовые запросы, так и запросы с изображениями, требующие аутентификации.

## Обзор

Этот модуль определяет класс `Reka`, который является провайдером для взаимодействия с Reka AI API. Он поддерживает создание завершений текста и загрузку изображений для использования в запросах. Для работы требуется аутентификация.

## Подробнее

Класс `Reka` предоставляет методы для аутентификации, создания запросов к Reka AI API и загрузки изображений. Он использует куки для аутентификации и предоставляет возможность отправки запросов как в текстовом формате, так и с использованием изображений.

## Классы

### `Reka(AbstractProvider)`

**Описание**: Класс `Reka` является провайдером для взаимодействия с Reka AI API.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `domain` (str): Доменное имя Reka AI.
- `url` (str): URL Reka AI.
- `working` (bool): Указывает, работает ли провайдер.
- `needs_auth` (bool): Указывает, требуется ли аутентификация.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу.
- `default_vision_model` (str): Модель зрения по умолчанию.
- `cookies` (dict): Куки для аутентификации.
- `proxy` (str): Прокси для выполнения запросов (устанавливается в `create_completion`).

**Методы**:
- `create_completion`: Создает завершение текста на основе предоставленных сообщений и параметров.
- `upload_image`: Загружает изображение на сервер Reka AI.
- `get_access_token`: Получает токен доступа для аутентификации.

### `create_completion`

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
        Создает завершение текста на основе предоставленных сообщений и параметров.

        Args:
            model (str): Название используемой модели.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Указывает, использовать ли потоковую передачу.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
            image (ImageType, optional): Изображение для отправки. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            CreateResult: Результат создания завершения.

        Raises:
            ValueError: Если не найдены куки или `appSession` в куках для домена Reka AI.

        Как работает функция:
        1. Устанавливает прокси-сервер из аргумента `proxy` в атрибут класса `cls.proxy`.
        2. Проверяет наличие `api_key`. Если он не предоставлен, пытается получить куки для домена `cls.domain`.
        3. Если куки не найдены или отсутствует `appSession` в куках, вызывает исключение `ValueError`.
        4. Если `api_key` не предоставлен, пытается получить его с помощью метода `get_access_token`.
        5. Формирует список `conversation` на основе предоставленных сообщений, преобразуя их в формат, ожидаемый Reka AI.
        6. Если предоставлено изображение (`image`), загружает его с помощью метода `upload_image` и добавляет URL изображения и тип медиа в последнее сообщение в `conversation`.
        7. Формирует заголовки (`headers`) для HTTP-запроса, включая токен авторизации (`api_key`).
        8. Формирует данные (`json_data`) для отправки в теле запроса, включая историю разговора, параметры потоковой передачи, использования поисковой системы и интерпретатора кода, название модели и случайное зерно.
        9. Отправляет POST-запрос к Reka AI API (`/api/chat`) с использованием куки, заголовков, данных и прокси-сервера.
        10. Итерируется по строкам ответа, извлекая данные о токенах и генерируя (`yield`) разницу между текущими и предыдущими токенами.

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
### `upload_image`
```python
    def upload_image(cls, access_token, image: ImageType) -> str:
        """
        Загружает изображение на сервер Reka AI.

        Args:
            access_token (str): Токен доступа для аутентификации.
            image (ImageType): Изображение для загрузки.

        Returns:
            str: URL загруженного изображения.

        Как работает функция:
        1. Генерирует случайный токен `boundary_token` для разделения данных в форме multipart/form-data.
        2. Формирует заголовки (`headers`) для HTTP-запроса, включая токен авторизации и content-type с использованием сгенерированного токена.
        3. Преобразует изображение (`image`) в байты с помощью функции `to_bytes`.
        4. Формирует тело запроса (`data`) в формате multipart/form-data, включая данные изображения и токен разделения.
        5. Отправляет POST-запрос к Reka AI API (`/api/upload-image`) с использованием куки, заголовков, данных и прокси-сервера.
        6. Извлекает URL изображения из JSON-ответа и возвращает его.
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
### `get_access_token`
```python
    def get_access_token(cls):
        """
        Получает токен доступа для аутентификации.

        Returns:
            str: Токен доступа.

        Raises:
            ValueError: Если не удалось получить токен доступа.

        Как работает функция:
        1. Формирует заголовки (`headers`) для HTTP-запроса.
        2. Отправляет GET-запрос к Reka AI API (`/bff/auth/access_token`) с использованием куки, заголовков и прокси-сервера.
        3. Извлекает токен доступа из JSON-ответа и возвращает его.
        4. В случае ошибки вызывает исключение `ValueError` с описанием ошибки и предложением обновить куки или войти в систему.
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

        except Exception as e:
            raise ValueError(f"Failed to get access token: {e}, refresh your cookies / log in into {cls.domain}")