### **Анализ кода модуля `backend.py`**

## \file /hypotez/src/endpoints/freegpt-webui-ru/server/backend.py

Модуль содержит API для взаимодействия с FreeGPT WebUI на русском языке, включая обработку запросов к моделям G4F, поддержку прокси и управление диалогами.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Организована структура API через класс `Backend_Api`.
    - Использование потоков для обновления прокси.
    - Обработка ошибок с возвратом информации об ошибке.
- **Минусы**:
    - Отсутствие документации и подробных комментариев.
    - Использование устаревшего стиля логирования через `print` вместо `logger`.
    - Не все переменные и параметры аннотированы типами.
    - Не используется `j_loads` для чтения конфигурационных файлов.
    - Смешанный стиль кавычек (используются и двойные, и одинарные).
    - Отсутствие обработки возможных исключений при запросах к внешним API (например, `ddg-api`).

**Рекомендации по улучшению:**

1.  **Добавить документацию**:
    *   Добавить docstring к классам и функциям, описывающие их назначение, аргументы и возвращаемые значения.
    *   Включить примеры использования функций.

2.  **Использовать логирование**:
    *   Заменить `print` на `logger` из модуля `src.logger`.

3.  **Добавить аннотации типов**:
    *   Добавить аннотации типов для всех переменных и параметров функций.

4.  **Использовать `j_loads`**:
    *   Для чтения конфигурационных файлов заменить стандартное использование `open` и `json.load` на `j_loads`.

5.  **Унифицировать кавычки**:
    *   Использовать только одинарные кавычки (`'`) в Python-коде.

6.  **Обработка исключений**:
    *   Добавить обработку возможных исключений при запросах к внешним API (например, `ddg-api`).

7.  **Рефакторинг**:
    *   Разбить функцию `build_messages` на более мелкие, чтобы повысить читаемость и упростить тестирование.
    *   Улучшить обработку jailbreak, сделав ее более гибкой и менее подверженной ошибкам.
    *   Удалить закомментированный код или добавить объяснения, почему он был закомментирован.

**Оптимизированный код:**

