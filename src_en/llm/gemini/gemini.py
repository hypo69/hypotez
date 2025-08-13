# # \file src/llm/gemini/gemini.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

""".. module::  src.llm.gemini.gemini
   :platform: Windows, Unix
   :synopsis: Google generative llm integration
   https://github.com/google-gemini/generative-ai-python/blob/main/docs/api/google/generativeai.md

.. module:: src.llm.gemini.gemini"""
import codecs # Not used, you can delete
import re # Not used, you can delete
import asyncio
import time
import json # It is not used directly in j_loads/dumps, but can come in handy while we leave
import requests
import http # Not used directly, but can come in handy for httpstatus while leaving
from io import IOBase
from pathlib import Path
from typing import Optional, Dict, List, Any, Union
from types import SimpleNamespace
import base64 # Not used, you can delete

import google.generativeai as genai
import grpc # Для grpc.StatusCode.DEADLINE_EXCEEDED

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
from src.utils.printer import pprint as print # Castle Print is used
from src.logger import logger

timeout_check = TimeoutCheck()

# --- Constants for timouts and attempts ---
NETWORK_ERROR_MAX_ATTEMPTS = 5
SERVICE_UNAVAILABLE_MAX_ATTEMPTS = 3
INVALID_INPUT_MAX_ATTEMPTS = 3
INITIAL_RETRY_SLEEP_SECONDS = 2
NETWORK_RETRY_SLEEP_SECONDS = 120 # 2 minutes
SERVICE_RETRY_SLEEP_SECONDS_BASE = 10
QUOTA_EXHAUSTED_SLEEP_SECONDS = 14400 # 4 hours

