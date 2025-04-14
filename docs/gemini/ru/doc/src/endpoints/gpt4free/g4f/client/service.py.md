# Модуль service

## Обзор

Модуль `service` предоставляет функциональность для выбора и настройки провайдеров и моделей для работы с API. Он включает в себя функции для конвертации строк в объекты провайдеров, получения моделей и провайдеров на основе заданных параметров, а также для получения информации о последнем использованном провайдере.

## Подробней

Модуль `service` играет важную роль в проекте `hypotez`, поскольку он позволяет динамически выбирать и настраивать различные провайдеры и модели, используемые для генерации текста. Он обеспечивает гибкость и расширяемость системы, позволяя легко добавлять и использовать новые провайдеры и модели.

## Функции

### `convert_to_provider`

```python
def convert_to_provider(provider: str) -> ProviderType:
    """
    Преобразует строку с именем провайдера в объект провайдера.

    Args:
        provider (str): Имя провайдера. Может содержать несколько провайдеров, разделенных пробелами.

    Returns:
        ProviderType: Объект провайдера.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.
    """
    ...
```

**Назначение**: Преобразует строку с именем провайдера в объект провайдера. Если указано несколько провайдеров через пробел, создает `IterListProvider`.

**Как работает функция**:
- Проверяет, содержит ли строка `provider` пробелы. Если да, разбивает строку на список провайдеров.
- Преобразует каждый элемент списка в соответствующий объект провайдера с помощью `ProviderUtils.convert`.
- Если список провайдеров пуст, вызывает исключение `ProviderNotFoundError`.
- Если в строке `provider` нет пробелов, пытается найти провайдера в `ProviderUtils.convert`.
- Если провайдер не найден, вызывает исключение `ProviderNotFoundError`.

**Примеры**:
```python
# Пример 1: Преобразование строки с именем провайдера в объект провайдера
provider = convert_to_provider("You")
# Пример 2: Преобразование строки с несколькими именами провайдеров в объект IterListProvider
provider = convert_to_provider("You Llama2")
# Пример 3: Обработка ошибки, когда провайдер не найден
try:
    provider = convert_to_provider("NonExistentProvider")
except ProviderNotFoundError as ex:
    logger.error("Provider not found", ex, exc_info=True)
```

### `get_model_and_provider`

```python
def get_model_and_provider(model    : Union[Model, str], 
                           provider : Union[ProviderType, str, None], 
                           stream   : bool,
                           ignore_working: bool = False,
                           ignore_stream: bool = False,
                           logging: bool = True,
                           has_images: bool = False) -> tuple[str, ProviderType]:
    """
    Получает модель и провайдера на основе входных параметров.

    Args:
        model (Union[Model, str]): Модель для использования, либо объект, либо строковый идентификатор.
        provider (Union[ProviderType, str, None]): Провайдер для использования, либо объект, либо строковый идентификатор, либо None.
        stream (bool): Указывает, следует ли выполнять операцию в потоковом режиме.
        ignore_working (bool, optional): Если True, игнорирует рабочий статус провайдера.
        ignore_stream (bool, optional): Если True, игнорирует возможность потоковой передачи провайдера.
        logging (bool, optional): Если True, включает логирование.
        has_images (bool, optional): Если True, указывает, что запрос содержит изображения.

    Returns:
        tuple[str, ProviderType]: Кортеж, содержащий имя модели и тип провайдера.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.
        ModelNotFoundError: Если модель не найдена.
        ProviderNotWorkingError: Если провайдер не работает.
        StreamNotSupportedError: Если потоковая передача не поддерживается провайдером.
    """
    ...
```

**Назначение**: Получает модель и провайдера на основе входных параметров.

**Как работает функция**:
- Выполняет проверку версии, если `debug.version_check` имеет значение `True`.
- Если `provider` является строкой, преобразует ее в объект провайдера с помощью `convert_to_provider`.
- Если `model` является строкой, пытается найти модель в `ModelUtils.convert`.
- Если `provider` не указан, определяет модель и провайдера по умолчанию в зависимости от наличия изображений и типа модели.
- Проверяет, работает ли провайдер, если `ignore_working` имеет значение `False`.
- Проверяет, поддерживает ли провайдер потоковую передачу, если `ignore_stream` имеет значение `False` и `stream` имеет значение `True`.
- Выполняет логирование, если `logging` имеет значение `True`.

**Примеры**:
```python
# Пример 1: Получение модели и провайдера по умолчанию
model, provider = get_model_and_provider(model=None, provider=None, stream=False)
# Пример 2: Получение модели и провайдера с указанием имени провайдера
model, provider = get_model_and_provider(model="gpt-3.5-turbo", provider="You", stream=False)
# Пример 3: Получение модели и провайдера с указанием объекта провайдера
provider_obj = convert_to_provider("You")
model, provider = get_model_and_provider(model="gpt-3.5-turbo", provider=provider_obj, stream=False)
# Пример 4: Обработка ошибки, когда провайдер не работает
try:
    model, provider = get_model_and_provider(model="gpt-3.5-turbo", provider="Test", stream=False)
except ProviderNotWorkingError as ex:
    logger.error("Provider is not working", ex, exc_info=True)
```

### `get_last_provider`

```python
def get_last_provider(as_dict: bool = False) -> Union[ProviderType, dict[str, str], None]:
    """
    Получает последнего использованного провайдера.

    Args:
        as_dict (bool, optional): Если True, возвращает информацию о провайдере в виде словаря.

    Returns:
        Union[ProviderType, dict[str, str]]: Последний использованный провайдер, либо объект, либо словарь.
    """
    ...
```

**Назначение**: Получает информацию о последнем использованном провайдере.

**Как работает функция**:
- Получает последнего использованного провайдера из `debug.last_provider`.
- Если последний провайдер является экземпляром `BaseRetryProvider`, получает последнего провайдера из него.
- Если `as_dict` имеет значение `True`, возвращает информацию о провайдере в виде словаря, содержащего имя, URL, модель и метку провайдера.

**Примеры**:
```python
# Пример 1: Получение последнего использованного провайдера в виде объекта
last_provider = get_last_provider()
# Пример 2: Получение последнего использованного провайдера в виде словаря
last_provider_dict = get_last_provider(as_dict=True)