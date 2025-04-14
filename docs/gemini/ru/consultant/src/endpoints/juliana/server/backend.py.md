### **Анализ кода модуля `backend.py`**

**Качество кода:**

- **Соответствие стандартам**: 5/10
- **Плюсы**:
    - Код структурирован в классы и функции, что облегчает понимание общей логики.
    - Использование `threading` для обновления прокси позволяет выполнять эту задачу в фоновом режиме.
- **Минусы**:
    - Отсутствуют аннотации типов для параметров функций и переменных.
    - Не используется модуль `logger` для логирования ошибок.
    - Не все функции имеют docstring, отсутствует описание возвращаемых значений и исключений.
    - Использование `print` для вывода информации об ошибках вместо `logger.error`.
    - Не обрабатываются все возможные исключения, что может привести к непредсказуемому поведению.
    - Не используется `j_loads` или `j_loads_ns` для чтения JSON.
    - Не используются одинарные кавычки.
    - Присутствуют необработанные исключения, что может привести к сбою сервера.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех параметров функций и переменных. Это улучшит читаемость и поможет избежать ошибок.
2.  **Использовать `logger` для логирования**:
    - Заменить `print` на `logger.info`, `logger.warning` и `logger.error` для логирования информации, предупреждений и ошибок соответственно.
3.  **Добавить docstring для всех функций**:
    - Добавить docstring для всех функций, чтобы объяснить их назначение, параметры и возвращаемые значения.
4.  **Обработка исключений**:
    - Добавить обработку исключений для всех возможных ошибок, чтобы избежать непредсказуемого поведения.
    - Использовать `logger.error` для логирования ошибок и передачи информации об исключении.
5.  **Использовать `j_loads` или `j_loads_ns`**:
    - Заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns` для чтения JSON или конфигурационных файлов.
6.  **Использовать одинарные кавычки**:
    - Заменить двойные кавычки на одинарные.
7.  **Улучшить читаемость кода**:
    - Добавить пробелы вокруг операторов присваивания для повышения читаемости.
8.  **Документация и комментарии**:
    - Добавить подробные комментарии для всех ключевых участков кода, объясняющие их назначение.
9.  **Использовать webdriver**:
    - Использовать webdriver из модуля `src.webdriver` проекта `hypotez`.
10. **Перевести docstring на русский язык**
    - Сделать переводы всех docstring с английского языка на русский.
11. **Улучшить обработку прокси**:
    - Добавить логирование ошибок при обновлении прокси.
    - Улучшить обработку прокси, чтобы избежать проблем с подключением.
12. **Заменить множественный импорт на отдельные строки**:
    - Разделить множественный импорт в начале файла на отдельные строки для улучшения читаемости.

**Оптимизированный код:**

```python
import os
import time
import json
import random
import threading
import re
from typing import Optional, List, Dict, Any

from googletrans import Translator
from flask import Flask, request
from datetime import datetime
from requests import get

from src.logger import logger
# from src.webdirver import Driver, Chrome, Firefox, Playwright

class Backend_Api:
    """
    API для обработки запросов к backend.

    Args:
        app (Flask): Flask-приложение.
        config (dict): Конфигурация приложения.

    """
    def __init__(self, app: Flask, config: Dict[str, Any]) -> None:
        """
        Инициализация API.

        Args:
            app (Flask): Flask-приложение.
            config (dict): Конфигурация приложения.
        """
        self.app = app
        self.use_auto_proxy = config['use_auto_proxy']
        self.routes = {
            '/backend-api/v2/conversation': {
                'function': self._conversation,
                'methods': ['POST']
            }
        }

        if self.use_auto_proxy:
            update_proxies = threading.Thread(
                target=update_working_proxies, daemon=True)
            update_proxies.start()

    def _conversation(self) -> Any:
        """
        Обрабатывает запрос на разговор.

        Получает параметры из JSON-запроса, такие как `stream`, `jailbreak`, `model` и `messages`,
        затем генерирует ответ с использованием ChatCompletion.create. Если происходит ошибка,
        она логируется и возвращается сообщение об ошибке.

        Returns:
            Flask.Response: Streaming-ответ или JSON-ответ с информацией об ошибке.

        Raises:
            Exception: Если возникает ошибка при обработке запроса.
        """
        try:
            streaming: bool = request.json.get('stream', True)
            jailbreak: str = request.json['jailbreak']
            model: str = request.json['model']
            messages: List[Dict[str, str]] = build_messages(jailbreak)

            #random_proxy = get_random_proxy() # получаем случайный прокси
            #proxies = {"http": random_proxy, "https": random_proxy} # создаем словарь с прокси

            # Generate response
            response = ChatCompletion.create(model=model,
                                             messages=messages)
            #if 'curl_cffi.requests.errors.RequestsError' in response:
            #        response = ChatCompletion.create(model=model, stream=False,
            #                                         messages=messages)

            return self.app.response_class(generate_stream(response, jailbreak), mimetype='text/event-stream')

        except Exception as ex:
            logger.error('Ошибка при обработке запроса', ex, exc_info=True)
            return {
                '_action': '_ask',
                'success': False,
                "error": f"Произошла ошибка: {str(ex)}"
            }, 400


