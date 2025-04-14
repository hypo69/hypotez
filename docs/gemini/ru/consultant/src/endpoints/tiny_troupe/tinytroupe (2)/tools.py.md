### **Анализ кода модуля `tools.py`**

**Описание:**
Модуль `tools.py` содержит классы инструментов (tools), которые агенты могут использовать для выполнения специализированных задач. Включает базовый класс `TinyTool` и его подклассы, такие как `TinyCalendar` и `TinyWordProcessor`.

**Расположение:**
Файл расположен в `hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/tools.py`. Это указывает на то, что модуль является частью подсистемы `tinytroupe`, возможно, связанной с управлением задачами и взаимодействием агентов.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура классов для инструментов.
    - Использование логирования для отслеживания работы инструментов.
    - Наличие базового класса `TinyTool`, который определяет интерфейс для всех инструментов.
    - Использование `ArtifactExporter` и `TinyEnricher` для расширения функциональности инструментов.
- **Минусы**:
    - Отсутствие аннотаций типов для переменных и параметров функций.
    - Не все методы имеют docstring.
    - Использование `logger = logging.getLogger("tinytroupe")` вместо `from src.logger import logger`.
    - Смешанный стиль кавычек (использование как одинарных, так и двойных кавычек).
    - TODO комментарии, которые не были обработаны.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений.

2.  **Улучшить docstring**:
    - Добавить docstring для всех методов и классов, используя формат, описанный в инструкции.
    - Перевести docstring на русский язык.

3.  **Использовать `logger` из `src.logger`**:
    - Изменить способ инициализации логгера на `from src.logger import logger`.

4.  **Унифицировать стиль кавычек**:
    - Использовать только одинарные кавычки для строк.

5.  **Обработать TODO комментарии**:
    - Рассмотреть и обработать все TODO комментарии, либо удалить их, если они больше не актуальны.

6.  **Добавить обработку исключений**:
    - Добавить обработку исключений, где это необходимо, и использовать `logger.error` для логирования ошибок.

7.  **Улучшить структуру `TinyCalendar`**:
    - В `TinyCalendar` заменить `self.calenar` на `self.calendar` (очепятка).

8.  **Использовать `j_loads`**:
    - Использовать `j_loads` или `j_loads_ns` для чтения JSON.

**Оптимизированный код:**

