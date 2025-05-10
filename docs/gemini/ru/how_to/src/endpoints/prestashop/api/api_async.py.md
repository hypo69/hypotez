## Как использовать класс `PrestaShopAsync`
=========================================================================================

Описание
-------------------------
Класс `PrestaShopAsync` предоставляет асинхронные методы для взаимодействия с API PrestaShop, 
позволяя выполнять CRUD операции, поиск и загрузку изображений. 
Он также включает обработку ошибок для ответов и методы для обработки данных API.

Шаги выполнения
-------------------------
1. **Инициализация:** Создайте экземпляр класса `PrestaShopAsync`, передав домен API, ключ API и необязательные аргументы.
2. **Проверка связи:** Используйте метод `ping()` для проверки связи с API.
3. **CRUD операции:**
    - `create()`: Создает новый ресурс в PrestaShop API.
    - `read()`: Читает ресурс из PrestaShop API.
    - `write()`: Обновляет существующий ресурс в PrestaShop API.
    - `unlink()`: Удаляет ресурс из PrestaShop API.
4. **Поиск:**
    - `search()`: Ищет ресурсы в PrestaShop API, используя фильтры.
5. **Загрузка изображений:**
    - `create_binary()`: Загружает бинарный файл (например, изображение) на ресурс PrestaShop API.
    - `upload_image()`: Загружает изображение из URL на ресурс PrestaShop API.
6. **Дополнительные методы:**
    - `get_apis()`: Возвращает список всех доступных API.
    - `get_languages_schema()`: Возвращает схему для языков.
    - `get_data()`: Получает данные из ресурса PrestaShop API и сохраняет их в файл.
    - `get_product_images()`: Получает изображения для товара.

Пример использования
-------------------------

```python
import asyncio

async def main():
    api = PrestaShopAsync(
        API_DOMAIN='https://your-prestashop-domain.com',
        API_KEY='your_api_key',
        debug=True,
        data_format='JSON',
    )

    # Проверка связи
    await api.ping() 

    # Создание нового ресурса
    data = {
        'tax': {
            'rate': 3.000,
            'active': '1',
            'name': {
                'language': {
                    'attrs': {'id': '1'},
                    'value': '3% tax'
                }
            }
        }
    }
    new_tax_record = await api.create('taxes', data)

    # Обновление ресурса
    update_data = {
        'tax': {
            'id': str(new_tax_record['id']),
            'rate': 3.000,
            'active': '1',
            'name': {
                'language': {
                    'attrs': {'id': '1'},
                    'value': '3% tax'
                }
            }
        }
    }
    updated_tax_record = await api.write('taxes', update_data)

    # Удаление ресурса
    await api.unlink('taxes', str(new_tax_record['id']))

    # Поиск ресурсов
    taxes = await api.search('taxes', filter='[name]=%[5]%', limit='3')
    for tax in taxes:
        print(tax)

    # Загрузка изображения из URL
    await api.upload_image('images/products/22', 22, 'https://example.com/image.jpg', 'product_image')

if __name__ == "__main__":
    asyncio.run(main())
```