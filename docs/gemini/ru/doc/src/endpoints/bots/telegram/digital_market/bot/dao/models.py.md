# Модуль `models`

## Обзор

Модуль `models` содержит классы, которые используются для представления данных о пользователе, товарах, категориях и покупках в базе данных.

## Детали

Модуль импортирует необходимые библиотеки:
```python
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Text, ForeignKey, text
from bot.dao.database import Base
```
 
## Классы

### `User`
**Описание**:  Класс `User` представляет пользователя в базе данных.

**Атрибуты**:
 - `telegram_id` (int): Телеграмм ID пользователя.
 - `username` (str | None): Username пользователя в Телеграмм.
 - `first_name` (str | None): Имя пользователя.
 - `last_name` (str | None): Фамилия пользователя.
 - `purchases` (List['Purchase']): Список покупок, совершенных пользователем.

**Методы**:
 - `__repr__()`: Возвращает строковое представление объекта `User`.

```python
class User(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    purchases: Mapped[List['Purchase']] = relationship(
        "Purchase",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username=\'{self.username}\')>"
```

### `Category`
**Описание**:  Класс `Category` представляет категорию товара в базе данных.

**Атрибуты**:
 - `category_name` (str): Название категории.
 - `products` (List["Product"]): Список товаров, принадлежащих к данной категории.

**Методы**:
 - `__repr__()`: Возвращает строковое представление объекта `Category`.

```python
class Category(Base):
    __tablename__ = 'categories'

    category_name: Mapped[str] = mapped_column(Text, nullable=False)
    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category(id={self.id}, name=\'{self.category_name}\')>"
```

### `Product`
**Описание**:  Класс `Product` представляет товар в базе данных.

**Атрибуты**:
 - `name` (str): Название товара.
 - `description` (str): Описание товара.
 - `price` (int): Цена товара.
 - `file_id` (str | None): ID файла, содержащего изображение товара в Телеграмм.
 - `category_id` (int): ID категории, к которой принадлежит товар.
 - `hidden_content` (str):  
 - `category` (Category): Объект `Category`, представляющий категорию товара.
 - `purchases` (List['Purchase']): Список покупок данного товара.

**Методы**:
 - `__repr__()`: Возвращает строковое представление объекта `Product`.

```python
class Product(Base):
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int]
    file_id: Mapped[str | None] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    hidden_content: Mapped[str] = mapped_column(Text)
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    purchases: Mapped[List['Purchase']] = relationship(
        "Purchase",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name=\'{self.name}\', price={self.price})>"
```

### `Purchase`
**Описание**:  Класс `Purchase` представляет покупку в базе данных.

**Атрибуты**:
 - `user_id` (int): ID пользователя, совершившего покупку.
 - `product_id` (int): ID товара, который был куплен.
 - `price` (int): Цена покупки.
 - `payment_type` (str): Способ оплаты.
 - `payment_id` (str): Уникальный ID платежа.
 - `user` (User): Объект `User`, представляющий пользователя, совершившего покупку.
 - `product` (Product): Объект `Product`, представляющий товар, который был куплен.

**Методы**:
 - `__repr__()`: Возвращает строковое представление объекта `Purchase`.

```python
class Purchase(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    price: Mapped[int]
    payment_type: Mapped[str]
    payment_id: Mapped[str] = mapped_column(unique=True)
    user: Mapped["User"] = relationship("User", back_populates="purchases")
    product: Mapped["Product"] = relationship("Product", back_populates="purchases")

    def __repr__(self):
        return f"<Purchase(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, date={self.created_at})>"
```

## Примеры

```python
# Импорт необходимых моделей
from bot.dao.models import User, Product, Category, Purchase

# Создание пользователя
user = User(telegram_id=123456789, username='@username', first_name='Имя', last_name='Фамилия')

# Создание категории
category = Category(category_name='Категория')

# Создание товара
product = Product(name='Название товара', description='Описание товара', price=1000, category=category)

# Создание покупки
purchase = Purchase(user=user, product=product, price=1000, payment_type='Card', payment_id='1234567890')
```