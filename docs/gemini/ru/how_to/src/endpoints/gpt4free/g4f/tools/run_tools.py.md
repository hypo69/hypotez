### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет инструменты для обработки различных задач, включая веб-поиск, продолжение разговора и работу с "bucket". Он содержит классы для управления API ключами и обработки "thinking" чанков, а также асинхронные и синхронные функции для запуска этих инструментов.

Шаги выполнения
-------------------------
1. **Определение класса `ToolHandler`**:
   - Класс содержит статические методы для обработки различных типов инструментов.
   - Метод `validate_arguments` проверяет и разбирает аргументы инструментов. Если аргументы представлены в виде строки JSON, они преобразуются в словарь Python.

2. **Обработка инструмента поиска (`process_search_tool`)**:
   - Метод `process_search_tool` асинхронно выполняет поиск в интернете на основе контента сообщения и аргументов инструмента.
   - Результаты поиска и источники добавляются в сообщение.

3. **Обработка инструмента продолжения (`process_continue_tool`)**:
   - Метод `process_continue_tool` подготавливает сообщение для продолжения разговора.
   - Для определенных провайдеров (не "OpenaiAccount" и "HuggingFaceAPI") добавляет последнюю строку сообщения в новый запрос.

4. **Обработка инструмента bucket (`process_bucket_tool`)**:
   - Метод `process_bucket_tool` заменяет идентификаторы bucket в сообщениях контентом из соответствующих bucket.
   - Добавляет инструкции по использованию источников, если в сообщении есть bucket и источники.

5. **Обработка инструментов (`process_tools`)**:
   - Метод `process_tools` выполняет итерацию по списку вызовов инструментов (`tool_calls`).
   - Вызывает соответствующие методы обработки инструментов (`process_search_tool`, `process_continue_tool`, `process_bucket_tool`) в зависимости от имени функции инструмента.

6. **Управление API ключами (`AuthManager`)**:
   - Класс `AuthManager` управляет загрузкой API ключей из файлов конфигурации.
   - Метод `load_api_key` загружает API ключ из файла, если провайдеру требуется аутентификация.

7. **Обработка "thinking" чанков (`ThinkingProcessor`)**:
   - Класс `ThinkingProcessor` обрабатывает чанки, содержащие теги `<think>` и `</think>`.
   - Метод `process_thinking_chunk` извлекает информацию о времени, затраченном на "размышление", и возвращает результаты.

8. **Выполнение веб-поиска (`perform_web_search`)**:
   - Функция `perform_web_search` выполняет поиск в интернете и возвращает обновленные сообщения и источники.
   - Использует `do_search` для выполнения поиска на основе запроса.

9. **Асинхронный запуск инструментов (`async_iter_run_tools`)**:
   - Функция `async_iter_run_tools` асинхронно запускает инструменты и возвращает результаты.
   - Сначала выполняет веб-поиск, затем загружает API ключ (если необходимо) и обрабатывает вызовы инструментов.

10. **Синхронный запуск инструментов (`iter_run_tools`)**:
    - Функция `iter_run_tools` синхронно запускает инструменты и возвращает результаты.
    - Сначала выполняет веб-поиск, затем загружает API ключ (если необходимо) и обрабатывает вызовы инструментов.
    - Использует `ThinkingProcessor` для обработки "thinking" чанков.

Пример использования
-------------------------

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
from .. import debug

# Constants
BUCKET_INSTRUCTIONS = """
Instruction: Make sure to add the sources of cites using [[domain]](Url) notation after the reference. Example: [[a-z0-9.]](http://example.com)
"""

TOOL_NAMES = {
    "SEARCH": "search_tool",
    "CONTINUE": "continue_tool",
    "BUCKET": "bucket_tool"
}

