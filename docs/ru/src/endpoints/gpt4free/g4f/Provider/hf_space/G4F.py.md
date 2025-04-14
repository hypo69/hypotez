# Модуль `G4F.py`

## Обзор

Модуль предоставляет классы `FluxDev` и `G4F`, предназначенные для взаимодействия с сервисами генерации изображений на базе Hugging Face Spaces. Класс `G4F` является наследником класса `DeepseekAI_JanusPro7b` и предоставляет функциональность для генерации изображений с использованием моделей "flux" и "flux-dev".

## Подробнее

Этот модуль позволяет пользователям генерировать изображения, используя различные модели, предоставляемые сервисами Hugging Face Spaces. Он включает в себя функциональность для получения токенов GPU, форматирования запросов и обработки ответов от API. Модуль также обеспечивает поддержку прокси и куки для выполнения запросов.

## Классы

### `FluxDev`

**Описание**: Класс для взаимодействия с сервисом `BlackForestLabs_Flux1Dev`.

**Наследует**: `BlackForestLabs_Flux1Dev`

**Атрибуты**:
- `url` (str): URL сервиса.
- `space` (str): Имя пространства на Hugging Face.
- `referer` (str): Referer для HTTP-запросов.

### `G4F`

**Описание**: Класс для взаимодействия с сервисом `roxky/Janus-Pro-7B` через G4F framework.

**Наследует**: `DeepseekAI_JanusPro7b`

**Атрибуты**:
- `label` (str): Метка для идентификации провайдера.
- `space` (str): Имя пространства на Hugging Face.
- `url` (str): URL сервиса.
- `api_url` (str): URL API сервиса.
- `url_flux` (str): URL для выполнения запросов к flux.
- `referer` (str): Referer для HTTP-запросов.
- `default_model` (str): Модель, используемая по умолчанию ("flux").
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список моделей для генерации изображений.
- `models` (list): Список всех поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Асинхронный генератор для создания изображений.

