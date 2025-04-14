### **Анализ кода модуля `admin.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/admin/admin.py

Модуль содержит набор обработчиков для админ-панели Telegram-бота, включая добавление товаров, просмотр статистики и удаление товаров.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование `aiogram` для создания Telegram-бота.
    - Применение конечных автоматов (`FSMContext`) для управления состоянием при добавлении товаров.
    - Разделение кода на отдельные обработчики для каждой функции админ-панели.
- **Минусы**:
    - Недостаточное количество комментариев и документации.
    - Обработка исключений без логирования.
    - Повторяющийся код, особенно в обработке ошибок при редактировании сообщений.
    - Отсутствуют аннотации типов для переменных в некоторых местах.

**Рекомендации по улучшению:**

1.  **Добавить документацию к каждой функции и классу**. Описать назначение, параметры и возвращаемые значения.
2.  **Добавить логирование ошибок**. Использовать `logger.error` для записи информации об ошибках, чтобы упростить отладку.
3.  **Улучшить обработку исключений**. Избегать повторения кода при обработке исключений. Можно вынести повторяющийся блок кода в отдельную функцию.
4.  **Добавить аннотации типов**. Указать типы для всех переменных, аргументов функций и возвращаемых значений.
5.  **Использовать более конкретные исключения**. Вместо `Exception as e` использовать более конкретные типы исключений, такие как `AiogramError`, `ValueError` и т.д.
6.  **Улучшить форматирование кода**. Следовать стандартам PEP8 для улучшения читаемости кода.
7.  **Избавиться от дублирования кода**. Например, повторяющийся код в блоках `try...except` можно вынести в отдельную функцию.

**Оптимизированный код:**

