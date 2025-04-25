## Как использовать модуль `src.endpoints.prestashop.language`

=========================================================================================

### Описание
-------------------------
Модуль `src.endpoints.prestashop.language` предоставляет функциональность для работы с языками в PrestaShop. Он использует API PrestaShop для взаимодействия с сущностью `language`.

### Шаги выполнения
-------------------------
1. **Инициализация класса:** 
   - Создайте экземпляр класса `PrestaLanguage`, передавая в конструктор домен API и ключ API для доступа к PrestaShop.
   - В конструкторе необходимо указать правильные домен API и ключ API, которые будут использоваться для запросов к PrestaShop. 
   - Конструктор класса устанавливает базовые настройки для подключения к API PrestaShop и инициализирует переменные, которые используются в других методах.
2. **Получение информации о языках:**
   - Используйте метод `get_languages_schema()` для получения актуального списка языков, доступных в магазине PrestaShop.
   - Метод отправляет запрос к API PrestaShop и возвращает словарь с информацией о языках, которые доступны в магазине.
   - В словаре содержится список языков с их ID, а также другая информация, например, название языка.
3. **Получение имени языка по индексу:**
   - Метод `get_lang_name_by_index(lang_index)` получает имя языка по его индексу в таблице PrestaShop.
   - Метод отправляет запрос к API PrestaShop и возвращает имя языка в виде строки, например, 'en', 'ru' или 'he'.
4. **Добавление, удаление и обновление языков:**
   - Используйте методы `add_language_PrestaShop(lang_name, lang_iso)`, `delete_language_PrestaShop(lang_id)` и `update_language_PrestaShop(lang_id, new_lang_name)` для управления языками в PrestaShop.
   - Методы добавляют, удаляют или обновляют языки в PrestaShop с помощью API.
   - Методы `add_language_PrestaShop` и `update_language_PrestaShop` принимают название языка и его ISO код.
   - Метод `delete_language_PrestaShop` принимает ID языка, который необходимо удалить.


### Пример использования
-------------------------

```python
from src.endpoints.prestashop.language import PrestaLanguage

# Домен API и ключ API для подключения к PrestaShop
API_DOMAIN = 'https://www.example.com'
API_KEY = 'your_api_key'

# Инициализация класса PrestaLanguage
lang_class = PrestaLanguage(API_DOMAIN=API_DOMAIN, API_KEY=API_KEY)

# Получение актуального списка языков
languagas_schema = lang_class.get_languages_schema()

# Вывод полученной информации
print(languagas_schema)

# Получение имени языка по индексу
lang_name = lang_class.get_lang_name_by_index(1)
print(f'Название языка с индексом 1: {lang_name}')

# Добавление нового языка
lang_class.add_language_PrestaShop('German', 'de')

# Удаление языка с ID 3
lang_class.delete_language_PrestaShop(3)

# Обновление названия языка с ID 4
lang_class.update_language_PrestaShop(4, 'Updated Language Name')
```