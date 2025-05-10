## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код демонстрирует структуру JSON, которую можно использовать для создания нового товара в Prestashop через API. JSON содержит все необходимые поля для создания товара, включая его название, описание, цену, артикул, изображения, категории и т.д.

Шаги выполнения
-------------------------
1. **Заполните поля JSON:**  
   - Подставьте реальные значения в поля JSON.  
   - Обратите внимание на обязательные поля и их типы данных (числа, строки, булевы значения).
   - Все ID (категорий, изображений, налоговых групп, производителей, поставщиков) должны существовать в вашей Prestashop.  
2. **Отправьте JSON через API:** 
   - Используйте библиотеку запросов (например, `requests` в Python) для отправки JSON на API Prestashop.
   - Установите правильные заголовки для запроса (Content-Type, Authorization).
   - Обработайте ответ API для проверки результата.

Пример использования
-------------------------

```python
import requests
import json

API_URL = "http://your-prestashop-domain/api/products" # Замените
API_KEY = "YOUR_API_KEY" # Замените

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {API_KEY}"
}

data = {
  "product": {
    "id_default_combination": None,
    "id_tax_rules_group": "1",
    "reference": "REF-001",
    "quantity": "100",
    "price": "10.000000",
    "state": "1",
    "available_for_order": "1",
    "show_price": "1",
    "visibility": "both",
    "id_category_default": "2",
    "name": [
      {
        "language": {
          "id": "1"
        },
        "value": "Новый товар"
      }
    ],
    "description_short": [
      {
        "language": {
          "id": "1"
        },
        "value": "<p>Краткое описание нового товара.</p>"
      }
    ],
    "link_rewrite": [
      {
        "language": {
          "id": "1"
        },
        "value": "novyj-produkt"
      }
    ]
  }
}

try:
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    response.raise_for_status() # Проверяем статус ответа
    print("товар успешно создан.")
except requests.exceptions.RequestException as e:
    print(f"Ошибка при создании товара: {e}")