## Функции

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        prompt: str = None,
        aspect_ratio: str = "1:1",
        width: int = None,
        height: int = None,
        seed: int = None,
        cookies: dict = None,
        api_key: str = None,
        zerogpu_uuid: str = "[object Object]",
        **kwargs
    ) -> AsyncResult:
        """
        Асинхронный генератор для создания изображений.

        Args:
            model (str): Модель для генерации изображений.
            messages (Messages): Сообщения для генерации изображения.
            proxy (str, optional): Прокси-сервер. По умолчанию `None`.
            prompt (str, optional): Текст запроса. По умолчанию `None`.
            aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
            width (int, optional): Ширина изображения. По умолчанию `None`.
            height (int, optional): Высота изображения. По умолчанию `None`.
            seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `None`.
            cookies (dict, optional): Куки для запросов. По умолчанию `None`.
            api_key (str, optional): API-ключ. По умолчанию `None`.
            zerogpu_uuid (str, optional): UUID для zerogpu. По умолчанию "[object Object]".
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий промежуточные результаты и итоговое изображение.

        Как работает функция:
        1. Проверяет, является ли модель "flux" или "flux-dev". Если да, то вызывает `FluxDev.create_async_generator` для генерации изображения.
        2. Если модель не содержит `cls.default_model`, вызывает `super().create_async_generator` для генерации изображения.
        3. Форматирует ширину и высоту изображения, чтобы они были кратны 8.
        4. Если `prompt` не предоставлен, форматирует `messages` в `prompt`.
        5. Если `seed` не предоставлен, генерирует случайное число.
        6. Формирует `payload` для запроса к API.
        7. Получает токен GPU, если `api_key` не предоставлен.
        8. Формирует заголовки запроса, включая `x-zerogpu-token` и `x-zerogpu-uuid`.
        9. Определяет внутреннюю асинхронную функцию `generate`, которая отправляет запрос к API и возвращает URL изображения.
        10. Создает и запускает асинхронную задачу для генерации изображения.
        11. Отправляет промежуточные результаты `Reasoning` с информацией о статусе генерации.
        12. После завершения задачи возвращает `ImageResponse` с URL изображения и `prompt`.
        13. Отправляет финальный результат `Reasoning` с информацией о времени завершения генерации.
        """

        # Обработка моделей "flux" и "flux-dev"
        # Вызов соответствующей функции для генерации изображения
        # Если модель не является одной из flux моделей, вызывается родительский класс
        # для обработки запроса
        # Форматирование размеров изображения и формирование запроса
        # Получение токена GPU и выполнение запроса к API
        # Обработка результатов и возврат изображения

        # Определение внутренней асинхронной функции `generate`
        # Отправка запроса к API и обработка ответа
        # Возврат URL изображения

        # Создание и запуск асинхронной задачи для генерации изображения
        # Отправка промежуточных результатов `Reasoning`
        # Возврат `ImageResponse` с URL изображения и `prompt`
        # Отправка финального результата `Reasoning`

        #A - Проверка модели и вызов соответствующего генератора
        #|
        #B - super().create_async_generator
        #|
        #C -  Форматирование размеров изображения и формирование запроса
        #|
        #D - Получение токена GPU
        #|
        #E - Отправка запроса к API и обработка ответа
        #|
        #F -  Обработка результатов и возврат изображения
        #G - Отправка финального результата `Reasoning`

        #A
        #|
        #|---B- Нет
        #|   |
        #|   |-> super().create_async_generator
        #|
        #C
        #|
        #D
        #|
        #E
        #|
        #F
        #|
        #G

        if model in ("flux", "flux-dev"):
            async for chunk in FluxDev.create_async_generator(
                model, messages,
                proxy=proxy,
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                width=width,
                height=height,
                seed=seed,
                cookies=cookies,
                api_key=api_key,
                zerogpu_uuid=zerogpu_uuid,
                **kwargs
            ):
                yield chunk
            return
        if cls.default_model not in model:
            async for chunk in super().create_async_generator(
                model, messages,
                proxy=proxy,
                prompt=prompt,
                seed=seed,
                cookies=cookies, 
                api_key=api_key,
                zerogpu_uuid=zerogpu_uuid,
                **kwargs
            ):
                yield chunk
            return

        model = cls.get_model(model)
        width = max(32, width - (width % 8))
        height = max(32, height - (height % 8))
        if prompt is None:
            prompt = format_image_prompt(messages)
        if seed is None:
            seed = random.randint(9999, 2**32 - 1)

        payload = {
            "data": [
                prompt,
                seed,
                width,
                height,
                True,
                1
            ],
            "event_data": None,
            "fn_index": 3,
            "session_hash": get_random_string(),
            "trigger_id": 10
        }
        async with ClientSession() as session:
            if api_key is None:
                yield Reasoning(status="Acquiring GPU Token")
                zerogpu_uuid, api_key = await get_zerogpu_token(cls.space, session, JsonConversation(), cookies)
            headers = {
                "x-zerogpu-token": api_key,
                "x-zerogpu-uuid": zerogpu_uuid,
            }
            headers = {k: v for k, v in headers.items() if v is not None}
            async def generate():
                """
                Внутренняя асинхронная функция для отправки запроса и обработки ответа.
                Args:
                    Отсутствуют

                Returns:
                    ImageResponse: Объект ImageResponse с URL изображения и текстом запроса.

                Raises:
                    Exception: Если при запросе возникла ошибка.

                Как работает внутренняя функция:
                1. Отправляет POST-запрос к `cls.url_flux` с данными `payload`, прокси и заголовками.
                2. Проверяет статус ответа с помощью `raise_for_status`.
                3. Преобразует ответ в JSON.
                4. Извлекает URL изображения из JSON-ответа.
                5. Возвращает объект `ImageResponse` с URL изображения и текстом запроса.

                Примеры:
                    Этот метод вызывается только внутри `create_async_generator`, поэтому примеры его прямого вызова не требуются.
                """
                async with session.post(cls.url_flux, json=payload, proxy=proxy, headers=headers) as response:
                    await raise_for_status(response)
                    response_data = await response.json()
                    image_url = response_data["data"][0]['url']
                    return ImageResponse(image_url, alt=prompt)
            background_tasks = set()
            started = time.time()
            task = asyncio.create_task(generate())
            background_tasks.add(task)
            task.add_done_callback(background_tasks.discard)
            while background_tasks:
                yield Reasoning(status=f"Generating {time.time() - started:.2f}s")
                await asyncio.sleep(0.2)
            yield await task
            yield Reasoning(status=f"Finished {time.time() - started:.2f}s")
```

**Примеры**:

```python
# Пример использования функции create_async_generator
# (код для примера, может потребоваться адаптация)
# async for chunk in G4F.create_async_generator(model="flux", messages=[{"role": "user", "content": "A cat"}], width=512, height=512):
#     print(chunk)