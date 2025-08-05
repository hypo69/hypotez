## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предоставляет набор функций и классов, которые используются для работы с клавиатурами, компрессией подсказок (prompts) и вставкой HTML-тегов в текст. 

Шаги выполнения
-------------------------
1. **Классы клавиатур `keyboards`**:
    - Класс `keyboards` предоставляет два метода:
        - `_keyboard_two_blank(self, data: list[str], name: list[str]) -> types.InlineKeyboardMarkup`: 
            Создает инлайн-клавиатуру с двумя полями для каждой кнопки. 
            Принимает два списка: `data` - данные для кнопок, `name` - текст кнопок. 
            Возвращает объект `types.InlineKeyboardMarkup`.
        - `_reply_keyboard(self, name: list[str])`: 
            Создает обычную клавиатуру с кнопками, заданными в списке `name`. 
            Возвращает объект `types.ReplyKeyboardMarkup`.
2. **Класс компрессии подсказок `PromptsCompressor`**:
    - Класс `PromptsCompressor` предоставляет два метода:
        - `__init__(self)`: 
            Инициализирует класс, задавая список `commands_size`, который хранит информацию о размерах и структуре подсказок.
        - `get_prompt(self, info: list[str], ind: int) -> str`: 
            Возвращает отформатированную подсказку. 
            Принимает список `info` с данными, которые необходимо вставить в подсказку, и индекс `ind` для выбора типа подсказки.
            Заменяет placeholder'ы в подсказке из `prompts.json` на данные из списка `info`.
        - `html_tags_insert(response: str) -> str`: 
            Статический метод, который вставляет HTML-теги в строку `response`. 
            Заменяет различные шаблоны текста на соответствующие HTML-теги.

Пример использования
-------------------------

```python
from src.endpoints.bots.telegram.ToolBoxbot-main.ToolBox.BaseSettings.AuxiliaryClasses import keyboards, PromptsCompressor

# Создание клавиатуры
kb = keyboards()
inline_keyboard = kb._keyboard_two_blank(data=['data1', 'data2'], name=['Button 1', 'Button 2'])

# Создание компрессора подсказок
prompts_compressor = PromptsCompressor()

# Получение подсказки с данными
info = ['topic', 'ta', 'style', 'length']
prompt = prompts_compressor.get_prompt(info, 2)

# Вставка HTML-тегов в текст
response = '#### Title\n*Text with bold* and ```code```'
response_with_html = PromptsCompressor.html_tags_insert(response)
```