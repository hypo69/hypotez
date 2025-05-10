# Модуль для работы с агентом, использующим браузер

## Обзор

Модуль `src.ai.openai.chat_openai.browser_agent` предоставляет класс `AIBrowserAgent`, который позволяет быстро настроить и запустить ИИ-агента, способного искать информацию в Google и анализировать веб-страницы.  

Этот модуль использует библиотеку `langchain_openai` для взаимодействия с OpenAI, `browser_use` для управления браузером и `asyncio` для асинхронного выполнения задач. 

## Подробей

Модуль `src.ai.openai.chat_openai.browser_agent`  позволяет создавать ИИ-агентов, которые способны взаимодействовать с веб-страницами.  Он интегрирует языковые модели OpenAI с браузером, используя библиотеку `browser_use` для выполнения задач, связанных с веб-контентом.

## Классы

### `AIBrowserAgent`

**Описание**: Класс для создания агента, использующего браузер для выполнения задач.

**Атрибуты**:

 - `api_key` (str): Ключ API OpenAI (необязательный). Если не указан, будет использован ключ из переменных окружения.
 - `model_name` (str): Название языковой модели OpenAI для использования (по умолчанию "gpt-4o-mini").
 - `search_engine` (str): Поисковая система для использования (по умолчанию "google").
 - `llm` (ChatOpenAI): Экземпляр `ChatOpenAI` для работы с языковой моделью.
 - `custom_driver` (Optional[object]): Дополнительно вводимый экземпляр WebDriver, по умолчанию `None` (браузер_use по умолчанию).

**Методы**:

 - `run_task(task_prompt: str) -> Optional[str]`: Запускает агента для выполнения заданной задачи.

    **Параметры**:
     - `task_prompt` (str): Текст задачи для агента.

    **Возвращает**:
     - `Optional[str]`: Результат выполнения задачи в виде строки, или `None` в случае ошибки.

    **Как работает функция**: 
    - `run_task` -  использует `browser_use` для управления браузером и OpenAI для обработки языковой модели.
    - `run_task`  принимает текст задачи и использует `Agent` из `browser_use` для выполнения этой задачи.
    - Функция создает экземпляр `Agent` с заданным текстом задачи,  `llm`  и  `driver`.  
    - Она запускает `agent.run()` для выполнения задачи и возвращает результат выполнения в виде строки, если задача выполнена успешно.
    - Если при выполнении задачи произошла ошибка, функция возвращает `None`.

 - `find_product_alternatives(product_url: Optional[str] = None, sku: Optional[str] = None) -> Optional[str]`: Ищет в сети аналоги для товара по заданному URL или SKU.

    **Параметры**:
     - `product_url` (Optional[str]): URL товара, для которого нужно найти аналоги (опционально).
     - `sku` (Optional[str]): SKU товара, для которого нужно найти аналоги (опционально).

    **Возвращает**:
     - `Optional[str]`: Строку с описанием найденных аналогов, или `None` в случае ошибки.

    **Как работает функция**: 
    - `find_product_alternatives` -  предназначена для поиска аналогов товара. 
    - Она  собирает поисковый запрос, основываясь на  `product_url`  или  `sku`.
    - Функция формирует текст задачи для агента,  указывая поисковую систему, URL поиска и задание найти список аналогов. 
    - Затем,  `find_product_alternatives`  вызывает  `self.run_task()`  для запуска агента с заданным текстом задачи. 
    - Возвращает полученный результат в виде строки,  содержащей описание найденных аналогов.
    - Если  `product_url`  и  `sku`  не указаны,  функция выводит предупреждение и возвращает  `None`.

 - `ask(q: str) -> Optional[str]`: Синхронная обертка для асинхронного метода `ask_async`. Не рекомендуется к использованию.

    **Параметры**:
     - `q` (str): Вопрос, на который нужно ответить.

    **Возвращает**:
     - `Optional[str]`: Ответ на вопрос в виде строки, или `None` в случае ошибки.

    **Как работает функция**:
    - `ask`  использует  `self.run_task()`  для синхронного выполнения задачи.
    - Она принимает текст вопроса,  формирует текст задачи,  запускает  `self.run_task()`  и возвращает полученный результат.

 - `ask_async(q: str) -> Optional[str]`: Отвечает на заданный вопрос, используя поиск в интернете, если это необходимо.

    **Параметры**:
     - `q` (str): Вопрос, на который нужно ответить.

    **Возвращает**:
     - `Optional[str]`: Ответ на вопрос в виде строки, или `None` в случае ошибки.

    **Как работает функция**:
    - `ask_async`  работает аналогично  `ask`,  но использует  `self.run_task()`  в асинхронном режиме.
    - Она принимает текст вопроса,  формирует текст задачи,  запускает  `self.run_task()`  в асинхронном режиме и возвращает полученный результат.

## Функции

### `main()`

**Назначение**: Пример использования класса `AIBrowserAgent`.

**Как работает функция**:
- `main`  представляет пример использования класса `AIBrowserAgent`  для поиска аналогов товара и ответа на вопросы.
- В примере  `main`  создается экземпляр  `AIBrowserAgent`  с использованием API ключа OpenAI и заданной языковой модели. 
- Затем,  `main`  выполняет  `find_product_alternatives`  для поиска аналогов по заданному SKU и  `ask_async`  для получения ответа на вопрос.
- Функция выводит найденные аналоги и ответ на вопрос в консоль.
- Если при выполнении задач возникают ошибки,  `main`  выводит соответствующие сообщения об ошибках.

## Параметры класса

- `api_key` (str): Ключ API OpenAI (необязательный). Если не указан, будет использован ключ из переменных окружения.
- `model_name` (str): Название языковой модели OpenAI для использования (по умолчанию "gpt-4o-mini").
- `search_engine` (str): Поисковая система для использования (по умолчанию "google").
- `custom_driver` (Optional[object]): Дополнительно вводимый экземпляр WebDriver, по умолчанию `None` (браузер_use по умолчанию).

## Примеры

```python
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Пример использования локатора
close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```


**Пример использования**
```python
#  Пример использования AIBrowserAgent с дефолтным драйвером
agent = AIBrowserAgent(api_key='YOUR_API_KEY', model_name='gpt-4o-mini')

# Поиск аналогов по SKU
sku: str = '1493001'
alternatives = await agent.find_product_alternatives(sku=sku)
if alternatives:
    print("Найденные аналоги:")
    print(alternatives)
else:
    print("Не удалось найти аналоги.")

# Ответ на вопрос
question = "Какая сейчас погода в Москве?"
answer = await agent.ask_async(question)  # Используем асинхронный метод напрямую
if answer:
    print("Ответ на вопрос:")
    print(answer)
else:
    print("Не удалось получить ответ на вопрос.")
```

**Пример использования с кастомным WebDriver**
```python
# Создание инстанса WebDriver (пример с Firefox)
selenium_driver = Firefox()  # (Or with args you use in Firefox class)

# Адаптация Selenium-based драйвера для Playwright
playwright_driver = PlaywrightFirefoxAdapter(selenium_driver)

# Создание инстанса AIBrowserAgent с кастомным WebDriver
agent = AIBrowserAgent(api_key='YOUR_API_KEY', model_name='gpt-4o-mini', custom_driver=playwright_driver)

# Поиск аналогов по URL
product_url = "https://www.apple.com/iphone-14/"  # Замените на URL интересующего вас товара
alternatives = await agent.find_product_alternatives(product_url=product_url)
if alternatives:
    print("Найденные аналоги:")
    print(alternatives)
else:
    print("Не удалось найти аналоги.")
```