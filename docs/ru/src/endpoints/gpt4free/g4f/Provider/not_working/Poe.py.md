# Модуль Poe

## Обзор

Модуль `Poe` предоставляет реализацию для взаимодействия с платформой Poe (poe.com) для получения ответов от различных моделей, таких как Llama-2, CodeLlama, GPT-3.5, GPT-4 и Google-PaLM.

## Подробнее

Этот модуль является частью проекта `hypotez` и позволяет использовать различные AI-модели через веб-интерфейс Poe. Он использует Selenium WebDriver для автоматизации взаимодействия с веб-сайтом Poe, отправки запросов и получения ответов. Модуль поддерживает потоковую передачу ответов, что позволяет получать ответы в режиме реального времени.

## Классы

### `Poe`

**Описание**: Класс `Poe` является поставщиком (провайдером) для взаимодействия с платформой Poe.

**Наследует**:
- `AbstractProvider`: Класс `Poe` наследует `AbstractProvider`, который предоставляет базовую структуру для всех поставщиков в проекте `hypotez`.

**Атрибуты**:
- `url` (str): URL-адрес платформы Poe.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `needs_auth` (bool): Указывает, требуется ли аутентификация для использования провайдера.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу ответов.
- `models` (keys): Список моделей, поддерживаемых провайдером.

**Методы**:
- `create_completion`: Создает запрос на завершение текста к платформе Poe.

## Функции

### `create_completion`

```python
@classmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    proxy: str = None,
    webdriver: WebDriver = None,
    user_data_dir: str = None,
    headless: bool = True,
    **kwargs
) -> CreateResult:
    """
    Создает запрос на завершение текста к платформе Poe.

    Args:
        cls: Ссылка на класс.
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для отправки.
        stream (bool): Флаг, указывающий, следует ли использовать потоковую передачу.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        webdriver (WebDriver, optional): Инстанс веб-драйвера Selenium. По умолчанию `None`.
        user_data_dir (str, optional): Путь к каталогу пользовательских данных браузера. По умолчанию `None`.
        headless (bool, optional): Флаг, указывающий, следует ли запускать браузер в безголовом режиме. По умолчанию `True`.
        **kwargs: Дополнительные аргументы.

    Returns:
        CreateResult: Результат создания завершения текста.

    Raises:
        ValueError: Если указанная модель не поддерживается.
        RuntimeError: Если не удалось найти текстовое поле для ввода запроса.

    """
```

**Назначение**: Функция `create_completion` отправляет запрос на платформу Poe с использованием Selenium WebDriver для получения ответа от указанной модели. Она автоматизирует взаимодействие с веб-сайтом Poe, ввод запроса и получение результата.

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Имя модели для использования. Если не указано, используется `gpt-3.5-turbo`.
- `messages (Messages)`: Список сообщений, формирующих запрос.
- `stream (bool)`: Определяет, будет ли ответ возвращаться потоком.
- `proxy (str, optional)`: Прокси-сервер для использования. По умолчанию `None`.
- `webdriver (WebDriver, optional)`: Экземпляр веб-драйвера Selenium для повторного использования. По умолчанию `None`.
- `user_data_dir (str, optional)`: Каталог пользовательских данных браузера для сохранения сессии. По умолчанию `None`.
- `headless (bool, optional)`: Запуск браузера в "headless" режиме (без графического интерфейса). По умолчанию `True`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `CreateResult`: Итерируемый объект, возвращающий части ответа от модели, если `stream` равен `True`.

**Вызывает исключения**:
- `ValueError`: Если указанная модель не найдена в списке поддерживаемых моделей.
- `RuntimeError`: Если не удается найти элемент `textarea` на странице Poe, что может указывать на проблему с аутентификацией.

**Как работает функция**:

1. **Инициализация**:
   - Проверяет и выбирает модель, используемую по умолчанию (`gpt-3.5-turbo`), если модель не указана.
   - Форматирует сообщения для создания единого запроса.
   - Создает или использует существующий экземпляр `WebDriverSession` для управления сессией браузера.

2. **Взаимодействие с WebDriver**:
   - Пытается открыть страницу Poe с выбранной моделью.
   - Ожидает появления элемента `textarea` для ввода текста.
   - В случае неудачи (например, если пользователь не залогинен), пытается повторно открыть браузер и повторить попытку.

3. **Отправка запроса и получение ответа**:
   - Вводит отформатированный запрос в `textarea`.
   - Нажимает кнопку отправки сообщения.

4. **Обработка потока ответов**:
   - Использует JavaScript для перехвата и возврата чанков ответа от веб-страницы.
   - Возвращает чанки до тех пор, пока не будет получен финальный чанк (`None`).

5. **Завершение**:
   - Закрывает сессию WebDriver после получения всех чанков.

**Внутренние функции**:

Внутри `create_completion` используются анонимные функции JavaScript, выполняемые через `driver.execute_script`, для перехвата сообщений WebSocket и извлечения текста ответа.

**ASCII flowchart**:

```
Начало
  ↓
Выбор модели
  ↓
Форматирование запроса
  ↓
Создание WebDriverSession
  ↓
Открытие страницы Poe
  ↓
Ожидание textarea
  ↓
Ввод запроса в textarea
  ↓
Нажатие кнопки отправки
  ↓
Цикл:
  ↓
  → Перехват ответа JS
  ↓
  → Проверка чанка
  │   Да: Возврат чанка
  │   Нет: Проверка завершения
  │       Да: Выход из цикла
  │       Нет: Ожидание
  ↑
Завершение
```

**Примеры**:

```python
# Пример использования с потоковой передачей
messages = [{"role": "user", "content": "Напиши стихотворение о весне."}]
for chunk in Poe.create_completion(model="gpt-3.5-turbo", messages=messages, stream=True):
    print(chunk, end="")
```

```python
# Пример использования с передачей существующего веб-драйвера
from selenium import webdriver
driver = webdriver.Chrome()
messages = [{"role": "user", "content": "Расскажи о себе."}]
for chunk in Poe.create_completion(model="gpt-3.5-turbo", messages=messages, stream=True, webdriver=driver):
    print(chunk, end="")
driver.quit()