```python
"""
Модуль инструментов для агентов TinyTroupe
==========================================

Модуль содержит классы инструментов, которые агенты могут использовать для выполнения специализированных задач.
Включает базовый класс :class:`TinyTool` и его подклассы, такие как :class:`TinyCalendar` и :class:`TinyWordProcessor`.
"""
import textwrap
import json
import copy
from typing import Optional, Dict, Any, List

from src.logger import logger  # Используем logger из src.logger
import tinytroupe.utils as utils
from tinytroupe.extraction import ArtifactExporter
from tinytroupe.enrichment import TinyEnricher
from tinytroupe.utils import JsonSerializableRegistry
from pathlib import Path


class TinyTool(JsonSerializableRegistry):
    """
    Базовый класс для инструментов агентов.

    Args:
        name (str): Название инструмента.
        description (str): Краткое описание инструмента.
        owner (Optional[str]): Агент, владеющий инструментом. Если `None`, инструмент может использоваться любым агентом.
        real_world_side_effects (bool): Указывает, имеет ли инструмент реальные побочные эффекты.
        exporter (Optional[ArtifactExporter]): Экспортер для результатов работы инструмента. Если `None`, экспорт результатов невозможен.
        enricher (Optional[TinyEnricher]): Обогатитель для результатов работы инструмента. Если `None`, обогащение результатов невозможно.
    """

    def __init__(
        self,
        name: str,
        description: str,
        owner: Optional[str] = None,
        real_world_side_effects: bool = False,
        exporter: Optional[ArtifactExporter] = None,
        enricher: Optional[TinyEnricher] = None,
    ) -> None:
        """
        Инициализация нового инструмента.

        Args:
            name (str): Название инструмента.
            description (str): Краткое описание инструмента.
            owner (Optional[str]): Агент, владеющий инструментом. Если `None`, инструмент может использоваться любым агентом.
            real_world_side_effects (bool): Указывает, имеет ли инструмент реальные побочные эффекты.
            exporter (Optional[ArtifactExporter]): Экспортер для результатов работы инструмента. Если `None`, экспорт результатов невозможен.
            enricher (Optional[TinyEnricher]): Обогатитель для результатов работы инструмента. Если `None`, обогащение результатов невозможно.
        """
        self.name: str = name
        self.description: str = description
        self.owner: Optional[str] = owner
        self.real_world_side_effects: bool = real_world_side_effects
        self.exporter: Optional[ArtifactExporter] = exporter
        self.enricher: Optional[TinyEnricher] = enricher

    def _process_action(self, agent: str, action: Dict[str, Any]) -> bool:
        """
        Обрабатывает действие, выполняемое агентом.

        Args:
            agent (str): Агент, выполняющий действие.
            action (Dict[str, Any]): Словарь, представляющий действие.

        Returns:
            bool: `True`, если действие было успешно обработано, `False` в противном случае.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def _protect_real_world(self) -> None:
        """
        Предупреждает об использовании инструмента с реальными побочными эффектами.
        """
        if self.real_world_side_effects:
            logger.warning(
                f' !!!!!!!!!! Tool {self.name} has REAL-WORLD SIDE EFFECTS. This is NOT just a simulation. Use with caution. !!!!!!!!!!'
            )

    def _enforce_ownership(self, agent: str) -> None:
        """
        Проверяет, имеет ли агент право на использование инструмента.

        Args:
            agent (str): Агент, пытающийся использовать инструмент.

        Raises:
            ValueError: Если агент не является владельцем инструмента.
        """
        if self.owner is not None and agent.name != self.owner.name:
            raise ValueError(
                f'Agent {agent.name} does not own tool {self.name}, which is owned by {self.owner.name}.'
            )

    def set_owner(self, owner: str) -> None:
        """
        Устанавливает владельца инструмента.

        Args:
            owner (str): Новый владелец инструмента.
        """
        self.owner = owner

    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определений действий.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для ограничений действий.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def process_action(self, agent: str, action: Dict[str, Any]) -> None:
        """
        Обрабатывает действие агента с учетом защиты от реального мира и проверки владельца.

        Args:
            agent (str): Агент, выполняющий действие.
            action (Dict[str, Any]): Словарь, представляющий действие.
        """
        self._protect_real_world()
        self._enforce_ownership(agent)
        self._process_action(agent, action)


# TODO under development
class TinyCalendar(TinyTool):
    """
    Инструмент календаря для агентов.

    Args:
        owner (Optional[str]): Владелец календаря.
    """

    def __init__(self, owner: Optional[str] = None) -> None:
        """
        Инициализация календаря.

        Args:
            owner (Optional[str]): Владелец календаря.
        """
        super().__init__(
            'calendar',
            'A basic calendar tool that allows agents to keep track meetings and appointments.',
            owner=owner,
            real_world_side_effects=False,
        )

        # maps date to list of events. Each event itself is a dictionary with keys "title", "description", "owner", "mandatory_attendees", "optional_attendees", "start_time", "end_time"
        self.calendar: Dict[str, List[Dict[str, Any]]] = {}

    def add_event(
        self,
        date: str,
        title: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        mandatory_attendees: Optional[List[str]] = None,
        optional_attendees: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> None:
        """
        Добавляет событие в календарь.

        Args:
            date (str): Дата события.
            title (str): Название события.
            description (Optional[str]): Описание события.
            owner (Optional[str]): Владелец события.
            mandatory_attendees (Optional[List[str]]): Список обязательных участников.
            optional_attendees (Optional[List[str]]): Список необязательных участников.
            start_time (Optional[str]): Время начала события.
            end_time (Optional[str]): Время окончания события.
        """
        if date not in self.calendar:
            self.calendar[date] = []
        self.calendar[date].append(
            {
                'title': title,
                'description': description,
                'owner': owner,
                'mandatory_attendees': mandatory_attendees,
                'optional_attendees': optional_attendees,
                'start_time': start_time,
                'end_time': end_time,
            }
        )

    def find_events(
        self,
        year: int,
        month: int,
        day: int,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
    ) -> None:
        """
        Ищет события в календаре.

        Args:
            year (int): Год.
            month (int): Месяц.
            day (int): День.
            hour (Optional[int]): Час.
            minute (Optional[int]): Минута.
        """
        # TODO
        pass

    def _process_action(self, agent: str, action: Dict[str, Any]) -> bool:
        """
        Обрабатывает действие, связанное с календарем.

        Args:
            agent (str): Агент, выполняющий действие.
            action (Dict[str, Any]): Словарь, представляющий действие.

        Returns:
            bool: `True`, если действие было успешно обработано, `False` в противном случае.
        """
        if action['type'] == 'CREATE_EVENT' and action['content'] is not None:
            # parse content json
            try:
                event_content: Dict[str, Any] = json.loads(action['content'])

                # checks whether there are any kwargs that are not valid
                valid_keys: List[str] = [
                    'title',
                    'description',
                    'mandatory_attendees',
                    'optional_attendees',
                    'start_time',
                    'end_time',
                ]
                utils.check_valid_fields(event_content, valid_keys)

                # uses the kwargs to create a new event
                self.add_event(**event_content)

                return True
            except json.JSONDecodeError as ex:
                logger.error(
                    'Ошибка при разборе JSON контента', ex, exc_info=True
                )  # Логируем ошибку
                return False

        else:
            return False

    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определений действий календаря.

        Returns:
            str: Prompt для определений действий.
        """
        prompt: str = """
              - CREATE_EVENT: You can create a new event in your calendar. The content of the event has many fields, and you should use a JSON format to specify them. Here are the possible fields:
                * title: The title of the event. Mandatory.
                * description: A brief description of the event. Optional.
                * mandatory_attendees: A list of agent names who must attend the event. Optional.
                * optional_attendees: A list of agent names who are invited to the event, but are not required to attend. Optional.
                * start_time: The start time of the event. Optional.
                * end_time: The end time of the event. Optional.
            """
        # TODO how the atendee list will be handled? How will they be notified of the invitation? I guess they must also have a calendar themselves. <-------------------------------------

        return utils.dedent(prompt)

    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для ограничений действий календаря.

        Returns:
            str: Prompt для ограничений действий.
        """
        prompt: str = """
              
            """
        # TODO

        return textwrap.dedent(prompt)


class TinyWordProcessor(TinyTool):
    """
    Инструмент текстового процессора для агентов.

    Args:
        owner (Optional[str]): Владелец текстового процессора.
        exporter (Optional[ArtifactExporter]): Экспортер для сохранения документов.
        enricher (Optional[TinyEnricher]): Обогатитель контента документов.
    """

    def __init__(
        self,
        owner: Optional[str] = None,
        exporter: Optional[ArtifactExporter] = None,
        enricher: Optional[TinyEnricher] = None,
    ) -> None:
        """
        Инициализация текстового процессора.

        Args:
            owner (Optional[str]): Владелец текстового процессора.
            exporter (Optional[ArtifactExporter]): Экспортер для сохранения документов.
            enricher (Optional[TinyEnricher]): Обогатитель контента документов.
        """
        super().__init__(
            'wordprocessor',
            'A basic word processor tool that allows agents to write documents.',
            owner=owner,
            real_world_side_effects=False,
            exporter=exporter,
            enricher=enricher,
        )

    def write_document(self, title: str, content: str, author: Optional[str] = None) -> None:
        """
        Создает и сохраняет документ.

        Args:
            title (str): Название документа.
            content (str): Содержание документа.
            author (Optional[str]): Автор документа.
        """
        logger.debug(f'Writing document with title {title} and content: {content}')

        if self.enricher is not None:
            requirements: str = """
            Turn any draft or outline into an actual and long document, with many, many details. Include tables, lists, and other elements.
            The result **MUST** be at least 5 times larger than the original content in terms of characters - do whatever it takes to make it this long and detailed.
            """

            content = self.enricher.enrich_content(
                requirements=requirements,
                content=content,
                content_type='Document',
                context_info=None,
                context_cache=None,
                verbose=False,
            )

        if self.exporter is not None:
            self.exporter.export(
                artifact_name=f'{title}.{author}',
                artifact_data=content,
                content_type='Document',
                content_format='md',
                target_format='md',
            )
            self.exporter.export(
                artifact_name=f'{title}.{author}',
                artifact_data=content,
                content_type='Document',
                content_format='md',
                target_format='docx',
            )

            json_doc: Dict[str, Any] = {'title': title, 'content': content, 'author': author}
            self.exporter.export(
                artifact_name=f'{title}.{author}',
                artifact_data=json_doc,
                content_type='Document',
                content_format='md',
                target_format='json',
            )

    def _process_action(self, agent: str, action: Dict[str, Any]) -> bool:
        """
        Обрабатывает действие, связанное с текстовым процессором.

        Args:
            agent (str): Агент, выполняющий действие.
            action (Dict[str, Any]): Словарь, представляющий действие.

        Returns:
            bool: `True`, если действие было успешно обработано, `False` в противном случае.
        """
        try:
            if action['type'] == 'WRITE_DOCUMENT' and action['content'] is not None:
                # parse content json
                doc_spec: Dict[str, Any]
                if isinstance(action['content'], str):
                    doc_spec = json.loads(action['content'])
                else:
                    doc_spec = action['content']

                # checks whether there are any kwargs that are not valid
                valid_keys: List[str] = ['title', 'content', 'author']
                utils.check_valid_fields(doc_spec, valid_keys)

                # uses the kwargs to create a new document
                self.write_document(**doc_spec)

                return True

            else:
                return False
        except json.JSONDecodeError as ex:
            logger.error(
                f'Error parsing JSON content: {ex}. Original content: {action["content"]}',
                ex,
                exc_info=True,
            )
            return False

    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определений действий текстового процессора.

        Returns:
            str: Prompt для определений действий.
        """
        prompt: str = """
            - WRITE_DOCUMENT: you can create a new document. The content of the document has many fields, and you should use a JSON format to specify them. Here are the possible fields:
                * title: The title of the document. Mandatory.
                * content: The actual content of the document. You **must** use Markdown to format this content. Mandatory.
                * author: The author of the document. You should put your own name. Optional.
            """
        return utils.dedent(prompt)

    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для ограничений действий текстового процессора.

        Returns:
            str: Prompt для ограничений действий.
        """
        prompt: str = """
            - Whenever you WRITE_DOCUMENT, you write all the content at once. Moreover, the content should be long and detailed, unless there\'s a good reason for it not to be.
            - When you WRITE_DOCUMENT, you follow these additional guidelines:
                * For any milestones or timelines mentioned, try mentioning specific owners or partner teams, unless there\'s a good reason not to do so.
            """
        return utils.dedent(prompt)