def build_messages(jailbreak: str) -> List[Dict[str, str]]:
    """
    Строит список сообщений для разговора.

    Извлекает данные из JSON-запроса, такие как `conversation`, `internet_access` и `prompt`,
    затем генерирует системное сообщение, добавляет существующий разговор, результаты веб-поиска (если разрешено)
    и инструкции jailbreak (если разрешено). В конце добавляет prompt и обрезает разговор до последних 13 сообщений.

    Args:
        jailbreak (str): Инструкции для "взлома" (jailbreak).

    Returns:
        List[Dict[str, str]]: Список сообщений для разговора.
    """
    _conversation: List[Dict[str, str]] = request.json['meta']['content']['conversation']
    internet_access: bool = request.json['meta']['content']['internet_access']
    prompt: Dict[str, str] = request.json['meta']['content']['parts'][0]

    # Generate system message
    current_date: str = datetime.now().strftime("%Y-%m-%d")
    system_message: str = (
        f'You are ChatGPT also known as ChatGPT, a large language model trained by OpenAI. '
        f'Strictly follow the users instructions. '
        f'Current date: {current_date}. '
        f'{set_response_language(prompt)}'
    )

    # Initialize the conversation with the system message
    conversation: List[Dict[str, str]] = [{'role': 'system', 'content': system_message}]

    # Add the existing conversation
    conversation += _conversation

    # Add web results if enabled
    conversation += fetch_search_results(
        prompt["content"]) if internet_access else []

    # Add jailbreak instructions if enabled
    if jailbreak_instructions := isJailbreak(jailbreak):
        conversation += jailbreak_instructions

    # Add the prompt
    conversation += [prompt]

    # Reduce conversation size to avoid API Token quantity error
    conversation: List[Dict[str, str]] = conversation[-13:] if len(conversation) > 12 else conversation

    return conversation


def fetch_search_results(query: str) -> List[Dict[str, str]]:
    """
    Получает результаты поиска из DuckDuckGo API.

    Отправляет запрос к API DuckDuckGo для поиска заданного запроса, ограничивает количество результатов
    до 5 и форматирует результаты в список сообщений для разговора.

    Args:
        query (str): Поисковой запрос.

    Returns:
        List[Dict[str, str]]: Список сообщений с результатами поиска.
    """
    search = get('https://ddg-api.herokuapp.com/search',
                 params={
                     'query': query,
                     'limit': 5,
                 })

    results: List[Dict[str, str]] = []
    snippets: str = ""
    for index, result in enumerate(search.json()):
        snippet: str = f'[{index + 1}] "{result["snippet"]}" URL:{result["link"]}.'
        snippets += snippet
    results.append({'role': 'system', 'content': snippets})

    return results


def generate_stream(response: Any, jailbreak: str) -> Any:
    """
    Генерирует поток сообщений на основе ответа.

    В зависимости от того, включены ли инструкции jailbreak, генерирует поток сообщений,
    проверяя, успешно ли выполнен "взлом", и возвращает соответствующие сообщения.

    Args:
        response (Any): Ответ от API.
        jailbreak (str): Инструкции для "взлома" (jailbreak).

    Yields:
        Any: Сообщения из потока.
    """
    if isJailbreak(jailbreak):
        response_jailbreak: str = ''
        jailbroken_checked: bool = False
        for message in response:
            response_jailbreak += message
            if jailbroken_checked:
                yield message
            else:
                if response_jailbroken_success(response_jailbreak):
                    jailbroken_checked = True
                if response_jailbroken_failed(response_jailbreak):
                    yield response_jailbreak
                    jailbroken_checked = True
    else:
        yield from response


def response_jailbroken_success(response: str) -> bool:
    """
    Проверяет, успешно ли выполнен "взлом".

    Ищет в ответе строку 'ACT:', чтобы определить, успешно ли выполнен "взлом".

    Args:
        response (str): Ответ от API.

    Returns:
        bool: True, если "взлом" успешен, иначе False.
    """
    act_match = re.search(r'ACT:', response, flags=re.DOTALL)
    return bool(act_match)


def response_jailbroken_failed(response: str) -> bool:
    """
    Проверяет, не удалось ли выполнить "взлом".

    Определяет, не удалось ли выполнить "взлом", проверяя, начинается ли ответ со строк "GPT:" или "ACT:".

    Args:
        response (str): Ответ от API.

    Returns:
        bool: True, если "взлом" не удался, иначе False.
    """
    return False if len(response) < 4 else not (response.startswith("GPT:") or response.startswith("ACT:"))


def set_response_language(prompt: Dict[str, str]) -> str:
    """
    Определяет язык ответа на основе языка запроса.

    Использует Google Translate API для определения языка запроса и возвращает строку,
    указывающую, на каком языке должен быть ответ.

    Args:
        prompt (Dict[str, str]): Запрос.

    Returns:
        str: Строка, указывающая язык ответа.
    """
    translator = Translator()
    detected_language = translator.detect(prompt['content']).lang
    return f"You will respond in the language: {detected_language}. "


def isJailbreak(jailbreak: str) -> Optional[List[Dict[str, str]]]:
    """
    Определяет, включены ли инструкции jailbreak.

    Если jailbreak не "Default", возвращает соответствующие инструкции из словаря `special_instructions`.

    Args:
        jailbreak (str): Инструкции для "взлома" (jailbreak).

    Returns:
        Optional[List[Dict[str, str]]]: Список инструкций jailbreak или None, если jailbreak "Default".
    """
    if jailbreak != "Default":
        return special_instructions[jailbreak] if jailbreak in special_instructions else None
    else:
        return None