## Как использовать модуль `src.utils.convertors.md2dict`
=========================================================================================

Описание
-------------------------
Модуль `src.utils.convertors.md2dict`  предназначен для преобразования строки Markdown в структурированный словарь. 
Он также может извлекать JSON-содержимое, если оно присутствует в Markdown.

Шаги выполнения
-------------------------
1. **Преобразование Markdown в HTML**:
    - Функция `md2html` использует библиотеку `markdown2` для преобразования строки Markdown в HTML.
    - Она может принимать список расширений markdown2 для настройки процесса конвертации.
2. **Парсинг HTML**:
    - Функция `md2dict` анализирует полученный HTML-код, чтобы извлечь заголовки и текст.
    - Она использует регулярные выражения для поиска заголовков и разделения текста на секции, основанные на уровне заголовков.
3. **Создание словаря**:
    - Функция создает словарь, где ключи — это заголовки, а значения — это списки строк, соответствующие тексту в каждой секции.

Пример использования
-------------------------

```python
from src.utils.convertors.md2dict import md2dict

md_string = """
# Заголовок 1

## Заголовок 2

Это текст в секции 2.

### Заголовок 3

Это текст в секции 3.
"""

sections = md2dict(md_string)
print(sections)
```

**Результат:**
```python
{'Заголовок 1': ['Заголовок 2', 'Это текст в секции 2.', 'Заголовок 3', 'Это текст в секции 3.'],
 'Заголовок 2': ['Заголовок 3', 'Это текст в секции 3.'],
 'Заголовок 3': ['Это текст в секции 3.']}
```

**Дополнительные сведения:**

- Функция `md2html` может принимать опциональный параметр `extras`, который представляет собой список расширений markdown2.
- Функция `md2dict` возвращает пустой словарь, если возникает ошибка во время парсинга.
- Модуль использует `logger` для записи ошибок.