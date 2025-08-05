# Модуль `simple_browser`

## Обзор

Модуль `simple_browser` предоставляет функциональность для запуска задач с использованием LLM через LangChain и стандартных агентов. Он использует инструменты, взаимодействующие с `BrowserController` и/или API поиска. 

## Подробнее

Модуль содержит класс `SimpleDriver`, который позволяет:

- Конфигурировать модели (Gemini, OpenAI).
- Устанавливать API ключи.
- Запускать задачу с использованием LLM и доступных инструментов (веб-поиск, браузер).
- Выполнять задачу до конечного результата (`run_task`).
- Стриминговать выполнение задачи (`stream_task`).

## Классы

### `SimpleDriver`

**Описание**: 
Класс `SimpleDriver` реализует функциональность для запуска задач с использованием LLM и агентов, интегрированных с веб-браузером. 

**Наследует**:
- `Config`
- `Driver`

**Атрибуты**:

- `GEMINI_API_KEY` (Optional[str]): API ключ для Google Gemini.
- `OPENAI_API_KEY` (Optional[str]): API ключ для OpenAI.
- `openai_model_name` (Optional[str]): Имя модели OpenAI.
- `gemini_model_name` (Optional[str]): Имя модели Google Gemini.
- `start_browser` (bool): Флаг, указывающий, нужно ли запускать веб-браузер. По умолчанию `True`.

**Методы**:

- `simple_process_task_async(task:str = 'Hello, world!') -> Any`: Запускает задачу асинхронно с использованием агента и выбранной LLM модели. 

**Принцип работы**:

Класс `SimpleDriver` наследует  `Config` и `Driver`, что позволяет ему использовать настройки для API ключей и конфигурацию драйвера веб-браузера.

**Пример**:

```python
# Создание инстанса драйвера
driver = SimpleDriver(gemini_model_name = 'gemini-2.5-flash-preview-04-17')

# Чтение инструкции для задачи
task = Path(__root__ / 'src' / 'webdriver' / 'ai_browser' / 'instructions' / 'get_news_from_nocamel_site.md').read_text(encoding='utf-8')

# Запуск задачи асинхронно
result = asyncio.run(driver.simple_process_task_async(task))

# Вывод результата выполнения задачи
print(f"Результат выполнения задачи: {result}")
```

## Функции

### `main`

**Назначение**:
Основная функция для запуска агента и выполнения задачи.

**Пример**:

```python
def main():
    """
    Основная функция для запуска агента и выполнения задачи.
    """
    # Пример использования
    driver = SimpleDriver(gemini_model_name = 'gemini-2.5-flash-preview-04-17')
    task = Path(__root__ / 'src' / 'webdriver' / 'ai_browser' / 'instructions' / 'get_news_from_nocamel_site.md').read_text(encoding='utf-8')
    result = asyncio.run(driver.simple_process_task_async(task))
    print(f"Результат выполнения задачи: {result}")

if __name__ == "__main__":
    main()
```

## Методы класса

### `simple_process_task_async`

```python
    async def simple_process_task_async(self, task:str = 'Hello, world!') -> Any:
        try:
            # Инициализация агента с списком моделей и задачей
            # Убедитесь, что ваш класс Agent может принимать список LLM объектов в параметре 'llm'
            agent = Agent(
                task=task,
                llm=self.gemini, # Передача инициализированнoй модели
                # Другие параметры для Agent, если они есть
            )
            logger.info(f"Агент начинает выполнение задачи: \"{task}\"")
            result: Any = await agent.run() # Ожидание результата работы агента
            result_dict:dict = result.__dict__ # Преобразование результата в словарь
            logger.info("Агент завершил выполнение задачи.")
            ...
            return result_dict 
        except Exception as agent_err:
            logger.error("Произошла ошибка во время инициализации или выполнения задачи агентом.", agent_err, exc_info=True)
            ...
            return '' # Возврат None при ошибке агента
```

**Назначение**:
Запускает задачу асинхронно с использованием агента и выбранной LLM модели.

**Параметры**:

- `task` (str, optional): Текст задачи, которую нужно выполнить. По умолчанию 'Hello, world!'.

**Возвращает**:
- `Any`: Возвращает словарь с результатами выполнения задачи или пустую строку в случае ошибки.

**Вызывает исключения**:
- `Exception`: Если во время инициализации или выполнения задачи агентом возникла ошибка.

**Как работает функция**:
1. Инициализирует агента с помощью `Agent` с задачей `task` и выбранной моделью LLM (в данном случае `self.gemini`).
2. Запускает асинхронное выполнение задачи с помощью `agent.run()`.
3. Преобразовывает результат в словарь `result_dict`.
4. Логирует информацию о начале и завершении выполнения задачи.
5. Возвращает словарь с результатами.
6. В случае ошибки логирует ошибку и возвращает пустую строку. 

**Пример**:

```python
task = "Расскажите мне анекдот"
result = await driver.simple_process_task_async(task) 
print(f"Результат выполнения задачи: {result}")
```

## Параметры класса

- `GEMINI_API_KEY` (Optional[str]): API ключ для Google Gemini.
- `OPENAI_API_KEY` (Optional[str]): API ключ для OpenAI.
- `openai_model_name` (Optional[str]): Имя модели OpenAI.
- `gemini_model_name` (Optional[str]): Имя модели Google Gemini.
- `start_browser` (bool): Флаг, указывающий, нужно ли запускать веб-браузер. По умолчанию `True`.

**Примеры**:

```python
# Задание API ключей и модели
driver = SimpleDriver(GEMINI_API_KEY='your_gemini_api_key', gemini_model_name='gemini-pro')

# Задание API ключей и модели
driver = SimpleDriver(OPENAI_API_KEY='your_openai_api_key', openai_model_name='gpt-3.5-turbo')

# Вызов функции
driver = SimpleDriver(start_browser=False) # Отключение запуска браузера