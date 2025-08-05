# Модуль `gemini`

## Обзор

Этот модуль предоставляет класс `GoogleGenerativeAi` для взаимодействия с моделями Google Generative AI (Gemini) через API. Он позволяет отправлять текстовые запросы, вести диалоги, описывать изображения и загружать файлы, используя API Google Gemini.

## Подробней

Этот модуль реализует API для взаимодействия с моделями Google Gemini, позволяя выполнять различные задачи, такие как:

- Отправка текстовых запросов и получение ответов
- Ведение диалогов с сохранением истории
- Описание изображений, включая распознавание объектов и описание действий на изображениях
- Загрузка файлов

## Классы

### `class GoogleGenerativeAi`

**Описание**: Класс `GoogleGenerativeAi` предоставляет методы для взаимодействия с API Google Gemini.

**Атрибуты**:

- `api_key` (str): API ключ Google Gemini, необходимый для аутентификации.
- `model_name` (str): Имя модели Google Gemini, которую нужно использовать.
- `generation_config` (Dict): Словарь с конфигурационными параметрами генерации текста.
- `system_instruction` (Optional[str]): Системные инструкции для модели.

**Методы**:

- `__init__(api_key: str, model_name: str = "gemini-2.0-flash-exp", generation_config: Dict = None, system_instruction: Optional[str] = None)`:
    - Инициализирует объект `GoogleGenerativeAi` с API-ключом, именем модели и настройками генерации.
    - Параметр `system_instruction` позволяет задать системные инструкции для модели.
- `ask(q: str, attempts: int = 15) -> Optional[str]`:
    - Отправляет текстовый запрос `q` к модели и возвращает ответ.
    - `attempts` - количество попыток, если запрос не удался.
- `chat(q: str) -> Optional[str]`:
    - Отправляет запрос `q` в чат, поддерживая историю диалога.
    - Возвращает ответ модели.
    - История чата сохраняется в JSON файл.
- `describe_image(image: Path | bytes, mime_type: Optional[str] = 'image/jpeg', prompt: Optional[str] = '') -> Optional[str]`:
    - Описывает изображение, отправленное в виде пути к файлу или байтов.
    - `image`: путь к файлу изображения или байты изображения.
    - `mime_type`: mime-тип изображения.
    - `prompt`: текстовый промпт для описания изображения.
    - Возвращает текстовое описание изображения.
- `upload_file(file: str | Path | IOBase, file_name: Optional[str] = None) -> bool`:
    - Загружает файл в Gemini API.
    - `file`: путь к файлу, имя файла или файловый объект.
    - `file_name`: имя файла для Gemini API.

**Пример**:

```python
from src.ai.gemini import GoogleGenerativeAi
from src import gs

# Замените на свой ключ API
system_instruction = "Ты - полезный ассистент. Отвечай на все вопросы кратко"
ai = GoogleGenerativeAi(api_key=gs.credentials.gemini.api_key, system_instruction=system_instruction)

# Пример запроса к модели
response = ai.ask("Какая погода сегодня?")
print(response)
```

## Функции

### `j_loads`

**Назначение**: Функция `j_loads` извлекает данные из JSON-файла и преобразует их в словарь.

**Параметры**:

- `path` (str): Путь к JSON-файлу.
- `ns` (bool): Если `True`, использует `Namespace` для создания объекта, иначе - словарь.

**Возвращает**:

- `dict | Namespace`: Словарь или объект `Namespace` с данными из JSON-файла.

**Вызывает исключения**:

- `FileNotFoundError`: Если файл не найден.
- `json.JSONDecodeError`: Если файл не содержит валидный JSON.

**Пример**:

```python
from src.utils.jjson import j_loads

data = j_loads("config.json")
print(data)
```

## Примеры использования

```python
import asyncio
from pathlib import Path
from src.ai.gemini import GoogleGenerativeAi
from src import gs
from src.utils.jjson import j_loads

# Замените на свой ключ API
system_instruction = "Ты - полезный ассистент. Отвечай на все вопросы кратко"
ai = GoogleGenerativeAi(api_key=gs.credentials.gemini.api_key, system_instruction=system_instruction)

async def main():
    # Пример вызова describe_image с промптом
    image_path = Path(r"test.jpg")  # Замените на путь к вашему изображению

    if not image_path.is_file():
        print(
            f"Файл {image_path} не существует. Поместите в корневую папку с программой файл с названием test.jpg"
        )
    else:
        prompt = """Проанализируй это изображение. Выдай ответ в формате JSON,
        где ключом будет имя объекта, а значением его описание.
         Если есть люди, опиши их действия."""

        description = await ai.describe_image(image_path, prompt=prompt)
        if description:
            print("Описание изображения (с JSON форматом):")
            print(description)
            try:
                parsed_description = j_loads(description)

            except Exception as ex:
                print("Не удалось распарсить JSON. Получен текст:")
                print(description)

        else:
            print("Не удалось получить описание изображения.")

        # Пример без JSON вывода
        prompt = "Проанализируй это изображение. Перечисли все объекты, которые ты можешь распознать."
        description = await ai.describe_image(image_path, prompt=prompt)
        if description:
            print("Описание изображения (без JSON формата):")
            print(description)

    file_path = Path('test.txt')
    with open(file_path, "w") as f:
        f.write("Hello, Gemini!")

    file_upload = await ai.upload_file(file_path, 'test_file.txt')
    print(file_upload)

    # Пример чата
    while True:
        user_message = input("You: ")
        if user_message.lower() == 'exit':
            break
        ai_message = await ai.chat(user_message)
        if ai_message:
            print(f"Gemini: {ai_message}")
        else:
            print("Gemini: Ошибка получения ответа")


if __name__ == "__main__":
    asyncio.run(main())
```

## Дополнительно

- **Логирование:** Все диалоги и ошибки записываются в соответствующие файлы в директории `external_storage/gemini_data/log`.
    - Логи сохраняются в следующие файлы: `info.log`, `debug.log`, `errors.log`, `log.json`.
    - **Рекомендация:**  Регулярно очищайте директорию `logs`, чтобы избежать накопления больших файлов.

- **История чата:** История диалогов хранится в JSON и текстовых файлах в директории `external_storage/gemini_data/history/`.
    - Каждый новый диалог создаёт новые файлы.
    - **Рекомендация:**  Регулярно очищайте директорию `history`, чтобы избежать накопления больших файлов.

- **Обработка ошибок:** Программа обрабатывает сетевые ошибки, ошибки аутентификации и ошибки API с механизмом повторных попыток.

- **Автозапуск:** Скрипт `run.ps1` обеспечивает запуск приложения в фоновом режиме при старте системы (только для Windows).

- **Вызов из командной строки:** После установки, приложение можно вызывать из любой директории с помощью команды `ai`. Для корректной работы команды `ai` требуется перезагрузка терминала после установки.

## Замечания

- Обязательно замените `gs.credentials.gemini.api_key` на ваш действительный API-ключ Google Gemini в файле `config.json`.
- Убедитесь, что у вас установлен `google-generativeai`, `requests`, `grpcio`, `google-api-core` и `google-auth` .
- Убедитесь, что у вас есть файл `test.jpg` в корневой папке с программой или измените путь к изображению в примере `main`.
- Скрипт `install.ps1` требует запуска от имени администратора.

## Лицензия

Этот проект распространяется под [MIT].

## Автор

[hypo69]