### **Инструкции по использованию кода нормализации строк и чисел**

=========================================================================================

Описание
-------------------------
Данный модуль предоставляет набор функций для нормализации строк, булевых значений, целых чисел и чисел с плавающей точкой. Он также включает вспомогательные методы для обработки текста, такие как удаление HTML-тегов и специальных символов. Ниже описано, как использовать различные функции этого модуля.

Шаги выполнения
-------------------------
1. **Импортируйте необходимые функции** из модуля `src.utils.string.normalizer`.
2. **Используйте функции** для нормализации данных в зависимости от типа данных.

Пример использования
-------------------------

```python
from src.utils.string.normalizer import (
    normalize_string,
    normalize_boolean,
    normalize_int,
    normalize_float,
    normalize_sql_date,
    remove_line_breaks,
    remove_html_tags,
    remove_special_characters,
    normalize_sku,
    simplify_string,
)

# Пример использования normalize_string
input_str = " Пример строки <b>с HTML</b> "
normalized_str = normalize_string(input_str)
print(f"Original string: {input_str}")
print(f"Normalized string: {normalized_str}")  # Output: Пример строки с HTML

# Пример использования normalize_boolean
input_bool = "yes"
normalized_bool = normalize_boolean(input_bool)
print(f"Original boolean: {input_bool}")
print(f"Normalized boolean: {normalized_bool}")  # Output: True

# Пример использования normalize_int
input_int = "42"
normalized_int = normalize_int(input_int)
print(f"Original integer: {input_int}")
print(f"Normalized integer: {normalized_int}")  # Output: 42

# Пример использования normalize_float
input_float = "$1,234.56"
normalized_float = normalize_float(input_float)
print(f"Original float: {input_float}")
print(f"Normalized float: {normalized_float}")  # Output: 1234.56

# Пример использования normalize_sql_date
input_date = "12/06/2024"
normalized_date = normalize_sql_date(input_date)
print(f"Original date: {input_date}")
print(f"Normalized date: {normalized_date}")  # Output: 2024-12-06

# Пример использования remove_line_breaks
input_text_with_breaks = "Текст\nс переносами\rстрок."
normalized_text = remove_line_breaks(input_text_with_breaks)
print(f"Original text with line breaks: {input_text_with_breaks}")
print(f"Normalized text: {normalized_text}")

# Пример использования remove_html_tags
input_html_text = "<p>Текст с <b>HTML</b> тегами.</p>"
normalized_html_text = remove_html_tags(input_html_text)
print(f"Original HTML text: {input_html_text}")
print(f"Normalized HTML text: {normalized_html_text}")

# Пример использования remove_special_characters
input_text_with_special_chars = "Текст#с#спец#символами."
normalized_special_chars_text = remove_special_characters(input_text_with_special_chars, chars=['#'])
print(f"Original text with special chars: {input_text_with_special_chars}")
print(f"Normalized text: {normalized_special_chars_text}")

# Пример использования normalize_sku
input_sku = "מקט: 303235-A"
normalized_sku_text = normalize_sku(input_sku)
print(f"Original SKU text: {input_sku}")
print(f"Normalized text: {normalized_sku_text}")

# Пример использования simplify_string
example_str = "It's a test string with 'single quotes', numbers 123 and symbols!"
simplified_str = simplify_string(example_str)
print(f"Original string: {example_str}")
print(f"Simplified string: {simplified_str}")
```