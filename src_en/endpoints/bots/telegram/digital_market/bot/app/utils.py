import hashlib
from urllib import parse
from urllib.parse import urlparse
from bot.config import settings


def calculate_signature(login, cost, inv_id, password, user_id, user_telegram_id, product_id, is_result=False):
    if is_result:
        base_string = f"{cost}:{inv_id}:{password}"  # For a result URL
    else:
        base_string = f"{login}:{cost}:{inv_id}:{password}"  # For Initital URL and Success url

    additional_params = {
        'Shp_user_id': user_id,
        'Shp_user_telegram_id': user_telegram_id,
        'Shp_product_id': product_id
    }
    for key, value in sorted(additional_params.items()):
        base_string += f":{key}={value}"

    return hashlib.md5(base_string.encode('utf-8')).hexdigest()


def generate_payment_link(cost: float, number: int, description: str,
                          user_id: int, user_telegram_id: int, product_id: int,
                          is_test=1, robokassa_payment_url='https://auth.robokassa.ru/Merchant/Index.aspx') -> str:
    """Generates a link for payment via Robokassa with mandatory parameters.

    : Param Cost: The cost of goods
    : Param Number: Order Number
    : Param Description: Order Description
    : Param User_id: User ID
    : Param user_telegram_id: Telegram ID user
    : Param Product_id: Product ID
    : param is_test: test mode flag (1 - test, 0 - combat mode)
    : PAram Robokassa_Payment_URL: URL for payment Robokassa
    : Return: link to payment page"""
    signature = calculate_signature(
        settings.MRH_LOGIN,
        cost,
        number,
        settings.MRH_PASS_1,
        user_id,
        user_telegram_id,
        product_id
    )

    data = {
        'MerchantLogin': settings.MRH_LOGIN,
        'OutSum': cost,
        'InvId': number,
        'Description': description,
        'SignatureValue': signature,
        'IsTest': is_test,
        'Shp_user_id': user_id,
        'Shp_user_telegram_id': user_telegram_id,
        'Shp_product_id': product_id
    }

    return f'{robokassa_payment_url}?{parse.urlencode(data)}'


def parse_response(request: str) -> dict:
    """It is separated by the query on the parameter.

    :param request: String request
    :return: Dictionary with parameters"""
    return dict(parse.parse_qsl(urlparse(request).query))


def check_signature_result(out_sum, inv_id, received_signature, password, user_id, user_telegram_id, product_id) -> bool:
    signature = calculate_signature(
        settings.MRH_LOGIN,
        out_sum,
        inv_id,
        password,
        user_id,
        user_telegram_id,
        product_id,
        is_result=True  # Important flag for Result url
    )
    return signature.lower() == received_signature.lower()


def result_payment(request: str) -> str:
    """Processing the result of payment (resulturl).

    : Param Request: Request string with payment parameters
    : return: 'ok' + order number, if payment was successful, otherwise 'bad sign'"""
    params = parse_response(request)
    out_sum = params['OutSum']
    inv_id = params['InvId']
    signature = params['SignatureValue']
    user_id = params['Shp_user_id']
    user_telegram_id = params['Shp_user_telegram_id']
    product_id = params['Shp_product_id']

    if check_signature_result(out_sum, inv_id, signature, settings.MRH_PASS_2, user_id, user_telegram_id, product_id):
        return f'OK{inv_id}'
    return "bad sign"


def check_success_payment(request: str) -> str:
    """Checks the success of payment (SUCCESSURL).

    : Param Request: Request string with payment parameters
    : Return: Successful payment message or 'bad sign' with the wrong signature"""
    params = parse_response(request)
    out_sum = params['OutSum']
    inv_id = params['InvId']
    signature = params['SignatureValue']
    user_id = params['Shp_user_id']
    user_telegram_id = params['Shp_user_telegram_id']
    product_id = params['Shp_product_id']

    if check_signature_result(out_sum, inv_id, signature, settings.MRH_PASS_1, user_id, user_telegram_id, product_id):
        return "Thank you for using our service"
    return "bad sign"
