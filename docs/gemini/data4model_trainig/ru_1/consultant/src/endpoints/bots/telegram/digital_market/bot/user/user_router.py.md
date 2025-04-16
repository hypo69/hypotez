### **Анализ кода модуля `user_router.py`**

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование `aiogram` для обработки Telegram ботов.
  - Логическая структура разделения обработчиков команд и callback-запросов.
  - Применение `CommandStart` фильтра для обработки команды `/start`.
  - Использование `AsyncSession` для работы с базой данных асинхронно.
- **Минусы**:
  - Отсутствуют docstring для функций, что затрудняет понимание их назначения.
  - Не все переменные аннотированы типами.
  - Использование `Exception as e` вместо `Exception as ex` в блоке `try-except`.
  - Отсутствует логирование ошибок.

**Рекомендации по улучшению**:

1.  **Добавить docstring для каждой функции**:
    - Описать назначение функции, аргументы, возвращаемые значения и возможные исключения.
2.  **Улучшить аннотацию типов**:
    - Добавить аннотации типов для всех переменных, где это возможно.
3.  **Исправить обработку исключений**:
    - Использовать `ex` вместо `e` при обработке исключений.
    - Добавить логирование ошибок с использованием `logger.error`.
4.  **Улучшить стиль кода**:
    - Привести код в соответствие со стандартами PEP8.
5.  **Добавить обработку ошибок**:
    - Добавить обработку возможных ошибок при работе с базой данных и Telegram API.

**Оптимизированный код**:

```python
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.dao import UserDAO
from bot.user.kbs import main_user_kb, purchases_kb
from bot.user.schemas import TelegramIDModel, UserModel
from src.logger import logger # Import logger

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message, session_with_commit: AsyncSession) -> None:
    """
    Обработчик команды `/start`. Регистрирует пользователя в базе данных, если его там нет.
    Args:
        message (Message): Объект сообщения от Telegram.
        session_with_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
    Returns:
        None
    """
    user_id: int = message.from_user.id
    user_info = await UserDAO.find_one_or_none(
        session=session_with_commit,
        filters=TelegramIDModel(telegram_id=user_id)
    )

    if user_info:
        await message.answer(
            f"👋 Привет, {message.from_user.full_name}! Выберите необходимое действие",
            reply_markup=main_user_kb(user_id)
        )
        return

    values: UserModel = UserModel(
        telegram_id=user_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    await UserDAO.add(session=session_with_commit, values=values)
    await message.answer(f"🎉 <b>Благодарим за регистрацию!</b>. Теперь выберите необходимое действие.",
                         reply_markup=main_user_kb(user_id))


@user_router.callback_query(F.data == "home")
async def page_home(call: CallbackQuery) -> None:
    """
    Обработчик callback-запроса для кнопки "Домой".
    Args:
        call (CallbackQuery): Объект callback-запроса от Telegram.
    Returns:
        None
    """
    await call.answer("Главная страница")
    await call.message.answer(
        f"👋 Привет, {call.from_user.full_name}! Выберите необходимое действие",
        reply_markup=main_user_kb(call.from_user.id)
    )


@user_router.callback_query(F.data == "about")
async def page_about(call: CallbackQuery) -> None:
    """
    Обработчик callback-запроса для кнопки "О магазине".
    Args:
        call (CallbackQuery): Объект callback-запроса от Telegram.
    Returns:
        None
    """
    await call.answer("О магазине")
    await call.message.answer(
        text=(
            "🎓 Добро пожаловать в наш учебный магазин!\n\n"
            "🚀 Этот бот создан как демонстрационный проект для статьи на Хабре.\n\n"
            "👨\u200d💻 Автор: Яковенко Алексей\n\n"
            "🛍️ Здесь вы можете изучить принципы работы телеграм-магазина, "
            "ознакомиться с функциональностью и механизмами взаимодействия с пользователем.\n\n"
            "📚 Этот проект - это отличный способ погрузиться в мир разработки ботов "
            "и электронной коммерции в Telegram.\n\n"
            "💡 Исследуйте, учитесь и вдохновляйтесь!\n\n"
            "Данные для тестовой оплаты:\n\n"
            "Карта: 1111 1111 1111 1026\n"
            "Годен до: 12/26\n"
            "CVC-код: 000\n"
        ),
        reply_markup=call.message.reply_markup
    )


@user_router.callback_query(F.data == "my_profile")
async def page_about(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обработчик callback-запроса для кнопки "Мой профиль".
    Args:
        call (CallbackQuery): Объект callback-запроса от Telegram.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
    Returns:
        None
    """
    await call.answer("Профиль")

    # Получаем статистику покупок пользователя
    purchases: dict = await UserDAO.get_purchase_statistics(session=session_without_commit, telegram_id=call.from_user.id)
    total_amount: int = purchases.get("total_amount", 0)
    total_purchases: int = purchases.get("total_purchases", 0)

    # Формируем сообщение в зависимости от наличия покупок
    if total_purchases == 0:
        await call.message.answer(
            text="🔍 <b>У вас пока нет покупок.</b>\n\n"
                 "Откройте каталог и выберите что-нибудь интересное!",
            reply_markup=main_user_kb(call.from_user.id)
        )
    else:
        text: str = (
            f"🛍 <b>Ваш профиль:</b>\n\n"
            f"Количество покупок: <b>{total_purchases}</b>\n"
            f"Общая сумма: <b>{total_amount}₽</b>\n\n"
            "Хотите просмотреть детали ваших покупок?"
        )
        await call.message.answer(
            text=text,
            reply_markup=purchases_kb()
        )


@user_router.callback_query(F.data == "purchases")
async def page_user_purchases(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обработчик callback-запроса для кнопки "Мои покупки".
    Args:
        call (CallbackQuery): Объект callback-запроса от Telegram.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
    Returns:
        None
    """
    await call.answer("Мои покупки")
    try:
        await call.message.delete()
    except Exception as ex: # Change e to ex
        logger.error('Error while deleting message', ex, exc_info=True) # Add logging

    # Получаем список покупок пользователя
    purchases = await UserDAO.get_purchased_products(session=session_without_commit, telegram_id=call.from_user.id)

    if not purchases:
        await call.message.answer(
            text=f"🔍 <b>У вас пока нет покупок.</b>\n\n"
                 f"Откройте каталог и выберите что-нибудь интересное!",
            reply_markup=main_user_kb(call.from_user.id)
        )
        return

    # Для каждой покупки отправляем информацию
    for purchase in purchases:
        product = purchase.product
        file_text = "📦 <b>Товар включает файл:</b>" if product.file_id else "📄 <b>Товар не включает файлы:</b>"

        product_text = (
            f"🛒 <b>Информация о вашем товаре:</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔹 <b>Название:</b> <i>{product.name}</i>\n"
            f"🔹 <b>Описание:</b>\n<i>{product.description}</i>\n"
            f"🔹 <b>Цена:</b> <b>{product.price} ₽</b>\n"
            f"🔹 <b>Закрытое описание:</b>\n<i>{product.hidden_content}</i>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"{file_text}\n"
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
        text="🙏 Спасибо за доверие!",
        reply_markup=main_user_kb(call.from_user.id)
    )