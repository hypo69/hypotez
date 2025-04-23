### Как использовать класс `AIBrowserAgent`
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует, как использовать класс `AIBrowserAgent` для создания агента, который может искать информацию в Google и анализировать веб-страницы. Он включает инициализацию агента, поиск аналогов продукта и получение ответа на вопрос с использованием поисковой системы.

Шаги выполнения
-------------------------
1. **Инициализация агента**: Создается экземпляр класса `AIBrowserAgent` с указанием API-ключа, названия модели и поисковой системы.
2. **Поиск аналогов продукта**: Вызывается метод `find_product_alternatives` для поиска аналогов продукта по URL или SKU.
3. **Получение ответа на вопрос**: Вызывается метод `ask_async` для получения ответа на вопрос с использованием поисковой системы.
4. **Вывод результатов**: Результаты поиска аналогов и ответа на вопрос выводятся в консоль.

Пример использования
-------------------------

```python
import asyncio
from src.llm.openai.chat_open_ai.browser_agent import AIBrowserAgent
from src import gs

async def main():
    """
    Пример использования класса BrowserAgent.
    """
    # api_key: str = gs.credentials.openai.hypotez.api_key  # Replace with your actual method of obtaining the API key
    api_key: str = None  # Replace with your actual method of obtaining the API key
    model_name: str = 'gpt-4o-mini'  # gpt-4o-mini существует, если указан api_key

    #########################################################################
    # OPTIONAL:  Inject custom Chrome, Firefox, Edge driver
    # selenium_driver = Firefox()  # (Or with args you use in Firefox class)
    # playwright_driver = PlaywrightFirefoxAdapter(selenium_driver)
    # agent = BrowserAgent(api_key=api_key, model_name=model_name, custom_driver = playwright_driver)
    #########################################################################
    agent = AIBrowserAgent(api_key=api_key, model_name=model_name) #  Default browser_use driver

    # Пример поиска аналогов продукта
    sku: str = '1493001'
    product_url: str = None  # "https://www.apple.com/iphone-14/"  # Замените на URL интересующего вас продукта
    alternatives = await agent.find_product_alternatives(product_url=product_url, sku=sku)
    if alternatives:
        print("Найденные аналоги:")
        print(alternatives)
    else:
        print("Не удалось найти аналоги.")

    # Пример ответа на вопрос
    question = "Какая сейчас погода в Москве?"
    answer = await agent.ask_async(question)  # Используем асинхронный метод напрямую
    if answer:
        print("Ответ на вопрос:")
        print(answer)
    else:
        print("Не удалось получить ответ на вопрос.")


if __name__ == "__main__":
    asyncio.run(main())