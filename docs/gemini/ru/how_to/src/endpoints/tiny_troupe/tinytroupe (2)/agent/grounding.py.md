### **Как использовать блок кода для коннекторов граундинга**

=========================================================================================

Описание
-------------------------
Этот код определяет набор классов для подключения различных источников данных (файлы, веб-страницы) к агенту для расширения его знаний. Он включает абстрактный класс `GroundingConnector` и его реализации для семантического поиска, локальных файлов и веб-страниц.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `JsonSerializableRegistry` и `utils` из `tinytroupe`.
   - Импортируются модули `logger` из `tinytroupe.agent`.
   - Импортируются классы `VectorStoreIndex` и `SimpleDirectoryReader` из `llama_index.core`.

2. **Определение абстрактного класса `GroundingConnector`**:
   - Класс определяет интерфейс для коннекторов граундинга.
   - Определены методы, которые должны быть реализованы в подклассах:
     - `retrieve_relevant`: Извлекает релевантные данные из источника.
     - `retrieve_by_name`: Извлекает источник данных по имени.
     - `list_sources`: Возвращает список доступных источников данных.

3. **Определение базового класса `BaseSemanticGroundingConnector`**:
   - Класс расширяет `GroundingConnector` и добавляет функциональность семантического поиска на основе `VectorStoreIndex` из библиотеки `llama_index`.
   - Метод `_post_init` вызывается после инициализации объекта и выполняет дополнительную настройку, такую как инициализация индекса.
   - Метод `retrieve_relevant` извлекает релевантные фрагменты текста на основе семантического поиска.
   - Метод `retrieve_by_name` извлекает контент по имени документа.
   - Метод `add_document` добавляет один документ для семантического поиска.
   - Метод `add_documents` добавляет несколько документов для семантического поиска и обновляет индекс.

4. **Определение класса `LocalFilesGroundingConnector`**:
   - Класс расширяет `BaseSemanticGroundingConnector` и добавляет функциональность для работы с локальными файлами.
   - Метод `add_folders` добавляет путь к папке с файлами для граундинга.
   - Метод `add_folder` добавляет одну папку для граундинга.
   - Метод `add_file_path` добавляет путь к файлу для граундинга.
   - Метод `_mark_folder_as_loaded` отмечает папку как загруженную, чтобы избежать повторной загрузки.

5. **Определение класса `WebPagesGroundingConnector`**:
   - Класс расширяет `BaseSemanticGroundingConnector` и добавляет функциональность для работы с веб-страницами.
   - Метод `add_web_urls` добавляет URL-адреса для граундинга.
   - Метод `add_web_url` добавляет один URL-адрес для граундинга.
   - Метод `_mark_web_url_as_loaded` отмечает URL-адрес как загруженный, чтобы избежать повторной загрузки.

Пример использования
-------------------------

```python
    from tinytroupe.agent.grounding import LocalFilesGroundingConnector

    # Создание экземпляра коннектора для локальных файлов
    local_files_connector = LocalFilesGroundingConnector(name="Мои файлы", folders_paths=["/path/to/your/files"])

    # Добавление папки с файлами для граундинга
    local_files_connector.add_folder("/path/to/your/files")

    # Поиск релевантной информации
    relevant_info = local_files_connector.retrieve_relevant("ключевое слово", top_k=5)

    # Вывод результатов
    for info in relevant_info:
        print(info)
```
```python
    from tinytroupe.agent.grounding import WebPagesGroundingConnector

    # Создание экземпляра коннектора для веб-страниц
    web_pages_connector = WebPagesGroundingConnector(name="Мои веб-страницы", web_urls=["http://example.com"])

    # Добавление URL-адреса для граундинга
    web_pages_connector.add_web_url("http://example.com")

    # Поиск релевантной информации
    relevant_info = web_pages_connector.retrieve_relevant("ключевое слово", top_k=5)

    # Вывод результатов
    for info in relevant_info:
        print(info)