### Анализ кода модуля `service.py`

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код достаточно хорошо структурирован и содержит обработку исключений.
  - Присутствуют аннотации типов.
  - Есть docstring для функций.
- **Минусы**:
  - Docstring написаны на английском языке.
  - Используется `Union`, когда можно использовать `|`.
  - Не все переменные аннотированы.
  - Отсутствуют логирования.

**Рекомендации по улучшению**:
- Перевести docstring на русский язык.
- Использовать `|` вместо `Union`.
- Добавить логирование для отслеживания ошибок и важной информации.
- Добавить аннотации типов для всех переменных.
- Для обработки ошибок использовать `logger.error` из `src.logger.logger`.
- Изменить имя переменной исключения с `e` на `ex`.

**Оптимизированный код**:
```python
from __future__ import annotations

from typing import Union, Optional

from .. import debug, version
from ..errors import ProviderNotFoundError, ModelNotFoundError, ProviderNotWorkingError, StreamNotSupportedError
from ..models import Model, ModelUtils, default, default_vision
from ..Provider import ProviderUtils
from ..providers.types import BaseRetryProvider, ProviderType
from ..providers.retry_provider import IterListProvider
from src.logger import logger
from typing import List

def convert_to_provider(provider: str) -> ProviderType:
    """
    Преобразует строку с именем провайдера в объект провайдера.

    Args:
        provider (str): Имя провайдера.

    Returns:
        ProviderType: Объект провайдера.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.
    """
    if " " in provider:
        provider_list: List[ProviderType] = [ProviderUtils.convert[p] for p in provider.split() if p in ProviderUtils.convert]
        if not provider_list:
            msg = f'Providers not found: {provider}'
            logger.error(msg)
            raise ProviderNotFoundError(msg)
        provider: IterListProvider = IterListProvider(provider_list, False)
    elif provider in ProviderUtils.convert:
        provider: ProviderType = ProviderUtils.convert[provider]
    elif provider:
        msg = f'Provider not found: {provider}'
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
    has_images: bool = False
) -> tuple[str, ProviderType]:
    """
    Получает модель и провайдера на основе входных параметров.

    Args:
        model (Model | str): Модель для использования, объект или строковый идентификатор.
        provider (ProviderType | str | None): Провайдер для использования, объект, строковый идентификатор или None.
        stream (bool): Указывает, следует ли выполнять операцию в режиме потока.
        ignore_working (bool, optional): Если True, игнорирует рабочий статус провайдера. По умолчанию False.
        ignore_stream (bool, optional): Если True, игнорирует поддержку потоковой передачи у провайдера. По умолчанию False.
        logging (bool, optional): Логировать ли использование провайдера и модели. По умолчанию True.
        has_images (bool, optional): Указывает, содержит ли запрос изображения. По умолчанию False.

    Returns:
        tuple[str, ProviderType]: Кортеж, содержащий имя модели и тип провайдера.

    Raises:
        ProviderNotFoundError: Если провайдер не найден.
        ModelNotFoundError: Если модель не найдена.
        ProviderNotWorkingError: Если провайдер не работает.
        StreamNotSupportedError: Если потоковая передача не поддерживается провайдером.
    """
    if debug.version_check:
        debug.version_check: bool = False
        version.utils.check_version()

    if isinstance(provider, str):
        provider: ProviderType = convert_to_provider(provider)

    if isinstance(model, str):
        if model in ModelUtils.convert:
            model: Model = ModelUtils.convert[model]

    if not provider:
        if not model:
            if has_images:
                model: Model = default_vision
                provider: ProviderType = default_vision.best_provider
            else:
                model: Model = default
                provider: ProviderType = model.best_provider
        elif isinstance(model, str):
            if model in ProviderUtils.convert:
                provider: ProviderType = ProviderUtils.convert[model]
                model: str = getattr(provider, "default_model", "")
            else:
                msg = f'Model not found: {model}'
                logger.error(msg)
                raise ModelNotFoundError(msg)
        elif isinstance(model, Model):
            provider: ProviderType = model.best_provider
        else:
            msg = f"Unexpected type: {type(model)}"
            logger.error(msg)
            raise ValueError(msg)
    if not provider:
        msg = f'No provider found for model: {model}'
        logger.error(msg)
        raise ProviderNotFoundError(msg)

    provider_name: str = provider.__name__ if hasattr(provider, "__name__") else type(provider).__name__

    if isinstance(model, Model):
        model: str = model.name

    if not ignore_working and not provider.working:
        msg = f"{provider_name} is not working"
        logger.error(msg)
        raise ProviderNotWorkingError(msg)

    if isinstance(provider, BaseRetryProvider):
        if not ignore_working:
            provider.providers: List[ProviderType] = [p for p in provider.providers if p.working]

    if not ignore_stream and not provider.supports_stream and stream:
        msg = f'{provider_name} does not support "stream" argument'
        logger.error(msg)
        raise StreamNotSupportedError(msg)

    if logging:
        if model:
            debug.log(f'Using {provider_name} provider and {model} model')
        else:
            debug.log(f'Using {provider_name} provider')

    debug.last_provider: ProviderType = provider
    debug.last_model: str = model

    return model, provider

def get_last_provider(as_dict: bool = False) -> Union[ProviderType, dict[str, str], None]:
    """
    Получает последнего использованного провайдера.

    Args:
        as_dict (bool, optional): Если True, возвращает информацию о провайдере в виде словаря. По умолчанию False.

    Returns:
        Union[ProviderType, dict[str, str], None]: Последний использованный провайдер, объект или словарь.
    """
    last: ProviderType = debug.last_provider
    if isinstance(last, BaseRetryProvider):
        last: ProviderType = last.last_provider
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