### **Анализ кода модуля `tiny_person_factory.py`**

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на логические блоки.
  - Используются комментарии для пояснения функциональности.
  - Присутствует обработка исключений.
- **Минусы**:
  - Отсутствуют аннотации типов для переменных и возвращаемых значений функций.
  - Используется устаревший стиль `Union[]` вместо `|`.
  - Не все docstring переведены на русский язык.
  - Не используется модуль `logger` из `src.logger.logger` для логирования ошибок.

**Рекомендации по улучшению**:

1. **Добавить аннотации типов**:
   - Добавить аннотации типов для всех переменных и возвращаемых значений функций, чтобы улучшить читаемость и облегчить отладку.
     ```python
     def __init__(self, context_text: str, simulation_id: str | None = None):
         ...
     ```

2. **Использовать `|` вместо `Union[]`**:
   - Заменить `Union[]` на `|` для указания типов.
     ```python
     simulation_id: str | None = None
     ```

3. **Перевести docstring на русский язык**:
   - Перевести все docstring на русский язык, чтобы соответствовать требованиям.

4. **Использовать модуль `logger` из `src.logger.logger`**:
   - Заменить все экземпляры логирования на использование модуля `logger` из `src.logger.logger`.
     ```python
     from src.logger import logger

     try:
         ...
     except Exception as ex:
         logger.error('Описание ошибки', ex, exc_info=True)
     ```

5. **Улучшить docstring**:
   - Добавить более подробное описание для всех функций, включая информацию о том, что именно делает функция, какие параметры принимает и что возвращает.

6. **Использовать одинарные кавычки**:
   - Заменить двойные кавычки на одинарные кавычки для строковых литералов.

**Оптимизированный код**:

