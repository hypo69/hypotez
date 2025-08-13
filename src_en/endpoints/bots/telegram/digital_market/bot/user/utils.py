from aiogram import Bot
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from bot.config import settings
from bot.dao.dao import PurchaseDao, ProductDao
from bot.user.kbs import main_user_kb
from bot.user.schemas import PaymentData


async def successful_payment_logic(session: AsyncSession, payment_data, currency, user_tg_id, bot: Bot):
    product_id = int(payment_data.get("product_id"))
    price = payment_data.get("price")
    payment_type = payment_data.get("payment_type")
    payment_id = payment_data.get("payment_id")
    user_id = payment_data.get("user_id")
    await PurchaseDao.add(session=session, values=PaymentData(**payment_data))
    product_data = await ProductDao.find_one_or_none_by_id(session=session,
                                                           data_id=product_id)

    # Sending notifications to administrators
    for admin_id in settings.ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=(
                    f"💲 Пользователь c ID {user_id} купил товар <b>{product_data.name}</b> (ID: {product_id}) "
                    f"за <b>{price} {currency}</b>."
                )
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления администраторам: {e}")

    # Sending information to the user
    file_text = "📦 <b>Товар включает файл:</b>" if product_data.file_id else "📄 <b>Товар не включает файлы:</b>"
    product_text = (
        f"🎉 <b>Спасибо за покупку!</b>\n\n"
        f"🛒 <b>Информация о вашем товаре:</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🔹 <b>Название:</b> <b>{product_data.name}</b>\n"
        f"🔹 <b>Описание:</b>\n<i>{product_data.description}</i>\n"
        f"🔹 <b>Цена:</b> <b>{price} {currency}</b>\n"
        f"🔹 <b>Закрытое описание:</b>\n<i>{product_data.hidden_content}</i>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"{file_text}\n\n"
        f"ℹ️ <b>Информацию о всех ваших покупках вы можете найти в личном профиле.</b>"
    )

    if product_data.file_id:
        await bot.send_document(document=product_data.file_id,
                                chat_id=user_tg_id,
                                caption=product_text, reply_markup=main_user_kb(user_tg_id))

    else:
        await bot.send_message(chat_id=user_tg_id, text=product_text, reply_markup=main_user_kb(user_tg_id))

    # Automatic return for purchase
    if payment_type == 'stars':
        await bot.refund_star_payment(user_id=user_tg_id, telegram_payment_charge_id=payment_id)