### Как использовать класс `Config`
=========================================================================================

Описание
-------------------------
Класс `Config` предназначен для хранения и управления конфигурационными параметрами, используемыми в модуле `emil_design.py`. Он определяет значения для различных настроек, таких как конечная точка API, режим работы (dev, dev8, prod), формат POST-запросов, домен API и ключ API. В зависимости от значения `MODE` и наличия переменных окружения, класс определяет соответствующие значения для домена и ключа API.

Шаги выполнения
-------------------------
1. **Инициализация класса**: Создайте экземпляр класса `Config`. При инициализации автоматически загружаются переменные окружения (если `USE_ENV` установлен в `True`) или используются значения по умолчанию для разных режимов (`dev`, `dev8`, `prod`).
2. **Получение значений конфигурации**: Получите доступ к атрибутам класса `Config`, чтобы получить значения конфигурационных параметров, таких как `API_DOMAIN`, `API_KEY` и `MODE`.
3. **Использование в коде**: Используйте полученные значения конфигурации в других частях кода для настройки поведения программы, например, для определения конечной точки API или для аутентификации при запросах к PrestaShop.

Пример использования
-------------------------

```python
from src.endpoints.emil.emil_design import Config
from src.logger.logger import logger

# Создание экземпляра класса Config
config = Config()

# Получение значений конфигурации
api_domain = config.API_DOMAIN
api_key = config.API_KEY
mode = config.MODE

# Использование значений в коде
logger.info(f"API Domain: {api_domain}")
logger.info(f"API Key: {api_key}")
logger.info(f"Mode: {mode}")

# Пример использования API_DOMAIN и API_KEY для настройки PrestaShop
# presta = PrestaShop(api_domain=api_domain, api_key=api_key)
# presta.get_products()
```

### Как использовать метод `process_suppliers` в классе `EmilDesign`
=========================================================================================

Описание
-------------------------
Метод `process_suppliers` в классе `EmilDesign` предназначен для обработки поставщиков на основе предоставленного префикса. Если префикс не указан, используются все поставщики, перечисленные в конфигурации. Для каждого поставщика метод получает соответствующий грабер и запускает асинхронные сценарии обработки.

Шаги выполнения
-------------------------
1. **Создание экземпляра класса `EmilDesign`**:
   ```python
   from src.endpoints.emil.emil_design import EmilDesign
   emil_design = EmilDesign()
   ```

2. **Вызов метода `process_suppliers`**: Вызовите метод `process_suppliers` с указанием префикса поставщика (или без него, чтобы обработать всех поставщиков).
   ```python
   import asyncio
   asyncio.run(emil_design.process_suppliers(supplier_prefix='prefix1'))  # Обработка конкретного поставщика
   # или
   asyncio.run(emil_design.process_suppliers())  # Обработка всех поставщиков из конфигурации
   ```

3. **Обработка результатов**: Метод возвращает `True` в случае успешной обработки и `False` в случае ошибки. Логирование ошибок и предупреждений происходит внутри метода.
   ```python
   import asyncio
   from src.endpoints.emil.emil_design import EmilDesign
   from src.logger.logger import logger
   
   async def main():
       emil_design = EmilDesign()
       result = await emil_design.process_suppliers(supplier_prefix='prefix1')
       if result:
           logger.info("Обработка поставщиков выполнена успешно.")
       else:
           logger.error("Произошла ошибка при обработке поставщиков.")
   
   if __name__ == "__main__":
       asyncio.run(main())
   ```

Пример использования
-------------------------

```python
import asyncio
from src.endpoints.emil.emil_design import EmilDesign
from src.logger.logger import logger

async def main():
    emil_design = EmilDesign()
    result = await emil_design.process_suppliers(supplier_prefix='supplier_prefix')
    if result:
        logger.info("Suppliers processed successfully.")
    else:
        logger.error("An error occurred while processing suppliers.")

if __name__ == "__main__":
    asyncio.run(main())
```

### Как использовать метод `describe_images` в классе `EmilDesign`
=========================================================================================

Описание
-------------------------
Метод `describe_images` в классе `EmilDesign` предназначен для описания изображений на основе предоставленных инструкций и примеров с использованием моделей Gemini и OpenAI. Метод считывает системные инструкции и подсказки из файлов, получает список изображений для обработки из указанной директории и генерирует описания для каждого изображения с использованием выбранной модели.

