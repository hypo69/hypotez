### **Анализ кода модуля `story`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/story.py

Этот модуль предоставляет механизмы для создания историй в TinyTroupe, основанных на симуляциях окружения или агентов.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован и разбит на логические блоки.
    - Использование docstring для документирования классов и методов.
    - Четкое разделение ответственности между классами и методами.
- **Минусы**:
    - Отсутствуют аннотации типов для параметров и возвращаемых значений.
    - Использование `Exception` без конкретизации типа исключения.
    - Docstring на английском языке.

**Рекомендации по улучшению**:

1.  Добавить аннотации типов для параметров и возвращаемых значений во всех методах.
2.  Конкретизировать типы исключений вместо использования `Exception`.
3.  Перевести docstring на русский язык.
4.  Улучшить обработку ошибок, добавив логирование с использованием модуля `logger` из `src.logger`.
5.  Добавить проверки входных данных, чтобы избежать неожиданного поведения.

**Оптимизированный код:**

```python
"""
Модуль для создания историй в TinyTroupe на основе симуляций.
================================================================

Модуль предоставляет класс :class:`TinyStory`, который помогает создавать истории, основанные на симуляциях
окружения или агентов в TinyTroupe. Он позволяет задавать цели истории, контекст, а также учитывать
историю взаимодействий для генерации продолжения истории.

Пример использования
----------------------

>>> from tinytroupe.environment import TinyWorld
>>> from tinytroupe.story import TinyStory
>>> world = TinyWorld()
>>> story = TinyStory(environment=world, purpose="Создание интересной истории о мире.")
>>> start = story.start_story(requirements="Начать захватывающую историю о развитии мира.", number_of_words=150)
>>> print(start)
"""

from typing import List, Optional
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
import tinytroupe.utils as utils
from tinytroupe import openai_utils
from src.logger import logger  # Импортируем модуль logger


class TinyStory:
    """
    Класс для создания историй на основе симуляций в TinyTroupe.
    """

    def __init__(
        self,
        environment: Optional[TinyWorld] = None,
        agent: Optional[TinyPerson] = None,
        purpose: str = "Быть реалистичной симуляцией.",
        context: str = "",
        first_n: int = 10,
        last_n: int = 20,
        include_omission_info: bool = True,
    ) -> None:
        """
        Инициализирует историю. История может быть об окружении или агенте.
        У истории также есть цель, которая используется для направления генерации истории.
        Истории знают, что они связаны с симуляциями, поэтому можно указывать цели, связанные с симуляцией.

        Args:
            environment (Optional[TinyWorld], optional): Окружение, в котором происходит история. По умолчанию None.
            agent (Optional[TinyPerson], optional): Агент в истории. По умолчанию None.
            purpose (str, optional): Цель истории. По умолчанию "Быть реалистичной симуляцией.".
            context (str, optional): Текущий контекст истории. По умолчанию "". Фактическая история будет добавлена к этому контексту.
            first_n (int, optional): Количество первых взаимодействий, которые нужно включить в историю. По умолчанию 10.
            last_n (int, optional): Количество последних взаимодействий, которые нужно включить в историю. По умолчанию 20.
            include_omission_info (bool, optional): Нужно ли включать информацию об опущенных взаимодействиях. По умолчанию True.

        Raises:
            ValueError: Если одновременно предоставлены и environment, и agent, или ни один из них.
        """

        # Проверяем, что предоставлен ровно один из параметров: environment или agent
        if environment and agent:
            raise ValueError(
                'Должен быть предоставлен либо параметр "environment", либо "agent", но не оба'
            )
        if not (environment or agent):
            raise ValueError("Необходимо предоставить хотя бы один из параметров")

        self.environment = environment
        self.agent = agent

        self.purpose = purpose

        self.current_story = context

        self.first_n = first_n
        self.last_n = last_n
        self.include_omission_info = include_omission_info

    def start_story(
        self,
        requirements: str = "Начать интересную историю об агентах.",
        number_of_words: int = 100,
        include_plot_twist: bool = False,
    ) -> str:
        """
        Начинает новую историю.

        Args:
            requirements (str, optional): Требования к началу истории. По умолчанию "Начать интересную историю об агентах.".
            number_of_words (int, optional): Количество слов в начале истории. По умолчанию 100.
            include_plot_twist (bool, optional): Нужно ли включать сюжетный поворот. По умолчанию False.

        Returns:
            str: Начало истории.
        """

        rendering_configs = {
            "purpose": self.purpose,
            "requirements": requirements,
            "current_simulation_trace": self._current_story(),
            "number_of_words": number_of_words,
            "include_plot_twist": include_plot_twist,
        }

        messages = utils.compose_initial_LLM_messages_with_templates(
            "story.start.system.mustache",
            "story.start.user.mustache",
            rendering_configs,
        )
        try:
            next_message = openai_utils.client().send_message(messages, temperature=1.5)

            start = next_message["content"]

            self.current_story += utils.dedent(
                f"""

                ## Начало истории

                {start}

                """
            )

            return start
        except Exception as ex:
            logger.error(
                "Ошибка при генерации начала истории", ex, exc_info=True
            )  # Логируем ошибку
            return ""  # Возвращаем пустую строку в случае ошибки

    def continue_story(
        self,
        requirements: str = "Продолжить историю интересным образом.",
        number_of_words: int = 100,
        include_plot_twist: bool = False,
    ) -> str:
        """
        Предлагает продолжение истории.

        Args:
            requirements (str, optional): Требования к продолжению истории. По умолчанию "Продолжить историю интересным образом.".
            number_of_words (int, optional): Количество слов в продолжении истории. По умолчанию 100.
            include_plot_twist (bool, optional): Нужно ли включать сюжетный поворот. По умолчанию False.

        Returns:
            str: Продолжение истории.
        """

        rendering_configs = {
            "purpose": self.purpose,
            "requirements": requirements,
            "current_simulation_trace": self._current_story(),
            "number_of_words": number_of_words,
            "include_plot_twist": include_plot_twist,
        }

        messages = utils.compose_initial_LLM_messages_with_templates(
            "story.continuation.system.mustache",
            "story.continuation.user.mustache",
            rendering_configs,
        )
        try:
            next_message = openai_utils.client().send_message(messages, temperature=1.5)

            continuation = next_message["content"]

            self.current_story += utils.dedent(
                f"""

                ## Продолжение истории

                {continuation}

                """
            )

            return continuation
        except Exception as ex:
            logger.error(
                "Ошибка при генерации продолжения истории", ex, exc_info=True
            )  # Логируем ошибку
            return ""  # Возвращаем пустую строку в случае ошибки

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

            ## Новые взаимодействия симуляции для рассмотрения

            {interaction_history}

            """
        )

        return self.current_story