## \file src/llm/gemini/gemini_client.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль клиента для взаимодействия с Google Gemini API
=======================================================

Модуль предоставляет простой интерфейс для отправки запросов
к модели Gemini через метод `ask()`.

Пример использования
--------------------

Пример синхронного запроса:

.. code-block:: python

    client = GeminiClient()
    response = client.ask('Что такое искусственный интеллект?')
    print(response)

Пример с контекстом (RAG):

.. code-block:: python

    context = ['Компания основана в 2020 году', 'Основной продукт - ИИ помощник']
    response = client.ask('Когда основана компания?', context=context)
    print(response)

.. module:: src.llm.gemini.gemini_client
"""

import header
from header import __root__
from src import gs
from src.logger import logger
from src.utils.printer import pprint as print

from pathlib import Path
from typing import Optional, List, Union

from src.llm.gemini.gemini import GoogleGenerativeAi
from src.utils.jjson import j_loads_ns
from types import SimpleNamespace


class GeminiClient:
    """
    Клиент для взаимодействия с Google Gemini API.

    Класс предоставляет упрощённый интерфейс для работы с моделью Gemini
    через метод `ask()` без сохранения истории диалога.

    Attributes:
        model (GoogleGenerativeAi): Экземпляр класса для работы с Gemini API.
        api_key (str): API ключ для доступа к сервису.
        model_name (str): Название используемой модели.
        system_instruction (Optional[str]): Системная инструкция для модели.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        system_instruction: Optional[str] = None,
        generation_config: Optional[dict] = None
    ):
        """
        Инициализация клиента Gemini.

        Функция загружает настройки из aistros.json, если параметры не указаны явно.
        Приоритет: явно переданные параметры > настройки из aistros.json > значения по умолчанию.

        Args:
            api_key (Optional[str]): API ключ. Если не указан, берётся из gs.credentials на основе key_name из aistros.json.
            model_name (Optional[str]): Название модели. Если не указано, берётся из aistros.json.
            system_instruction (Optional[str]): Системная инструкция для модели.
            generation_config (Optional[dict]): Конфигурация генерации ответов.

        Raises:
            ValueError: Если API ключ не указан и не найден в credentials.

        Example:
            >>> client = GeminiClient()
            >>> response = client.ask('Привет!')
            >>> print(response)
        """
        # Загрузка конфигурации из aistros.json
        aistros_config: SimpleNamespace = j_loads_ns(Path(__root__) / 'src' / 'endpoints' / 'aistros' / 'aistros.json')
        
        if not aistros_config:
            logger.warning('Не удалось загрузить aistros.json, используются значения по умолчанию')
            aistros_config = SimpleNamespace(
                model_name='gemini-2.0-flash-lite',
                generation_config={'response_mime_type': 'text/plain'}
            )

        # Установка параметров с учётом приоритета (явные параметры > aistros.json > умолчания)
        self.model_name: str = model_name or getattr(aistros_config, 'model_name', 'gemini-2.0-flash-lite')
        self.system_instruction: Optional[str] = system_instruction or getattr(aistros_config, 'system_instruction', None)
        
        # Получение API ключа (либо явно передан, либо из credentials по key_name из aistros.json)
        self.api_key: str = api_key or self._get_api_key(aistros_config)
        
        if not self.api_key:
            error_message: str = 'API ключ не найден. Укажите api_key или настройте gs.credentials.gemini и key_name в aistros.json'
            logger.error(error_message)
            raise ValueError(error_message)

        # Конфигурация генерации
        gen_config: dict = generation_config or getattr(aistros_config, 'generation_config', {'response_mime_type': 'text/plain'})

        try:
            self.model: GoogleGenerativeAi = GoogleGenerativeAi(
                api_key=self.api_key,
                model_name=self.model_name,
                generation_config=gen_config,
                system_instruction=self.system_instruction
            )
            logger.info(f'Клиент Gemini инициализирован с моделью {self.model_name}')
        except Exception as ex:
            logger.error('Ошибка инициализации клиента Gemini', ex, exc_info=True)
            raise

    def _get_api_key(self, aistros_config: SimpleNamespace) -> str:
        """
        Функция извлекает API ключ из credentials на основе key_name из конфигурации.

        Args:
            aistros_config (SimpleNamespace): Загруженная конфигурация из aistros.json.

        Returns:
            str: API ключ из gs.credentials.gemini.<key_name>.api_key или пустая строка.

        Example:
            >>> key = self._get_api_key(config)
        """
        if not hasattr(aistros_config, 'key_name'):
            logger.error('В aistros.json отсутствует параметр key_name')
            return ''

        key_name: str = aistros_config.key_name

        try:
            if not hasattr(gs.credentials, 'gemini'):
                logger.error('В credentials отсутствует секция gemini')
                return ''

            if not hasattr(gs.credentials.gemini, key_name):
                logger.error(f'В credentials.gemini отсутствует ключ {key_name}')
                return ''

            api_key: str = getattr(gs.credentials.gemini, key_name).api_key
            logger.info(f'API ключ успешно получен из credentials.gemini.{key_name}')
            return api_key

        except AttributeError as ex:
            logger.error(f'Ошибка доступа к API ключу {key_name}', ex, exc_info=True)
            return ''
        except Exception as ex:
            logger.error('Ошибка при получении API ключа', ex, exc_info=True)
            return ''

    def ask(
        self,
        question: str,
        attempts: int = 15,
        context: Optional[Union[str, List[str]]] = None,
        clean_response: bool = True
    ) -> Optional[str]:
        """
        Функция отправляет запрос модели и возвращает ответ.

        Args:
            question (str): Текст вопроса для модели.
            attempts (int): Количество попыток при ошибках. По умолчанию 15.
            context (Optional[Union[str, List[str]]]): Контекст для RAG.
            clean_response (bool): Очищать ли ответ от markdown разметки. По умолчанию True.

        Returns:
            Optional[str]: Ответ модели или None при ошибке.

        Example:
            >>> client = GeminiClient()
            >>> answer = client.ask('Что такое Python?')
            >>> print(answer)
            Python - это высокоуровневый язык программирования...
        """
        if not question:
            logger.error('Вопрос не может быть пустым')
            return None

        try:
            logger.debug(f'Отправка запроса: {question[:100]}...')
            response: Optional[str] = self.model.ask(
                q=question,
                attempts=attempts,
                context=context,
                clean_response=clean_response
            )

            if response:
                logger.info('Ответ получен успешно')
                return response
            else:
                logger.warning('Модель вернула пустой ответ')
                return None

        except Exception as ex:
            logger.error('Ошибка при выполнении запроса', ex, exc_info=True)
            return None

    def ask_with_context(
        self,
        question: str,
        context: Union[str, List[str]],
        attempts: int = 15
    ) -> Optional[str]:
        """
        Функция отправляет запрос с контекстом (RAG pattern).

        Args:
            question (str): Вопрос пользователя.
            context (Union[str, List[str]]): Контекст для модели (документы, факты).
            attempts (int): Количество попыток. По умолчанию 15.

        Returns:
            Optional[str]: Ответ модели с учётом контекста.

        Example:
            >>> context = ['Компания основана в 2020', 'Продукт - AI Assistant']
            >>> answer = client.ask_with_context('Когда основана?', context)
            >>> print(answer)
            Компания основана в 2020 году.
        """
        return self.ask(
            question=question,
            context=context,
            attempts=attempts
        )


