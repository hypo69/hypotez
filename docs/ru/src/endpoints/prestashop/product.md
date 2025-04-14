# Документация для разработчика: `product.md`

## Обзор

Этот документ предоставляет подробное описание структуры JSON для создания и обновления продуктов в PrestaShop через API. Он содержит информацию о каждом поле, его назначении и требованиях к формату данных. Также включены примеры использования на Python для упрощения интеграции.

## Подробнее

Этот файл содержит JSON-структуру, описывающую формат данных для создания или обновления продукта в PrestaShop через API. Он определяет обязательные и необязательные поля, их типы и допустимые значения, а также предоставляет примеры на Python для работы с API PrestaShop. Данный код является частью модуля `prestashop` и используется для взаимодействия с API PrestaShop для управления продуктами.

## Структура JSON для продукта PrestaShop

```json
{
  "product": {
    "id_default_combination": null,
    "id_tax_rules_group": "1",
    "id_manufacturer": "0",
    "id_supplier": "0",
    "reference": "REF-001",
    "ean13": "1234567890123",
    "upc": "987654321098",
    "ecotax": "0.000000",
    "quantity": "100",
    "minimal_quantity": "1",
    "price": "10.000000",
    "wholesale_price": "5.000000",
    "on_sale": "0",
    "online_only": "0",
    "unity": null,
    "unit_price": "0.000000",
    "reduction_price": "0.000000",
    "reduction_percent": "0.000000",
    "reduction_from": "0000-00-00",
    "reduction_to": "0000-00-00",
    "cache_is_pack": "0",
    "cache_has_attachments": "0",
    "cache_default_attribute": "0",
    "advanced_stock_management": "0",
    "pack_stock_type": "3",
    "state": "1",
    "available_for_order": "1",
    "show_price": "1",
    "visibility": "both",
    "id_category_default": "2",
    "associations": {
      "categories": [
        {
          "id": "2"
        }
      ],
      "images": [
        {
          "id": "1"
        }
      ]
    },
    "name": [
      {
        "language": {
          "id": "1"
        },
        "value": "Новый продукт"
      }
    ],
    "description": [
      {
        "language": {
          "id": "1"
        },
        "value": "<p>Описание нового продукта.</p>"
      }
    ],
    "description_short": [
      {
        "language": {
          "id": "1"
        },
        "value": "<p>Краткое описание нового продукта.</p>"
      }
    ],
    "meta_title": [
      {
        "language": {
          "id": "1"
        },
        "value": "Мета заголовок продукта"
      }
    ],
    "meta_description": [
      {
        "language": {
          "id": "1"
        },
        "value": "Мета описание продукта"
      }
    ],
    "meta_keywords": [
      {
        "language": {
          "id": "1"
        },
        "value": "ключевые слова, продукта"
      }
    ],
    "link_rewrite": [
      {
        "language": {
          "id": "1"
        },
        "value": "novyj-produkt"
      }
    ],
    "available_now": [
      {
        "language": {
          "id": "1"
        },
        "value": "В наличии"
      }
    ],
    "available_later": [
      {
        "language": {
          "id": "1"
        },
        "value": "Скоро в продаже"
      }
    ]
  }
}
```

### Разъяснения по полям:

*   **`product`:** Корневой элемент, содержащий все данные продукта.

*   **Общие поля:**

    *   `id_default_combination`: ID комбинации по умолчанию (если есть комбинации). `null`, если нет комбинаций.
    *   `id_tax_rules_group`: ID группы налогов. Важно! Должно существовать в Prestashop.
    *   `id_manufacturer`: ID производителя.
    *   `id_supplier`: ID поставщика.
    *   `reference`: Артикул.
    *   `ean13`: EAN-13 штрихкод.
    *   `upc`: UPC штрихкод.
    *   `ecotax`: Экологический налог.
    *   `quantity`: Количество на складе.
    *   `minimal_quantity`: Минимальное количество для заказа.
    *   `price`: Цена (без налога). Обратите внимание на формат (дробное число).
    *   `wholesale_price`: Оптовая цена.
    *   `on_sale`: Показывать значок "Распродажа" (0 или 1).
    *   `online_only`: Доступен только онлайн (0 или 1).
    *   `unity`: Единица измерения (например, "шт").
    *   `unit_price`: Цена за единицу измерения.
    *   `reduction_price`: Скидка в валюте.
    *   `reduction_percent`: Скидка в процентах.
    *   `reduction_from`: Дата начала скидки.
    *   `reduction_to`: Дата окончания скидки.
    *   `cache_is_pack`: Является ли товар комплектом (0 или 1).
    *   `cache_has_attachments`: Есть ли прикрепленные файлы (0 или 1).
    *   `cache_default_attribute`: ID атрибута по умолчанию (для комбинаций).
    *   `advanced_stock_management`: Использовать ли расширенное управление складом (0 или 1).
    *   `pack_stock_type`: Тип управления складом для комплектов (1-3).
    *   `state`: Активен (0 или 1).
    *   `available_for_order`: Доступен для заказа (0 или 1).
    *   `show_price`: Показывать цену (0 или 1).
    *   `visibility`: Видимость (`both`, `catalog`, `search`, `none`).
    *   `id_category_default`: ID категории по умолчанию. Важно! Должна существовать в Prestashop.

