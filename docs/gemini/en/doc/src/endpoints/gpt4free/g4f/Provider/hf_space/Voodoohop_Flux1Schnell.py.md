# Документация для `Voodoohop_Flux1Schnell.py`

## Описание

Модуль `Voodoohop_Flux1Schnell.py` предоставляет реализацию асинхронного провайдера для генерации изображений с использованием API `Voodoohop Flux-1-Schnell`. Он позволяет взаимодействовать с сервисом для создания изображений на основе текстовых запросов.

## Содержание

- [Описание](#описание)
- [Классы](#классы)
    - [Voodoohop_Flux1Schnell](#voodoohop_flux1schnell)
- [Параметры класса](#параметры-класса)
- [Методы класса](#методы-класса)
    - [create_async_generator](#create_async_generator)

## Классы

### `Voodoohop_Flux1Schnell`

**Описание**:
Класс `Voodoohop_Flux1Schnell` реализует асинхронный провайдер для генерации изображений с использованием API `Voodoohop Flux-1-Schnell`.
**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовый функционал для асинхронных генераторов.
- `ProviderModelMixin`: Добавляет поддержку выбора модели.

**Атрибуты**:
- `label` (str): Метка провайдера, отображаемая пользователю.
- `url` (str): URL главной страницы провайдера.
- `api_endpoint` (str): URL API для взаимодействия.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_image_model` (str): Модель для генерации изображений по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список поддерживаемых моделей для генерации изображений.
- `models` (list): Список поддерживаемых моделей.

**Принцип работы**:
Класс предоставляет интерфейс для взаимодействия с API `Voodoohop Flux-1-Schnell` с целью генерации изображений на основе текстового запроса. Он использует асинхронные запросы для отправки запроса к API и получения результата в виде изображения.

## Параметры класса

- `label` (str): "Voodoohop Flux-1-Schnell" - Название провайдера.
- `url` (str): "https://voodoohop-flux-1-schnell.hf.space" - URL-адрес сервиса.
- `api_endpoint` (str): "https://voodoohop-flux-1-schnell.hf.space/call/infer" - URL-адрес API для запросов.
- `working` (bool): True - Указывает, что провайдер работает.
- `default_model` (str): "voodoohop-flux-1-schnell" - Модель, используемая по умолчанию.
- `default_image_model` (str): default_model - Модель для генерации изображений по умолчанию.
- `model_aliases` (dict): {"flux-schnell": default_model, "flux": default_model} - Псевдонимы моделей.
- `image_models` (list): list(model_aliases.keys()) - Список моделей для изображений.
- `models` (list): image_models - Список моделей.

## Методы класса

### `create_async_generator`

```python
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
    Создает асинхронный генератор для получения изображений от API `Voodoohop Flux-1-Schnell`.

    Args:
        cls (type[Voodoohop_Flux1Schnell]): Класс провайдера.
        model (str): Используемая модель.
        messages (Messages): Список сообщений для формирования запроса.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        prompt (str, optional): Текст запроса. По умолчанию `None`.
        width (int, optional): Ширина изображения. По умолчанию 768.
        height (int, optional): Высота изображения. По умолчанию 768.
        num_inference_steps (int, optional): Количество шагов для генерации изображения. По умолчанию 2.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию 0.
        randomize_seed (bool, optional): Флаг для рандомизации зерна. По умолчанию `True`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий объекты `ImageResponse` с URL изображений.

    Raises:
        ResponseError: Если при генерации изображения возникает ошибка.

    Как работает функция:
    - Функция принимает параметры для генерации изображения, включая модель, текст запроса, размеры изображения и другие настройки.
    - Происходит форматирование текста запроса `format_image_prompt`.
    - Создается полезная нагрузка (payload) с данными для запроса к API.
    - Устанавливается минимальный размер сторон изображения в 32 пикселя и выравнивание по 8.
    - Отправляется асинхронный POST-запрос к API с использованием `ClientSession`.
    - В цикле проверяется статус ответа, и при получении события `complete` извлекается URL изображения.
    - Если возникает ошибка, выбрасывается исключение `ResponseError`.
    - Функция возвращает асинхронный генератор, который выдает объекты `ImageResponse` с URL изображений.

    Пример:
        >>> model = "voodoohop-flux-1-schnell"
        >>> messages = [{"role": "user", "content": "A cat in space"}]
        >>> async for response in Voodoohop_Flux1Schnell.create_async_generator(model=model, messages=messages):
        ...     print(response)
        ...
        <src.providers.response.ImageResponse object at 0x...>
    """
```