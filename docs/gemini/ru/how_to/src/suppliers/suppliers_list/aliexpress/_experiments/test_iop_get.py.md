### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот код демонстрирует взаимодействие с API AliExpress через библиотеку `iop`. Он создает клиент `IopClient`, выполняет запрос к API для генерации партнерской ссылки и выводит информацию об ответе, такую как тело ответа, тип, код, сообщение и идентификатор запроса.

Шаги выполнения
-------------------------
1. **Импорт библиотеки `iop`**:
   ```python
   import iop
   ```
   Этот шаг импортирует библиотеку `iop`, которая используется для взаимодействия с API AliExpress.

2. **Создание клиента `IopClient`**:
   ```python
   client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93eb26aabc391d187732af93')
   client.log_level = iop.P_LOG_LEVEL_DEBUG
   ```
   Здесь создается экземпляр класса `IopClient` с указанием URL API, ключа приложения и секрета приложения. Также устанавливается уровень логирования для отладки.

3. **Создание запроса `IopRequest`**:
   ```python
   request = iop.IopRequest('aliexpress.affiliate.link.generate')
   ```
   Создается объект запроса `IopRequest` с указанием метода API `aliexpress.affiliate.link.generate`, который используется для генерации партнерской ссылки.

4. **Добавление параметров к запросу**:
   ```python
   request.add_api_param('promotion_link_type', '0')
   request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
   request.add_api_param('tracking_id', 'default')
   ```
   К запросу добавляются параметры, необходимые для генерации партнерской ссылки: тип ссылки, исходный URL товара и идентификатор отслеживания.

5. **Выполнение запроса**:
   ```python
   response = client.execute(request)
   ```
   Выполняется запрос к API с использованием созданного клиента и запроса. Результат сохраняется в переменной `response`.

6. **Вывод информации об ответе**:
   ```python
   print(response.body)
   print(response.type)
   print(response.code)
   print(response.message)
   print(response.request_id)
   print(response.body)
   ```
   Выводится различная информация об ответе API, включая тело ответа, тип ответа, код, сообщение об ошибке и идентификатор запроса.

Пример использования
-------------------------

```python
import iop

# Создание клиента IopClient
client = iop.IopClient('https://api-sg.aliexpress.com/sync', '345846782', 'e1b26aac391d1bc3987732af93eb26aabc391d187732af93')
client.log_level = iop.P_LOG_LEVEL_DEBUG

# Создание запроса IopRequest
request = iop.IopRequest('aliexpress.affiliate.link.generate')

# Добавление параметров к запросу
request.add_api_param('promotion_link_type', '0')
request.add_api_param('source_values', 'https://www.aliexpress.com/item/1005005058280371.html')
request.add_api_param('tracking_id', 'default')

# Выполнение запроса
response = client.execute(request)

# Вывод информации об ответе
print(response.body)
print(response.type)
print(response.code)
print(response.message)
print(response.request_id)
print(response.body)