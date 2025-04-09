### **Анализ кода модуля `hendlers.py`**

## \file /hypotez/src/endpoints/bots/telegram/movie_bot-main/apps/hendlers.py

Модуль содержит обработчики для Telegram-бота, который позволяет искать фильмы и сериалы. Он использует библиотеку `aiogram` для работы с Telegram API, а также модуль `apps.search` для выполнения поисковых запросов.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код достаточно хорошо структурирован и понятен.
    - Используются `FSMContext` для управления состоянием пользователя.
    - Применены `Router` для организации обработчиков.
- **Минусы**:
    - Не хватает аннотаций типов для переменных и возвращаемых значений функций.
    - Отсутствует подробная документация для функций и классов.
    - Не используется логирование ошибок.
    - Жестко заданы строковые значения, такие как сообщения пользователю.
    - Не все строки отформатированы согласно PEP8 (например, отсутствуют пробелы вокруг операторов).
    - Не используются `j_loads` или `j_loads_ns` для чтения конфигурационных файлов (если таковые имеются).
    - Отсутствуют комментарии, объясняющие назначение отдельных блоков кода.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Для всех переменных, аргументов функций и возвращаемых значений добавить аннотации типов.

2.  **Добавить документацию**:
    - Для каждой функции и класса добавить docstring с описанием назначения, аргументов и возвращаемых значений.

3.  **Внедрить логирование**:
    - Использовать модуль `logger` для логирования ошибок и других важных событий.

4.  **Использовать константы для строковых значений**:
    - Вынести строковые значения, такие как сообщения пользователю, в константы для удобства изменения и поддержки.

5.  **Улучшить форматирование кода**:
    - Привести код в соответствие со стандартами PEP8, добавив пробелы вокруг операторов и т.д.

6.  **Обработка ошибок**:
    - Добавить обработку исключений с логированием ошибок.

7.  **Использовать `j_loads` или `j_loads_ns`**:
    - Если используются JSON или конфигурационные файлы, заменить `open` и `json.load` на `j_loads` или `j_loads_ns`.

8. **Улучшить взаимодействие с вебдрайвером**
    - Если в дальнейшем планируется работа с вебдрайвером, убедиться, что используется подход с наследованием `Driver`, `Chrome`, `Firefox` или `Playwright`.

**Оптимизированный код:**

```python
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import apps.keyboard as kb
from apps.search import search_query
from typing import Dict, Optional

from src.logger import logger  # Добавлен импорт logger

router: Router = Router()

type_movies: Dict[str, str] = {'film': 'Фильм', 'series': 'Сериал'}

WELCOME_MESSAGE: str = "Добро пожаловать, "
FIND_MOVIE_MESSAGE: str = 'Найти интересующий фильм'
TYPE_MOVIE_CHOICE_MESSAGE: str = 'Укажите фильм или сериал вы ищите'
ENTER_MOVIE_NAME_MESSAGE: str = 'Введите название'
MOVIE_NOT_FOUND_MESSAGE: str = "Ваш {movie_type} не найден 😢"
SEARCH_RESULT_MESSAGE: str = "По вашему запросу найдено ✨✨✨:"


class Params(StatesGroup):
    """
    Состояния для FSM (машины состояний) пользователя.
    """
    type_movie = State()
    name = State()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start.

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Отправляем приветственное сообщение
        await message.answer(f"{WELCOME_MESSAGE}" +
                             f"<b>{message.from_user.full_name}</b> 😎",
                             parse_mode="html")
        # Предлагаем найти фильм
        await message.answer(FIND_MOVIE_MESSAGE, reply_markup=kb.find_movie)
    except Exception as ex:
        logger.error('Error in command_start_handler', ex, exc_info=True)


@router.callback_query(F.data == 'new_movies')
async def movie_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик нажатия на кнопку "new_movies".

    Args:
        callback (CallbackQuery): Объект обратного вызова от нажатия кнопки.
        state (FSMContext): Контекст состояний пользователя.
    """
    try:
        # Устанавливаем состояние ожидания выбора типа фильма
        await state.set_state(Params.type_movie)
        # Редактируем сообщение, предлагая выбрать тип фильма
        await callback.message.edit_text(TYPE_MOVIE_CHOICE_MESSAGE,
                                         reply_markup=kb.choice)
    except Exception as ex:
        logger.error('Error in movie_handler', ex, exc_info=True)


@router.callback_query(F.data == 'series')
async def series_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик нажатия на кнопку "series".

    Args:
        callback (CallbackQuery): Объект обратного вызова от нажатия кнопки.
        state (FSMContext): Контекст состояний пользователя.
    """
    try:
        # Удаляем предыдущее сообщение
        await callback.message.delete()
        # Обновляем данные состояния, указывая тип фильма "series"
        await state.update_data(type_movie='series')
        # Устанавливаем состояние ожидания ввода названия фильма
        await state.set_state(Params.name)
        # Отправляем сообщение с просьбой ввести название
        await callback.message.answer(ENTER_MOVIE_NAME_MESSAGE)
    except Exception as ex:
        logger.error('Error in series_handler', ex, exc_info=True)


@router.callback_query(F.data == 'film')
async def film_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик нажатия на кнопку "film".

    Args:
        callback (CallbackQuery): Объект обратного вызова от нажатия кнопки.
        state (FSMContext): Контекст состояний пользователя.
    """
    try:
        # Удаляем предыдущее сообщение
        await callback.message.delete()
        # Обновляем данные состояния, указывая тип фильма "film"
        await state.update_data(type_movie='film')
        # Устанавливаем состояние ожидания ввода названия фильма
        await state.set_state(Params.name)
        # Отправляем сообщение с просьбой ввести название
        await callback.message.answer(ENTER_MOVIE_NAME_MESSAGE)
    except Exception as ex:
        logger.error('Error in film_handler', ex, exc_info=True)


@router.message(Params.name)
async def name_handler(message: Message, state: FSMContext) -> None:
    """
    Обработчик ввода названия фильма.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Контекст состояний пользователя.
    """
    try:
        # Обновляем данные состояния, сохраняя название фильма
        await state.update_data(name=message.text)
        # Получаем данные из состояния
        data: Dict[str, str] = await state.get_data()
        # Выполняем поисковый запрос
        movie: Optional[Dict] = search_query(data['name'], data['type_movie'])
        # Отправляем информацию о запросе
        await message.answer(f"Название: <b>{data['name']}</b>\n" +
                             f"Тип: <b>{type_movies[data['type_movie']]}</b>",
                             parse_mode="html")
        # Если фильм найден
        if movie:
            # Отправляем сообщение о результате поиска
            await message.answer(SEARCH_RESULT_MESSAGE)
            # Отправляем информацию о фильме
            await message.answer(f"<b>{movie['title']}</b>\n" +
                                 f"{movie['description']}\n" +
                                 f"{movie['link']}", parse_mode="html")
        else:
            # Отправляем сообщение о том, что фильм не найден
            await message.answer(MOVIE_NOT_FOUND_MESSAGE.format(movie_type=type_movies[data['type_movie']]))
        # Предлагаем найти новый фильм
        await message.answer(FIND_MOVIE_MESSAGE, reply_markup=kb.find_movie)
        # Очищаем состояние
        await state.clear()
    except Exception as ex:
        logger.error('Error in name_handler', ex, exc_info=True)