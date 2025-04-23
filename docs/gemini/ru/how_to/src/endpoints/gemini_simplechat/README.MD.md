### **Инструкции для генерации документации к коду**

=========================================================================================

1. **Анализируй код**: Пойми логику и действия, выполняемые данным фрагментом кода.

2. **Создай пошаговую инструкцию**:
    - **Описание**: Объясни, что делает данный блок кода.
    - **Шаги выполнения**: Опиши последовательность действий в коде.
    - **Пример использования**: Приведи пример кода, как использовать данный фрагмент в проекте.

3. **Промер**:
3.
Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет класс `GoogleGenerativeAi` для взаимодействия с моделями Google Gemini API. Он включает функции для отправки текстовых запросов, ведения диалогов, описания изображений и загрузки файлов. Код также содержит примеры использования этих функций, включая загрузку и чтение изображений и файлов, а также интерактивный чат.

Шаги выполнения
-------------------------
1. **Клонирование репозитория**: Клонируйте репозиторий `gemini-simplechat-ru` с GitHub.
2. **Установка зависимостей**: Установите необходимые библиотеки, указанные в файле `requirements.txt`, с помощью `pip install -r requirements.txt`.
3. **Настройка конфигурационного файла**: В файле `/config.json` укажите необходимые настройки, такие как API-ключ Gemini, имя модели и пути к различным директориям. Обязательно замените `XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` на ваш действительный API-ключ Google Gemini.
4. **Использование скрипта `install.ps1` (только для Windows)**: Запустите скрипт `install.ps1` от имени администратора, чтобы скопировать файлы проекта в папку `AI Assistant` в директории `%LOCALAPPDATA%`, настроить автозапуск приложения и добавить возможность вызова приложения из командной строки с помощью команды `ai`.
5. **Запуск веб-сервера**: Запустите веб-сервер с помощью команды `python main.py`. После запуска веб-интерфейс будет доступен по адресу `http://127.0.0.1:8000`.

Пример использования
-------------------------

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

4. **Избегай расплывчатых терминов** вроде "получаем" или "делаем". Будь конкретным, что именно делает код, например: "проверяет", "валидирует" или "отправляет".