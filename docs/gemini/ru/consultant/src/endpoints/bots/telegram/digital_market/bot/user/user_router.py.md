### **Анализ кода модуля `user_router.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/user/user_router.py

**Качество кода**:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код достаточно хорошо структурирован и читаем.
  - Используются асинхронные функции, что хорошо для работы с ботами.
  - Применяются `Router` и `F` из `aiogram` для обработки сообщений и callback-запросов.
  - Используется `AsyncSession` для работы с базой данных.
  - Есть обработка различных сценариев (регистрация, просмотр профиля, история покупок).
- **Минусы**:
  - Отсутствуют docstring для функций.
  - Используется `except Exception as e: pass`, что является плохой практикой.
  - Не хватает логирования.
  - Не все переменные аннотированы типами.

**Рекомендации по улучшению**:

1.  **Добавить docstring для каждой функции и метода**, чтобы объяснить их назначение, параметры и возвращаемые значения.
2.  **Заменить `except Exception as e: pass`** на более конкретную обработку исключений с логированием ошибки.
3.  **Добавить логирование** для отслеживания действий пользователя и возможных ошибок.
4.  **Аннотировать все переменные типами**.
5.  **Использовать одинарные кавычки** для строк.
6.  **Соблюдать PEP8** для форматирования кода.
7.  **Перевести все комментарии и docstring на русский язык**.

**Оптимизированный код**:

