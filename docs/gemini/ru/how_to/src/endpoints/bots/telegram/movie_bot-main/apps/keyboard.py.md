### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код создает два набора кнопок для Telegram-ботов, используя библиотеку `aiogram`. Первый набор (`find_movie`) содержит одну кнопку для поиска новых фильмов. Второй набор (`choice`) предлагает пользователю выбор между фильмами и сериалами.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются классы `InlineKeyboardButton` и `InlineKeyboardMarkup` из библиотеки `aiogram.types`. `InlineKeyboardButton` используется для создания отдельных кнопок, а `InlineKeyboardMarkup` — для объединения этих кнопок в клавиатуру.

2. **Создание клавиатуры `find_movie`**:
   - Создается объект `InlineKeyboardMarkup` с именем `find_movie`.
   - В `inline_keyboard` передается список списков, где каждый внутренний список представляет собой строку кнопок. В данном случае создается одна строка с одной кнопкой.
   - Кнопка создается с текстом 'Найти' и callback-данными 'new_movies'. Callback-данные используются для обработки нажатия на кнопку.

3. **Создание клавиатуры `choice`**:
   - Создается объект `InlineKeyboardMarkup` с именем `choice`.
   - В `inline_keyboard` передается список списков, где каждый внутренний список представляет собой строку кнопок. В данном случае создается одна строка с двумя кнопками.
   - Первая кнопка создается с текстом 'Сериал' и callback-данными 'series'.
   - Вторая кнопка создается с текстом 'Фильм' и callback-данными 'film'.

Пример использования
-------------------------

```python
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = 'YOUR_BOT_TOKEN'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

find_movie = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти', callback_data='new_movies')]
])

choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сериал', callback_data='series'),
     InlineKeyboardButton(text='Фильм', callback_data='film')]
])

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Функция отправляет приветственное сообщение и предлагает выбрать действие.
    """
    await message.reply("Привет! Что вы хотите найти?", reply_markup=choice)

@dp.callback_query_handler(lambda c: c.data == 'new_movies')
async def process_callback_find_movie(callback_query: types.CallbackQuery):
    """
    Обработчик callback-данных для кнопки 'Найти'.
    """
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вы нажали кнопку "Найти".')

@dp.callback_query_handler(lambda c: c.data in ['series', 'film'])
async def process_callback_choice(callback_query: types.CallbackQuery):
    """
    Обработчик callback-данных для кнопок 'Сериал' и 'Фильм'.
    """
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data == 'series':
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали Сериал.')
    elif callback_query.data == 'film':
        await bot.send_message(callback_query.from_user.id, 'Вы выбрали Фильм.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)