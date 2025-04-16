### **Анализ кода модуля `mental_faculty.py`**

**Расположение файла в проекте:** `hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/agent/mental_faculty.py`

**Назначение модуля:** Модуль определяет основные классы для представления и управления ментальными способностями агентов в системе TinyTroupe. Он включает абстрактный базовый класс `TinyMentalFaculty`, а также его реализации: `CustomMentalFaculty`, `RecallFaculty`, `FilesAndWebGroundingFaculty` и `TinyToolUse`.

**Связь с другими модулями:**
- Модуль использует классы `LocalFilesGroundingConnector` и `WebPagesGroundingConnector` из модуля `tinytroupe.agent.grounding`.
- Использует `JsonSerializableRegistry` из `tinytroupe.utils`.
- Использует модуль логирования `src.logger`.

**Основные компоненты:**

- **`TinyMentalFaculty`**: Абстрактный базовый класс для всех ментальных способностей. Определяет основные методы, такие как `process_action`, `actions_definitions_prompt` и `actions_constraints_prompt`, которые должны быть реализованы в подклассах.
- **`CustomMentalFaculty`**: Представляет настраиваемую ментальную способность, определяемую пользователем через конфигурацию действий и ограничений.
- **`RecallFaculty`**: Реализует способность агента извлекать информацию из памяти.
- **`FilesAndWebGroundingFaculty`**: Обеспечивает агенту доступ к локальным файлам и веб-страницам.
- **`TinyToolUse`**: Позволяет агенту использовать инструменты для выполнения задач.

## Качество кода:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура классов, абстрактный базовый класс и его реализации.
    - Использование `textwrap.dedent` для улучшения читаемости многострочных строк.
    - Наличие docstring для классов и методов.
- **Минусы**:
    - Некоторые docstring отсутствуют или неполные.
    - Отсутствуют аннотации типов для некоторых переменных.
    - Не везде используется модуль `logger` для логирования.

## Рекомендации по улучшению:

1.  **Документация**:
    *   Дополнить docstring для всех классов и методов, включая описание параметров, возвращаемых значений и возможных исключений.
    *   Перевести все docstring на русский язык.
    *   Добавить примеры использования для основных классов и методов.
2.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных, где они отсутствуют.
3.  **Логирование**:
    *   Использовать модуль `logger` для логирования важных событий и ошибок.
    *   Добавить логирование в методы `process_action` для отслеживания выполнения действий.
4.  **Обработка исключений**:
    *   Добавить обработку исключений в методы, где это необходимо.
    *   Использовать `logger.error` для логирования ошибок.
5.  **Форматирование**:
    *   Убедиться, что весь код соответствует стандартам PEP8.
6.  **Использование одинарных кавычек**:
    *   Привести все строки к использованию одинарных кавычек.

## Оптимизированный код:

