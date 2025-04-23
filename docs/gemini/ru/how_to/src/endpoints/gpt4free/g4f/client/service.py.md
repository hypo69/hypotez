### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код предоставляет функции для управления и выбора моделей и провайдеров в системе. Он включает в себя функции для конвертации строк в объекты провайдеров, получения модели и провайдера на основе входных параметров, а также для получения последнего использованного провайдера.

Шаги выполнения
-------------------------
1. **Конвертация строки в провайдер**: Функция `convert_to_provider` преобразует строковое представление провайдера в объект провайдера. Если строка содержит несколько провайдеров, разделенных пробелами, она создает `IterListProvider` из списка провайдеров.

2. **Получение модели и провайдера**: Функция `get_model_and_provider` определяет модель и провайдера на основе входных параметров. Она обрабатывает различные типы входных данных (модель и провайдер могут быть строками или объектами) и выбирает оптимальные значения по умолчанию, если они не указаны явно.

3. **Обработка ошибок**: В функции `get_model_and_provider` проверяется работоспособность провайдера и поддержка потоковой передачи. Если провайдер не работает или не поддерживает потоковую передачу, вызываются исключения `ProviderNotWorkingError` или `StreamNotSupportedError` соответственно.

4. **Получение последнего использованного провайдера**: Функция `get_last_provider` возвращает последний использованный провайдер. Если `as_dict` установлен в `True`, она возвращает информацию о провайдере в виде словаря.

Пример использования
-------------------------

```python
from __future__ import annotations

from typing import Union

from .. import debug, version
from ..errors import ProviderNotFoundError, ModelNotFoundError, ProviderNotWorkingError, StreamNotSupportedError
from ..models import Model, ModelUtils, default, default_vision
from ..Provider import ProviderUtils
from ..providers.types import BaseRetryProvider, ProviderType
from ..providers.retry_provider import IterListProvider


def convert_to_provider(provider: str) -> ProviderType:
    """
    Конвертирует строковое представление провайдера в объект провайдера.

    Args:
        provider (str): Строковое представление провайдера.

    Returns:
        ProviderType: Объект провайдера.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.
    """
    if " " in provider:
        provider_list = [ProviderUtils.convert[p] for p in provider.split() if p in ProviderUtils.convert]
        if not provider_list:
            raise ProviderNotFoundError(f'Providers not found: {provider}')
        provider = IterListProvider(provider_list, False)
    elif provider in ProviderUtils.convert:
        provider = ProviderUtils.convert[provider]
    elif provider:
        raise ProviderNotFoundError(f'Provider not found: {provider}')
    return provider


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
        stream (bool): Указывает, должна ли операция выполняться как поток.
        ignore_working (bool, optional): Если True, игнорирует рабочий статус провайдера.
        ignore_stream (bool, optional): Если True, игнорирует возможность потоковой передачи провайдера.

    Returns:
        tuple[str, ProviderType]: Кортеж, содержащий имя модели и тип провайдера.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.
        ModelNotFoundError: Если модель не найдена.
        ProviderNotWorkingError: Если провайдер не работает.
        StreamNotSupportedError: Если потоковая передача не поддерживается провайдером.
    """
    if debug.version_check:
        debug.version_check = False
        version.utils.check_version()

    if isinstance(provider, str):
        provider = convert_to_provider(provider)

    if isinstance(model, str):
        if model in ModelUtils.convert:
            model = ModelUtils.convert[model]

    if not provider:
        if not model:
            if has_images:
                model = default_vision
                provider = default_vision.best_provider
            else:
                model = default
                provider = model.best_provider
        elif isinstance(model, str):
            if model in ProviderUtils.convert:
                provider = ProviderUtils.convert[model]
                model = getattr(provider, "default_model", "")
            else:
                raise ModelNotFoundError(f'Model not found: {model}')
        elif isinstance(model, Model):
            provider = model.best_provider
        else:
            raise ValueError(f"Unexpected type: {type(model)}")
    if not provider:
        raise ProviderNotFoundError(f'No provider found for model: {model}')

    provider_name = provider.__name__ if hasattr(provider, "__name__") else type(provider).__name__

    if isinstance(model, Model):
        model = model.name

    if not ignore_working and not provider.working:
        raise ProviderNotWorkingError(f"{provider_name} is not working")

    if isinstance(provider, BaseRetryProvider):
        if not ignore_working:
            provider.providers = [p for p in provider.providers if p.working]

    if not ignore_stream and not provider.supports_stream and stream:
        raise StreamNotSupportedError(f'{provider_name} does not support "stream" argument')

    if logging:
        if model:
            debug.log(f'Using {provider_name} provider and {model} model')
        else:
            debug.log(f'Using {provider_name} provider')

    debug.last_provider = provider
    debug.last_model = model

    return model, provider


def get_last_provider(as_dict: bool = False) -> Union[ProviderType, dict[str, str], None]:
    """
    Извлекает последнего использованного провайдера.

    Args:
        as_dict (bool, optional): Если True, возвращает информацию о провайдере в виде словаря.

    Returns:
        Union[ProviderType, dict[str, str]]: Последний использованный провайдер, либо объект, либо словарь.
    """
    last = debug.last_provider
    if isinstance(last, BaseRetryProvider):
        last = last.last_provider
    if as_dict:
        if last:
            return {
                "name": last.__name__ if hasattr(last, "__name__") else type(last).__name__,
                "url": last.url,
                "model": debug.last_model,
                "label": getattr(last, "label", None) if hasattr(last, "label") else None
            }
        else:
            return {}
    return last


# Пример использования функций
try:
    # Получение модели и провайдера
    model_name, provider_object = get_model_and_provider(model="gpt-3.5-turbo", provider="FreeGPT", stream=False)
    print(f"Модель: {model_name}, Провайдер: {provider_object.__name__}")

    # Получение последнего использованного провайдера в виде словаря
    last_provider_info = get_last_provider(as_dict=True)
    print(f"Последний провайдер: {last_provider_info}")
except ProviderNotFoundError as e:
    print(f"Ошибка: {e}")
except ModelNotFoundError as e:
    print(f"Ошибка: {e}")
except ProviderNotWorkingError as e:
    print(f"Ошибка: {e}")
except StreamNotSupportedError as e:
    print(f"Ошибка: {e}")