### **Анализ кода модуля `tiny_person_validator.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/validation/tiny_person_validator.py

Модуль содержит класс `TinyPersonValidator`, который используется для валидации экземпляра `TinyPerson` с использованием OpenAI LLM.

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Четкая структура кода, разделение на логические блоки.
  - Использование шаблонов `chevron` для генерации prompt'ов.
  - Логирование процесса валидации.
- **Минусы**:
  - Отсутствуют аннотации типов для переменных и возвращаемых значений в функциях.
  - Не используется `j_loads` для загрузки `json`.
  - Не все переменные объявлены с использованием snake_case.
  - Не хватает docstring для класса `TinyPersonValidator`.
  - Не используется модуль `logger` из `src.logger.logger`.

**Рекомендации по улучшению:**
- Добавить docstring для класса `TinyPersonValidator`.
- Добавить аннотации типов для переменных и возвращаемых значений в функциях.
- Использовать `logger` из `src.logger.logger` вместо стандартного `logging`.
- Заменить `open` на `j_loads` для загрузки `json`.
- Привести все переменные к snake_case.
- Добавить обработку исключений с логированием ошибок.

**Оптимизированный код:**
```python
import os
import json
import chevron
from typing import Optional, Tuple

from tinytroupe import openai_utils
from tinytroupe.agent import TinyPerson
from tinytroupe import config
import tinytroupe.utils as utils
from src.logger import logger # Импортируем logger из src.logger.logger

default_max_content_display_length: int = config['OpenAI'].getint('MAX_CONTENT_DISPLAY_LENGTH', 1024)


class TinyPersonValidator:
    """
    Класс для валидации экземпляра TinyPerson с использованием OpenAI LLM.
    """

    @staticmethod
    def validate_person(
        person: TinyPerson,
        expectations: Optional[str] = None,
        include_agent_spec: bool = True,
        max_content_length: int = default_max_content_display_length
    ) -> Tuple[Optional[float], Optional[str]]:
        """
        Выполняет валидацию экземпляра TinyPerson, используя OpenAI LLM.

        Метод отправляет серию вопросов экземпляру TinyPerson для проверки его ответов с использованием OpenAI LLM.
        Метод возвращает значение float, представляющее собой оценку уверенности процесса валидации.
        Если процесс валидации завершается неудачно, метод возвращает None.

        Args:
            person (TinyPerson): Экземпляр TinyPerson для валидации.
            expectations (Optional[str], optional): Ожидания, используемые в процессе валидации. По умолчанию None.
            include_agent_spec (bool, optional): Флаг, указывающий, следует ли включать спецификацию агента в prompt. По умолчанию True.
            max_content_length (int, optional): Максимальная длина контента, отображаемого при рендеринге разговора.

        Returns:
            Tuple[Optional[float], Optional[str]]: Кортеж, содержащий оценку уверенности процесса валидации (от 0.0 до 1.0) и обоснование оценки,
                                                    или (None, None), если процесс валидации завершается неудачно.
        """
        # Инициализация текущих сообщений
        current_messages: list = []

        # Генерация prompt'а для проверки person
        check_person_prompt_template_path: str = os.path.join(os.path.dirname(__file__), 'prompts/check_person.mustache')
        try:
            with open(check_person_prompt_template_path, 'r', encoding='utf-8') as f:
                check_agent_prompt_template: str = f.read()
        except FileNotFoundError as ex:
            logger.error(f'Template file not found: {check_person_prompt_template_path}', ex, exc_info=True)
            return None, None
        except Exception as ex:
            logger.error('Error while reading template file', ex, exc_info=True)
            return None, None

        system_prompt: str = chevron.render(check_agent_prompt_template, {'expectations': expectations})

        # use dedent
        import textwrap
        user_prompt: str = textwrap.dedent(
            """
            Now, based on the following characteristics of the person being interviewed, and following the rules given previously, 
            create your questions and interview the person. Good luck!

            """
        )

        if include_agent_spec:
            user_prompt += f"\n\n{json.dumps(person._persona, indent=4)}"
        else:
            user_prompt += f"\n\nMini-biography of the person being interviewed: {person.minibio()}"

        logger.info(f'Starting validation of the person: {person.name}')

        # Отправка начальных сообщений в LLM
        current_messages.append({'role': 'system', 'content': system_prompt})
        current_messages.append({'role': 'user', 'content': user_prompt})

        try:
            message: dict = openai_utils.client().send_message(current_messages)
        except Exception as ex:
            logger.error('Error while sending message to OpenAI client', ex, exc_info=True)
            return None, None

        # Какую строку искать для завершения разговора
        termination_mark: str = '```json'

        while message is not None and not (termination_mark in message['content']):
            # Добавление вопросов к текущим сообщениям
            questions: str = message['content']
            current_messages.append({'role': message['role'], 'content': questions})
            logger.info(f'Question validation:\n{questions}')

            # Задаем вопросы человеку
            try:
                person.listen_and_act(questions, max_content_length=max_content_length)
            except Exception as ex:
                logger.error('Error while person listening and acting', ex, exc_info=True)
                return None, None

            responses: str = person.pop_actions_and_get_contents_for('TALK', False)
            logger.info(f'Person reply:\n{responses}')

            # Добавление ответов к текущему разговору и проверка следующего сообщения
            current_messages.append({'role': 'user', 'content': responses})
            try:
                message = openai_utils.client().send_message(current_messages)
            except Exception as ex:
                logger.error('Error while sending message to OpenAI client', ex, exc_info=True)
                return None, None

        if message is not None:
            try:
                json_content: dict = utils.extract_json(message['content'])
                # read score and justification
                score: float = float(json_content['score'])
                justification: str = json_content['justification']
                logger.info(f'Validation score: {score:.2f}; Justification: {justification}')

                return score, justification
            except (ValueError, KeyError, TypeError) as ex:
                logger.error('Error while extracting score and justification', ex, exc_info=True)
                return None, None
        else:
            return None, None