### **Анализ кода модуля `models.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/dao/models.py

Модуль содержит определения моделей базы данных для Telegram-бота цифрового рынка.
Модели включают: User, Category, Product и Purchase.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и организован.
  - Используются аннотации типов.
  - Присутствуют `__repr__` методы для удобного представления объектов.
  - Используются cascade для автоматического удаления связанных записей.
- **Минусы**:
  - Отсутствует документация для классов и их атрибутов.
  - Не все типы переменных указаны с использованием `|` вместо `Union[]`

**Рекомендации по улучшению**:
1.  Добавить docstring к каждому классу и методу, описывающие их назначение, аргументы и возвращаемые значения.
2.  Использовать `|` вместо `Union[]` для аннотаций типов.
3.  Добавить комментарии к наиболее сложным участкам кода.
4.  Устранить дублирование информации, например, в классе `Purchase` поле `price` дублирует цену продукта.
5.  Добавить обработку исключений и логирование.

**Оптимизированный код**:

```python
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Text, ForeignKey
from bot.dao.database import Base
from src.logger import logger


class User(Base):
    """
    Модель пользователя Telegram-бота.

    Args:
        telegram_id (int): Уникальный идентификатор пользователя в Telegram.
        username (str | None): Имя пользователя в Telegram (может отсутствовать).
        first_name (str | None): Имя пользователя.
        last_name (str | None): Фамилия пользователя.
        purchases (List['Purchase']): Список покупок пользователя.
    """
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    purchases: Mapped[List['Purchase']] = relationship(
        "Purchase",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта User.

        Returns:
            str: Строковое представление объекта User.
        """
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username='{self.username}')>"


class Category(Base):
    """
    Модель категории товаров.

    Args:
        category_name (str): Название категории.
        products (List["Product"]): Список товаров в категории.
    """
    __tablename__ = 'categories'

    category_name: Mapped[str] = mapped_column(Text, nullable=False)
    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта Category.

        Returns:
            str: Строковое представление объекта Category.
        """
        return f"<Category(id={self.id}, name='{self.category_name}')>"


class Product(Base):
    """
    Модель товара.

    Args:
        name (str): Название товара.
        description (str): Описание товара.
        price (int): Цена товара.
        file_id (str | None): Идентификатор файла (может отсутствовать).
        category_id (int): Идентификатор категории товара.
        hidden_content (str): Скрытое содержимое товара.
        category (Category): Категория товара.
        purchases (List['Purchase']): Список покупок, связанных с товаром.
    """
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

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта Product.

        Returns:
            str: Строковое представление объекта Product.
        """
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"


class Purchase(Base):
    """
    Модель покупки.

    Args:
        user_id (int): Идентификатор пользователя, совершившего покупку.
        product_id (int): Идентификатор купленного товара.
        price (int): Цена товара на момент покупки.
        payment_type (str): Тип платежа.
        payment_id (str): Уникальный идентификатор платежа.
        user (User): Пользователь, совершивший покупку.
        product (Product): Купленный товар.
    """
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    price: Mapped[int]
    payment_type: Mapped[str]
    payment_id: Mapped[str] = mapped_column(unique=True)
    user: Mapped["User"] = relationship("User", back_populates="purchases")
    product: Mapped["Product"] = relationship("Product", back_populates="purchases")

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта Purchase.

        Returns:
            str: Строковое представление объекта Purchase.
        """
        return f"<Purchase(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, date={self.created_at})>"