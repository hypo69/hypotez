### **Анализ кода модуля `grounding.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/agent/grounding.py

Модуль содержит классы для реализации коннекторов, обеспечивающих интеграцию агента с различными источниками знаний.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование абстрактного класса `GroundingConnector` для определения интерфейса коннекторов.
    - Применение декоратора `@utils.post_init` для отложенной инициализации.
    - Наличие классов для работы с локальными файлами и веб-страницами.
    - Управление загруженными ресурсами (файлами, URL) для предотвращения повторной обработки.
- **Минусы**:
    - Отсутствуют аннотации типов для переменных в некоторых местах.
    - Смешанный стиль комментариев (русский и английский языки).
    - Недостаточно подробные docstring для некоторых методов.
    - Дублирование кода в методах `add_web_url` и `add_web_urls`.
    - Использование `print` для вывода ошибок вместо `logger.error`.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных, где они отсутствуют.

2.  **Унифицировать стиль комментариев и docstring**:
    - Перевести все комментарии и docstring на русский язык и привести к единому стилю.

3.  **Улучшить docstring**:
    - Добавить более подробные описания для всех методов, включая аргументы, возвращаемые значения и возможные исключения.

4.  **Изменить обработку ошибок**:
    - Заменить `print` на `logger.error` для логирования ошибок.

5.  **Улучшить структуру кода**:
    - Избегать дублирования кода, например, в методах `add_web_url` и `add_web_urls`.

**Оптимизированный код:**

