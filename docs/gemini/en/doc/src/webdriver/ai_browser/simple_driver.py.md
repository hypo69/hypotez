# Модуль SimpleDriver

## Обзор

Этот модуль предоставляет класс `SimpleDriver`, который используется для запуска задач с использованием LLM через LangChain и стандартных агентов. Он предоставляет функциональность для:

- Конфигурирования моделей (Gemini, OpenAI).
- Установки API ключей.
- Запуска задачи с использованием LLM и доступных инструментов (веб-поиск, браузер).
- Выполнения задачи до конечного результата (`run_task`).
- Стриминга выполнения задачи (`stream_task`).

## Подробности

Этот модуль взаимодействует с модулями LangChain, BrowserController и API поиска. Он предоставляет простой интерфейс для запуска задач с использованием LLM.

## Классы

### `SimpleDriver`

**Описание**:  Класс `SimpleDriver` наследует от `Config` и `Driver`,  предоставляя функциональность для запуска задач с использованием LangChain и стандартных агентов.

**Inherits**: 
- `Config` (конфигурация LLM): Предоставляет настройки для подключения к LLM (Gemini, OpenAI) и установки API ключей.
- `Driver`: Предоставляет базовые функции для работы с браузером и Selenium.

**Attributes**:

- `GEMINI_API_KEY`: API ключ для Google Gemini.
- `OPENAI_API_KEY`: API ключ для OpenAI.
- `openai_model_name`: Название модели OpenAI (например, `text-davinci-003`).
- `gemini_model_name`: Название модели Gemini (например, `gemini-pro`).
- `start_browser`: Флаг, указывающий, следует ли запускать браузер.

**Methods**:

- `simple_process_task_async(task: str = 'Hello, world!') -> Any`: Асинхронная функция, выполняющая задачу с использованием LLM.

**How It Works**:

1. Инициализирует LLM (Gemini или OpenAI) в зависимости от конфигурации.
2. Создает экземпляр агента (Agent) с выбранным LLM и задачей.
3. Выполняет задачу с использованием агента.
4. Возвращает результат выполнения задачи в виде словаря.

**Пример**:

```python
# Создание экземпляра SimpleDriver с использованием Gemini
driver = SimpleDriver(gemini_model_name='gemini-pro')

# Задание задачи
task = 'Расскажите мне о последних новостях.'

# Выполнение задачи
result = asyncio.run(driver.simple_process_task_async(task))

# Вывод результата
print(f"Результат выполнения задачи: {result}")
```

## Функции

### `main()`

**Purpose**: Основная функция для запуска агента и выполнения задачи.

**Parameters**:

- None.

**Returns**: 

- None.

**How the Function Works**: 

1. Создает экземпляр `SimpleDriver` с использованием модели Gemini.
2. Загружает задачу из файла.
3. Выполняет задачу с использованием `simple_process_task_async`.
4. Выводит результат выполнения задачи.

**Examples**:

```python
if __name__ == "__main__":
    main()
```

## Примечание:

- Этот модуль предоставляет базовый пример запуска задач с использованием LLM. 
- Он может быть расширен для работы с различными типами задач и LLM.
- Внутренние модули, такие как `logger` и `j_loads`, предоставляют дополнительные функции для работы с журналами и форматами данных.

## Parameter Details
- `task` (str):  Задача, которую нужно выполнить.
- `agent_err` (Exception):  Исключение, которое возникло во время выполнения задачи.
- `result` (Any): Результат выполнения задачи.
- `result_dict` (dict): Результат выполнения задачи в виде словаря.
- `driver` (SimpleDriver): Экземпляр класса `SimpleDriver`.
- `task` (str): Задача, которую нужно выполнить.

## Examples

```python
# Создание экземпляра SimpleDriver с использованием OpenAI
driver = SimpleDriver(openai_model_name='text-davinci-003')

# Задание задачи
task = 'Напишите короткий рассказ о кошке.'

# Выполнение задачи
result = asyncio.run(driver.simple_process_task_async(task))

# Вывод результата
print(f"Результат выполнения задачи: {result}")
```

## Inner Functions

### `simple_process_task_async`

```python
    async def simple_process_task_async(self, task:str = \'Hello, world!\') -> Any:
        try:
            # Инициализация агента с списком моделей и задачей
            # Убедитесь, что ваш класс Agent может принимать список LLM объектов в параметре \'llm\'\n
            agent = Agent(
                task=task,
                llm=self.gemini, # Передача инициализированнoй модели
                # Другие параметры для Agent, если они есть
            )
            logger.info(f"Агент начинает выполнение задачи: \\"{task}\\"")
            result: Any = await agent.run() # Ожидание результата работы агента
            result_dict:dict = result.__dict__ # Преобразование результата в словарь
            logger.info("Агент завершил выполнение задачи.")
            ...
            return result_dict 
        except Exception as agent_err:
            logger.error("Произошла ошибка во время инициализации или выполнения задачи агентом.", agent_err, exc_info=True)
            ...
            return \'\' # Возврат None при ошибке агента
```

**Purpose**: Асинхронная функция, выполняющая задачу с использованием LLM.

**Parameters**:

- `task` (str):  Задача, которую нужно выполнить.

**Returns**: 

- `Any`: Результат выполнения задачи.

**Raises Exceptions**:

- `Exception`:  Если возникает ошибка во время инициализации или выполнения задачи агентом.

**How the Function Works**: 

1. Инициализирует агента с выбранным LLM и задачей.
2. Выполняет задачу с использованием агента.
3. Возвращает результат выполнения задачи.

**Examples**:

```python
# Выполнение задачи
result = asyncio.run(driver.simple_process_task_async(task))