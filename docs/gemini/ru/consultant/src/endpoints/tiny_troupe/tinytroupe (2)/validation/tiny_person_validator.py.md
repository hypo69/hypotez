### **Анализ кода модуля `tiny_person_validator.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/validation/tiny_person_validator.py

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Четкая структура класса `TinyPersonValidator`.
  - Использование `chevron` для шаблонизации промптов.
  - Логирование процесса валидации.
- **Минусы**:
  - Отсутствуют аннотации типов для переменных и параметров функций.
  - Использование устаревшего стиля форматирования кода (например, отсутствие пробелов вокруг операторов).
  - Не используется модуль `logger` из `src.logger.logger`.
  - Нет обработки исключений.

#### **Рекомендации по улучшению**:
- Добавить аннотации типов для всех переменных и параметров функций.
- Использовать пробелы вокруг операторов присваивания для улучшения читаемости.
- Заменить `logging` на `logger` из `src.logger.logger`.
- Добавить обработку исключений для повышения надежности кода.
- Добавить docstring для класса `TinyPersonValidator`.
- Оптимизировать импорты, убрав неиспользуемые.
- Добавить комментарии для пояснения логики работы кода.
- Перевести все комментарии и docstring на русский язык, если они на английском.

#### **Оптимизированный код**:

```python
import os
import json
import chevron
from typing import Optional, Tuple

from src.logger import logger  # Используем logger из src.logger
from tinytroupe import openai_utils
from tinytroupe.agent import TinyPerson
from tinytroupe import config
import tinytroupe.utils as utils


default_max_content_display_length: int = config['OpenAI'].getint('MAX_CONTENT_DISPLAY_LENGTH', 1024)


class TinyPersonValidator:
    """
    Валидатор экземпляра TinyPerson с использованием LLM OpenAI.

    Предоставляет метод для оценки соответствия TinyPerson заданным ожиданиям,
    возвращая оценку уверенности и обоснование.
    """

    @staticmethod
    def validate_person(
        person: TinyPerson,
        expectations: Optional[str] = None,
        include_agent_spec: bool = True,
        max_content_length: int = default_max_content_display_length
    ) -> Tuple[Optional[float], Optional[str]]:
        """
        Проверяет экземпляр TinyPerson, используя LLM OpenAI.

        Этот метод отправляет серию вопросов экземпляру TinyPerson для проверки его ответов, используя LLM OpenAI.
        Метод возвращает значение типа float, представляющее оценку уверенности процесса проверки.
        Если процесс проверки завершается неудачно, метод возвращает None.

        Args:
            person (TinyPerson): Экземпляр TinyPerson для проверки.
            expectations (Optional[str], optional): Ожидания, используемые в процессе проверки. По умолчанию None.
            include_agent_spec (bool, optional): Следует ли включать спецификацию агента в запрос. По умолчанию False.
            max_content_length (int, optional): Максимальная длина контента, отображаемого при рендеринге разговора.

        Returns:
            Tuple[Optional[float], Optional[str]]: Кортеж, содержащий оценку уверенности процесса проверки (от 0.0 до 1.0)
            и обоснование оценки, или (None, None), если процесс проверки завершается неудачно.
        """
        # Инициализация текущих сообщений
        current_messages: list[dict] = []

        # Получение пути к шаблону промта для проверки персонажа
        check_person_prompt_template_path: str = os.path.join(os.path.dirname(__file__), 'prompts/check_person.mustache')
        try:
            with open(check_person_prompt_template_path, 'r', encoding='utf-8') as f:
                check_agent_prompt_template: str = f.read()
        except FileNotFoundError as ex:
            logger.error(f'Template file not found: {check_person_prompt_template_path}', ex, exc_info=True)
            return None, None
        except Exception as ex:
            logger.error(f'Error reading template file: {check_person_prompt_template_path}', ex, exc_info=True)
            return None, None

        # Рендеринг системного промта с использованием шаблона и ожиданий
        try:
            system_prompt: str = chevron.render(check_agent_prompt_template, {'expectations': expectations})
        except Exception as ex:
            logger.error('Error rendering system prompt with Chevron', ex, exc_info=True)
            return None, None

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
            logger.error('Error sending initial messages to OpenAI client', ex, exc_info=True)
            return None, None

        # Определение строки для завершения разговора
        termination_mark: str = '```json'

        # Цикл обработки сообщений до достижения точки завершения или получения None
        while message is not None and not (termination_mark in message['content']):
            # Добавление вопросов к текущим сообщениям
            questions: str = message['content']
            current_messages.append({'role': message['role'], 'content': questions})
            logger.info(f'Question validation:\n{questions}')

            # Запрос вопросов к персонажу
            try:
                person.listen_and_act(questions, max_content_length=max_content_length)
            except Exception as ex:
                logger.error('Error during person listen and act', ex, exc_info=True)
                return None, None

            responses: str = person.pop_actions_and_get_contents_for('TALK', False)
            logger.info(f'Person reply:\n{responses}')

            # Добавление ответов к текущему разговору и проверка следующего сообщения
            current_messages.append({'role': 'user', 'content': responses})
            try:
                message: dict = openai_utils.client().send_message(current_messages)
            except Exception as ex:
                logger.error('Error while sending message to client', ex, exc_info=True)
                return None, None

        # Если сообщение не None, извлекаем JSON контент
        if message is not None:
            try:
                json_content: dict = utils.extract_json(message['content'])
                # Чтение оценки и обоснования
                score: float = float(json_content['score'])
                justification: str = json_content['justification']
                logger.info(f'Validation score: {score:.2f}; Justification: {justification}')

                return score, justification
            except (ValueError, KeyError, TypeError) as ex:
                logger.error('Error extracting score and justification from JSON content', ex, exc_info=True)
                return None, None

        else:
            return None, None