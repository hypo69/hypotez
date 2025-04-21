# -*- coding: utf-8 -*-
"""
   Мне удается запустить только с ключами, которые обязательно должны быть прописаны в .env файле.
"""
import os
import asyncio
from typing import List, Dict, Any, Optional

# LangChain компоненты
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# Ваш класс Agent (убедитесь, что он импортирован правильно)
from browser_use import Agent # Или другой путь, если необходимо

from dotenv import load_dotenv
load_dotenv()

# Ваши внутренние модули
import header # type: ignore
from header import __root__ # type: ignore
from src import gs # type: ignore
from src.logger import logger
from dataclasses import dataclass, field

@dataclass
class Config:
    """
    Класс для хранения конфигурации API ключей и других параметров.
    Включает методы для загрузки конфигурации из файла .env.
    """
    os.environ["GEMINI_API_KEY"] = getattr(gs.credentials.gemini, 'kazarinov', None)
    # self.gemini_api_key = os.getenv("GEMINI_API_KEY")
    # self.openai_api_key = os.getenv("OPENAI_API_KEY")


class Driver:
    """
    Класс для запуска задач с использованием LLM через LangChain и Agent.

    Предоставляет статический метод для инициализации моделей и выполнения
    задачи с помощью Agent.
    """

    @staticmethod
    async def run_task(
        model_configs: List[Dict[str, str]],
        task: str
    ) -> Optional[str]:
        """
        Выполняет задачу, используя указанные LLM-модели.

        Инициализирует одну или несколько моделей (Gemini, OpenAI) на основе
        предоставленного списка конфигураций и запускает агент для выполнения задачи.

        Args:
            model_configs (List[Dict[str, str]]): Список словарей, где каждый словарь
                содержит одну пару 'провайдер': 'имя_модели'.
                Пример: [{'gemini': 'gemini-1.5-flash'}, {'openai': 'gpt-4o'}]
            task (str): Текст задачи, которую должен выполнить агент.

        Returns:
            Optional[str]: Строка с результатом работы агента или None в случае ошибки.
        """
        initialized_llms: List[Any] = [] # Список для хранения инициализированных объектов LLM

        # 1. Валидация входного списка конфигураций
        if not isinstance(model_configs, list) or not model_configs:
            logger.error(f"Некорректный ввод 'model_configs': ожидался непустой список, получено {type(model_configs)}")
            return None

        logger.info(f"Начало инициализации моделей из конфигурации: {model_configs}")

        # 2. Инициализация моделей на основе конфигураций
        for config_dict in model_configs:
            if not isinstance(config_dict, dict) or len(config_dict) != 1:
                logger.warning(f"Пропуск невалидного элемента конфигурации: {config_dict}. Ожидался словарь вида {{'провайдер': 'модель'}}.")
                continue

            try:
                # Извлечение провайдера и имени модели
                provider, model_name = next(iter(config_dict.items()))
                provider: str = provider.lower()

                # Инициализация соответствующей модели
                if provider == 'gemini':
                    logger.info(f"Инициализация модели Gemini: {model_name}")
                    # Проверка наличия ключа API
                    # Обучение на модели Казаринова!
                  # Предполагается, что 'provider_lower' == 'gemini' и 'model_name' определены выше
                    # Также предполагается, что 'gs', 'logger', 'ChatGoogleGenerativeAi', 'initialized_llms' доступны

                    try:
                        logger.info(f"Инициализация модели Gemini: {model_name}")

                        # 1. Безопасно получаем ключ API с помощью getattr
                        # Обучение на модели Казаринова! (Комментарий сохранен)
                        api_key_gemini = os.getenv("GEMINI_API_KEY") # Получаем ключ API из переменной окружения

                        # 2. Проверяем, найден ли ключ
                        if not api_key_gemini:
                            logger.error("Ключ API Google (`gs.credentials.gemini.kazarinov`) не найден. Пропуск модели Gemini.")
                            ...
                            continue # Переходим к следующей итерации цикла

                        # 3. Инициализируем модель, передавая ключ напрямую через правильный параметр
                        llm = ChatGoogleGenerativeAI(
                            model=model_name,
                            api_key=api_key_gemini, # Используем правильное имя параметра
                            # Дополнительные параметры Gemini, если нужны:
                            # temperature=0.7,
                            convert_system_message_to_human=True # Этот параметр может быть полезен
                        )

                        logger.debug(f"Модель Gemini '{model_name}' успешно инициализирована.")

                    # Перехватываем возможные ошибки при инициализации модели LangChain
                    except Exception as init_err:
                        logger.error(f"Не удалось инициализировать модель Gemini '{model_name}': {init_err}", exc_info=True)
                        continue # Пропускаем эту модель при ошибке инициализации

                    # --- Остальная часть вашего цикла продолжается ниже ---
                    
                    logger.debug(f"Модель Gemini '{model_name}' успешно инициализирована.")
                    break

                elif provider == 'openai':
                    logger.info(f"Инициализация модели OpenAI: {model_name}")
                    # Проверка наличия ключа API
                    api_key_openai = getattr(getattr(gs.credentials.openai, 'hypotez', {}), 'api_key', None)
                    if not api_key_openai:
                         logger.error("Ключ API OpenAI (gs.credentials.openai.hypotez.api_key) не найден.")
                         continue # Пропуск этой модели

                    llm = ChatOpenAI(
                        model=model_name,
                        api_key=api_key_openai,
                        # Дополнительные параметры OpenAI, если нужны:
                        # temperature=0.7,
                    )

                    logger.debug(f"Модель OpenAI '{model_name}' успешно инициализирована.")

                else:
                    logger.warning(f"Неподдерживаемый провайдер LLM в конфигурации: '{provider}'. Пропуск.")

            except StopIteration: # Если словарь пуст
                 logger.warning(f"Пропуск пустого словаря в конфигурации: {config_dict}")
                 ...
                 continue
            except AttributeError as attr_err: # Ошибка доступа к вложенным атрибутам gs.credentials
                 logger.error(f"Ошибка доступа к конфигурации ключей API для '{provider}': {attr_err}. Проверьте структуру 'gs.credentials'.", exc_info=True)
                 ...
                 continue # Пропуск этой модели
            except Exception as init_err: # Другие ошибки инициализации (например, от LangChain)
                logger.error(f"Не удалось инициализировать модель {provider}:{model_name}", init_err, exc_info=True)
                ...
                continue # Пропуск этой модели

        # # Проверка, были ли успешно инициализированы какие-либо модели
        # if not initialized_llms:
        #     logger.error("Не удалось инициализировать ни одну LLM модель из предоставленной конфигурации.")
        #     ...
        #     return None

        logger.info(f"Успешно инициализировано {len(initialized_llms)} модель(ей).")

        # 3. Инициализация и запуск агента
        try:
            # Инициализация агента с списком моделей и задачей
            # Убедитесь, что ваш класс Agent может принимать список LLM объектов в параметре 'llm'
            agent = Agent(
                task=task,
                llm=llm, # Передача инициализированнoй модели
                # Другие параметры для Agent, если они есть
            )
            logger.info(f"Агент начинает выполнение задачи: \"{task}\"")
            result: Any = await agent.run() # Ожидание результата работы агента
            logger.info("Агент завершил выполнение задачи.")

            # 4. Обработка и возврат результата
            if isinstance(result, str):
                return result
            elif result is not None:
                 logger.warning(f"Агент вернул результат нестрокового типа ({type(result)}). Преобразование в строку.")
                 try:
                     return str(result) # Попытка преобразования в строку
                 except Exception as str_conv_err:
                      logger.error(f"Не удалось преобразовать результат агента в строку: {str_conv_err}", exc_info=True)
                      return None
            else:
                 logger.warning("Агент вернул None.")
                 return None # Возврат None, если агент вернул None

        except Exception as agent_err:
            logger.error("Произошла ошибка во время инициализации или выполнения задачи агентом.", agent_err, exc_info=True)
            return None # Возврат None при ошибке агента


