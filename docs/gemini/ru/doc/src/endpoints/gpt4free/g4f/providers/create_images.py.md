# Модуль для создания изображений

## Обзор

Модуль `create_images.py` предназначен для обработки запросов на создание изображений на основе текстовых подсказок. Он использует другие провайдеры для выполнения задач, не связанных с созданием изображений, и предоставляет функциональность для синхронного и асинхронного создания изображений. Модуль позволяет встраивать запросы на создание изображений непосредственно в текстовые сообщения, используя специальный тег `<img data-prompt="keywords for the image">`.

## Подробнее

Этот модуль является частью системы, позволяющей генерировать изображения на основе текстовых запросов. Он обрабатывает сообщения, содержащие специальные теги с подсказками для генерации изображений, и использует предоставленные функции для создания изображений. Полученные изображения встраиваются в ответ.

## Классы

### `CreateImagesProvider`

**Описание**: Класс провайдера для создания изображений на основе текстовых подсказок.

**Наследует**: `BaseProvider`

**Атрибуты**:

-   `provider` (ProviderType): Базовый провайдер для обработки задач, не связанных с изображениями.
-   `create_images` (callable): Функция для синхронного создания изображений.
-   `create_images_async` (callable): Функция для асинхронного создания изображений.
-   `system_message` (str): Сообщение, объясняющее возможность создания изображений.
-   `include_placeholder` (bool): Флаг, определяющий, нужно ли включать заполнитель изображения в вывод.
-   `__name__` (str): Имя провайдера.
-   `url` (str): URL провайдера.
-   `working` (bool): Указывает, работает ли провайдер.
-   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу.

**Методы**:

-   `__init__`: Инициализирует экземпляр класса `CreateImagesProvider`.
-   `create_completion`: Создает результат завершения, обрабатывая подсказки для создания изображений в сообщениях.
-   `create_async`: Асинхронно создает ответ, обрабатывая подсказки для создания изображений в сообщениях.

