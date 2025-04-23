### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предназначен для автоматического улучшения кода в файле, указанном пользователем. Он использует библиотеку `g4f` для взаимодействия с моделью GPT-4, которая анализирует предоставленный код и вносит улучшения, такие как добавление type hints, без удаления лицензионных комментариев или существующего кода.

Шаги выполнения
-------------------------
1. **Импорт библиотек**:
   - Импортируются необходимые библиотеки: `sys`, `re`, `Path` из `pathlib`, `path` из `os` и `g4f`.
   - `sys.path.append` добавляет путь к родительскому каталогу для импорта модуля `g4f`.

2. **Функция `read_code(text)`**:
   - Функция извлекает код из текстового блока, заключенного в markdown-разметку ```python ... ```.
   - Использует регулярное выражение для поиска и извлечения кода.

3. **Запрос пути к файлу**:
   - Запрашивает у пользователя путь к файлу, который нужно улучшить.

4. **Чтение кода из файла**:
   - Открывает указанный файл в режиме чтения и считывает его содержимое в переменную `code`.

5. **Формирование запроса к GPT-4**:
   - Создает текстовый запрос (`prompt`) для модели GPT-4, включающий:
     - Инструкцию улучшить код из файла.
     - Обернутый в ```py код из переменной `code`.
     - Дополнительные инструкции: не удалять ничего, добавить type hints (если возможно), не добавлять type hints к kwargs и не удалять лицензионные комментарии.

6. **Взаимодействие с GPT-4**:
   - Использует `g4f.ChatCompletion.create` для отправки запроса к модели GPT-4.
   - Параметры:
     - `model`: `g4f.models.default` (используется модель по умолчанию).
     - `messages`: список сообщений, содержащий запрос (`prompt`).
     - `timeout`: время ожидания ответа от модели (300 секунд).
     - `stream`: `True` для получения ответа по частям.
   - Ответ от модели собирается в список `response`, и каждая часть ответа выводится в консоль.

7. **Обработка ответа от GPT-4**:
   - Объединяет все части ответа в одну строку `response`.
   - Извлекает улучшенный код из ответа с помощью функции `read_code(response)`.

8. **Запись улучшенного кода в файл**:
   - Открывает исходный файл в режиме записи и записывает в него улучшенный код.

Пример использования
-------------------------

```python
import sys
from pathlib import Path
import re
import g4f  #type: ignore

def read_code(text: str) -> str | None:
    """
    Извлекает код из текстового блока markdown.

    Args:
        text (str): Текст для поиска кода.

    Returns:
        str | None: Извлеченный код или None, если код не найден.
    """
    if match := re.search(r"```(python|py|)\\n(?P<code>[\\S\\s]+?)\\n```", text):
        return match.group("code")
    return None

def improve_code(file_path: str) -> None:
    """
    Автоматически улучшает код в указанном файле с использованием GPT-4.

    Args:
        file_path (str): Путь к файлу, который нужно улучшить.
    """
    try:
        with open(file_path, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return

    prompt = f"""
    Improve the code in this file:
    ```py
    {code}
    ```
    Don't remove anything.
    Add typehints if possible.
    Don't add any typehints to kwargs.
    Don't remove license comments.
    """

    print("Create code...")
    response = []
    try:
        for chunk in g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
            timeout=300,
            stream=True
        ):
            response.append(chunk)
            print(chunk, end="", flush=True)
        print()
    except Exception as e:
        print(f"Ошибка при взаимодействии с GPT-4: {e}")
        return

    response_text = "".join(response)

    if improved_code := read_code(response_text):
        try:
            with open(file_path, "w") as file:
                file.write(improved_code)
            print(f"Код в файле {file_path} успешно улучшен.")
        except Exception as e:
            print(f"Ошибка при записи в файл: {e}")
    else:
        print("Улучшенный код не был извлечен из ответа GPT-4.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Path: ")

    improve_code(file_path)
```