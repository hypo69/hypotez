# Модуль BlackForestLabs_Flux1Schnell

## Обзор

Модуль `BlackForestLabs_Flux1Schnell` предоставляет класс `BlackForestLabs_Flux1Schnell`, который реализует асинхронный генератор для взаимодействия с моделью `BlackForestLabs Flux-1-Schnell`, доступной на Hugging Face Spaces. Этот модуль позволяет генерировать изображения на основе текстовых подсказок.

## Детали

### Класс `BlackForestLabs_Flux1Schnell`

```python
class BlackForestLabs_Flux1Schnell(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Класс, реализующий асинхронный генератор для модели BlackForestLabs Flux-1-Schnell.

    Inherits:
        AsyncGeneratorProvider: Базовый класс для асинхронных генераторов.
        ProviderModelMixin: Миксин для работы с моделями.

    Attributes:
        label (str): Имя модели (BlackForestLabs Flux-1-Schnell).
        url (str): URL адрес модели на Hugging Face Spaces.
        api_endpoint (str): URL адрес API для отправки запросов.
        working (bool): Флаг, указывающий, что модель доступна и работает.
        default_model (str): Название модели по умолчанию.
        default_image_model (str): Название модели по умолчанию для генерации изображений.
        model_aliases (dict): Словарь с псевдонимами для модели.
        image_models (list): Список моделей, поддерживающих генерацию изображений.
        models (list): Список всех поддерживаемых моделей.

    Methods:
        create_async_generator(model: str, messages: Messages, proxy: str = None, prompt: str = None, width: int = 768, height: int = 768, num_inference_steps: int = 2, seed: int = 0, randomize_seed: bool = True, **kwargs) -> AsyncResult:
            Создает асинхронный генератор для модели.
    """

    label = "BlackForestLabs Flux-1-Schnell"
    url = "https://black-forest-labs-flux-1-schnell.hf.space"
    api_endpoint = "https://black-forest-labs-flux-1-schnell.hf.space/call/infer"

    working = True

    default_model = "black-forest-labs-flux-1-schnell"
    default_image_model = default_model
    model_aliases = {"flux-schnell": default_image_model, "flux": default_image_model}
    image_models = list(model_aliases.keys())
    models = image_models
    
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        prompt: str = None,
        width: int = 768,
        height: int = 768,
        num_inference_steps: int = 2,
        seed: int = 0,
        randomize_seed: bool = True,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для модели.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений.
            proxy (str, optional): Прокси-сервер для запросов. По умолчанию `None`.
            prompt (str, optional): Текстовая подсказка для генерации изображения. По умолчанию `None`.
            width (int, optional): Ширина изображения. По умолчанию 768.
            height (int, optional): Высота изображения. По умолчанию 768.
            num_inference_steps (int, optional): Количество шагов для генерации. По умолчанию 2.
            seed (int, optional): Затравка для генератора случайных чисел. По умолчанию 0.
            randomize_seed (bool, optional): Флаг, указывающий, следует ли рандомизировать затравку. По умолчанию `True`.
            **kwargs: Дополнительные аргументы для модели.

        Returns:
            AsyncResult: Асинхронный результат.

        Raises:
            ResponseError: Если сервер возвращает ошибку.
        """
        width = max(32, width - (width % 8))
        height = max(32, height - (height % 8))
        prompt = format_image_prompt(messages, prompt)
        payload = {
            "data": [
                prompt,
                seed,
                randomize_seed,
                width,
                height,
                num_inference_steps
            ]
        }
        async with ClientSession() as session:
            async with session.post(cls.api_endpoint, json=payload, proxy=proxy) as response:
                await raise_for_status(response)
                response_data = await response.json()
                event_id = response_data['event_id']
                while True:
                    async with session.get(f"{cls.api_endpoint}/{event_id}", proxy=proxy) as status_response:
                        await raise_for_status(status_response)
                        while not status_response.content.at_eof():
                            event = await status_response.content.readuntil(b'\n\n')
                            if event.startswith(b'event:'):
                                event_parts = event.split(b'data: ')
                                if len(event_parts) < 2:
                                    continue
                                event_type = event_parts[0].split(b': ')[1]
                                data = event_parts[1]
                                if event_type == b'error':
                                    raise ResponseError(f"Error generating image: {data.decode(errors='ignore')}")
                                elif event_type == b'complete':
                                    json_data = json.loads(data)
                                    image_url = json_data[0]['url']
                                    yield ImageResponse(images=[image_url], alt=prompt)
                                    return
```
## Внутренние функции
### `format_image_prompt(messages: Messages, prompt: str = None) -> str:`

Функция форматирует текстовую подсказку для генерации изображения.

**Назначение**: Функция принимает список сообщений (`messages`) и необязательную текстовую подсказку (`prompt`). Она формирует строку, объединяя все сообщения и добавление `prompt`, если он не `None`. Эта строка используется как подсказка для генерации изображения.

**Параметры**:

- `messages` (Messages): Список сообщений, которые нужно объединить в подсказку.
- `prompt` (str, optional): Дополнительная текстовая подсказка для генерации изображения. По умолчанию `None`.

**Возвращает**:

- `str`: Сформированная строка с текстовой подсказкой.

**Как работает функция**:
Функция начинается с проверки значения `prompt`. Если `prompt` не `None`, то функция объединяет все сообщения в `messages` в строку, разделяя их пробелами. Затем к получившейся строке добавляется `prompt`. В противном случае, если `prompt` равен `None`, то функция просто объединяет все сообщения в `messages` в строку, разделяя их пробелами.

**Примеры**:

```python
>>> messages = ['Привет', 'как дела?']
>>> prompt = 'Я хочу увидеть картинку с кошкой.'
>>> format_image_prompt(messages, prompt)
'Привет как дела? Я хочу увидеть картинку с кошкой.'

>>> messages = ['Я хочу увидеть картинку', 'с кошкой', 'которая спит']
>>> format_image_prompt(messages)
'Я хочу увидеть картинку с кошкой которая спит'
```


### `raise_for_status(response: ClientResponse) -> None:`

Функция проверяет код ответа HTTP-запроса.

**Назначение**: Функция принимает ответ HTTP-запроса (`response`) и проверяет его код состояния. Если код состояния не равен 200, то функция вызывает исключение `ResponseError`.

**Параметры**:

- `response` (ClientResponse): Ответ HTTP-запроса.

**Возвращает**:

- `None`.

**Как работает функция**:
Функция `raise_for_status` проверяет статус ответа HTTP-запроса. Если статус не равен 200, то функция вызывает исключение ResponseError, передавая в него статус ответа и текст ошибки. 

**Примеры**:

```python
>>> response = ClientResponse(status=200, text='OK')
>>> raise_for_status(response)
>>> # Ничего не происходит, так как статус ответа 200

>>> response = ClientResponse(status=404, text='Not Found')
>>> raise_for_status(response)
>>> # Возникает исключение ResponseError, так как статус ответа 404