#### `__init__`

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
        system_message (str, optional): Системное сообщение, добавляемое к сообщениям. По умолчанию предопределенное сообщение.
        include_placeholder (bool, optional): Нужно ли включать заполнители изображений в вывод. По умолчанию True.

    """
```

**Назначение**: Инициализирует класс `CreateImagesProvider`, устанавливая необходимые атрибуты, такие как базовый провайдер, функции для создания изображений (синхронную и асинхронную), системное сообщение и флаг включения заполнителей.

**Параметры**:

-   `provider` (ProviderType): Базовый провайдер, используемый для обработки задач, не связанных с созданием изображений.
-   `create_images` (callable): Функция, вызываемая для синхронного создания изображений на основе текстовой подсказки.
-   `create_async` (callable): Функция, вызываемая для асинхронного создания изображений на основе текстовой подсказки.
-   `system_message` (str, optional): Сообщение, которое добавляется в начало каждого запроса, чтобы объяснить модели, как генерировать изображения. По умолчанию используется значение `system_message`, определенное в модуле.
-   `include_placeholder` (bool, optional): Флаг, указывающий, следует ли включать заполнитель (placeholder) для изображений в возвращаемый результат. По умолчанию установлено значение `True`.

**Как работает функция**:

Функция инициализирует атрибуты класса `CreateImagesProvider` с переданными значениями. Это позволяет настроить провайдер с различными функциями создания изображений, системными сообщениями и параметрами включения заполнителей.

**Примеры**:

```python
# Пример инициализации CreateImagesProvider с фиктивными функциями и провайдером
class MockProvider:
    __name__ = "MockProvider"
    url = "http://example.com"
    working = True
    supports_stream = False

    def create_completion(self, model, messages, stream, **kwargs):
        yield "Test"

    async def create_async(self, model, messages, **kwargs):
        return "Test"

def mock_create_images(prompt):
    yield f"Image: {prompt}"

async def mock_create_async(prompt):
    return f"Async Image: {prompt}"

provider = MockProvider()
image_provider = CreateImagesProvider(
    provider=provider,
    create_images=mock_create_images,
    create_async=mock_create_async
)

print(image_provider.provider.__name__)  # Вывод: MockProvider
print(image_provider.url)  # Вывод: http://example.com
```

#### `create_completion`

```python
def create_completion(
    self,
    model: str,
    messages: Messages,
    stream: bool = False,
    **kwargs
) -> CreateResult:
    """
    Создает результат завершения, обрабатывая любые подсказки для создания изображений, найденные в сообщениях.

    Args:
        model (str): Модель для использования при создании.
        messages (Messages): Сообщения для обработки, которые могут содержать подсказки для создания изображений.
        stream (bool, optional): Указывает, следует ли передавать результаты потоком. По умолчанию False.
        **kwargs: Дополнительные именованные аргументы для провайдера.

    Yields:
        CreateResult: Выдает фрагменты обработанных сообщений, включая данные изображения, если применимо.

    Note:
        Этот метод обрабатывает сообщения для обнаружения подсказок для создания изображений. Когда такая подсказка найдена,
        он вызывает функцию синхронного создания изображений и включает полученное изображение в вывод.
    """
```

**Назначение**: Создает результат завершения, обрабатывая сообщения для обнаружения подсказок создания изображений и встраивая результаты в выходной поток.

**Параметры**:

-   `model` (str): Имя модели, используемой для генерации завершения.
-   `messages` (Messages): Список сообщений, которые необходимо обработать. Эти сообщения могут содержать текстовые подсказки для генерации изображений.
-   `stream` (bool, optional): Флаг, указывающий, следует ли возвращать результаты в виде потока. По умолчанию установлено значение `False`.
-   `**kwargs`: Дополнительные аргументы, которые передаются базовому провайдеру.

**Как работает функция**:

1.  Вставляет системное сообщение в начало списка сообщений, чтобы указать модели, как обрабатывать запросы на создание изображений.
2.  Итерируется по фрагментам, генерируемым базовым провайдером (`self.provider`).
3.  Если фрагмент является экземпляром `ImageResponse`, он немедленно выдается.
4.  Если фрагмент является строкой и содержит тег `<img data-prompt="...">`, функция пытается извлечь подсказку для создания изображения.
5.  Вызывает функцию `self.create_images` для генерации изображения на основе извлеченной подсказки.
6.  Вставляет сгенерированное изображение в поток вывода.

**Примеры**:

```python
# Пример использования create_completion с фиктивными функциями и провайдером
class MockProvider:
    __name__ = "MockProvider"
    url = "http://example.com"
    working = True
    supports_stream = False

    def create_completion(self, model, messages, stream, **kwargs):
        text = messages[0]['content']
        if "<img data-prompt=" in text:
            yield '<img data-prompt="test_prompt">'
        else:
            yield "Test"

    async def create_async(self, model, messages, **kwargs):
        return "Test"

def mock_create_images(prompt):
    yield f"Image: {prompt}"

async def mock_create_async(prompt):
    return f"Async Image: {prompt}"

provider = MockProvider()
image_provider = CreateImagesProvider(
    provider=provider,
    create_images=mock_create_images,
    create_async=mock_create_async
)

messages = [{"role": "user", "content": "<img data-prompt='test_prompt'>"}]
result = image_provider.create_completion("test_model", messages)
for item in result:
    print(item)
# Ожидаемый вывод:
# Image: test_prompt
```

#### `create_async`

```python
async def create_async(
    self,
    model: str,
    messages: Messages,
    **kwargs
) -> str:
    """
    Асинхронно создает ответ, обрабатывая любые подсказки для создания изображений, найденные в сообщениях.

    Args:
        model (str): Модель для использования при создании.
        messages (Messages): Сообщения для обработки, которые могут содержать подсказки для создания изображений.
        **kwargs: Дополнительные именованные аргументы для провайдера.

    Returns:
        str: Обработанная строка ответа, включая асинхронно сгенерированные данные изображения, если применимо.

    Note:
        Этот метод обрабатывает сообщения для обнаружения подсказок для создания изображений. Когда такая подсказка найдена,
        он вызывает функцию асинхронного создания изображений и включает полученное изображение в вывод.
    """
```

**Назначение**: Асинхронно создает ответ, обрабатывая сообщения для обнаружения подсказок создания изображений и встраивая результаты в строку ответа.

**Параметры**:

-   `model` (str): Имя модели, используемой для генерации ответа.
-   `messages` (Messages): Список сообщений, содержащих текст и, возможно, теги с подсказками для генерации изображений.
-   `**kwargs`: Дополнительные аргументы, передаваемые базовому провайдеру.

**Как работает функция**:

1.  Вставляет системное сообщение в начало списка сообщений, чтобы указать модели, как обрабатывать запросы на создание изображений.
2.  Вызывает асинхронную функцию `self.provider.create_async` для получения ответа от базового провайдера.
3.  Ищет в ответе теги `<img data-prompt="...">`, чтобы извлечь подсказки для создания изображений.
4.  Вызывает асинхронную функцию `self.create_images_async` для каждого найденного тега, чтобы сгенерировать изображение на основе подсказки.
5.  Заменяет теги в ответе сгенерированными изображениями.

**Примеры**:

```python
# Пример использования create_async с фиктивными функциями и провайдером
class MockProvider:
    __name__ = "MockProvider"
    url = "http://example.com"
    working = True
    supports_stream = False

    def create_completion(self, model, messages, stream, **kwargs):
        yield "Test"

    async def create_async(self, model, messages, **kwargs):
        text = messages[0]['content']
        if "<img data-prompt=" in text:
            return '<img data-prompt="test_prompt">'
        else:
            return "Test"

def mock_create_images(prompt):
    yield f"Image: {prompt}"

async def mock_create_async(prompt):
    return f"Async Image: {prompt}"

provider = MockProvider()
image_provider = CreateImagesProvider(
    provider=provider,
    create_images=mock_create_images,
    create_async=mock_create_async
)

async def main():
    messages = [{"role": "user", "content": "<img data-prompt='test_prompt'>"}]
    result = await image_provider.create_async("test_model", messages)
    print(result)

# Запуск примера (в асинхронном контексте):
# asyncio.run(main())
# Ожидаемый вывод:
# Async Image: test_prompt