```python
"""
Модуль для создания экземпляров TinyPerson
=========================================

Модуль содержит класс :class:`TinyPersonFactory`, который используется для создания экземпляров TinyPerson на основе контекста.
"""
import os
import json
import chevron

from .tiny_factory import TinyFactory
from src.logger import logger
from tinytroupe import openai_utils
from tinytroupe.agent import TinyPerson
import tinytroupe.utils as utils
from tinytroupe.control import transactional
from typing import List, Optional


class TinyPersonFactory(TinyFactory):
    """
    Фабрика для создания экземпляров TinyPerson.
    """

    def __init__(self, context_text: str, simulation_id: str | None = None) -> None:
        """
        Инициализирует экземпляр TinyPersonFactory.

        Args:
            context_text (str): Контекстный текст, используемый для генерации экземпляров TinyPerson.
            simulation_id (str | None, optional): ID симуляции. По умолчанию None.
        """
        super().__init__(simulation_id)
        self.person_prompt_template_path: str = os.path.join(os.path.dirname(__file__), 'prompts/generate_person.mustache')
        self.context_text: str = context_text
        self.generated_minibios: List[str] = []  # keep track of the generated persons. We keep the minibio to avoid generating the same person twice.
        self.generated_names: List[str] = []

    @staticmethod
    def generate_person_factories(number_of_factories: int, generic_context_text: str) -> Optional[List['TinyPersonFactory']]:
        """
        Генерирует список экземпляров TinyPersonFactory, используя OpenAI LLM.

        Args:
            number_of_factories (int): Количество экземпляров TinyPersonFactory для генерации.
            generic_context_text (str): Общий контекстный текст, используемый для генерации экземпляров TinyPersonFactory.

        Returns:
            list: Список экземпляров TinyPersonFactory.
        """
        logger.info(f'Starting the generation of the {number_of_factories} person factories based on that context: {generic_context_text}')

        system_prompt: str = open(os.path.join(os.path.dirname(__file__), 'prompts/generate_person_factory.md')).read()

        messages: List[dict] = []
        messages.append({'role': 'system', 'content': system_prompt})

        user_prompt: str = chevron.render('Please, create {{number_of_factories}} person descriptions based on the following broad context: {{context}}', {
            'number_of_factories': number_of_factories,
            'context': generic_context_text
        })

        messages.append({'role': 'user', 'content': user_prompt})

        response = openai_utils.client().send_message(messages)

        if response is not None:
            result: List[dict] = utils.extract_json(response['content'])

            factories: List['TinyPersonFactory'] = []
            for i in range(number_of_factories):
                logger.debug(f'Generating person factory with description: {result[i]}')
                factories.append(TinyPersonFactory(result[i]))

            return factories

        return None

    def generate_person(self,
                        agent_particularities: str | None = None,
                        temperature: float = 1.5,
                        frequency_penalty: float = 0.0,
                        presence_penalty: float = 0.0,
                        attepmpts: int = 10) -> Optional[TinyPerson]:
        """
        Генерирует экземпляр TinyPerson, используя OpenAI LLM.

        Args:
            agent_particularities (str, optional): Особенности агента. По умолчанию None.
            temperature (float, optional): Температура для выборки из LLM. По умолчанию 1.5.
            frequency_penalty (float, optional): Штраф за частоту. По умолчанию 0.0.
            presence_penalty (float, optional): Штраф за присутствие. По умолчанию 0.0.
            attepmpts (int, optional): Количество попыток генерации. По умолчанию 10.

        Returns:
            TinyPerson | None: Экземпляр TinyPerson, сгенерированный с использованием LLM, или None в случае ошибки.
        """

        logger.info(f'Starting the person generation based on that context: {self.context_text}')

        # read example specs from files.
        example_1: dict = json.load(open(os.path.join(os.path.dirname(__file__), '../examples/agents/Friedrich_Wolf.agent.json')))
        example_2: dict = json.load(open(os.path.join(os.path.dirname(__file__), '../examples/agents/Sophie_Lefevre.agent.json')))

        # We must include all agent names generated in the whole of the simulation, not only the ones generated by this factory,
        # since they all share the same name space.
        #
        # For the minibios, we only need to keep track of the ones generated by this factory, since they are unique to each factory
        # and are used to guide the sampling process.
        prompt: str = chevron.render(open(self.person_prompt_template_path).read(), {
            'context': self.context_text,
            'agent_particularities': agent_particularities,

            # Note that we need to dump them to JSON strings, to ensure we get double quotes,
            # and other formatting issues are avoided.
            'example_1': json.dumps(example_1['persona'], indent=4),
            'example_2': json.dumps(example_2['persona'], indent=4),

            'already_generated_minibios': self.generated_minibios,
            'already_generated_names': TinyPerson.all_agents_names()
        })

        def aux_generate(attempt: int) -> Optional[dict]:
            """
            Вспомогательная функция для генерации персонажа.

            Args:
                attempt (int): Номер попытки.

            Returns:
                dict | None: Спецификация агента или None, если не удалось сгенерировать.
            """

            messages: List[dict] = []
            messages += [{'role': 'system', 'content': 'You are a system that generates specifications for realistic simulations of people. You follow the generation rules and constraints carefully.'},
                         {'role': 'user', 'content': prompt}]

            if attempt > 1:
                # we failed once already due to repetition, so we try to further reinforce the message to avoid repetition.
                messages.append({'role': 'user', 'content': 'IMPORTANT: Please ensure you **do not** generate the same name again. Agent names **must** be unique.' +
                                                             'Read the list of already generated names to avoid repetition. If necessary, generate a longer name to ensure it is new.'})

            # due to a technicality, we need to call an auxiliary method to be able to use the transactional decorator.
            message = self._aux_model_call(messages=messages,
                                            temperature=temperature,
                                            frequency_penalty=frequency_penalty,
                                            presence_penalty=presence_penalty)

            if message is not None:
                result: dict = utils.extract_json(message['content'])

                logger.debug(f'At attempt {attempt}, generated person parameters:\\n{json.dumps(result, indent=4, sort_keys=True)}')

                # only accept the generated spec if the name is not already in the generated names, because they must be unique.
                if result['name'].lower() not in self.generated_names:
                    return result
                else:
                    logger.info(f'Person with name {result["name"]} was already generated, cannot be reused.')

            return None  # no suitable agent was generated

        agent_spec: dict | None = None
        attempt: int = 0
        while agent_spec is None and attempt < attepmpts:
            try:
                attempt += 1
                agent_spec = aux_generate(attempt=attempt)
            except Exception as ex:
                logger.error(f'Error while generating agent specification: {ex}', ex, exc_info=True)

        # create the fresh agent
        if agent_spec is not None:
            # the agent is created here. This is why the present method cannot be cached. Instead, an auxiliary method is used
            # for the actual model call, so that it gets cached properly without skipping the agent creation.
            person: TinyPerson = TinyPerson(agent_spec['name'])
            self._setup_agent(person, agent_spec)
            self.generated_minibios.append(person.minibio())
            self.generated_names.append(person.get('name').lower())
            return person
        else:
            logger.error(f'Could not generate an agent after {attepmpts} attempts.')
            return None

    def generate_people(self, number_of_people: int,
                        agent_particularities: str | None = None,
                        temperature: float = 1.5,
                        frequency_penalty: float = 0.0,
                        presence_penalty: float = 0.0,
                        attepmpts: int = 10,
                        verbose: bool = False) -> List[TinyPerson]:
        """
        Генерирует список экземпляров TinyPerson, используя OpenAI LLM.

        Args:
            number_of_people (int): Количество экземпляров TinyPerson для генерации.
            agent_particularities (str | None, optional): Особенности агента. По умолчанию None.
            temperature (float, optional): Температура для выборки из LLM. По умолчанию 1.5.
            frequency_penalty (float, optional): Штраф за частоту. По умолчанию 0.0.
            presence_penalty (float, optional): Штраф за присутствие. По умолчанию 0.0.
            attepmpts (int, optional): Количество попыток генерации. По умолчанию 10.
            verbose (bool, optional): Флаг verbose. По умолчанию False.

        Returns:
            list: Список экземпляров TinyPerson, сгенерированных с использованием LLM.
        """
        people: List[TinyPerson] = []
        for i in range(number_of_people):
            person: TinyPerson | None = self.generate_person(agent_particularities=agent_particularities,
                                            temperature=temperature,
                                            frequency_penalty=frequency_penalty,
                                            presence_penalty=presence_penalty,
                                            attepmpts=attepmpts)
            if person is not None:
                people.append(person)
                info_msg: str = f'Generated person {i+1}/{number_of_people}: {person.minibio()}'
                logger.info(info_msg)
                if verbose:
                    print(info_msg)
            else:
                logger.error(f'Could not generate person {i+1}/{number_of_people}.')

        return people

    @transactional
    def _aux_model_call(self, messages: List[dict], temperature: float, frequency_penalty: float, presence_penalty: float) -> Optional[dict]:
        """
        Вспомогательный метод для выполнения вызова модели.

        Args:
            messages (List[dict]): Список сообщений для отправки в модель.
            temperature (float): Температура для выборки из LLM.
            frequency_penalty (float): Штраф за частоту.
            presence_penalty (float): Штраф за присутствие.

        Returns:
            dict | None: Ответ от модели или None в случае ошибки.
        """
        return openai_utils.client().send_message(messages,
                                                  temperature=temperature,
                                                  frequency_penalty=frequency_penalty,
                                                  presence_penalty=presence_penalty,
                                                  response_format={'type': 'json_object'})

    @transactional
    def _setup_agent(self, agent: TinyPerson, configuration: dict) -> None:
        """
        Настраивает агента с необходимыми элементами.

        Args:
            agent (TinyPerson): Экземпляр агента для настройки.
            configuration (dict): Конфигурация агента.
        """
        agent.include_persona_definitions(configuration)

        # does not return anything, as we don't want to cache the agent object itself.