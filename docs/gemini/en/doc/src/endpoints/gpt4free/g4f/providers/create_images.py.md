# Модуль создания изображений

## Обзор

Этот модуль предоставляет класс `CreateImagesProvider`, который используется для создания изображений на основе текстовых запросов.
Он обрабатывает запросы на создание изображений, встроенные в содержимое сообщения, используя предоставленные функции создания изображений.

## Подробнее

Этот модуль позволяет интегрировать создание изображений в процесс обработки текстовых сообщений.
Он использует регулярные выражения для обнаружения тегов `<img data-prompt="...">` в сообщениях и вызывает соответствующие функции для создания изображений на основе содержимого атрибута `data-prompt`.

## Классы

### `CreateImagesProvider`

**Описание**: Класс-провайдер для создания изображений на основе текстовых запросов.

**Наследует**:
- `BaseProvider`: Базовый класс для провайдеров.

**Атрибуты**:
- `provider` (`ProviderType`): Базовый провайдер для обработки задач, не связанных с изображениями.
- `create_images` (`callable`): Функция для синхронного создания изображений.
- `create_images_async` (`callable`): Функция для асинхронного создания изображений.
- `system_message` (`str`): Системное сообщение, объясняющее возможность создания изображений.
- `include_placeholder` (`bool`): Флаг, определяющий, следует ли включать заполнитель изображения в выходные данные.
- `__name__` (`str`): Имя провайдера.
- `url` (`str`): URL-адрес провайдера.
- `working` (`bool`): Указывает, работает ли провайдер.
- `supports_stream` (`bool`): Указывает, поддерживает ли провайдер потоковую передачу.

**Принцип работы**:

Класс `CreateImagesProvider` предназначен для расширения функциональности базового провайдера путем добавления возможности создания изображений на основе текстовых запросов. Он принимает базовый провайдер и две функции: одну для синхронного создания изображений и другую для асинхронного. При обработке сообщений он ищет специальные теги `<img data-prompt="...">`, извлекает запрос из атрибута `data-prompt` и использует предоставленные функции для создания изображений.

Он работает следующим образом:
   1. **Инициализация**: При создании экземпляра класса `CreateImagesProvider` передаются базовый провайдер, функции для создания изображений (синхронная и асинхронная), системное сообщение и флаг `include_placeholder`.
   2. **Обработка сообщений**: Методы `create_completion` (синхронный) и `create_async` (асинхронный) принимают сообщения, ищут в них теги `<img data-prompt="...">`, извлекают запросы и используют соответствующие функции для создания изображений.
   3. **Создание изображений**: Когда запрос на создание изображения обнаружен, вызывается соответствующая функция (синхронная или асинхронная) для создания изображения.
   4. **Формирование ответа**: Ответ формируется путем замены тега `<img data-prompt="...">` на результат создания изображения. Флаг `include_placeholder` определяет, следует ли включать исходный тег в выходные данные.

