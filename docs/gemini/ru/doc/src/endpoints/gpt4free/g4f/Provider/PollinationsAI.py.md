# Модуль `PollinationsAI`

## Обзор

Модуль `PollinationsAI` предоставляет асинхронный интерфейс для взаимодействия с API Pollinations AI, который позволяет генерировать как текст, так и изображения. Модуль поддерживает потоковую передачу данных, кэширование и различные параметры настройки для генерации контента.

## Подробней

Модуль `PollinationsAI` является частью проекта `hypotez` и предназначен для интеграции с сервисом Pollinations AI, предоставляющим возможности генерации контента на основе моделей машинного обучения. Модуль асинхронный, что позволяет эффективно обрабатывать запросы к API, не блокируя основной поток выполнения.

## Классы

### `PollinationsAI`

**Описание**: Класс `PollinationsAI` является основным классом модуля, который реализует функциональность взаимодействия с API Pollinations AI.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронной генерации данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, "Pollinations AI".
- `url` (str): URL сервиса Pollinations AI, "https://pollinations.ai".
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (True).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (True).
- `text_api_endpoint` (str): URL для текстового API, "https://text.pollinations.ai".
- `openai_endpoint` (str): URL для OpenAI API, "https://text.pollinations.ai/openai".
- `image_api_endpoint` (str): URL для API генерации изображений, "https://image.pollinations.ai/".
- `default_model` (str): Модель по умолчанию для генерации текста, "openai".
- `default_image_model` (str): Модель по умолчанию для генерации изображений, "flux".
- `default_vision_model` (str): Модель по умолчанию для задач, связанных с компьютерным зрением, совпадает с `default_model`.
- `text_models` (list): Список поддерживаемых текстовых моделей, включающий `default_model`.
- `image_models` (list): Список поддерживаемых моделей для генерации изображений, включающий `default_image_model`.
- `extra_image_models` (list): Список дополнительных моделей для генерации изображений.
- `vision_models` (list): Список моделей для задач компьютерного зрения.
- `extra_text_models` (list): Список дополнительных текстовых моделей.
- `_models_loaded` (bool): Флаг, указывающий на то, что список моделей был загружен (False).
- `model_aliases` (dict): Словарь псевдонимов моделей.

**Методы**:
- `get_models()`: Получает список доступных моделей.
- `create_async_generator()`: Создает асинхронный генератор для генерации контента.
- `_generate_image()`: Генерирует изображение на основе заданных параметров.
- `_generate_text()`: Генерирует текст на основе заданных параметров.

### `PollinationsAI.get_models`

```python
    @classmethod
    def get_models(cls, **kwargs):
        """
        Получает список доступных моделей из API Pollinations AI.

        Args:
            **kwargs: Дополнительные параметры.

        Returns:
            list: Список доступных текстовых и графических моделей.

        Raises:
            Exception: Если не удается получить список моделей, используются модели по умолчанию.

        Как работает функция:
        1. Проверяет, были ли уже загружены модели (cls._models_loaded). Если да, возвращает текущий список.
        2. Пытается получить список моделей изображений с image.pollinations.ai/models.
        3. Пытается получить список текстовых моделей с text.pollinations.ai/models.
        4. Объединяет все списки моделей, удаляя дубликаты.
        5. В случае ошибки при получении списка моделей, использует модели по умолчанию.
        6. Устанавливает флаг cls._models_loaded в True.

        ASCII flowchart:
        A: Проверка: cls._models_loaded == False
        |
        B: Получение списка моделей изображений
        |
        C: Получение списка текстовых моделей
        |
        D: Объединение списков моделей
        |
        E: Обработка исключений
        |
        F: cls._models_loaded = True
        |
        G: Возврат списка моделей

        Примеры:
        >>> PollinationsAI.get_models()
        ['openai', 'flux']
        """
```

