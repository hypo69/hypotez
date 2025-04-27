# BlackForestLabs_Flux1Schnell Provider

## Overview

Этот модуль предоставляет класс `BlackForestLabs_Flux1Schnell`, который используется для асинхронной генерации изображений с помощью модели Flux-1-Schnell от BlackForestLabs. Модель доступна через Hugging Face Spaces.

## Details

Класс `BlackForestLabs_Flux1Schnell` реализует интерфейс `AsyncGeneratorProvider` и `ProviderModelMixin` из `hypotez`. Он обеспечивает следующие функции:

- **Асинхронная генерация изображений**: Класс позволяет асинхронно генерировать изображения с помощью модели Flux-1-Schnell.
- **Обработка подсказок**: Класс принимает текст подсказки и преобразует его в формат, подходящий для модели.
- **Обработка ответов**: Класс получает ответ от модели и преобразует его в формат `ImageResponse` для удобства использования.

## Classes

### `class BlackForestLabs_Flux1Schnell(AsyncGeneratorProvider, ProviderModelMixin)`

**Описание**: Класс `BlackForestLabs_Flux1Schnell` реализует асинхронную генерацию изображений с использованием модели Flux-1-Schnell от BlackForestLabs.

**Наследует**:
    - `AsyncGeneratorProvider`: Предоставляет функции для асинхронной генерации данных.
    - `ProviderModelMixin`: Предоставляет базовые функции для работы с моделями.

**Атрибуты**:

- `label`: Строка, которая используется для идентификации провайдера.
- `url`: Строка, которая указывает на адрес Hugging Face Spaces, где размещена модель.
- `api_endpoint`: Строка, которая указывает на конечную точку API для модели.
- `working`: Булево значение, которое указывает, доступна ли модель.
- `default_model`: Строка, которая содержит имя модели по умолчанию.
- `default_image_model`: Строка, которая содержит имя модели по умолчанию для генерации изображений.
- `model_aliases`: Словарь, который содержит псевдонимы для модели.
- `image_models`: Список строк, которые содержат имена доступных моделей для генерации изображений.
- `models`: Список строк, которые содержат имена доступных моделей.

**Методы**:

#### `create_async_generator(model: str, messages: Messages, proxy: str = None, prompt: str = None, width: int = 768, height: int = 768, num_inference_steps: int = 2, seed: int = 0, randomize_seed: bool = True, **kwargs) -> AsyncResult`

**Описание**: Функция, которая создает асинхронный генератор для получения изображений, сгенерированных моделью Flux-1-Schnell.

**Параметры**:

- `model`: Строка, которая указывает на модель, которую нужно использовать для генерации изображений.
- `messages`: Список `Messages`, содержащий текст подсказки для модели.
- `proxy`: Строка, которая указывает на прокси-сервер, который нужно использовать для доступа к модели.
- `prompt`: Строка, которая содержит текст подсказки для модели.
- `width`: Целое число, которое указывает на желаемую ширину изображения.
- `height`: Целое число, которое указывает на желаемую высоту изображения.
- `num_inference_steps`: Целое число, которое указывает на количество шагов для генерации изображения.
- `seed`: Целое число, которое указывает на начальное значение для генератора случайных чисел.
- `randomize_seed`: Булево значение, которое указывает, нужно ли использовать случайное начальное значение для генератора случайных чисел.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в модель.

**Возвращает**:
    - `AsyncResult`: Асинхронный генератор, который генерирует изображения.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Schnell import BlackForestLabs_Flux1Schnell

# Создание провайдера
provider = BlackForestLabs_Flux1Schnell()

# Создание асинхронного генератора
async_generator = await provider.create_async_generator(
    model="flux-schnell",
    messages=[
        {
            "role": "user",
            "content": "Сгенерируй изображение с котиком."
        }
    ],
    width=512,
    height=512
)

# Получение сгенерированного изображения
async for image_response in async_generator:
    # Обработка изображения
    image_url = image_response.images[0]
    # ...
```