*   **`associations`:** Ассоциации с другими сущностями.

    *   `categories`: Массив категорий, к которым принадлежит продукт. `id` категорий должны существовать.
    *   `images`: Массив ID изображений, связанных с продуктом. `id` изображений должны существовать (обычно сначала загружаются изображения, а потом привязываются к продукту).

*   **Многоязычные поля:**

    *   `name`: Название продукта (для каждого языка).
    *   `description`: Полное описание продукта (для каждого языка).
    *   `description_short`: Краткое описание продукта (для каждого языка).
    *   `meta_title`: Мета-заголовок (для каждого языка).
    *   `meta_description`: Мета-описание (для каждого языка).
    *   `meta_keywords`: Мета-ключевые слова (для каждого языка).
    *   `link_rewrite`: URL-адрес (для каждого языка). Генерируется автоматически на основе названия, но можно указать вручную. Важно, чтобы был уникальным.
    *   `available_now`: Текст, отображаемый, когда товар в наличии.
    *   `available_later`: Текст, отображаемый, когда товара нет в наличии.

### Важные моменты:

*   **`id` значений:** Все ID (категорий, изображений, налоговых групп, производителей, поставщиков) должны существовать в вашей Prestashop. Сначала нужно создать эти сущности через API или вручную через административную панель.
*   **Языки:** Необходимо указать значения для каждого языка, поддерживаемого вашим магазином. В примере только один язык (id=1).
*   **Формат данных:** Строго соблюдайте формат данных (числа, строки, булевы значения).
*   **Кодировка:** Используйте кодировку UTF-8 для JSON.
*   **Ошибки:** API Prestashop возвращает подробные сообщения об ошибках. Внимательно их читайте и исправляйте проблемы в вашем JSON.
*   **Версия Prestashop:** API может немного отличаться в разных версиях Prestashop. Проверяйте документацию для вашей версии.
*   **Комбинации:** Если вы работаете с комбинациями, вам понадобится гораздо более сложный JSON. Посмотрите примеры в документации Prestashop API для работы с комбинациями.

## Примеры

### Пример использования (Python):

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
        "value": "Новый продукт"
      }
    ],
    "description_short": [
      {
        "language": {
          "id": "1"
        },
        "value": "<p>Краткое описание нового продукта.</p>"
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
    response.raise_for_status()  # Raises HTTPError for bad responses (4XX, 5XX)
    print("Product created successfully!")
    print(response.json())  # Prints the JSON response from the API (e.g., the ID of the created product)

except requests.exceptions.RequestException as ex:
    print(f"Error creating product: {ex}")
    if response is not None:
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
```

**Пояснения:**

1.  **Импорт библиотек**: Импортируются библиотеки `requests` для выполнения HTTP-запросов и `json` для работы с JSON-данными.
2.  **Определение констант**:
    *   `API_URL`: URL-адрес API PrestaShop для создания продуктов. Необходимо заменить на актуальный URL вашего магазина.
    *   `API_KEY`: Ключ API для аутентификации. Необходимо заменить на ваш ключ API PrestaShop.
3.  **Формирование заголовков**: Определяются заголовки HTTP-запроса, включающие тип контента (`application/json`) и ключ API для аутентификации. Ключ API передается в формате Basic Authentication.
4.  **Определение данных**: `data` содержит структуру JSON с данными продукта, которые будут отправлены в API. В примере заполнены основные поля:
    *   `id_tax_rules_group`: ID группы налогов.
    *   `reference`: Артикул продукта.
    *   `quantity`: Количество на складе.
    *   `price`: Цена продукта.
    *   `state`: Состояние продукта (активен или нет).
    *   `available_for_order`: Доступен ли продукт для заказа.
    *   `show_price`: Показывать ли цену продукта.
    *   `visibility`: Видимость продукта (например, "both" - виден везде).
    *   `id_category_default`: ID категории по умолчанию.
    *   `name`: Название продукта на разных языках.
    *   `description_short`: Краткое описание продукта на разных языках.
    *   `link_rewrite`: URL-адрес продукта на разных языках.
5.  **Отправка запроса**:
    *   Блок `try...except` используется для обработки возможных ошибок при отправке запроса.
    *   `requests.post(API_URL, headers=headers, data=json.dumps(data))`: Отправляет POST-запрос к API PrestaShop с данными продукта в формате JSON. `json.dumps(data)` преобразует структуру `data` в JSON-строку.
    *   `response.raise_for_status()`: Проверяет статус код ответа. Если код находится в диапазоне 4xx или 5xx, вызывается исключение `HTTPError`.
    *   `print("Product created successfully!")`: Выводит сообщение об успешном создании продукта.
    *   `print(response.json())`: Выводит JSON-ответ от API, который может содержать ID созданного продукта и другие данные.
6.  **Обработка ошибок**:
    *   `except requests.exceptions.RequestException as ex`: Перехватывает исключения, связанные с ошибками при отправке запроса (например, проблемы с соединением, неверный URL и т.д.).
    *   `print(f"Error creating product: {ex}")`: Выводит сообщение об ошибке.
    *   `print(f"Response status code: {response.status_code}")`: Выводит код статуса ответа (например, 400, 401, 500).
    *   `print(f"Response content: {response.text}")`: Выводит содержимое ответа, которое может содержать более подробную информацию об ошибке.