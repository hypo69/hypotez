### **Анализ кода модуля `memory.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/agent/memory.py

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Наличие базовой структуры для работы с памятью агента.
    - Использование классов `TinyMemory`, `EpisodicMemory` и `SemanticMemory` для различных типов памяти.
    - Применение паттерна `Template Method` в классах `TinyMemory` и `SemanticMemory`.
    - Использование декоратора `@utils.post_init` для постобработки инициализации.
- **Минусы**:
    - Отсутствуют docstring для некоторых методов, например, `_build_document_from(memory)`.
    - Не все типы аннотированы.
    - Не хватает логирования для отладки и мониторинга.
    - В методах `retrieve_first` и `retrieve_last` класса `EpisodicMemory` переменная `omisssion_info` пишется с тремя `s`.

#### **Рекомендации по улучшению**:
1.  **Документирование**:
    - Добавить docstring для всех методов, включая приватные (`_build_document_from`).
    - Улучшить описание существующих docstring, сделав их более подробными и понятными.
    - Перевести все docstring на русский язык, придерживаясь формата, указанного в инструкции.

2.  **Типизация**:
    - Добавить аннотации типов для всех переменных и параметров функций, где это необходимо.
    - Использовать `|` вместо `Union`.

3.  **Логирование**:
    - Добавить логирование в ключевые моменты выполнения кода, чтобы упростить отладку и мониторинг.
    - Логировать ошибки и исключения с использованием `logger.error`.

4.  **Обработка исключений**:
    - Добавить обработку исключений в методы, где это необходимо, и логировать их.

5.  **Исправление опечаток**:
    - Исправить опечатку в названии переменной `omisssion_info` на `omission_info` в методах `retrieve_first` и `retrieve_last` класса `EpisodicMemory`.

6.  **Улучшение структуры кода**:
    - Рассмотреть возможность использования абстрактных классов и интерфейсов для более четкого определения структуры классов памяти.

7.  **Общая структура модуля**:
    - Добавить в начало модуля общее описание.

#### **Оптимизированный код**:

