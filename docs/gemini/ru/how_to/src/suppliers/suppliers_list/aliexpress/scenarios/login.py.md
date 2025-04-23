### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для автоматического входа в аккаунт AliExpress с использованием WebDriver. Он выполняет шаги по открытию страницы входа, принятию cookies, вводу email и пароля, а также нажатию кнопки входа.

Шаги выполнения
-------------------------
1. **Инициализация WebDriver**:
   - Функция принимает объект `Supplier`, содержащий WebDriver (`s.driver`) и локаторы (`s.locators['login']`).
   - WebDriver используется для управления браузером.

2. **Переход на страницу AliExpress**:
   - WebDriver открывает главную страницу AliExpress (`https://www.aliexpress.com`).

3. **Принятие cookies**:
   - Функция выполняет действие для принятия cookies, используя локатор `cookies_accept`.
   - Вызывается метод `_d.execute_locator(_l['cookies_accept'])`, который выполняет клик по элементу, отвечающему за принятие cookies.
   - Задержка в 0.7 секунды (`_d.wait(.7)`) после выполнения действия.

4. **Открытие формы входа**:
   - Функция выполняет действие для открытия формы входа, используя локатор `open_login`.
   - Вызывается метод `_d.execute_locator(_l['open_login'])`, который выполняет клик по элементу, открывающему форму входа.
   - Задержка в 2 секунды (`_d.wait(2)`) после выполнения действия.

5. **Ввод email**:
   - Функция пытается ввести email, используя локатор `email_locator`.
   - Вызывается метод `_d.execute_locator(_l['email_locator'])`, который возвращает `True` при успешном выполнении и `False` в противном случае.
   - Если ввод email не удался, в коде предусмотрена логика обработки `False` (TODO).
   - Задержка в 0.7 секунды (`_d.wait(.7)`) после выполнения действия.

6. **Ввод пароля**:
   - Функция пытается ввести пароль, используя локатор `password_locator`.
   - Вызывается метод `_d.execute_locator(_l['password_locator'])`, который возвращает `True` при успешном выполнении и `False` в противном случае.
   - Если ввод пароля не удался, в коде предусмотрена логика обработки `False` (TODO).
   - Задержка в 0.7 секунды (`_d.wait(.7)`) после выполнения действия.

7. **Нажатие кнопки входа**:
   - Функция пытается нажать кнопку входа, используя локатор `loginbutton_locator`.
   - Вызывается метод `_d.execute_locator(_l['loginbutton_locator'])`, который возвращает `True` при успешном выполнении и `False` в противном случае.
   - Если нажатие кнопки входа не удалось, в коде предусмотрена логика обработки `False` (TODO).

Пример использования
-------------------------

```python
import pytest
from src.suppliers.supplier import Supplier
from src.webdriver import Driver, Chrome
from src.config import Config
from src.logger.logger import logger

def test_login():
    # Инициализация WebDriver
    driver = Driver(Chrome)

    # Создание объекта Supplier
    supplier = Supplier(
        name='aliexpress',
        url='https://www.aliexpress.com',
        driver=driver,
        profile=Config.get_supplier_profile(supplier_name='aliexpress')
    )

    # Определение локаторов для входа (пример)
    supplier.locators = {
        'login': {
            'cookies_accept': {'by': 'XPATH', 'selector': '//button[contains(text(),"OK")]'},
            'open_login': {'by': 'XPATH', 'selector': '//a[@id="login-link"]'},
            'email_locator': {'by': 'ID', 'selector': 'fm-login-id'},
            'password_locator': {'by': 'ID', 'selector': 'fm-login-password'},
            'loginbutton_locator': {'by': 'XPATH', 'selector': '//button[contains(@class, "fm-submit")]'}
        }
    }

    # Вызов функции login
    result = login(supplier)

    # Логирование результата
    logger.info(f'Результат входа: {result}')

    # Закрытие браузера
    driver.close()