### **Анализ кода модуля `README.MD`**

#### **1. Качество кода:**

-   **Соответствие стандартам**: 7/10
-   **Плюсы**:
    -   Хорошее общее описание функциональности модуля.
    -   Подробные инструкции по установке и настройке.
    -   Примеры использования основных методов класса `GoogleGenerativeAI`.
    -   Указания по обработке ошибок и логированию.
-   **Минусы**:
    -   Отсутствуют docstring для методов класса `GoogleGenerativeAI` в разделе "Методы класса `GoogleGenerativeAI`".
    -   Не все переменные аннотированы типами в примерах кода.
    -   В некоторых местах используется английский язык (например, "avaible_maodels"), необходимо перевести на русский.
    -   Не хватает описания структуры проекта и назначения основных файлов.

#### **2. Рекомендации по улучшению:**

1.  **Документация методов класса `GoogleGenerativeAI`**:

    -   Добавить docstring для каждого метода класса `GoogleGenerativeAI` в разделе "Методы класса `GoogleGenerativeAI`", описывая назначение метода, аргументы, возвращаемые значения и возможные исключения.

        Пример:

        ```markdown
        -   **`__init__(api_key: str, model_name: str = "gemini-2.0-flash-exp", generation_config: Dict = None, system_instruction: Optional[str] = None)`:**
            -   Инициализирует объект `GoogleGenerativeAI` с API-ключом, именем модели и настройками генерации.
            -   Параметр `system_instruction` позволяет задать системные инструкции для модели.
            ```python
            def __init__(api_key: str, model_name: str = "gemini-2.0-flash-exp", generation_config: Dict = None, system_instruction: Optional[str] = None):
                """
                Инициализирует объект `GoogleGenerativeAI`.

                Args:
                    api_key (str): API-ключ Google Gemini.
                    model_name (str, optional): Имя модели Gemini. По умолчанию "gemini-2.0-flash-exp".
                    generation_config (Dict, optional): Настройки генерации. По умолчанию `None`.
                    system_instruction (Optional[str], optional): Системные инструкции для модели. По умолчанию `None`.

                Returns:
                    None

                Example:
                    >>> ai = GoogleGenerativeAI(api_key="ваш_api_ключ", system_instruction="Ты - полезный ассистент.")
                """
                ...
            ```

        -   **`ask(q: str, attempts: int = 15) -> Optional[str]`:**

            ```python
            def ask(q: str, attempts: int = 15) -> Optional[str]:
                """
                Отправляет текстовый запрос к модели и возвращает ответ.

                Args:
                    q (str): Текстовый запрос.
                    attempts (int, optional): Количество попыток, если запрос не удался. По умолчанию 15.

                Returns:
                    Optional[str]: Ответ модели или `None` в случае неудачи.

                Example:
                    >>> answer = ai.ask("Как дела?")
                    >>> print(answer)
                    "У меня все хорошо."
                """
                ...
            ```

        -   **`chat(q: str) -> Optional[str]`:**

            ```python
            def chat(q: str) -> Optional[str]:
                """
                Отправляет запрос в чат, поддерживая историю диалога.

                Args:
                    q (str): Текстовый запрос.

                Returns:
                    Optional[str]: Ответ модели или `None` в случае неудачи.

                Example:
                    >>> response = ai.chat("Привет!")
                    >>> print(response)
                    "Здравствуйте! Чем могу помочь?"
                """
                ...
            ```

        -   **`describe_image(image: Path | bytes, mime_type: Optional[str] = 'image/jpeg', prompt: Optional[str] = '') -> Optional[str]`:**

            ```python
            def describe_image(image: Path | bytes, mime_type: Optional[str] = 'image/jpeg', prompt: Optional[str] = '') -> Optional[str]:
                """
                Описывает изображение, отправленное в виде пути к файлу или байтов.

                Args:
                    image (Path | bytes): Путь к файлу изображения или байты изображения.
                    mime_type (Optional[str], optional): Mime-тип изображения. По умолчанию 'image/jpeg'.
                    prompt (Optional[str], optional): Текстовый промпт для описания изображения. По умолчанию ''.

                Returns:
                    Optional[str]: Текстовое описание изображения или `None` в случае неудачи.

                Example:
                    >>> image_path = Path("test.jpg")
                    >>> description = ai.describe_image(image_path, prompt="Опиши изображение")
                    >>> print(description)
                    "На изображении изображен пейзаж с горами и озером."
                """
                ...
            ```

        -   **`upload_file(file: str | Path | IOBase, file_name: Optional[str] = None) -> bool`:**

            ```python
            def upload_file(file: str | Path | IOBase, file_name: Optional[str] = None) -> bool:
                """
                Загружает файл в Gemini API.

                Args:
                    file (str | Path | IOBase): Путь к файлу, имя файла или файловый объект.
                    file_name (Optional[str], optional): Имя файла для Gemini API. По умолчанию `None`.

                Returns:
                    bool: `True`, если файл успешно загружен, `False` в противном случае.

                Example:
                    >>> file_path = Path("test.txt")
                    >>> result = ai.upload_file(file_path, "test_file.txt")
                    >>> print(result)
                    True
                """
                ...
            ```

2.  **Аннотации типов**:

    -   Добавить аннотации типов для всех переменных в примерах кода, где это возможно.

3.  **Локализация**:

    -   Исправить опечатку "avaible_maodels" на "available_models" и перевести на русский язык "Доступные модели".
    -   Проверить весь текст на наличие английских слов и перевести их на русский.

4.  **Структура проекта**:

    -   Добавить краткое описание структуры проекта и назначения основных файлов. Например:

        ```markdown
        ## Структура проекта

        -   `/src`: Содержит исходный код проекта.
            -   `/src/ai`: Модули, связанные с AI-моделями.
                -   `/src/ai/gemini.py`: Класс `GoogleGenerativeAI` для взаимодействия с Gemini API.
            -   `/src/utils`: Вспомогательные утилиты.
                -   `/src/utils/jjson.py`: Модуль для работы с JSON.
        -   `/config.json`: Файл конфигурации с API-ключом и другими настройками.
        -   `main.py`: Основной скрипт для запуска веб-сервера и примера использования.
        ```

5.  **Улучшение примеров**:

    -   Улучшить примеры использования, добавив больше пояснений и примеров обработки ошибок.
    -   В примере `main()` добавить аннотации типов.
    -   Использовать `logger` для логирования ошибок и информации.

6.  **Обновление зависимостей**:

    -   Убедиться, что список зависимостей в `requirements.txt` актуален и содержит все необходимые библиотеки.

#### **3. Оптимизированный код:**

```markdown
# Google Gemini API Интеграция

