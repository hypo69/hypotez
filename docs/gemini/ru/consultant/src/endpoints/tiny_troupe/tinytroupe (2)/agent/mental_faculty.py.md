### **Анализ кода модуля `mental_faculty.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура классов, использование наследования для реализации различных типов ментальных способностей.
    - Использование `textwrap.dedent` для улучшения читаемости многострочных строк.
    - Наличие базовой структуры для расширения функциональности агента через добавление новых ментальных способностей.
- **Минусы**:
    - Отсутствие логирования в некоторых методах, что затрудняет отладку и мониторинг.
    - Не все переменные аннотированы типами.
    - Docstring'и не всегда полные и не соответствуют стандарту оформления.

**Рекомендации по улучшению:**

1.  **Добавить логирование**:
    - В методы `__init__` всех классов добавить логирование для отслеживания процесса инициализации.
    - В методы `process_action` добавить логирование для записи действий и их результатов.
    - Логировать важные события, такие как добавление действий и ограничений в `CustomMentalFaculty`.

2.  **Улучшить документацию**:
    - Привести все docstring к единому стандарту, включая описание аргументов, возвращаемых значений и возможных исключений.
    - Добавить примеры использования для наиболее важных классов и методов.
    - Описать назначение каждого класса и метода более подробно.

3.  **Добавить аннотации типов**:
    - Указать типы для всех переменных в методах `__init__`.
    - Убедиться, что все аргументы и возвращаемые значения функций аннотированы типами.

4.  **Обработка исключений**:
    - Добавить обработку исключений в методах `process_action` для более надежной работы.

5.  **Использовать константы для строковых значений**:
    - Заменить строковые литералы, такие как `'type'`, `'content'`, на константы для уменьшения вероятности опечаток и улучшения читаемости.

6.  **Пересмотреть использование словарей для хранения ограничений**:
    - Использование списка для хранения ограничений может быть неэффективным. Рассмотреть возможность использования множества (set) или словаря, если требуется дополнительная информация о каждом ограничении.

**Оптимизированный код:**

