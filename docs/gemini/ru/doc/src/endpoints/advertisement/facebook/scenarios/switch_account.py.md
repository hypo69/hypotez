# Переключение между аккаунтами Facebook

## Обзор

Этот модуль предоставляет функцию `switch_account`, которая используется для переключения между аккаунтами в Facebook. 
Функция предназначена для автоматизации процесса переключения аккаунтов с помощью веб-драйвера. 

## Подробней

Модуль использует веб-драйвер (`driver`) для автоматизации действий в веб-браузере. 
Он содержит локаторы для элементов на странице Facebook, которые используются для переключения между аккаунтами. 
Функция `switch_account` выполняет поиск кнопки "Переключить" и нажимает ее.
Функция предполагает, что страница Facebook уже открыта и авторизована. 

## Функции

### `switch_account`

**Назначение**: Переключение между аккаунтами Facebook

**Параметры**:
- `driver` (Driver): Инстанс драйвера (например, Chrome, Firefox).

**Возвращает**:
- `None` 

**Как работает функция**:
- Функция выполняет поиск кнопки "Переключить" (`locator.switch_to_account_button`) с помощью веб-драйвера.
- Если кнопка найдена, она нажимает на нее, тем самым инициируя процесс переключения аккаунтов.

**Примеры**:

```python
from src.endpoints.advertisement.facebook.scenarios import switch_account
from src.webdriver.driver import Driver, Chrome
driver = Driver(Chrome) # Создаем инстанс драйвера
switch_account(driver) # Вызываем функцию для переключения между аккаунтами
```

## Локаторы

Модуль использует локаторы из JSON-файла `post_message.json`. 
Файл содержит локаторы для элементов на странице Facebook.

## Примеры

```python
from src.endpoints.advertisement.facebook.scenarios import switch_account
from src.webdriver.driver import Driver, Chrome
driver = Driver(Chrome) # Создаем инстанс драйвера
switch_account(driver) # Вызываем функцию для переключения между аккаунтами
```