```python
"""
Модуль для работы с различными типами памяти агента
=======================================================

Модуль содержит классы для реализации различных типов памяти агента, таких как эпизодическая и семантическая память.
Он предоставляет интерфейсы для хранения, извлечения и обработки информации, необходимой для функционирования агента.

Пример использования
----------------------

>>> from tinytroupe.agent.memory import EpisodicMemory, SemanticMemory
>>> episodic_memory = EpisodicMemory()
>>> semantic_memory = SemanticMemory()
>>> episodic_memory.store({'role': 'user', 'content': 'Hello'})
>>> semantic_memory.store({'type': 'action', 'content': 'I am walking'})
"""
from tinytroupe.agent.mental_faculty import TinyMentalFaculty
from tinytroupe.agent.grounding import BaseSemanticGroundingConnector
import tinytroupe.utils as utils

from llama_index.core import Document
from typing import Any, List, Optional
import copy

from src.logger import logger

#######################################################################################################################
# Memory mechanisms
#######################################################################################################################


class TinyMemory(TinyMentalFaculty):
    """
    Базовый класс для различных типов памяти.
    """

    def _preprocess_value_for_storage(self, value: Any) -> Any:
        """
        Предобрабатывает значение перед сохранением в память.

        Args:
            value (Any): Значение для предобработки.

        Returns:
            Any: Предобработанное значение.
        """
        # По умолчанию не выполняем предобработку значения
        return value

    def _store(self, value: Any) -> None:
        """
        Сохраняет значение в памяти.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError("Подклассы должны реализовать этот метод.")

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

    def retrieve(self, first_n: int | None, last_n: int | None, include_omission_info: bool = True) -> list:
        """
        Извлекает первые `n` и/или последние `n` значения из памяти. Если `n` равно `None`, извлекаются все значения.

        Args:
            first_n (int | None): Количество первых значений для извлечения.
            last_n (int | None): Количество последних значений для извлечения.
            include_omission_info (bool): Нужно ли включать информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Извлеченные значения.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError("Подклассы должны реализовать этот метод.")

    def retrieve_recent(self) -> list:
        """
        Извлекает самые последние значения из памяти.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError("Подклассы должны реализовать этот метод.")

    def retrieve_all(self) -> list:
        """
        Извлекает все значения из памяти.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError("Подклассы должны реализовать этот метод.")

    def retrieve_relevant(self, relevance_target: str, top_k: int = 20) -> list:
        """
        Извлекает все значения из памяти, которые соответствуют заданной цели.

        Args:
            relevance_target (str): Цель соответствия.
            top_k (int): Количество релевантных значений для извлечения. По умолчанию 20.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError("Подклассы должны реализовать этот метод.")


class EpisodicMemory(TinyMemory):
    """
    Предоставляет возможности эпизодической памяти для агента. Эпизодическая память - это способность помнить конкретные события или эпизоды в прошлом.
    Этот класс предоставляет простую реализацию эпизодической памяти, где агент может хранить и извлекать сообщения из памяти.

    Подклассы этого класса могут использоваться для предоставления различных реализаций памяти.
    """

    MEMORY_BLOCK_OMISSION_INFO = {'role': 'assistant', 'content': "Info: there were other messages here, but they were omitted for brevity.", 'simulation_timestamp': None}

    def __init__(
        self, fixed_prefix_length: int = 100, lookback_length: int = 100
    ) -> None:
        """
        Инициализирует память.

        Args:
            fixed_prefix_length (int): Фиксированная длина префикса. По умолчанию 100.
            lookback_length (int): Длина ретроспективы. По умолчанию 100.
        """
        self.fixed_prefix_length = fixed_prefix_length
        self.lookback_length = lookback_length

        self.memory: list = []

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

    def retrieve(self, first_n: int | None, last_n: int | None, include_omission_info: bool = True) -> list:
        """
        Извлекает первые `n` и/или последние `n` значения из памяти. Если `n` равно `None`, извлекаются все значения.

        Args:
            first_n (int | None): Количество первых значений для извлечения.
            last_n (int | None): Количество последних значений для извлечения.
            include_omission_info (bool): Нужно ли включать информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Извлеченные значения.
        """

        omission_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

        # используем другие методы в классе для реализации
        if first_n is not None and last_n is not None:
            return self.retrieve_first(first_n) + omission_info + self.retrieve_last(last_n)
        elif first_n is not None:
            return self.retrieve_first(first_n)
        elif last_n is not None:
            return self.retrieve_last(last_n)
        else:
            return self.retrieve_all()

    def retrieve_recent(self, include_omission_info: bool = True) -> list:
        """
        Извлекает самые последние значения из памяти.

        Args:
            include_omission_info (bool): Нужно ли включать информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Список последних значений из памяти.
        """
        omission_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

        # вычисляем фиксированный префикс
        fixed_prefix = self.memory[: self.fixed_prefix_length] + omission_info

        # сколько значений для ретроспективы осталось?
        remaining_lookback = min(
            len(self.memory) - len(fixed_prefix), self.lookback_length
        )

        # вычисляем оставшиеся значения ретроспективы и возвращаем конкатенацию
        if remaining_lookback <= 0:
            return fixed_prefix
        else:
            return fixed_prefix + self.memory[-remaining_lookback:]

    def retrieve_all(self) -> list:
        """
        Извлекает все значения из памяти.

        Returns:
            list: Все значения из памяти.
        """
        return copy.copy(self.memory)

    def retrieve_relevant(self, relevance_target: str, top_k: int) -> list:
        """
        Извлекает топ-k значений из памяти, которые наиболее соответствуют заданной цели.

        Args:
            relevance_target (str): Цель соответствия.
            top_k (int): Количество релевантных значений для извлечения.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError("Подклассы должны реализовать этот метод.")

    def retrieve_first(self, n: int, include_omission_info: bool = True) -> list:
        """
        Извлекает первые `n` значений из памяти.

        Args:
            n (int): Количество первых значений для извлечения.
            include_omission_info (bool): Нужно ли включать информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Список первых `n` значений из памяти.
        """
        omission_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

        return self.memory[:n] + omission_info

    def retrieve_last(self, n: int, include_omission_info: bool = True) -> list:
        """
        Извлекает последние `n` значений из памяти.

        Args:
            n (int): Количество последних значений для извлечения.
            include_omission_info (bool): Нужно ли включать информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Список последних `n` значений из памяти.
        """
        omission_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

        return omission_info + self.memory[-n:]


@utils.post_init
class SemanticMemory(TinyMemory):
    """
    В когнитивной психологии семантическая память - это память о значениях, понимании и других знаниях, основанных на концепциях, не связанных с конкретным
    опытом. Она не упорядочена во времени и не связана с запоминанием конкретных событий или эпизодов. Этот класс предоставляет простую реализацию
    семантической памяти, где агент может хранить и извлекать семантическую информацию.
    """

    serializable_attrs = ["memories"]

    def __init__(self, memories: Optional[List[dict]] = None) -> None:
        """
        Инициализирует семантическую память.

        Args:
            memories (Optional[List[dict]]): Список воспоминаний. По умолчанию None.
        """
        self.memories: list = memories or []

        # @post_init гарантирует, что _post_init будет вызван после метода __init__

    def _post_init(self) -> None:
        """
        Этот метод будет запущен после __init__, так как у класса есть декоратор @post_init.
        Удобно разделять некоторые процессы инициализации, чтобы упростить десериализацию.
        """

        if not hasattr(self, 'memories') or self.memories is None:
            self.memories = []

        self.semantic_grounding_connector = BaseSemanticGroundingConnector("Semantic Memory Storage")
        self.semantic_grounding_connector.add_documents(self._build_documents_from(self.memories))

    def _preprocess_value_for_storage(self, value: dict) -> Any:
        """
        Предобрабатывает значение перед сохранением в семантическую память.

        Args:
            value (dict): Значение для предобработки.

        Returns:
            Any: Предобработанное значение.
        """
        engram: str | None = None

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
        Сохраняет значение в семантическую память.

        Args:
            value (Any): Значение для сохранения.
        """
        engram_doc = self._build_document_from(self._preprocess_value_for_storage(value))
        self.semantic_grounding_connector.add_document(engram_doc)

    def retrieve_relevant(self, relevance_target: str, top_k: int = 20) -> list:
        """
        Извлекает все значения из памяти, которые соответствуют заданной цели.

        Args:
            relevance_target (str): Цель соответствия.
            top_k (int): Количество релевантных значений для извлечения. По умолчанию 20.

        Returns:
            list: Список релевантных значений.
        """
        return self.semantic_grounding_connector.retrieve_relevant(relevance_target, top_k)

    #####################################
    # Auxiliary compatibility methods
    #####################################

    def _build_document_from(self, memory: Any) -> Document:
        """
        Строит документ из записи памяти.

        Args:
            memory (Any): Запись памяти.

        Returns:
            Document: Документ.
        """
        # TODO: добавить любые метаданные?
        return Document(text=str(memory))

    def _build_documents_from(self, memories: list) -> list:
        """
        Строит список документов из списка записей памяти.

        Args:
            memories (list): Список записей памяти.

        Returns:
            list: Список документов.
        """
        return [self._build_document_from(memory) for memory in memories]