# Модуль `DeepInfra` - провайдер API для DeepInfra.com

## Обзор

Модуль предоставляет реализацию класса `DeepInfra`, который используется для взаимодействия с API DeepInfra.com. DeepInfra.com - платформа для доступа к различным моделям искусственного интеллекта, включая модели обработки текста, генерации изображений и другие.

Класс `DeepInfra` наследует от `OpenaiTemplate` и предоставляет методы для отправки запросов к API, обработки ответов и взаимодействия с моделями DeepInfra.com.

##  Подробнее

Модуль предназначен для использования в качестве провайдера API для DeepInfra.com в рамках проекта `hypotez`. Он позволяет использовать различные модели DeepInfra.com для выполнения задач обработки текста, генерации изображений и других задач, связанных с искусственным интеллектом.

## Классы

### `class DeepInfra(OpenaiTemplate)`

**Описание**: Класс `DeepInfra`  представляет собой провайдер API для DeepInfra.com.

**Наследует**: `OpenaiTemplate`

**Атрибуты**:
- `url`: Основной URL DeepInfra.com
- `login_url`: URL для входа в личный кабинет на DeepInfra.com
- `api_base`: Основной URL API DeepInfra.com
- `working`: Флаг, указывающий, что провайдер API в рабочем состоянии
- `needs_auth`: Флаг, указывающий, что для использования API требуется авторизация
- `default_model`: Имя модели по умолчанию для текстовых задач
- `default_image_model`: Имя модели по умолчанию для задач генерации изображений
- `models`: Список доступных моделей для текстовых задач
- `image_models`: Список доступных моделей для генерации изображений

**Методы**:
- `get_models()`: Получение списка доступных моделей
- `get_image_models()`: Получение списка моделей для генерации изображений
- `create_async_generator()`: Создание асинхронного генератора для работы с моделью
- `create_async_image()`: Создание асинхронного генератора для работы с моделью генерации изображений

#### `get_models()`: Получение списка доступных моделей

**Назначение**: Получение списка доступных моделей для текстовых задач и генерации изображений.

**Параметры**:
- `**kwargs`: Дополнительные аргументы для получения списка моделей

**Возвращает**:
- `list`: Список доступных моделей

**Пример**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepInfra import DeepInfra

models = DeepInfra.get_models()
print(models)
```

#### `get_image_models()`: Получение списка моделей для генерации изображений

**Назначение**: Получение списка доступных моделей для генерации изображений.

**Параметры**:
- `**kwargs`: Дополнительные аргументы для получения списка моделей

**Возвращает**:
- `list`: Список доступных моделей для генерации изображений

**Пример**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepInfra import DeepInfra

image_models = DeepInfra.get_image_models()
print(image_models)
```

#### `create_async_generator()`: Создание асинхронного генератора для работы с моделью

**Назначение**: Создание асинхронного генератора для работы с моделью DeepInfra.com.

**Параметры**:
- `model`: Имя модели DeepInfra.com.
- `messages`: Список сообщений для модели.
- `stream`: Флаг, указывающий, требуется ли потоковая передача данных.
- `prompt`: Текстовый запрос для модели.
- `temperature`: Температура модели, влияет на креативность ответа.
- `max_tokens`: Максимальное количество токенов в ответе.
- `**kwargs`: Дополнительные аргументы для работы с моделью.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который возвращает результаты работы модели.

**Пример**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepInfra import DeepInfra

async def main():
    messages = [
        {"role": "user", "content": "Привет, как дела?"},
    ]
    async for chunk in DeepInfra.create_async_generator(model="meta-llama/Meta-Llama-3.1-70B-Instruct", messages=messages, stream=True):
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

#### `create_async_image()`: Создание асинхронного генератора для работы с моделью генерации изображений

**Назначение**: Создание асинхронного генератора для работы с моделью генерации изображений DeepInfra.com.

**Параметры**:
- `prompt`: Текстовый запрос для модели.
- `model`: Имя модели DeepInfra.com для генерации изображений.
- `api_key`: Ключ API для DeepInfra.com.
- `api_base`: Основной URL API DeepInfra.com.
- `proxy`: URL для прокси-сервера.
- `timeout`: Время ожидания ответа от API DeepInfra.com.
- `extra_data`: Дополнительные данные для модели.
- `**kwargs`: Дополнительные аргументы для работы с моделью.

**Возвращает**:
- `ImageResponse`: Объект, содержащий результат работы модели генерации изображений.

**Пример**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepInfra import DeepInfra

async def main():
    prompt = "Фотография кошки на диване"
    response = await DeepInfra.create_async_image(prompt=prompt, model="stabilityai/sd3.5")
    print(response.images)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Параметры класса
- `url`: Основной URL DeepInfra.com.
- `login_url`: URL для входа в личный кабинет на DeepInfra.com.
- `api_base`: Основной URL API DeepInfra.com.
- `working`: Флаг, указывающий, что провайдер API в рабочем состоянии.
- `needs_auth`: Флаг, указывающий, что для использования API требуется авторизация.
- `default_model`: Имя модели по умолчанию для текстовых задач.
- `default_image_model`: Имя модели по умолчанию для задач генерации изображений.
- `models`: Список доступных моделей для текстовых задач.
- `image_models`: Список доступных моделей для генерации изображений.

## Примеры
```python
# Пример использования класса DeepInfra для работы с моделью генерации изображений
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepInfra import DeepInfra

async def main():
    prompt = "Фотография кошки на диване"
    response = await DeepInfra.create_async_image(prompt=prompt, model="stabilityai/sd3.5")
    print(response.images)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

```python
# Пример использования класса DeepInfra для работы с моделью для текстовых задач
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepInfra import DeepInfra

async def main():
    messages = [
        {"role": "user", "content": "Привет, как дела?"},
    ]
    async for chunk in DeepInfra.create_async_generator(model="meta-llama/Meta-Llama-3.1-70B-Instruct", messages=messages, stream=True):
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

```python
# Пример использования класса DeepInfra для получения списка доступных моделей
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepInfra import DeepInfra

models = DeepInfra.get_models()
print(models)