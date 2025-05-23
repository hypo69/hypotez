## Как использовать функцию `pprint`

=========================================================================================

### Описание
-------------------------
Функция `pprint` предназначена для вывода данных в консоль с применением стилей форматирования (цвет, фон, шрифт). 

### Шаги выполнения
-------------------------
1. **Принимает входные данные**: Функция получает в качестве аргумента переменную `print_data`, которая может быть типа `None`, `dict`, `list`, `str` или `Path`.
2. **Проверяет тип входных данных**:  Функция определяет тип данных `print_data`. 
3. **Форматирует данные**: В зависимости от типа данных, функция:
    - **Словарь**:  Преобразует словарь в строку с форматированием JSON (`json.dumps(print_data, indent=4)`).
    - **Список**: Выводит каждый элемент списка в отдельной строке.
    - **Строка**:  Выводит строку как есть.
    - **Путь**:  Выводит путь к файлу.
4. **Применяет стили**: Функция применяет заданные цвета (`text_color`), фон (`bg_color`) и стиль шрифта (`font_style`) к строке с данными.
5. **Выводит результат**:  Выводит отформатированную строку в консоль.


### Пример использования
-------------------------

```python
from src.utils.printer import pprint

# Вывод словаря с зеленым цветом текста
pprint({"name": "Alice", "age": 30}, text_color="green")

# Вывод списка с синим цветом текста и жирным шрифтом
pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")

# Вывод строки с желтым цветом текста, красным фоном и подчеркиванием
pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")

# Вывод пути к файлу
pprint("/path/to/file.txt")
```