```python
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.dao import UserDAO
from bot.user.kbs import main_user_kb, purchases_kb
from bot.user.schemas import TelegramIDModel, UserModel
from src.logger.logger import logger # Импорт модуля logger

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message, session_with_commit: AsyncSession) -> None:
    """
    Обрабатывает команду /start.

    Args:
        message (Message): Объект сообщения от Telegram.
        session_with_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД.

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при обработке запроса к базе данных.
    """
    user_id: int = message.from_user.id # ID пользователя
    try:
        user_info = await UserDAO.find_one_or_none(
            session=session_with_commit,
            filters=TelegramIDModel(telegram_id=user_id)
        )

        if user_info:
            await message.answer(
                f'👋 Привет, {message.from_user.full_name}! Выберите необходимое действие',
                reply_markup=main_user_kb(user_id)
            )
            return

        values = UserModel(
            telegram_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        await UserDAO.add(session=session_with_commit, values=values)
        await message.answer(f'🎉 <b>Благодарим за регистрацию!</b>. Теперь выберите необходимое действие.',
                             reply_markup=main_user_kb(user_id))
    except Exception as ex:
        logger.error('Ошибка при обработке команды /start', ex, exc_info=True)


@user_router.callback_query(F.data == 'home')
async def page_home(call: CallbackQuery) -> None:
    """
    Обрабатывает callback-запрос для перехода на главную страницу.

    Args:
        call (CallbackQuery): Объект callback-запроса от Telegram.

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при отправке ответа.
    """
    try:
        await call.answer('Главная страница')
        await call.message.answer(
            f'👋 Привет, {call.from_user.full_name}! Выберите необходимое действие',
            reply_markup=main_user_kb(call.from_user.id)
        )
    except Exception as ex:
        logger.error('Ошибка при переходе на главную страницу', ex, exc_info=True)


@user_router.callback_query(F.data == 'about')
async def page_about(call: CallbackQuery) -> None:
    """
    Обрабатывает callback-запрос для отображения информации о магазине.

    Args:
        call (CallbackQuery): Объект callback-запроса от Telegram.

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при отправке ответа.
    """
    try:
        await call.answer('О магазине')
        await call.message.answer(
            text=(
                '🎓 Добро пожаловать в наш учебный магазин!\n\n'
                '🚀 Этот бот создан как демонстрационный проект для статьи на Хабре.\n\n'
                '👨‍💻 Автор: Яковенко Алексей\n\n'
                '🛍️ Здесь вы можете изучить принципы работы телеграм-магазина, '
                'ознакомиться с функциональностью и механизмами взаимодействия с пользователем.\n\n'
                '📚 Этот проект - это отличный способ погрузиться в мир разработки ботов '
                'и электронной коммерции в Telegram.\n\n'
                '💡 Исследуйте, учитесь и вдохновляйтесь!\n\n'
                'Данные для тестовой оплаты:\n\n'
                'Карта: 1111 1111 1111 1026\n'
                'Годен до: 12/26\n'
                'CVC-код: 000\n'
            ),
            reply_markup=call.message.reply_markup
        )
    except Exception as ex:
        logger.error('Ошибка при отображении информации о магазине', ex, exc_info=True)


@user_router.callback_query(F.data == 'my_profile')
async def page_about(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обрабатывает callback-запрос для отображения профиля пользователя.

    Args:
        call (CallbackQuery): Объект callback-запроса от Telegram.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД (без коммита).

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при получении статистики покупок или отправке ответа.
    """
    user_id: int = call.from_user.id # ID пользователя
    try:
        await call.answer('Профиль')

        # Получаем статистику покупок пользователя
        purchases: dict = await UserDAO.get_purchase_statistics(session=session_without_commit, telegram_id=user_id)
        total_amount: int = purchases.get('total_amount', 0)
        total_purchases: int = purchases.get('total_purchases', 0)

        # Формируем сообщение в зависимости от наличия покупок
        if total_purchases == 0:
            await call.message.answer(
                text='🔍 <b>У вас пока нет покупок.</b>\n\n'
                     'Откройте каталог и выберите что-нибудь интересное!',
                reply_markup=main_user_kb(user_id)
            )
        else:
            text: str = (
                f'🛍 <b>Ваш профиль:</b>\n\n'
                f'Количество покупок: <b>{total_purchases}</b>\n'
                f'Общая сумма: <b>{total_amount}₽</b>\n\n'
                'Хотите просмотреть детали ваших покупок?'
            )
            await call.message.answer(
                text=text,
                reply_markup=purchases_kb()
            )
    except Exception as ex:
        logger.error('Ошибка при отображении профиля пользователя', ex, exc_info=True)


@user_router.callback_query(F.data == 'purchases')
async def page_user_purchases(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обрабатывает callback-запрос для отображения истории покупок пользователя.

    Args:
        call (CallbackQuery): Объект callback-запроса от Telegram.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД (без коммита).

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при удалении предыдущего сообщения,
                   получении списка покупок или отправке информации о товаре.
    """
    user_id: int = call.from_user.id # ID пользователя
    try:
        await call.answer('Мои покупки')
        try:
            await call.message.delete()
        except Exception as ex: # Обработка исключения при удалении сообщения
            logger.warning('Не удалось удалить предыдущее сообщение', ex, exc_info=True)

        # Получаем список покупок пользователя
        purchases: list = await UserDAO.get_purchased_products(session=session_without_commit, telegram_id=user_id)

        if not purchases:
            await call.message.answer(
                text=f'🔍 <b>У вас пока нет покупок.</b>\n\n'
                     f'Откройте каталог и выберите что-нибудь интересное!',
                reply_markup=main_user_kb(user_id)
            )
            return

        # Для каждой покупки отправляем информацию
        for purchase in purchases:
            product = purchase.product
            file_text: str = '📦 <b>Товар включает файл:</b>' if product.file_id else '📄 <b>Товар не включает файлы:</b>'

            product_text: str = (
                '🛒 <b>Информация о вашем товаре:</b>\n'
                '━━━━━━━━━━━━━━━━━━\n'
                f'🔹 <b>Название:</b> <i>{product.name}</i>\n'
                f'🔹 <b>Описание:</b>\n<i>{product.description}</i>\n'
                f'🔹 <b>Цена:</b> <b>{product.price} ₽</b>\n'
                f'🔹 <b>Закрытое описание:</b>\n<i>{product.hidden_content}</i>\n'
                '━━━━━━━━━━━━━━━━━━\n'
                f'{file_text}\n'
            )

            if product.file_id:
                # Отправляем файл с текстом
                await call.message.answer_document(
                    document=product.file_id,
                    caption=product_text,
                )
            else:
                # Отправляем только текст
                await call.message.answer(
                    text=product_text,
                )

        await call.message.answer(
            text='🙏 Спасибо за доверие!',
            reply_markup=main_user_kb(user_id)
        )
    except Exception as ex:
        logger.error('Ошибка при отображении истории покупок пользователя', ex, exc_info=True)