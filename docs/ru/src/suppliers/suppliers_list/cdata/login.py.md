# Модуль `login.py`

## Обзор

Модуль `login.py` предназначен для реализации интерфейса авторизации на веб-сайте `https://reseller.c-data.co.il/Login` с использованием веб-драйвера. Он содержит функцию `login`, которая выполняет следующие шаги: открывает страницу авторизации, заполняет поля email и пароля, нажимает кнопку входа и логирует успешную авторизацию.

## Подробнее

Модуль предназначен для автоматизации процесса входа в систему `C-data` через веб-интерфейс. Используется веб-драйвер для взаимодействия с элементами страницы.
Расположение файла в структуре проекта указывает на его принадлежность к модулю `cdata` в рамках поставщиков (`suppliers`). Это подразумевает, что модуль отвечает за специфическую логику авторизации для данного поставщика.

## Функции

### `login`

```python
def login(self) -> bool:
    """
    Выполняет авторизацию на сайте C-data.

    Args:
        self: Объект класса, в котором определен метод. Предполагается, что объект имеет атрибуты `get_url`, `locators`, `find`, `print` и `log`.

    Returns:
        bool: `True` в случае успешной авторизации.

    Raises:
        Нет явных исключений, но возможны исключения, связанные с работой веб-драйвера,
        например, `NoSuchElementException`, если не удается найти элементы на странице.
    """
```

**Назначение**:
Функция `login` выполняет процесс авторизации на сайте `C-data`. Она открывает страницу входа, заполняет поля email и пароля, нажимает кнопку входа и логирует факт успешной авторизации.

**Параметры**:
- `self`: Экземпляр класса, содержащего метод `login`. Ожидается, что `self` имеет доступ к атрибутам и методам, необходимым для взаимодействия с веб-драйвером и параметрами авторизации.

**Возвращает**:
- `True`: Если авторизация прошла успешно.

**Как работает функция**:
1.  Открывает страницу авторизации, используя метод `self.get_url('https://reseller.c-data.co.il/Login')`.
2.  Извлекает данные для email и пароля из атрибута `self.locators['login']`.
3.  Определяет локаторы для полей email, пароля и кнопки входа, извлекая их из `self.locators['login']`.
4.  Выводит в лог локаторы для email, пароля и кнопки входа, используя `self.print()`.
5.  Находит элементы email и пароля на странице, используя `self.find()`, и заполняет их значениями email и пароля соответственно.
6.  Находит и нажимает кнопку входа, используя `self.find(loginbutton_locator).click()`.
7.  Логирует успешную авторизацию, используя `self.log('C-data logged in')`.
8.  Возвращает `True`, указывая на успешное завершение процесса авторизации.

**Примеры**:

```python
# Пример вызова функции login
# Предполагается, что существует объект класса, у которого есть метод login
# и необходимые атрибуты (get_url, locators, find, print, log)
class CDATAClient:
    def __init__(self, driver):
        self.driver = driver
        self.locators = {
            'login': {
                'email': 'test@example.com',
                'password': 'password',
                'email_locator': {'by': 'XPATH', 'selector': '//input[@id="email"]'},
                'password_locator': {'by': 'XPATH', 'selector': '//input[@id="password"]'},
                'loginbutton_locator': {'by': 'XPATH', 'selector': '//button[@id="login"]'}
            }
        }

    def get_url(self, url):
        self.driver.get(url)

    def find(self, locator):
        from selenium.webdriver.common.by import By
        by_method = getattr(By, locator[0])
        return self.driver.find_element(by_method, locator[1])

    def log(self, message):
        print(message)
    def print(self, message):
        print(message)
    def login(self):
        self.get_url('https://reseller.c-data.co.il/Login')

        email = self.locators['login']['email']
        password = self.locators['login']['password']

        email_locator = (self.locators['login']['email_locator']['by'],
                            self.locators['login']['email_locator']['selector'])

        password_locator = (self.locators['login']['password_locator']['by'],
                                self.locators['login']['password_locator']['selector'])

        loginbutton_locator =  (self.locators['login']['loginbutton_locator']['by'],
                                    self.locators['login']['loginbutton_locator']['selector'])


        self.print(f''' email_locator {email_locator}
                password_locator {password_locator}
                loginbutton_locator {loginbutton_locator}''')

        self.find(email_locator).send_keys(email)
        self.find(password_locator).send_keys(password)
        self.find(loginbutton_locator).click()
        self.log('C-data logged in')
        return True
# Пример использования
# from selenium import webdriver
# driver = webdriver.Chrome()  # Инициализация веб-драйвера Chrome
# client = CDATAClient(driver)
# success = client.login()
# print(f"Login successful: {success}")
# driver.quit()  # Закрытие веб-драйвера
```

В данном примере, создан класс `CDATAClient`, который имитирует взаимодействие с веб-драйвером и содержит необходимую информацию для авторизации. Затем создается экземпляр этого класса, вызывается метод `login`, и результат выводится в консоль.
Обрати внимание, что для запуска этого примера требуется установленный веб-драйвер (например, ChromeDriver для Chrome) и библиотека Selenium.