# Модуль `Prodia.py`

## Обзор

Модуль `Prodia.py` предоставляет асинхронный интерфейс для взаимодействия с API сервиса Prodia, который позволяет генерировать изображения на основе текстовых запросов. Этот модуль включает в себя класс `Prodia`, который наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`, и предназначен для асинхронной генерации изображений.

## Подробнее

Модуль предоставляет возможность выбора различных моделей для генерации изображений, установки параметров генерации, таких как количество шагов, уровень детализации и начальное зерно. Он также обеспечивает асинхронный опрос API для получения сгенерированного изображения.

## Классы

### `Prodia`

**Описание**: Класс `Prodia` предоставляет интерфейс для взаимодействия с API сервиса Prodia для генерации изображений на основе текстовых запросов.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для выбора и управления моделями.

**Аттрибуты**:
- `url` (str): URL главной страницы сервиса Prodia.
- `api_endpoint` (str): URL API для генерации изображений.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию для генерации изображений.
- `default_image_model` (str): Псевдоним для `default_model`.
- `image_models` (List[str]): Список доступных моделей для генерации изображений.
- `models` (List[str]): Список всех доступных моделей, включая модели изображений.

**Методы**:
- `get_model(model: str) -> str`: Возвращает имя модели на основе предоставленного псевдонима или имени, используя модель по умолчанию, если предоставленная модель не найдена.
- `create_async_generator(...) -> AsyncResult`: Асинхронно генерирует изображения на основе предоставленных параметров.
- `_poll_job(...) -> str`: Асинхронно опрашивает API для получения статуса задачи генерации изображения и возвращает URL изображения, когда задача выполнена.

## Функции

### `get_model`

```python
    @classmethod
    def get_model(cls, model: str) -> str:
        """
        Возвращает имя модели на основе предоставленного псевдонима или имени.

        Args:
            model (str): Имя или псевдоним модели.

        Returns:
            str: Имя модели.

        Как работает функция:
        1. Проверяет, есть ли предоставленная модель в списке доступных моделей (`cls.models`).
        2. Если модель не найдена в списке, проверяет, есть ли она в списке псевдонимов моделей (`cls.model_aliases`).
        3. Если модель не найдена ни в одном из списков, возвращает модель по умолчанию (`cls.default_model`).

        ASCII flowchart:
        A[Проверка наличия модели в cls.models]
        |
        B[Если модель не найдена] -- C[Проверка наличия модели в cls.model_aliases]
                                    |
                                    D[Если модель не найдена] -- E[Возврат cls.default_model]
        Примеры:
        >>> Prodia.get_model('absolutereality_v181.safetensors [3d9d4d2b]')
        'absolutereality_v181.safetensors [3d9d4d2b]'
        >>> Prodia.get_model('non_existent_model')
        'absolutereality_v181.safetensors [3d9d4d2b]'
        """
        ...
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        negative_prompt: str = "",
        steps: str = 20, # 1-25
        cfg: str = 7, # 0-20
        seed: Optional[int] = None,
        sampler: str = "DPM++ 2M Karras", # "Euler", "Euler a", "Heun", "DPM++ 2M Karras", "DPM++ SDE Karras", "DDIM"
        aspect_ratio: str = "square", # "square", "portrait", "landscape"
        **kwargs
    ) -> AsyncResult:
        """
        Асинхронно генерирует изображения на основе предоставленных параметров.

        Args:
            model (str): Имя модели для генерации изображения.
            messages (Messages): Список сообщений, содержащих текстовый запрос.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            negative_prompt (str, optional): Негативный запрос, указывающий, чего не должно быть на изображении. По умолчанию "".
            steps (str, optional): Количество шагов для генерации изображения. По умолчанию "20".
            cfg (str, optional): Уровень детализации изображения. По умолчанию "7".
            seed (Optional[int], optional): Начальное зерно для генерации случайных чисел. По умолчанию `None`.
            sampler (str, optional): Алгоритм дискретизации. По умолчанию "DPM++ 2M Karras".
            aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "square".
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий объект `ImageResponse` с URL сгенерированного изображения.

        Как работает функция:
        1. Получает имя модели с помощью метода `get_model`.
        2. Если `seed` не указан, генерирует случайное число в диапазоне от 0 до 10000.
        3. Формирует заголовки запроса.
        4. Создает асинхронную сессию `aiohttp.ClientSession` с заданными заголовками.
        5. Извлекает текстовый запрос из последнего сообщения в списке `messages`.
        6. Формирует параметры запроса, включая текстовый запрос, модель, негативный запрос, количество шагов, уровень детализации, начальное зерно и алгоритм дискретизации.
        7. Отправляет GET-запрос к API сервиса Prodia с параметрами запроса и прокси-сервером.
        8. Получает `job_id` из ответа API.
        9. Опрашивает API с помощью метода `_poll_job` для получения URL сгенерированного изображения.
        10. Генерирует объект `ImageResponse` с URL изображения и текстовым запросом.

        ASCII flowchart:
        A[Получение имени модели]
        |
        B[Генерация случайного seed, если не указан]
        |
        C[Формирование заголовков запроса]
        |
        D[Создание асинхронной сессии]
        |
        E[Извлечение текстового запроса]
        |
        F[Формирование параметров запроса]
        |
        G[Отправка GET-запроса к API]
        |
        H[Получение job_id]
        |
        I[Опрос API для получения URL изображения]
        |
        J[Генерация ImageResponse]

        Примеры:
        >>> messages = [{'content': 'A beautiful landscape'}]
        >>> async def example():
        ...     async for response in Prodia.create_async_generator(model='absolutereality_v181.safetensors [3d9d4d2b]', messages=messages):
        ...         print(response)
        >>> asyncio.run(example())
        # image_url: https://images.prodia.xyz/{job_id}.png, alt: A beautiful landscape
        """
        ...
