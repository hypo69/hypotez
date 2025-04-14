### Анализ кода модуля `service.py`

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код достаточно хорошо структурирован и читаем.
    - Присутствуют аннотации типов.
    - Используются исключения для обработки ошибок.
- **Минусы**:
    - Не все функции и методы имеют подробные docstring, особенно внутренние.
    - Используется `Union` вместо `|` для обозначения типов.
    - Отсутствует логирование с использованием модуля `logger` из `src.logger`.

**Рекомендации по улучшению:**

1.  **Документация**:
    - Добавить docstring для всех функций, методов и классов, включая внутренние функции.
    - Описать каждый параметр и возвращаемое значение, а также возможные исключения.
    - Перевести существующие docstring на русский язык, если они на английском.
2.  **Типизация**:
    - Заменить `Union` на `|` для обозначения объединения типов.
3.  **Логирование**:
    - Добавить логирование с использованием модуля `logger` из `src.logger` для отслеживания важных событий и ошибок.
    - Логировать ошибки с использованием `logger.error` и передавать исключение `ex` в качестве аргумента.
4.  **Обработка исключений**:
    - Использовать `ex` вместо `e` в блоках `except`.
5.  **Форматирование**:
    - Использовать одинарные кавычки для строк.

**Оптимизированный код:**

```python
from __future__ import annotations

from typing import Union, Optional

from .. import debug, version
from ..errors import ProviderNotFoundError, ModelNotFoundError, ProviderNotWorkingError, StreamNotSupportedError
from ..models import Model, ModelUtils, default, default_vision
from ..Provider import ProviderUtils
from ..providers.types import BaseRetryProvider, ProviderType
from ..providers.retry_provider import IterListProvider

from src.logger import logger  # Import logger


def convert_to_provider(provider: str) -> ProviderType:
    """Преобразует строку с именем провайдера в объект провайдера.

    Args:
        provider (str): Имя провайдера. Может содержать несколько провайдеров, разделенных пробелом.

    Returns:
        ProviderType: Объект провайдера.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.
    """
    if ' ' in provider:
        provider_list = [ProviderUtils.convert[p] for p in provider.split() if p in ProviderUtils.convert]
        if not provider_list:
            msg = f'Провайдеры не найдены: {provider}'
            logger.error(msg)
            raise ProviderNotFoundError(msg)
        provider = IterListProvider(provider_list, False)
    elif provider in ProviderUtils.convert:
        provider = ProviderUtils.convert[provider]
    elif provider:
        msg = f'Провайдер не найден: {provider}'
        logger.error(msg)
        raise ProviderNotFoundError(msg)
    return provider


def get_model_and_provider(
    model: Model | str,
    provider: ProviderType | str | None,
    stream: bool,
    ignore_working: bool = False,
    ignore_stream: bool = False,
    logging: bool = True,
    has_images: bool = False,
) -> tuple[str, ProviderType]:
    """Извлекает модель и провайдера на основе входных параметров.

    Args:
        model (Model | str): Модель для использования, либо объект, либо строковый идентификатор.
        provider (ProviderType | str | None): Провайдер для использования, либо объект, либо строковый идентификатор, либо None.
        stream (bool): Указывает, следует ли выполнять операцию в потоковом режиме.
        ignore_working (bool, optional): Если True, игнорирует рабочий статус провайдера. По умолчанию False.
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
                model = getattr(provider, 'default_model', '')
            else:
                msg = f'Модель не найдена: {model}'
                logger.error(msg)
                raise ModelNotFoundError(msg)
        elif isinstance(model, Model):
            provider = model.best_provider
        else:
            msg = f'Неожиданный тип: {type(model)}'
            logger.error(msg)
            raise ValueError(msg)
    if not provider:
        msg = f'Не найден провайдер для модели: {model}'
        logger.error(msg)
        raise ProviderNotFoundError(msg)

    provider_name = provider.__name__ if hasattr(provider, '__name__') else type(provider).__name__

    if isinstance(model, Model):
        model = model.name

    if not ignore_working and not provider.working:
        msg = f'{provider_name} не работает'
        logger.error(msg)
        raise ProviderNotWorkingError(msg)

    if isinstance(provider, BaseRetryProvider):
        if not ignore_working:
            provider.providers = [p for p in provider.providers if p.working]

    if not ignore_stream and not provider.supports_stream and stream:
        msg = f'{provider_name} не поддерживает аргумент "stream"'
        logger.error(msg)
        raise StreamNotSupportedError(msg)

    if logging:
        if model:
            debug.log(f'Используется провайдер {provider_name} и модель {model}')
        else:
            debug.log(f'Используется провайдер {provider_name}')

    debug.last_provider = provider
    debug.last_model = model

    return model, provider


def get_last_provider(as_dict: bool = False) -> Union[ProviderType, dict[str, str], None]:
    """Извлекает последнего использованного провайдера.

    Args:
        as_dict (bool, optional): Если True, возвращает информацию о провайдере в виде словаря. По умолчанию False.

    Returns:
        ProviderType | dict[str, str] | None: Последний использованный провайдер, либо объект, либо словарь, либо None.
    """
    last = debug.last_provider
    if isinstance(last, BaseRetryProvider):
        last = last.last_provider
    if as_dict:
        if last:
            return {
                'name': last.__name__ if hasattr(last, '__name__') else type(last).__name__,
                'url': last.url,
                'model': debug.last_model,
                'label': getattr(last, 'label', None) if hasattr(last, 'label') else None,
            }
        else:
            return {}
    return last