# Модуль для создания клавиатур для бота Telegram
=========================================================

Этот модуль содержит функции для создания различных клавиатур для бота Telegram, 
используемого в цифровом маркете.

## Содержание (TOC)
- ## Функции
   - ### `main_user_kb(user_id: int) -> InlineKeyboardMarkup`
   - ### `catalog_kb(catalog_data: List[Category]) -> InlineKeyboardMarkup`
   - ### `purchases_kb() -> InlineKeyboardMarkup`
   - ### `product_kb(product_id, price, stars_price) -> InlineKeyboardMarkup`
   - ### `get_product_buy_youkassa(price) -> InlineKeyboardMarkup`
   - ### `get_product_buy_robocassa(price: int, payment_link: str) -> InlineKeyboardMarkup`
   - ### `get_product_buy_stars(price) -> InlineKeyboardMarkup`


## Функции

### `main_user_kb(user_id: int) -> InlineKeyboardMarkup`

**Назначение**: 
Создает основную клавиатуру для пользователя.
- Включает кнопки:
  - "👤 Мои покупки" 
  - "🛍 Каталог" 
  - "ℹ️ О магазине" 
  - "🌟 Поддержать автора 🌟" 
- Если пользователь администратор, добавляет кнопку "⚙️ Админ панель".


**Параметры**:
- `user_id (int)`: ID пользователя.


**Возвращает**:
- `InlineKeyboardMarkup`:  Inline клавиатура.


**Примеры**:
```python
>>> main_user_kb(12345)  # Создание клавиатуры для пользователя с ID 12345
InlineKeyboardMarkup(...)
```

### `catalog_kb(catalog_data: List[Category]) -> InlineKeyboardMarkup`

**Назначение**: Создает клавиатуру для каталога товаров. 

**Параметры**:
- `catalog_data (List[Category])`: Список категорий товаров.

**Возвращает**:
- `InlineKeyboardMarkup`: Inline клавиатура.

**Пример**:
```python
>>> catalog_data = [
    Category(id=1, category_name='Одежда'), 
    Category(id=2, category_name='Обувь')
] 
>>> catalog_kb(catalog_data)  
InlineKeyboardMarkup(...)
```

### `purchases_kb() -> InlineKeyboardMarkup`

**Назначение**: Создает клавиатуру для раздела "Мои покупки".

**Возвращает**:
- `InlineKeyboardMarkup`: Inline клавиатура.


**Примеры**:
```python
>>> purchases_kb() 
InlineKeyboardMarkup(...)
```

### `product_kb(product_id, price, stars_price) -> InlineKeyboardMarkup`

**Назначение**: Создает клавиатуру для страницы товара.

**Параметры**:
- `product_id`: ID товара.
- `price`: Цена товара в рублях.
- `stars_price`: Цена товара в звездах.

**Возвращает**:
- `InlineKeyboardMarkup`: Inline клавиатура.


**Примеры**:
```python
>>> product_kb(1, 1000, 500) 
InlineKeyboardMarkup(...)
```

### `get_product_buy_youkassa(price) -> InlineKeyboardMarkup`

**Назначение**: Создает клавиатуру для оплаты через ЮКассу.

**Параметры**:
- `price`: Цена товара.

**Возвращает**:
- `InlineKeyboardMarkup`: Inline клавиатура.


**Примеры**:
```python
>>> get_product_buy_youkassa(1000)
InlineKeyboardMarkup(...)
```

### `get_product_buy_robocassa(price: int, payment_link: str) -> InlineKeyboardMarkup`

**Назначение**: Создает клавиатуру для оплаты через Robocassa.

**Параметры**:
- `price`: Цена товара.
- `payment_link`: Ссылка на страницу оплаты Robocassa.

**Возвращает**:
- `InlineKeyboardMarkup`: Inline клавиатура.


**Примеры**:
```python
>>> get_product_buy_robocassa(1000, 'https://example.com/payment')
InlineKeyboardMarkup(...)
```

### `get_product_buy_stars(price) -> InlineKeyboardMarkup`

**Назначение**: Создает клавиатуру для оплаты звездами.

**Параметры**:
- `price`: Цена товара в звездах.

**Возвращает**:
- `InlineKeyboardMarkup`: Inline клавиатура.


**Примеры**:
```python
>>> get_product_buy_stars(500)
InlineKeyboardMarkup(...)
```