### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
Данный блок кода определяет словарь `scenario`, который содержит информацию о различных товарах (`Apple Wathes`, `Murano Glass`) и их настройках для парсинга и категоризации. Каждый товар имеет атрибуты, такие как URL, состояние (`condition`), правила для категорий PrestaShop (`presta_categories`), флаг чекбокса (`checkbox`) и правило цены (`price_rule`).

Шаги выполнения
-------------------------
1.  **Импорт модуля**: Убедитесь, что модуль `src.scenario._experiments` импортирован в вашем коде.

2.  **Использование словаря `scenario`**: Получите доступ к словарю `scenario`, чтобы получить информацию о конкретном товаре.
3.  **Чтение атрибутов товара**: Извлеките нужные атрибуты товара, такие как URL, состояние или правила для категорий PrestaShop.
4.  **Применение настроек**: Используйте извлеченные атрибуты для настройки парсера, категоризатора или других компонентов вашего приложения.

Пример использования
-------------------------

```python
from src.scenario._experiments import scenario

# Функция извлекает URL для товара "Apple Wathes"
apple_watches_url = scenario["Apple Wathes"]["url"]
print(f"URL для Apple Wathes: {apple_watches_url}")

# Функция извлекает категории PrestaShop для товара "Murano Glass"
murano_glass_categories = scenario["Murano Glass"]["presta_categories"]
print(f"Категории PrestaShop для Murano Glass: {murano_glass_categories}")

# Проверка активности товара "Apple Wathes"
apple_watches_active = scenario["Apple Wathes"]["active"]
if apple_watches_active:
    print("Товар Apple Wathes активен")
else:
    print("Товар Apple Wathes неактивен")
```