# Документация: https://habr.com/ru/articles/875798/

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # Импортируем класс для работы с Google Gemini
from browser_use import Agent
import asyncio

import header
from header import __root__
from src import gs
from src.logger import logger


class Driver:
    """Класс использует `browser_use` 
    и `langchain_openai` для поиска и получения данных с веб-страниц."""

    async def run_task(model_name: str = "gpt-4o", task:str = '' , models_list:list = ['gemini','openai']) -> str:
        """
        Исполяет сценарий 

        Args:
            model_name: Название языковой модели для использования (по умолчанию gpt-4o).
            use_google: Если True, используется Google Gemini. Если False, используется OpenAI.

        Returns:
            Строку с результатом работы агента, содержащую название статьи и сгенерированный комментарий.
            Возвращает None, если произошла ошибка.
        """
        try:
            # Выбор модели в зависимости от параметра use_google
            if 'gemini' in models_list:
                # Инициализация модели Google Gemini
                gemini = ChatGoogleGenerativeAI(
                    model="gemini-pro", 
                    google_api_key=gs.credentials.google.api_key
                )
            else:
                # Инициализация модели OpenAI
                openai = ChatOpenAI(
                    model=model_name, 
                    api_key=gs.credentials.openai.hypotez.api_key
                )

            task = f"""Открой https://chatgpt.com/, введи в окно ввода на странице chatgpt следующий текст:`Hello, world` 
            и нажми кнопку отправки сообщения. когда модель вернет ответ и верни мне ответ модели"""

            agent = Agent(
                task=task,
                llm=['openai'],
            )
            logger.info(f"Агент начал работу")
            result = await agent.run()
            logger.info(f"Агент завершил работу.")
            return result
        except Exception as e:
            logger.error(f"Произошла ошибка: {e}")
            return ''


async def main():
    """ Основная функция для выполнения задачи """
    
    # Параметр use_google позволяет выбирать между OpenAI и Google Gemini
    result = await Driver.run_task(model_name="gpt-4o")  # Пример работы с Google Gemini

    if result:
        print("Результат работы агента:")
        print(result)
    else:
        print("Не удалось получить результат.")


if __name__ == "__main__":
    asyncio.run(main())
