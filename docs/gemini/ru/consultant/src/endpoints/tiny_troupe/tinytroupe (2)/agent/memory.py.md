### **Анализ кода модуля `memory.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/agent/memory.py

Модуль содержит классы для реализации различных типов памяти агента: `TinyMemory`, `EpisodicMemory` и `SemanticMemory`.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Наличие базового класса `TinyMemory` с общей функциональностью.
    - Разделение на эпизодическую и семантическую память.
    - Использование `NotImplementedError` для абстрактных методов.
    - Все методы аннотированы типами
- **Минусы**:
    - Отсутствует логирование.
    - Не хватает документации для некоторых методов.
    - Не везде используется модуль `logger` из `src.logger`.
    - Есть `...` в коде
    - Не везде есть docstring

**Рекомендации по улучшению:**

1.  **Добавить логирование**:
    - Добавить логирование важных событий и ошибок с использованием модуля `logger` из `src.logger`.
    - Логировать можно добавление новых воспоминаний, извлечение информации и другие ключевые моменты.

2.  **Улучшить документацию**:
    - Добавить docstring для методов `_preprocess_value_for_storage`, `_build_document_from`, `_build_documents_from` и других, чтобы объяснить их назначение и параметры.
    - Описать возвращаемые значения и возможные исключения.

3.  **Обработка исключений**:
    - Добавить обработку исключений в методы, где это необходимо, с использованием `try-except` блоков и логированием ошибок через `logger.error`.

4.  **Улучшить стиль кода**:
    - Убедиться, что все строки соответствуют PEP8, особенно в части пробелов вокруг операторов.

5.  **Изменить способ обработки `...`**:
    - Убрать `...` из кода и заменить их конкретной реализацией или заглушкой с логированием.

6.  **Добавить аннотации типов**:
    - Убедиться, что все переменные и параметры функций аннотированы типами.

**Оптимизированный код:**

