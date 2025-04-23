### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор вспомогательных функций, предназначенных для обработки и форматирования данных, используемых в различных запросах и ответах, особенно при взаимодействии с большими языковыми моделями (LLM). Функции охватывают преобразование данных в строки, форматирование промптов, получение системных промптов, обработку сообщений пользователей, генерацию случайных строк и шестнадцатеричных значений, фильтрацию None значений, конкатенацию чанков и форматирование куки.

Шаги выполнения
-------------------------

1. **Преобразование значений в строку (to_string)**:
   - Проверяет тип входного значения.
   - Если значение является строкой, функция возвращает его без изменений.
   - Если значение является словарем, функция проверяет наличие ключей `name`, `bucket_id` или `type`. В зависимости от наличия ключей возвращает пустую строку, содержимое файла из указанной директории (bucket), или значение ключа `text`.
   - Если значение является списком, функция рекурсивно вызывает `to_string` для каждого элемента списка и объединяет результаты в одну строку.

2. **Форматирование промпта (format_prompt)**:
   - Преобразует список сообщений в единую строку, добавляя специальные токены форматирования при необходимости.
   - Если `add_special_tokens` равно `False` и в списке сообщений не более одного элемента, возвращает содержимое первого сообщения, преобразованное в строку.
   - Форматирует каждое сообщение в виде `role.capitalize(): content`, где `role` – роль сообщения (например, "User" или "Assistant"), а `content` – содержимое сообщения.
   - Объединяет все отформатированные сообщения в одну строку, разделяя их символом новой строки (`\n`).

3. **Получение системного промпта (get_system_prompt)**:
   - Извлекает содержимое всех сообщений с ролью "system" и объединяет их в одну строку, разделяя символом новой строки.

4. **Получение последнего сообщения пользователя (get_last_user_message)**:
   - Итерируется по списку сообщений в обратном порядке, пока не найдет сообщение с ролью "user".
   - Возвращает содержимое этого сообщения, предварительно удалив пробелы в начале и конце строки.

5. **Форматирование промпта для изображений (format_image_prompt)**:
   - Если передан `prompt`, возвращает его. В противном случае вызывает `get_last_user_message` для извлечения последнего сообщения пользователя.

6. **Ограничение максимальной длины промпта (format_prompt_max_length)**:
   - Форматирует промпт и обрезает его, если длина превышает `max_lenght`.
   - Если длина промпта превышает `max_lenght`, пытается укоротить его, оставляя только первые и последние три сообщения.
   - Если и это не помогает, оставляет только системные сообщения и последнее сообщение.
   - Если и это не помогает, оставляет только последнее сообщение.

7. **Генерация случайной строки (get_random_string)**:
   - Генерирует случайную строку заданной длины, состоящую из строчных букв и цифр.

8. **Генерация случайного шестнадцатеричного значения (get_random_hex)**:
   - Генерирует случайную шестнадцатеричную строку заданной длины.

9. **Фильтрация None значений (filter_none)**:
   - Создает новый словарь, исключая элементы, значения которых равны `None`.

10. **Конкатенация чанков (concat_chunks)**:
    - Объединяет чанки в одну строку, исключая пустые чанки и чанки, являющиеся экземплярами исключений.

11. **Форматирование куки (format_cookies)**:
    - Форматирует куки в строку, разделяя их символом `; `.

Пример использования
-------------------------

```python
from __future__ import annotations

import random
import string
from pathlib import Path

# from ..typing import Messages, Cookies, AsyncIterator, Iterator
# from ..tools.files import get_bucket_dir, read_bucket
# from .. import debug

Messages = list[dict[str, str]]
Cookies = dict[str, str]
AsyncIterator = object
Iterator = object


def to_string(value: str | dict | list) -> str:
    if isinstance(value, str):
        return value
    elif isinstance(value, dict):
        if "name" in value:
            return ""
        elif "bucket_id" in value:
            # bucket_dir = Path(get_bucket_dir(value.get("bucket_id")))
            # return "".join(read_bucket(bucket_dir))
            return "bucket_content"
        elif value.get("type") == "text":
            return value.get("text", "")
        return ""
    elif isinstance(value, list):
        return "".join([to_string(v) for v in value if isinstance(v, dict) and v.get("type", "text") == "text"])
    return str(value)


def format_prompt(messages: Messages, add_special_tokens: bool = False, do_continue: bool = False,
                  include_system: bool = True) -> str:
    if not add_special_tokens and len(messages) <= 1:
        return to_string(messages[0]["content"])
    messages = [
        (message["role"], to_string(message["content"]))
        for message in messages
        if include_system or message.get("role") != "system"
    ]
    formatted = "\n".join([
        f'{role.capitalize()}: {content}'
        for role, content in messages
        if content.strip()
    ])
    if do_continue:
        return formatted
    return f"{formatted}\nAssistant:"


def get_system_prompt(messages: Messages) -> str:
    return "\n".join([m["content"] for m in messages if m["role"] == "system"])


def get_last_user_message(messages: Messages) -> str:
    user_messages = []
    last_message = None if len(messages) == 0 else messages[-1]
    messages = messages.copy()
    while last_message is not None and messages:
        last_message = messages.pop()
        if last_message["role"] == "user":
            content = to_string(last_message["content"]).strip()
            if content:
                user_messages.append(content)
        else:
            return "\n".join(user_messages[::-1])
    return "\n".join(user_messages[::-1])


def format_image_prompt(messages: Messages, prompt: str = None) -> str:
    if prompt is None:
        return get_last_user_message(messages)
    return prompt


def format_prompt_max_length(messages: Messages, max_lenght: int) -> str:
    prompt = format_prompt(messages)
    start = len(prompt)
    if start > max_lenght:
        if len(messages) > 6:
            prompt = format_prompt(messages[:3] + messages[-3:])
        if len(prompt) > max_lenght:
            if len(messages) > 2:
                prompt = format_prompt([m for m in messages if m["role"] == "system"] + messages[-1:])
            if len(prompt) > max_lenght:
                prompt = messages[-1]["content"]
        # debug.log(f"Messages trimmed from: {start} to: {len(prompt)}")
    return prompt


def get_random_string(length: int = 10) -> str:
    return ''.join(
        random.choice(string.ascii_lowercase + string.digits)
        for _ in range(length)
    )


def get_random_hex(length: int = 32) -> str:
    return ''.join(
        random.choice("abcdef" + string.digits)
        for _ in range(length)
    )


def filter_none(**kwargs) -> dict:
    return {
        key: value
        for key, value in kwargs.items()
        if value is not None
    }


async def async_concat_chunks(chunks: AsyncIterator) -> str:
    # return concat_chunks([chunk async for chunk in chunks])
    return "async concat"


def concat_chunks(chunks: Iterator) -> str:
    return "".join([
        str(chunk) for chunk in chunks
        if chunk and not isinstance(chunk, Exception)
    ])


def format_cookies(cookies: Cookies) -> str:
    return "; ".join([f"{k}={v}" for k, v in cookies.items()])


# Пример использования format_prompt
messages = [
    {"role": "system", "content": "Ты полезный ассистент."},
    {"role": "user", "content": "Привет!"}
]

formatted_prompt = format_prompt(messages, add_special_tokens=True)
print(f"Formatted prompt: {formatted_prompt}")

# Пример использования get_random_string
random_string = get_random_string(15)
print(f"Random string: {random_string}")

# Пример использования filter_none
filtered_dict = filter_none(a=1, b=None, c=3)
print(f"Filtered dict: {filtered_dict}")