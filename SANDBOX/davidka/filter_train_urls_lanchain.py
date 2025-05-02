## \file path/to/your/file.py # Укажите правильный путь
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для асинхронной классификации URL-адресов с использованием Gemini LLM.
=============================================================================
Модуль определяет тип веб-страницы (товар, категория, главная и т.д.)
на основе её URL, используя модель Google Gemini через LangChain.
Он загружает инструкции для LLM из файла и сохраняет результаты
классификации в JSON-файл.

Зависимости:
    - langchain
    - langchain-google-genai
    - pathlib
    - src.gs (предполагается наличие)
    - src.utils.file (предполагается наличие)
    - src.utils.jjson (предполагается наличие)
    - src.logger (предполагается наличие)
    - SANDBOX.davidka.utils (предполагается наличие)

 ```rst
 .. module:: src.module_name.file_name # Укажите правильный модуль
 ```
"""

import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, Union # Union будет заменен на |

from typing import Optional

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chains import LLMChain

# Всегда импортируем header и __root__
import header
from header import __root__
# Импортируем gs (предполагается его наличие и конфигурация)
from src import gs
# Импортируем утилиты
from src.utils.file import read_text_file # Убедитесь, что функция существует
from src.utils.jjson import j_dumps, j_loads, j_loads_ns
# Импортируем функцию для получения URL (убедитесь, что она существует)
from SANDBOX.davidka.utils import fetch_urls_from_all_mining_files

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from src.logger import logger # Предполагается импорт логгера проекта
from src.utils.printer import pprint as print



class Config:
    GEMINI_API_KEY: str = gs.credentials.gemini.onela.api_key
    GEMINI_MODEL_NAME: str = 'gemini-2.5-flash-preview-04-17'

def initialize_gemini(api_key: Optional[str] = None, model_name: Optional[str] = None) -> BaseChatModel | None:
    """
    Функция синхронно инициализирует и возвращает клиент модели Gemini.

    Args:
        api_key (Optional[str], optional): API ключ для Gemini. По умолчанию используется из `Config`.
        model_name (Optional[str], optional): Имя модели Gemini. По умолчанию используется из `Config`.

    Returns:
        BaseChatModel | None: Инициализированный объект ChatGoogleGenerativeAI или None в случае ошибки.

    Raises:
        None: Ошибки логируются, исключения не пробрасываются наружу.
    """
    api_key: str = api_key if api_key else Config.GEMINI_API_KEY
    model_name: str  = model_name if model_name else Config.GEMINI_MODEL_NAME


    try:
        return ChatGoogleGenerativeAI(
            apy_key=api_key,
            model=model_name,
            # temperature=0.1,
            # convert_system_message_to_human=True # Оставляем для совместимости
        )

        return 
    except Exception as ex:
        # Логирование ошибки при возникновении исключения во время инициализации
        logger.error('Ошибка инициализации Gemini.', ex, exc_info=True)
        # Возврат None при любом исключительном событии
        return None

async def build_chain(llm: BaseChatModel) -> LLMChain | None:
    """
    Функция асинхронно строит и возвращает цепочку LLMChain для модели Gemini.
    Загружает шаблон промпта из файла.

    Args:
        llm (BaseChatModel): Инициализированный клиент LLM.

    Returns:
        LLMChain | None: Созданная цепочка LangChain или None в случае ошибки чтения файла.
    """
    # Объявление переменных
    prompt_template: PromptTemplate | None = None
    prompt_content: str | None = None
    chain: LLMChain | None = None
    # Путь к файлу с инструкциями
    instruction_file: Path = Config.ENDPOINT /'instructions'/ 'filter_urls.md'

    try:
        # Чтение содержимого файла с инструкциями
        prompt_content = read_text_file(instruction_file)
        if not prompt_content:
             logger.error(f'Не удалось прочитать файл инструкций: {instruction_file}')
             return None

        # Создание шаблона промпта
        prompt_template = PromptTemplate(
            input_variables=['TARGET_URL'],
            template=prompt_content
        )
        # Создание и возврат цепочки
        chain = LLMChain(llm=llm, prompt=prompt_template)
        return chain

    except FileNotFoundError:
        logger.error(f"Файл с инструкциями не найден: {instruction_file}")
        return None
    except Exception as ex:
        logger.error(f"Ошибка при построении цепочки LLMChain: {ex}", exc_info=True)
        return None


async def get_page_category(url: str, chain: LLMChain) -> str | None:
    """
    Функция асинхронно вызывает цепочку LLMChain с использованием `ainvoke`
    и получает строковый результат классификации URL.

    Args:
        url (str): URL-адрес для классификации.
        chain (LLMChain): Предварительно созданная цепочка LLMChain.

    Returns:
        str | None: Строка с ответом LLM (предположительно JSON) или None в случае ошибки.
    """
    # Объявление переменной
    response_str: str | None = None

    try:
        # Асинхронный вызов цепочки с использованием ainvoke
        # ainvoke для LLMChain возвращает строку
        response_str = await chain.ainvoke({'TARGET_URL': url})
        # Удаление возможных лишних пробелов/переносов строк из ответа LLM
        return response_str.strip() if response_str else None
    except Exception as ex:
        # Логирование ошибки при вызове цепочки
        logger.error(f'Ошибка при вызове chain.ainvoke для URL {url}', ex, exc_info=True)
        return None # Возвращаем None в случае исключения


async def main():
    """
    Основная асинхронная функция для запуска процесса классификации URL.
    Инициализирует LLM, читает URL, вызывает классификатор и сохраняет результаты.
    """
    # --- Объявление переменных ---
    gemini_llm: BaseChatModel | None = None
    chain: LLMChain | None = None
    # Путь к файлу для сохранения результатов (используем относительный путь)
    results_dir: Path = __root__ / 'output' # Папка для результатов в корне проекта
    results_dir.mkdir(exist_ok=True) # Создаем папку, если её нет
    filtered_urls_file: Path = results_dir / 'filtered_urls_results.json'
    data_dict: Dict[str, Any] = {} # Словарь для хранения результатов URL -> JSON-строка ответа
    urls_to_process: list[str] = []
    url: str | None = None # Текущий URL в цикле
    llm_response_str: str | None = None # Строковый ответ от LLM
    json_dump_result: str | None = None # Результат j_dumps

    # --- Инициализация ---
    logger.info('Запуск процесса классификации URL...')
    gemini_llm = initialize_gemini() # Используем значения из Config

    if not gemini_llm:
        logger.error('Не удалось инициализировать Gemini LLM. Выход.')
        return # Завершаем выполнение, если LLM не инициализирован

    # Строим цепочку один раз
    chain = await build_chain(gemini_llm)
    if not chain:
        logger.error('Не удалось построить цепочку LLMChain. Выход.')
        return # Завершаем выполнение, если цепочку не удалось создать

    # --- Загрузка данных ---
    logger.info(f'Попытка загрузки предыдущих результатов из: {filtered_urls_file}')
    if filtered_urls_file.exists():
        data_dict = j_loads(filtered_urls_file) # Загружаем существующие результаты
        if not isinstance(data_dict, dict):
             logger.warning(f'Файл {filtered_urls_file} не содержит словарь. Начинаем с пустого словаря.')
             data_dict = {}
        else:
             logger.info(f'Загружено {len(data_dict)} записей из файла.')
    else:
        logger.info('Файл с предыдущими результатами не найден. Будет создан новый.')
        data_dict = {}

    # Получение списка URL для обработки
    # Убедитесь, что функция fetch_urls_from_all_mining_files существует и возвращает list[str]
    try:
        # Замените ключи на актуальные для вашей функции
        urls_to_process = fetch_urls_from_all_mining_files(['random_urls', 'output_product_data_set1'])
        logger.info(f'Получено {len(urls_to_process)} URL для обработки.')
    except Exception as ex:
        logger.error("Ошибка при получении списка URL", ex, exc_info=True)
        return # Завершаем, если не можем получить URL

    # --- Обработка URL ---
    processed_count: int = 0
    saved_count: int = 0
    for url in urls_to_process:
        processed_count += 1
        logger.info(f'Обработка URL {processed_count}/{len(urls_to_process)}: {url}')

        # Пропуск уже обработанных URL
        if url in data_dict:
            logger.info(f'URL {url} уже есть в результатах, пропускаем.')
            continue

        # Вызов функции классификации
        llm_response_str = await get_page_category(url, chain)

        if llm_response_str:
            # Сохраняем сырой строковый ответ от LLM
            # j_dumps здесь просто создает JSON-строку из строки ответа LLM
            # Это может быть избыточно, если llm_response_str УЖЕ валидный JSON.
            # Если вы хотите сохранить именно распарсенный объект, нужно добавить j_loads_ns(llm_response_str)
            json_dump_result = j_dumps(llm_response_str) # Дамп строки как JSON строки
            data_dict[url] = json_dump_result # Сохраняем результат дампа
            logger.info(f'Успешно получен ответ для {url}.')
            print(f'Результат для {url}: {json_dump_result}') # Используем проектный или стандартный print
            saved_count += 1
        else:
            # Сохраняем информацию об ошибке, если ответа нет
            data_dict[url] = j_dumps({'error': 'failed_to_get_response'}) # Дамп словаря ошибки
            logger.warning(f'Не удалось получить ответ для URL: {url}')

        # Периодическое сохранение (например, каждые 10 новых результатов)
        if saved_count > 0 and saved_count % 10 == 0:
             logger.info(f'Сохранение промежуточных результатов ({len(data_dict)} записей)...')
             j_dumps(data_dict, filtered_urls_file, indent=2) # Сохраняем обновленный словарь в файл
             logger.info('Промежуточные результаты сохранены.')
             # Сбрасываем счетчик сохраненных, чтобы избежать повторного сохранения без новых данных
             saved_count = 0


    # --- Финальное сохранение ---
    logger.info('Обработка всех URL завершена. Финальное сохранение результатов...')
    j_dumps(data_dict, filtered_urls_file, indent=2) # Запись итогового словаря в файл
    logger.info(f'Финальные результаты сохранены в файл: {filtered_urls_file}')


# Запуск асинхронной основной функции
if __name__ == '__main__':
    # Проверка наличия API ключа (простая)
    if not Config.GEMINI_API_KEY:
        logger.error("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        logger.error("!!! API ключ Gemini не найден в Config.GEMINI_API_KEY      !!!")
        logger.error("!!! Укажите ключ перед запуском.                           !!!")
        logger.error("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        # Запуск асинхронного кода
        asyncio.run(main())
