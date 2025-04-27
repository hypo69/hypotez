# Модуль для работы с языками в PrestaShop

## Обзор

Модуль предоставляет интерфейс для взаимодействия с сущностью `language` в CMS `Prestashop` через `API PrestaShop`.

## Детали

Модуль используется для выполнения следующих задач:

- Получение списка языков, доступных в магазине PrestaShop.
- Получение деталей конкретного языка по его идентификатору.
- Добавление нового языка в магазин.
- Обновление данных существующего языка.
- Удаление языка из магазина.

## Классы

### `PrestaLanguage`

**Описание**: Класс, отвечающий за настройки языков магазина PrestaShop.

**Наследует**: `PrestaShop`

**Атрибуты**:

- `API_DOMAIN` (str): Домен API PrestaShop.
- `API_KEY` (str): Ключ API PrestaShop.

**Методы**:

- `get_lang_name_by_index(lang_index: int | str) -> str`: Функция извлекает ISO код языка из магазина `Prestashop`.
- `get_languages_schema() -> Optional[dict]`: Функция извлекает словарь актуальных языков для данного магазина.

#### `get_lang_name_by_index`

**Цель**: Функция извлекает ISO код языка из магазина `Prestashop`.

**Параметры**:

- `lang_index` (int | str): Индекс языка в таблице PrestaShop.

**Возвращает**:

- `str`: Имя языка ISO по его индексу в таблице PrestaShop.

**Возможные исключения**:

- `Exception`: В случае ошибки при получении языка по индексу.

**Как работает функция**:

Функция отправляет запрос к API PrestaShop для получения информации о языке по его индексу. 

**Примеры**:

```python
>>> prestalanguage = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)
>>> prestalanguage.get_lang_name_by_index(1)
'en'
>>> prestalanguage.get_lang_name_by_index(2)
'he'
```

#### `get_languages_schema`

**Цель**: Функция извлекает словарь актуальных языков для данного магазина.

**Параметры**:

- Отсутствуют.

**Возвращает**:

- `Optional[dict]`:  Схема языков или `None` в случае ошибки.

**Возможные исключения**:

- `Exception`: В случае ошибки при получении схемы языков.

**Как работает функция**:

Функция отправляет запрос к API PrestaShop для получения схемы языков.

**Примеры**:

```python
>>> prestalanguage = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)
>>> prestalanguage.get_languages_schema()
{
    "languages": {
            "language": [
                            {
                            "attrs": {
                                "id": "1"
                            },
                            "value": ""
                            },
                            {
                            "attrs": {
                                "id": "2"
                            },
                            "value": ""
                            },
                            {
                            "attrs": {
                                "id": "3"
                            },
                            "value": ""
                            }
                        ]
    }
}
```

## Функции

### `main`

**Цель**:  Функция, запускаемая при выполнении модуля.

**Параметры**:

- Отсутствуют.

**Возвращает**:

- Отсутствует.

**Как работает функция**:

Функция создает экземпляр класса `PrestaLanguage`, получает схему языков и выводит ее на консоль.

**Примеры**:

```python
>>> asyncio.run(main())
{
    "languages": {
            "language": [
                            {
                            "attrs": {
                                "id": "1"
                            },
                            "value": ""
                            },
                            {
                            "attrs": {
                                "id": "2"
                            },
                            "value": ""
                            },
                            {
                            "attrs": {
                                "id": "3"
                            },
                            "value": ""
                            }
                        ]
    }
}
```

## Примеры

```python
# Создание экземпляра класса PrestaLanguage
prestalanguage = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)

# Получение ISO кода языка по индексу
lang_name = prestalanguage.get_lang_name_by_index(1)
print(f"Имя языка по индексу 1: {lang_name}")

# Получение схемы языков
languages_schema = prestalanguage.get_languages_schema()
print(f"Схема языков: {languages_schema}")
```

##  Дополнительные замечания

- Модуль использует модуль `logger` для вывода логов.
- Для получения схемы языков используется метод `_exec` класса `PrestaShop`, который отправляет запрос к API PrestaShop.
- Модуль предполагает, что у каждого магазина своя нумерация языков.
-  Модуль импортирует модули `asyncio`, `header`, `gs`, `PrestaShop`, `PrestaShopException`, `pprint` (как `print`) и `logger`.