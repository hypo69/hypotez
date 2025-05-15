## \file src/llm/gemini/gemini.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module::  src.llm.gemini.gemini
   :platform: Windows, Unix
   :synopsis: Google generative llm integration
   https://github.com/google-gemini/generative-ai-python/blob/main/docs/api/google/generativeai.md

.. module:: src.llm.gemini.gemini
"""
import codecs
import re
import asyncio
import time
import json
import requests
import http
from io import IOBase
from pathlib import Path
from typing import Optional, Dict, List, Any
from types import SimpleNamespace
import base64

import google.generativeai as genai


from grpc import RpcError
from google.api_core.exceptions import (
    GatewayTimeout,
    RetryError,
    ServiceUnavailable,
    ResourceExhausted,
    InvalidArgument,
)
from google.auth.exceptions import (
    DefaultCredentialsError,
    RefreshError,
)

import header
from header import __root__
from src import gs

from src.utils.file import read_text_file, save_text_file
from src.utils.date_time import TimeoutCheck
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.image import get_image_bytes
from src.utils.string.ai_string_utils import normalize_answer, string_for_train
from src.utils.printer import pprint as print # Используется кастомный print
from src.logger import logger

timeout_check = TimeoutCheck()
# Removed dataclasses imports as they are no longer needed


class GoogleGenerativeAi:
    """
    Класс для взаимодействия с моделями Google GenerativeAi.

    Атрибуты:
        api_key (str): Ключ API для доступа к Google Generative AI.
        generation_config (Dict): Конфигурация для генерации ответов моделью.
                                  По умолчанию `{'response_mime_type': 'text/plain'}`.
                                  Допустимые mime-типы: `text/plain`, `application/json`,
                                  `application/xml`, `application/yaml`, `text/x.enum`.
        system_instruction (Optional[str]): Системная инструкция для модели. По умолчанию `None`.
        model_name (str): Имя используемой модели Gemini.
        config (SimpleNamespace): Загруженная конфигурация из файла 'gemini.json'.
        history_dir (Path): Директория для сохранения истории чатов.
        timestamp (str): Текущая временная метка для именования файлов истории.
        model (Any): Инициализированный клиент модели `genai.GenerativeModel`.
        _chat (Any): Активный сеанс чата с моделью.
        chat_history (List[Dict]): История текущего диалога в памяти.
        chat_name (str): Имя текущего чата для сохранения истории.
        history_json_file (Path): Путь к JSON файлу с историей текущего чата.
        # dialogue_txt_path (Path): (Не используется активно в текущей логике, но объявлено)
        # history_txt_file (Path): (Не используется активно в текущей логике, но объявлено)
    """
    ENDPOINT:Path = __root__/ 'src'/ 'llm'/ 'gemini'
    config: SimpleNamespace = j_loads_ns(ENDPOINT/ 'gemini.json')
    api_key: str
    system_instruction: str
    model_name: str = config.model_name
    model: 'genai.GenerativeModel'

    timestamp: str
    _chat: Any
    chat_history: List[Dict] = []
    chat_session_name: str = gs.now
    history_dir: Path = Path()
    history_json_file: Path = Path()
    dialogue_txt_path: Path = Path() 
    history_txt_file: Path = Path() 


    def __init__(
        self,
        api_key: str,
        model_name: str,
        generation_config: Optional[Dict] = {'response_mime_type': 'text/plain'},
        system_instruction: Optional[str] = None,
    ):
        """
        Инициализирует экземпляр класса GoogleGenerativeAi.

        Args:
            api_key (str): Ключ API для Google Generative AI.
            model_name (str): Имя модели Gemini для использования (например, 'gemini-pro').
            generation_config (Dict, optional): Конфигурация генерации.
                                                По умолчанию `{'response_mime_type': 'text/plain'}`.
            system_instruction (Optional[str], optional): Системная инструкция для модели.
                                                         По умолчанию `None`.
        """
        
        self.api_key = api_key
        self.model_name = model_name 
        self.generation_config = generation_config
        self.system_instruction = system_instruction

        self.history_dir = Path(__root__, gs.path.external_storage, 'chats')
        self.timestamp = gs.now


        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                system_instruction=self.system_instruction,
            )
            self._chat = self._start_chat()
            ...
            logger.info(f"Модель {self.model.model_name} инициализирована", None, False)
        except (DefaultCredentialsError, RefreshError) as ex:
             logger.error('Ошибка аутентификации Gemini API', ex)
             ...
             raise # Повторный вызыв исключения, чтобы прервать инициализацию
        except Exception as ex:
            logger.error('Не удалось инициализировать модель Gemini', ex)
            ...
            raise # Повторный вызыв исключения, чтобы прервать инициализацию
        ...


    def _start_chat(self,system_instruction: Optional[str] = '') -> Any: # Возвращаемый тип Any, т.к. genai.ChatSession не экспортируется явно
        """
        Функция запускает новый сеанс чата с моделью.

        Учитывает наличие `system_instruction` при инициализации чата.

        Returns:
            Any: Объект сеанса чата (`genai.ChatSession`).
        """
        if self.system_instruction:
            # Запуск чата с системной инструкцией
            return self.model.start_chat(history=[{'role': 'user', 'parts': [self.system_instruction]}])
        else:
            # Запуск чата без системной инструкции
            return self.model.start_chat(history=[])


    async def _save_chat_history(self) -> bool:
        """
        Функция асинхронно сохраняет текущую историю чата в JSON файл.

        Имя файла формируется из `chat_name` и `timestamp`.

        Returns:
            bool: `True` в случае успешного сохранения, `False` при ошибке.
        """
        json_file_name: str = f'{self.chat_session_name}-{self.timestamp}.json'
        self.history_json_file = Path(self.history_dir, json_file_name)

        # Создание директории, если она не существует
        try:
            self.history_dir.mkdir(parents=True, exist_ok=True)
        except Exception as ex:
            logger.error(f'Не удалось создать директорию для истории чата: {self.history_dir}', ex)
            return False

        if not j_dumps(data=self.chat_history, file_path=self.history_json_file, mode='w'):
            logger.error(f"Ошибка сохранения истории чата в файл {self.history_json_file=}", None, False)
            return False
        logger.info(f"История чата сохранена в файл {self.history_json_file=}", None, False)
        return True

    async def _load_chat_history(self, chat_data_folder: Optional[str | Path]) -> None:
        """
        Функция асинхронно загружает историю чата из JSON файла.

        Опционально принимает путь к папке с данными чата. Если указан,
        использует 'history.json' из этой папки. Иначе использует
        текущий `self.history_json_file`.

        Args:
            chat_data_folder (Optional[str | Path]): Путь к папке с файлом 'history.json'.

        Returns:
            None
        """
        history_to_load: Optional[List[Dict]] = None
        target_file: Path = self.history_json_file # По умолчанию используем текущий файл

        try:
            if chat_data_folder:
                # Если указана папка, формируем путь к history.json в ней
                target_file = Path(chat_data_folder, 'history.json')

            if target_file.exists():
                history_to_load = j_loads(target_file)
                if history_to_load is not None:
                    self.chat_history = history_to_load
                    # Перезапускаем чат с загруженной историей
                    self._chat = self._start_chat() # Начинаем с чистого чата (возможно, с system prompt)
                    # Добавляем загруженные сообщения в историю сеанса _chat
                    for entry in self.chat_history:
                        # Проверка на валидность роли (должна быть 'user' или 'model')
                        if entry.get('role') in ('user', 'model'):
                             # Убедимся, что parts существует и является списком
                             if isinstance(entry.get('parts'), list):
                                 self._chat.history.append(entry)
                             else:
                                 logger.warning(f"Пропуск записи истории с некорректным форматом 'parts': {entry}")
                        else:
                            logger.warning(f"Пропуск записи истории с некорректной ролью: {entry}")

                    logger.info(f"История чата ({len(self.chat_history)} сообщений) загружена из файла. \n{target_file=}", None, False)
                else:
                     logger.error(f"Файл истории {target_file=} пуст или содержит некорректные данные.", None, False)
            else:
                logger.info(f"Файл истории {target_file=} не найден. Новая история будет создана.", None, False)
                self.chat_history = [] # Убедимся, что история пуста, если файл не найден
                self._chat = self._start_chat() # Начинаем новый чат

        except Exception as ex:
            logger.error(f"Ошибка загрузки истории чата из файла {target_file=}", ex) # Добавлено exc_info
            self.chat_history = [] # Сброс истории при ошибке загрузки
            self._chat = self._start_chat() # Начинаем новый чат при ошибке

    def clear_history(self) -> None:
        """
        Функция очищает историю чата в памяти и удаляет связанный JSON файл истории.

        Returns:
            None
        """
        try:
            self.chat_history = []  # Очистка истории в памяти
            if hasattr(self, 'history_json_file') and self.history_json_file.exists():
                self.history_json_file.unlink()  # Удаление файла истории
                logger.info(f"Файл истории {self.history_json_file} удалён.")
        except Exception as ex:
            logger.error('Ошибка при очистке истории чата.', ex) # Добавлено exc_info

    async def chat(self, q: str, chat_session_name: Optional[str] = '', flag: Optional[str] = 'save_chat') -> Optional[str]:
        """
        Функция обрабатывает чат-запрос пользователя, управляет историей и возвращает ответ модели.

        Args:
            q (str): Вопрос пользователя.
            chat_name (str): Имя чата для сохранения/загрузки истории.
            flag (str, optional): Режим управления историей. По умолчанию 'save_chat'.
                                  (Текущая реализация не использует `flag`, история всегда сохраняется).
                                  Потенциальные значения (не реализованы полностью):
                                  "save_chat": Загружает и сохраняет историю.
                                  "read_and_clear": Загружает историю, затем очищает её перед новым запросом.
                                  "clear": Очищает историю перед запросом.
                                  "start_new": Архивирует старую историю (если есть) и начинает новую.

        Returns:
            Optional[str]: Текстовый ответ модели или `None` в случае ошибки.
        """
        self.chat_session_name = chat_session_name if chat_session_name else self.chat_session_name 
        response: Any = None # Инициализация переменной ответа
        response_text: Optional[str] = None # Инициализация переменной для текста ответа

        # --- Логика флагов (закомментирована в оригинале, оставлена для справки) ---
        # try:
        #     if flag == "save_chat":
        #         await self._load_chat_history(chat_data_folder) # chat_data_folder не передан
        #
        #     if flag == "read_and_clear":
        #         logger.info(f"Прочитал историю чата и начал новый", text_color='gray')
        #         await self._load_chat_history(chat_data_folder)
        #         self.chat_history = []  # Очистка истории
        #
        #     if flag == "read_and_start_new":
        #         logger.info(f"Прочитал историю чата, сохранил и начал новый", text_color='gray')
        #         await self._load_chat_history(chat_data_folder)
        #         self.chat_history = []  # Очистка истории
        #         flag = "start_new"
        #
        #     elif flag == "clear":
        #         logger.info(f"Вытер прошлую историю")
        #         self.chat_history = []  # Очистка истории
        #
        #     elif flag == "start_new":
        #         timestamp = time.strftime("%Y%m%d_%H%M%S")
        #         archive_file = self.history_dir / f"history_{timestamp}.json"
        #         logger.info(f"Сохранил прошлую историю в {timestamp}", text_color='gray')
        #         if self.chat_history:
        #             j_dumps(data=self.chat_history, file_path=archive_file, mode="w")
        #         self.chat_history = []  # Начать новую историю
        # except Exception as ex:
        #     logger.error(f"Ошибка обработки флага '{flag}'", ex)
        #     # Продолжаем выполнение с текущей историей


        try:
            # Отправка запроса модели
            try:
                # Асинхронная отправка сообщения
                response = await self._chat.send_message_async(q)

            except ResourceExhausted as ex:
                logger.error("Исчерпан ресурс (Resource exhausted)", ex, False)
                # Попытка перезапуска чата через некоторое время
                await asyncio.sleep(30000) # Пауза перед перезапуском
                self._start_chat()
                # Рекурсивный вызов не рекомендуется, лучше вернуть None или поднять исключение
                # await self.chat(q, chat_name, flag)
                return None # Возврат None после исчерпания ресурса

            except InvalidArgument as ex:
                 logger.error("Недопустимый аргумент (InvalidArgument)", ex, False)
                 # Проверка на превышение лимита токенов
                 if hasattr(ex, 'message') and 'maximum number of tokens allowed' in ex.message:
                    logger.warning("Превышен лимит токенов, перезапуск чата...")
                    self._start_chat()
                    # Повторный вызов после перезапуска
                    return await self.chat(q, chat_name, flag) # Повторная попытка
                 return None # Возврат None при других InvalidArgument

            except RpcError as ex:
                # Обработка ошибок gRPC, включая таймауты
                logger.error(f"Ошибка RPC: {ex.code()} - {ex.details()}", ex, False)
                # Проверка на специфичные коды ошибок, например, DEADLINE_EXCEEDED
                if ex.code() == grpc.StatusCode.DEADLINE_EXCEEDED or \
                   (hasattr(ex, 'details') and 'Deadline Exceeded' in ex.details()):
                     timeout: int = 300 # Уменьшенное время ожидания
                     logger.debug(f'Таймаут RPC. Пауза {timeout} секунд.')
                     await asyncio.sleep(timeout)
                     self._start_chat()
                     return await self.chat(q, chat_name, flag) # Повторная попытка
                return None # Возврат None при других RPC ошибках

            except Exception as ex:
                 logger.error("Общая ошибка при отправке сообщения в чат", ex) # exc_info=True
                 # Пример обработки специфичной ошибки по тексту (менее надежно)
                 # if hasattr(ex, 'text') and '504 Deadline Exceeded' in ex.text:
                 #     timeout:int = 3000
                 #     logger.debug(f'Going sleep for {timeout/360} hours') # Опечатка: 3000 секунд = 50 минут
                 #     await asyncio.sleep(timeout)
                 #     self._start_chat()
                 #     return await self.chat(q,  chat_name, flag)
                 return None # Возврат None при необработанной ошибке

            # Обработка ответа и метаданных
            try:
                # Извлечение метаданных об использовании токенов
                if hasattr(response, 'usage_metadata') and response.usage_metadata:
                    response_token_count = response.usage_metadata.candidates_token_count
                    total_token_count = response.usage_metadata.total_token_count
                    prompt_token_count = response.usage_metadata.prompt_token_count

                    logger.info(f"Токены в ответе: {response_token_count}")
                    logger.info(f"Токены в запросе: {prompt_token_count}")
                    logger.info(f"Общее количество токенов: {total_token_count}")
                else:
                    # Это может произойти, если генерация не удалась или API не вернул метаданные
                    logger.warning("Метаданные об использовании токенов отсутствуют в ответе (usage_metadata is None or empty).")

            except AttributeError:
                # На случай, если у объекта response вообще нет атрибута usage_metadata
                logger.warning("Атрибут 'usage_metadata' отсутствует в объекте ответа.")
            except Exception as meta_ex:
                 logger.error("Ошибка при извлечении метаданных токенов", meta_ex) # exc_info=True

            # Проверка и извлечение текста ответа
            if hasattr(response, 'text') and response.text:
                response_text = response.text
                # Добавление запроса и ответа в историю
                self.chat_history.append({"role": "user", "parts": [q]})
                self.chat_history.append({"role": "model", "parts": [response_text]})
                # Сохранение обновленной истории
                await self._save_chat_history()
                return response_text # Возврат текста ответа
            else:
                logger.error(f"Пустой ответ от модели. Ответ: {response}", None, False)
                ... # 
                return None # Возврат None при пустом ответе

        except Exception as ex:
            # Логгирование общей ошибки выполнения метода chat
            logger.error(f"Критическая ошибка в методе chat. Ответ: {response}", ex) # exc_info=True
            return None # Возврат None при критической ошибке

    def ask(self, q: str, attempts: int = 15, save_dialogue: bool = False, clean_response: bool = True) -> Optional[str]:
        """
        Метод синхронно отправляет текстовый запрос модели и возвращает ответ.

        Использует `generate_content` (не для чата). Повторяет запрос при ошибках.

        Args:
            q (str): Текстовый запрос к модели.
            attempts (int): Количество попыток отправки запроса. По умолчанию 15.
            save_dialogue (bool): Флаг сохранения диалога (вопрос/ответ) в файл.
                                 (Примечание: использует нереализованный `_save_dialogue`). По умолчанию False.
            clean_response (bool): Флаг очистки ответа от разметки кода. По умолчанию True.

        Returns:
            Optional[str]: Текстовый ответ модели или `None` в случае неудачи после всех попыток.

        Raises:
            (Implicitly raises exceptions during network/API errors if not caught)
        """
        response: Any = None # Объявление переменной для ответа
        response_text: Optional[str] = None # Объявление переменной для текста ответа

        for attempt in range(attempts):
            try:
                response = self.model.generate_content(q)

                # Проверка наличия текста в ответе
                if hasattr(response, 'text') and response.text:
                    response_text = response.text
                    if save_dialogue:
                        # Вызов нереализованного метода _save_dialogue
                        # self._save_dialogue([
                        #     {"role": "user", "content": q},
                        #     {"role": "model", "content": response_text},
                        # ])
                        logger.warning("Функция _save_dialogue не реализована, история не сохранена.")

                    # Возврат очищенного или полного ответа
                    return normalize_answer(response_text) if clean_response else response_text
                else:
                    # Логгирование отсутствия ответа и пауза перед повторной попыткой
                    sleep_time = 2 ** attempt
                    logger.debug(
                        f"От модели не получен ответ. Попытка: {attempt + 1}/{attempts}. Пауза: {sleep_time} сек.",
                        None,
                        False
                    )
                    time.sleep(sleep_time)
                    continue  # Переход к следующей попытке

            except requests.exceptions.RequestException as ex:
                max_attempts_network = 5
                if attempt >= max_attempts_network: # Скорректировано условие
                    logger.error(f"Сетевая ошибка после {max_attempts_network} попыток.", ex, False)
                    break # Прерывание цикла после макс. попыток
                sleep_time_network = 120 # Уменьшена пауза до 2 минут
                logger.debug(
                    f"Сетевая ошибка. Попытка: {attempt + 1}/{attempts}. Пауза: {sleep_time_network/60} мин. Время: {gs.now}",
                    ex,
                    False,
                )
                time.sleep(sleep_time_network)
                continue  # Переход к следующей попытке

            except (GatewayTimeout, ServiceUnavailable) as ex:
                max_attempts_service = 3
                if attempt >= max_attempts_service: # Скорректировано условие
                     logger.error(f"Сервис недоступен после {max_attempts_service} попыток.", ex, False)
                     break # Прерывание цикла
                sleep_time_service = 2**attempt + 10
                logger.error(f"Сервис недоступен. Попытка: {attempt + 1}/{attempts}. Пауза: {sleep_time_service} сек.", ex, False)
                time.sleep(sleep_time_service)
                continue # Переход к следующей попытке

            except ResourceExhausted as ex:
                logger.critical(f"""
                ------------------------------------------------------------------------
                           
                Исчерпн лимит
                           Внимание! В ответе будет передан `ResourceExhausted` строкой

                -------------------------------------------------------------------------
                """, None, False)
                # print(ex)
                # TOO_MANY_REQUESTS_TIMEOUT:int = 20
                # if ex.code == http.HTTPStatus.TOO_MANY_REQUESTS:
                #     logger.debug(
                #         f"Много запросов в минуту. \nПопытка: {attempt + 1}/{attempts}. \nПауза: {TOO_MANY_REQUESTS_TIMEOUT} сек. Время: {gs.now}\n",
                #         ex,
                #         False,
                #     )
                #     time.sleep(TOO_MANY_REQUESTS_TIMEOUT)  
                #     continue # Переход к следующей попытке

                # # Длительная пауза при исчерпании квоты
                # timeout_quota = 14400 # 4 часа
                # logger.debug(
                #     f"Исчерпана квота. Попытка: {attempt + 1}/{attempts}. Пауза: {timeout_quota/3600} час(ов). Время: {gs.now}",
                #     ex,
                #     False,
                # )
                # time.sleep(timeout_quota)
                # continue # Переход к следующей попытке
                return "ResourceExhausted"

            except (DefaultCredentialsError, RefreshError) as ex:
                logger.error("Ошибка аутентификации.", ex, False)
                return None  # Прекращение попыток при ошибке аутентификации

            except (ValueError, TypeError) as ex: # Ошибки, связанные с некорректными входными данными
                max_attempts_input = 3
                if attempt >= max_attempts_input: # Скорректировано условие
                    logger.error(f"Ошибка входных данных после {max_attempts_input} попыток.", ex, False)
                    break # Прерывание цикла
                timeout_input = 5
                logger.error(
                    f"Некорректные входные данные. Попытка: {attempt + 1}/{attempts}. Пауза: {timeout_input} сек. Время: {gs.now}",
                    ex,
                    None, # Не передаем исключение в лог как ошибку приложения
                )
                time.sleep(timeout_input)
                continue # Переход к следующей попытке

            except (InvalidArgument, RpcError) as ex: # Ошибки API
                logger.error("Ошибка API.", ex, False)
                return None # Прекращение попыток при ошибке API

            except Exception as ex: # Неожиданные ошибки
                logger.error("Неожиданная ошибка.", ex) # Добавлено exc_info
                return None # Прекращение попыток при неизвестной ошибке

        logger.error(f"Не удалось получить ответ от модели после {attempts} попыток.")
        return None # Возврат None, если все попытки исчерпаны

    async def ask_async(self, q: str, attempts: int = 15, save_dialogue: bool = False, clean_response: bool = True) -> Optional[str]:
        """
        Метод асинхронно отправляет текстовый запрос модели и возвращает ответ.

        Использует `generate_content` (не для чата) в отдельном потоке. Повторяет запрос при ошибках.

        Args:
            q (str): Текстовый запрос к модели.
            attempts (int): Количество попыток отправки запроса. По умолчанию 15.
            save_dialogue (bool): Флаг сохранения диалога (вопрос/ответ) в файл.
                                 (Примечание: использует нереализованный `_save_dialogue`). По умолчанию False.
            clean_response (bool): Флаг очистки ответа от разметки кода. По умолчанию True.

        Returns:
            Optional[str]: Текстовый ответ модели или `None` в случае неудачи после всех попыток.

        Raises:
            (Implicitly raises exceptions during network/API errors if not caught)
        """
        response: Any = None # Объявление переменной для ответа
        response_text: Optional[str] = None # Объявление переменной для текста ответа

        for attempt in range(attempts):
            try:
                # Запуск синхронного метода generate_content в отдельном потоке
                response = await self.model.generate_content_async(str(q))
                logger.info(f'Модель {self.model.model_name} Обработала запрос',None, False)
                # Проверка наличия текста в ответе
                if hasattr(response, 'text') and response.text:
                    response_text = response.text
                    if save_dialogue:
                        # Вызов нереализованного метода _save_dialogue
                        # self._save_dialogue([
                        #     {"role": "user", "content": q},
                        #     {"role": "model", "content": response_text},
                        # ])
                        logger.warning("Функция _save_dialogue не реализована, история не сохранена.")

                    # Возврат очищенного или полного ответа
                    return normalize_answer(response_text) if clean_response else response_text

                else:
                     # Логгирование отсутствия ответа и асинхронная пауза
                    sleep_time = 2 ** attempt
                    logger.debug(
                        f"От модели не получен ответ. Попытка: {attempt + 1}/{attempts}. Асинхронная пауза: {sleep_time} сек.",
                        None,
                        False
                    )
                    await asyncio.sleep(sleep_time)  # Асинхронная пауза
                    continue  # Переход к следующей попытке


            except requests.exceptions.RequestException as ex:
                max_attempts_network = 5
                if attempt >= max_attempts_network: # Скорректировано условие
                    logger.error(f"Сетевая ошибка после {max_attempts_network} попыток.", ex, False)
                    break # Прерывание цикла
                sleep_time_network: int = 120 # Уменьшена пауза до 2 минут
                logger.debug(
                    f"Сетевая ошибка. Попытка: {attempt + 1}/{attempts}. Асинхронная пауза: {sleep_time_network/60} мин. Время: {gs.now}",
                    ex,
                    False,
                )
                await asyncio.sleep(sleep_time_network)  # Асинхронная пауза
                continue  # Переход к следующей попытке

            except (GatewayTimeout, ServiceUnavailable) as ex:
                max_attempts_service = 3
                if attempt >= max_attempts_service: # Скорректировано условие
                     logger.error(f"Сервис недоступен после {max_attempts_service} попыток.", ex, False)
                     break # Прерывание цикла
                sleep_time_service = 2**attempt + 10
                logger.error(f"Сервис недоступен. Попытка: {attempt + 1}/{attempts}. Асинхронная пауза: {sleep_time_service} сек.", ex, False)
                await asyncio.sleep(sleep_time_service) # Асинхронная пауза
                continue # Переход к следующей попытке

            except ResourceExhausted as ex:
                 # Длительная асинхронная пауза при исчерпании квоты
                timeout_quota: int = 14400 # 4 часа
                logger.debug(
                    f"Исчерпана квота. Попытка: {attempt + 1}/{attempts}. Асинхронная пауза: {timeout_quota/3600} час(ов). Время: {gs.now}",
                    ex,
                    False,
                )
                await asyncio.sleep(timeout_quota)  # Асинхронная пауза
                continue # Переход к следующей попытке

            except (DefaultCredentialsError, RefreshError) as ex:
                logger.error("Ошибка аутентификации.", ex)
                return None  # Прекращение попыток при ошибке аутентификации

            except (ValueError, TypeError) as ex: # Ошибки, связанные с некорректными входными данными
                max_attempts_input = 3
                if attempt >= max_attempts_input: # Скорректировано условие
                    logger.error(f"Ошибка входных данных после {max_attempts_input} попыток.", ex)
                    break # Прерывание цикла
                timeout_input = 5
                logger.error(
                    f"Некорректные входные данные. Попытка: {attempt + 1}/{attempts}. Асинхронная пауза: {timeout_input} сек. Время: {gs.now}",
                    ex,
                    None, # Не передаем исключение в лог как ошибку приложения
                )
                await asyncio.sleep(timeout_input) # Асинхронная пауза
                continue # Переход к следующей попытке

            except (InvalidArgument, RpcError) as ex: # Ошибки API
                logger.error("Ошибка API.", ex, False)
                ... # Логгирование ошибки API
                return None # Прекращение попыток при ошибке API

            except Exception as ex: # Неожиданные ошибки
                logger.error("Неожиданная ошибка.", ex) 
                ...
                return None # Прекращение попыток при неизвестной ошибке

        logger.error(f"Не удалось получить ответ от модели после {attempts} попыток.")
        return None # Возврат None, если все попытки исчерпаны


    def describe_image(
        self, image: Path | bytes, mime_type: Optional[str] = 'image/jpeg', prompt: Optional[str] = ''
    ) -> Optional[str]:
        """
        Функция отправляет изображение (и опциональный промпт) в модель Gemini Pro Vision
        и возвращает его текстовое описание.

        Args:
            image (Path | bytes): Путь к файлу изображения или байты изображения.
            mime_type (Optional[str]): MIME-тип изображения. По умолчанию 'image/jpeg'.
            prompt (Optional[str]): Текстовый промпт для модели вместе с изображением. По умолчанию ''.

        Returns:
            Optional[str]: Текстовое описание изображения от модели или `None` при ошибке.
        """
        
        image_data: bytes
        content: List[Any]
        response: Any = None
        response_text: Optional[str] = None
        start_time: float = time.time() # Засекаем время начала

        try:
            # Подготовка данных изображения
            if isinstance(image, Path):
                img_bytes = get_image_bytes(image) # Извлечение байтов из файла
                if img_bytes is None:
                     logger.error(f"Не удалось прочитать байты изображения из файла: {image}")
                     return None
                image_data = img_bytes
            elif isinstance(image, bytes):
                image_data = image
            else:
                logger.error(f"Некорректный тип для 'image'. Ожидается Path или bytes, получено: {type(image)}")
                return None

            # Формирование контента для запроса
            # Используем формат, подходящий для generate_content с multimodal input
            # https://ai.google.dev/tutorials/python_quickstart#generate_text_from_image_input
            content_parts: List[Any] = []
            if prompt:
                content_parts.append(prompt) # Добавляем текст промпта

            # Добавляем изображение в формате PIL Image (предпочтительно для gemini)
            # или как словарь с base64 данными, если PIL недоступен/нежелателен.
            # Для простоты оставим вариант с передачей байтов напрямую,
            # но учтем, что API может ожидать PIL Image.
            # Попробуем передать байты напрямую в generate_content
            content_parts.append(
                # Формируем структуру, которую понимает generate_content
                # Вместо словаря с role/parts, передаем список [prompt, image_data]
                {'mime_type': mime_type, 'data': image_data}
            )

            # Отправка запроса и получение ответа
            try:
                # Передаем список частей [prompt, image_dict]
                response = self.model.generate_content(content_parts)

            except DefaultCredentialsError as ex:
                logger.error("Ошибка аутентификации:", ex)
                return None
            except (InvalidArgument, RpcError) as ex:
                logger.error("Ошибка API:", ex, False)
                return None
            except RetryError as ex:
                logger.error("Модель перегружена (RetryError). Попробуйте позже:", ex, False)
                return None
            except Exception as ex:
                logger.error("Ошибка при отправке запроса модели:", ex)
                return None
            finally:
                # Логгирование времени выполнения запроса
                 processing_time = time.time() - start_time
                 logger.info(f'\nВремя обработки изображения: {processing_time:.2f} сек.\n', text_color='yellow', bg_color='red')


            # Обработка ответа
            if hasattr(response, 'text') and response.text:
                 response_text = response.text
                 return response_text # Возврат текста ответа
            else:
                 # Логгирование случая, когда ответ не содержит текста
                 logger.info(f"{{Модель вернула ответ без текста: {response}}}", text_color='cyan')
                 # Можно также проверить response.prompt_feedback для информации о блокировке
                 if hasattr(response, 'prompt_feedback'):
                     logger.warning(f"Обратная связь по промпту: {response.prompt_feedback}")
                 return None

        except Exception as ex:
            # Логгирование общих ошибок при обработке изображения
            logger.error("Произошла ошибка при обработке изображения:", ex)
            ... # Оставляем как есть
            return None

    async def upload_file(
        self, file: str | Path | IOBase, file_name: Optional[str] = None
    ) -> Optional[Any]: # Возвращает объект File или None
        """
        Асинхронно загружает файл в Google AI File API.

        https://github.com/google-gemini/generative-ai-python/blob/main/docs/api/google/generativeai/upload_file.md

        Args:
            file (str | Path | IOBase): Путь к файлу или файловый объект.
            file_name (Optional[str]): Имя файла для отображения в API. Если None,
                                       используется имя из пути файла.

        Returns:
            Optional[Any]: Объект `File` от API в случае успеха, иначе `None`.
                           (Тип Any, т.к. `file_types.File` не экспортируется явно).
        """
        
        response: Any = None
        resolved_file_path: Optional[Path] = None
        resolved_file_name: Optional[str] = file_name

        try:
            # Определение пути и имени файла
            if isinstance(file, Path):
                resolved_file_path = file
                if resolved_file_name is None:
                    resolved_file_name = file.name
            elif isinstance(file, str):
                 resolved_file_path = Path(file)
                 if resolved_file_name is None:
                    resolved_file_name = resolved_file_path.name
            elif isinstance(file, IOBase):
                 # Для IOBase путь не используется, но имя нужно
                 if resolved_file_name is None:
                     logger.warning("Для IOBase рекомендуется указывать file_name.")
                     # Можно попытаться извлечь имя, если возможно
                     if hasattr(file, 'name'):
                         resolved_file_name = Path(file.name).name
                     else:
                         resolved_file_name = 'uploaded_file' # Имя по умолчанию
                 # Передаем сам объект IOBase в path
                 resolved_file_path = file # type: ignore
            else:
                 logger.error(f"Неподдерживаемый тип для 'file': {type(file)}")
                 ...
                 return None

            # Асинхронная загрузка файла
            logger.debug(f"Начало загрузки файла: {resolved_file_name or resolved_file_path}")
            response = await genai.upload_file_async(
                path=resolved_file_path, # type: ignore
                mime_type=None, # Автоопределение MIME-типа
                name=resolved_file_name, # Уникальное имя ресурса (опционально)
                display_name=resolved_file_name, # Отображаемое имя
                resumable=True, # Использовать возобновляемую загрузку
            )
            logger.debug(f"Файл '{response.display_name}' (URI: {response.uri}) успешно загружен.", None, False)
            return response

        except Exception as ex:
            logger.error(f"Ошибка загрузки файла '{resolved_file_name or file}'", ex)
            # Попытка удаления файла при ошибке (если имя известно и предполагается, что он мог быть создан частично)
            # В оригинальной логике была попытка удаления и повторной загрузки, что может привести к рекурсии.
            # Ограничимся сообщением об ошибке.
            # try:
            #     if resolved_file_name: # Удаление возможно только если имя известно
            #         logger.info(f"Попытка удаления файла {resolved_file_name} после ошибки загрузки...")
            #         await genai.delete_file_async(resolved_file_name) # Имя ресурса может отличаться от display_name
            #         logger.debug(f"Файл {resolved_file_name} удален после ошибки.", None, False)
            #     # await self.upload_file(file, file_name) # Убран рекурсивный вызов
            # except Exception as del_ex:
            #     logger.error(f"Ошибка при попытке удаления файла {resolved_file_name} после неудачной загрузки", del_ex, False)
            ...
            return None


async def main():
    """Основная асинхронная функция для демонстрации работы класса."""
    # Проверка наличия ключа API
    onela:str = gs.credentials.gemini.onela.api_key
    kazarinov:str = gs.credentials.gemini.kazarinov.api_key
    system_instruction = 'Ты - полезный ассистент. Отвечай на все вопросы кратко'
    model_name = 'gemini-2.5-flash-preview-04-17' # Пример имени модели, замените при необходимости

    if not onela and not kazarinov:
        logger.error("Ключ API Gemini не найден в gs.credentials.gemini.api_key.")
        ...
        return


    try:
        llm = GoogleGenerativeAi(
            api_key = kazarinov,       # <- здесь можно менять ключ API
            model_name = model_name, #  имя модели
            system_instruction = system_instruction
        )
    except Exception as ех:
        logger.error(f"Не удалось инициализировать GoogleGenerativeAi:", ех)
        ...
        return


    # # --- Пример описания изображения ---
    # image_path = Path('test.jpg')  # Замените на путь к вашему изображению

    # if not image_path.is_file():
    #     logger.info(
    #         f"Файл изображения {image_path} не существует. Поместите файл с таким именем в корневую папку."
    #     )
    # else:
    #     # Пример 1: Запрос описания в JSON
    #     prompt_json = """Проанализируй это изображение. Выдай ответ в формате JSON,
    #     где ключом будет имя объекта, а значением его описание.
    #      Если есть люди, опиши их действия."""

    #     description_json = llm.describe_image(image_path, prompt=prompt_json) # describe_image синхронный
    #     if description_json:
    #         logger.info("Описание изображения (запрос JSON):")
    #         logger.info(description_json)
    #         # Попытка парсинга JSON
    #         parsed_description = j_loads(description_json) # Используем j_loads для безопасного парсинга
    #         if parsed_description:
    #              logger.info("JSON успешно распарсен.")
    #              # print(parsed_description, text_color='green') # Используем кастомный print
    #         else:
    #              logger.warning("Не удалось распарсить JSON из ответа модели.")
    #     else:
    #         logger.info("Не удалось получить описание изображения (запрос JSON).")

    #     # Пример 2: Запрос простого описания
    #     prompt_simple = "Проанализируй это изображение. Перечисли все объекты, которые ты можешь распознать."
    #     description_simple = llm.describe_image(image_path, prompt=prompt_simple) # describe_image синхронный
    #     if description_simple:
    #         logger.info("\nОписание изображения (простой запрос):")
    #         logger.info(description_simple)
    #     else:
    #          logger.info("Не удалось получить описание изображения (простой запрос).")


    # # --- Пример загрузки файла ---
    # file_path_txt = Path('test.txt')
    # try:
    #     with open(file_path_txt, 'w', encoding='utf-8') as f:
    #         f.write("Hello, Gemini File API!")
    #     logger.info(f"Тестовый файл {file_path_txt} создан.")

    #     # Асинхронная загрузка файла
    #     file_upload_response = await llm.upload_file(file_path_txt, 'test_file_from_sdk.txt')
    #     if file_upload_response:
    #         logger.info("Ответ API на загрузку файла:")
    #         logger.info(file_upload_response) # Логгируем ответ API
    #     else:
    #          logger.error("Не удалось загрузить файл.")

    # except IOError as e:
    #     logger.error(f"Ошибка при создании тестового файла {file_path_txt}: {e}")
    # except Exception as e:
    #      logger.error(f"Ошибка при загрузке файла: {e}")
    # finally:
    #     # Опционально: удаление тестового файла
    #     if file_path_txt.exists():
    #         try:
    #             file_path_txt.unlink()
    #             logger.info(f"Тестовый файл {file_path_txt} удален.")
    #         except OSError as e:
    #             logger.error(f"Не удалось удалить тестовый файл {file_path_txt}: {e}")


    # --- Пример чата ---
    logger.info("\nНачало сеанса чата. Введите 'exit' для выхода.")
    chat_session_name = f'chat_session_{gs.now}' # Уникальное имя для сессии чата
    llm_message = await llm.ask_async('Привет! Как дела?') # Пример начального сообщения')
    while True:
        try:
            user_message = input("You: ")
        except EOFError: # Обработка Ctrl+D/EOF
             logger.info("\nЗавершение чата по EOF.")
             break
        if user_message.lower() == 'exit':
            logger.info("Завершение чата по команде пользователя.")
            break

        # Асинхронный вызов чата
        llm_message = await llm.chat(user_message, chat_name=chat_session_name)
        if llm_message:
            # Используем logger для вывода ответа Gemini
            logger.info(f"Gemini: {llm_message}")
        else:
            # Сообщение об ошибке уже должно быть в логах из метода chat
            logger.warning("Gemini: Не удалось получить ответ.")


if __name__ == "__main__":
    asyncio.run(main())