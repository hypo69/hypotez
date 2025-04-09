### **Анализ кода модуля `run_tools.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/tools/run_tools.py

Модуль содержит классы и функции для обработки инструментов, используемых в g4f, таких как поиск в интернете, продолжение генерации текста и работа с "bucket".

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код разбит на классы и функции, что облегчает понимание и поддержку.
    - Используются аннотации типов.
    - Есть обработка исключений.
- **Минусы**:
    - Некоторые docstring отсутствуют или неполные.
    - Не все переменные аннотированы типами.
    - В некоторых местах используется смешанный стиль кавычек (как одинарные, так и двойные).
    - Используются двойные кавычки в строках вместо одинарных.

**Рекомендации по улучшению:**

1.  **Добавить docstring**:
    - Добавить docstring для всех классов и методов, включая описание аргументов, возвращаемых значений и возможных исключений.
2.  **Улучшить существующие docstring**:
    - Перевести существующие docstring на русский язык и сделать их более подробными, следуя указанному в инструкции формату.
3.  **Исправить стиль кавычек**:
    - Заменить все двойные кавычки на одинарные.
4.  **Использовать `logger`**:
    - Заменить `debug.error` на `logger.error` из модуля `src.logger`.
5.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это возможно.
6.  **Обработка исключений**:
    - Использовать `ex` вместо `e` в блоках обработки исключений.
7.  **Избавиться от неоднозначности**:
    - Убедиться, что названия переменных и функций отражают их назначение.
8.  **Удалить неиспользуемые импорты**:
    - Проверить и удалить все неиспользуемые импорты.

**Оптимизированный код:**

