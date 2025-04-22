## \file src/webdriver/ai_browser/use_ai.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для запуска задач с использованием LLM через LangChain и кастомного Agent.

Предоставляет функциональность для:
- Конфигурирования моделей (Gemini, OpenAI) через словарь.
- Установки API ключей в переменные окружения при старте из gs.credentials.
- Запуска задачи на ВСЕХ активных моделях.
- Сбора и возврата результатов от каждой активной модели.

Зависимости:
    - langchain-openai
    - langchain-google-genai
    - langchain-core
    - python-dotenv
    - browser_use (кастомный модуль Agent)
    - src.gs (кастомный модуль)
    - src.logger (кастомный модуль)

.. module:: src.webdriver.ai_browser.use_ai
"""

import os
import asyncio
from typing import List, Dict, Any, Optional, Callable, Type, Tuple
from pathlib import Path

# LangChain компоненты
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel # Базовый класс для type hinting
from langchain_core.exceptions import LangChainException # Для обработки ошибок LangChain

# Ваш класс Agent (убедитесь, что он импортирован правильно)
from browser_use import Agent # Пример: если browser_use находится в корне src

from dotenv import load_dotenv
load_dotenv() # Функция загружает переменные окружения из .env файла

# Ваши внутренние модули
import header # type: ignore
from header import __root__ # type: ignore
from src import gs # type: ignore
from src.utils.jjson import j_loads # type: ignore
from src.logger import logger


# --- Класс Конфигурации (API ключи устанавливаются в env) ---
class Config:
    """
    Класс для хранения статической конфигурации приложения.

    Содержит словарь доступных моделей, список URL для обработки,
    и шаблон задачи. API КЛЮЧИ УСТАНАВЛИВАЮТСЯ В ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ
    ПРИ ОПРЕДЕЛЕНИИ КЛАССА из `gs.credentials`.
    """
    ENDPOINT:Path = __root__/ 'src'/ 'webdriver'/ 'ai_browser'
    config: Dict[str, Any] = j_loads(ENDPOINT/ 'use_ai.json')
    models_to_use: Dict[str, Dict[str, str]] = config['models_to_use']

    # --- Установка API ключей в переменные окружения ---
    try:
        _gemini_key_source = 'gs.credentials.gemini.kazarinov' # В
        gemini_key = getattr(gs.credentials.gemini, 'kazarinov', None)
        os.environ['GEMINI_API_KEY'] = gemini_key if gemini_key else ''
        if not os.environ.get('GEMINI_API_KEY'): # Используем get для большей безопасности
            logger.warning(f"Ключ API Gemini не найден в '{_gemini_key_source}'. Переменная окружения GEMINI_API_KEY пуста.")
        else:
            logger.debug("Ключ API Gemini установлен в переменную окружения GEMINI_API_KEY.")

        _openai_key_source = 'gs.credentials.openai.hypotez.api_key'
        openai_hypotez_creds = getattr(gs.credentials.openai, 'hypotez', None)
        openai_key = getattr(openai_hypotez_creds, 'api_key', None) if openai_hypotez_creds else None
        os.environ['OPENAI_API_KEY'] = openai_key if openai_key else ''
        if not os.environ.get('OPENAI_API_KEY'): # Используем get для большей безопасности
            logger.warning(f"Ключ API OpenAI не найден в '{_openai_key_source}'. Переменная окружения OPENAI_API_KEY пуста.")
        else:
            logger.debug("Ключ API OpenAI установлен в переменную окружения OPENAI_API_KEY.")

    except AttributeError as e:
        logger.error(f"Ошибка доступа к атрибутам gs.credentials при установке ключей API: {e}. Убедитесь, что структура gs.credentials корректна.", exc_info=False)
        os.environ.setdefault('GEMINI_API_KEY', '')
        os.environ.setdefault('OPENAI_API_KEY', '')
        logger.warning("Переменные окружения GEMINI_API_KEY и OPENAI_API_KEY установлены в пустые строки из-за ошибки доступа к gs.credentials.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при установке ключей API в переменные окружения: {e}", exc_info=True)
        os.environ.setdefault('GEMINI_API_KEY', '')
        os.environ.setdefault('OPENAI_API_KEY', '')
        logger.warning("Переменные окружения GEMINI_API_KEY и OPENAI_API_KEY установлены в пустые строки из-за неожиданной ошибки.")



# --- Вспомогательные функции ---

def _get_active_model_configs(models_config: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    """
    Фильтрует словарь конфигураций моделей, оставляя только активные.

    Args:
        models_config: Словарь с конфигурациями всех моделей.

    Returns:
        Словарь, содержащий только конфигурации моделей со статусом 'active'.
    """
    active_models = {}
    if not isinstance(models_config, dict):
        logger.error("Некорректный формат 'models_to_use'. Ожидается словарь.")
        return active_models # Возвращаем пустой словарь

    for provider_key, model_details in models_config.items():
        if isinstance(model_details, dict) and model_details.get('status') == 'active':
            if model_details.get('model_name'):
                active_models[provider_key] = model_details
                logger.debug(f"Модель '{provider_key}' ({model_details.get('model_name')}) активна.")
            else:
                 logger.warning(f"Активная модель '{provider_key}' пропущена: отсутствует ключ 'model_name'.")
        elif isinstance(model_details, dict) and model_details.get('status') != 'active':
             logger.debug(f"Модель '{provider_key}' не активна (status='{model_details.get('status')}').")
        else:
            logger.warning(f"Некорректная конфигурация для провайдера '{provider_key}'. Пропускается.")

    return active_models

def _initialize_llm(provider_key: str, model_details: Dict[str, str]) -> Optional[BaseChatModel]:
    """
    Инициализирует экземпляр LLM на основе провайдера и конфигурации.

    Читает API ключ из переменных окружения.

    Args:
        provider_key: Идентификатор провайдера (например, 'gemini', 'openai').
        model_details: Словарь с конфигурацией модели (должен содержать 'model_name').

    Returns:
        Инициализированный экземпляр BaseChatModel или None в случае ошибки.
    """
    provider_type = provider_key.lower()
    model_name = model_details.get('model_name') # Уже проверено в _get_active_model_configs

    logger.info(f"Попытка инициализации модели: Провайдер='{provider_key}', Имя='{model_name}'")

    try:
        if provider_type == 'gemini':
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                logger.error(f'Инициализация Gemini "{model_name}" невозможна: ключ GEMINI_API_KEY отсутствует или пуст.')
                return None
            llm_instance = ChatGoogleGenerativeAI(model=model_name, api_key=api_key, convert_system_message_to_human=True)
            logger.info(f'Модель Gemini "{model_name}" успешно инициализирована.')
            return llm_instance

        elif provider_type == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                logger.error(f'Инициализация OpenAI "{model_name}" невозможна: ключ OPENAI_API_KEY отсутствует или пуст.')
                return None
            llm_instance = ChatOpenAI(model=model_name, api_key=api_key)
            logger.info(f'Модель OpenAI "{model_name}" успешно инициализирована.')
            return llm_instance

        # Добавьте сюда elif для других провайдеров, если необходимо
        # elif provider_type == 'anthropic':
        #    api_key = os.getenv('ANTHROPIC_API_KEY') # Пример
        #    # ... инициализация Anthropic ...

        else:
            logger.warning(f"Неизвестный тип провайдера '{provider_key}'. Невозможно инициализировать модель '{model_name}'.")
            return None

    except LangChainException as lc_err:
        logger.error(f'Ошибка LangChain при инициализации модели: Провайдер="{provider_key}", Имя="{model_name}". Ошибка: {lc_err}', exc_info=False) # exc_info=False для краткости
        return None
    except Exception as init_err:
        logger.error(f'Неожиданная ошибка инициализации модели: Провайдер="{provider_key}", Имя="{model_name}". Ошибка: {init_err}', exc_info=True)
        return None


# --- Основная логика выполнения задачи ---

async def _run_agent_task(llm: BaseChatModel, task: str, provider_key: str) -> Optional[str]:
    """
    Инициализирует и запускает Agent с предоставленной моделью и задачей.
    (Модифицировано для логирования имени провайдера)

    Args:
        llm (BaseChatModel): Инициализированный экземпляр LLM.
        task (str): Текст задачи для выполнения Agent'ом.
        provider_key (str): Имя провайдера для логирования.

    Returns:
        Optional[str]: Результат выполнения задачи Agent'ом в виде строки,
                       или None в случае ошибки или если Agent вернул None.
    """
    try:
        agent = Agent(
            task=task,
            llm=llm,
        )
        task_preview: str = task[:100].replace(os.linesep, ' ')
        model_identifier: str = getattr(llm, "model", "N/A") # Уточняем модель, если доступно
        logger.info(f'Агент [{provider_key}] с моделью {llm.__class__.__name__} ({model_identifier}) начинает выполнение задачи: "{task_preview}..."')

        # --- ВАЖНО: Убедитесь, что agent.run() асинхронный ---
        # Если agent.run() синхронный, его нужно запускать в executor:
        # result: Any = await asyncio.to_thread(agent.run)
        # Если он асинхронный (async def run(...)):
        result: Any = await agent.run()
        # ----------------------------------------------------

        logger.info(f'Агент [{provider_key}] с моделью {llm.__class__.__name__} ({model_identifier}) завершил выполнение задачи.')

        if result:
            return result
        else:
            logger.warning(f'Агент [{provider_key}] вернул None.')
            return None

    except Exception as agent_err:
        model_identifier_on_error: str = getattr(llm, "model", "N/A")
        logger.error(f'Ошибка во время инициализации или выполнения задачи агентом [{provider_key}] с моделью {llm.__class__.__name__} ({model_identifier_on_error}): {agent_err}', exc_info=True)
        return None # Возвращаем None при ошибке агента


async def run_task_on_active_models(
    task: str,
    app_config: Config = Config,    
) -> Optional[Dict[str, Optional[str]]]:
    """
    Выполняет задачу на ВСЕХ активных моделях из конфигурации асинхронно.

    1. Получает конфигурации активных моделей.
    2. Пытается инициализировать каждую активную модель.
    3. Запускает выполнение задачи (`_run_agent_task`) параллельно для всех
       успешно инициализированных моделей с помощью `asyncio.gather`.
    4. Собирает результаты (или None в случае ошибок) в словарь.

    Args:
        app_config (Config): Экземпляр конфигурации приложения.
        task (str): Текст задачи для передачи агенту.

    Returns:
        Optional[Dict[str, Optional[str]]]: Словарь, где ключ - идентификатор модели
        (например, 'gemini' или 'openai'), а значение - результат (str) или None (при ошибке).
        Возвращает None, если ни одна модель в конфигурации не была активной или
        если произошла критическая ошибка при подготовке задач.
    """
    # 1. Получить активные конфигурации
    active_models:dict = _get_active_model_configs(app_config.models_to_use)
    results: Dict[str, Optional[str]] = {}
    tasks_to_run: List[Tuple[str, asyncio.Task]] = [] # Список для хранения (provider_key, asyncio_task)

    if not active_models:
        logger.error("В конфигурации не найдено ни одной активной и корректно описанной модели. Задачи не будут запущены.")
        return None # Возвращаем None, если нет активных моделей

    logger.info(f"Запуск задачи на активных моделях: {list(active_models.keys())}")


    # 2. Инициализировать модели и подготовить задачи
    for provider_key, model_details in active_models.items():
        llm_instance = _initialize_llm(provider_key, model_details)

        if llm_instance:
            # Создаем корутину для запуска _run_agent_task
            agent_coro = _run_agent_task(llm_instance, task, provider_key)
            # Оборачиваем корутину в asyncio.Task для gather
            asyncio_task = asyncio.create_task(agent_coro, name=f"AgentTask_{provider_key}")
            tasks_to_run.append((provider_key, asyncio_task))
        else:
            # Если инициализация не удалась, сразу записываем None в результат
            logger.warning(f"Пропуск запуска задачи для модели '{provider_key}' из-за ошибки инициализации.")
            results[provider_key] = None

    if not tasks_to_run:
        logger.warning("Не удалось подготовить ни одной задачи для запуска (все активные модели не инициализировались?).")
        # Возвращаем словарь с None для всех активных, но неинициализированных моделей
        return results # results уже содержит None для них

    # 3. Запустить задачи параллельно и собрать результаты
    provider_keys_in_gather = [key for key, _ in tasks_to_run]
    coroutines_in_gather = [task for _, task in tasks_to_run]

    logger.info(f"Запуск {len(coroutines_in_gather)} задач агентов параллельно...")
    # return_exceptions=True позволяет получить исключение как результат вместо падения gather
    gathered_results = await asyncio.gather(*coroutines_in_gather, return_exceptions=True)
    logger.info("Все задачи агентов завершены.")

    # 4. Обработать результаты (включая возможные исключения)
    for i, provider_key in enumerate(provider_keys_in_gather):
        result_or_exception = gathered_results[i]
        print(result_or_exception)
        if isinstance(result_or_exception, Exception):
            logger.error(f"Задача для провайдера '{provider_key}' завершилась с исключением: {result_or_exception}", exc_info=False) # exc_info=False, т.к. исключение уже содержит трассировку
            results[provider_key] = None # Ошибка во время выполнения _run_agent_task
        elif result_or_exception is None:
             logger.warning(f"Задача для провайдера '{provider_key}' вернула None.")
             results[provider_key] = None # Агент вернул None или была ошибка внутри _run_agent_task
        else:
             results[provider_key] = result_or_exception # Успешный результат (строка)

    return results


async def main() -> None:
    """
    Основная асинхронная точка входа для запуска обработки страниц.

    Создает конфигурацию (при этом устанавливаются ключи API в env),
    итерирует по списку URL, формирует задачу и запускает ее выполнение
    на всех активных моделях с помощью `run_task_on_active_models`.
    Выводит полученные результаты в консоль.
    """
    # Создание экземпляра Config (устанавливает env vars)
    app_config = Config()

    logger.info("Начало обработки списка страниц товаров...")

    num_pages: int = len(app_config.product_pages_list)
    for i, product_page in enumerate(app_config.product_pages_list, 1):
        logger.info(f"--- Обработка страницы {i}/{num_pages}: {product_page} ---")

        current_task: str = f"Перейди на страницу {product_page}\n{app_config.task_description}"

        # Запуск задачи на всех активных моделях
        all_results: Optional[Dict[str, Optional[str]]] = await run_task_on_active_models(
            app_config=app_config,
            task=current_task
        )

        # Обработка словаря результатов
        print(f"\n--- Результаты для страницы {product_page} ---")
        if all_results is not None:
            if not all_results:
                 print("   Нет результатов для отображения (возможно, не было активных моделей или все завершились ошибкой?).")
            else:
                # Сортируем для консистентного вывода
                for model_key in sorted(all_results.keys()):
                    result = all_results[model_key]
                    print(f"  Результат от модели '{model_key}':")
                    if result is not None:
                        # Ограничим вывод для читаемости в консоли
                        output_preview = result[:500] + ('...' if len(result) > 500 else '')
                        print(f"    ```\n    {output_preview}\n    ```")
                        # Можно добавить полное логирование результата:
                        # logger.debug(f"Полный результат от '{model_key}':\n{result}")
                    else:
                        print("    (ошибка или нет результата)")
        else:
            print("   Не удалось получить результаты (нет активных моделей в конфигурации или критическая ошибка).")
        print("-" * (len(f"--- Результаты для страницы {product_page} ---") + 1))


    logger.info("Обработка всех страниц завершена.")


if __name__ == "__main__":
    # Запуск основного асинхронного цикла событий
    try:
        # Установим более подробный уровень логирования для asyncio, если нужно
        # logging.getLogger('asyncio').setLevel(logging.DEBUG)
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Выполнение прервано пользователем.")
    except Exception as main_err:
        logger.error(f"Критическая ошибка в основном цикле выполнения: {main_err}", exc_info=True)