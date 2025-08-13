import datetime

from aiohttp import web
from aiogram.types import Update
from loguru import logger
from bot.app.utils import check_signature_result
from bot.config import bot, dp, settings
from bot.dao.database import async_session_maker
from bot.user.utils import successful_payment_logic


async def handle_webhook(request: web.Request):
    try:
        update = Update(**await request.json())
        await dp.feed_update(bot, update)
        return web.Response(status=200)
    except Exception as e:
        logger.error(f"Ошибка при обработке вебхука: {e}")
        return web.Response(status=500)


# A function for processing a request for EndPome "HELLO, World!"
async def home_page(request: web.Request) -> web.Response:
    """Processor to display the main page with information about the service."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""<! Doctype html>
    <html lang = "ru">
    <head>
        <meta charset = "UTF-8">
        <meta name = "ViewPort" Content = "Width = Device-Width, Initial-Scale = 1.0">
        <Title> Aiohttp Demonstration </ Title>
        <Style>
            Body {{font-Family: arial, sans-serif; Line-height: 1.6; Padding: 20px; Max-Width: 800px; Margin: 0 Auto; }}
            h1 {{color: # 333; }}
            .info {{background-color: # f4f4f4; Padding: 15px; Border-Radius: 5px; Margin-Top: 20px; }}
        </style>
    </ Head>
    <body>
        <h1> Hello, my name is Yakovenko Alexey </ h1>
        <p> Here you see that Aiohttp is able to rendere with the HTML page. </p>
        <div Class = "Info">
            <p> through aiohttp, this project is processed: </p>
            <ul>
                <li> hucks from the telegrams of the bot </li>
                <li> hooks for processing answers from Robokassa </li>
            </ul>
        </div>
        <p> The current server time: {Current_time} </p>
    </body>
    </ html>"""
    return web.Response(text=html_content, content_type='text/html')


async def robokassa_result(request: web.Request) -> web.Response:
    """Processing a request from Robokassa on Resulturl.

    : Param Receist: HTTP request
    : Return: Text response with the results of the check"""
    logger.success("Получен ответ от Робокассы!")
    data = await request.post()

    # We extract the parameters from the request
    signature = data.get('SignatureValue')
    out_sum = data.get('OutSum')
    inv_id = data.get('InvId')
    user_id = data.get('Shp_user_id')
    user_telegram_id = data.get('Shp_user_telegram_id')
    product_id = data.get('Shp_product_id')

    # Checking signature
    if check_signature_result(
        out_sum=out_sum,
        inv_id=inv_id,
        received_signature=signature,
        password=settings.MRH_PASS_2,
        user_id=user_id,
        user_telegram_id=user_telegram_id,
        product_id=product_id
    ):
        result = f"OK{inv_id}"
        logger.info(f"Успешная проверка подписи для InvId: {inv_id}")

        payment_data = {
            'user_id': int(user_id),
            'payment_id': signature,
            'price': int(out_sum),
            'product_id': int(product_id),
            'payment_type': "robocassa"
        }
        async with async_session_maker() as session:
            await successful_payment_logic(
                session=session,
                payment_data=payment_data,
                currency="₽",
                user_tg_id=int(user_telegram_id),
                bot=bot
            )
            await session.commit()
    else:
        result = "bad sign"
        logger.warning(f"Неверная подпись для InvId: {inv_id}")

    logger.info(f"Ответ: {result}")
    return web.Response(text=result)


async def robokassa_fail(request):
    # We get parameters from the GET request
    inv_id = request.query.get('InvId')
    out_sum = request.query.get('OutSum')
    print(f"Неудачный платеж: сумма {out_sum}, ID {inv_id}")
    return web.Response(text="Платеж не удался", content_type='text/html')
