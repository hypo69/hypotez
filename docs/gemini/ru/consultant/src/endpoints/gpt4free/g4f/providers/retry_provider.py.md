### **Анализ кода модуля `retry_provider.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код достаточно структурирован и логически понятен.
  - Используются аннотации типов.
  - Присутствует обработка исключений.
- **Минусы**:
  - Не все функции и классы имеют подробные docstring.
  - Местами отсутствует логирование.
  - Используются конструкции `Union[]` вместо `|`.
  - В некоторых местах комментарии не соответствуют PEP8.
  - Отсутствует единый стиль логирования (используется `print` вместо `logger`).

#### **Рекомендации по улучшению**:
1. **Документирование**:
   - Добавить подробные docstring для всех классов и функций, включая описание параметров, возвращаемых значений и возможных исключений.
   - Перевести существующие docstring на русский язык.
2. **Логирование**:
   - Заменить все `print` statements на `logger.debug` или `logger.info` в зависимости от важности сообщения.
   - Добавить логирование в блоки `except`, используя `logger.error` с передачей исключения (`ex`) и `exc_info=True`.
3. **Обработка исключений**:
   - Использовать `ex` вместо `e` в блоках `except`.
4. **Использование `|` вместо `Union[]`**:
   - Заменить все конструкции `Union[]` на `|` для обозначения объединения типов.
5. **Форматирование**:
   - Убедиться, что все строки используют одинарные кавычки (`'`).
   - Добавить пробелы вокруг операторов присваивания (`=`).
6. **Комментарии**:
   - Сделать комментарии более информативными, избегая общих фраз вроде "получаем" или "делаем".
7. **Общая структура**:
   - Добавить заголовок модуля с описанием его назначения и примерами использования.

#### **Оптимизированный код**:

