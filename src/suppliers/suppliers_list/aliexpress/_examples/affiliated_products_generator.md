
файл примеров для модуля `affiliated_products_generator.py`. Этот файл показывает, как использовать класс `AliAffiliatedProducts` для сбора данных о товарах и обработки аффилированных ссылок.

### Пример использования `AliAffiliatedProducts`

```python
# пример_использования.py

from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts

def main():
    # Задайте параметры рекламной кампании
    campaign_name = "summer_sale_2024"
    campaign_category = "electronics"  # Можно задать None, если категория не нужна
    language = "EN"  # Язык для кампании
    currency = "USD"  # Валюта для кампании

    # Создайте экземпляр класса AliAffiliatedProducts
    parser = AliAffiliatedProducts(
        campaign_name,
        campaign_category,
        language,
        currency
    )

    # Пример URL товаров или их ID
    prod_urls = [
        '123',
        'https://www.aliexpress.com/item/123.html',
        '456',
        'https://www.aliexpress.com/item/456.html',
    ]

    # Обработайте товары и получите список товаров с аффилированными ссылками
    products = parser.process_affiliate_products(prod_urls)

    # Проверьте результаты
    if products:
        print(f"Получено {len(products)} аффилированных товаров.")
        for product in products:
            print(f"товар ID: {product.product_id}")
            print(f"Аффилированная ссылка: {product.promotion_link}")
            print(f"Локальный путь к изображению: {product.local_image_path}")
            if product.local_video_path:
                print(f"Локальный путь к видео: {product.local_video_path}")
            print()
    else:
        print("Не удалось получить аффилированные товары.")

if __name__ == "__main__":
    main()
```

### Объяснение примера

- **Создание экземпляра `AliAffiliatedProducts`**:
  ```python
  parser = AliAffiliatedProducts(
      campaign_name,
      campaign_category,
      language,
      currency
  )
  ```
  Здесь мы создаем объект класса `AliAffiliatedProducts`, передавая параметры рекламной кампании.

- **Список URL товаров или их ID**:
  ```python
  prod_urls = [
      '123',
      'https://www.aliexpress.com/item/123.html',
      '456',
      'https://www.aliexpress.com/item/456.html',
  ]
  ```
  Пример списка товаров. Можно указать как просто ID, так и полные URL.

- **Обработка товаров**:
  ```python
  products = parser.process_affiliate_products(prod_urls)
  ```
  Мы вызываем метод `process_affiliate_products`, который обрабатывает товары, получает аффилированные ссылки и сохраняет изображения и видео.

- **Проверка результатов**:
  ```python
  if products:
      print(f"Получено {len(products)} аффилированных товаров.")
      for product in products:
          print(f"товар ID: {product.product_id}")
          print(f"Аффилированная ссылка: {product.promotion_link}")
          print(f"Локальный путь к изображению: {product.local_image_path}")
          if product.local_video_path:
              print(f"Локальный путь к видео: {product.local_video_path}")
          print()
  else:
      print("Не удалось получить аффилированные товары.")
  ```
  Здесь мы проверяем, есть ли обработанные товары, и выводим информацию о каждом товаре.

Этот пример демонстрирует базовое использование класса `AliAffiliatedProducts` и его методов. Вы можете адаптировать его под свои нужды и добавить больше функциональности, если это необходимо.

### Полный файл примеров

```python
# пример_использования.py

from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts

def main():
    # Задайте параметры рекламной кампании
    campaign_name = "summer_sale_2024"
    campaign_category = "electronics"  # Можно задать None, если категория не нужна
    language = "EN"  # Язык для кампании
    currency = "USD"  # Валюта для кампании

    # Создайте экземпляр класса AliAffiliatedProducts
    parser = AliAffiliatedProducts(
        campaign_name,
        campaign_category,
        language,
        currency
    )

    # Пример URL товаров или их ID
    prod_urls = [
        '123',
        'https://www.aliexpress.com/item/123.html',
        '456',
        'https://www.aliexpress.com/item/456.html',
    ]

    # Обработайте товары и получите список товаров с аффилированными ссылками
    products = parser.process_affiliate_products(prod_urls)

    # Проверьте результаты
    if products:
        print(f"Получено {len(products)} аффилированных товаров.")
        for product in products:
            print(f"товар ID: {product.product_id}")
            print(f"Аффилированная ссылка: {product.promotion_link}")
            print(f"Локальный путь к изображению: {product.local_image_path}")
            if product.local_video_path:
                print(f"Локальный путь к видео: {product.local_video_path}")
            print()
    else:
        print("Не удалось получить аффилированные товары.")

if __name__ == "__main__":
    main()
```

Этот файл можно использовать как шаблон для тестирования работы класса и методов модуля `affiliated_products_generator.py`.