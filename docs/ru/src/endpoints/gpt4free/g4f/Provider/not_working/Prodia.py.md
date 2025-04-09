# Модуль `Prodia`

## Обзор

Модуль `Prodia` предоставляет асинхронный интерфейс для взаимодействия с API сервиса Prodia для генерации изображений. Он позволяет генерировать изображения на основе текстовых запросов, используя различные модели и параметры. Модуль поддерживает выбор модели, задание негативного запроса, количества шагов, конфигурации (CFG), зерна (seed), метода выборки (sampler) и соотношения сторон (aspect ratio).

## Подробнее

Модуль `Prodia` является асинхронным провайдером, реализующим функциональность генерации изображений с использованием API сервиса Prodia. Он наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, что обеспечивает возможность использования различных моделей и асинхронную обработку запросов.
Модуль предназначен для интеграции в системы, требующие автоматической генерации изображений на основе текстовых запросов.

## Классы

### `Prodia`

**Описание**: Класс `Prodia` предоставляет методы для взаимодействия с API сервиса Prodia для генерации изображений.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): Базовый URL сервиса Prodia.
- `api_endpoint` (str): URL API для генерации изображений.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию для генерации изображений.
- `default_image_model` (str): Модель изображения, используемая по умолчанию. Дублирует `default_model`.
- `image_models` (List[str]): Список доступных моделей изображений.
- `models` (List[str]): Список всех доступных моделей, в данном случае совпадает с `image_models`.

**Методы**:
- `get_model(model: str) -> str`: Возвращает имя модели на основе предоставленного alias или имени, при отсуствии возвращает `default_model`.
- `create_async_generator(...) -> AsyncResult`: Асинхронно генерирует изображение на основе заданных параметров.
- `_poll_job(...) -> str`: Опрашивает API до завершения генерации изображения.

## Функции

### `get_model`

```python
    @classmethod
    def get_model(cls, model: str) -> str:
        """ Возвращает имя модели на основе предоставленного alias или имени, при отсуствии возвращает `default_model`.
        Args:
            model (str): Имя модели или alias.

        Returns:
            str: Имя модели.
        """
        ...
```

**Назначение**: Функция `get_model` определяет, какую модель использовать для генерации изображения.

**Параметры**:
- `model` (str): Имя модели, указанное пользователем.

**Возвращает**:
- `str`: Если `model` есть в списке доступных моделей, возвращает `model`. Если `model` есть в списке alias, возвращает соответствующую модель из `model_aliases`. В противном случае возвращает `default_model`.

**Как работает функция**:

1. Проверяет, находится ли запрошенная модель в списке доступных моделей (`cls.models`).
2. Если модель не найдена в списке доступных моделей, проверяет, есть ли она в списке alias моделей (`cls.model_aliases`).
3. Если модель не найдена ни в одном из списков, возвращает модель по умолчанию (`cls.default_model`).

```
A: Проверка наличия model в cls.models
|
B: model присутствует в cls.models?
|  Да: Возврат model
|  Нет: 
|   C: Проверка наличия model в cls.model_aliases
|   |
|   D: model присутствует в cls.model_aliases?
|   |  Да: Возврат cls.model_aliases[model]
|   |  Нет: Возврат cls.default_model
```

**Примеры**:

```python
# Пример 1: Модель найдена в списке доступных моделей
model = Prodia.get_model('absolutereality_v181.safetensors [3d9d4d2b]')
print(model)  # Вывод: absolutereality_v181.safetensors [3d9d4d2b]

# Пример 2: Модель не найдена, возвращается модель по умолчанию
model = Prodia.get_model('non_existent_model')
print(model)  # Вывод: absolutereality_v181.safetensors [3d9d4d2b]
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
        """ Асинхронно генерирует изображение на основе заданных параметров.
        Args:
            model (str): Имя модели для генерации изображения.
            messages (Messages): Список сообщений, содержащих текстовый запрос.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
            negative_prompt (str, optional): Негативный запрос, указывающий, что не должно быть на изображении. По умолчанию "".
            steps (str, optional): Количество шагов для генерации изображения. По умолчанию "20".
            cfg (str, optional): Значение CFG (Classifier-Free Guidance). По умолчанию "7".
            seed (Optional[int], optional): Зерно для генерации случайного изображения. По умолчанию `None`.
            sampler (str, optional): Метод выборки. По умолчанию "DPM++ 2M Karras".
            aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "square".
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий URL сгенерированного изображения.

        Raises:
            Exception: Если возникает ошибка при выполнении запроса или обработке ответа.
        """
        ...
```

**Назначение**: Функция `create_async_generator` отправляет запрос к API Prodia для генерации изображения на основе заданных параметров и возвращает URL этого изображения.

**Параметры**:
- `model` (str): Имя модели для генерации изображения.
- `messages` (Messages): Список сообщений, содержащих текстовый запрос.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `negative_prompt` (str, optional): Негативный запрос, указывающий, что не должно быть на изображении. По умолчанию "".
- `steps` (str, optional): Количество шагов для генерации изображения. По умолчанию "20".
- `cfg` (str, optional): Значение CFG (Classifier-Free Guidance). По умолчанию "7".
- `seed` (Optional[int], optional): Зерно для генерации случайного изображения. По умолчанию `None`.
- `sampler` (str, optional): Метод выборки. По умолчанию "DPM++ 2M Karras".
- `aspect_ratio` (str, optional): Соотношение сторон изображения. По умолчанию "square".
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий URL сгенерированного изображения.