### `PollinationsAI.create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        proxy: str = None,
        cache: bool = False,
        # Image generation parameters
        prompt: str = None,
        aspect_ratio: str = "1:1",
        width: int = None,
        height: int = None,
        seed: Optional[int] = None,
        nologo: bool = True,
        private: bool = False,
        enhance: bool = False,
        safe: bool = False,
        n: int = 1,
        # Text generation parameters
        media: MediaListType = None,
        temperature: float = None,
        presence_penalty: float = None,
        top_p: float = None,
        frequency_penalty: float = None,
        response_format: Optional[dict] = None,
        extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "voice", "modalities", "audio"],
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для генерации текста или изображений.

        Args:
            model (str): Название модели для использования.
            messages (Messages): Список сообщений для генерации текста.
            stream (bool): Флаг, указывающий на потоковую передачу данных (True).
            proxy (str): URL прокси-сервера (None).
            cache (bool): Флаг, указывающий на использование кэша (False).
            prompt (str): Текст запроса для генерации изображения (None).
            aspect_ratio (str): Соотношение сторон изображения ("1:1").
            width (int): Ширина изображения (None).
            height (int): Высота изображения (None).
            seed (Optional[int]): Зерно для случайной генерации (None).
            nologo (bool): Флаг, указывающий на отсутствие логотипа (True).
            private (bool): Флаг, указывающий на приватность (False).
            enhance (bool): Флаг, указывающий на улучшение качества (False).
            safe (bool): Флаг, указывающий на безопасный режим (False).
            n (int): Количество генерируемых изображений (1).
            media (MediaListType): Список медиа-файлов для генерации текста (None).
            temperature (float): Температура для генерации текста (None).
            presence_penalty (float): Штраф за присутствие токенов (None).
            top_p (float): Вероятность выбора наиболее вероятных токенов (None).
            frequency_penalty (float): Штраф за частоту токенов (None).
            response_format (Optional[dict]): Формат ответа (None).
            extra_parameters (list[str]): Список дополнительных параметров.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий чанки сгенерированного контента.

        Raises:
            ModelNotFoundError: Если указанная модель не найдена.
            Exception: Прочие исключения, возникшие в процессе генерации.

        Как работает функция:
        1. Загружает список доступных моделей, вызывая метод `cls.get_models()`.
        2. Определяет, нужно ли использовать аудио-модель, проверяя наличие аудиоданных в `media` или параметре `kwargs`.
        3. Получает модель, используя метод `cls.get_model(model)`.
        4. Если модель относится к списку моделей изображений, вызывает метод `cls._generate_image()` для генерации изображения.
        5. Если модель относится к списку текстовых моделей, вызывает метод `cls._generate_text()` для генерации текста.
        6. Возвращает асинхронный генератор, который выдает чанки сгенерированного контента.

        ASCII flowchart:
        A: Загрузка списка моделей (cls.get_models())
        |
        B: Определение типа модели (аудио/изображение/текст)
        |
        C: Вызов соответствующего метода генерации (_generate_image или _generate_text)
        |
        D: Возврат асинхронного генератора

        Примеры:
        >>> async for chunk in PollinationsAI.create_async_generator(model="openai", messages=[{"role": "user", "content": "Hello"}], stream=True):
        ...     print(chunk)

        >>> async for chunk in PollinationsAI.create_async_generator(model="flux", prompt="A beautiful landscape", aspect_ratio="16:9"):
        ...     print(chunk)
        """
        # Load model list
        cls.get_models()
        if not model:
            has_audio = "audio" in kwargs
            if not has_audio and media is not None:
                for media_data, filename in media:
                    if is_data_an_audio(media_data, filename):\n
                        has_audio = True
                        break
            model = next(iter(cls.audio_models)) if has_audio else model
        try:
            model = cls.get_model(model)
        except ModelNotFoundError:
            if model not in cls.image_models:
                raise

        if model in cls.image_models:
            async for chunk in cls._generate_image(
                model=model,
                prompt=format_image_prompt(messages, prompt),
                proxy=proxy,
                aspect_ratio=aspect_ratio,
                width=width,
                height=height,
                seed=seed,
                cache=cache,
                nologo=nologo,
                private=private,
                enhance=enhance,
                safe=safe,
                n=n
            ):
                yield chunk
        else:
            async for result in cls._generate_text(
                model=model,
                messages=messages,
                media=media,
                proxy=proxy,
                temperature=temperature,
                presence_penalty=presence_penalty,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                response_format=response_format,
                seed=seed,
                cache=cache,
                stream=stream,
                extra_parameters=extra_parameters,
                **kwargs
            ):
                yield result
```

### `PollinationsAI._generate_image`

```python
    @classmethod
    async def _generate_image(
        cls,
        model: str,
        prompt: str,
        proxy: str,
        aspect_ratio: str,
        width: int,
        height: int,
        seed: Optional[int],
        cache: bool,
        nologo: bool,
        private: bool,
        enhance: bool,
        safe: bool,
        n: int
    ) -> AsyncResult:
        """
        Генерирует изображение с использованием API Pollinations AI.

        Args:
            model (str): Модель для генерации изображения.
            prompt (str): Текст запроса для генерации изображения.
            proxy (str): URL прокси-сервера (None).
            aspect_ratio (str): Соотношение сторон изображения.
            width (int): Ширина изображения.
            height (int): Высота изображения.
            seed (Optional[int]): Зерно для случайной генерации (None).
            nologo (bool): Флаг, указывающий на отсутствие логотипа.
            private (bool): Флаг, указывающий на приватность.
            enhance (bool): Флаг, указывающий на улучшение качества.
            safe (bool): Флаг, указывающий на безопасный режим.
            n (int): Количество генерируемых изображений.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий URL сгенерированных изображений.

        Raises:
            Exception: Если не удается получить изображение.

        Внутренние функции:
          - `get_image_url(i: int = 0, seed: Optional[int] = None) -> str`: Формирует URL для запроса изображения.

        Как работает функция:
        1. Формирует параметры запроса, используя функцию `use_aspect_ratio`.
        2. Создает URL для запроса к API генерации изображений.
        3. Определяет внутреннюю функцию `get_image_url`, которая формирует URL для получения изображения с учетом параметров `seed` и `cache`.
        4. Отправляет асинхронный GET-запрос к API.
        5. В случае ошибки логирует ее и возвращает URL ответа.
        6. Возвращает объект `ImageResponse`, содержащий список URL сгенерированных изображений и исходный запрос.

        ASCII flowchart:
        A: Формирование параметров запроса
        |
        B: Создание URL запроса
        |
        C: Определение внутренней функции get_image_url
        |
        D: Отправка асинхронного GET-запроса
        |
        E: Обработка ошибок и возврат URL ответа
        |
        F: Возврат ImageResponse

        Примеры:
        >>> async for chunk in PollinationsAI._generate_image(model="flux", prompt="A cat", aspect_ratio="1:1", width=512, height=512, n=1):
        ...     print(chunk)
        """
        params = use_aspect_ratio({\n
            "width": width,
            "height": height,
            "model": model,
            "nologo": str(nologo).lower(),
            "private": str(private).lower(),
            "enhance": str(enhance).lower(),
            "safe": str(safe).lower()
        }, aspect_ratio)
        query = "&".join(f"{k}={quote_plus(str(v))}" for k, v in params.items() if v is not None)
        prompt = quote_plus(prompt)[:2048-256-len(query)]
        url = f"{cls.image_api_endpoint}prompt/{prompt}?{query}"

        def get_image_url(i: int = 0, seed: Optional[int] = None):
            """
            Формирует URL для запроса изображения.

            Args:
                i (int): Индекс изображения.
                seed (Optional[int]): Зерно для случайной генерации.

            Returns:
                str: URL для запроса изображения.
            """
            if i == 0:
                if not cache and seed is None:
                    seed = random.randint(0, 2**32)
            else:
                seed = random.randint(0, 2**32)
            return f"{url}&seed={seed}" if seed else url

        async with ClientSession(headers=DEFAULT_HEADERS, connector=get_connector(proxy=proxy)) as session:
            async def get_image(i: int = 0, seed: Optional[int] = None):
                """
                Получает URL изображения.

                Args:
                    i (int): Индекс изображения.
                    seed (Optional[int]): Зерно для случайной генерации.

                Returns:
                    str: URL изображения.
                """
                async with session.get(get_image_url(i, seed), allow_redirects=False) as response:
                    try:
                        await raise_for_status(response)
                    except Exception as ex:
                        debug.error(f"Error fetching image: {ex}")
                        return str(response.url)
                    return str(response.url)
            yield ImageResponse(await asyncio.gather(*[\n
                get_image(i, seed) for i in range(int(n))\n
            ]), prompt)
```

### `PollinationsAI._generate_text`

```python
    @classmethod
    async def _generate_text(
        cls,
        model: str,
        messages: Messages,
        media: MediaListType,
        proxy: str,
        temperature: float,
        presence_penalty: float,
        top_p: float,
        frequency_penalty: float,
        response_format: Optional[dict],\n
        seed: Optional[int],\n
        cache: bool,
        stream: bool,
        extra_parameters: list[str],\n
        **kwargs
    ) -> AsyncResult:
        """
        Генерирует текст с использованием API Pollinations AI.

        Args:
            model (str): Модель для генерации текста.
            messages (Messages): Список сообщений для генерации текста.
            media (MediaListType): Список медиа-файлов для генерации текста.
            proxy (str): URL прокси-сервера.
            temperature (float): Температура для генерации текста.
            presence_penalty (float): Штраф за присутствие токенов.
            top_p (float): Top P-значение для генерации текста.
            frequency_penalty (float): Штраф за частоту токенов.
            response_format (Optional[dict]): Формат ответа.
            seed (Optional[int]): Зерно для случайной генерации.
            cache (bool): Флаг, указывающий на использование кэша.
            stream (bool): Флаг, указывающий на потоковую передачу данных.
            extra_parameters (list[str]): Список дополнительных параметров.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий чанки сгенерированного текста.

        Raises:
            Exception: Если не удается сгенерировать текст.

        Как работает функция:
        1. Устанавливает случайное зерно, если оно не задано и кэширование не используется.
        2. Определяет, включен ли режим JSON.
        3. Отправляет POST-запрос к API text или OpenAI в зависимости от модели.
        4. Формирует данные запроса, включая сообщения, модель, параметры генерации и прочее.
        5. Обрабатывает различные типы ответов: plain text, event stream, JSON.
        6. Извлекает сгенерированный контент из ответа и возвращает его в виде чанков.

        ASCII flowchart:
        A: Установка зерна случайности
        |
        B: Определение режима JSON
        |
        C: Отправка POST-запроса к API
        |
        D: Формирование данных запроса
        |
        E: Обработка различных типов ответов
        |
        F: Извлечение и возврат контента

        Примеры:
        >>> async for chunk in PollinationsAI._generate_text(model="openai", messages=[{"role": "user", "content": "Hello"}], stream=True):
        ...     print(chunk)
        """
        if not cache and seed is None:
            seed = random.randint(9999, 99999999)
        json_mode = False
        if response_format and response_format.get("type") == "json_object":
            json_mode = True

        async with ClientSession(headers=DEFAULT_HEADERS, connector=get_connector(proxy=proxy)) as session:
            if model in cls.audio_models:
                url = cls.text_api_endpoint
                stream = False
            else:
                url = cls.openai_endpoint
            extra_parameters = {param: kwargs[param] for param in extra_parameters if param in kwargs}
            data = filter_none(**{\n
                "messages": list(render_messages(messages, media)),
                "model": model,
                "temperature": temperature,
                "presence_penalty": presence_penalty,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "jsonMode": json_mode,
                "stream": stream,
                "seed": seed,
                "cache": cache,
                **extra_parameters
            })
            async with session.post(url, json=data) as response:
                await raise_for_status(response)
                async for chunk in save_response_media(response, format_image_prompt(messages), [model]):
                    yield chunk
                    return
                if response.headers["content-type"].startswith("text/plain"):
                    yield await response.text()
                    return
                elif response.headers["content-type"].startswith("text/event-stream"):
                    async for line in response.content:
                        if line.startswith(b"data: "):\n
                            if line[6:].startswith(b"[DONE]"):
                                break
                            result = json.loads(line[6:])
                            choices = result.get("choices", [{}])
                            choice = choices.pop() if choices else {}
                            content = choice.get("delta", {}).get("content")
                            if content:
                                yield content
                            if "usage" in result:
                                yield Usage(**result["usage"])
                            finish_reason = choice.get("finish_reason")
                            if finish_reason:
                                yield FinishReason(finish_reason)
                    return
                result = await response.json()
                choice = result["choices"][0]
                message = choice.get("message", {})
                content = message.get("content", "")

                if "tool_calls" in message:
                    yield ToolCalls(message["tool_calls"])

                if content:
                    yield content

                if "usage" in result:
                    yield Usage(**result["usage"])

                finish_reason = choice.get("finish_reason")
                if finish_reason:
                    yield FinishReason(finish_reason)
```

## Функции

В данном модуле функции отсутствуют.