```python
from tinytroupe.utils import JsonSerializableRegistry
import tinytroupe.utils as utils
import os # Импортируем модуль os для работы с файловой системой
from typing import List, Optional, Callable
from pathlib import Path

from tinytroupe.agent import logger
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.readers.web import SimpleWebPageReader


#######################################################################################################################
# Grounding connectors
#######################################################################################################################

class GroundingConnector(JsonSerializableRegistry):
    """
    Абстрактный класс, представляющий коннектор заземления. Коннектор заземления - это компонент, который позволяет агенту заземлять
    свои знания во внешних источниках, таких как файлы, веб-страницы, базы данных и т.д.
    """

    serializable_attributes: List[str] = ['name']

    def __init__(self, name: str) -> None:
        """
        Инициализирует экземпляр класса GroundingConnector.

        Args:
            name (str): Имя коннектора заземления.
        """
        self.name: str = name

    def retrieve_relevant(self, relevance_target: str, source: str, top_k: int = 20) -> list:
        """
        Извлекает все значения из памяти, релевантные данной цели.

        Args:
            relevance_target (str): Цель релевантности.
            source (str): Источник.
            top_k (int): Количество извлекаемых элементов. По умолчанию 20.

        Returns:
            list: Список релевантных значений.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def retrieve_by_name(self, name: str) -> str:
        """
        Извлекает источник контента по его имени.

        Args:
            name (str): Имя источника контента.

        Returns:
            str: Источник контента.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def list_sources(self) -> list:
        """
        Перечисляет имена доступных источников контента.

        Returns:
            list: Список имен источников контента.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')


@utils.post_init
class BaseSemanticGroundingConnector(GroundingConnector):
    """
    Базовый класс для семантических коннекторов заземления. Семантический коннектор заземления - это компонент, который индексирует и извлекает
    документы на основе так называемого "семантического поиска" (т.е. поиска на основе embeddings). Эта конкретная реализация
    основана на классе VectorStoreIndex из библиотеки LLaMa-Index. Здесь "документы" относятся к структуре данных llama-index,
    которая хранит единицу контента, не обязательно файл.
    """

    serializable_attributes: List[str] = ['documents']

    def __init__(self, name: str = 'Semantic Grounding') -> None:
        """
        Инициализирует экземпляр класса BaseSemanticGroundingConnector.

        Args:
            name (str): Имя коннектора заземления. По умолчанию 'Semantic Grounding'.
        """
        super().__init__(name)

        self.documents: Optional[List] = None
        self.name_to_document: Optional[dict] = None

        # @post_init ensures that _post_init is called after the __init__ method

    def _post_init(self) -> None:
        """
        Этот метод будет запущен после __init__, так как класс имеет декоратор @post_init.
        Удобно разделять некоторые процессы инициализации, чтобы упростить десериализацию.
        """
        self.index: Optional[VectorStoreIndex] = None

        if not hasattr(self, 'documents') or self.documents is None:
            self.documents = []

        if not hasattr(self, 'name_to_document') or self.name_to_document is None:
            self.name_to_document = {}

        self.add_documents(self.documents)

    def retrieve_relevant(self, relevance_target: str, top_k: int = 20) -> list:
        """
        Извлекает все значения из памяти, релевантные данной цели.

        Args:
            relevance_target (str): Цель релевантности.
            top_k (int): Количество извлекаемых элементов. По умолчанию 20.

        Returns:
            list: Список релевантных значений.
        """
        if self.index is not None:
            retriever = self.index.as_retriever(similarity_top_k=top_k)
            nodes = retriever.retrieve(relevance_target)
        else:
            nodes = []

        retrieved = []
        for node in nodes:
            content = 'SOURCE: ' + node.metadata.get('file_name', '(unknown)')
            content += '\n' + 'SIMILARITY SCORE:' + str(node.score)
            content += '\n' + 'RELEVANT CONTENT:' + node.text
            retrieved.append(content)

            logger.debug(f'Content retrieved: {content[:200]}')

        return retrieved

    def retrieve_by_name(self, name: str) -> list:
        """
        Извлекает источник контента по его имени.

        Args:
            name (str): Имя источника контента.

        Returns:
            list: Список источников контента.
        """
        # TODO also optionally provide a relevance target?
        results = []
        if self.name_to_document is not None and name in self.name_to_document:
            docs = self.name_to_document[name]
            for i, doc in enumerate(docs):
                if doc is not None:
                    content = f'SOURCE: {name}\n'
                    content += f'PAGE: {i}\n'
                    content += 'CONTENT: \n' + doc.text[:10000]  # TODO a more intelligent way to limit the content
                    results.append(content)

        return results

    def list_sources(self) -> list:
        """
        Перечисляет имена доступных источников контента.

        Returns:
            list: Список имен источников контента.
        """
        if self.name_to_document is not None:
            return list(self.name_to_document.keys())
        else:
            return []

    def add_document(self, document, doc_to_name_func: Optional[Callable] = None) -> None:
        """
        Индексирует документ для семантического извлечения.

        Args:
            document: Документ для индексации.
            doc_to_name_func (Optional[Callable]): Функция для получения имени документа.
        """
        self.add_documents([document], doc_to_name_func)

    def add_documents(self, new_documents: List, doc_to_name_func: Optional[Callable] = None) -> None:
        """
        Индексирует документы для семантического извлечения.

        Args:
            new_documents (List): Список документов для индексации.
            doc_to_name_func (Optional[Callable]): Функция для получения имени документа.
        """
        # index documents by name
        if len(new_documents) > 0:
            # add the new documents to the list of documents
            self.documents += new_documents

            # process documents individually too
            for document in new_documents:

                # out of an abundance of caution, we sanitize the text
                document.text = utils.sanitize_raw_string(document.text)

                if doc_to_name_func is not None:
                    name = doc_to_name_func(document)

                    # self.name_to_document[name] contains a list, since each source file could be split into multiple pages
                    if name in self.name_to_document:
                        self.name_to_document[name].append(document)
                    else:
                        self.name_to_document[name] = [document]

            # index documents for semantic retrieval
            if self.index is None:
                self.index = VectorStoreIndex.from_documents(self.documents)
            else:
                self.index.refresh(self.documents)


@utils.post_init
class LocalFilesGroundingConnector(BaseSemanticGroundingConnector):
    """
    Коннектор заземления для локальных файлов.
    """

    serializable_attributes: List[str] = ['folders_paths']

    def __init__(self, name: str = 'Local Files', folders_paths: Optional[List[str]] = None) -> None:
        """
        Инициализирует экземпляр класса LocalFilesGroundingConnector.

        Args:
            name (str): Имя коннектора. По умолчанию 'Local Files'.
            folders_paths (Optional[List[str]]): Список путей к папкам. По умолчанию None.
        """
        super().__init__(name)

        self.folders_paths: Optional[List[str]] = folders_paths

        # @post_init ensures that _post_init is called after the __init__ method

    def _post_init(self) -> None:
        """
        Выполняется после __init__. Используется для отложенной инициализации.
        """
        self.loaded_folders_paths: List[str] = []

        if not hasattr(self, 'folders_paths') or self.folders_paths is None:
            self.folders_paths = []

        self.add_folders(self.folders_paths)

    def add_folders(self, folders_paths: Optional[List[str]]) -> None:
        """
        Добавляет пути к папкам с файлами, используемыми для заземления.

        Args:
            folders_paths (Optional[List[str]]): Список путей к папкам.
        """

        if folders_paths is not None:
            for folder_path in folders_paths:
                try:
                    logger.debug(f'Adding the following folder to grounding index: {folder_path}')
                    self.add_folder(folder_path)
                except (FileNotFoundError, ValueError) as ex:
                    logger.error(f'Error: {ex}', exc_info=True) # Логируем ошибку с использованием logger.error
                    logger.error(f'Current working directory: {os.getcwd()}', exc_info=True) # Логируем текущую рабочую директорию
                    logger.error(f'Provided path: {folder_path}', exc_info=True) # Логируем предоставленный путь
                    logger.error('Please check if the path exists and is accessible.', exc_info=True) # Логируем сообщение о проверке доступности пути

    def add_folder(self, folder_path: str) -> None:
        """
        Добавляет путь к папке с файлами, используемыми для заземления.

        Args:
            folder_path (str): Путь к папке.
        """

        if folder_path not in self.loaded_folders_paths:
            self._mark_folder_as_loaded(folder_path)

            # for PDF files, please note that the document will be split into pages: https://github.com/run-llama/llama_index/issues/15903
            new_files = SimpleDirectoryReader(folder_path).load_data()
            self.add_documents(new_files, lambda doc: doc.metadata['file_name'])

    def add_file_path(self, file_path: str) -> None:
        """
        Добавляет путь к файлу, используемому для заземления.

        Args:
            file_path (str): Путь к файлу.
        """
        # a trick to make SimpleDirectoryReader work with a single file
        new_files = SimpleDirectoryReader(input_files=[file_path]).load_data()

        logger.debug(f'Adding the following file to grounding index: {new_files}')
        self.add_documents(new_files, lambda doc: doc.metadata['file_name'])

    def _mark_folder_as_loaded(self, folder_path: str) -> None:
        """
        Отмечает папку как загруженную.

        Args:
            folder_path (str): Путь к папке.
        """
        if folder_path not in self.loaded_folders_paths:
            self.loaded_folders_paths.append(folder_path)

        if folder_path not in self.folders_paths:
            self.folders_paths.append(folder_path)


@utils.post_init
class WebPagesGroundingConnector(BaseSemanticGroundingConnector):
    """
    Коннектор заземления для веб-страниц.
    """

    serializable_attributes: List[str] = ['web_urls']

    def __init__(self, name: str = 'Web Pages', web_urls: Optional[List[str]] = None) -> None:
        """
        Инициализирует экземпляр класса WebPagesGroundingConnector.

        Args:
            name (str): Имя коннектора. По умолчанию 'Web Pages'.
            web_urls (Optional[List[str]]): Список URL веб-страниц. По умолчанию None.
        """
        super().__init__(name)

        self.web_urls: Optional[List[str]] = web_urls

        # @post_init ensures that _post_init is called after the __init__ method

    def _post_init(self) -> None:
        """
        Выполняется после __init__. Используется для отложенной инициализации.
        """
        self.loaded_web_urls: List[str] = []

        if not hasattr(self, 'web_urls') or self.web_urls is None:
            self.web_urls = []

        # load web urls
        self.add_web_urls(self.web_urls)

    def add_web_urls(self, web_urls: List[str]) -> None:
        """
        Добавляет данные, полученные из указанных URL-адресов, в заземление.

        Args:
            web_urls (List[str]): Список URL веб-страниц.
        """
        filtered_web_urls = [url for url in web_urls if url not in self.loaded_web_urls]
        for url in filtered_web_urls:
            self._mark_web_url_as_loaded(url)

        if len(filtered_web_urls) > 0:
            new_documents = SimpleWebPageReader(html_to_text=True).load_data(filtered_web_urls)
            self.add_documents(new_documents, lambda doc: doc.id_)

    def add_web_url(self, web_url: str) -> None:
        """
        Добавляет данные, полученные из указанного URL-адреса, в заземление.

        Args:
            web_url (str): URL веб-страницы.
        """
        # we do it like this because the add_web_urls could run scrapes in parallel, so it is better
        # to implement this one in terms of the other
        self.add_web_urls([web_url])

    def _mark_web_url_as_loaded(self, web_url: str) -> None:
        """
        Отмечает веб-URL как загруженный.

        Args:
            web_url (str): URL веб-страницы.
        """
        if web_url not in self.loaded_web_urls:
            self.loaded_web_urls.append(web_url)

        if web_url not in self.web_urls:
            self.web_urls.append(web_url)