Шаги выполнения
-------------------------
1. **Создание экземпляра класса `EmilDesign`**:
   ```python
   from src.endpoints.emil.emil_design import EmilDesign
   emil = EmilDesign()
   ```

2. **Вызов метода `describe_images`**: Вызовите метод `describe_images` с указанием языка для описания. Дополнительно можно передать словарь с конфигурацией моделей.
   ```python
   emil.describe_images(lang='he')
   # или с указанием конфигурации моделей:
   emil.describe_images(lang='he', models={
       'gemini': {'model_name': 'gemini-1.5-flash'},
       'openai': {'model_name': 'gpt-4o-mini', 'assistant_id': 'asst_uDr5aVY3qRByRwt5qFiMDk43'}
   })
   ```

3. **Обработка результатов**: Метод не возвращает значения. Результаты работы (описания изображений) сохраняются в JSON-файлы в директории `self.data_path`, а список обработанных изображений — в файл `described_images.txt`. Ошибки и информация о процессе логируются.

Пример использования
-------------------------

```python
from src.endpoints.emil.emil_design import EmilDesign

emil = EmilDesign()
emil.describe_images(lang='he')
```

### Как использовать метод `promote_to_facebook` в классе `EmilDesign`
=========================================================================================

Описание
-------------------------
Метод `promote_to_facebook` в классе `EmilDesign` предназначен для продвижения изображений и их описаний в Facebook. Метод использует драйвер Chrome для открытия страницы Facebook, загружает сообщения с описаниями изображений из JSON-файла и публикует их в группе Facebook.

Шаги выполнения
-------------------------
1. **Создание экземпляра класса `EmilDesign`**:
   ```python
   from src.endpoints.emil.emil_design import EmilDesign
   emil_design = EmilDesign()
   ```

2. **Вызов метода `promote_to_facebook`**: Вызовите метод `promote_to_facebook`.
   ```python
   import asyncio
   asyncio.run(emil_design.promote_to_facebook())
   ```

3. **Обработка результатов**: Метод не возвращает значения. Ошибки и информация о процессе логируются.

Пример использования
-------------------------

```python
import asyncio
from src.endpoints.emil.emil_design import EmilDesign

async def main():
    emil_design = EmilDesign()
    await emil_design.promote_to_facebook()

if __name__ == "__main__":
    asyncio.run(main())
```

### Как использовать метод `upload_described_products_to_prestashop` в классе `EmilDesign`
=========================================================================================

Описание
-------------------------
Метод `upload_described_products_to_prestashop` в классе `EmilDesign` предназначен для загрузки информации о товарах в PrestaShop. Метод получает список JSON-файлов с описаниями товаров из указанной директории, преобразует их в объекты `ProductFields` и добавляет товары в PrestaShop с использованием API.

Шаги выполнения
-------------------------
1. **Создание экземпляра класса `EmilDesign`**:
   ```python
   from src.endpoints.emil.emil_design import EmilDesign
   emil = EmilDesign()
   ```

2. **Вызов метода `upload_described_products_to_prestashop`**: Вызовите метод `upload_described_products_to_prestashop` с указанием идентификатора языка. Можно также передать список объектов `SimpleNamespace` с информацией о товарах, но обычно он формируется автоматически из JSON-файлов.
   ```python
   emil.upload_described_products_to_prestashop(id_lang=2)
   # или с указанием списка товаров:
   # products_list = [SimpleNamespace(...), SimpleNamespace(...)]
   # emil.upload_described_products_to_prestashop(products_list=products_list, id_lang=2)
   ```

3. **Обработка результатов**: Метод возвращает `True` в случае успешной загрузки и `False` в случае ошибки. Ошибки и информация о процессе логируются.

Пример использования
-------------------------

```python
from src.endpoints.emil.emil_design import EmilDesign
from src.logger.logger import logger

emil = EmilDesign()
result = emil.upload_described_products_to_prestashop(id_lang=2)
if result:
    logger.info("Товары успешно загружены в PrestaShop.")
else:
    logger.error("Произошла ошибка при загрузке товаров в PrestaShop.")