## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой интеграцию с API Google Gemini, которая позволяет взаимодействовать с моделями Google Generative AI (Gemini). Он предоставляет класс `GoogleGenerativeAi` для отправки текстовых запросов, ведения диалогов, описания изображений и загрузки файлов, используя API Google Gemini.

Шаги выполнения
-------------------------
1. **Инициализация класса `GoogleGenerativeAi`**:
   - Создается экземпляр класса `GoogleGenerativeAi` с вашим API-ключом и настройками генерации.
   - Можно также указать системные инструкции для модели.
2. **Использование методов класса**:
   - **`ask(q: str, attempts: int = 15) -> Optional[str]`**: Отправка текстового запроса `q` к модели и получение ответа.
   - **`chat(q: str) -> Optional[str]`**:  Отправка запроса `q` в чат, поддерживая историю диалога. 
   - **`describe_image(image: Path | bytes, mime_type: Optional[str] = 'image/jpeg', prompt: Optional[str] = '') -> Optional[str]`**: Описание изображения с использованием модели Gemini.
   - **`upload_file(file: str | Path | IOBase, file_name: Optional[str] = None) -> bool`**: Загрузка файла в Gemini API.

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