```python
"""
Модуль для представления ментальных способностей агента.
========================================================

Модуль содержит классы для определения и управления ментальными способностями агента,
такие как память, доступ к файлам и использование инструментов.

Пример использования:
----------------------

>>> faculty = RecallFaculty()
>>> print(faculty)
Mental Faculty: Memory Recall
"""
from tinytroupe.agent.grounding import LocalFilesGroundingConnector, WebPagesGroundingConnector
from tinytroupe.utils import JsonSerializableRegistry
import tinytroupe.utils as utils
from src.logger import logger # подключение модуля логгирования
import tinytroupe.agent as agent

from typing import Callable, List, Dict, Any, Optional
import textwrap  # to dedent strings

#######################################################################################################################
# Mental faculties
#######################################################################################################################
    
class TinyMentalFaculty(JsonSerializableRegistry):
    """
    Представляет ментальную способность агента.

    Ментальные способности - это когнитивные навыки, которыми обладает агент.
    """

    def __init__(self, name: str, requires_faculties: Optional[List[str]] = None) -> None:
        """
        Инициализирует ментальную способность.

        Args:
            name (str): Название ментальной способности.
            requires_faculties (Optional[List[str]]): Список ментальных способностей, необходимых для правильной работы этой способности. По умолчанию `None`.
        """
        self.name: str = name
        
        if requires_faculties is None:
            self.requires_faculties: List[str] = []
        else:
            self.requires_faculties: List[str] = requires_faculties
        logger.info(f"Mental faculty {self.name} initialized with required faculties {self.requires_faculties}") # логирование инициализации

    def __str__(self) -> str:
        return f"Mental Faculty: {self.name}"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, TinyMentalFaculty):
            return self.name == other.name
        return False
    
    def process_action(self, agent: Any, action: dict) -> bool:
        """
        Обрабатывает действие, связанное с этой способностью.

        Args:
            agent (Any): Агент, выполняющий действие.
            action (dict): Действие для обработки.
        
        Returns:
            bool: `True`, если действие успешно обработано, `False` в противном случае.

        Raises:
            NotImplementedError: Если подкласс не реализует этот метод.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения действий, связанных с этой способностью.

        Raises:
            NotImplementedError: Если подкласс не реализует этот метод.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия, связанные с этой способностью.

        Raises:
            NotImplementedError: Если подкласс не реализует этот метод.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class CustomMentalFaculty(TinyMentalFaculty):
    """
    Представляет пользовательскую ментальную способность агента.

    Пользовательские ментальные способности - это когнитивные навыки, которые агент имеет
    и которые определяются пользователем только путем указания действий, которые способность может выполнять, или ограничений, которые
    способность вводит. Ограничения могут быть связаны с действиями, которые способность может выполнять, или быть независимыми,
    более общими ограничениями, которым должен следовать агент.
    """

    def __init__(self, name: str, requires_faculties: Optional[List[str]] = None,
                 actions_configs: Optional[Dict[str, Dict[str, Any]]] = None, constraints: Optional[List[str]] = None) -> None:
        """
        Инициализирует пользовательскую ментальную способность.

        Args:
            name (str): Название ментальной способности.
            requires_faculties (Optional[List[str]]): Список ментальных способностей, необходимых для правильной работы этой способности.
              Формат: ["faculty1", "faculty2", ...]. По умолчанию `None`.
            actions_configs (Optional[Dict[str, Dict[str, Any]]]): Словарь с конфигурацией действий, которые эта способность может выполнять.
              Формат: {<action_name>: {"description": <description>, "function": <function>}}. По умолчанию `None`.
            constraints (Optional[List[str]]): Список ограничений, вводимых этой способностью.
              Формат: [<constraint1>, <constraint2>, ...]. По умолчанию `None`.
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
        logger.info(f"Custom mental faculty {self.name} initialized with actions {self.actions_configs} and constraints {self.constraints}") # логирование инициализации
    
    def add_action(self, action_name: str, description: str, function: Callable = None) -> None:
        """
        Добавляет действие к этой способности.

        Args:
            action_name (str): Название действия.
            description (str): Описание действия.
            function (Callable, optional): Функция, выполняемая при вызове действия. По умолчанию `None`.
        """
        self.actions_configs[action_name] = {"description": description, "function": function}
        logger.info(f"Action {action_name} added to faculty {self.name}") # логирование добавления действия

    def add_actions(self, actions: Dict[str, Dict[str, Any]]) -> None:
        """
        Добавляет несколько действий к этой способности.

        Args:
            actions (dict): Словарь действий, которые нужно добавить.
        """
        for action_name, action_config in actions.items():
            self.add_action(action_name, action_config['description'], action_config['function'])
        logger.info(f"Actions {actions.keys()} added to faculty {self.name}") # логирование добавления действий
    
    def add_action_constraint(self, constraint: str) -> None:
        """
        Добавляет ограничение на действие.

        Args:
            constraint (str): Ограничение для добавления.
        """
        self.constraints.append(constraint)
        logger.info(f"Constraint {constraint} added to faculty {self.name}") # логирование добавления ограничения
    
    def add_actions_constraints(self, constraints: List[str]) -> None:
        """
        Добавляет несколько ограничений на действия.

        Args:
            constraints (list): Список ограничений для добавления.
        """
        for constraint in constraints:
            self.add_action_constraint(constraint)
        logger.info(f"Constraints {constraints} added to faculty {self.name}") # логирование добавления ограничений

    def process_action(self, agent: Any, action: dict) -> bool:
        """
        Обрабатывает действие.

        Args:
            agent (Any): Агент, выполняющий действие.
            action (dict): Действие для обработки.

        Returns:
            bool: `True`, если действие успешно обработано, `False` в противном случае.
        """
        logger.debug(f"Processing action: {action}")

        action_type: str = action['type']
        if action_type in self.actions_configs:
            action_config: Dict[str, Any] = self.actions_configs[action_type]
            action_function: Callable = action_config.get("function", None)

            if action_function is not None:
                try:
                    action_function(agent, action)
                except Exception as ex:
                    logger.error(f"Error while processing action {action_type}", ex, exc_info=True) # логирование ошибки
                    return False
            
            # one way or another, the action was processed
            return True 
        
        else:
            return False
    
    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения действий, связанных с этой способностью.
        """
        prompt: str = ""
        for action_name, action_config in self.actions_configs.items():
            prompt += f"  - {action_name.upper()}: {action_config['description']}\n"
        
        return prompt

    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия, связанные с этой способностью.
        """
        prompt: str = ""
        for constraint in self.constraints:
            prompt += f"  - {constraint}\n"
        
        return prompt


class RecallFaculty(TinyMentalFaculty):
    """
    Представляет способность вспоминать информацию из памяти.
    """

    def __init__(self) -> None:
        """
        Инициализирует способность вспоминать информацию из памяти.
        """
        super().__init__("Memory Recall")
        logger.info("Recall faculty initialized") # логирование инициализации
        

    def process_action(self, agent: Any, action: dict) -> bool:
        """
        Обрабатывает действие, связанное с вспоминанием информации.

        Args:
            agent (Any): Агент, выполняющий действие.
            action (dict): Действие для обработки.

        Returns:
            bool: `True`, если действие успешно обработано, `False` в противном случае.
        """
        logger.debug(f"Processing action: {action}")

        if action['type'] == "RECALL" and action['content'] is not None:
            content: str = action['content']

            semantic_memories: List[str] = agent.retrieve_relevant_memories(relevance_target=content)

            agent.logger.info(f"Recalling information related to '{content}'. Found {len(semantic_memories)} relevant memories.")

            if len(semantic_memories) > 0:
                # a string with each element in the list in a new line starting with a bullet point
                agent.think("I have remembered the following information from my semantic memory and will use it to guide me in my subsequent actions: \n" +
                        "\n".join([f"  - {item}" for item in semantic_memories]))
            else:
                agent.think(f"I can't remember anything about '{content}'.")
            
            return True
        
        else:
            return False

    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения действий, связанных с этой способностью.
        """
        prompt: str = """
              - RECALL: you can recall information from your memory. To do, you must specify a "mental query" to locate the desired memory. If the memory is found, it is brought to your conscience.
            """

        return textwrap.dedent(prompt)
    
    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия, связанные с этой способностью.
        """
        prompt: str = """
            - Before concluding you don't know something or don't have access to some information, you **must** try to RECALL it from your memory.
            - You try to RECALL information from your semantic/factual memory, so that you can have more relevant elements to think and talk about, whenever such an action would be likely
                to enrich the current interaction. To do so, you must specify able "mental query" that is related to the things you've been thinking, listening and talking about.
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
            - It may take several tries of RECALL to get the relevant information you need. If you don't find what you are looking for, you can try again with a **very** different "mental query".
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
            folders_paths (Optional[List[str]]): Список путей к локальным папкам. По умолчанию `None`.
            web_urls (Optional[List[str]]): Список URL-адресов веб-страниц. По умолчанию `None`.
        """
        super().__init__("Local Files and Web Grounding")

        self.local_files_grounding_connector: LocalFilesGroundingConnector = LocalFilesGroundingConnector(folders_paths=folders_paths)
        self.web_grounding_connector: WebPagesGroundingConnector = WebPagesGroundingConnector(web_urls=web_urls)
        logger.info(f"Files and Web Grounding faculty initialized with folders {folders_paths} and urls {web_urls}") # логирование инициализации

    def process_action(self, agent: Any, action: dict) -> bool:
        """
        Обрабатывает действие, связанное с доступом к файлам и веб-страницам.

        Args:
            agent (Any): Агент, выполняющий действие.
            action (dict): Действие для обработки.

        Returns:
            bool: `True`, если действие успешно обработано, `False` в противном случае.
        """
        try:
            if action['type'] == "CONSULT" and action['content'] is not None:
                target_name: str = action['content']

                results: List[str] = []
                results.append(self.local_files_grounding_connector.retrieve_by_name(target_name))
                results.append(self.web_grounding_connector.retrieve_by_name(target_name))

                if len(results) > 0:
                    agent.think(f"I have read the following document: \n{results}")
                else:
                    agent.think(f"I can't find any document with the name '{target_name}'.")
                
                return True
            
            elif action['type'] == "LIST_DOCUMENTS" and action['content'] is not None:
                available_names: List[str] = []
                available_names += self.local_files_grounding_connector.list_sources()
                available_names += self.web_grounding_connector.list_sources()

                if len(available_names) > 0:
                    agent.think(f"I have the following documents available to me: {available_names}")
                else:
                    agent.think(f"I don't have any documents available for inspection.")
                
                return True

            else:
                return False
        except Exception as ex:
            logger.error("Error while processing FilesAndWebGroundingFaculty action", ex, exc_info=True) # логирование ошибки
            return False


    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения действий, связанных с этой способностью.
        """
        prompt: str = """
            - LIST_DOCUMENTS: you can list the names of the documents you have access to, so that you can decide which to access, if any, to accomplish your goals. Documents is a generic term and includes any 
                kind of "packaged" information you can access, such as emails, files, chat messages, calendar events, etc. It also includes, in particular, web pages.
                The order of in which the documents are listed is not relevant.
            - CONSULT: you can retrieve and consult a specific document, so that you can access its content and accomplish your goals. To do so, you specify the name of the document you want to consult.
            """

        return textwrap.dedent(prompt)
    
    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия, связанные с этой способностью.
        """
        prompt: str = """
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
    которым обладают люди и приматы.
    """

    def __init__(self, tools: List[Any]) -> None:
        """
        Инициализирует способность использования инструментов.

        Args:
            tools (list): Список инструментов, доступных агенту.
        """
        super().__init__("Tool Use")
    
        self.tools: List[Any] = tools
        logger.info(f"Tool Use faculty initialized with tools {tools}") # логирование инициализации
    
    def process_action(self, agent: Any, action: dict) -> bool:
        """
        Обрабатывает действие, связанное с использованием инструментов.

        Args:
            agent (Any): Агент, выполняющий действие.
            action (dict): Действие для обработки.

        Returns:
            bool: `True`, если действие успешно обработано, `False` в противном случае.
        """
        try:
            for tool in self.tools:
                if tool.process_action(agent, action):
                    return True
            
            return False
        except Exception as ex:
            logger.error("Error while processing TinyToolUse action", ex, exc_info=True) # логирование ошибки
            return False
    
    def actions_definitions_prompt(self) -> str:
        """
        Возвращает prompt для определения действий, связанных с этой способностью.
        """
        # each tool should provide its own actions definitions prompt
        prompt: str = ""
        for tool in self.tools:
            prompt += tool.actions_definitions_prompt()
        
        return prompt
    
    def actions_constraints_prompt(self) -> str:
        """
        Возвращает prompt для определения ограничений на действия, связанные с этой способностью.
        """
        # each tool should provide its own actions constraints prompt
        prompt: str = ""
        for tool in self.tools:
            prompt += tool.actions_constraints_prompt()
        
        return prompt