```python
class CreateImagesProvider(BaseProvider):
    """
    Провайдер для создания изображений на основе текстовых запросов.

    Наследует:
        BaseProvider: Базовый класс для провайдеров.

    Атрибуты:
        provider (ProviderType): Базовый провайдер для обработки задач, не связанных с изображениями.
        create_images (callable): Функция для синхронного создания изображений.
        create_images_async (callable): Функция для асинхронного создания изображений.
        system_message (str): Системное сообщение, объясняющее возможность создания изображений.
        include_placeholder (bool): Флаг, определяющий, следует ли включать заполнитель изображения в выходные данные.
        __name__ (str): Имя провайдера.
        url (str): URL-адрес провайдера.
        working (bool): Указывает, работает ли провайдер.
        supports_stream (bool): Указывает, поддерживает ли провайдер потоковую передачу.
    """

    def __init__(
        self,
        provider: ProviderType,
        create_images: callable,
        create_async: callable,
        system_message: str = system_message,
        include_placeholder: bool = True
    ) -> None:
        """
        Инициализирует CreateImagesProvider.

        Args:
            provider (ProviderType): Базовый провайдер.
            create_images (callable): Функция для синхронного создания изображений.
            create_async (callable): Функция для асинхронного создания изображений.
            system_message (str, optional): Системное сообщение, добавляемое к сообщениям. По умолчанию используется предопределенное сообщение.
            include_placeholder (bool, optional): Определяет, включать ли заполнители изображений в вывод. По умолчанию True.
        """
        self.provider = provider
        self.create_images = create_images
        self.create_images_async = create_async
        self.system_message = system_message
        self.include_placeholder = include_placeholder
        self.__name__ = provider.__name__
        self.url = provider.url
        self.working = provider.working
        self.supports_stream = provider.supports_stream

    def create_completion(
        self,
        model: str,
        messages: Messages,
        stream: bool = False,
        **kwargs
    ) -> CreateResult:
        """
        Создает результат завершения, обрабатывая все запросы на создание изображений, найденные в сообщениях.

        Args:
            model (str): Модель для использования при создании.
            messages (Messages): Сообщения для обработки, которые могут содержать запросы изображений.
            stream (bool, optional): Указывает, следует ли передавать результаты в потоковом режиме. По умолчанию False.
            **kwargs: Дополнительные аргументы ключевого слова для провайдера.

        Yields:
            CreateResult: Выдает фрагменты обработанных сообщений, включая данные изображения, если применимо.

        Примечание:
            Этот метод обрабатывает сообщения для обнаружения запросов на создание изображений. Когда такой запрос найден,
            он вызывает синхронную функцию создания изображений и включает полученное изображение в выходные данные.
        """
        messages.insert(0, {"role": "system", "content": self.system_message})
        buffer = ""
        for chunk in self.provider.create_completion(model, messages, stream, **kwargs):
            if isinstance(chunk, ImageResponse):
                yield chunk
            elif isinstance(chunk, str) and buffer or "<" in chunk:
                buffer += chunk
                if ">" in buffer:
                    match = re.search(r'<img data-prompt="(.*?)">', buffer)
                    if match:
                        placeholder, prompt = match.group(0), match.group(1)
                        start, append = buffer.split(placeholder, 1)
                        if start:
                            yield start
                        if self.include_placeholder:
                            yield placeholder
                        if debug.logging:
                            print(f"Create images with prompt: {prompt}")
                        yield from self.create_images(prompt)
                        if append:
                            yield append
                    else:
                        yield buffer
                    buffer = ""
            else:
                yield chunk

    async def create_async(
        self,
        model: str,
        messages: Messages,
        **kwargs
    ) -> str:
        """
        Асинхронно создает ответ, обрабатывая все запросы на создание изображений, найденные в сообщениях.

        Args:
            model (str): Модель для использования при создании.
            messages (Messages): Сообщения для обработки, которые могут содержать запросы изображений.
            **kwargs: Дополнительные аргументы ключевого слова для провайдера.

        Returns:
            str: Обработанная строка ответа, включая асинхронно сгенерированные данные изображения, если применимо.

        Примечание:
            Этот метод обрабатывает сообщения для обнаружения запросов на создание изображений. Когда такой запрос найден,
            он вызывает асинхронную функцию создания изображений и включает полученное изображение в выходные данные.
        """
        messages.insert(0, {"role": "system", "content": self.system_message})
        response = await self.provider.create_async(model, messages, **kwargs)
        matches = re.findall(r'(<img data-prompt="(.*?)">)', response)
        results = []
        placeholders = []
        for placeholder, prompt in matches:
            if placeholder not in placeholders:
                if debug.logging:
                    print(f"Create images with prompt: {prompt}")
                results.append(self.create_images_async(prompt))
                placeholders.append(placeholder)
        results = await asyncio.gather(*results)
        for idx, result in enumerate(results):
            placeholder = placeholders[idx]
            if self.include_placeholder:
                result = placeholder + result
            response = response.replace(placeholder, result)
        return response
```

## Методы класса

### `__init__`

```python
def __init__(
    self,
    provider: ProviderType,
    create_images: callable,
    create_async: callable,
    system_message: str = system_message,
    include_placeholder: bool = True
) -> None:
    """
    Инициализирует CreateImagesProvider.

    Args:
        provider (ProviderType): Базовый провайдер.
        create_images (callable): Функция для синхронного создания изображений.
        create_async (callable): Функция для асинхронного создания изображений.
        system_message (str, optional): Системное сообщение, добавляемое к сообщениям. По умолчанию используется предопределенное сообщение.
        include_placeholder (bool, optional): Определяет, включать ли заполнители изображений в вывод. По умолчанию True.
    """
```

**Назначение**:
Инициализирует экземпляр класса `CreateImagesProvider`.

**Параметры**:
- `provider` (`ProviderType`): Базовый провайдер, который будет использоваться для выполнения основных задач.
- `create_images` (`callable`): Функция, используемая для синхронного создания изображений.
- `create_async` (`callable`): Функция, используемая для асинхронного создания изображений.
- `system_message` (`str`, optional): Системное сообщение, которое будет добавлено к сообщениям для указания возможности создания изображений. По умолчанию используется значение `system_message`.
- `include_placeholder` (`bool`, optional): Определяет, следует ли включать заполнитель изображения в выходные данные. По умолчанию `True`.

**Примеры**:
```python
# Пример инициализации CreateImagesProvider
from ..providers import OpenAi
from asyncio import run

async def create_image(prompt: str) -> str:
    # Здесь должна быть логика создания изображения на основе запроса prompt
    return f"Image created with prompt: {prompt}"

async def main():
    provider = CreateImagesProvider(
        provider=OpenAi.AsyncProvider(),
        create_images=lambda prompt: create_image(prompt),
        create_async=create_image
    )
    print(provider)

if __name__ == "__main__":
    run(main())
```