```python
"""
Модуль для работы с ментальными способностями агента
=====================================================

Модуль содержит классы для представления и управления ментальными способностями агентов.
Он включает абстрактный базовый класс :class:`TinyMentalFaculty`, а также его реализации:
:class:`CustomMentalFaculty`, :class:`RecallFaculty`, :class:`FilesAndWebGroundingFaculty` и :class:`TinyToolUse`.

Пример использования
----------------------

>>> from tinytroupe.agent.mental_faculty import RecallFaculty
>>> recall_faculty = RecallFaculty()
>>> print(recall_faculty)
Mental Faculty: Memory Recall
"""

from tinytroupe.agent.grounding import LocalFilesGroundingConnector, WebPagesGroundingConnector
from tinytroupe.utils import JsonSerializableRegistry
import tinytroupe.utils as utils

import tinytroupe.agent as agent

from typing import Callable, Optional, Dict, List, Any
import textwrap  # to dedent strings

from src.logger import logger

#######################################################################################################################
# Mental faculties
#######################################################################################################################
    
class TinyMentalFaculty(JsonSerializableRegistry):
    """
    Представляет ментальную способность агента.
    Ментальные способности - это когнитивные способности, которыми обладает агент.
    """

    def __init__(self, name: str, requires_faculties: Optional[List[str]] = None) -> None:
        """
        Инициализирует ментальную способность.

        Args:
            name (str): Название ментальной способности.
            requires_faculties (Optional[List[str]]): Список ментальных способностей, необходимых для правильной работы этой способности.
               Формат: ["faculty1", "faculty2", ...]
        """
        self.name = name
        
        if requires_faculties is None:
            self.requires_faculties: List[str] = []
        else:
            self.requires_faculties: List[str] = requires_faculties

    def __str__(self) -> str:
        return f'Mental Faculty: {self.name}'
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, TinyMentalFaculty):
            return self.name == other.name
        return False
    
    def process_action(self, agent: 'agent.Agent', action: Dict[str, Any]) -> bool:
        """
        Обрабатывает действие, связанное с этой способностью.

        Args:
            agent (agent.Agent): Агент, выполняющий действие.
            action (Dict[str, Any]): Действие для обработки.

        Returns:
            bool: True, если действие было успешно обработано, False в противном случае.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')
    
    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения действий, связанных с этой способностью.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия, связанные с этой способностью.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Subclasses must implement this method.')


class CustomMentalFaculty(TinyMentalFaculty):
    """
    Представляет настраиваемую ментальную способность агента.
    Настраиваемые ментальные способности - это когнитивные способности,
    которые определяются пользователем путем указания действий, которые может выполнять способность,
    или ограничений, которые вводит способность. Ограничения могут быть связаны с действиями,
    которые может выполнять способность, или быть независимыми, более общими ограничениями,
    которым должен следовать агент.
    """

    def __init__(self, name: str, requires_faculties: Optional[List[str]] = None,
                 actions_configs: Optional[Dict[str, Dict[str, Any]]] = None, constraints: Optional[List[str]] = None) -> None:
        """
        Инициализирует настраиваемую ментальную способность.

        Args:
            name (str): Название ментальной способности.
            requires_faculties (Optional[List[str]]): Список ментальных способностей, необходимых для правильной работы этой способности.
              Формат: ["faculty1", "faculty2", ...]
            actions_configs (Optional[Dict[str, Dict[str, Any]]]): Словарь с конфигурацией действий, которые может выполнять эта способность.
              Формат: {<action_name>: {"description": <description>, "function": <function>}}
            constraints (Optional[List[str]]): Список с ограничениями, введенными этой способностью.
              Формат: [<constraint1>, <constraint2>, ...]
        """

        super().__init__(name, requires_faculties)

        # {<action_name>: {"description": <description>, "function": <function>}}
        if actions_configs is None:
            self.actions_configs: Dict[str, Dict[str, Any]] = {}
        else:
            self.actions_configs: Dict[str, Dict[str, Any]] = actions_configs
        
        # [<constraint1>, <constraint2>, ...]
        if constraints is None:
            self.constraints: List[str] = []
        else:
            self.constraints: List[str] = constraints
    
    def add_action(self, action_name: str, description: str, function: Optional[Callable] = None) -> None:
        """
        Добавляет действие к этой способности.

        Args:
            action_name (str): Название действия.
            description (str): Описание действия.
            function (Optional[Callable]): Функция, выполняющая действие.
        """
        self.actions_configs[action_name] = {'description': description, 'function': function}

    def add_actions(self, actions: Dict[str, Dict[str, Any]]) -> None:
        """
        Добавляет несколько действий к этой способности.

        Args:
            actions (Dict[str, Dict[str, Any]]): Словарь действий.
        """
        for action_name, action_config in actions.items():
            self.add_action(action_name, action_config['description'], action_config['function'])
    
    def add_action_constraint(self, constraint: str) -> None:
        """
        Добавляет ограничение на действие.

        Args:
            constraint (str): Ограничение.
        """
        self.constraints.append(constraint)
    
    def add_actions_constraints(self, constraints: List[str]) -> None:
        """
        Добавляет несколько ограничений на действия.

        Args:
            constraints (List[str]): Список ограничений.
        """
        for constraint in constraints:
            self.add_action_constraint(constraint)

    def process_action(self, agent: 'agent.Agent', action: Dict[str, Any]) -> bool:
        """
        Обрабатывает действие.

        Args:
            agent (agent.Agent): Агент, выполняющий действие.
            action (Dict[str, Any]): Действие для обработки.

        Returns:
            bool: True, если действие было успешно обработано, False в противном случае.
        """
        logger.debug(f'Processing action: {action}')

        action_type = action['type']
        if action_type in self.actions_configs:
            action_config = self.actions_configs[action_type]
            action_function = action_config.get('function', None)

            if action_function is not None:
                action_function(agent, action)
            
            # one way or another, the action was processed
            return True 
        
        else:
            return False
    
    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения действий.
        """
        prompt = ''
        for action_name, action_config in self.actions_configs.items():
            prompt += f'  - {action_name.upper()}: {action_config["description"]}\\n'
        
        return prompt

    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия.
        """
        prompt = ''
        for constraint in self.constraints:
            prompt += f'  - {constraint}\\n'
        
        return prompt


class RecallFaculty(TinyMentalFaculty):
    """
    Представляет способность агента извлекать информацию из памяти.
    """

    def __init__(self) -> None:
        """
        Инициализирует способность извлечения информации из памяти.
        """
        super().__init__('Memory Recall')
        

    def process_action(self, agent: 'agent.Agent', action: Dict[str, Any]) -> bool:
        """
        Обрабатывает действие извлечения информации из памяти.

        Args:
            agent (agent.Agent): Агент, выполняющий действие.
            action (Dict[str, Any]): Действие для обработки.

        Returns:
            bool: True, если действие было успешно обработано, False в противном случае.
        """
        logger.debug(f'Processing action: {action}')

        if action['type'] == 'RECALL' and action['content'] is not None:
            content = action['content']

            semantic_memories = agent.retrieve_relevant_memories(relevance_target=content)

            logger.info(f'Recalling information related to \'{content}\'. Found {len(semantic_memories)} relevant memories.')

            if len(semantic_memories) > 0:
                # a string with each element in the list in a new line starting with a bullet point
                agent.think('I have remembered the following information from my semantic memory and will use it to guide me in my subsequent actions: \\n' + \
                        '\\n'.join([f'  - {item}' for item in semantic_memories]))
            else:
                agent.think(f'I can\'t remember anything about \'{content}\'.')
            
            return True
        
        else:
            return False

    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения действия извлечения информации из памяти.
        """
        prompt = \
            """
              - RECALL: you can recall information from your memory. To do, you must specify a "mental query" to locate the desired memory. If the memory is found, it is brought to your conscience.
            """

        return textwrap.dedent(prompt)
    
    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действие извлечения информации из памяти.
        """
        prompt = \
          """
            - Before concluding you don\'t know something or don\'t have access to some information, you **must** try to RECALL it from your memory.
            - You try to RECALL information from your semantic/factual memory, so that you can have more relevant elements to think and talk about, whenever such an action would be likely
                to enrich the current interaction. To do so, you must specify able "mental query" that is related to the things you\'ve been thinking, listening and talking about.
                Example:
                ```
                <THINK A>
                <RECALL B, which is something related to A>
                <THINK about A and B>
                <TALK about A and B>
                DONE
                ```
            - If you RECALL:
                * you use a "mental query" that describe the elements you are looking for, you do not use a question. It is like a keyword-based search query.
                For example, instead of "What are the symptoms of COVID-19?", you would use "COVID-19 symptoms".
                * you use keywords likely to be found in the text you are looking for. For example, instead of "Brazil economic outlook", you would use "Brazil economy", "Brazil GPD", "Brazil inflation", etc.
            - It may take several tries of RECALL to get the relevant information you need. If you don\'t find what you are looking for, you can try again with a **very** different "mental query".
                Be creative: you can use synonyms, related concepts, or any other strategy you think might help you to find the information you need. Avoid using the same terms in different queries, as it is likely to return the same results. Whenever necessary, you should retry RECALL a couple of times before giving up the location of more information.
                Example:
                ```
                <THINK something>
                <RECALL "cat products">
                <THINK something>
                <RECALL "feline artifacts">
                <THINK something>
                <RECALL "pet store">
                <THINK something>
                <TALK something>
                DONE
                ```
            - You **may** interleave THINK and RECALL so that you can better reflect on the information you are trying to recall.
            - If you need information about a specific document, you **must** use CONSULT instead of RECALL. This is because RECALL **does not** allow you to select the specific document, and only brings small 
                relevant parts of variious documents - while CONSULT brings the precise document requested for your inspection, with its full content. 
                Example:
                ```
                LIST_DOCUMENTS
                <CONSULT some document name>
                <THINK something about the retrieved document>
                <TALK something>
                DONE
                ``` 
          """

        return textwrap.dedent(prompt)
    

class FilesAndWebGroundingFaculty(TinyMentalFaculty):
    """
    Позволяет агенту получать доступ к локальным файлам и веб-страницам для обоснования своих знаний.
    """


    def __init__(self, folders_paths: Optional[List[str]] = None, web_urls: Optional[List[str]] = None) -> None:
        """
        Инициализирует способность доступа к файлам и веб-страницам.

        Args:
            folders_paths (Optional[List[str]]): Список путей к локальным папкам.
            web_urls (Optional[List[str]]): Список URL-адресов веб-страниц.
        """
        super().__init__('Local Files and Web Grounding')

        self.local_files_grounding_connector: LocalFilesGroundingConnector = LocalFilesGroundingConnector(folders_paths=folders_paths)
        self.web_grounding_connector: WebPagesGroundingConnector = WebPagesGroundingConnector(web_urls=web_urls)

    def process_action(self, agent: 'agent.Agent', action: Dict[str, Any]) -> bool:
        """
        Обрабатывает действие, связанное с доступом к файлам и веб-страницам.

        Args:
            agent (agent.Agent): Агент, выполняющий действие.
            action (Dict[str, Any]): Действие для обработки.

        Returns:
            bool: True, если действие было успешно обработано, False в противном случае.
        """
        if action['type'] == 'CONSULT' and action['content'] is not None:
            target_name = action['content']

            results: List[str] = []
            results.append(self.local_files_grounding_connector.retrieve_by_name(target_name))
            results.append(self.web_grounding_connector.retrieve_by_name(target_name))

            if len(results) > 0:
                agent.think(f'I have read the following document: \\n{results}')
            else:
                agent.think(f'I can\'t find any document with the name \'{target_name}\'.')
            
            return True
        
        elif action['type'] == 'LIST_DOCUMENTS' and action['content'] is not None:
            available_names: List[str] = []
            available_names += self.local_files_grounding_connector.list_sources()
            available_names += self.web_grounding_connector.list_sources()

            if len(available_names) > 0:
                agent.think(f'I have the following documents available to me: {available_names}')
            else:
                agent.think(f'I don\'t have any documents available for inspection.')
            
            return True

        else:
            return False


    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения действий, связанных с доступом к файлам и веб-страницам.
        """
        prompt = \
            """
            - LIST_DOCUMENTS: you can list the names of the documents you have access to, so that you can decide which to access, if any, to accomplish your goals. Documents is a generic term and includes any 
                kind of "packaged" information you can access, such as emails, files, chat messages, calendar events, etc. It also includes, in particular, web pages.
                The order of in which the documents are listed is not relevant.
            - CONSULT: you can retrieve and consult a specific document, so that you can access its content and accomplish your goals. To do so, you specify the name of the document you want to consult.
            """

        return textwrap.dedent(prompt)
    
    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия, связанные с доступом к файлам и веб-страницам.
        """
        prompt = \
          """
            - You are aware that you have documents available to you to help in your tasks. Even if you already have knowledge about a topic, you 
              should believe that the documents can provide you with additional information that can be useful to you.
            - If you want information that might be in documents, you first LIST_DOCUMENTS to see what is available and decide if you want to access any of them.
            - You LIST_DOCUMENTS when you suspect that relevant information might be in some document, but you are not sure which one.
            - You only CONSULT the relevant documents for your present goals and context. You should **not** CONSULT documents that are not relevant to the current situation.
              You use the name of the document to determine its relevance before accessing it.
            - If you need information about a specific document, you **must** use CONSULT instead of RECALL. This is because RECALL **does not** allow you to select the specific document, and only brings small 
                relevant parts of variious documents - while CONSULT brings the precise document requested for your inspection, with its full content. 
                Example:
                ```
                LIST_DOCUMENTS
                <CONSULT some document name>
                <THINK something about the retrieved document>
                <TALK something>
                DONE
                ``` 
            - If you need information from specific documents, you **always** CONSULT it, **never** RECALL it.   
            - You can only CONSULT few documents before issuing DONE. 
                Example:
                ```
                <CONSULT some document name>
                <THINK something about the retrieved document>
                <TALK something>
                <CONSULT some document name>
                <THINK something about the retrieved document>
                <TALK something>
                DONE
                ```
            - When deciding whether to use RECALL or CONSULT, you should consider whether you are looking for any information about some topic (use RECALL) or if you are looking for information from
                specific documents (use CONSULT). To know if you have potentially relevant documents available, use LIST_DOCUMENTS first.
          """

        return textwrap.dedent(prompt)
    
    
class TinyToolUse(TinyMentalFaculty):
    """
    Позволяет агенту использовать инструменты для выполнения задач.
    Использование инструментов - один из важнейших когнитивных навыков,
    которым обладают люди и приматы, как мы знаем.
    """

    def __init__(self, tools: List['agent.Agent']) -> None:
        """
        Инициализирует способность использования инструментов.

        Args:
            tools (List[agent.Agent]): Список инструментов, доступных агенту.
        """
        super().__init__('Tool Use')
    
        self.tools: List['agent.Agent'] = tools
    
    def process_action(self, agent: 'agent.Agent', action: Dict[str, Any]) -> bool:
        """
        Обрабатывает действие, связанное с использованием инструментов.

        Args:
            agent (agent.Agent): Агент, выполняющий действие.
            action (Dict[str, Any]): Действие для обработки.

        Returns:
            bool: True, если действие было успешно обработано, False в противном случае.
        """
        for tool in self.tools:
            if tool.process_action(agent, action):
                return True
        
        return False
    
    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения действий, связанных с использованием инструментов.
        """
        # each tool should provide its own actions definitions prompt
        prompt = ''
        for tool in self.tools:
            prompt += tool.actions_definitions_prompt()
        
        return prompt
    
    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия, связанные с использованием инструментов.
        """
        # each tool should provide its own actions constraints prompt
        prompt = ''
        for tool in self.tools:
            prompt += tool.actions_constraints_prompt()
        
        return prompt