# Модуль service.py

## Обзор

Модуль `service.py` предназначен для управления провайдерами и моделями, используемыми в проекте `hypotez`. Он предоставляет функции для преобразования строк в объекты провайдеров, получения моделей и провайдеров на основе заданных параметров, а также для получения информации о последнем использованном провайдере. Модуль также обрабатывает ошибки, связанные с отсутствием провайдеров, моделей или неработоспособностью провайдеров.

## Подробнее

Модуль содержит функции для преобразования идентификаторов провайдеров в соответствующие объекты, а также для извлечения моделей и провайдеров на основе входных параметров. Он также включает обработку ошибок, связанных с отсутствием провайдеров, моделей или неработоспособностью провайдеров. Этот код используется для динамического выбора и настройки провайдеров и моделей в системе, что позволяет гибко адаптироваться к различным условиям и требованиям.

## Функции

### `convert_to_provider`

```python
def convert_to_provider(provider: str) -> ProviderType:
    """Преобразует строку, представляющую провайдера, в объект ProviderType.

    Args:
        provider (str): Строка с именем провайдера. Может содержать несколько провайдеров, разделенных пробелами.

    Returns:
        ProviderType: Объект провайдера.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.

    Как работает функция:
    - Проверяет, содержит ли строка `provider` пробелы. Если да, разделяет строку на список провайдеров.
    - Преобразует каждый провайдер в списке в соответствующий объект ProviderType, используя `ProviderUtils.convert`.
    - Если ни один провайдер не найден, вызывает исключение `ProviderNotFoundError`.
    - Если строка `provider` не содержит пробелов, пытается преобразовать ее в объект ProviderType, используя `ProviderUtils.convert`.
    - Если провайдер не найден, вызывает исключение `ProviderNotFoundError`.

    Примеры:
    >>> convert_to_provider("FreeGPT")
    <src.providers.FreeGPT.FreeGPT object at ...>

    >>> convert_to_provider("FreeGPT Bing")
    <src.providers.retry_provider.IterListProvider object at ...>

    >>> convert_to_provider("NonExistentProvider")
    Traceback (most recent call last):
      ...
    src.errors.ProviderNotFoundError: Provider not found: NonExistentProvider
    """
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
    """Извлекает модель и провайдера на основе входных параметров.

    Args:
        model (Union[Model, str]): Модель для использования, объект или строковый идентификатор.
        provider (Union[ProviderType, str, None]): Провайдер для использования, объект, строковый идентификатор или None.
        stream (bool): Указывает, должна ли операция выполняться в режиме потока.
        ignore_working (bool, optional): Если True, игнорирует статус работоспособности провайдера. По умолчанию False.
        ignore_stream (bool, optional): Если True, игнорирует возможность потоковой передачи провайдера. По умолчанию False.
        logging (bool, optional): Если True, включает логирование. По умолчанию True.
        has_images (bool, optional): Если True, указывает, что запрос содержит изображения. По умолчанию False.

    Returns:
        tuple[str, ProviderType]: Кортеж, содержащий имя модели и тип провайдера.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.
        ModelNotFoundError: Если модель не найдена.
        ProviderNotWorkingError: Если провайдер не работает.
        StreamNotSupportedError: Если потоковая передача не поддерживается провайдером.

    Как работает функция:
    - Проверяет версию и обновляет, если необходимо.
    - Преобразует строковое представление провайдера в объект ProviderType, используя функцию `convert_to_provider`.
    - Преобразует строковое представление модели в объект Model, используя `ModelUtils.convert`.
    - Если провайдер не указан, выбирает провайдера по умолчанию в зависимости от наличия изображений и типа модели.
    - Проверяет работоспособность провайдера и поддерживает ли он потоковую передачу, если это необходимо.
    - Логирует использование провайдера и модели.

    Примеры:
    >>> get_model_and_provider(model="gpt-3.5-turbo", provider="FreeGPT", stream=False)
    ('gpt-3.5-turbo', <src.providers.FreeGPT.FreeGPT object at ...>)

    >>> get_model_and_provider(model=default, provider=None, stream=True, ignore_stream=True)
    ('gpt-3.5-turbo', <src.providers.FreeGPT.FreeGPT object at ...>)
    """
```

### `get_last_provider`

```python
def get_last_provider(as_dict: bool = False) -> Union[ProviderType, dict[str, str], None]:
    """Извлекает последнего использованного провайдера.

    Args:
        as_dict (bool, optional): Если True, возвращает информацию о провайдере в виде словаря. По умолчанию False.

    Returns:
        Union[ProviderType, dict[str, str], None]: Последний использованный провайдер, объект или словарь.

    Как работает функция:
    - Получает последнего использованного провайдера из `debug.last_provider`.
    - Если провайдер является `BaseRetryProvider`, извлекает последнего использованного провайдера из него.
    - Если `as_dict` равен True, возвращает информацию о провайдере в виде словаря, содержащего имя, URL, модель и метку.
    - В противном случае возвращает объект провайдера.

    Примеры:
    >>> get_last_provider()
    <src.providers.FreeGPT.FreeGPT object at ...>

    >>> get_last_provider(as_dict=True)
    {'name': 'FreeGPT', 'url': 'https://freegpt.org/', 'model': 'gpt-3.5-turbo', 'label': None}
    """