```python
import asyncio
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.logger import logger  # Добавлен импорт logger
from bot.config import settings, bot
from bot.dao.dao import UserDAO, ProductDao, CategoryDao, PurchaseDao
from bot.admin.kbs import admin_kb, admin_kb_back, product_management_kb, cancel_kb_inline, catalog_admin_kb, \
    admin_send_file_kb, admin_confirm_kb, dell_product_kb
from bot.admin.schemas import ProductModel, ProductIDModel
from bot.admin.utils import process_dell_text_msg

admin_router = Router()


class AddProduct(StatesGroup):
    """
    Класс состояний для добавления нового товара.
    """
    name = State()
    description = State()
    price = State()
    file_id = State()
    category_id = State()
    hidden_content = State()
    confirm_add = State()


async def handle_admin_panel_error(call: CallbackQuery, error: Exception) -> None:
    """
    Обрабатывает ошибки при открытии админ-панели, отправляя сообщение об ошибке.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        error (Exception): Объект исключения.
    """
    error_message = "Произошла ошибка при открытии админ-панели. Пожалуйста, попробуйте еще раз."
    try:
        await call.message.answer(
            text=error_message,
            reply_markup=admin_kb()
        )
    except Exception as ex:
        logger.error("Failed to send error message", ex, exc_info=True)


@admin_router.callback_query(F.data == "admin_panel", F.from_user.id.in_(settings.ADMIN_IDS))
async def start_admin(call: CallbackQuery) -> None:
    """
    Обработчик для запуска админ-панели.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
    """
    await call.answer('Доступ в админ-панель разрешен!')
    try:
        await call.message.edit_text(
            text="Вам разрешен доступ в админ-панель. Выберите необходимое действие.",
            reply_markup=admin_kb()
        )
    except Exception as ex:
        logger.error('Error while editing admin panel message', ex, exc_info=True)
        try:
            await call.message.delete()
            await call.message.answer(
                text="Вам разрешен доступ в админ-панель. Выберите необходимое действие.",
                reply_markup=admin_kb()
            )
        except Exception as ex:
            logger.error('Error while deleting and sending admin panel message', ex, exc_info=True)
            await handle_admin_panel_error(call, ex)


@admin_router.callback_query(F.data == 'statistic', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_statistic(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обработчик для получения статистики пользователей и заказов.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy.
    """
    await call.answer('Запрос на получение статистики...')
    await call.answer('📊 Собираем статистику...')

    stats = await UserDAO.get_statistics(session=session_without_commit)
    payment_stats = await PurchaseDao.get_payment_stats(session=session_without_commit)
    stats_message = (
        "📈 Статистика пользователей:\n\n"
        f"👥 Всего пользователей: {stats['total_users']}\n"
        f"🆕 Новых за сегодня: {stats['new_today']}\n"
        f"📅 Новых за неделю: {stats['new_week']}\n"
        f"📆 Новых за месяц: {stats['new_month']}\n\n"
        f"💰 Общая статистика по заказам:\n\n{payment_stats}"
    )
    await call.message.edit_text(
        text=stats_message,
        reply_markup=admin_kb()
    )


@admin_router.callback_query(F.data == "cancel", F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_cancel(call: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для отмены сценария добавления товара.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        state (FSMContext): Объект FSMContext.
    """
    await state.clear()
    await call.answer('Отмена сценария добавления товара')
    await call.message.delete()
    await call.message.answer(
        text="Отмена добавления товара.",
        reply_markup=admin_kb_back()
    )


@admin_router.callback_query(F.data == 'delete_product', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_start_dell(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обработчик для запуска режима удаления товаров.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy.
    """
    await call.answer('Режим удаления товаров')
    all_products = await ProductDao.find_all(session=session_without_commit)

    await call.message.edit_text(
        text=f"На данный момент в базе данных {len(all_products)} товаров. Для удаления нажмите на кнопку ниже"
    )
    for product_data in all_products:
        file_id = product_data.file_id
        file_text = "📦 Товар с файлом" if file_id else "📄 Товар без файла"

        product_text = (f'🛒 Описание товара:\n\n'
                        f'🔹 <b>Название товара:</b> <b>{product_data.name}</b>\n'
                        f'🔹 <b>Описание:</b>\n\n<b>{product_data.description}</b>\n\n'
                        f'🔹 <b>Цена:</b> <b>{product_data.price} ₽</b>\n'
                        f'🔹 <b>Описание (закрытое):</b>\n\n<b>{product_data.hidden_content}</b>\n\n'
                        f'<b>{file_text}</b>')
        if file_id:
            await call.message.answer_document(document=file_id, caption=product_text,
                                               reply_markup=dell_product_kb(product_data.id))
        else:
            await call.message.answer(text=product_text, reply_markup=dell_product_kb(product_data.id))


@admin_router.callback_query(F.data.startswith('dell_'), F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_start_dell(call: CallbackQuery, session_with_commit: AsyncSession) -> None:
    """
    Обработчик для удаления товара.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        session_with_commit (AsyncSession): Асинхронная сессия SQLAlchemy.
    """
    product_id = int(call.data.split('_')[-1])
    await ProductDao.delete(session=session_with_commit, filters=ProductIDModel(id=product_id))
    await call.answer(f"Товар с ID {product_id} удален!", show_alert=True)
    await asyncio.sleep(1.5)
    await call.message.delete()


@admin_router.callback_query(F.data == 'process_products', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_products(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обработчик для отображения панели управления товарами.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy.
    """
    await call.answer('Режим управления товарами')
    all_products_count = await ProductDao.count(session=session_without_commit)
    await call.message.edit_text(
        text=f"На данный момент в базе данных {all_products_count} товаров. Что будем делать?",
        reply_markup=product_management_kb()
    )


@admin_router.callback_query(F.data == 'add_product', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_add_product(call: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для запуска сценария добавления товара.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        state (FSMContext): Объект FSMContext.
    """
    await call.answer('Запущен сценарий добавления товара.')
    await call.message.delete()
    msg = await call.message.answer(text="Для начала укажите имя товара: ", reply_markup=cancel_kb_inline())
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(AddProduct.name)


@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.name)
async def admin_process_name(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения имени товара.

    Args:
        message (Message): Объект Message.
        state (FSMContext): Объект FSMContext.
    """
    await state.update_data(name=message.text)
    await process_dell_text_msg(message, state)
    msg = await message.answer(text="Теперь дайте короткое описание товару: ", reply_markup=cancel_kb_inline())
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(AddProduct.description)


@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.description)
async def admin_process_description(message: Message, state: FSMContext, session_without_commit: AsyncSession) -> None:
    """
    Обработчик для получения описания товара.

    Args:
        message (Message): Объект Message.
        state (FSMContext): Объект FSMContext.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy.
    """
    await state.update_data(description=message.html_text)
    await process_dell_text_msg(message, state)
    catalog_data = await CategoryDao.find_all(session=session_without_commit)
    msg = await message.answer(text="Теперь выберите категорию товара: ", reply_markup=catalog_admin_kb(catalog_data))
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(AddProduct.category_id)


@admin_router.callback_query(F.data.startswith("add_category_"),
                             F.from_user.id.in_(settings.ADMIN_IDS),
                             AddProduct.category_id)
async def admin_process_category(call: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для получения категории товара.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        state (FSMContext): Объект FSMContext.
    """
    category_id = int(call.data.split("_")[-1])
    await state.update_data(category_id=category_id)
    await call.answer('Категория товара успешно выбрана.')
    msg = await call.message.edit_text(text="Введите цену товара: ", reply_markup=cancel_kb_inline())
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(AddProduct.price)


@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.price)
async def admin_process_price(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения цены товара.

    Args:
        message (Message): Объект Message.
        state (FSMContext): Объект FSMContext.
    """
    try:
        price = int(message.text)
        await state.update_data(price=price)
        await process_dell_text_msg(message, state)
        msg = await message.answer(
            text="Отправьте файл (документ), если требуется или нажмите на 'БЕЗ ФАЙЛА', если файл не требуется",
            reply_markup=admin_send_file_kb()
        )
        await state.update_data(last_msg_id=msg.message_id)
        await state.set_state(AddProduct.file_id)
    except ValueError as ex:
        logger.error('Invalid price value', ex, exc_info=True)
        await message.answer(text="Ошибка! Необходимо ввести числовое значение для цены.")
        return


@admin_router.callback_query(F.data == "without_file", F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.file_id)
async def admin_process_without_file(call: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для случая, когда файл для товара не требуется.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        state (FSMContext): Объект FSMContext.
    """
    await state.update_data(file_id=None)
    await call.answer('Файл не выбран.')
    msg = await call.message.edit_text(
        text="Теперь отправьте контент, который отобразится после покупки товара внутри карточки",
        reply_markup=cancel_kb_inline())
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(AddProduct.hidden_content)


@admin_router.message(F.document, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.file_id)
async def admin_process_without_file(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения файла (документа) для товара.

    Args:
        message (Message): Объект Message.
        state (FSMContext): Объект FSMContext.
    """
    await state.update_data(file_id=message.document.file_id)
    await process_dell_text_msg(message, state)
    msg = await message.answer(
        text="Теперь отправьте контент, который отобразится после покупки товара внутри карточки",
        reply_markup=cancel_kb_inline())
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(AddProduct.hidden_content)


@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.hidden_content)
async def admin_process_hidden_content(message: Message, state: FSMContext, session_without_commit: AsyncSession) -> None:
    """
    Обработчик для получения скрытого контента товара.

    Args:
        message (Message): Объект Message.
        state (FSMContext): Объект FSMContext.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy.
    """
    await state.update_data(hidden_content=message.html_text)

    product_data = await state.get_data()
    category_info = await CategoryDao.find_one_or_none_by_id(session=session_without_commit,
                                                             data_id=product_data.get("category_id"))

    file_id = product_data.get("file_id")
    file_text = "📦 Товар с файлом" if file_id else "📄 Товар без файла"

    product_text = (f'🛒 Проверьте, все ли корректно:\n\n'
                    f'🔹 <b>Название товара:</b> <b>{product_data["name"]}</b>\n'
                    f'🔹 <b>Описание:</b>\n\n<b>{product_data["description"]}</b>\n\n'
                    f'🔹 <b>Цена:</b> <b>{product_data["price"]} ₽</b>\n'
                    f'🔹 <b>Описание (закрытое):</b>\n\n<b>{product_data["hidden_content"]}</b>\n\n'
                    f'🔹 <b>Категория:</b> <b>{category_info.category_name} (ID: {category_info.id})</b>\n\n'
                    f'<b>{file_text}</b>')
    await process_dell_text_msg(message, state)

    if file_id:
        msg = await message.answer_document(document=file_id, caption=product_text, reply_markup=admin_confirm_kb())
    else:
        msg = await message.answer(text=product_text, reply_markup=admin_confirm_kb())
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(AddProduct.confirm_add)


@admin_router.callback_query(F.data == "confirm_add", F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_confirm_add(call: CallbackQuery, state: FSMContext, session_with_commit: AsyncSession) -> None:
    """
    Обработчик для подтверждения добавления товара.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        state (FSMContext): Объект FSMContext.
        session_with_commit (AsyncSession): Асинхронная сессия SQLAlchemy.
    """
    await call.answer('Приступаю к сохранению файла!')
    product_data = await state.get_data()
    await bot.delete_message(chat_id=call.from_user.id, message_id=product_data["last_msg_id"])
    del product_data["last_msg_id"]
    await ProductDao.add(session=session_with_commit, values=ProductModel(**product_data))
    await call.message.answer(text="Товар успешно добавлен в базу данных!", reply_markup=admin_kb())