```python
import os
import time
import json
import random
import threading
import re
from typing import Optional, List, Dict
import g4f
from g4f import ChatCompletion
from googletrans import Translator
from flask import Flask, request, Response
from datetime import datetime
from requests import get, Response as RequestsResponse
from server.auto_proxy import get_random_proxy, update_working_proxies
from server.config import special_instructions
from src.logger import logger
from pathlib import Path


class Backend_Api:
    """
    API для взаимодействия с FreeGPT WebUI.

    Предоставляет endpoint для обработки диалогов с использованием моделей G4F,
    поддержку автоматической смены прокси и другие функции.

    Args:
        app (Flask): Flask-приложение.
        config (dict): Конфигурация приложения.

    Example:
        >>> app = Flask(__name__)
        >>> config = {'use_auto_proxy': True}
        >>> backend_api = Backend_Api(app, config)
    """

    def __init__(self, app: Flask, config: dict) -> None:
        """
        Инициализация API.

        Args:
            app (Flask): Flask-приложение.
            config (dict): Конфигурация приложения.
        """
        self.app = app
        self.use_auto_proxy: bool = config['use_auto_proxy']
        self.routes: Dict[str, dict] = {
            '/backend-api/v2/conversation': {
                'function': self._conversation,
                'methods': ['POST']
            }
        }

        if self.use_auto_proxy:
            update_proxies: threading.Thread = threading.Thread(
                target=update_working_proxies, daemon=True)
            update_proxies.start()

    def _conversation(self) -> Response | tuple[dict, int]:
        """
        Обрабатывает запрос на создание диалога.

        Извлекает параметры из запроса, формирует сообщение для модели,
        получает ответ от модели и возвращает его в формате stream.

        Returns:
            Response | tuple[dict, int]: Stream ответа или сообщение об ошибке.
        """
        try:
            streaming: bool = request.json.get('stream', True)
            jailbreak: str = request.json['jailbreak']
            model: str = request.json['model']
            messages: list[dict] = build_messages(jailbreak)

            # random_proxy = get_random_proxy() # получаем случайный прокси
            # proxies = {"http": random_proxy, "https": random_proxy} # создаем словарь с прокси

            # Generate response
            response: str = ChatCompletion.create(model=model,
                                                 messages=messages)
            # if 'curl_cffi.requests.errors.RequestsError' in response:
            #        response = ChatCompletion.create(model=model, stream=False,
            #                                         messages=messages)

            return self.app.response_class(generate_stream(response, jailbreak), mimetype='text/event-stream')

        except Exception as ex:
            logger.error('Ошибка при обработке запроса conversation', ex, exc_info=True)
            return {
                '_action': '_ask',
                'success': False,
                "error": f"an error occurred {str(ex)}"
            }, 400


def build_messages(jailbreak: str) -> list[dict]:
    """
    Формирует список сообщений для отправки в модель.

    Собирает системное сообщение, историю разговора, результаты поиска в интернете (если разрешено)
    и инструкции для jailbreak (если включено).

    Args:
        jailbreak (str): Название jailbreak.

    Returns:
        list[dict]: Список сообщений для модели.
    """
    _conversation: list[dict] = request.json['meta']['content']['conversation']
    internet_access: bool = request.json['meta']['content']['internet_access']
    prompt: dict = request.json['meta']['content']['parts'][0]

    # Generate system message
    current_date: str = datetime.now().strftime("%Y-%m-%d")
    system_message: str = (
        f'You are ChatGPT also known as ChatGPT, a large language model trained by OpenAI. '
        f'Strictly follow the users instructions. '
        f'Current date: {current_date}. '
        f'{set_response_language(prompt)}'
    )

    # Initialize the conversation with the system message
    conversation: list[dict] = [{'role': 'system', 'content': system_message}]

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
    conversation: list[dict] = conversation[-13:] if len(
        conversation) > 12 else conversation

    return conversation


def fetch_search_results(query: str) -> list[dict]:
    """
    Выполняет поиск в интернете и возвращает результаты.

    Использует DuckDuckGo API для поиска информации в интернете.

    Args:
        query (str): Поисковой запрос.

    Returns:
        list[dict]: Список результатов поиска.
    """
    try:
        search: RequestsResponse = get(
            'https://ddg-api.herokuapp.com/search',
            params={
                'query': query,
                'limit': 5,
            })
        search.raise_for_status()  # Проверка на HTTP ошибки

        results: list[dict] = []
        snippets: str = ""
        for index, result in enumerate(search.json()):
            snippet: str = f'[{index + 1}] "{result["snippet"]}" URL:{result["link"]}.'
            snippets += snippet
        results.append({'role': 'system', 'content': snippets})

        return results
    except Exception as ex:
        logger.error('Ошибка при выполнении поиска', ex, exc_info=True)
        return []


def generate_stream(response: str, jailbreak: str) -> iter:
    """
    Генерирует stream сообщений на основе ответа.

    Args:
        response (str): Ответ от модели.
        jailbreak (str): Название jailbreak.

    Yields:
        str: Часть сообщения для stream.
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
    Проверяет, успешно ли выполнен jailbreak.

    Args:
        response (str): Ответ от модели.

    Returns:
        bool: True, если jailbreak выполнен успешно, иначе False.
    """
    act_match: re.Match | None = re.search(r'ACT:', response, flags=re.DOTALL)
    return bool(act_match)


def response_jailbroken_failed(response: str) -> bool:
    """
    Проверяет, не провален ли jailbreak.

    Args:
        response (str): Ответ от модели.

    Returns:
        bool: True, если jailbreak провален, иначе False.
    """
    return False if len(response) < 4 else not (response.startswith("GPT:") or response.startswith("ACT:"))


def set_response_language(prompt: dict) -> str:
    """
    Определяет язык ответа на основе языка запроса.

    Args:
        prompt (dict): Запрос пользователя.

    Returns:
        str: Строка с указанием языка для ответа.
    """
    translator: Translator = Translator()
    detected_language: str = translator.detect(prompt['content']).lang
    return f"You will respond in the language: {detected_language}. "


def isJailbreak(jailbreak: str) -> Optional[list[dict]]:
    """
    Проверяет, является ли jailbreak допустимым.

    Args:
        jailbreak (str): Название jailbreak.

    Returns:
        Optional[list[dict]]: Инструкции для jailbreak, если он допустим, иначе None.
    """
    if jailbreak != "Default":
        return special_instructions[jailbreak] if jailbreak in special_instructions else None
    else:
        return None