```python
from __future__ import annotations

import re
import json
import asyncio
import time
from pathlib import Path
from typing import Optional, Callable, AsyncIterator, Iterator, Dict, Any, Tuple, List, Union

from ..typing import Messages
from ..providers.helper import filter_none
from ..providers.asyncio import to_async_iterator
from ..providers.response import Reasoning, FinishReason, Sources
from ..providers.types import ProviderType
from ..cookies import get_cookies_dir
from .web_search import do_search, get_search_message
from .files import read_bucket, get_bucket_dir
from src.logger import logger  # Import logger
# Constants
BUCKET_INSTRUCTIONS = """
Instruction: Make sure to add the sources of cites using [[domain]](Url) notation after the reference. Example: [[a-z0-9.]](http://example.com)
"""

TOOL_NAMES = {
    'SEARCH': 'search_tool',
    'CONTINUE': 'continue_tool',
    'BUCKET': 'bucket_tool'
}

class ToolHandler:
    """
    Обработчик инструментов.
    ========================

    Класс ToolHandler предназначен для обработки различных типов инструментов,
    таких как поиск в интернете, продолжение генерации и работа с "bucket".
    """
    
    @staticmethod
    def validate_arguments(data: dict) -> dict:
        """
        Проверяет и обрабатывает аргументы инструментов.

        Args:
            data (dict): Словарь, содержащий аргументы инструмента.

        Returns:
            dict: Отфильтрованный словарь аргументов.

        Raises:
            ValueError: Если аргументы не являются словарем или JSON-строкой.

        Example:
            >>> ToolHandler.validate_arguments({'arguments': '{"query": "example"}'})
            {'query': 'example'}
        """
        if 'arguments' in data:
            if isinstance(data['arguments'], str):
                data['arguments'] = json.loads(data['arguments'])
            if not isinstance(data['arguments'], dict):
                raise ValueError('Tool function arguments must be a dictionary or a json string')
            else:
                return filter_none(**data['arguments'])
        else:
            return {}
            
    @staticmethod
    async def process_search_tool(messages: Messages, tool: dict) -> Tuple[Messages, Sources | None]:
        """
        Обрабатывает запросы инструмента поиска.

        Args:
            messages (Messages): Список сообщений.
            tool (dict): Словарь, содержащий информацию об инструменте.

        Returns:
            Tuple[Messages, Sources | None]: Обновленный список сообщений и источники.

        Example:
            >>> messages = [{'role': 'user', 'content': 'search example'}]
            >>> tool = {'function': {'arguments': {'query': 'example'}}}
            >>> await ToolHandler.process_search_tool(messages, tool)
            ([{'role': 'user', 'content': 'example search results'}], None)
        """
        messages = messages.copy()
        args = ToolHandler.validate_arguments(tool['function'])
        messages[-1]['content'], sources = await do_search(
            messages[-1]['content'],
            **args
        )
        return messages, sources
    
    @staticmethod
    def process_continue_tool(messages: Messages, tool: dict, provider: Any) -> Tuple[Messages, Dict[str, Any]]:
        """
        Обрабатывает запросы инструмента продолжения.

        Args:
            messages (Messages): Список сообщений.
            tool (dict): Словарь, содержащий информацию об инструменте.
            provider (Any): Провайдер.

        Returns:
            Tuple[Messages, Dict[str, Any]]: Обновленный список сообщений и дополнительные аргументы.

        Example:
            >>> messages = [{'role': 'user', 'content': 'example text'}]
            >>> tool = {'function': {}}
            >>> provider = 'TestProvider'
            >>> ToolHandler.process_continue_tool(messages, tool, provider)
            ([{'role': 'user', 'content': 'example text'}, {'role': 'user', 'content': 'Carry on from this point:\\nexample text'}], {})
        """
        kwargs = {}
        if provider not in ('OpenaiAccount', 'HuggingFaceAPI'):
            messages = messages.copy()
            last_line = messages[-1]['content'].strip().splitlines()[-1]
            content = f'Carry on from this point:\\n{last_line}'
            messages.append({'role': 'user', 'content': content})
        else:
            # Enable provider native continue
            kwargs['action'] = 'continue'
        return messages, kwargs
    
    @staticmethod
    def process_bucket_tool(messages: Messages, tool: dict) -> Messages:
        """
        Обрабатывает запросы инструмента bucket.

        Args:
            messages (Messages): Список сообщений.
            tool (dict): Словарь, содержащий информацию об инструменте.

        Returns:
            Messages: Обновленный список сообщений.

        Example:
            >>> messages = [{'role': 'user', 'content': '{"bucket_id":"123"}'}]
            >>> tool = {'function': {}}
            >>> ToolHandler.process_bucket_tool(messages, tool)
            [{'role': 'user', 'content': 'bucket content'}]
        """
        messages = messages.copy()
        
        def on_bucket(match):
            """
            Внутренняя функция для замены bucket_id на содержимое bucket.
            Args:
                match: (re.Match): Результат сопоставления регулярного выражения.
            Returns:
                str: Содержимое bucket.
            """
            return ''.join(read_bucket(get_bucket_dir(match.group(1))))
            
        has_bucket = False
        for message in messages:
            if 'content' in message and isinstance(message['content'], str):
                new_message_content = re.sub(r'{"bucket_id":"([^"]*)"}', on_bucket, message['content'])
                if new_message_content != message['content']:
                    has_bucket = True
                    message['content'] = new_message_content

        last_message_content = messages[-1]['content']      
        if has_bucket and isinstance(last_message_content, str):
            if '\\nSource: ' in last_message_content:
                messages[-1]['content'] = last_message_content + BUCKET_INSTRUCTIONS
                    
        return messages

    @staticmethod
    async def process_tools(messages: Messages, tool_calls: List[dict], provider: Any) -> Tuple[Messages, Sources | None, Dict[str, Any]]:
        """
        Обрабатывает все вызовы инструментов и возвращает обновленные сообщения и kwargs.

        Args:
            messages (Messages): Список сообщений.
            tool_calls (List[dict]): Список вызовов инструментов.
            provider (Any): Провайдер.

        Returns:
            Tuple[Messages, Sources | None, Dict[str, Any]]: Обновленный список сообщений, источники и дополнительные аргументы.

        Example:
            >>> messages = [{'role': 'user', 'content': 'search example'}]
            >>> tool_calls = [{'type': 'function', 'function': {'name': 'search_tool', 'arguments': {'query': 'example'}}}]
            >>> provider = 'TestProvider'
            >>> await ToolHandler.process_tools(messages, tool_calls, provider)
            ([{'role': 'user', 'content': 'example search results'}], None, {})
        """
        if not tool_calls:
            return messages, {}, {}
            
        extra_kwargs = {}
        messages = messages.copy()
        sources = None
        
        for tool in tool_calls:
            if tool.get('type') != 'function':
                continue
                
            function_name = tool.get('function', {}).get('name')
            
            if function_name == TOOL_NAMES['SEARCH']:
                messages, sources = await ToolHandler.process_search_tool(messages, tool)
                
            elif function_name == TOOL_NAMES['CONTINUE']:
                messages, kwargs = ToolHandler.process_continue_tool(messages, tool, provider)
                extra_kwargs.update(kwargs)
                
            elif function_name == TOOL_NAMES['BUCKET']:
                messages = ToolHandler.process_bucket_tool(messages, tool)
                
        return messages, sources, extra_kwargs


class AuthManager:
    """
    Менеджер аутентификации.
    ========================

    Класс AuthManager предназначен для управления API-ключами.
    """
    
    @staticmethod
    def get_api_key_file(cls) -> Path:
        """
        Получает путь к файлу API-ключа для провайдера.

        Args:
            cls: Класс провайдера.

        Returns:
            Path: Путь к файлу API-ключа.

        Example:
            >>> AuthManager.get_api_key_file(MockProvider)
            PosixPath('/path/to/cookies/api_key_MockProvider.json')
        """
        return Path(get_cookies_dir()) / f'api_key_{cls.parent if hasattr(cls, "parent") else cls.__name__}.json'
    
    @staticmethod
    def load_api_key(provider: Any) -> Optional[str]:
        """
        Загружает API-ключ из файла конфигурации, если необходимо.

        Args:
            provider (Any): Провайдер.

        Returns:
            Optional[str]: API-ключ или None, если ключ не требуется или не найден.

        Example:
            >>> AuthManager.load_api_key(MockProvider)
            'test_api_key'
        """
        if not getattr(provider, 'needs_auth', False):
            return None
            
        auth_file = AuthManager.get_api_key_file(provider)
        try:
            if auth_file.exists():
                with auth_file.open('r') as f:
                    auth_result = json.load(f)
                return auth_result.get('api_key')
        except (json.JSONDecodeError, PermissionError, FileNotFoundError) as ex:
            logger.error(f'Failed to load API key: {ex.__class__.__name__}: {ex}', exc_info=True)
        return None


class ThinkingProcessor:
    """
    Обработчик thinking chunks.
    ===========================

    Класс ThinkingProcessor предназначен для обработки "thinking chunks",
    которые указывают на процесс размышления модели.
    """
    
    @staticmethod
    def process_thinking_chunk(chunk: str, start_time: float = 0) -> Tuple[float, List[Union[str, Reasoning]]]:
        """
        Обрабатывает thinking chunk и возвращает время и результаты.

        Args:
            chunk (str): Chunk текста.
            start_time (float, optional): Время начала размышления. По умолчанию 0.

        Returns:
            Tuple[float, List[Union[str, Reasoning]]]: Время и список результатов.

        Example:
            >>> ThinkingProcessor.process_thinking_chunk('<think>example</think>')
            (0, [Reasoning(status='🤔 Is thinking...', is_thinking='<think>'), Reasoning('example'), Reasoning(status='Finished', is_thinking='</think>')])
        """
        results = []
        
        # Handle non-thinking chunk
        if not start_time and '<think>' not in chunk and '</think>' not in chunk:
            return 0, [chunk]
            
        # Handle thinking start
        if '<think>' in chunk and '`<think>`' not in chunk:
            before_think, *after = chunk.split('<think>', 1)
            
            if before_think:
                results.append(before_think)
                
            results.append(Reasoning(status='🤔 Is thinking...', is_thinking='<think>'))
            
            if after:
                if '</think>' in after[0]:
                    after, *after_end = after[0].split('</think>', 1)
                    results.append(Reasoning(after))
                    results.append(Reasoning(status='Finished', is_thinking='</think>'))
                    if after_end:
                        results.append(after_end[0])
                    return 0, results
                else:
                    results.append(Reasoning(after[0]))
                
            return time.time(), results
            
        # Handle thinking end
        if '</think>' in chunk:
            before_end, *after = chunk.split('</think>', 1)
            
            if before_end:
                results.append(Reasoning(before_end))
                
            thinking_duration = time.time() - start_time if start_time > 0 else 0
            
            status = f'Thought for {thinking_duration:.2f}s' if thinking_duration > 1 else 'Finished'
            results.append(Reasoning(status=status, is_thinking='</think>'))
            
            # Make sure to handle text after the closing tag
            if after and after[0].strip():
                results.append(after[0])
                
            return 0, results
            
        # Handle ongoing thinking
        if start_time:
            return start_time, [Reasoning(chunk)]
            
        return start_time, [chunk]


async def perform_web_search(messages: Messages, web_search_param: Any) -> Tuple[Messages, Optional[Sources]]:
    """
    Выполняет поиск в интернете и возвращает обновленные сообщения и источники.

    Args:
        messages (Messages): Список сообщений.
        web_search_param (Any): Параметр поиска в интернете.

    Returns:
        Tuple[Messages, Optional[Sources]]: Обновленный список сообщений и источники.

    Example:
        >>> messages = [{'role': 'user', 'content': 'example'}]
        >>> web_search_param = 'example query'
        >>> await perform_web_search(messages, web_search_param)
        ([{'role': 'user', 'content': 'example search results'}], None)
    """
    messages = messages.copy()
    sources = None
    
    if not web_search_param:
        return messages, sources
        
    try:
        search_query = web_search_param if isinstance(web_search_param, str) and web_search_param != 'true' else None
        messages[-1]['content'], sources = await do_search(messages[-1]['content'], search_query)
    except Exception as ex:
        logger.error(f'Couldn\'t do web search: {ex.__class__.__name__}: {ex}', exc_info=True)
        
    return messages, sources


async def async_iter_run_tools(
    provider: ProviderType, 
    model: str, 
    messages: Messages, 
    tool_calls: Optional[List[dict]] = None, 
    **kwargs
) -> AsyncIterator:
    """
    Асинхронно запускает инструменты и возвращает результаты.

    Args:
        provider (ProviderType): Провайдер.
        model (str): Модель.
        messages (Messages): Список сообщений.
        tool_calls (Optional[List[dict]], optional): Список вызовов инструментов. По умолчанию None.
        **kwargs: Дополнительные аргументы.

    Yields:
        AsyncIterator: Результаты выполнения инструментов.

    Example:
        >>> provider = MockProvider()
        >>> model = 'test_model'
        >>> messages = [{'role': 'user', 'content': 'example'}]
        >>> async for chunk in async_iter_run_tools(provider, model, messages):
        ...     print(chunk)
        example response
    """
    # Process web search
    sources = None
    web_search = kwargs.get('web_search')
    if web_search:
        messages, sources = await perform_web_search(messages, web_search)
    
    # Get API key if needed
    api_key = AuthManager.load_api_key(provider)
    if api_key and 'api_key' not in kwargs:
        kwargs['api_key'] = api_key
    
    # Process tool calls
    if tool_calls:
        messages, sources, extra_kwargs = await ToolHandler.process_tools(messages, tool_calls, provider)
        kwargs.update(extra_kwargs)
    
    # Generate response
    create_function = provider.get_async_create_function()
    response = to_async_iterator(create_function(model=model, messages=messages, **kwargs))
    
    async for chunk in response:
        yield chunk
        
    # Yield sources if available
    if sources:
        yield sources


def iter_run_tools(
    iter_callback: Callable,
    model: str,
    messages: Messages,
    provider: Optional[str] = None,
    tool_calls: Optional[List[dict]] = None,
    **kwargs
) -> Iterator:
    """
    Синхронно запускает инструменты и возвращает результаты.

    Args:
        iter_callback (Callable): Функция обратного вызова для итерации.
        model (str): Модель.
        messages (Messages): Список сообщений.
        provider (Optional[str], optional): Провайдер. По умолчанию None.
        tool_calls (Optional[List[dict]], optional): Список вызовов инструментов. По умолчанию None.
        **kwargs: Дополнительные аргументы.

    Yields:
        Iterator: Результаты выполнения инструментов.

    Example:
        >>> def mock_iter_callback(**kwargs):
        ...     yield 'example response'
        >>> model = 'test_model'
        >>> messages = [{'role': 'user', 'content': 'example'}]
        >>> for chunk in iter_run_tools(mock_iter_callback, model, messages):
        ...     print(chunk)
        example response
    """
    # Process web search
    web_search = kwargs.get('web_search')
    sources = None
    
    if web_search:
        try:
            messages = messages.copy()
            search_query = web_search if isinstance(web_search, str) and web_search != 'true' else None
            # Note: Using asyncio.run inside sync function is not ideal, but maintaining original pattern
            messages[-1]['content'], sources = asyncio.run(do_search(messages[-1]['content'], search_query))
        except Exception as ex:
            logger.error(f'Couldn\'t do web search: {ex.__class__.__name__}: {ex}', exc_info=True)
    
    # Get API key if needed
    if provider is not None and getattr(provider, 'needs_auth', False) and 'api_key' not in kwargs:
        api_key = AuthManager.load_api_key(provider)
        if api_key:
            kwargs['api_key'] = api_key
    
    # Process tool calls
    if tool_calls:
        for tool in tool_calls:
            if tool.get('type') == 'function':
                function_name = tool.get('function', {}).get('name')
                
                if function_name == TOOL_NAMES['SEARCH']:
                    tool['function']['arguments'] = ToolHandler.validate_arguments(tool['function'])
                    messages[-1]['content'] = get_search_message(
                        messages[-1]['content'],
                        raise_search_exceptions=True,
                        **tool['function']['arguments']
                    )
                elif function_name == TOOL_NAMES['CONTINUE']:
                    if provider not in ('OpenaiAccount', 'HuggingFace'):
                        last_line = messages[-1]['content'].strip().splitlines()[-1]
                        content = f'Carry on from this point:\\n{last_line}'
                        messages.append({'role': 'user', 'content': content})
                    else:
                        # Enable provider native continue
                        kwargs['action'] = 'continue'
                elif function_name == TOOL_NAMES['BUCKET']:
                    def on_bucket(match):
                        """
                        Внутренняя функция для замены bucket_id на содержимое bucket.
                        Args:
                            match: (re.Match): Результат сопоставления регулярного выражения.
                        Returns:
                            str: Содержимое bucket.
                        """
                        return ''.join(read_bucket(get_bucket_dir(match.group(1))))
                    has_bucket = False
                    for message in messages:
                        if 'content' in message and isinstance(message['content'], str):
                            new_message_content = re.sub(r'{"bucket_id":"([^"]*)"}', on_bucket, message['content'])
                            if new_message_content != message['content']:
                                has_bucket = True
                                message['content'] = new_message_content
                    last_message = messages[-1]['content']
                    if has_bucket and isinstance(last_message, str):
                        if '\\nSource: ' in last_message:
                            messages[-1]['content'] = last_message + BUCKET_INSTRUCTIONS
    
    # Process response chunks
    thinking_start_time = 0
    processor = ThinkingProcessor()
    
    for chunk in iter_callback(model=model, messages=messages, provider=provider, **kwargs):
        if isinstance(chunk, FinishReason):
            if sources is not None:
                yield sources
                sources = None
            yield chunk
            continue
        elif isinstance(chunk, Sources):
            sources = None
        if not isinstance(chunk, str):
            yield chunk
            continue
            
        thinking_start_time, results = processor.process_thinking_chunk(chunk, thinking_start_time)
        
        for result in results:
            yield result

    if sources is not None:
        yield sources