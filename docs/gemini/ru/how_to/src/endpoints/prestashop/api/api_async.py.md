Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой асинхронный клиент для взаимодействия с API PrestaShop, который позволяет выполнять различные операции, такие как создание, чтение, обновление, удаление и поиск ресурсов, а также загрузку изображений.

Шаги выполнения
-------------------------
1. **Инициализация класса `PrestaShopAsync`**:
   - Создается экземпляр класса `PrestaShopAsync` с указанием домена API, ключа API, формата данных и режима отладки.
   - Пример:
     ```python
     api = PrestaShopAsync(
         api_domain='https://your-prestashop-domain.com',
         api_key='your_api_key',
         data_format='JSON',
         debug=True
     )
     ```

2. **Проверка соединения с API**:
   - Вызывается метод `ping()` для проверки доступности API.
   - Пример:
     ```python
     await api.ping()
     ```

3. **Создание ресурса**:
   - Подготавливаются данные для создания нового ресурса, например, налога.
   - Вызывается метод `create()` с указанием типа ресурса и данных.
   - Пример:
     ```python
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
     rec = await api.create('taxes', data)
     ```

4. **Чтение ресурса**:
   - Вызывается метод `read()` для получения данных о конкретном ресурсе по его ID.
   - Пример:
     ```python
     resource_id = 123
     resource = await api.read('products', resource_id)
     ```

5. **Обновление ресурса**:
   - Подготавливаются данные для обновления существующего ресурса.
   - Вызывается метод `write()` с указанием типа ресурса и обновленных данных.
   - Пример:
     ```python
     update_data = {
         'tax': {
             'id': str(rec['id']),
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
     update_rec = await api.write('taxes', update_data)
     ```

6. **Удаление ресурса**:
   - Вызывается метод `unlink()` для удаления ресурса по его ID.
   - Пример:
     ```python
     await api.unlink('taxes', str(rec['id']))
     ```

7. **Поиск ресурсов**:
   - Вызывается метод `search()` с указанием типа ресурса и фильтра для поиска.
   - Пример:
     ```python
     recs = await api.search('taxes', filter='[name]=%[5]%', limit='3')
     for rec in recs:
         pprint(rec)
     ```

8. **Загрузка изображения**:
   - Вызывается метод `create_binary()` для загрузки бинарного файла (изображения) в API.
   - Пример:
     ```python
     await api.create_binary('images/products/22', 'img.jpeg', 'image')
     ```

9. **Асинхронная загрузка изображения**:
   - Вызывается метод `upload_image_async()` для асинхронной загрузки изображения по URL.
   - Пример:
     ```python
     resource = 'images/products/22'
     resource_id = 22
     img_url = 'https://example.com/image.jpg'
     img_name = 'my_image'
     response = await api.upload_image_async(resource, resource_id, img_url, img_name)
     ```

Пример использования
-------------------------

```python
import asyncio
from src.endpoints.prestashop.api.api_async import PrestaShopAsync
from src.utils.printer import pprint as print

async def main():
    api = PrestaShopAsync(
        api_domain='https://your-prestashop-domain.com/api',
        api_key='your_api_key',
        data_format='JSON',
        debug=True
    )

    await api.ping()

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

    rec = await api.create('taxes', data)

    update_data = {
        'tax': {
            'id': str(rec['id']),
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

    update_rec = await api.write('taxes', update_data)

    await api.unlink('taxes', str(rec['id']))

    recs = await api.search('taxes', filter='[name]=%[5]%', limit='3')

    for rec in recs:
        print(rec)

    await api.create_binary('images/products/22', 'img.jpeg', 'image')

if __name__ == "__main__":
    asyncio.run(main())