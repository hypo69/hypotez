### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор функций для обработки текста, включая извлечение кода из markdown-блоков, фильтрацию JSON и управление асинхронными генераторами. Он предоставляет инструменты для разбора и очистки текста, что может быть полезно при работе с данными, полученными из различных источников.

Шаги выполнения
-------------------------
1. **`filter_markdown(text: str, allowd_types=None, default=None) -> str`**:
   - Функция ищет markdown-блок кода в переданной строке `text`.
   - Использует регулярное выражение для поиска блока кода, начинающегося и заканчивающегося символами ```.
   - Если `allowd_types` не указан или тип блока кода есть в списке `allowd_types`, возвращает код из этого блока.
   - Если блок кода не найден или его тип не разрешен, возвращает значение `default`.

2. **`filter_json(text: str) -> str`**:
   - Специализированная функция для извлечения JSON-блоков из текста.
   - Вызывает `filter_markdown` с параметрами, настроенными на поиск JSON-блоков (````json````).
   - Возвращает извлеченный JSON-код или исходный текст, если JSON-блок не найден.

3. **`find_stop(stop: Optional[list[str]], content: str, chunk: str = None)`**:
   - Функция ищет первое вхождение одного из стоп-слов в строке `content`.
   - Если стоп-слово найдено, обрезает `content` до этого стоп-слова.
   - Если также передан `chunk`, обрезает и его до найденного стоп-слова.
   - Возвращает индекс первого найденного стоп-слова, обрезанный `content` и обрезанный `chunk`.

4. **`filter_none(**kwargs) -> dict`**:
   - Функция принимает произвольное количество аргументов в виде ключевых слов.
   - Создает и возвращает словарь, содержащий только те пары ключ-значение, где значение не равно `None`.

5. **`safe_aclose(generator: AsyncGenerator) -> None`**:
   - Асинхронная функция для безопасного закрытия асинхронного генератора.
   - Проверяет, существует ли генератор и имеет ли он метод `aclose`.
   - Вызывает `aclose` и перехватывает возможные исключения, логируя их как предупреждения.

Пример использования
-------------------------

```python
import asyncio
from typing import AsyncGenerator, Optional, List

async def process_text(text: str) -> None:
    """
    Пример использования функций для обработки текста и асинхронного генератора.
    """
    # Пример использования filter_markdown
    markdown_code = filter_markdown(text, allowd_types=["python"], default="")
    print(f"Извлеченный python-код: {markdown_code}")

    # Пример использования filter_json
    json_code = filter_json(text)
    print(f"Извлеченный JSON-код: {json_code}")

    # Пример использования find_stop
    stop_words: Optional[List[str]] = ["END", "STOP"]
    content = "Текст до END и после"
    first_index, trimmed_content, _ = find_stop(stop_words, content)
    print(f"Индекс стоп-слова: {first_index}, обрезанный текст: {trimmed_content}")

    # Пример использования filter_none
    filtered_dict = filter_none(a=1, b=None, c="hello")
    print(f"Отфильтрованный словарь: {filtered_dict}")

    # Пример использования safe_aclose (предположим, что async_generator - это ваш асинхронный генератор)
    async def async_generator():
        yield "data1"
        yield "data2"
    
    ag: AsyncGenerator = async_generator()
    try:
        async for item in ag:
            print(f"Получено: {item}")
    finally:
        await safe_aclose(ag)

# Пример текста для обработки
example_text = """
Вот пример текста с markdown и JSON блоками:
```python
def hello():
    print("Hello, world!")
```
```json
{"key": "value"}
```
"""

# Запуск асинхронной функции
asyncio.run(process_text(example_text))
```