```

### `_poll_job`

```python
    @classmethod
    async def _poll_job(cls, session: ClientSession, job_id: str, proxy: str, max_attempts: int = 30, delay: int = 2) -> str:
        """
        Асинхронно опрашивает API для получения статуса задачи генерации изображения и возвращает URL изображения, когда задача выполнена.

        Args:
            session (ClientSession): Асинхронная сессия для выполнения запросов.
            job_id (str): Идентификатор задачи генерации изображения.
            proxy (str): URL прокси-сервера.
            max_attempts (int, optional): Максимальное количество попыток опроса API. По умолчанию 30.
            delay (int, optional): Задержка в секундах между попытками опроса. По умолчанию 2.

        Returns:
            str: URL сгенерированного изображения.

        Raises:
            Exception: Если задача генерации изображения завершилась с ошибкой или истекло время ожидания.

        Как работает функция:
        1. Выполняет цикл опроса API до тех пор, пока не будет достигнуто максимальное количество попыток (`max_attempts`).
        2. Отправляет GET-запрос к API сервиса Prodia для получения статуса задачи.
        3. Получает статус задачи из ответа API.
        4. Если статус задачи равен "succeeded", возвращает URL сгенерированного изображения.
        5. Если статус задачи равен "failed", вызывает исключение `Exception`.
        6. Если статус задачи не равен ни "succeeded", ни "failed", ожидает `delay` секунд и повторяет попытку.
        7. Если после `max_attempts` попыток статус задачи не изменился, вызывает исключение `Exception`.

        ASCII flowchart:
        A[Начало цикла опроса API]
        |
        B[Отправка GET-запроса к API для получения статуса задачи]
        |
        C[Получение статуса задачи]
        |
        D[Проверка статуса: "succeeded"] -- E[Возврат URL изображения]
        |
        F[Проверка статуса: "failed"] -- G[Вызов исключения Exception]
        |
        H[Ожидание delay секунд]
        |
        I[Повторение цикла, пока не достигнуто max_attempts]
        |
        J[Вызов исключения Exception, если время ожидания истекло]

        Примеры:
        >>> import aiohttp
        >>> async def example():
        ...     async with aiohttp.ClientSession() as session:
        ...         try:
        ...             image_url = await Prodia._poll_job(session, 'job_id', None)
        ...             print(image_url)
        ...         except Exception as e:
        ...             print(f"Error: {e}")
        >>> asyncio.run(example())
        # https://images.prodia.xyz/{job_id}.png
        """
        ...