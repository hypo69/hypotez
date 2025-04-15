### **Анализ кода модуля `story`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/story.py

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код достаточно хорошо структурирован и содержит docstring для классов и методов.
    - Использование `utils.dedent` для форматирования текста.
- **Минусы**:
    - Docstring написаны на английском языке, требуется перевод на русский.
    - Отсутствуют аннотации типов для переменных класса `TinyStory`.
    - Не используется модуль `logger` для логирования.
    - Не обрабатываются исключения с логированием ошибок.

#### **Рекомендации по улучшению**:

1.  **Документация**:
    *   Перевести все docstring на русский язык, соблюдая формат, указанный в инструкции.
    *   Добавить подробное описание каждого параметра и возвращаемого значения.
    *   Указывать, какие исключения может вызывать метод.
2.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных в `__init__`.
3.  **Логирование**:
    *   Добавить логирование с использованием модуля `logger` для отслеживания хода выполнения программы и записи ошибок.
4.  **Обработка исключений**:
    *   Добавить блоки `try...except` для обработки возможных исключений, особенно при взаимодействии с внешними сервисами (например, `openai_utils.client().send_message`).
    *   Логировать ошибки с использованием `logger.error`, передавая исключение и `exc_info=True`.

#### **Оптимизированный код**:

```python
"""
Модуль для создания историй в TinyTroupe
===========================================

Этот модуль предоставляет вспомогательные механизмы для создания подходящих историй в TinyTroupe.
"""

from typing import List, Optional
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
import tinytroupe.utils as utils
from tinytroupe import openai_utils
from src.logger import logger  # Импортируем модуль logger

class TinyStory:
    """
    Класс для создания историй на основе симуляций TinyTroupe.
    """

    def __init__(
        self,
        environment: Optional[TinyWorld] = None,
        agent: Optional[TinyPerson] = None,
        purpose: str = "Be a realistic simulation.",
        context: str = "",
        first_n: int = 10,
        last_n: int = 20,
        include_omission_info: bool = True,
    ) -> None:
        """
        Инициализация истории. История может быть об окружении или агенте.
        Также имеет цель, которая используется для направления генерации истории.
        Истории знают, что они связаны с симуляциями, поэтому можно указать цели, связанные с симуляцией.

        Args:
            environment (Optional[TinyWorld], optional): Окружение, в котором происходит история. По умолчанию None.
            agent (Optional[TinyPerson], optional): Агент в истории. По умолчанию None.
            purpose (str, optional): Цель истории. По умолчанию "Be a realistic simulation.".
            context (str, optional): Текущий контекст истории. По умолчанию "". Фактическая история будет добавлена к этому контексту.
            first_n (int, optional): Количество первых взаимодействий, которые нужно включить в историю. По умолчанию 10.
            last_n (int, optional): Количество последних взаимодействий, которые нужно включить в историю. По умолчанию 20.
            include_omission_info (bool, optional): Включать ли информацию об опущенных взаимодействиях. По умолчанию True.

        Raises:
            Exception: Если предоставлены и `environment`, и `agent` или ни один из них.
        """

        # ровно один из этих параметров должен быть предоставлен
        if environment and agent:
            raise Exception('Either \'environment\' or \'agent\' should be provided, not both')

        if not (environment or agent):
            raise Exception('At least one of the parameters should be provided')

        self.environment = environment
        self.agent = agent

        self.purpose = purpose

        self.current_story = context

        self.first_n = first_n
        self.last_n = last_n
        self.include_omission_info = include_omission_info

    def start_story(
        self,
        requirements: str = "Start some interesting story about the agents.",
        number_of_words: int = 100,
        include_plot_twist: bool = False,
    ) -> str:
        """
        Начинает новую историю.

        Args:
            requirements (str, optional): Требования к началу истории. По умолчанию "Start some interesting story about the agents.".
            number_of_words (int, optional): Количество слов в начале истории. По умолчанию 100.
            include_plot_twist (bool, optional): Включать ли неожиданный поворот сюжета. По умолчанию False.

        Returns:
            str: Начало истории.

        Raises:
            Exception: Если возникает ошибка при отправке сообщения в OpenAI.
        """
        rendering_configs = {
            'purpose': self.purpose,
            'requirements': requirements,
            'current_simulation_trace': self._current_story(),
            'number_of_words': number_of_words,
            'include_plot_twist': include_plot_twist,
        }

        messages = utils.compose_initial_LLM_messages_with_templates(
            'story.start.system.mustache', 'story.start.user.mustache', rendering_configs
        )

        try:
            next_message = openai_utils.client().send_message(messages, temperature=1.5)  # Отправляем сообщение и получаем ответ
            start = next_message['content']  # Извлекаем контент из ответа
        except Exception as ex:
            logger.error('Error while sending message to OpenAI', ex, exc_info=True)
            raise  # Перебрасываем исключение для дальнейшей обработки

        self.current_story += utils.dedent(
            f"""

            ## The story begins

            {start}

            """
        )

        return start

    def continue_story(
        self,
        requirements: str = "Continue the story in an interesting way.",
        number_of_words: int = 100,
        include_plot_twist: bool = False,
    ) -> str:
        """
        Предлагает продолжение истории.

        Args:
            requirements (str, optional): Требования к продолжению истории. По умолчанию "Continue the story in an interesting way.".
            number_of_words (int, optional): Количество слов в продолжении истории. По умолчанию 100.
            include_plot_twist (bool, optional): Включать ли неожиданный поворот сюжета. По умолчанию False.

        Returns:
            str: Продолжение истории.

        Raises:
            Exception: Если возникает ошибка при отправке сообщения в OpenAI.
        """
        rendering_configs = {
            'purpose': self.purpose,
            'requirements': requirements,
            'current_simulation_trace': self._current_story(),
            'number_of_words': number_of_words,
            'include_plot_twist': include_plot_twist,
        }

        messages = utils.compose_initial_LLM_messages_with_templates(
            'story.continuation.system.mustache',
            'story.continuation.user.mustache',
            rendering_configs,
        )
        try:
            next_message = openai_utils.client().send_message(messages, temperature=1.5)  # Отправляем сообщение и получаем ответ
            continuation = next_message['content']  # Извлекаем контент из ответа
        except Exception as ex:
            logger.error('Error while sending message to OpenAI', ex, exc_info=True)
            raise  # Перебрасываем исключение для дальнейшей обработки

        self.current_story += utils.dedent(
            f"""

            ## The story continues

            {continuation}

            """
        )

        return continuation

    def _current_story(self) -> str:
        """
        Получает текущую историю.

        Returns:
            str: Текущая история.
        """
        interaction_history = ""

        if self.agent is not None:
            interaction_history += self.agent.pretty_current_interactions(
                first_n=self.first_n,
                last_n=self.last_n,
                include_omission_info=self.include_omission_info,
            )
        elif self.environment is not None:
            interaction_history += self.environment.pretty_current_interactions(
                first_n=self.first_n,
                last_n=self.last_n,
                include_omission_info=self.include_omission_info,
            )

        self.current_story += utils.dedent(
            f"""

            ## New simulation interactions to consider

            {interaction_history}

            """
        )

        return self.current_story