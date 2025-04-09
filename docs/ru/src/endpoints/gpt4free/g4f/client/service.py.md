# Модуль service

## Обзор

Модуль `service` содержит функции для получения и преобразования поставщиков и моделей, используемых в проекте `hypotez`. Он также предоставляет инструменты для отладки и проверки версий.

## Подробней

Этот модуль обеспечивает централизованный доступ к различным провайдерам и моделям, гарантируя, что они правильно настроены и совместимы. Функции в этом модуле обрабатывают преобразование строк в объекты провайдеров и моделей, проверяют их работоспособность и поддерживают ли они потоковую передачу. Модуль также содержит функциональность для логирования и отладки, что помогает отслеживать используемые провайдеры и модели.

## Функции

### `convert_to_provider`

```python
def convert_to_provider(provider: str) -> ProviderType:
    """
    Преобразует строку с именем провайдера в объект провайдера.

    Args:
        provider (str): Строка с именем провайдера. Может содержать несколько провайдеров, разделенных пробелами.

    Returns:
        ProviderType: Объект провайдера.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.

    Как работает функция:
    1. Проверяет, содержит ли строка `provider` пробелы. Если да, то разделяет строку на список провайдеров.
    2. Преобразует каждый элемент списка в соответствующий объект провайдера, используя `ProviderUtils.convert`.
    3. Если ни один из провайдеров не найден, вызывает исключение `ProviderNotFoundError`.
    4. Если в строке `provider` нет пробелов, пытается преобразовать её напрямую в объект провайдера, используя `ProviderUtils.convert`.
    5. Если провайдер не найден, вызывает исключение `ProviderNotFoundError`.

    ASCII flowchart:
    ProviderString --> HasSpaces?
    HasSpaces? -- Yes --> SplitString --> ConvertProviders --> AnyProvidersFound?
    AnyProvidersFound? -- No --> RaiseError
    HasSpaces? -- No --> ConvertProvider --> ProviderFound?
    ProviderFound? -- No --> RaiseError
    """
    ...
```

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.client.service import convert_to_provider
from src.endpoints.gpt4free.g4f.providers import RetryProvider

try:
    provider = convert_to_provider('FakeProvider')
    print(provider)
except Exception as ex:
    print(f"Error: {ex}")

try:
    provider = convert_to_provider('BingAI')
    print(provider)
except Exception as ex:
    print(f"Error: {ex}")

try:
    provider = convert_to_provider('BingAI Ails')
    print(provider)
except Exception as ex:
    print(f"Error: {ex}")
```

### `get_model_and_provider`

```python
def get_model_and_provider(model: Union[Model, str],
                           provider: Union[ProviderType, str, None],
                           stream: bool,
                           ignore_working: bool = False,
                           ignore_stream: bool = False,
                           logging: bool = True,
                           has_images: bool = False) -> tuple[str, ProviderType]:
    """
    Извлекает модель и провайдера на основе входных параметров.

    Args:
        model (Union[Model, str]): Модель для использования, либо объект, либо строковый идентификатор.
        provider (Union[ProviderType, str, None]): Провайдер для использования, либо объект, либо строковый идентификатор, либо None.
        stream (bool): Указывает, следует ли выполнять операцию в потоковом режиме.
        ignore_working (bool, optional): Если True, игнорирует рабочее состояние провайдера. По умолчанию False.
        ignore_stream (bool, optional): Если True, игнорирует возможность потоковой передачи провайдера. По умолчанию False.

    Returns:
        tuple[str, ProviderType]: Кортеж, содержащий имя модели и тип провайдера.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.
        ModelNotFoundError: Если модель не найдена.
        ProviderNotWorkingError: Если провайдер не работает.
        StreamNotSupportedError: Если потоковая передача не поддерживается провайдером.

    Как работает функция:
    1. Выполняет проверку версии, если `debug.version_check` имеет значение True.
    2. Преобразует строковое представление провайдера в объект провайдера, используя `convert_to_provider`, если `provider` является строкой.
    3. Преобразует строковое представление модели в объект модели, используя `ModelUtils.convert`, если `model` является строкой.
    4. Если `provider` не указан:
       - Если `model` также не указана, выбирает модель и провайдера по умолчанию, учитывая наличие изображений (`has_images`).
       - Если `model` является строкой, пытается найти провайдера по имени модели, используя `ProviderUtils.convert`. Если провайдер найден, устанавливает модель по умолчанию для этого провайдера.
       - Если `model` является объектом `Model`, выбирает лучшего провайдера для этой модели.
    5. Если провайдер не найден, вызывает исключение `ProviderNotFoundError`.
    6. Проверяет, работает ли провайдер, если `ignore_working` имеет значение False. Если провайдер не работает, вызывает исключение `ProviderNotWorkingError`.
    7. Если провайдер является `BaseRetryProvider`, фильтрует список провайдеров, оставляя только работающие, если `ignore_working` имеет значение False.
    8. Проверяет, поддерживает ли провайдер потоковую передачу, если `stream` имеет значение True и `ignore_stream` имеет значение False. Если потоковая передача не поддерживается, вызывает исключение `StreamNotSupportedError`.
    9. Логирует используемого провайдера и модель, если `logging` имеет значение True.

    ASCII flowchart:
    Start --> VersionCheck?
    VersionCheck? -- Yes --> CheckVersion
    Start --> ConvertProviderIfString
    ConvertProviderIfString --> ConvertModelIfString
    ConvertModelIfString --> ProviderSpecified?
    ProviderSpecified? -- No --> ModelSpecified?
    ModelSpecified? -- No --> HasImages?
    HasImages? -- Yes --> SetDefaultVisionModelAndProvider
    HasImages? -- No --> SetDefaultModelAndProvider
    ModelSpecified? -- Yes --> ModelIsString?
    ModelIsString? -- Yes --> FindProviderByModelName --> SetDefaultModelForProvider
    ModelIsString? -- No --> ModelIsObjectModel?
    ModelIsObjectModel? -- Yes --> SetBestProviderForModel
    ModelIsObjectModel? -- No --> RaiseValueError
    ProviderSpecified? -- Yes --> CheckProviderWorking?
    CheckProviderWorking? -- No --> RaiseProviderNotWorkingError
    CheckProviderWorking? -- Yes --> ProviderIsRetryProvider?
    ProviderIsRetryProvider? -- Yes --> FilterWorkingProviders
    ProviderIsRetryProvider? -- No --> CheckStreamSupport?
    CheckStreamSupport? -- No --> RaiseStreamNotSupportedError
    CheckStreamSupport? -- Yes --> LogProviderAndModel
    """
    ...