def main():
    """
    Функция демонстрирует использование клиента Gemini.

    Example:
        >>> python gemini_client.py
    """
    # Инициализация клиента
    client: GeminiClient = GeminiClient()

    # Пример 1: Простой запрос
    print('\n--- Пример 1: Простой запрос ---')
    response: Optional[str] = client.ask('Что такое машинное обучение? Ответь кратко.')
    if response:
        print(f'Ответ: {response}')

    # Пример 2: Запрос с контекстом (RAG)
    print('\n--- Пример 2: Запрос с контекстом ---')
    context: List[str] = [
        'Компания "TechCorp" основана в 2020 году.',
        'Основной продукт - платформа для анализа данных DataViz Pro.',
        'Главный офис находится в Москве.',
        'Количество сотрудников - 150 человек.'
    ]

    question: str = 'Расскажи о компании TechCorp'
    response_with_context: Optional[str] = client.ask_with_context(question, context)
    if response_with_context:
        print(f'Ответ с контекстом: {response_with_context}')

    # Пример 3: Технический вопрос
    print('\n--- Пример 3: Технический вопрос ---')
    tech_question: str = 'Объясни разницу между list и tuple в Python одним предложением'
    tech_response: Optional[str] = client.ask(tech_question)
    if tech_response:
        print(f'Ответ: {tech_response}')


if __name__ == '__main__':
    main()