```python
"""
Модуль для реализации логики повторных вызовов провайдеров при сбоях.
====================================================================

Модуль содержит классы `IterListProvider` и `RetryProvider`, которые позволяют организовать
повторные попытки использования различных провайдеров для получения результатов,
а также обрабатывать исключения, возникающие в процессе.

Пример использования
----------------------

>>> providers = [Provider1, Provider2]
>>> retry_provider = RetryProvider(providers=providers, shuffle=True, single_provider_retry=False, max_retries=3)
>>> for chunk in retry_provider.create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}]):
>>>     print(chunk)
"""

from __future__ import annotations

import random
from typing import Type, List, CreateResult, Messages, AsyncResult

from src.logger import logger  # Импорт модуля логирования
from .types import BaseProvider, BaseRetryProvider, ProviderType
from .response import MediaResponse, ProviderInfo
from .. import debug
from ..errors import RetryProviderError, RetryNoProviderError


class IterListProvider(BaseRetryProvider):
    def __init__(
        self,
        providers: List[Type[BaseProvider]],
        shuffle: bool = True
    ) -> None:
        """
        Инициализация класса IterListProvider.

        Args:
            providers (List[Type[BaseProvider]]): Список провайдеров для использования.
            shuffle (bool): Флаг, указывающий, следует ли перемешивать список провайдеров.
        """
        self.providers: List[Type[BaseProvider]] = providers
        self.shuffle: bool = shuffle
        self.working: bool = True
        self.last_provider: Type[BaseProvider] = None

    def create_completion(
        self,
        model: str,
        messages: Messages,
        stream: bool = False,
        ignore_stream: bool = False,
        ignored: list[str] = [],
        **kwargs,
    ) -> CreateResult:
        """
        Создает завершение, используя доступных провайдеров, с возможностью потоковой передачи ответа.

        Args:
            model (str): Модель, используемая для завершения.
            messages (Messages): Сообщения, используемые для генерации завершения.
            stream (bool, optional): Флаг, указывающий, следует ли передавать ответ потоком. Defaults to False.
            ignore_stream (bool, optional): Флаг, указывающий, следует ли игнорировать потоковую передачу. Defaults to False.
            ignored (list[str], optional): Список провайдеров, которые следует игнорировать. Defaults to [].
            **kwargs: Дополнительные аргументы.

        Yields:
            CreateResult: Токены или результаты от завершения.

        Raises:
            RetryProviderError: Если все провайдеры вернули ошибку.
            RetryNoProviderError: Если не найдено ни одного провайдера.
        """
        exceptions: dict = {}
        started: bool = False

        for provider in self.get_providers(stream and not ignore_stream, ignored):
            self.last_provider: Type[BaseProvider] = provider
            logger.debug(f'Используется провайдер {provider.__name__}')
            yield ProviderInfo(**provider.get_dict(), model=model if model else getattr(provider, 'default_model'))
            try:
                response = provider.get_create_function()(model, messages, stream=stream, **kwargs)
                for chunk in response:
                    if chunk:
                        yield chunk
                        if isinstance(chunk, (str, MediaResponse)):
                            started = True
                if started:
                    return
            except Exception as ex:
                exceptions[provider.__name__] = ex
                logger.error(f'Провайдер {provider.__name__} {type(ex).__name__}: {ex}', exc_info=True)
                if started:
                    raise ex
                yield ex

        raise_exceptions(exceptions)

    async def create_async_generator(
        self,
        model: str,
        messages: Messages,
        stream: bool = True,
        ignore_stream: bool = False,
        ignored: list[str] = [],
        **kwargs
    ) -> AsyncResult:
        """
        Асинхронно создает генератор завершений, используя доступных провайдеров.

        Args:
            model (str): Модель, используемая для завершения.
            messages (Messages): Сообщения, используемые для генерации завершения.
            stream (bool, optional): Флаг, указывающий, следует ли передавать ответ потоком. Defaults to True.
            ignore_stream (bool, optional): Флаг, указывающий, следует ли игнорировать потоковую передачу. Defaults to False.
            ignored (list[str], optional): Список провайдеров, которые следует игнорировать. Defaults to [].
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncResult: Асинхронные токены или результаты от завершения.

        Raises:
            RetryProviderError: Если все провайдеры вернули ошибку.
            RetryNoProviderError: Если не найдено ни одного провайдера.
        """
        exceptions: dict = {}
        started: bool = False

        for provider in self.get_providers(stream and not ignore_stream, ignored):
            self.last_provider: Type[BaseProvider] = provider
            logger.debug(f'Используется провайдер {provider.__name__}')
            yield ProviderInfo(**provider.get_dict(), model=model if model else getattr(provider, 'default_model'))
            try:
                response = provider.get_async_create_function()(model, messages, stream=stream, **kwargs)
                if hasattr(response, '__aiter__'):
                    async for chunk in response:
                        if chunk:
                            yield chunk
                            if isinstance(chunk, (str, MediaResponse)):
                                started = True
                elif response:
                    response = await response
                    if response:
                        yield response
                        started = True
                if started:
                    return
            except Exception as ex:
                exceptions[provider.__name__] = ex
                logger.error(f'Провайдер {provider.__name__} {type(ex).__name__}: {ex}', exc_info=True)
                if started:
                    raise ex
                yield ex

        raise_exceptions(exceptions)

    def get_create_function(self) -> callable:
        """
        Возвращает функцию создания завершения.

        Returns:
            callable: Функция создания завершения.
        """
        return self.create_completion

    def get_async_create_function(self) -> callable:
        """
        Возвращает асинхронную функцию создания завершения.

        Returns:
            callable: Асинхронная функция создания завершения.
        """
        return self.create_async_generator

    def get_providers(self, stream: bool, ignored: list[str]) -> list[ProviderType]:
        """
        Возвращает список доступных провайдеров.

        Args:
            stream (bool): Флаг, указывающий, требуется ли потоковая передача.
            ignored (list[str]): Список провайдеров, которые следует игнорировать.

        Returns:
            list[ProviderType]: Список доступных провайдеров.
        """
        providers: list[ProviderType] = [p for p in self.providers if (p.supports_stream or not stream) and p.__name__ not in ignored]
        if self.shuffle:
            random.shuffle(providers)
        return providers


class RetryProvider(IterListProvider):
    def __init__(
        self,
        providers: List[Type[BaseProvider]],
        shuffle: bool = True,
        single_provider_retry: bool = False,
        max_retries: int = 3,
    ) -> None:
        """
        Инициализация класса RetryProvider.

        Args:
            providers (List[Type[BaseProvider]]): Список провайдеров для использования.
            shuffle (bool): Флаг, указывающий, следует ли перемешивать список провайдеров.
            single_provider_retry (bool): Флаг, указывающий, следует ли повторять попытки для одного провайдера.
            max_retries (int): Максимальное количество повторных попыток для одного провайдера.
        """
        super().__init__(providers, shuffle)
        self.single_provider_retry: bool = single_provider_retry
        self.max_retries: int = max_retries

    def create_completion(
        self,
        model: str,
        messages: Messages,
        stream: bool = False,
        **kwargs,
    ) -> CreateResult:
        """
        Создает завершение, используя доступных провайдеров, с возможностью повторных попыток для одного провайдера.

        Args:
            model (str): Модель, используемая для завершения.
            messages (Messages): Сообщения, используемые для генерации завершения.
            stream (bool, optional): Флаг, указывающий, следует ли передавать ответ потоком. Defaults to False.
            **kwargs: Дополнительные аргументы.

        Yields:
            CreateResult: Токены или результаты от завершения.

        Raises:
            RetryProviderError: Если все попытки для одного провайдера завершились неудачей.
        """
        if self.single_provider_retry:
            exceptions: dict = {}
            started: bool = False
            provider: Type[BaseProvider] = self.providers[0]
            self.last_provider: Type[BaseProvider] = provider
            for attempt in range(self.max_retries):
                try:
                    logger.debug(f'Используется провайдер {provider.__name__} (попытка {attempt + 1})')
                    response = provider.get_create_function()(model, messages, stream=stream, **kwargs)
                    for chunk in response:
                        if isinstance(chunk, str) or isinstance(chunk, MediaResponse):
                            yield chunk
                            started = True
                    if started:
                        return
                except Exception as ex:
                    exceptions[provider.__name__] = ex
                    logger.error(f'Провайдер {provider.__name__}: {type(ex).__name__}: {ex}', exc_info=True)
                    if started:
                        raise ex
            raise_exceptions(exceptions)
        else:
            yield from super().create_completion(model, messages, stream, **kwargs)

    async def create_async_generator(
        self,
        model: str,
        messages: Messages,
        stream: bool = True,
        **kwargs
    ) -> AsyncResult:
        """
        Асинхронно создает генератор завершений, используя доступных провайдеров,
        с возможностью повторных попыток для одного провайдера.

        Args:
            model (str): Модель, используемая для завершения.
            messages (Messages): Сообщения, используемые для генерации завершения.
            stream (bool, optional): Флаг, указывающий, следует ли передавать ответ потоком. Defaults to True.
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncResult: Асинхронные токены или результаты от завершения.

        Raises:
            RetryProviderError: Если все попытки для одного провайдера завершились неудачей.
        """
        exceptions: dict = {}
        started: bool = False

        if self.single_provider_retry:
            provider: Type[BaseProvider] = self.providers[0]
            self.last_provider: Type[BaseProvider] = provider
            for attempt in range(self.max_retries):
                try:
                    logger.debug(f'Используется провайдер {provider.__name__} (попытка {attempt + 1})')
                    response = provider.get_async_create_function()(model, messages, stream=stream, **kwargs)
                    if hasattr(response, '__aiter__'):
                        async for chunk in response:
                            if isinstance(chunk, str) or isinstance(chunk, MediaResponse):
                                yield chunk
                                started = True
                    else:
                        response = await response
                        if response:
                            yield response
                            started = True
                    if started:
                        return
                except Exception as ex:
                    exceptions[provider.__name__] = ex
                    logger.error(f'Провайдер {provider.__name__}: {type(ex).__name__}: {ex}', exc_info=True)
            raise_exceptions(exceptions)
        else:
            async for chunk in super().create_async_generator(model, messages, stream, **kwargs):
                yield chunk


def raise_exceptions(exceptions: dict) -> None:
    """
    Вызывает комбинированное исключение, если во время повторных попыток возникли какие-либо исключения.

    Args:
        exceptions (dict): Словарь исключений, возникших во время повторных попыток.

    Raises:
        RetryProviderError: Если какой-либо провайдер столкнулся с исключением.
        RetryNoProviderError: Если ни один провайдер не найден.
    """
    if exceptions:
        raise RetryProviderError('RetryProvider failed:\\n' + '\\n'.join([
            f'{p}: {type(exception).__name__}: {exception}' for p, exception in exceptions.items()
        ]))

    raise RetryNoProviderError('No provider found')