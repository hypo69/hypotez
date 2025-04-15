# Модуль `Prodia.py`

## Обзор

Модуль предоставляет асинхронный интерфейс для генерации изображений с использованием API Prodia. Поддерживает выбор модели, передачу текстовых запросов, задание негативных промптов и настройку параметров генерации, таких как количество шагов, коэффициент cfg, зерно (seed) и метод дискретизации (sampler).

## Подробнее

Модуль содержит класс `Prodia`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он предназначен для взаимодействия с API Prodia для генерации изображений на основе заданных параметров.

## Классы

### `Prodia`

**Описание**: Класс для асинхронной генерации изображений через API Prodia.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL главной страницы Prodia.
- `api_endpoint` (str): URL API для генерации изображений.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_image_model` (str): Модель изображения, используемая по умолчанию.
- `image_models` (list[str]): Список доступных моделей изображений.
- `models` (list[str]): Список всех доступных моделей.

**Принцип работы**:
Класс `Prodia` предназначен для асинхронной генерации изображений с использованием API Prodia. Он предоставляет методы для выбора модели, передачи текстовых запросов, задания негативных промптов и настройки параметров генерации, таких как количество шагов, коэффициент cfg, зерно (seed) и метод дискретизации (sampler).

Класс содержит атрибуты, определяющие URL главной страницы Prodia, URL API для генерации изображений, флаг, указывающий на работоспособность провайдера, модель, используемая по умолчанию, и список доступных моделей изображений.

#### `get_model`

```python
    @classmethod
    def get_model(cls, model: str) -> str:
        if model in cls.models:
            return model
        elif model in cls.model_aliases:
            return cls.model_aliases[model]
        else:
            return cls.default_model
```

**Назначение**: Получает имя модели.

**Параметры**:
- `model` (str): Имя модели.

**Возвращает**:
- `str`: Имя модели, если она найдена в списке доступных моделей или алиасов моделей. В противном случае возвращает имя модели по умолчанию.

**Как работает функция**:
Функция `get_model` принимает имя модели в качестве аргумента и возвращает соответствующее имя модели из списка доступных моделей или алиасов моделей. Если модель не найдена, возвращается модель по умолчанию.

**Примеры**:
```python
# Пример 1: Модель найдена в списке доступных моделей
model_name = Prodia.get_model('absolutereality_v181.safetensors [3d9d4d2b]')
print(model_name)  # Вывод: absolutereality_v181.safetensors [3d9d4d2b]

# Пример 2: Модель не найдена, возвращается модель по умолчанию
model_name = Prodia.get_model('unknown_model')
print(model_name)  # Вывод: absolutereality_v181.safetensors [3d9d4d2b]
```

#### `create_async_generator`

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
```

**Назначение**: Создает асинхронный генератор для генерации изображений.

**Параметры**:
- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений, содержащих запрос пользователя.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `negative_prompt` (str, optional): Негативный промпт. По умолчанию пустая строка.
- `steps` (str, optional): Количество шагов для генерации изображения. По умолчанию 20.
- `cfg` (str, optional): Коэффициент cfg. По умолчанию 7.
- `seed` (Optional[int], optional): Зерно для генерации случайных чисел. По умолчанию `None`.
- `sampler` (str, optional): Метод дискретизации. По умолчанию "DPM++ 2M Karras".
- `aspect_ratio` (str, optional): Соотношение сторон изображения. По умолчанию "square".
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий объекты `ImageResponse`.

**Как работает функция**:
Функция `create_async_generator` создает асинхронный генератор для генерации изображений с использованием API Prodia. Она принимает параметры, такие как имя модели, список сообщений, прокси-сервер, негативный промпт, количество шагов, коэффициент cfg, зерно и метод дискретизации.

Внутри функции происходит выбор модели, формирование параметров запроса к API Prodia и выполнение запроса с использованием асинхронной сессии. После получения идентификатора задания функция вызывает метод `_poll_job` для ожидания завершения генерации изображения и получения URL изображения.

**Примеры**:
```python
# Пример: Создание асинхронного генератора для генерации изображения
async def main():
    model = 'absolutereality_v181.safetensors [3d9d4d2b]'
    messages = [{'role': 'user', 'content': 'A beautiful landscape'}]
    async for image_response in Prodia.create_async_generator(model=model, messages=messages):
        print(image_response.image_url)

if __name__ == '__main__':
    asyncio.run(main())
```

#### `_poll_job`

```python
    @classmethod
    async def _poll_job(cls, session: ClientSession, job_id: str, proxy: str, max_attempts: int = 30, delay: int = 2) -> str:
        for _ in range(max_attempts):
            async with session.get(f"https://api.prodia.com/job/{job_id}", proxy=proxy) as response:
                response.raise_for_status()
                job_status = await response.json()

                if job_status["status"] == "succeeded":
                    return f"https://images.prodia.xyz/{job_id}.png"
                elif job_status["status"] == "failed":
                    raise Exception("Image generation failed")

            await asyncio.sleep(delay)

        raise Exception("Timeout waiting for image generation")
```

**Назначение**: Опрашивает API Prodia для получения статуса задания генерации изображения.

**Параметры**:
- `session` (ClientSession): Асинхронная сессия для выполнения HTTP-запросов.
- `job_id` (str): Идентификатор задания.
- `proxy` (str): Адрес прокси-сервера.
- `max_attempts` (int, optional): Максимальное количество попыток опроса. По умолчанию 30.
- `delay` (int, optional): Задержка между попытками опроса в секундах. По умолчанию 2.

**Возвращает**:
- `str`: URL сгенерированного изображения.

**Вызывает исключения**:
- `Exception`: Если генерация изображения завершилась неудачей или превышено максимальное количество попыток опроса.

**Как работает функция**:
Функция `_poll_job` опрашивает API Prodia для получения статуса задания генерации изображения. Она выполняет HTTP-запросы к API Prodia с использованием асинхронной сессии и проверяет статус задания. Если статус задания "succeeded", функция возвращает URL сгенерированного изображения. Если статус задания "failed", функция вызывает исключение. Если превышено максимальное количество попыток опроса, функция также вызывает исключение.

**Примеры**:
```python
# Пример: Опрос API Prodia для получения статуса задания
async def main():
    async with ClientSession() as session:
        job_id = '12345'
        image_url = await Prodia._poll_job(session, job_id, proxy=None)
        print(image_url)

if __name__ == '__main__':
    asyncio.run(main())