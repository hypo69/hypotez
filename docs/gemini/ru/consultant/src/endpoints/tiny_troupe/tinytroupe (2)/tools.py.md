### **Анализ кода модуля `tools.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на классы, что обеспечивает определенную структуру и упрощает поддержку.
    - Использование `logger` для логирования.
    - Наличие базовой структуры для инструментов (`TinyTool`).
- **Минусы**:
    - Отсутствуют аннотации типов для параметров функций и переменных.
    - Не все docstring заполнены согласно требованиям.
    - В коде используются двойные кавычки вместо одинарных.
    - В блоках `try-except` используется `e` вместо `ex` для исключений.
    - Не все TODO комментарии актуальны и требуют пересмотра.
    - Смешанный стиль форматирования строк (использование тройных кавычек и `textwrap.dedent`).

#### **Рекомендации по улучшению**:

1. **Добавить аннотации типов**:
   - Для всех параметров функций и переменных необходимо добавить аннотации типов.

2. **Улучшить документацию**:
   - Дополнить docstring для всех классов и методов, указав параметры, возвращаемые значения и возможные исключения.
   - Перевести все комментарии и docstring на русский язык.
   - Исправить docstring в соответствии с заданным форматом.

3. **Исправить стиль кавычек**:
   - Заменить двойные кавычки на одинарные во всем коде.

4. **Обновить блоки `try-except`**:
   - Использовать `ex` вместо `e` в блоках обработки исключений.
   - Добавить логирование ошибок с использованием `logger.error` и передачей исключения как аргумента.

5. **Пересмотреть TODO комментарии**:
   - Оценить актуальность всех TODO комментариев и либо выполнить соответствующие задачи, либо удалить устаревшие комментарии.

6. **Унифицировать форматирование строк**:
   - Привести все многострочные строки к единому стилю (либо тройные кавычки, либо `textwrap.dedent`).

7. **Использовать `j_loads` или `j_loads_ns` для JSON**:
   - Если в коде происходит чтение JSON-файлов, заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.

8. **webdriver**:
    - Убедиться, что вебдрайвер импортируется и используется правильно, с учетом предоставленных инструкций.

#### **Оптимизированный код**:

```python
"""
Модуль для работы с инструментами агентов
=========================================

Модуль содержит классы для определения и управления инструментами, которые агенты могут использовать для выполнения задач.
Включает базовый класс `TinyTool` и его подклассы, такие как `TinyCalendar` и `TinyWordProcessor`.
"""

import textwrap
import json
import copy
from typing import Optional, Dict, List

import logging
from src.logger import logger  # Используем logger из src.logger

import tinytroupe.utils as utils
from tinytroupe.extraction import ArtifactExporter
from tinytroupe.enrichment import TinyEnricher
from tinytroupe.utils import JsonSerializableRegistry


class TinyTool(JsonSerializableRegistry):
    """
    Базовый класс для инструментов, используемых агентами.
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
        Инициализирует новый инструмент.

        Args:
            name (str): Имя инструмента.
            description (str): Краткое описание инструмента.
            owner (Optional[str], optional): Агент, владеющий инструментом. Если `None`, инструмент может использоваться любым агентом. По умолчанию `None`.
            real_world_side_effects (bool): Указывает, имеет ли инструмент реальные побочные эффекты. По умолчанию `False`.
            exporter (Optional[ArtifactExporter], optional): Экспортер для экспорта результатов действий инструмента. По умолчанию `None`.
            enricher (Optional[TinyEnricher], optional): Обогатитель для обогащения результатов действий инструмента. По умолчанию `None`.
        """
        self.name = name
        self.description = description
        self.owner = owner
        self.real_world_side_effects = real_world_side_effects
        self.exporter = exporter
        self.enricher = enricher

    def _process_action(self, agent, action: Dict) -> bool:
        """
        Обрабатывает действие, выполненное агентом с использованием этого инструмента.

        Args:
            agent: Агент, выполняющий действие.
            action (dict): Словарь, описывающий действие.

        Returns:
            bool: `True`, если действие было успешно обработано, иначе `False`.

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
                f'!!!!!!!!!! Tool {self.name} has REAL-WORLD SIDE EFFECTS. This is NOT just a simulation. Use with caution. !!!!!!!!!!'
            )

    def _enforce_ownership(self, agent) -> None:
        """
        Проверяет, имеет ли агент право на использование инструмента.

        Args:
            agent: Агент, пытающийся использовать инструмент.

        Raises:
            ValueError: Если агент не является владельцем инструмента.
        """
        if self.owner is not None and agent.name != self.owner.name:
            raise ValueError(
                f'Agent {agent.name} does not own tool {self.name}, which is owned by {self.owner.name}.'
            )

    def set_owner(self, owner) -> None:
        """
        Устанавливает владельца инструмента.

        Args:
            owner: Новый владелец инструмента.
        """
        self.owner = owner

    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt с определениями возможных действий инструмента.

        Returns:
            str: Prompt с определениями действий.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt с ограничениями на действия инструмента.

        Returns:
            str: Prompt с ограничениями на действия.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def process_action(self, agent, action: Dict) -> None:
        """
        Выполняет действие с использованием инструмента.

        Args:
            agent: Агент, выполняющий действие.
            action (dict): Словарь, описывающий действие.
        """
        self._protect_real_world()
        self._enforce_ownership(agent)
        self._process_action(agent, action)


# TODO under development
class TinyCalendar(TinyTool):
    """
    Инструмент календаря для агентов.
    """

    def __init__(self, owner: Optional[str] = None) -> None:
        """
        Инициализирует инструмент календаря.

        Args:
            owner (Optional[str], optional): Владелец календаря. По умолчанию `None`.
        """
        super().__init__(
            'calendar',
            'A basic calendar tool that allows agents to keep track meetings and appointments.',
            owner=owner,
            real_world_side_effects=False,
        )

        # maps date to list of events. Each event itself is a dictionary with keys "title", "description", "owner", "mandatory_attendees", "optional_attendees", "start_time", "end_time"
        self.calendar: Dict = {}

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
            description (Optional[str], optional): Описание события. По умолчанию `None`.
            owner (Optional[str], optional): Владелец события. По умолчанию `None`.
            mandatory_attendees (Optional[List[str]], optional): Список обязательных участников. По умолчанию `None`.
            optional_attendees (Optional[List[str]], optional): Список необязательных участников. По умолчанию `None`.
            start_time (Optional[str], optional): Время начала события. По умолчанию `None`.
            end_time (Optional[str], optional): Время окончания события. По умолчанию `None`.
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
            hour (Optional[int], optional): Час. По умолчанию `None`.
            minute (Optional[int], optional): Минута. По умолчанию `None`.
        """
        # TODO
        pass

    def _process_action(self, agent, action: Dict) -> bool:
        """
        Обрабатывает действие, связанное с календарем.

        Args:
            agent: Агент, выполняющий действие.
            action (dict): Словарь, описывающий действие.

        Returns:
            bool: `True`, если действие было успешно обработано, иначе `False`.
        """
        if action['type'] == 'CREATE_EVENT' and action['content'] is not None:
            # parse content json
            event_content = json.loads(action['content'])

            # checks whether there are any kwargs that are not valid
            valid_keys = [
                'title',
                'description',
                'mandatory_attendees',
                'optional_attendees',
                'start_time',
                'end_time',
            ]
            utils.check_valid_fields(event_content, valid_keys)

            # uses the kwargs to create a new event
            self.add_event(event_content)

            return True

        else:
            return False

    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt с определениями возможных действий для календаря.

        Returns:
            str: Prompt с определениями действий.
        """
        prompt = """
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
        Возвращает prompt с ограничениями на действия для календаря.

        Returns:
            str: Prompt с ограничениями на действия.
        """
        prompt = """
              
            """
        # TODO

        return textwrap.dedent(prompt)


class TinyWordProcessor(TinyTool):
    """
    Инструмент текстового процессора для агентов.
    """

    def __init__(
        self,
        owner: Optional[str] = None,
        exporter: Optional[ArtifactExporter] = None,
        enricher: Optional[TinyEnricher] = None,
    ) -> None:
        """
        Инициализирует инструмент текстового процессора.

        Args:
            owner (Optional[str], optional): Владелец текстового процессора. По умолчанию `None`.
            exporter (Optional[ArtifactExporter], optional): Экспортер для экспорта документов. По умолчанию `None`.
            enricher (Optional[TinyEnricher], optional): Обогатитель контента. По умолчанию `None`.
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
            author (Optional[str], optional): Автор документа. По умолчанию `None`.
        """
        logger.debug(f'Writing document with title {title} and content: {content}')

        if self.enricher is not None:
            requirements = """
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

            json_doc = {'title': title, 'content': content, 'author': author}
            self.exporter.export(
                artifact_name=f'{title}.{author}',
                artifact_data=json_doc,
                content_type='Document',
                content_format='md',
                target_format='json',
            )

    def _process_action(self, agent, action: Dict) -> bool:
        """
        Обрабатывает действие, связанное с текстовым процессором.

        Args:
            agent: Агент, выполняющий действие.
            action (dict): Словарь, описывающий действие.

        Returns:
            bool: `True`, если действие было успешно обработано, иначе `False`.
        """
        try:
            if action['type'] == 'WRITE_DOCUMENT' and action['content'] is not None:
                # parse content json
                if isinstance(action['content'], str):
                    doc_spec = json.loads(action['content'])
                else:
                    doc_spec = action['content']

                # checks whether there are any kwargs that are not valid
                valid_keys = ['title', 'content', 'author']
                utils.check_valid_fields(doc_spec, valid_keys)

                # uses the kwargs to create a new document
                self.write_document(**doc_spec)

                return True

            else:
                return False
        except json.JSONDecodeError as ex:  # Исправлено: e -> ex
            logger.error(
                f'Error parsing JSON content: {ex}. Original content: {action["content"]}',
                ex,
                exc_info=True,
            )  # Добавлено логирование ошибки
            return False

    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt с определениями возможных действий для текстового процессора.

        Returns:
            str: Prompt с определениями действий.
        """
        prompt = """
            - WRITE_DOCUMENT: you can create a new document. The content of the document has many fields, and you should use a JSON format to specify them. Here are the possible fields:
                * title: The title of the document. Mandatory.
                * content: The actual content of the document. You **must** use Markdown to format this content. Mandatory.
                * author: The author of the document. You should put your own name. Optional.
            """
        return utils.dedent(prompt)

    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt с ограничениями на действия для текстового процессора.

        Returns:
            str: Prompt с ограничениями на действия.
        """
        prompt = """
            - Whenever you WRITE_DOCUMENT, you write all the content at once. Moreover, the content should be long and detailed, unless there's a good reason for it not to be.
            - When you WRITE_DOCUMENT, you follow these additional guidelines:
                * For any milestones or timelines mentioned, try mentioning specific owners or partner teams, unless there's a good reason not to do so.
            """
        return utils.dedent(prompt)