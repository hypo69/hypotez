# Документация для `switch_account.py`

## Обзор

Файл `switch_account.py` содержит функцию `switch_account`, предназначенную для переключения между аккаунтами в Facebook с использованием веб-драйвера. Он загружает локаторы из JSON-файла и использует их для взаимодействия с элементами на веб-странице.

## Более подробно

Этот код используется для автоматизации процесса переключения аккаунтов в Facebook. Он необходим для работы с рекламными кампаниями и другими функциями, требующими управления несколькими аккаунтами.

## Функции

### `switch_account`

```python
def switch_account(driver: Driver):
    """ Если есть кнопка `Переключить` - нажимаю её  """
    driver.execute_locator(locator.switch_to_account_button)
```

**Назначение**:

Функция выполняет переключение между аккаунтами в Facebook, если доступна кнопка "Переключить".

**Параметры**:

- `driver` (Driver): Экземпляр веб-драйвера, используемый для взаимодействия с веб-страницей.

**Возвращает**:

- `None`: Функция ничего не возвращает.

**Как работает функция**:

1. Функция `switch_account` принимает экземпляр веб-драйвера `driver`.
2. Вызывает метод `execute_locator` у драйвера, передавая локатор кнопки переключения аккаунта `locator.switch_to_account_button`. Этот метод нажимает на кнопку "Переключить", если она присутствует на странице.

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.endpoints.advertisement.facebook.scenarios.switch_account import switch_account

# Создание экземпляра драйвера Firefox
driver = Driver(Firefox)
# Вызов функции switch_account для переключения аккаунта
switch_account(driver)