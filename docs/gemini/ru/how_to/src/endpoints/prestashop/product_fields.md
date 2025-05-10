### Как использовать этот блок кода

Описание
-------------------------
Этот блок кода представляет собой пример JSON-структуры для создания или обновления товара в Prestashop через API. Он содержит подробную информацию о полях товара, включая общие атрибуты, ассоциации с категориями и изображениями, а также многоязычные поля для названия, описания и мета-данных.

Шаги выполнения
-------------------------
1.  **Подготовка данных:** Сформируйте JSON-объект, соответствующий структуре, представленной в коде. Убедитесь, что все необходимые поля заполнены корректными значениями. Особое внимание уделите ID существующих категорий, изображений и налоговых групп.
2.  **Настройка API-запроса:**  Подготовьте HTTP-запрос (например, POST или PUT) к API Prestashop. Укажите URL API endpoint для работы с товарами.
3.  **Добавление заголовков:**  Добавьте необходимые заголовки в запрос, включая `Content-Type: application/json` для указания формата данных и заголовок `Authorization` с вашим API-ключом.
4.  **Отправка запроса:** Отправьте сформированный JSON-объект в теле запроса к API Prestashop.
5.  **Обработка ответа:**  Проанализируйте ответ от API.  В случае успеха вы получите подтверждение создания или обновления товара. В случае ошибки API вернет подробное сообщение об ошибке, которое поможет вам исправить проблему в данных.

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
    response.raise_for_status()  # Проверка на HTTP ошибки
    print("Товар успешно создан/обновлен")
    print(response.json()) # Вывод ответа API
except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе к API: {e}")
    if response is not None:
        print(response.text) # Вывод текста ошибки от API
```