class ToolHandler:
    """Handles processing of different tool types"""
    
    @staticmethod
    def validate_arguments(data: dict) -> dict:
        """Validate and parse tool arguments"""
        if "arguments" in data:
            if isinstance(data["arguments"], str):
                data["arguments"] = json.loads(data["arguments"])
            if not isinstance(data["arguments"], dict):
                raise ValueError("Tool function arguments must be a dictionary or a json string")
            else:
                return filter_none(**data["arguments"])
        else:
            return {}
            
    @staticmethod
    async def process_search_tool(messages: Messages, tool: dict) -> Messages:
        """Process search tool requests"""
        messages = messages.copy()
        args = ToolHandler.validate_arguments(tool["function"])
        messages[-1]["content"], sources = await do_search(
            messages[-1]["content"],
            **args
        )
        return messages, sources
    
    @staticmethod
    def process_continue_tool(messages: Messages, tool: dict, provider: Any) -> Tuple[Messages, Dict[str, Any]]:
        """Process continue tool requests"""
        kwargs = {}
        if provider not in ("OpenaiAccount", "HuggingFaceAPI"):
            messages = messages.copy()
            last_line = messages[-1]["content"].strip().splitlines()[-1]
            content = f"Carry on from this point:\\n{last_line}"
            messages.append({"role": "user", "content": content})
        else:
            # Enable provider native continue
            kwargs["action"] = "continue"
        return messages, kwargs
    
    @staticmethod
    def process_bucket_tool(messages: Messages, tool: dict) -> Messages:
        """Process bucket tool requests"""
        messages = messages.copy()
        
        def on_bucket(match):
            return "".join(read_bucket(get_bucket_dir(match.group(1))))
            
        has_bucket = False
        for message in messages:
            if "content" in message and isinstance(message["content"], str):
                new_message_content = re.sub(r'{"bucket_id":"([^"]*)"}\', on_bucket, message["content"])\
                if new_message_content != message["content"]:
                    has_bucket = True
                    message["content"] = new_message_content

        last_message_content = messages[-1]["content"]      
        if has_bucket and isinstance(last_message_content, str):
            if "\\nSource: " in last_message_content:
                messages[-1]["content"] = last_message_content + BUCKET_INSTRUCTIONS
                    
        return messages

    @staticmethod
    async def process_tools(messages: Messages, tool_calls: List[dict], provider: Any) -> Tuple[Messages, Dict[str, Any]]:
        """Process all tool calls and return updated messages and kwargs"""
        if not tool_calls:
            return messages, {}
            
        extra_kwargs = {}
        messages = messages.copy()
        sources = None
        
        for tool in tool_calls:
            if tool.get("type") != "function":
                continue
                
            function_name = tool.get("function", {}).get("name")
            
            if function_name == TOOL_NAMES["SEARCH"]:\
                messages, sources = await ToolHandler.process_search_tool(messages, tool)
                
            elif function_name == TOOL_NAMES["CONTINUE"]:\
                messages, kwargs = ToolHandler.process_continue_tool(messages, tool, provider)\
                extra_kwargs.update(kwargs)\
                
            elif function_name == TOOL_NAMES["BUCKET"]:\
                messages = ToolHandler.process_bucket_tool(messages, tool)
                
        return messages, sources, extra_kwargs


class AuthManager:
    """Handles API key management"""
    
    @staticmethod
    def get_api_key_file(cls) -> Path:
        """Get the path to the API key file for a provider"""
        return Path(get_cookies_dir()) / f"api_key_{cls.parent if hasattr(cls, 'parent') else cls.__name__}.json"
    
    @staticmethod
    def load_api_key(provider: Any) -> Optional[str]:
        """Load API key from config file if needed"""
        if not getattr(provider, "needs_auth", False):
            return None
            
        auth_file = AuthManager.get_api_key_file(provider)
        try:
            if auth_file.exists():
                with auth_file.open("r") as f:\
                    auth_result = json.load(f)
                return auth_result.get("api_key")
        except (json.JSONDecodeError, PermissionError, FileNotFoundError) as e:
            debug.error(f"Failed to load API key: {e.__class__.__name__}: {e}")
        return None


class ThinkingProcessor:
    """Processes thinking chunks"""
    
    @staticmethod
    def process_thinking_chunk(chunk: str, start_time: float = 0) -> Tuple[float, List[Union[str, Reasoning]]]:
        """Process a thinking chunk and return timing and results."""
        results = []
        
        # Handle non-thinking chunk
        if not start_time and "<think>" not in chunk and "</think>" not in chunk:
            return 0, [chunk]
            
        # Handle thinking start
        if "<think>" in chunk and "`<think>`" not in chunk:
            before_think, *after = chunk.split("<think>", 1)
            
            if before_think:
                results.append(before_think)
                
            results.append(Reasoning(status="🤔 Is thinking...", is_thinking="<think>"))
            
            if after:
                if "</think>" in after[0]:
                    after, *after_end = after[0].split("</think>", 1)
                    results.append(Reasoning(after))
                    results.append(Reasoning(status="Finished", is_thinking="</think>"))
                    if after_end:
                        results.append(after_end[0])
                    return 0, results
                else:
                    results.append(Reasoning(after[0]))
                
            return time.time(), results
            
        # Handle thinking end
        if "</think>" in chunk:
            before_end, *after = chunk.split("</think>", 1)
            
            if before_end:
                results.append(Reasoning(before_end))
                
            thinking_duration = time.time() - start_time if start_time > 0 else 0
            
            status = f"Thought for {thinking_duration:.2f}s" if thinking_duration > 1 else "Finished"
            results.append(Reasoning(status=status, is_thinking="</think>"))
            
            # Make sure to handle text after the closing tag
            if after and after[0].strip():
                results.append(after[0])
                
            return 0, results
            
        # Handle ongoing thinking
        if start_time:\
            return start_time, [Reasoning(chunk)]
            
        return start_time, [chunk]


async def perform_web_search(messages: Messages, web_search_param: Any) -> Tuple[Messages, Optional[Sources]]:
    """Perform web search and return updated messages and sources"""
    messages = messages.copy()
    sources = None
    
    if not web_search_param:
        return messages, sources
        
    try:
        search_query = web_search_param if isinstance(web_search_param, str) and web_search_param != "true" else None
        messages[-1]["content"], sources = await do_search(messages[-1]["content"], search_query)
    except Exception as e:
        debug.error(f"Couldn\'t do web search: {e.__class__.__name__}: {e}")
        
    return messages, sources


async def async_iter_run_tools(
    provider: ProviderType, 
    model: str, 
    messages: Messages, 
    tool_calls: Optional[List[dict]] = None, 
    **kwargs
) -> AsyncIterator:\
    """Asynchronously run tools and yield results"""
    # Process web search
    sources = None
    web_search = kwargs.get('web_search')
    if web_search:\
        messages, sources = await perform_web_search(messages, web_search)
    
    # Get API key if needed
    api_key = AuthManager.load_api_key(provider)
    if api_key and "api_key" not in kwargs:
        kwargs["api_key"] = api_key
    
    # Process tool calls
    if tool_calls:\
        messages, sources, extra_kwargs = await ToolHandler.process_tools(messages, tool_calls, provider)
        kwargs.update(extra_kwargs)
    
    # Generate response
    create_function = provider.get_async_create_function()
    response = to_async_iterator(create_function(model=model, messages=messages, **kwargs))
    
    async for chunk in response:\
        yield chunk
        
    # Yield sources if available
    if sources:\
        yield sources


def iter_run_tools(
    iter_callback: Callable,
    model: str,
    messages: Messages,
    provider: Optional[str] = None,
    tool_calls: Optional[List[dict]] = None,
    **kwargs
) -> Iterator:\
    """Run tools synchronously and yield results"""
    # Process web search
    web_search = kwargs.get('web_search')
    sources = None
    
    if web_search:
        try:
            messages = messages.copy()
            search_query = web_search if isinstance(web_search, str) and web_search != "true" else None
            # Note: Using asyncio.run inside sync function is not ideal, but maintaining original pattern
            messages[-1]["content"], sources = asyncio.run(do_search(messages[-1]["content"], search_query))
        except Exception as e:
            debug.error(f"Couldn\'t do web search: {e.__class__.__name__}: {e}")
    
    # Get API key if needed
    if provider is not None and getattr(provider, "needs_auth", False) and "api_key" not in kwargs:\
        api_key = AuthManager.load_api_key(provider)
        if api_key:
            kwargs["api_key"] = api_key
    
    # Process tool calls
    if tool_calls:\
        for tool in tool_calls:
            if tool.get("type") == "function":
                function_name = tool.get("function", {}).get("name")
                
                if function_name == TOOL_NAMES["SEARCH"]:\
                    tool["function"]["arguments"] = ToolHandler.validate_arguments(tool["function"])
                    messages[-1]["content"] = get_search_message(
                        messages[-1]["content"],\
                        raise_search_exceptions=True,
                        **tool["function"]["arguments"]\
                    )
                elif function_name == TOOL_NAMES["CONTINUE"]:\
                    if provider not in ("OpenaiAccount", "HuggingFace"):\
                        last_line = messages[-1]["content"].strip().splitlines()[-1]
                        content = f"Carry on from this point:\\n{last_line}"
                        messages.append({"role": "user", "content": content})
                    else:
                        # Enable provider native continue
                        kwargs["action"] = "continue"
                elif function_name == TOOL_NAMES["BUCKET"]:\
                    def on_bucket(match):\
                        return "".join(read_bucket(get_bucket_dir(match.group(1))))
                    has_bucket = False
                    for message in messages:\
                        if "content" in message and isinstance(message["content"], str):\
                            new_message_content = re.sub(r'{"bucket_id":"([^"]*)"}\', on_bucket, message["content"])
                            if new_message_content != message["content"]:
                                has_bucket = True
                                message["content"] = new_message_content
                    last_message = messages[-1]["content"]
                    if has_bucket and isinstance(last_message, str):
                        if "\\nSource: " in last_message:
                            messages[-1]["content"] = last_message + BUCKET_INSTRUCTIONS
    
    # Process response chunks
    thinking_start_time = 0
    processor = ThinkingProcessor()
    
    for chunk in iter_callback(model=model, messages=messages, provider=provider, **kwargs):\
        if isinstance(chunk, FinishReason):\
            if sources is not None:
                yield sources
                sources = None
            yield chunk
            continue
        elif isinstance(chunk, Sources):\
            sources = None
        if not isinstance(chunk, str):
            yield chunk
            continue
            
        thinking_start_time, results = processor.process_thinking_chunk(chunk, thinking_start_time)
        
        for result in results:\
            yield result

    if sources is not None:\
        yield sources