Этот проект предоставляет класс `GoogleGenerativeAI` для взаимодействия с моделями Google Generative AI (Gemini). Он позволяет отправлять текстовые запросы, вести диалоги, описывать изображения и загружать файлы, используя API Google Gemini.

## Особенности

-   Поддержка различных моделей Gemini.
-   Сохранение истории диалогов в JSON и текстовый файлы.
-   Работа с текстом, изображениями и файлами.
-   Обработка ошибок с механизмом повторных попыток.
-   Возможность настраивать параметры генерации и системные инструкции.
-   Пример использования в `main()` с загрузкой и чтением изображений и файлов, а также с интерактивным чатом.
-   Веб-интерфейс для взаимодействия с чат-ботом.
-   Автоматический запуск приложения при старте системы и возможность вызова из командной строки (только для Windows).

## Требования

-   Python 3.7 или выше
-   Установленные библиотеки (см. `requirements.txt`).
-   Действительный API ключ Google Gemini (замените в файле  `config.json` на свой)
    [Получить ключ здесь](https://aistudio.google.com/app)

## Установка

1.  **Клонировать репозиторий:**

    ```bash
    git clone https://github.com/hypo69/gemini-simplechat-ru.git
    cd gemini-simplechat-ru
    ```

2.  **Установка зависимостей:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Создайте или настройте файл конфигурации:**

    В `/config.json`  можете поместить настройки, которые потребуются для вашей работы.
    Пример:

    ```json
    {
      "path": {
        "external_storage": "chat_data",
        "google_drive": "chat_data",
        "log": "/log",
        "tmp": "/tmp",
        "src": "/src",
        "root": ".",
        "endpoints": "."
      },
      "credentials": {
        "gemini": {
          "model_name": "gemini-1.5-flash-8b-exp-0924",
          "avaible_maodels": [
            "gemini-2.0-flash-exp",
            "gemini-1.5-flash-8b-exp-0924",
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b"
          ],
          "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" // <- ВАШ КЛЮЧ GEMINI API
        }
      },
      "fast_api": {
        "host": "127.0.0.1",
        "port": "3000",
        "index_path": "html/index.html"
      },
      "now": ""
    }
    ```

    **Примечание:** API ключ необходимо заменить на свой.

4.  **Использование скрипта `install.ps1` для установки (только для Windows)**

    Для автоматической установки проекта и настройки автозапуска приложения, вы можете использовать скрипт `install.ps1`, который скопирует все файлы проекта в папку `AI Assistant` в директории `%LOCALAPPDATA%`. Также скрипт настроит запуск `main.py` при старте системы через скрипт `run.ps1` и добавит возможность вызова приложения из командной строки с помощью команды `ai`.

    **Инструкции:**

    1.  Скопируйте скрипт `install.ps1` в корневую директорию проекта.
    2.  Откройте PowerShell от имени администратора.
    3.  Перейдите в директорию проекта: `cd <путь_к_проекту>`.
    4.  Запустите скрипт, выполнив команду: `.\\install.ps1`

        Скрипт создаст папку `AI Assistant` по пути  `%LOCALAPPDATA%\\AI Assistant`, скопирует в неё все файлы проекта, настроит автозапуск приложения при старте системы через скрипт `run.ps1`, и добавит команду `ai` для вызова приложения из командной строки.

## Запуск веб-сервера

Для запуска веб-сервера используйте команду:

```bash
python main.py
```

После запуска, веб-интерфейс будет доступен по адресу http://127.0.0.1:8000.

## Использование

### Инициализация

```python
from src.ai.gemini import GoogleGenerativeAI
import gs

system_instruction: str = "Ты - полезный ассистент. Отвечай на все вопросы кратко"
ai: GoogleGenerativeAI = GoogleGenerativeAI(api_key=gs.credentials.gemini.api_key, system_instruction=system_instruction)
```

### Методы класса `GoogleGenerativeAI`

-   **`__init__(api_key: str, model_name: str = "gemini-2.0-flash-exp", generation_config: Dict = None, system_instruction: Optional[str] = None)`:**
    -   Инициализирует объект `GoogleGenerativeAI` с API-ключом, именем модели и настройками генерации.
    -   Параметр `system_instruction` позволяет задать системные инструкции для модели.

    ```python
    def __init__(api_key: str, model_name: str = "gemini-2.0-flash-exp", generation_config: Dict = None, system_instruction: Optional[str] = None):
        """
        Инициализирует объект `GoogleGenerativeAI`.

        Args:
            api_key (str): API-ключ Google Gemini.
            model_name (str, optional): Имя модели Gemini. По умолчанию "gemini-2.0-flash-exp".
            generation_config (Dict, optional): Настройки генерации. По умолчанию `None`.
            system_instruction (Optional[str], optional): Системные инструкции для модели. По умолчанию `None`.

        Returns:
            None

        Example:
            >>> ai = GoogleGenerativeAI(api_key="ваш_api_ключ", system_instruction="Ты - полезный ассистент.")
        """
        ...
    ```

-   **`ask(q: str, attempts: int = 15) -> Optional[str]`:**
    -   Отправляет текстовый запрос `q` к модели и возвращает ответ.
    -   `attempts` - количество попыток, если запрос не удался.

    ```python
    def ask(q: str, attempts: int = 15) -> Optional[str]:
        """
        Отправляет текстовый запрос к модели и возвращает ответ.

        Args:
            q (str): Текстовый запрос.
            attempts (int, optional): Количество попыток, если запрос не удался. По умолчанию 15.

        Returns:
            Optional[str]: Ответ модели или `None` в случае неудачи.

        Example:
            >>> answer = ai.ask("Как дела?")
            >>> print(answer)
            "У меня все хорошо."
        """
        ...
    ```

-   **`chat(q: str) -> Optional[str]`:**
    -   Отправляет запрос `q` в чат, поддерживая историю диалога.
    -   Возвращает ответ модели.
    -   История чата сохраняется в JSON файл.

    ```python
    def chat(q: str) -> Optional[str]:
        """
        Отправляет запрос в чат, поддерживая историю диалога.

        Args:
            q (str): Текстовый запрос.

        Returns:
            Optional[str]: Ответ модели или `None` в случае неудачи.

        Example:
            >>> response = ai.chat("Привет!")
        >>> print(response)
        "Здравствуйте! Чем могу помочь?"
        """
        ...
    ```

-   **`describe_image(image: Path | bytes, mime_type: Optional[str] = 'image/jpeg', prompt: Optional[str] = '') -> Optional[str]`:**
    -   Описывает изображение, отправленное в виде пути к файлу или байтов.
    -   `image`: путь к файлу изображения или байты изображения.
    -   `mime_type`: mime-тип изображения.
    -   `prompt`: текстовый промпт для описания изображения.
    -   Возвращает текстовое описание изображения.

    ```python
    def describe_image(image: Path | bytes, mime_type: Optional[str] = 'image/jpeg', prompt: Optional[str] = '') -> Optional[str]:
        """
        Описывает изображение, отправленное в виде пути к файлу или байтов.

        Args:
            image (Path | bytes): Путь к файлу изображения или байты изображения.
            mime_type (Optional[str], optional): Mime-тип изображения. По умолчанию 'image/jpeg'.
            prompt (Optional[str], optional): Текстовый промпт для описания изображения. По умолчанию ''.

        Returns:
            Optional[str]: Текстовое описание изображения или `None` в случае неудачи.

        Example:
            >>> image_path = Path("test.jpg")
            >>> description = ai.describe_image(image_path, prompt="Опиши изображение")
            >>> print(description)
            "На изображении изображен пейзаж с горами и озером."
        """
        ...
    ```

-   **`upload_file(file: str | Path | IOBase, file_name: Optional[str] = None) -> bool`:**
    -   Загружает файл в Gemini API.
    -   `file`: путь к файлу, имя файла или файловый объект.
    -   `file_name`: имя файла для Gemini API.

    ```python
    def upload_file(file: str | Path | IOBase, file_name: Optional[str] = None) -> bool:
        """
        Загружает файл в Gemini API.

        Args:
            file (str | Path | IOBase): Путь к файлу, имя файла или файловый объект.
            file_name (Optional[str], optional): Имя файла для Gemini API. По умолчанию `None`.

        Returns:
            bool: `True`, если файл успешно загружен, `False` в противном случае.

        Example:
            >>> file_path = Path("test.txt")
            >>> result = ai.upload_file(file_path, "test_file.txt")
            >>> print(result)
            True
        """
        ...
    ```

### Пример использования

```python
import asyncio
from pathlib import Path
from src.ai.gemini import GoogleGenerativeAI
from src import gs
from src.utils.jjson import j_loads
from src.logger import logger

# Замените на свой ключ API
system_instruction: str = "Ты - полезный ассистент. Отвечай на все вопросы кратко"
ai: GoogleGenerativeAI = GoogleGenerativeAI(api_key=gs.credentials.gemini.api_key, system_instruction=system_instruction)

async def main():
    # Пример вызова describe_image с промптом
    image_path: Path = Path(r"test.jpg")  # Замените на путь к вашему изображению

    if not image_path.is_file():
        print(
            f"Файл {image_path} не существует. Поместите в корневую папку с программой файл с названием test.jpg"
        )
    else:
        prompt: str = """Проанализируй это изображение. Выдай ответ в формате JSON,
        где ключом будет имя объекта, а значением его описание.
         Если есть люди, опиши их действия."""

        description: str | None = await ai.describe_image(image_path, prompt=prompt)
        if description:
            print("Описание изображения (с JSON форматом):")
            print(description)
            try:
                parsed_description: dict = j_loads(description)

            except Exception as ex:
                logger.error("Не удалось распарсить JSON. Получен текст:", ex, exc_info=True)
                print("Не удалось распарсить JSON. Получен текст:")
                print(description)

        else:
            print("Не удалось получить описание изображения.")

        # Пример без JSON вывода
        prompt: str = "Проанализируй это изображение. Перечисли все объекты, которые ты можешь распознать."
        description: str | None = await ai.describe_image(image_path, prompt=prompt)
        if description:
            print("Описание изображения (без JSON формата):")
            print(description)

    file_path: Path = Path('test.txt')
    with open(file_path, "w") as f:
        f.write("Hello, Gemini!")

    file_upload: bool = await ai.upload_file(file_path, 'test_file.txt')
    print(file_upload)

    # Пример чата
    while True:
        user_message: str = input("You: ")
        if user_message.lower() == 'exit':
            break
        ai_message: str | None = await ai.chat(user_message)
        if ai_message:
            print(f"Gemini: {ai_message}")
        else:
            print("Gemini: Ошибка получения ответа")


if __name__ == "__main__":
    asyncio.run(main())
```

## Дополнительно

-   **Логирование:** Все диалоги и ошибки записываются в соответствующие файлы в директории `external_storage/gemini_data/log`.
    *   Логи сохраняются в следующие файлы: `info.log`, `debug.log`, `errors.log`, `log.json`.
    *   **Рекомендация:**  Регулярно очищайте директорию `logs`, чтобы избежать накопления больших файлов.

-   **История чата:** История диалогов хранится в JSON и текстовых файлах в директории `external_storage/gemini_data/history/`.
    *   Каждый новый диалог создаёт новые файлы.
    *   **Рекомендация:**  Регулярно очищайте директорию `history`, чтобы избежать накопления больших файлов.

-   **Обработка ошибок:** Программа обрабатывает сетевые ошибки, ошибки аутентификации и ошибки API с механизмом повторных попыток.
-   **Автозапуск:** Скрипт `run.ps1` обеспечивает запуск приложения в фоновом режиме при старте системы (только для Windows).
-   **Вызов из командной строки:** После установки, приложение можно вызывать из любой директории с помощью команды `ai`. Для корректной работы команды `ai` требуется перезагрузка терминала после установки.

## Замечания

-   Обязательно замените `gs.credentials.gemini.api_key` на ваш действительный API-ключ Google Gemini в файле `config.json`.
-   Убедитесь, что у вас установлен `google-generativeai`, `requests`, `grpcio`, `google-api-core` и `google-auth` .
-   Убедитесь, что у вас есть файл `test.jpg` в корневой папке с программой или измените путь к изображению в примере `main`.
-   Скрипт `install.ps1` требует запуска от имени администратора.

## Лицензия

Этот проект распространяется под [MIT].

## Автор

[hypo69]