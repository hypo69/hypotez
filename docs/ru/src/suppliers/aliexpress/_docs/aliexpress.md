# Модуль Aliexpress

## Обзор

Модуль `aliexpress` предоставляет класс `Aliexpress`, который объединяет функциональность классов `Supplier`, `AliRequests` и `AliApi` для взаимодействия с AliExpress. Он предназначен для задач, связанных с парсингом и взаимодействием с API AliExpress.

## Оглавление

- [Модуль Aliexpress](#модуль-aliexpress)
- [Класс Aliexpress](#класс-aliexpress)
  - [Метод __init__](#метод-__init__)

## Класс Aliexpress

### `Aliexpress`

**Описание**: Базовый класс для работы с AliExpress. Объединяет возможности классов `Supplier`, `AliRequests` и `AliApi` для удобного взаимодействия с AliExpress.

**Примеры использования**:

```python
# Инициализация без WebDriver
a = Aliexpress()

# Chrome WebDriver
a = Aliexpress('chrome')

# Режим Requests
a = Aliexpress(requests=True)
```

### Метод `__init__`

**Описание**: Инициализирует класс `Aliexpress`.

**Параметры**:

- `webdriver` (bool | str, optional): Определяет режим использования WebDriver. Возможные значения:
  - `False` (default): Без WebDriver.
  - `'chrome'`: Chrome WebDriver.
  - `'mozilla'`: Mozilla WebDriver.
  - `'edge'`: Edge WebDriver.
  - `'default'`: WebDriver по умолчанию в системе.
- `locale` (str | dict, optional): Настройки языка и валюты. По умолчанию `{'EN': 'USD'}`.
- `*args`: Дополнительные позиционные аргументы.
- `**kwargs`: Дополнительные именованные аргументы.

**Примеры**:

```python
# Инициализация без WebDriver
a = Aliexpress()

# Chrome WebDriver
a = Aliexpress('chrome')
```

**Возвращает**:
- Не возвращает значение.

**Вызывает исключения**:
- Возможные исключения, связанные с инициализацией WebDriver или ошибками при взаимодействии с AliExpress.

**Как работает функция**:

1. **Инициализация**:
   Функция инициализирует класс `Aliexpress` с заданными параметрами.

2. **Определение типа WebDriver**:
   Проверяется, какой тип WebDriver указан в параметре `webdriver`. В зависимости от значения, будет использован соответствующий WebDriver или он не будет использоваться вовсе.

3. **Настройка локали**:
   Если параметр `locale` предоставлен (в виде строки или словаря), он используется для настройки локали. В противном случае используется локаль по умолчанию `{'EN': 'USD'}`.

4. **Инициализация внутренних компонентов**:
   Создаются экземпляры классов `Supplier`, `AliRequests` и `AliApi`. Это включает настройку соединений, инициализацию структур данных и конфигураций.

5. **Присвоение (необязательных) аргументов**:
   Аргументы `*args` и `**kwargs` передаются внутренним компонентам (`Supplier`, `AliRequests`, `AliApi`).

**ASCII flowchart**:

```
Начало
│
├─── webdriver == 'chrome' or 'mozilla' or 'edge' or 'default'? ── ДА ── Использовать указанный/системный WebDriver
│   │                                                                  │
│   └─── НЕТ ── webdriver == False? ──────────────────────────────── ДА ── Не использовать WebDriver
│       │                                                                  │
│       └─── НЕТ ────────────────────────────────────────────────── Ошибка
│
│
├─── locale передан (str или dict)? ── ДА ── Использовать указанную локаль
│   │                                        │
│   └─── НЕТ ──────────────────────── Использовать локаль по умолчанию {'EN': 'USD'}
│
│
├─── Инициализация Supplier
│
├─── Инициализация AliRequests
│
├─── Инициализация AliApi
│
└─── Передача *args и **kwargs внутренним компонентам
│
Конец
```

**Примеры**:

```python
# Инициализация Aliexpress без WebDriver и с локалью по умолчанию
a = Aliexpress()

# Инициализация Aliexpress с Chrome WebDriver и локалью по умолчанию
a = Aliexpress('chrome')

# Инициализация Aliexpress с Chrome WebDriver и указанной локалью
a = Aliexpress('chrome', locale={'RU': 'RUB'})

# Инициализация Aliexpress без WebDriver и с указанной локалью
a = Aliexpress(webdriver=False, locale={'RU': 'RUB'})
```