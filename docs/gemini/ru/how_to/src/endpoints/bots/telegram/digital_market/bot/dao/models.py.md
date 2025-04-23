### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет модели базы данных, используемые для хранения информации о пользователях, категориях, товарах и покупках в контексте Telegram-бота для цифрового рынка. Он использует SQLAlchemy для определения структуры таблиц базы данных и связей между ними.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются классы и типы из `typing`, `sqlalchemy.orm` и `sqlalchemy`.
   - Импортируется базовый класс `Base` из модуля `bot.dao.database`.

2. **Определение класса `User`**:
   - Класс `User` представляет таблицу пользователей в базе данных.
   - `telegram_id`: Уникальный идентификатор пользователя в Telegram (BigInteger, не может быть `NULL`).
   - `username`: Имя пользователя (может быть `NULL`).
   - `first_name`: Имя пользователя (может быть `NULL`).
   - `last_name`: Фамилия пользователя (может быть `NULL`).
   - `purchases`: Список покупок, связанных с пользователем (связь "один ко многим" с классом `Purchase`).

3. **Определение класса `Category`**:
   - Класс `Category` представляет таблицу категорий товаров.
   - `category_name`: Название категории (Text, не может быть `NULL`).
   - `products`: Список товаров, связанных с категорией (связь "один ко многим" с классом `Product`).

4. **Определение класса `Product`**:
   - Класс `Product` представляет таблицу товаров.
   - `name`: Название товара (Text).
   - `description`: Описание товара (Text).
   - `price`: Цена товара (Integer).
   - `file_id`: Идентификатор файла, связанного с товаром (может быть `NULL`).
   - `category_id`: Идентификатор категории, к которой принадлежит товар (внешний ключ к таблице `categories`).
   - `hidden_content`: Скрытое содержимое (Text).
   - `category`: Категория, к которой принадлежит товар (связь "один ко многим" с классом `Category`).
   - `purchases`: Список покупок, связанных с товаром (связь "один ко многим" с классом `Purchase`).

5. **Определение класса `Purchase`**:
   - Класс `Purchase` представляет таблицу покупок.
   - `user_id`: Идентификатор пользователя, совершившего покупку (внешний ключ к таблице `users`).
   - `product_id`: Идентификатор товара, который был куплен (внешний ключ к таблице `products`).
   - `price`: Цена товара на момент покупки (Integer).
   - `payment_type`: Тип оплаты (String).
   - `payment_id`: Уникальный идентификатор платежа (String, unique).
   - `user`: Пользователь, совершивший покупку (связь "один ко многим" с классом `User`).
   - `product`: Товар, который был куплен (связь "один ко многим" с классом `Product`).

Пример использования
-------------------------

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Создание движка SQLAlchemy для подключения к базе данных
engine = create_engine('sqlite:///:memory:')  # Используем SQLite в памяти для примера

# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Создание пользователя
new_user = User(telegram_id=123456789, username='test_user', first_name='Test', last_name='User')
session.add(new_user)
session.commit()

# Создание категории
new_category = Category(category_name='Electronics')
session.add(new_category)
session.commit()

# Создание товара
new_product = Product(name='Smartphone', description='A high-end smartphone', price=999, category_id=new_category.id, hidden_content='secret')
session.add(new_product)
session.commit()

# Создание покупки
new_purchase = Purchase(user_id=new_user.id, product_id=new_product.id, price=999, payment_type='Credit Card', payment_id='12345')
session.add(new_purchase)
session.commit()

# Вывод информации о покупке
print(new_purchase)

# Закрытие сессии
session.close()