### `create_completion`

```python
def create_completion(
    self,
    model: str,
    messages: Messages,
    stream: bool = False,
    **kwargs
) -> CreateResult:
    """
    Создает результат завершения, обрабатывая все запросы на создание изображений, найденные в сообщениях.

    Args:
        model (str): Модель для использования при создании.
        messages (Messages): Сообщения для обработки, которые могут содержать запросы изображений.
        stream (bool, optional): Указывает, следует ли передавать результаты в потоковом режиме. По умолчанию False.
        **kwargs: Дополнительные аргументы ключевого слова для провайдера.

    Yields:
        CreateResult: Выдает фрагменты обработанных сообщений, включая данные изображения, если применимо.

    Примечание:
        Этот метод обрабатывает сообщения для обнаружения запросов на создание изображений. Когда такой запрос найден,
        он вызывает синхронную функцию создания изображений и включает полученное изображение в выходные данные.
    """
```

**Назначение**:
Создает результат завершения, обрабатывая все запросы на создание изображений, найденные в сообщениях.

**Параметры**:
- `model` (`str`): Модель для использования при создании.
- `messages` (`Messages`): Сообщения для обработки, которые могут содержать запросы изображений.
- `stream` (`bool`, optional): Указывает, следует ли передавать результаты в потоковом режиме. По умолчанию `False`.
- `**kwargs`: Дополнительные именованные аргументы для провайдера.

**Как работает функция**:
1. Вставляет системное сообщение в начало списка сообщений, чтобы указать возможность создания изображений.
2. Итерируется по фрагментам, возвращаемым базовым провайдером.
3. Если фрагмент является экземпляром `ImageResponse`, он немедленно возвращается.
4. Если фрагмент является строкой и содержит тег `<img data-prompt="...">`, он извлекает запрос и заменяет тег результатом создания изображения.
5. Если фрагмент не содержит тег, он возвращается без изменений.

**Пример**:
```python
# Пример вызова create_completion
from ..providers import OpenAi
from asyncio import run

async def create_image(prompt: str) -> str:
    # Здесь должна быть логика создания изображения на основе запроса prompt
    return f"Image created with prompt: {prompt}"

async def main():
    provider = CreateImagesProvider(
        provider=OpenAi.AsyncProvider(),
        create_images=lambda prompt: create_image(prompt),
        create_async=create_image
    )
    
    messages = [{"role": "user", "content": "Создай изображение: <img data-prompt='запрос изображения'>. И еще немного текста."}]
    
    async for chunk in provider.create_completion(model="default", messages=messages):
        print(chunk)

if __name__ == "__main__":
    run(main())
```

### `create_async`

```python
async def create_async(
    self,
    model: str,
    messages: Messages,
    **kwargs
) -> str:
    """
    Асинхронно создает ответ, обрабатывая все запросы на создание изображений, найденные в сообщениях.

    Args:
        model (str): Модель для использования при создании.
        messages (Messages): Сообщения для обработки, которые могут содержать запросы изображений.
        **kwargs: Дополнительные аргументы ключевого слова для провайдера.

    Returns:
        str: Обработанная строка ответа, включая асинхронно сгенерированные данные изображения, если применимо.

    Примечание:
        Этот метод обрабатывает сообщения для обнаружения запросов на создание изображений. Когда такой запрос найден,
        он вызывает асинхронную функцию создания изображений и включает полученное изображение в выходные данные.
    """
```

**Назначение**:
Асинхронно создает ответ, обрабатывая все запросы на создание изображений, найденные в сообщениях.

**Параметры**:
- `model` (`str`): Модель для использования при создании.
- `messages` (`Messages`): Сообщения для обработки, которые могут содержать запросы изображений.
- `**kwargs`: Дополнительные именованные аргументы для провайдера.

**Как работает функция**:
1. Вставляет системное сообщение в начало списка сообщений, чтобы указать возможность создания изображений.
2. Использует базовый провайдер для асинхронного создания ответа.
3. Находит все теги `<img data-prompt="...">` в ответе.
4. Для каждого найденного тега извлекает запрос и асинхронно создает изображение.
5. Заменяет теги результатами создания изображений.
6. Возвращает обработанный ответ.

**Пример**:
```python
# Пример вызова create_async
from ..providers import OpenAi
from asyncio import run

async def create_image(prompt: str) -> str:
    # Здесь должна быть логика создания изображения на основе запроса prompt
    return f"Image created with prompt: {prompt}"

async def main():
    provider = CreateImagesProvider(
        provider=OpenAi.AsyncProvider(),
        create_images=lambda prompt: create_image,
        create_async=create_image
    )
    
    messages = [{"role": "user", "content": "Создай изображение: <img data-prompt='запрос изображения'>. И еще немного текста."}]
    
    result = await provider.create_async(model="default", messages=messages)
    print(result)

if __name__ == "__main__":
    run(main())
```