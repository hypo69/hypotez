### **Анализ кода модуля `models.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/dao/models.py

Модуль содержит определения моделей базы данных для Telegram-бота цифрового рынка.
Модели включают: User, Category, Product, Purchase.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код использует SQLAlchemy для определения моделей базы данных, что обеспечивает удобное взаимодействие с базой данных.
  - Присутствуют `__repr__` методы для каждой модели, что упрощает отладку и логирование.
  - Используются аннотации типов для переменных.
- **Минусы**:
  - Отсутствуют docstring для классов и их полей.
  - В аннотациях используется `List[]` вместо `list[]`

**Рекомендации по улучшению:**

- Добавить docstring для каждого класса и его полей, чтобы улучшить понимание структуры базы данных.
- Изменить `List[]` на `list[]`.
- Добавить комментарии к наиболее важным частям кода.

**Оптимизированный код:**

```python
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Text, ForeignKey
from bot.dao.database import Base


class User(Base):
    """
    Модель пользователя Telegram-бота.

    Attributes:
        telegram_id (int): Уникальный идентификатор пользователя в Telegram.
        username (str | None): Имя пользователя в Telegram (может отсутствовать).
        first_name (str | None): Имя пользователя.
        last_name (str | None): Фамилия пользователя.
        purchases (list['Purchase']): Список покупок, связанных с пользователем.
    """
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    purchases: Mapped[list['Purchase']] = relationship( #  Устанавливаем связь "один ко многим" с таблицей покупок
        "Purchase",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта User.
        """
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username='{self.username}')>"


class Category(Base):
    """
    Модель категории продукта.

    Attributes:
        category_name (str): Название категории.
        products (list["Product"]): Список продуктов, связанных с категорией.
    """
    __tablename__ = 'categories'

    category_name: Mapped[str] = mapped_column(Text, nullable=False)
    products: Mapped[list["Product"]] = relationship( # Устанавливаем связь "один ко многим" с таблицей продуктов
        "Product",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта Category.
        """
        return f"<Category(id={self.id}, name='{self.category_name}')>"


class Product(Base):
    """
    Модель продукта.

    Attributes:
        name (str): Название продукта.
        description (str): Описание продукта.
        price (int): Цена продукта.
        file_id (str | None): Идентификатор файла, связанного с продуктом (может отсутствовать).
        category_id (int): Идентификатор категории, к которой принадлежит продукт.
        hidden_content (str): Скрытое содержимое продукта.
        category (Category): Категория, к которой принадлежит продукт.
        purchases (list['Purchase']): Список покупок, связанных с продуктом.
    """
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int]
    file_id: Mapped[str | None] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    hidden_content: Mapped[str] = mapped_column(Text)
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    purchases: Mapped[list['Purchase']] = relationship( # Устанавливаем связь "один ко многим" с таблицей покупок
        "Purchase",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта Product.
        """
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"


class Purchase(Base):
    """
    Модель покупки.

    Attributes:
        user_id (int): Идентификатор пользователя, совершившего покупку.
        product_id (int): Идентификатор купленного продукта.
        price (int): Цена покупки.
        payment_type (str): Тип платежа.
        payment_id (str): Идентификатор платежа (уникальный).
        user (User): Пользователь, совершивший покупку.
        product (Product): Купленный продукт.
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
        """
        return f"<Purchase(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, date={self.created_at})>"