## Как использовать Grounding Connector в TinyTroupe

=========================================================================================

### Описание
-------------------------
Grounding Connector - это абстрактный класс, который позволяет агенту TinyTroupe извлекать информацию из внешних источников, таких как файлы, веб-страницы, базы данных и т.д. 

### Шаги выполнения
-------------------------
1. **Создай объект Grounding Connector:** 
   - Выбери подходящий подкласс Grounding Connector, например, `LocalFilesGroundingConnector` для файлов или `WebPagesGroundingConnector` для веб-страниц.
   - Инициализируй его с необходимыми параметрами.

2. **Добавь источники информации:**
   - Используй методы `add_documents` или `add_folder` для добавления данных из файлов или папок.
   - Используй методы `add_web_urls` или `add_web_url` для добавления данных из веб-страниц.

3. **Извлеки релевантную информацию:**
   - Используй метод `retrieve_relevant` для поиска информации, относящейся к заданному целевому запросу (relevance_target).
   - Используй метод `retrieve_by_name` для поиска информации по имени источника данных.

4. **Получи список источников:**
   - Используй метод `list_sources` для просмотра доступных источников информации.

### Пример использования
-------------------------

```python
from tinytroupe.agent import logger
from tinytroupe.agent.grounding import LocalFilesGroundingConnector, WebPagesGroundingConnector

# Создай объект для работы с файлами
files_connector = LocalFilesGroundingConnector(name="My Files", folders_paths=["path/to/my/files"])

# Добавь папку с файлами
files_connector.add_folder("path/to/another/folder")

# Извлеки релевантную информацию по запросу
relevance_target = "What is the capital of France?"
relevant_results = files_connector.retrieve_relevant(relevance_target)

# Выведи полученные результаты
for result in relevant_results:
    print(result)

# Создай объект для работы с веб-страницами
web_connector = WebPagesGroundingConnector(name="My Web Pages", web_urls=["https://www.example.com", "https://www.anothersite.com"])

# Добавь веб-страницы
web_connector.add_web_url("https://www.thirdwebsite.com")

# Извлеки информацию по имени источника
source_name = "https://www.example.com"
source_content = web_connector.retrieve_by_name(source_name)

# Выведи полученные результаты
for result in source_content:
    print(result)
```