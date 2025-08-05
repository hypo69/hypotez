## Как использовать модуль `src.utils.string.normalizer`
=========================================================================================

### Описание
-------------------------
Модуль `src.utils.string.normalizer` предоставляет набор функций для нормализации различных типов данных.  Он позволяет преобразовать строки, булевы значения, целые и числа с плавающей точкой в соответствующие форматы, а также предлагает вспомогательные функции для обработки текста, такие как удаление HTML-тегов и специальных символов.

### Шаги выполнения
-------------------------
1. **Импорт необходимых функций:** 
    - Импортируйте нужные функции из модуля `src.utils.string.normalizer` для нормализации данных. Например:
    ```python
    from src.utils.string.normalizer import normalize_string, normalize_boolean
    ```
2. **Использование функций:**
    - Вызовите соответствующую функцию нормализации, передавая в нее данные для преобразования.
    ```python
    normalized_str = normalize_string(" Пример строки <b>с HTML</b> ") 
    normalized_bool = normalize_boolean("yes")
    ```
3. **Обработка результата:** 
    - Полученный результат – это нормализованное значение, которое можно использовать в дальнейшей обработке.

### Пример использования
-------------------------
```python
from src.utils.string.normalizer import normalize_string, normalize_boolean, normalize_int, normalize_float, normalize_sql_date

# Нормализация строки
input_str = "  Пример строки с HTML-тегами <b>и пробелами</b>  "
normalized_str = normalize_string(input_str)
print(f'Нормализованная строка: {normalized_str}') 

# Нормализация булевого значения
input_bool = "true"
normalized_bool = normalize_boolean(input_bool)
print(f'Нормализованное булево значение: {normalized_bool}')

# Нормализация целого числа
input_int = "123"
normalized_int = normalize_int(input_int)
print(f'Нормализованное целое число: {normalized_int}')

# Нормализация числа с плавающей точкой
input_float = "123.45"
normalized_float = normalize_float(input_float)
print(f'Нормализованное число с плавающей точкой: {normalized_float}')

# Нормализация даты в SQL-формат
input_date = "2024-12-06"
normalized_date = normalize_sql_date(input_date)
print(f'Нормализованная дата в SQL-формате: {normalized_date}')
```