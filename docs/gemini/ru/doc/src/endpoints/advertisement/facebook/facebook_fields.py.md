# Модуль `facebook_fields`

## Обзор

Модуль `facebook_fields` обеспечивает доступ к полям, используемым для Facebook-объявлений и событий. 

## Подробней

Данный модуль предоставляет класс `FacebookFields`, который загружает данные о полях из JSON-файла. 
Файл `facebook_feilds.json` содержит список полей, необходимых для работы с объявлениями и событиями на Facebook. 
Класс `FacebookFields` предоставляет доступ к этим полям в виде атрибутов.

## Классы

### `FacebookFields`

**Описание**: Класс `FacebookFields`  предоставляет доступ к полям, используемым для Facebook-объявлений и событий. 
**Наследует**: 
**Атрибуты**:
   - `__init__`: конструктор класса, который инициализирует экземпляр `FacebookFields`, загружая поля из файла `facebook_feilds.json`.
   - `_payload`: приватный метод, который загружает поля из файла `facebook_feilds.json`  и устанавливает их как атрибуты объекта.

## Методы

### `__init__`

**Назначение**: Конструктор класса, инициализирует экземпляр `FacebookFields` и загружает поля из файла `facebook_feilds.json`.
**Параметры**: 
  - **self**: ссылка на текущий экземпляр. 
**Возвращает**:  `None`.
**Вызывает исключения**:  `None`

### `_payload`

**Назначение**:  Приватный метод, который загружает поля из файла `facebook_feilds.json` и устанавливает их как атрибуты объекта.
**Параметры**: 
  - **self**: ссылка на текущий экземпляр. 
**Возвращает**:  `bool`: `True`, если загрузка прошла успешно,  `False`  в случае ошибки.
**Вызывает исключения**:  `None`

**Пример**:

```python
from src.endpoints.advertisement.facebook.facebook_fields import FacebookFields

# Создание экземпляра класса
fields = FacebookFields()

# Доступ к полям
print(fields.name) # Вывод значения поля "name" из файла facebook_feilds.json
print(fields.ad_name) # Вывод значения поля "ad_name" из файла facebook_feilds.json
```

## Примеры

```python
from src.endpoints.advertisement.facebook.facebook_fields import FacebookFields

# Создание экземпляра класса
fields = FacebookFields()

# Доступ к полям
print(fields.name) # Вывод значения поля "name" из файла facebook_feilds.json
print(fields.ad_name) # Вывод значения поля "ad_name" из файла facebook_feilds.json