### **Анализ кода модуля `admin.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код разбит на логические блоки, что облегчает его понимание.
  - Использование `FSMContext` для управления состоянием пользователя.
  - Применение `aiogram` для обработки логики бота.
- **Минусы**:
  - Отсутствие логирования ошибок.
  - Некоторые участки кода содержат повторения (например, обработка исключений).
  - Не все функции и методы имеют docstring.
  - Жестко заданные тексты сообщений, что затрудняет локализацию.
  - Использование `Exception as e` вместо `Exception as ex`.

#### **Рекомендации по улучшению**:
1. **Добавить логирование**:
   - В каждый блок `try...except` добавить логирование с использованием `logger.error` для отслеживания ошибок.

2. **Улучшить обработку исключений**:
   - Избегать повторений в блоках `try...except`. Можно создать вспомогательную функцию для отправки сообщений об ошибках.

3. **Добавить docstring**:
   - Добавить docstring ко всем функциям и методам, чтобы улучшить понимание кода.

4. **Использовать `ex` вместо `e` в блоках обработки исключений**:
   - Заменить все экземпляры `Exception as e` на `Exception as ex`.

5. **Улучшить структуру сообщений**:
   - Вынести тексты сообщений в отдельные переменные или использовать шаблонизатор для упрощения локализации и изменения текстов.

6. **Улучшить обработку ошибок в `admin_process_price`**:
   - Добавить проверку на `None` или пустую строку перед попыткой преобразования в `int`.

7. **Устранить избыточность в `admin_process_start_dell`**:
   - Убрать дублирование кода, вынеся общую логику формирования сообщений в отдельную функцию.

8. **Обеспечить обработку ошибок при удалении сообщений**:
   - Добавить блок `try...except` вокруг `await bot.delete_message`, чтобы обрабатывать возможные ошибки при удалении сообщений.

9. **Использовать `j_loads` или `j_loads_ns`**:
   - Проверить, используются ли JSON-файлы конфигурации, и заменить стандартные методы чтения на `j_loads` или `j_loads_ns`.

10. **Аннотации типов**:
    - Убедиться, что все переменные и параметры функций имеют аннотации типов.

11. **Использовать webdriver**:
    - Если в коде используются элементы webdriver, убедиться, что они соответствуют правилам использования, определенным в системных инструкциях.

#### **Оптимизированный код**:

