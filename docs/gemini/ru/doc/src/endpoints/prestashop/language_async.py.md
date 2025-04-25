# Модуль `prestashop/language_async.py`

## Обзор

Этот модуль предоставляет асинхронный класс `PrestaLanguageAync`, который взаимодействует с API PrestaShop для управления настройками языков в магазине. 

## Классы

### `PrestaLanguageAync`

**Описание**: Класс, отвечающий за асинхронные операции с настройками языков в магазине PrestaShop. 
**Наследует**: `PrestaShopAsync`
**Атрибуты**:
    - `API_DOMAIN` (str): Домен API PrestaShop.
    - `API_KEY` (str): Ключ API PrestaShop.
    - `lang_string` (str): ISO-код языка.

**Методы**:

#### `__init__(self, *args, **kwargs)`

**Назначение**: Конструктор класса `PrestaLanguageAync`. 

**Параметры**:

- `*args`: Дополнительные позиционные аргументы.
- `**kwargs`: Дополнительные именованные аргументы.

**Как работает функция**:

Инициализирует объект класса `PrestaLanguageAync`, наследуя свойства от класса `PrestaShopAsync`. 
 
#### `get_lang_name_by_index(self, lang_index: int | str) -> str`

**Назначение**: Возвращает имя языка ISO по его индексу в таблице PrestaShop.

**Параметры**:

- `lang_index` (int | str): Индекс языка в таблице PrestaShop.

**Возвращает**:

- `str`: Имя языка ISO, например "en", "ru", "he". 

**Вызывает исключения**:

- `Exception`: В случае ошибки получения языка по индексу.

**Как работает функция**:

- Использует метод `super().get()` для получения данных о языке из API PrestaShop. 
- Выполняет обработку исключений. 

#### `get_languages_schema(self) -> dict`

**Назначение**: Возвращает схему языков магазина PrestaShop в виде словаря.

**Параметры**:

- Нет параметров.

**Возвращает**:

- `dict`: Словарь с информацией о языках магазина.

**Как работает функция**:

- Использует метод `super().get_languages_schema()` для получения схемы языков. 
- Выводит полученные данные с помощью функции `print`. 

## Функции

### `main()`

**Назначение**: Асинхронная функция, демонстрирующая использование класса `PrestaLanguageAync`.

**Параметры**:

- Нет параметров.

**Как работает функция**:

- Создает экземпляр класса `PrestaLanguageAync`.
- Вызывает метод `get_languages_schema()` для получения схемы языков. 
- Выводит полученные данные с помощью функции `print`. 

**Примеры**:

```python
async def main():
    """"""
    lang_class = PrestaLanguageAync()
    languagas_schema = await  lang_class.get_languages_schema()
    print(languagas_schema)