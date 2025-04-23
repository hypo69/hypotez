### Как использовать класс `PrestaShop` для взаимодействия с PrestaShop API
=========================================================================================

Описание
-------------------------
Класс `PrestaShop` предоставляет интерфейс для взаимодействия с PrestaShop API, позволяя выполнять CRUD-операции (создание, чтение, обновление, удаление) над ресурсами PrestaShop, а также осуществлять поиск и загрузку изображений. Он использует HTTP-запросы для обмена данными с API, поддерживая форматы JSON и XML.

Шаги выполнения
-------------------------
1. **Инициализация класса `PrestaShop`**:
   - Создайте экземпляр класса `PrestaShop`, передав необходимые параметры: `api_key` (ключ API), `api_domain` (доменное имя магазина PrestaShop), `data_format` (формат данных, по умолчанию 'JSON'), `default_lang` (ID языка по умолчанию) и `debug` (режим отладки).
   - Функция проверяет доступность API, отправляя HEAD-запрос к `api_domain`.
   - Если возникает ошибка при инициализации (например, неверный API-ключ или недоступный домен), будет выброшено исключение `PrestaShopAuthenticationError` или `PrestaShopException`.

2. **Выполнение операций CRUD**:
   - Используйте методы `create`, `read`, `write` и `unlink` для выполнения операций создания, чтения, обновления и удаления ресурсов соответственно.
   - Метод `create` создает новый ресурс, метод `read` извлекает существующий ресурс по его ID, метод `write` обновляет существующий ресурс, а метод `unlink` удаляет ресурс.

3. **Поиск ресурсов**:
   - Используйте метод `search` для поиска ресурсов, соответствующих заданным критериям фильтрации.
   - Можно указать фильтр (`filter`) для уточнения результатов поиска.

4. **Загрузка изображений**:
   - Используйте метод `create_binary` для загрузки бинарных файлов (например, изображений) в API PrestaShop.
   - Укажите путь к файлу (`file_path`) и имя файла (`file_name`).

5. **Получение схемы ресурса**:
   - Используйте метод `get_schema` для получения схемы определенного ресурса. Это может быть полезно для понимания структуры данных, ожидаемой API.

Пример использования
-------------------------

```python
from src.endpoints.prestashop.api import PrestaShop
from src.endpoints.prestashop.api import Config

# Создание экземпляра класса PrestaShop
api = PrestaShop(
    api_key=Config.API_KEY,
    api_domain=Config.API_DOMAIN,
    default_lang=1,
    debug=True,
    data_format=Config.POST_FORMAT,
)

# Определение данных для создания нового налога
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

# Создание налога
tax = api.create('taxes', data)
if tax:
    print(f"Налог создан: {tax}")

    # Чтение созданного налога
    tax_read = api.read('taxes', tax['tax']['id'])
    if tax_read:
        print(f"Налог прочитан: {tax_read}")

    # Обновление налога
    data['tax']['name']['language']['value'] = 'Новое название налога'
    tax_update = api.write('taxes', tax['tax']['id'], data)
    if tax_update:
        print(f"Налог обновлен: {tax_update}")

    # Удаление налога
    if api.unlink('taxes', tax['tax']['id']):
        print("Налог удален")
    else:
        print("Не удалось удалить налог")
else:
    print("Не удалось создать налог")

# Поиск налогов
taxes = api.search('taxes', filter='[name]=%tax%')
if taxes:
    print(f"Найденные налоги: {taxes}")
else:
    print("Налоги не найдены")

# Загрузка изображения (пример)
# api.create_binary('images/products/22', 'img.jpeg', 'image')