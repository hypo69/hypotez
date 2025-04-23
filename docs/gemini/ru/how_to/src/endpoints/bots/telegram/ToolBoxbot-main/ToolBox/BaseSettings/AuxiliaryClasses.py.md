### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот блок кода содержит классы `keyboards` и `PromptsCompressor`, предназначенные для создания клавиатур для Telegram-бота и обработки текстовых подсказок (prompt). Класс `keyboards` включает методы для создания инлайн-клавиатур и клавиатур ответов. Класс `PromptsCompressor` предназначен для сжатия и форматирования подсказок, а также для вставки HTML-тегов в текст ответа.

Шаги выполнения
-------------------------
1. **Инициализация класса `keyboards`**:
   - Создание экземпляра класса `keyboards` для работы с клавиатурами.
2. **Создание инлайн-клавиатуры с двумя полями**:
   - Вызов метода `_keyboard_two_blank` с передачей списка данных (`data`) и списка имен (`name`) для создания кнопок.
   - Метод создает инлайн-клавиатуру, добавляя кнопки в ряды по две, если количество кнопок четное, или с добавлением последней кнопки отдельно, если нечетное.
3. **Создание клавиатуры ответов**:
   - Вызов метода `_reply_keyboard` с передачей списка имен (`name`) для создания кнопок.
   - Метод создает клавиатуру ответов, добавляя кнопки на клавиатуру.
4. **Инициализация класса `PromptsCompressor`**:
   - Создание экземпляра класса `PromptsCompressor` для работы с текстовыми подсказками.
   - При инициализации определяется структура `commands_size`, содержащая списки параметров для различных типов подсказок.
5. **Получение подсказки (prompt)**:
   - Вызов метода `get_prompt` с передачей списка информации (`info`) и индекса (`ind`) для получения сжатой подсказки.
   - Метод открывает JSON-файл с подсказками, выбирает нужную подсказку по индексу и заменяет параметры в подсказке на предоставленную информацию.
6. **Вставка HTML-тегов в ответ**:
   - Вызов статического метода `html_tags_insert` с передачей текста ответа (`response`) для вставки HTML-тегов.
   - Метод использует регулярные выражения для поиска и замены определенных шаблонов в тексте ответа на соответствующие HTML-теги.

Пример использования
-------------------------

```python
from telebot import TeleBot
from telebot import types

# Подключите ваш токен от BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = TeleBot(BOT_TOKEN)

# Инициализация классов
keyboards_instance = keyboards()
prompts_compressor = PromptsCompressor()

# Пример использования _keyboard_two_blank
data = ["option1_callback", "option2_callback", "option3_callback"]
names = ["Option 1", "Option 2", "Option 3"]
inline_keyboard = keyboards_instance._keyboard_two_blank(data, names)

# Пример использования _reply_keyboard
reply_keyboard_names = ["Button 1", "Button 2", "Button 3"]
reply_keyboard = keyboards_instance._reply_keyboard(reply_keyboard_names)

# Пример использования get_prompt
info = ["Topic", "TA", "Tone", "Struct", "Length", "Extra"]
ind = 0
prompt = prompts_compressor.get_prompt(info, ind)

# Пример использования html_tags_insert
response_text = "#### Заголовок\n**Жирный текст**\n*Курсив*"
html_response = prompts_compressor.html_tags_insert(response_text)

# Отправка клавиатуры и текста в Telegram
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=inline_keyboard)
    bot.send_message(message.chat.id, html_response, parse_mode='HTML')

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=reply_keyboard)

if __name__ == '__main__':
    bot.polling(none_stop=True)
```