class GoogleGenerativeAi:
    """Class for interacting with Google Generativeai models.

    Attributes:
        API_KEY (str): API key for access to Google Generative Ai.
        Generation_Config (DICT): Configuration for generating answers to the model.
                                  By default `{'Response_mime_type': 'Text/Plain'}`.
                                  Permissible MIME Tips: `Text/Plain`,` Application/Json`,
                                  `Application/Xml`,` Application/Yaml`, `Text/X.Eenum`.
        System_instruction (Optional [str]): System instructions for the model. By default `none`.
        Model_name (str): The name is used by Gemini.
        Config (Simplenamespace): uploaded configuration from the file 'gemini.json'.
        History_Dir (Path): Directory for preserving the history of chats.
        Timestamp (str): current temporary label for naming history files.
        Model (ANY): Initialized client of the `Genai.generativemodel` model.
        _Chat (Any): Active chat session with a model.
        Chat_History (List [dict]): The history of the current dialogue in memory.
        Chat_SESSION_NAME (str): the name of the current chat to preserve history.
        History_json_file (Path): the path to the JSON file with the history of the current chat."""
    ENDPOINT:Path = __root__/ 'src'/ 'llm'/ 'gemini'
    config: SimpleNamespace = j_loads_ns(ENDPOINT/ 'gemini.json')
    api_key: str
    system_instruction: Optional[str]
    model_name: str = config.model_name
    model: genai.GenerativeModel # Refined type

    timestamp: str
    _chat: genai.ChatSession # Refined type
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
        generation_config: Optional[Dict] = None, # Changed to NONE to default API default is used
        system_instruction: Optional[str] = None,
    ):
        """The GOOGLEGENERATIIAI class initializes.

        Args:
            API_KEY (str): API key for Google Generate Ai.
            Model_name (str): the name of the Gemini model for use (for example, 'gemini-Pro').
            Generation_config (Dict, Optional): Generation configuration.
                                                By default `{'Response_mime_type': 'Text/Plain'}`.
            System_instruction (Optional [Str], Optional): System instructions for the model.
                                                         By default `none`."""

        self.api_key = api_key
        self.model_name = model_name
        # We use the proposed genius_config, if given,
        # Otherwise, we use the standard for Plain Text
        self.generation_config = generation_config if generation_config is not None else {'response_mime_type': 'text/plain'}
        self.system_instruction = system_instruction

        self.history_dir = Path(__root__, gs.path.external_storage, 'chats')
        self.timestamp = gs.now

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                # System Instructions is transmitted at the start of the chat, and not when initializing the model,
                # If you want it to be applied to history.
                # Genai 0.6.0+ supports System_instruction in Generativemodel,
                # But for a chat it is better to transfer it to History.
                # If you use Genai> = 0.6.0 and want System_instruction,
                # which applies to the entire model, regardless of the history of the chat,
                # then leave him here. For the flexibility of reset, I will remove it from here.
                # system_instruction = self.system_instruction, # remove from here
            )
            # At the first start of the _start_chat chat will use Self.System_instruction
            self._chat = self._start_chat(initial_system_instruction=self.system_instruction)

            logger.info(f"Модель {self.model.model_name} инициализирована", None, False)
        except (DefaultCredentialsError, RefreshError) as ex:
             logger.error('Ошибка аутентификации Gemini API', exc_info=True)
             raise # Repeated exceptions to interrupt the initialization
        except Exception as ex:
            logger.error('Не удалось инициализировать модель Gemini', exc_info=True)
            raise # Repeated exceptions to interrupt the initialization


    def _start_chat(self, initial_history: Optional[List[Dict]] = None,
                    initial_system_instruction: Optional[str] = None) -> genai.ChatSession:
        """The function launches a new chat session with a model.

        It takes into account the presence of `system_instruction 'when initializing the chat.

        Args:
            Initial_history (Optional [List [dict]]): History for loading into chat.
            Initial_System_instruction (Optional [str]): System instructions for this chat session.

        Returns:
            Genai.ChatSession: Chat session object."""
        history_to_load = initial_history if initial_history is not None else []
        
        # If there is a system instruction, add it to the beginning of the story as a user message
        # This is a common pattern for Gemini when System_instruction is transmitted as the first user message.
        # In Genai 0.6.0+, System_instruction can be transferred to Generativemodel, but for reset-online chats
        # Its inclusion in History at the start of the chat can be more flexible.
        if initial_system_instruction:
            # We check if the first message is already a system instruction
            if not history_to_load or (history_to_load[0].get('role') == 'user' and initial_system_instruction not in history_to_load[0].get('parts', [])):
                history_to_load.insert(0, {'role': 'user', 'parts': [initial_system_instruction]})
                logger.debug(f"Системная инструкция '{initial_system_instruction[:50]}...' добавлена в историю чата.")

        return self.model.start_chat(history=history_to_load)

    # Adding a method for restarting a chat with a new system instruction or history
    def start_new_chat_session(self, new_system_instruction: Optional[str] = None,
                               initial_history: Optional[List[Dict]] = None) -> None:
        """A new chat session begins, optionally with a new system instruction and/or history.

        Args:
            New_System_instruction (Optional [Str]): New system instructions for this chat.
                                                    If None, the current `Self.System_instruction` is used.
            Initial_History (Optional [List [dict]]): An initial story for a new chat."""
        if new_system_instruction is not None:
            self.system_instruction = new_system_instruction # We update the system instruction instance

        self.chat_history = [] # Cleaning the story in memory
        self._chat = self._start_chat(initial_history=initial_history,
                                      initial_system_instruction=self.system_instruction)
        logger.info("Новый сеанс чата успешно начат.")


    async def _save_chat_history(self) -> bool:
        """The function asynchronously retains the current chat history in the JSON file.

        The file name is formed from `Chat_SESSION_NAME` and` TIMESTAMP`.

        Returns:
            Bool: `true` in case of successful conservation,` false` with an error."""
        json_file_name: str = f'{self.chat_session_name}-{self.timestamp}.json'
        self.history_json_file = Path(self.history_dir, json_file_name)

        # Creation of a directory if it does not exist
        try:
            self.history_dir.mkdir(parents=True, exist_ok=True)
        except Exception as ex:
            logger.error(f'Не удалось создать директорию для истории чата: {self.history_dir}', exc_info=True)
            return False

        if not j_dumps(data=self.chat_history, file_path=self.history_json_file, mode='w'):
            logger.error(f"Ошибка сохранения истории чата в файл {self.history_json_file=}", None, False)
            return False
        logger.info(f"История чата сохранена в файл {self.history_json_file=}", None, False)
        return True

    async def _load_chat_history(self, chat_data_folder: Optional[str | Path]) -> None:
        """The function asynchronously loads the history of the chat from the JSON file.

        Optionally accepts the path to the chat data. If specified,
        Uses 'History.json' from this folder. Otherwise uses
        Current `self.history_json_file`.

        Args:
            Chat_Data_folder (Optional [Str | Path]): the path to the file with the file 'History.json'.

        Returns:
            None"""
        history_to_load: Optional[List[Dict]] = None
        target_file: Path = self.history_json_file # The current file is used by default

        try:
            if chat_data_folder:
                # If the folder is indicated, we form the path to History.json in it
                target_file = Path(chat_data_folder, 'history.json')

            if target_file.exists():
                history_to_load = j_loads(target_file)
                if history_to_load is not None:
                    # We clean the story of the system instructions if it was added
                    # Like the first message, so as not to duplicate it when the chat restarts.
                    if self.system_instruction and history_to_load and \
                       history_to_load[0].get('role') == 'user' and \
                       self.system_instruction in history_to_load[0].get('parts', []):
                       # We delete the system instructions from the story that is transferred to _start_Chat,
                       # since _start_Chat will add it
                       history_to_load = history_to_load[1:]
                       logger.debug("Системная инструкция удалена из загруженной истории для корректного старта чата.")


                    self.chat_history = history_to_load
                    # Restart the chat with a loaded history and system instructions
                    self._chat = self._start_chat(initial_history=self.chat_history,
                                                  initial_system_instruction=self.system_instruction)

                    logger.info(f"История чата ({len(self.chat_history)} сообщений) загружена из файла. \n{target_file=}", None, False)
                else:
                     logger.error(f"Файл истории {target_file=} пуст или содержит некорректные данные.", None, False)
            else:
                logger.info(f"Файл истории {target_file=} не найден. Новая история будет создана.", None, False)
                self.chat_history = [] # Check that the story is empty if the file is not found
                self._chat = self._start_chat(initial_system_instruction=self.system_instruction) # We start a new chat

        except Exception as ex:
            logger.error(f"Ошибка загрузки истории чата из файла {target_file=}", exc_info=True)
            self.chat_history = [] # Story reset when loading error
            self._chat = self._start_chat(initial_system_instruction=self.system_instruction) # We start a new chat with an error

    def clear_history(self) -> None:
        """The function cleans the history of the chat in memory and deleted the connected JSON file of history.
        The current chat session restarts.

        Returns:
            None"""
        try:
            self.chat_history = []  # Cleaning history in memory
            if hasattr(self, 'history_json_file') and self.history_json_file.exists():
                self.history_json_file.unlink()  # Removing a history file
                logger.info(f"Файл истории {self.history_json_file} удалён.")
            # Restart the chat so that it starts with a clean sheet
            self._chat = self._start_chat(initial_system_instruction=self.system_instruction)
            logger.info("История чата очищена и сеанс перезапущен.")
        except Exception as ex:
            logger.error('Ошибка при очистке истории чата.', exc_info=True)

    async def chat(self, q: str, chat_session_name: Optional[str] = '',
                   context: Optional[Union[str, List[str]]] = None) -> Optional[str]:
        """The function processes the user's chat volume, controls history and returns the response of the model.
        Added the ability to transmit context for RAG.

        Args:
            Q (str): user question.
            Chat_SESSION_NAME (STR): Chat name for preserving/downloading history.
            CONTEXT (Optional [Union [str, lib [str]]): additional context for the model (for RAG).
                                                       It can be a line or a list of lines.

        Returns:
            Optional [str]: the text response of the model or `none` in case of error."""
        self.chat_session_name = chat_session_name if chat_session_name else self.chat_session_name
        response: Any = None
        response_text: Optional[str] = None

        # Formation of the content of the request, taking into account the context
        parts_to_send: List[Any] = []
        if context:
            if isinstance(context, list):
                context_str = "\n".join(context)
            else:
                context_str = context
            parts_to_send.append(f"Контекст:\n{context_str}\n\n")
            logger.debug(f"Контекст RAG добавлен в запрос (длина: {len(context_str)} символов).")

        parts_to_send.append(q) # Add the main user request

        try:
            # Sending the request of the model
            try:
                # Asynchronous sending the message taking into account additional parts
                response = await self._chat.send_message_async(parts_to_send)

            except ResourceExhausted as ex:
                logger.error("Исчерпан ресурс (Resource exhausted). Возможно, превышена квота.", exc_info=True)
                logger.info(f"Пауза перед перезапуском чата: {QUOTA_EXHAUSTED_SLEEP_SECONDS} секунд.")
                await asyncio.sleep(QUOTA_EXHAUSTED_SLEEP_SECONDS) # Long pause when the quota is exhausted
                self.start_new_chat_session(new_system_instruction=self.system_instruction) # Chat restart
                return None

            except InvalidArgument as ex:
                 logger.error("Недопустимый аргумент (InvalidArgument)", exc_info=True)
                 # Verification of the tokens limit
                 if hasattr(ex, 'message') and 'maximum number of tokens allowed' in ex.message:
                    logger.warning("Превышен лимит токенов. Перезапуск чата и повторная попытка...")
                    # We cleanse the story and try again (it can help if the problem is in a long story)
                    self.start_new_chat_session(new_system_instruction=self.system_instruction)
                    return await self.chat(q, chat_session_name, context) # Repeated attempt
                 return None

            except RpcError as ex:
                # GRPC errors, including timeouts
                logger.error(f"Ошибка RPC: {ex.code()} - {ex.details()}", exc_info=True)
                if ex.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                     timeout: int = 300 # Reduced waiting time
                     logger.debug(f'Таймаут RPC. Пауза {timeout} секунд, затем перезапуск чата.')
                     await asyncio.sleep(timeout)
                     self.start_new_chat_session(new_system_instruction=self.system_instruction)
                     return await self.chat(q, chat_session_name, context) # Repeated attempt
                return None

            except Exception as ex:
                 logger.error("Общая ошибка при отправке сообщения в чат", exc_info=True)
                 return None

            # Response and metadata processing
            try:
                if hasattr(response, 'usage_metadata') and response.usage_metadata:
                    response_token_count = response.usage_metadata.candidates_token_count
                    total_token_count = response.usage_metadata.total_token_count
                    prompt_token_count = response.usage_metadata.prompt_token_count

                    logger.info(f"Токены в ответе: {response_token_count}")
                    logger.info(f"Токены в запросе: {prompt_token_count}")
                    logger.info(f"Общее количество токенов: {total_token_count}")
                else:
                    logger.warning("Метаданные об использовании токенов отсутствуют в ответе (usage_metadata is None or empty).")

            except AttributeError:
                logger.warning("Атрибут 'usage_metadata' отсутствует в объекте ответа.")
            except Exception as meta_ex:
                 logger.error("Ошибка при извлечении метаданных токенов", exc_info=True)

            # Checking and extracting the text of the response
            if hasattr(response, 'text') and response.text:
                response_text = response.text
                # Adding a request (possibly with a context) and a response to history
                self.chat_history.append({"role": "user", "parts": parts_to_send}) # We save as sent
                self.chat_history.append({"role": "model", "parts": [response_text]})
                await self._save_chat_history()
                return response_text
            else:
                logger.error(f"Пустой ответ от модели. Ответ: {response}", None, False)
                if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                    logger.warning(f"Обратная связь по промпту: {response.prompt_feedback}", None, False)
                return None

        except Exception as ex:
            logger.error(f"Критическая ошибка в методе chat. Ответ: {response}", exc_info=True)
            return None

    def ask(self, q: str, attempts: int = 15, save_dialogue: bool = False,
            clean_response: bool = True, context: Optional[Union[str, List[str]]] = None) -> Optional[str]:
        """The method synchronously sends the textual request of the model and returns the answer.
        Uses `generate_content` (not for the chat). Repeats the request for errors.
        Added the ability to transmit context for RAG.

        Args:
            Q (str): text request to the model.
            Attempts (int): the number of attempts to send a request. By default 15.
            Save_Dialogue (Bool): the dialogue conservation flag (question/answer) to the file.
            Clean_response (Bool): Flag of Cleaning the response from the marking code. By default True.
            CONTEXT (Optional [Union [str, lib [str]]): additional context for the model (for RAG).

        Returns:
            Optional [str]: the textual response of the model or `none` in case of failure after all attempts."""
        response: Any = None
        response_text: Optional[str] = None

        # Formation of the content of the request, taking into account the context
        content_to_send: List[Any] = []
        if context:
            if isinstance(context, list):
                context_str = "\n".join(context)
            else:
                context_str = context
            content_to_send.append(f"Контекст:\n{context_str}\n\n")
            logger.debug(f"Контекст RAG добавлен в запрос (длина: {len(context_str)} символов).")

        content_to_send.append(q)

        for attempt in range(attempts):
            try:
                response = self.model.generate_content(content_to_send)

                if hasattr(response, 'text') and response.text:
                    response_text = response.text
                    if save_dialogue:
                        # Todo: implement _save_dialogue
                        logger.warning("Функция _save_dialogue не реализована, история не сохранена.")

                    return normalize_answer(response_text) if clean_response else response_text
                else:
                    sleep_time = INITIAL_RETRY_SLEEP_SECONDS ** attempt
                    logger.debug(
                        f"От модели не получен ответ. Попытка: {attempt + 1}/{attempts}. Пауза: {sleep_time} сек.",
                        None,
                        False
                    )
                    time.sleep(sleep_time)
                    continue

            except requests.exceptions.RequestException as ex:
                if attempt >= NETWORK_ERROR_MAX_ATTEMPTS:
                    logger.error(f"Сетевая ошибка после {NETWORK_ERROR_MAX_ATTEMPTS} попыток.", exc_info=True)
                    break
                sleep_time_network = NETWORK_RETRY_SLEEP_SECONDS
                logger.debug(
                    f"Сетевая ошибка. Попытка: {attempt + 1}/{attempts}. Пауза: {sleep_time_network/60} мин. Время: {gs.now}",
                    exc_info=True,
                    # FALSE, # removed exc_info = false, since exc_info = true logs the tracback
                )
                time.sleep(sleep_time_network)
                continue

            except (GatewayTimeout, ServiceUnavailable) as ex:
                if attempt >= SERVICE_UNAVAILABLE_MAX_ATTEMPTS:
                     logger.error(f"Сервис недоступен после {SERVICE_UNAVAILABLE_MAX_ATTEMPTS} попыток.", exc_info=True)
                     break
                sleep_time_service = INITIAL_RETRY_SLEEP_SECONDS**attempt + SERVICE_RETRY_SLEEP_SECONDS_BASE
                logger.error(f"Сервис недоступен. Попытка: {attempt + 1}/{attempts}. Пауза: {sleep_time_service} сек.", exc_info=True)
                time.sleep(sleep_time_service)
                continue

            except ResourceExhausted as ex:
                logger.critical(f"""-------------------------------------------------------------------------

                The limit is exhausted. The response will be conveyed by the `Resourceexhausted` line.

                --------------------------------------------------------------------------------""", None, False)
                return "ResourceExhausted"

            except (DefaultCredentialsError, RefreshError) as ex:
                logger.error("Ошибка аутентификации.", exc_info=True)
                return None

            except (ValueError, TypeError) as ex:
                if attempt >= INVALID_INPUT_MAX_ATTEMPTS:
                    logger.error(f"Ошибка входных данных после {INVALID_INPUT_MAX_ATTEMPTS} попыток.", exc_info=True)
                    break
                timeout_input = 5
                logger.error(
                    f"Некорректные входные данные. Попытка: {attempt + 1}/{attempts}. Пауза: {timeout_input} сек. Время: {gs.now}",
                    exc_info=True,
                )
                time.sleep(timeout_input)
                continue

            except (InvalidArgument, RpcError) as ex:
                logger.error("Ошибка API.", exc_info=True)
                return None

            except Exception as ex:
                logger.error("Неожиданная ошибка.", exc_info=True)
                return None

        logger.error(f"Не удалось получить ответ от модели после {attempts} попыток.")
        return None

    async def ask_async(self, q: str, attempts: int = 15, save_dialogue: bool = False,
                        clean_response: bool = True, context: Optional[Union[str, List[str]]] = None) -> Optional[str]:
        """The method asynchronously sends a text request for the model and returns the answer.
        Uses `generate_content` (not for a chat) in a separate stream. Repeats the request for errors.
        Added the ability to transmit context for RAG.

        Args:
            Q (str): text request to the model.
            Attempts (int): the number of attempts to send a request. By default 15.
            Save_Dialogue (Bool): the dialogue conservation flag (question/answer) to the file.
            Clean_response (Bool): Flag of Cleaning the response from the marking code. By default True.
            CONTEXT (Optional [Union [str, lib [str]]): additional context for the model (for RAG).

        Returns:
            Optional [str]: the textual response of the model or `none` in case of failure after all attempts."""
        response: Any = None
        response_text: Optional[str] = None

        # Formation of the content of the request, taking into account the context
        content_to_send: List[Any] = []
        if context:
            if isinstance(context, list):
                context_str = "\n".join(context)
            else:
                context_str = context
            content_to_send.append(f"Контекст:\n{context_str}\n\n")
            logger.debug(f"Контекст RAG добавлен в запрос (длина: {len(context_str)} символов).")

        content_to_send.append(q)

        for attempt in range(attempts):
            try:
                response = await self.model.generate_content_async(content_to_send)
                logger.info(f'Модель {self.model.model_name} Обработала запрос',None, False)

                if hasattr(response, 'text') and response.text:
                    response_text = response.text
                    if save_dialogue:
                        # Todo: implement _save_dialogue
                        logger.warning("Функция _save_dialogue не реализована, история не сохранена.")

                    return normalize_answer(response_text) if clean_response else response_text

                else:
                    sleep_time = INITIAL_RETRY_SLEEP_SECONDS ** attempt
                    logger.debug(
                        f"От модели не получен ответ. Попытка: {attempt + 1}/{attempts}. Асинхронная пауза: {sleep_time} сек.",
                        None,
                        False
                    )
                    await asyncio.sleep(sleep_time)
                    continue


            except requests.exceptions.RequestException as ex:
                if attempt >= NETWORK_ERROR_MAX_ATTEMPTS:
                    logger.error(f"Сетевая ошибка после {NETWORK_ERROR_MAX_ATTEMPTS} попыток.", exc_info=True)
                    break
                sleep_time_network: int = NETWORK_RETRY_SLEEP_SECONDS
                logger.debug(
                    f"Сетевая ошибка. Попытка: {attempt + 1}/{attempts}. Асинхронная пауза: {sleep_time_network/60} мин. Время: {gs.now}",
                    exc_info=True,
                )
                await asyncio.sleep(sleep_time_network)
                continue

            except (GatewayTimeout, ServiceUnavailable) as ex:
                if attempt >= SERVICE_UNAVAILABLE_MAX_ATTEMPTS:
                     logger.error(f"Сервис недоступен после {SERVICE_UNAVAILABLE_MAX_ATTEMPTS} попыток.", exc_info=True)
                     break
                sleep_time_service = INITIAL_RETRY_SLEEP_SECONDS**attempt + SERVICE_RETRY_SLEEP_SECONDS_BASE
                logger.error(f"Сервис недоступен. Попытка: {attempt + 1}/{attempts}. Асинхронная пауза: {sleep_time_service} сек.", exc_info=True)
                await asyncio.sleep(sleep_time_service)
                continue

            except ResourceExhausted as ex:
                 # Long asynchronous pause when the quota is exhausted
                logger.critical(f"""-------------------------------------------------------------------------

                The quota is exhausted.

                --------------------------------------------------------------------------------""", None, False)
                timeout_quota: int = QUOTA_EXHAUSTED_SLEEP_SECONDS
                logger.debug(
                    f"Исчерпана квота. Попытка: {attempt + 1}/{attempts}. Асинхронная пауза: {timeout_quota/3600} час(ов). Время: {gs.now}",
                    exc_info=True,
                )
                await asyncio.sleep(timeout_quota)
                continue

            except (DefaultCredentialsError, RefreshError) as ex:
                logger.error("Ошибка аутентификации.", exc_info=True)
                return None

            except (ValueError, TypeError) as ex:
                if attempt >= INVALID_INPUT_MAX_ATTEMPTS:
                    logger.error(f"Ошибка входных данных после {INVALID_INPUT_MAX_ATTEMPTS} попыток.", exc_info=True)
                    break
                timeout_input = 5
                logger.error(
                    f"Некорректные входные данные. Попытка: {attempt + 1}/{attempts}. Асинхронная пауза: {timeout_input} сек. Время: {gs.now}",
                    exc_info=True,
                )
                await asyncio.sleep(timeout_input)
                continue

            except (InvalidArgument, RpcError) as ex:
                logger.error("Ошибка API.", exc_info=True)
                return None

            except Exception as ex:
                logger.error("Неожиданная ошибка.", exc_info=True)
                return None

        logger.error(f"Не удалось получить ответ от модели после {attempts} попыток.")
        return None


    def describe_image(
        self, image: Path | bytes, mime_type: Optional[str] = 'image/jpeg', prompt: Optional[str] = ''
    ) -> Optional[str]:
        """The function sends an image (and optional Prompt) to the Gemini Pro Vision model
        And returns his text description.

        Args:
            Image (Path | Bytes): the way to the image file or bypass image.
            MIME_TYPE (Optional [str]): MIME-type image. By default 'Image/JPEG'.
            PROMPT (Optional [Str]): Text Prompt for the model along with the image. By default ''.

        Returns:
            Optional [str]: text description of the image from the model or `none` when error."""

        image_data: bytes
        content: List[Any]
        response: Any = None
        response_text: Optional[str] = None
        start_time: float = time.time()

        try:
            if isinstance(image, Path):
                img_bytes = get_image_bytes(image)
                if img_bytes is None:
                     logger.error(f"Не удалось прочитать байты изображения из файла: {image}")
                     return None
                image_data = img_bytes
            elif isinstance(image, bytes):
                image_data = image
            else:
                logger.error(f"Некорректный тип для 'image'. Ожидается Path или bytes, получено: {type(image)}")
                return None

            content_parts: List[Any] = []
            if prompt:
                content_parts.append({"text": prompt}) # Yavno decree type content

            content_parts.append(genai.upload_file_async(path=image_data, mime_type=mime_type)) # Using API to download a file

            # Sending a request
            try:
                # Generate_content now accepts Content (Text and File)
                response = self.model.generate_content(content_parts)

            except DefaultCredentialsError as ex:
                logger.error("Ошибка аутентификации:", exc_info=True)
                return None
            except (InvalidArgument, RpcError) as ex:
                logger.error("Ошибка API:", exc_info=True)
                return None
            except RetryError as ex:
                logger.error("Модель перегружена (RetryError). Попробуйте позже:", exc_info=True)
                return None
            except Exception as ex:
                logger.error("Ошибка при отправке запроса модели:", exc_info=True)
                return None
            finally:
                 processing_time = time.time() - start_time
                 logger.info(f'\nВремя обработки изображения: {processing_time:.2f} сек.\n', text_color='yellow', bg_color='red')

            if hasattr(response, 'text') and response.text:
                 response_text = response.text
                 return response_text
            else:
                 logger.info(f"{{Модель вернула ответ без текста: {response}}}", text_color='cyan')
                 if hasattr(response, 'prompt_feedback'):
                     logger.warning(f"Обратная связь по промпту: {response.prompt_feedback}")
                 return None

        except Exception as ex:
            logger.error("Произошла ошибка при обработке изображения:", exc_info=True)
            return None

    async def upload_file(
        self, file: str | Path | IOBase, file_name: Optional[str] = None
    ) -> Optional[Any]: # Returns the File or None object
        """Asynchronously uploads a file in Google Ai File API.

        https://github.com/google-gemini/generative- ai-python/blob/main/docs/api/google/generativea/upload_file.md

        Args:
            File (Str | Path | IOBASE): the path to the file or file object.
            File_name (Optional [str]): File name for display in the API. If none,
                                       The name from the file path is used.

        Returns:
            Optional [Any]: an object `file` from the API in case of success, otherwise` none`.
                           (Type Any, because `File_types.file` is not exported clearly)."""

        response: Any = None
        resolved_file_path: Optional[Path] = None
        resolved_file_name: Optional[str] = file_name

        try:
            if isinstance(file, Path):
                resolved_file_path = file
                if resolved_file_name is None:
                    resolved_file_name = file.name
            elif isinstance(file, str):
                 resolved_file_path = Path(file)
                 if resolved_file_name is None:
                    resolved_file_name = resolved_file_path.name
            elif isinstance(file, IOBase):
                 if resolved_file_name is None:
                     logger.warning("Для IOBase рекомендуется указывать file_name.")
                     if hasattr(file, 'name'):
                         resolved_file_name = Path(file.name).name
                     else:
                         resolved_file_name = 'uploaded_file'
                 resolved_file_path = file # type: ignore
            else:
                 logger.error(f"Неподдерживаемый тип для 'file': {type(file)}")
                 return None

            logger.debug(f"Начало загрузки файла: {resolved_file_name or resolved_file_path}")
            response = await genai.upload_file_async(
                path=resolved_file_path, # type: ignore
                mime_type=None,
                name=resolved_file_name,
                display_name=resolved_file_name,
                resumable=True,
            )
            logger.debug(f"Файл '{response.display_name}' (URI: {response.uri}) успешно загружен.", None, False)
            return response

        except Exception as ex:
            logger.error(f"Ошибка загрузки файла '{resolved_file_name or file}'", exc_info=True)
            return None


