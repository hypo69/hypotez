# Модуль для сбора ссылок на отдельные чаты в чат-боте ChatGPT

## Обзор

Этот модуль содержит сценарий для сбора ссылок на отдельные чаты в чат-боте ChatGPT. 

## Подробнее

Сценарий использует вебдрайвер для взаимодействия с веб-страницей чат-бота и извлечения ссылок на чаты. 

## Функции

### `get_links(d:Driver)`

**Назначение**: Функция извлекает ссылки на отдельные чаты в чат-боте ChatGPT.

**Параметры**:

- `d` (Driver): Экземпляр вебдрайвера.

**Возвращает**:

- `links`: Список ссылок на отдельные чаты.

**Как работает функция**:

- Функция использует локаторы из `src.suppliers.chat_gpt.locators.chats_list.json` для поиска ссылок на чаты.
- С помощью метода `execute_locator` вебдрайвера извлекаются ссылки на чаты.
- Функция возвращает список найденных ссылок.

**Примеры**:

```python
from src.suppliers.chat_gpt.scenarios.grab_lilnks_to_chats import get_links
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox

# Создание инстанса драйвера (пример с Firefox)
driver = Driver(Firefox)
driver.get_url('https://chatgpt.com/')
links = get_links(driver)

print(links)
```

## Пример использования

```python
from src.suppliers.chat_gpt.scenarios.grab_lilnks_to_chats import get_links
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox

# Создание инстанса драйвера (пример с Firefox)
driver = Driver(Firefox)

# Загрузка страницы ChatGPT
driver.get_url('https://chatgpt.com/')

# Получение списка ссылок на чаты
links = get_links(driver)

# Вывод ссылок на консоль
for link in links:
    print(link)

# Закрытие драйвера
driver.close()
```