**Как работает функция**:

1. Определяет модель для генерации изображения, используя метод `cls.get_model(model)`.
2. Если `seed` не указан, генерирует случайное значение.
3. Формирует заголовки запроса, включая User-Agent, Referer и Origin.
4. Создает асинхронную сессию с использованием `aiohttp.ClientSession`.
5. Извлекает текстовый запрос из последнего сообщения в списке `messages`.
6. Формирует параметры запроса, включая текстовый запрос, модель, негативный запрос, количество шагов, CFG, зерно, метод выборки и соотношение сторон.
7. Отправляет GET-запрос к API Prodia с заданными параметрами.
8. Извлекает ID задачи (job ID) из ответа API.
9. Запускает асинхронный опрос API для получения URL сгенерированного изображения с помощью метода `cls._poll_job(session, job_id, proxy)`.
10. Возвращает объект `ImageResponse` с URL изображения и альтернативным текстом (текстовым запросом).

```
A: Определение модели (model = cls.get_model(model))
|
B: Проверка seed (seed is None)
|  Да: Генерация случайного seed
|  Нет: Использовать предоставленный seed
|
C: Формирование заголовков запроса (headers)
|
D: Создание асинхронной сессии (ClientSession)
|
E: Извлечение текстового запроса (prompt)
|
F: Формирование параметров запроса (params)
|
G: Отправка GET-запроса к API Prodia
|
H: Извлечение job ID из ответа
|
I: Запуск асинхронного опроса API (cls._poll_job)
|
J: Возврат ImageResponse с URL изображения
```

**Примеры**:

```python
# Пример вызова функции create_async_generator
import asyncio
from typing import List, Tuple, Dict

async def main():
    model = 'absolutereality_v181.safetensors [3d9d4d2b]'
    messages: List[Tuple[str, str]] = [("user", "A beautiful landscape")]
    proxy = None
    negative_prompt = "ugly, disfigured"
    steps = "25"
    cfg = "8"
    seed = 42
    sampler = "Euler a"
    aspect_ratio = "landscape"

    generator = await Prodia.create_async_generator(
        model=model,
        messages=messages,
        proxy=proxy,
        negative_prompt=negative_prompt,
        steps=steps,
        cfg=cfg,
        seed=seed,
        sampler=sampler,
        aspect_ratio=aspect_ratio
    )

    async for image_response in generator:
        print(image_response.url)

if __name__ == "__main__":
    asyncio.run(main())
```

### `_poll_job`

```python
    @classmethod
    async def _poll_job(cls, session: ClientSession, job_id: str, proxy: str, max_attempts: int = 30, delay: int = 2) -> str:
        """ Опрашивает API до завершения генерации изображения.
        Args:
            session (ClientSession): Асинхронная сессия для выполнения запросов.
            job_id (str): ID задачи генерации изображения.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
            max_attempts (int, optional): Максимальное количество попыток опроса. По умолчанию 30.
            delay (int, optional): Задержка в секундах между попытками опроса. По умолчанию 2.

        Returns:
            str: URL сгенерированного изображения.

        Raises:
            Exception: Если превышено максимальное количество попыток опроса или задача завершилась с ошибкой.
        """
        ...
```

**Назначение**: Функция `_poll_job` периодически опрашивает API Prodia, чтобы узнать статус задачи генерации изображения.

**Параметры**:
- `session` (ClientSession): Асинхронная сессия для выполнения запросов.
- `job_id` (str): ID задачи генерации изображения.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `max_attempts` (int, optional): Максимальное количество попыток опроса. По умолчанию 30.
- `delay` (int, optional): Задержка в секундах между попытками опроса. По умолчанию 2.

**Возвращает**:
- `str`: URL сгенерированного изображения.

**Вызывает исключения**:
- `Exception`: Если превышено максимальное количество попыток опроса или задача завершилась с ошибкой.

**Как работает функция**:

1. Выполняет цикл опроса API до тех пор, пока не будет достигнуто максимальное количество попыток (`max_attempts`).
2. Отправляет GET-запрос к API Prodia для получения статуса задачи.
3. Проверяет статус задачи:
   - Если статус "succeeded", возвращает URL сгенерированного изображения.
   - Если статус "failed", вызывает исключение `Exception` с сообщением об ошибке.
4. Если статус не "succeeded" и не "failed", ожидает заданное время (`delay`) и повторяет попытку.
5. Если после максимального количества попыток статус не "succeeded", вызывает исключение `Exception` с сообщением о таймауте.

```
A: Запуск цикла опроса (max_attempts)
|
B: Отправка GET-запроса к API Prodia для получения статуса задачи
|
C: Проверка статуса задачи (job_status["status"])
|  "succeeded": Возврат URL изображения
|  "failed": Вызов исключения Exception("Image generation failed")
|  Другой статус: Ожидание (asyncio.sleep(delay)) и повтор цикла
|
D: Если max_attempts достигнуто: Вызов исключения Exception("Timeout waiting for image generation")
```

**Примеры**:

```python
# Пример вызова функции _poll_job
import asyncio
from aiohttp import ClientSession

async def main():
    async with ClientSession() as session:
        job_id = "some_job_id"
        proxy = None

        try:
            image_url = await Prodia._poll_job(session, job_id, proxy)
            print(f"Image URL: {image_url}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())