async def main():
    """ Основная асинхронная функция для запуска задачи """

    # # Определение моделей для использования
    # models_to_use: List[Dict[str, str]] = [
    #     {'gemini': 'gemini-1.5-flash-latest'}, # Пример использования последней flash модели
    #     {'openai': 'gpt-4o'},
    #     # {'openai': 'gpt-3.5-turbo'} # Можно добавить еще моделей
    # ]

    # Определение моделей для использования
    models_to_use: List[Dict[str, str]] = [
        {'gemini': 'gemini-2.0-flash-exp'}, # Пример использования последней flash модели
    ]




    # Определение задачи
    my_task: str = "Найди в интернете и дай мне список 50 интернет магазинов, торгующех автоматикой. Предпочтение отдавей сайтам производителей."

    logger.info("Запуск задачи через Driver.run_task...")
    # Вызов статического метода класса Driver
    final_result: Optional[str] = await Driver.run_task(
        model_configs=models_to_use,
        task=my_task
    )

    if final_result is not None: # Явная проверка на None
        print("\n--- Результат работы агента ---")
        print(final_result)
        print("------------------------------")
    else:
        print("\n--- Не удалось получить результат выполнения задачи ---")


if __name__ == "__main__":
    # Запуск основного асинхронного цикла
    asyncio.run(main())