```

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.client.service import get_model_and_provider
from src.endpoints.gpt4free.g4f.models import Model
from src.endpoints.gpt4free.g4f.providers import RetryProvider

try:
    model, provider = get_model_and_provider(model="gpt-3.5-turbo", provider="BingAI", stream=False)
    print(f"Model: {model}, Provider: {provider}")
except Exception as ex:
    print(f"Error: {ex}")

try:
    model, provider = get_model_and_provider(model=Model.gpt_4, provider=RetryProvider, stream=True, ignore_working=True)
    print(f"Model: {model}, Provider: {provider}")
except Exception as ex:
    print(f"Error: {ex}")
```

### `get_last_provider`

```python
def get_last_provider(as_dict: bool = False) -> Union[ProviderType, dict[str, str], None]:
    """
    Извлекает последнего использованного провайдера.

    Args:
        as_dict (bool, optional): Если True, возвращает информацию о провайдере в виде словаря. По умолчанию False.

    Returns:
        Union[ProviderType, dict[str, str]]: Последний использованный провайдер, либо объект, либо словарь.

    Как работает функция:
    1. Получает последнего использованного провайдера из `debug.last_provider`.
    2. Если последний провайдер является `BaseRetryProvider`, получает последнего провайдера из него.
    3. Если `as_dict` имеет значение True, возвращает информацию о провайдере в виде словаря, содержащего имя, URL, модель и метку (если есть).
    4. Если `as_dict` имеет значение False, возвращает объект провайдера.

    ASCII flowchart:
    Start --> GetLastProvider
    GetLastProvider --> IsRetryProvider?
    IsRetryProvider? -- Yes --> GetLastProviderFromRetryProvider
    GetLastProvider --> AsDict?
    AsDict? -- Yes --> ReturnProviderAsDict
    AsDict? -- No --> ReturnProviderObject
    """
    ...
```

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.client.service import get_last_provider
from src.endpoints.gpt4free.g4f.models import Model
from src.endpoints.gpt4free.g4f.providers import RetryProvider
from src.endpoints.gpt4free.g4f import debug

try:
    model, provider = get_model_and_provider(model="gpt-3.5-turbo", provider="BingAI", stream=False)
    last_provider = get_last_provider()
    print(f"Last Provider: {last_provider}")
except Exception as ex:
    print(f"Error: {ex}")

try:
    model, provider = get_model_and_provider(model=Model.gpt_4, provider=RetryProvider, stream=True, ignore_working=True)
    last_provider_dict = get_last_provider(as_dict=True)
    print(f"Last Provider as Dict: {last_provider_dict}")
except Exception as ex:
    print(f"Error: {ex}")