```python
import asyncio
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.config import settings, bot
from bot.dao.dao import UserDAO, ProductDao, CategoryDao, PurchaseDao
from bot.admin.kbs import admin_kb, admin_kb_back, product_management_kb, cancel_kb_inline, catalog_admin_kb, \
    admin_send_file_kb, admin_confirm_kb, dell_product_kb
from bot.admin.schemas import ProductModel, ProductIDModel
from bot.admin.utils import process_dell_text_msg
from src.logger import logger  # Добавлен импорт logger

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


@admin_router.callback_query(F.data == "admin_panel", F.from_user.id.in_(settings.ADMIN_IDS))
async def start_admin(call: CallbackQuery) -> None:
    """
    Обработчик нажатия на кнопку "admin_panel".
    Предоставляет доступ в админ-панель.

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
        logger.error('Ошибка при открытии админ-панели', ex, exc_info=True)  # Добавлено логирование
        try:
            await call.message.delete()
            await call.message.answer(
                text="Вам разрешен доступ в админ-панель. Выберите необходимое действие.",
                reply_markup=admin_kb()
            )
        except Exception as ex:
            logger.error('Ошибка при удалении и отправке сообщения в админ-панели', ex, exc_info=True)  # Добавлено логирование
            await call.message.answer(
                text="Произошла ошибка при открытии админ-панели. Пожалуйста, попробуйте еще раз.",
                reply_markup=admin_kb()
            )


@admin_router.callback_query(F.data == 'statistic', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_statistic(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обработчик нажатия на кнопку "statistic".
    Предоставляет статистику по пользователям и заказам.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        session_without_commit (AsyncSession): Асинхровая сессия SQLAlchemy.
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
    Обработчик нажатия на кнопку "cancel".
    Отменяет сценарий добавления товара.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        state (FSMContext): Объект FSMContext.
    """
    await state.clear()
    await call.answer('Отмена сценария добавления товара')
    try:
        await call.message.delete()
    except Exception as ex:
        logger.error('Ошибка при удалении сообщения об отмене', ex, exc_info=True)  # Добавлено логирование
    await call.message.answer(
        text="Отмена добавления товара.",
        reply_markup=admin_kb_back()
    )


@admin_router.callback_query(F.data == 'delete_product', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_start_dell(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обработчик нажатия на кнопку "delete_product".
    Запускает режим удаления товаров.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        session_without_commit (AsyncSession): Асинхровая сессия SQLAlchemy.
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
        try:
            if file_id:
                await call.message.answer_document(document=file_id, caption=product_text,
                                                   reply_markup=dell_product_kb(product_data.id))
            else:
                await call.message.answer(text=product_text, reply_markup=dell_product_kb(product_data.id))
        except Exception as ex:
            logger.error(f'Ошибка при отправке товара с ID {product_data.id}', ex, exc_info=True)


@admin_router.callback_query(F.data.startswith('dell_'), F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_start_dell(call: CallbackQuery, session_with_commit: AsyncSession) -> None:
    """
    Обработчик нажатия на кнопку удаления товара.
    Удаляет товар из базы данных.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        session_with_commit (AsyncSession): Асинхровая сессия SQLAlchemy с коммитом.
    """
    product_id = int(call.data.split('_')[-1])
    try:
        await ProductDao.delete(session=session_with_commit, filters=ProductIDModel(id=product_id))
        await call.answer(f"Товар с ID {product_id} удален!", show_alert=True)
        await asyncio.sleep(1.5)
        await call.message.delete()
    except Exception as ex:
        logger.error(f'Ошибка при удалении товара с ID {product_id}', ex, exc_info=True)


@admin_router.callback_query(F.data == 'process_products', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_products(call: CallbackQuery, session_without_commit: AsyncSession) -> None:
    """
    Обработчик нажатия на кнопку "process_products".
    Предоставляет инструменты для управления товарами.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        session_without_commit (AsyncSession): Асинхровая сессия SQLAlchemy.
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
    Обработчик нажатия на кнопку "add_product".
    Запускает сценарий добавления товара.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        state (FSMContext): Объект FSMContext.
    """
    await call.answer('Запущен сценарий добавления товара.')
    try:
        await call.message.delete()
    except Exception as ex:
        logger.error('Ошибка при удалении сообщения о запуске сценария добавления товара', ex, exc_info=True)
    msg = await call.message.answer(text="Для начала укажите имя товара: ", reply_markup=cancel_kb_inline())
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(AddProduct.name)


@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.name)
async def admin_process_name(message: Message, state: FSMContext) -> None:
    """
    Обработчик ввода имени товара.

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
    Обработчик ввода описания товара.

    Args:
        message (Message): Объект Message.
        state (FSMContext): Объект FSMContext.
        session_without_commit (AsyncSession): Асинхровая сессия SQLAlchemy.
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
    Обработчик выбора категории товара.

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
    Обработчик ввода цены товара.

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
        logger.error('Ошибка при вводе цены товара', ex, exc_info=True)
        await message.answer(text="Ошибка! Необходимо ввести числовое значение для цены.")
        return


@admin_router.callback_query(F.data == "without_file", F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.file_id)
async def admin_process_without_file(call: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик выбора варианта "без файла".

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
    Обработчик получения файла (документа).

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
    Обработчик ввода скрытого контента товара.

    Args:
        message (Message): Объект Message.
        state (FSMContext): Объект FSMContext.
        session_without_commit (AsyncSession): Асинхровая сессия SQLAlchemy.
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
    Обработчик подтверждения добавления товара.

    Args:
        call (CallbackQuery): Объект CallbackQuery.
        state (FSMContext): Объект FSMContext.
        session_with_commit (AsyncSession): Асинхровая сессия SQLAlchemy с коммитом.
    """
    await call.answer('Приступаю к сохранению файла!')
    product_data = await state.get_data()
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=product_data["last_msg_id"])
    except Exception as ex:
        logger.error('Ошибка при удалении сообщения о подтверждении', ex, exc_info=True)
    del product_data["last_msg_id"]
    await ProductDao.add(session=session_with_commit, values=ProductModel(**product_data))
    await call.message.answer(text="Товар успешно добавлен в базу данных!", reply_markup=admin_kb())