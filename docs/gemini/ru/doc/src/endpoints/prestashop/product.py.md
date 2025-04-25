# Модуль для взаимодействия с товарами в PrestaShop

## Обзор

Этот модуль предоставляет логику взаимодействия с товарами в PrestaShop. 

Он определяет класс `PrestaProduct`, который наследует класс `PrestaShop` и обеспечивает следующие функциональные возможности:

- Получение схемы (структуры) товара с PrestaShop API.
- Поиск родительских категорий для заданной категории.
- Добавление нового товара в PrestaShop.
- Получение данных товара по его ID.
- Методы для работы с изображениями товаров.

## Классы

### `class PrestaProduct`

**Описание**: Класс для работы с товарами в PrestaShop API.
**Наследует**: `PrestaShop`
**Атрибуты**:
- `api_key` (Optional[str]): Ключ API для доступа к PrestaShop. По умолчанию используется значение из `Config.API_KEY`.
- `api_domain` (Optional[str]): Домен API для доступа к PrestaShop. По умолчанию используется значение из `Config.API_DOMAIN`.
**Методы**:
- `get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict:`: Получает схему (структуру) товара из PrestaShop API.
- `get_parent_category(self, id_category: int) -> Optional[int]:`: Получает родительскую категорию для заданной категории.
- `_add_parent_categories(self, f: ProductFields) -> None:`: Вычисляет и добавляет все уникальные родительские категории для списка ID категорий.
- `get_product(self, id_product: int, **kwargs) -> dict:`: Возвращает словарь полей товара из Prestashop по его ID.
- `add_new_product(self, f: ProductFields) -> dict:`: Добавляет новый товар в PrestaShop.
- `create_binary(self, resource: str, file_path: str, file_name: str) -> dict:`: Загружает изображение товара по пути к файлу.
- `upload_image_from_url(self, resource: str, id_product: int, image_url: str) -> dict:`: Загружает изображение товара по URL-адресу.


### `class Config`

**Описание**: Класс для конфигурации настроек PrestaShop.
**Атрибуты**:
- `MODE` (str): Режим работы. Может быть `dev`, `dev8` или `prod`.
- `API_DOMAIN` (str): Домен API для доступа к PrestaShop. 
- `API_KEY` (str): Ключ API для доступа к PrestaShop.

## Функции

### `example_add_new_product() -> None:`

**Назначение**: Пример добавления нового товара в PrestaShop.

**Параметры**: Нет

**Возвращает**: Нет

**Как работает**:

- Создает экземпляр класса `PrestaProduct`.
- Загружает пример данных товара из JSON-файла.
- Преобразует данные в XML-формат.
- Отправляет запрос на создание товара в PrestaShop API.
- Выводит результат в консоль.


### `example_get_product(id_product: int, **kwargs) -> None:`

**Назначение**: Пример получения товара из PrestaShop по его ID.

**Параметры**:
- `id_product` (int): ID товара в PrestaShop.

**Возвращает**: Нет

**Как работает**:
- Создает экземпляр класса `PrestaProduct`.
- Выполняет запрос на получение товара по ID.
- Выводит результат в консоль.

## Примеры

```python
# Пример добавления нового товара
example_add_new_product()

# Пример получения товара по ID
example_get_product(id_product=2191)
```