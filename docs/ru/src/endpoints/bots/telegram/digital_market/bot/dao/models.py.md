# Модуль dao.models

## Обзор

Модуль `dao.models` содержит определения моделей базы данных для Telegram-бота цифрового магазина. Он определяет структуру таблиц `users`, `categories`, `products` и `purchases` с использованием SQLAlchemy ORM.

## Подробней

Этот модуль определяет классы, которые представляют таблицы в базе данных и их взаимосвязи. Он использует SQLAlchemy для описания структуры таблиц и управления взаимодействием с базой данных. Каждая модель представляет собой таблицу и содержит поля, соответствующие столбцам таблицы.

## Классы

### `User`

**Описание**: Класс представляет модель пользователя в базе данных.

**Наследует**: `Base` из модуля `bot.dao.database`.

**Атрибуты**:

-   `telegram_id` (int): Уникальный идентификатор пользователя в Telegram.
-   `username` (str | None): Имя пользователя в Telegram (может быть `None`).
-   `first_name` (str | None): Имя пользователя (может быть `None`).
-   `last_name` (str | None): Фамилия пользователя (может быть `None`).
-   `purchases` (List['Purchase']): Список покупок, связанных с пользователем.

**Методы**:

-   `__repr__()`: Возвращает строковое представление объекта `User`.

### `Category`

**Описание**: Класс представляет модель категории товаров в базе данных.

**Наследует**: `Base` из модуля `bot.dao.database`.

**Атрибуты**:

-   `category_name` (str): Название категории.
-   `products` (List['Product']): Список товаров, связанных с категорией.

**Методы**:

-   `__repr__()`: Возвращает строковое представление объекта `Category`.

### `Product`

**Описание**: Класс представляет модель товара в базе данных.

**Наследует**: `Base` из модуля `bot.dao.database`.

**Атрибуты**:

-   `name` (str): Название товара.
-   `description` (str): Описание товара.
-   `price` (int): Цена товара.
-   `file_id` (str | None): Идентификатор файла, связанного с товаром (может быть `None`).
-   `category_id` (int): Идентификатор категории, к которой принадлежит товар.
-   `hidden_content` (str): Скрытое содержимое, связанное с товаром.
-   `category` (Category): Объект категории, к которой принадлежит товар.
-   `purchases` (List['Purchase']): Список покупок, связанных с товаром.

**Методы**:

-   `__repr__()`: Возвращает строковое представление объекта `Product`.

### `Purchase`

**Описание**: Класс представляет модель покупки в базе данных.

**Наследует**: `Base` из модуля `bot.dao.database`.

**Атрибуты**:

-   `user_id` (int): Идентификатор пользователя, совершившего покупку.
-   `product_id` (int): Идентификатор приобретенного товара.
-   `price` (int): Цена товара на момент покупки.
-   `payment_type` (str): Тип платежа.
-   `payment_id` (str): Идентификатор платежа.
-   `user` (User): Объект пользователя, совершившего покупку.
-   `product` (Product): Объект приобретенного товара.

**Методы**:

-   `__repr__()`: Возвращает строковое представление объекта `Purchase`.

## Методы класса

### `User.__repr__`

```python
def __repr__(self):
    return f"<User(id={self.id}, telegram_id={self.telegram_id}, username='{self.username}')>"
```

**Назначение**: Возвращает строковое представление объекта `User`.

**Параметры**:

-   `self`: Ссылка на экземпляр класса `User`.

**Возвращает**:

-   `str`: Строковое представление объекта `User`, содержащее его id, telegram_id и username.

**Как работает функция**:
Функция `__repr__` формирует строку, которая представляет объект `User`. В строке отображаются значения атрибутов `id`, `telegram_id` и `username` экземпляра класса.

**Примеры**:

```python
user = User(telegram_id=123456789, username='testuser')
print(user.__repr__())  # Вывод: <User(id=None, telegram_id=123456789, username='testuser')>
```

### `Category.__repr__`

```python
def __repr__(self):
    return f"<Category(id={self.id}, name='{self.category_name}')>"
```

**Назначение**: Возвращает строковое представление объекта `Category`.

**Параметры**:

-   `self`: Ссылка на экземпляр класса `Category`.

**Возвращает**:

-   `str`: Строковое представление объекта `Category`, содержащее его id и category_name.

**Как работает функция**:
Функция `__repr__` формирует строку, которая представляет объект `Category`. В строке отображаются значения атрибутов `id` и `category_name` экземпляра класса.

**Примеры**:

```python
category = Category(category_name='TestCategory')
print(category.__repr__())  # Вывод: <Category(id=None, name='TestCategory')>
```

### `Product.__repr__`

```python
def __repr__(self):
    return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
```

**Назначение**: Возвращает строковое представление объекта `Product`.

**Параметры**:

-   `self`: Ссылка на экземпляр класса `Product`.

**Возвращает**:

-   `str`: Строковое представление объекта `Product`, содержащее его id, name и price.

**Как работает функция**:
Функция `__repr__` формирует строку, которая представляет объект `Product`. В строке отображаются значения атрибутов `id`, `name` и `price` экземпляра класса.

**Примеры**:

```python
product = Product(name='TestProduct', description='Test Description', price=100)
print(product.__repr__())  # Вывод: <Product(id=None, name='TestProduct', price=100)>
```

### `Purchase.__repr__`

```python
def __repr__(self):
    return f"<Purchase(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, date={self.created_at})>"
```

**Назначение**: Возвращает строковое представление объекта `Purchase`.

**Параметры**:

-   `self`: Ссылка на экземпляр класса `Purchase`.

**Возвращает**:

-   `str`: Строковое представление объекта `Purchase`, содержащее его id, user_id, product_id и created_at.

**Как работает функция**:
Функция `__repr__` формирует строку, которая представляет объект `Purchase`. В строке отображаются значения атрибутов `id`, `user_id`, `product_id` и `created_at` экземпляра класса.

**Примеры**:

```python
purchase = Purchase(user_id=1, product_id=1, price=100, payment_type='card', payment_id='test_payment_id')
print(purchase.__repr__())  # Вывод: <Purchase(id=None, user_id=1, product_id=1, date=None)>