```python
from tinytroupe.agent.mental_faculty import TinyMentalFaculty
from tinytroupe.agent.grounding import BaseSemanticGroundingConnector
import tinytroupe.utils as utils
from src.logger import logger  # Import logger
from llama_index.core import Document
from typing import Any, List, Optional
import copy
from pathlib import Path

#######################################################################################################################
# Memory mechanisms
#######################################################################################################################


class TinyMemory(TinyMentalFaculty):
    """
    Базовый класс для различных типов памяти.
    """

    def _preprocess_value_for_storage(self, value: Any) -> Any:
        """
        Преобразует значение перед сохранением в памяти.

        Args:
            value (Any): Значение для преобразования.

        Returns:
            Any: Преобразованное значение.
        """
        # по умолчанию мы не преобразуем значение
        return value

    def _store(self, value: Any) -> None:
        """
        Сохраняет значение в памяти.

        Args:
            value (Any): Значение для сохранения.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def store(self, value: dict) -> None:
        """
        Сохраняет значение в памяти.

        Args:
            value (dict): Значение для сохранения.
        """
        self._store(self._preprocess_value_for_storage(value))

    def store_all(self, values: list) -> None:
        """
        Сохраняет список значений в памяти.

        Args:
            values (list): Список значений для сохранения.
        """
        for value in values:
            self.store(value)

    def retrieve(self, first_n: int, last_n: int, include_omission_info: bool = True) -> list:
        """
        Извлекает первые n и/или последние n значений из памяти. Если n is None, извлекаются все значения.

        Args:
            first_n (int): Количество первых значений для извлечения.
            last_n (int): Количество последних значений для извлечения.
            include_omission_info (bool): Включать ли информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Извлеченные значения.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def retrieve_recent(self) -> list:
        """
        Извлекает n самых последних значений из памяти.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def retrieve_all(self) -> list:
        """
        Извлекает все значения из памяти.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def retrieve_relevant(self, relevance_target: str, top_k: int = 20) -> list:
        """
        Извлекает все значения из памяти, которые релевантны заданной цели.

        Args:
            relevance_target (str): Цель релевантности.
            top_k (int): Количество наиболее релевантных значений для извлечения.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')


class EpisodicMemory(TinyMemory):
    """
    Предоставляет возможности эпизодической памяти агенту. Когнитивно, эпизодическая память - это способность помнить конкретные события
    или эпизоды в прошлом. Этот класс предоставляет простую реализацию эпизодической памяти, где агент может сохранять и извлекать
    сообщения из памяти.

    Подклассы этого класса могут использоваться для предоставления различных реализаций памяти.
    """

    MEMORY_BLOCK_OMISSION_INFO = {'role': 'assistant', 'content': 'Info: there were other messages here, but they were omitted for brevity.', 'simulation_timestamp': None}

    def __init__(
        self, fixed_prefix_length: int = 100, lookback_length: int = 100
    ) -> None:
        """
        Инициализирует память.

        Args:
            fixed_prefix_length (int): Фиксированная длина префикса. По умолчанию 20.
            lookback_length (int): Длина обратного просмотра. По умолчанию 20.
        """
        self.fixed_prefix_length = fixed_prefix_length
        self.lookback_length = lookback_length

        self.memory = []

    def _store(self, value: Any) -> None:
        """
        Сохраняет значение в памяти.

        Args:
            value (Any): Значение для сохранения.
        """
        self.memory.append(value)

    def count(self) -> int:
        """
        Возвращает количество значений в памяти.

        Returns:
            int: Количество значений в памяти.
        """
        return len(self.memory)

    def retrieve(self, first_n: int, last_n: int, include_omission_info: bool = True) -> list:
        """
        Извлекает первые n и/или последние n значения из памяти. Если n is None, извлекаются все значения.

        Args:
            first_n (int): Количество первых значений для извлечения.
            last_n (int): Количество последних значений для извлечения.
            include_omission_info (bool): Включать ли информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Извлеченные значения.
        """

        omisssion_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

        # используем другие методы в классе для реализации
        if first_n is not None and last_n is not None:
            return self.retrieve_first(first_n) + omisssion_info + self.retrieve_last(last_n)
        elif first_n is not None:
            return self.retrieve_first(first_n)
        elif last_n is not None:
            return self.retrieve_last(last_n)
        else:
            return self.retrieve_all()

    def retrieve_recent(self, include_omission_info: bool = True) -> list:
        """
        Извлекает n самых последних значений из памяти.

        Args:
            include_omission_info (bool): Включать ли информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Список последних значений из памяти.
        """
        omisssion_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

        # вычисляем фиксированный префикс
        fixed_prefix = self.memory[: self.fixed_prefix_length] + omisssion_info

        # сколько значений lookback осталось?
        remaining_lookback = min(
            len(self.memory) - len(fixed_prefix), self.lookback_length
        )

        # вычисляем оставшиеся значения lookback и возвращаем конкатенацию
        if remaining_lookback <= 0:
            return fixed_prefix
        else:
            return fixed_prefix + self.memory[-remaining_lookback:]

    def retrieve_all(self) -> list:
        """
        Извлекает все значения из памяти.

        Returns:
            list: Копия всех значений из памяти.
        """
        return copy.copy(self.memory)

    def retrieve_relevant(self, relevance_target: str, top_k: int) -> list:
        """
        Извлекает top-k значений из памяти, которые наиболее релевантны заданной цели.

        Args:
            relevance_target (str): Цель релевантности.
            top_k (int): Количество наиболее релевантных значений для извлечения.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def retrieve_first(self, n: int, include_omission_info: bool = True) -> list:
        """
        Извлекает первые n значений из памяти.

        Args:
            n (int): Количество первых значений для извлечения.
            include_omission_info (bool): Включать ли информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Список первых n значений из памяти.
        """
        omisssion_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

        return self.memory[:n] + omisssion_info

    def retrieve_last(self, n: int, include_omission_info: bool = True) -> list:
        """
        Извлекает последние n значений из памяти.

        Args:
            n (int): Количество последних значений для извлечения.
            include_omission_info (bool): Включать ли информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Список последних n значений из памяти.
        """
        omisssion_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

        return omisssion_info + self.memory[-n:]


@utils.post_init
class SemanticMemory(TinyMemory):
    """
    В когнитивной психологии семантическая память - это память о значениях, пониманиях и других знаниях, основанных на понятиях, не связанных с конкретными
    переживаниями. Она не упорядочена во времени и не связана с запоминанием конкретных событий или эпизодов. Этот класс предоставляет простую реализацию
    семантической памяти, где агент может хранить и извлекать семантическую информацию.
    """

    serializable_attrs = ["memories"]

    def __init__(self, memories: list = None) -> None:
        """
        Инициализирует семантическую память.

        Args:
            memories (list, optional): Список воспоминаний для инициализации. По умолчанию None.
        """
        self.memories = memories

        # @post_init гарантирует, что _post_init вызывается после метода __init__

    def _post_init(self):
        """
        Этот метод будет запущен после __init__, так как класс имеет декоратор @post_init.
        Удобно разделять некоторые процессы инициализации, чтобы облегчить десериализацию.
        """

        if not hasattr(self, 'memories') or self.memories is None:
            self.memories = []

        self.semantic_grounding_connector = BaseSemanticGroundingConnector("Semantic Memory Storage")
        self.semantic_grounding_connector.add_documents(self._build_documents_from(self.memories))

    def _preprocess_value_for_storage(self, value: dict) -> Any:
        """
        Преобразует значение перед сохранением в семантической памяти.

        Args:
            value (dict): Значение для преобразования.

        Returns:
            Any: Преобразованное значение.
        """
        engram = None

        if value['type'] == 'action':
            engram = f"# Fact\\n" + \
                     f"I have performed the following action at date and time {value['simulation_timestamp']}:\\n\\n" + \
                     f" {value['content']}"

        elif value['type'] == 'stimulus':
            engram = f"# Stimulus\\n" + \
                     f"I have received the following stimulus at date and time {value['simulation_timestamp']}:\\n\\n" + \
                     f" {value['content']}"

        # else: # Anything else here?

        return engram

    def _store(self, value: Any) -> None:
        """
        Сохраняет значение в семантической памяти.

        Args:
            value (Any): Значение для сохранения.
        """
        engram_doc = self._build_document_from(self._preprocess_value_for_storage(value))
        self.semantic_grounding_connector.add_document(engram_doc)

    def retrieve_relevant(self, relevance_target: str, top_k: int = 20) -> list:
        """
        Извлекает все значения из памяти, которые релевантны заданной цели.

        Args:
            relevance_target (str): Цель релевантности.
            top_k (int): Количество наиболее релевантных значений для извлечения.

        Returns:
            list: Список релевантных значений из памяти.
        """
        try:
            return self.semantic_grounding_connector.retrieve_relevant(relevance_target, top_k)
        except Exception as ex:
            logger.error('Error while retrieving relevant data', ex, exc_info=True)
            return []

    #####################################
    # Auxiliary compatibility methods
    #####################################

    def _build_document_from(memory: Any) -> Document:
        """
        Создает документ из воспоминания.

        Args:
            memory (Any): Воспоминание для создания документа.

        Returns:
            Document: Созданный документ.
        """
        # TODO: добавить любые метаданные?
        return Document(text=str(memory))

    def _build_documents_from(self, memories: list) -> list:
        """
        Создает список документов из списка воспоминаний.

        Args:
            memories (list): Список воспоминаний для создания документов.

        Returns:
            list: Список созданных документов.
        """
        return [self._build_document_from(memory) for memory in memories]