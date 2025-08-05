# Модуль для улучшения кода с помощью GPT-4 Free

## Обзор

Модуль `improve_code.py` предназначен для автоматического улучшения кода Python с помощью модели GPT-4 Free. Модуль анализирует исходный код, предоставляет его в качестве входных данных модели GPT-4 Free и, основываясь на полученном ответе, обновляет исходный файл. 

## Подробности

Модуль использует API gpt4free для взаимодействия с моделью GPT-4 Free. Основные этапы работы:

1. **Чтение кода:** Модуль считывает исходный код из указанного пользователем файла.
2. **Формирование запроса:** Создается запрос к GPT-4 Free с просьбой улучшить предоставленный код. В запросе указывается необходимость сохранения существующего кода, добавления аннотаций типов, где это возможно, избегая добавления аннотаций к аргументам ключевых слов и сохранения лицензионных комментариев.
3. **Получение ответа:** Модуль отправляет запрос к GPT-4 Free и получает ответ в виде текста, который содержит улучшенный код. 
4. **Обработка ответа:** Из полученного ответа извлекается обновленный код с помощью регулярного выражения.
5. **Запись улучшенного кода:** Обновленный код записывается в исходный файл.

## Функции

### `read_code`

**Назначение**: Извлекает код из текста, используя регулярное выражение.

**Параметры**:

- `text` (str): Текст, в котором необходимо найти код.

**Возвращает**:

- str: Извлеченный код или `None`, если код не найден.

**Как работает функция**:
- Функция использует регулярное выражение `r"```(python|py|)\\n(?P<code>[\\S\\s]+?)\\n```"` для поиска блока кода, заключенного между тройными кавычками. 
- Если код найден, функция возвращает его, иначе возвращает `None`.


**Примеры**:

```python
>>> text = "```python\nprint('Hello, world!')\n```"
>>> read_code(text)
"print('Hello, world!')"

>>> text = "Some text without code"
>>> read_code(text)
None
```

### `improve_code`

**Назначение**: Основная функция модуля, которая анализирует исходный код, отправляет его в модель GPT-4 Free и обновляет исходный файл.

**Параметры**:

- `path` (str): Путь к исходному файлу.

**Возвращает**:

- None

**Как работает функция**:
- Считывает исходный код из файла.
- Формирует запрос к модели GPT-4 Free с просьбой улучшить код.
- Получает ответ от модели.
- Извлекает улучшенный код из ответа.
- Записывает улучшенный код в исходный файл.


**Примеры**:

```python
>>> improve_code("my_file.py")
```

##  Пример файла

```python
                
import sys, re
from pathlib import Path
from os import path

sys.path.append(str(Path(__file__).parent.parent.parent))

import g4f

def read_code(text):
    """
    Извлекает код из текста, используя регулярное выражение.

    Args:
        text (str): Текст, в котором необходимо найти код.

    Returns:
        str: Извлеченный код или `None`, если код не найден.

    Example:
        >>> text = "```python\nprint('Hello, world!')\n```"
        >>> read_code(text)
        "print('Hello, world!')"

        >>> text = "Some text without code"
        >>> read_code(text)
        None
    """
    if match := re.search(r"```(python|py|)\\n(?P<code>[\\S\\s]+?)\\n```", text):
        return match.group("code")
    
path = input("Path: ")

with open(path, "r") as file:
    code = file.read()

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
for chunk in g4f.ChatCompletion.create(
    model=g4f.models.default,
    messages=[{"role": "user", "content": prompt}],
    timeout=300,
    stream=True
):
    response.append(chunk)
    print(chunk, end="", flush=True)
print()
response = "".join(response)

if code := read_code(response):
    with open(path, "w") as file:
        file.write(code)

                ```