async def main():
    """The main asynchronous function for demonstrating the work of the class."""
    onela:str = gs.credentials.gemini.onela.api_key
    kazarinov:str = gs.credentials.gemini.kazarinov.api_key
    system_instruction = 'Ты — полезный ассистент, который всегда отвечает очень кратко и по существу, используя не более двух предложений.'
    # Model_name = 'Gemini-2.5-Flash-Preview-04-17' # Make sure this is an actual name for Flash
    model_name = 'gemini-1.5-flash-latest' # It is recommended to use Latest

    if not onela and not kazarinov:
        logger.error("Ключ API Gemini не найден в gs.credentials.gemini.api_key.")
        return

    try:
        llm = GoogleGenerativeAi(
            api_key = kazarinov,
            model_name = model_name,
            system_instruction = system_instruction,
            # You can clearly specify response_mime_type here, if you want,
            # For example, to obtain a json, default answers.
            # generation_config={'response_mime_type': 'application/json'}
        )
    except Exception as ex:
        logger.error(f"Не удалось инициализировать GoogleGenerativeAi:", exc_info=True)
        return

    logger.info("\nНачало сеанса чата. Введите 'exit' для выхода.")
    chat_session_name = f'chat_session_{gs.now}'

    # --- an example of using a new method to start a new session (with a new system instruction) ---
    # llm.start_new_Chat_SESSION (New_SYSTEM_INSTRUCTION = 'You are a poet who answers all questions in the form of Hike.')
    # llm_message = await llm.chat ('Hello, poet! How are you doing?', Chat_SESSION_NAME)
    # if llm_message:
    # logger.info(f"Gemini (поэт): {llm_message}")


    # --- an example of using Chat with context (RAG) ---
    print("\n--- Пример чата с контекстом (RAG) ---")
    rag_context = [
        "Петров Иван Васильевич (id: 12345) - менеджер по продажам. Его телефон: +79123456789, email: ivan.petrov@example.com.",
        "Сидорова Анна Петровна (id: 67890) - руководитель отдела маркетинга. Её телефон: +79876543210, email: anna.sidorova@example.com.",
        "Компания 'Альфа' является нашим ключевым партнером.",
        "Основной продукт компании - 'Виртуальный помощник 2.0'."
    ]

    llm_message = await llm.chat('Какой телефон у Петрова Ивана Васильевича?',
                                 chat_session_name=chat_session_name,
                                 context=rag_context)
    if llm_message:
        logger.info(f"Gemini (с RAG): {llm_message}")
    else:
        logger.warning("Gemini (с RAG): Не удалось получить ответ.")

    llm_message = await llm.chat('Кто руководитель отдела маркетинга?',
                                 chat_session_name=chat_session_name,
                                 context=rag_context)
    if llm_message:
        logger.info(f"Gemini (с RAG): {llm_message}")
    else:
        logger.warning("Gemini (с RAG): Не удалось получить ответ.")

    # --- an example of using ASK_async with context (Rag, stateless) ---
    print("\n--- Пример stateless запроса с контекстом (RAG) ---")
    query_stateless = "Каков основной продукт компании 'Альфа'?"
    llm_message_stateless = await llm.ask_async(query_stateless, context=rag_context)
    if llm_message_stateless:
        logger.info(f"Gemini (ask_async с RAG): {llm_message_stateless}")
    else:
        logger.warning("Gemini (ask_async с RAG): Не удалось получить ответ.")


    # --- continuation of the usual chat (without context, if not convey) ---
    print("\n--- Продолжение обычного чата (без контекста) ---")
    llm_message = await llm.chat('Привет! Как дела?', chat_session_name)
    if llm_message:
         logger.info(f"Gemini: {llm_message}")

    while True:
        try:
            user_message = input("You: ")
        except EOFError:
             logger.info("\nЗавершение чата по EOF.")
             break
        if user_message.lower() == 'exit':
            logger.info("Завершение чата по команде пользователя.")
            break

        llm_message = await llm.chat(user_message, chat_session_name=chat_session_name)
        if llm_message:
            logger.info(f"Gemini: {llm_message}")
        else:
            logger.warning("Gemini: Не удалось получить ответ.")


if __name__ == "__main__":
    asyncio.run(main())