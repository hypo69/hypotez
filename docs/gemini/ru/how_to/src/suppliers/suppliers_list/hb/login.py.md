### **Инструкция по использованию блока кода**

=========================================================================================

Описание
-------------------------
Этот блок кода содержит функцию `login`, которая предназначена для выполнения авторизации поставщика. В текущей реализации функция всегда возвращает `True`, что может быть заглушкой или упрощенной версией для демонстрационных целей.

Шаги выполнения
-------------------------
1. Импортируется модуль `logger` из `src.logger.logger` для логирования событий.
2. Определяется функция `login`, которая принимает объект `s` типа `Supplier` в качестве аргумента.
3. Функция `login` возвращает булево значение `True`, что означает успешную авторизацию. В реальной системе здесь должна быть логика для проверки учетных данных и авторизации пользователя.

Пример использования
-------------------------

```python
from src.suppliers.suppliers import Supplier
from src.suppliers.suppliers_list.hb.login import login
from src.logger.logger import logger

def main():
    # Пример создания объекта Supplier (замените на реальные данные)
    supplier = Supplier(
        name="HBS",
        address="https://www.hb.com",
        login_url="https://www.hb.com/login",
        email="test@hb.com",
        password="password",
        account_number="1234567890",
        api_key="abcdef123456",
        phone_number="+1234567890",
        company_name="HB Company"
    )

    # Вызов функции login для авторизации поставщика
    if login(supplier):
        logger.info(f"Поставщик {supplier.name} успешно авторизован.")
    else:
        logger.error(f"Не удалось авторизовать поставщика {supplier.name}.")

if __name__ == "__main__":
    main()
```