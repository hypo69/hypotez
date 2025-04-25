# Модуль для работы с языками в PrestaShop

## Обзор

Модуль представляет интерфейс взаимодействия с сущностью `language` в cms `Prestashop` через `API Prestashop`. 

## Подробней

Модуль обеспечивает функционал для работы с языками в PrestaShop, включая:

- Получение списка языков в магазине PrestaShop.
- Получение детальной информации о языке по его идентификатору.
- Добавление нового языка в магазин PrestaShop.
- Обновление информации о языке.
- Удаление языка из магазина PrestaShop.

## Классы

### `PrestaLanguage`

**Описание**: Класс, отвечающий за настройки языков магазина PrestaShop. 

**Наследует**: `PrestaShop`

**Атрибуты**:

- `API_DOMAIN`: Домен API PrestaShop.
- `API_KEY`: Ключ API PrestaShop.

**Методы**:

- `get_lang_name_by_index(lang_index: int | str) -> str`: Функция извлекает ISO код азыка из магазина `Prestashop`.
- `get_languages_schema() -> Optional[dict]`: Функция извлекает словарь актуальных языков дла данного магазина.

**Примеры**:

```python
>>> prestalanguage = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)
>>> prestalanguage.add_language_PrestaShop('English', 'en')
>>> prestalanguage.delete_language_PrestaShop(3)
>>> prestalanguage.update_language_PrestaShop(4, 'Updated Language Name')
>>> print(prestalanguage.get_language_details_PrestaShop(5))
```

#### `get_lang_name_by_index(lang_index: int | str) -> str`

**Назначение**:  Функция извлекает ISO код азыка из магазина `Prestashop`.

**Параметры**:

- `lang_index`: Индекс языка в таблице PrestaShop.

**Возвращает**:

- Имя языка ISO по его индексу в таблице PrestaShop.

**Как работает функция**:

- Функция использует метод `get` родительского класса `PrestaShop` для получения информации о языке по его индексу.
- Она использует параметры `resource_id`, `display` и `io_format` для определения ресурса, формата вывода и режима отображения данных.
- В случае успешного выполнения возвращается ISO код языка.
- В случае возникновения ошибки записывается сообщение в лог и возвращается пустая строка.

**Примеры**:

```python
>>> prestalanguage.get_lang_name_by_index(1)
'en'
>>> prestalanguage.get_lang_name_by_index(2)
'he'
>>> prestalanguage.get_lang_name_by_index(3)
'ru'
```

#### `get_languages_schema() -> Optional[dict]`

**Назначение**: Функция извлекает словарь актуальных языков дла данного магазина.

**Параметры**:

- None

**Возвращает**:

- Language schema or `None` on failure.

**Как работает функция**:

- Функция выполняет запрос к API PrestaShop для получения списка языков.
- Использует метод `_exec` родительского класса `PrestaShop` для выполнения запроса.
- В случае успешного выполнения возвращает словарь с данными о языках.
- В случае возникновения ошибки записывает сообщение в лог и возвращает `None`.

**Примеры**:

```python
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

### `main()`

**Назначение**:  Асинхронная функция, которая выполняет пример использования класса `PrestaLanguage`.

**Параметры**:

- None

**Возвращает**:

- None

**Как работает функция**:

- Создает экземпляр класса `PrestaLanguage`.
- Выполняет асинхронный вызов метода `get_languages_schema` для получения списка языков.
- Выводит полученные данные о языках в консоль.

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

**Пример 1: Получение списка языков**

```python
>>> prestalanguage = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)
>>> languages_schema = prestalanguage.get_languages_schema()
>>> print(languages_schema)
```

**Пример 2: Получение информации о языке по его идентификатору**

```python
>>> prestalanguage = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)
>>> language_details = prestalanguage.get_language_details_PrestaShop(1)
>>> print(language_details)
```

**Пример 3: Добавление нового языка**

```python
>>> prestalanguage = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)
>>> prestalanguage.add_language_PrestaShop('English', 'en')
```

**Пример 4: Обновление информации о языке**

```python
>>> prestalanguage = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)
>>> prestalanguage.update_language_PrestaShop(1, 'Updated Language Name')
```

**Пример 5: Удаление языка**

```python
>>> prestalanguage = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)
>>> prestalanguage.delete_language_PrestaShop(1)