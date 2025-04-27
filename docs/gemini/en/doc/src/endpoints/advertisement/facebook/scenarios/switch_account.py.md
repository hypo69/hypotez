# Переключение между аккаунтами

## Обзор

Модуль `switch_account.py` реализует сценарий переключения между аккаунтами в Facebook.

## Details

Этот код находится в директории `src/endpoints/advertisement/facebook/scenarios` и содержит функцию `switch_account`, которая выполняет переключение между аккаунтами.

## Функции

### `switch_account`

**Purpose**:  Функция `switch_account` осуществляет переключение между аккаунтами Facebook.

**Parameters**:

- `driver` (Driver): Объект класса `Driver`  из модуля `src.webdriver.driver`, представляющий собой драйвер веб-браузера.

**How the Function Works**:

- Функция проверяет наличие кнопки "Переключить" на странице.
- Если кнопка "Переключить" найдена, она нажимается.
- Переключение между аккаунтами Facebook осуществляется.

**Examples**:

```python
from src.webdriver.driver import Driver
from src.endpoints.advertisement.facebook.scenarios.switch_account import switch_account

# Создаем объект драйвера Chrome
driver = Driver(Chrome)
# Выполняем переключение между аккаунтами
switch_account(driver)
```