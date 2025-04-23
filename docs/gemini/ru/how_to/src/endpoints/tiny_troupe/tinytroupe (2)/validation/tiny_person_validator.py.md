### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует валидацию экземпляра класса `TinyPerson` с использованием OpenAI LLM. Он отправляет серию вопросов экземпляру `TinyPerson` и проверяет его ответы, возвращая оценку достоверности и обоснование.

Шаги выполнения
-------------------------
1. **Инициализация**: 
   - Определяются переменные и пути, необходимые для валидации.
   - Устанавливается максимальная длина отображаемого контента.
   - Инициализируется логгер для записи информации о процессе валидации.
   
2. **Подготовка Prompt**:
   - Формируется системный prompt на основе шаблона `check_person.mustache`.
   - Определяется пользовательский prompt с инструкциями для проведения интервью с `TinyPerson`.
   - К пользовательскому prompt добавляется либо подробная информация о персоне, либо мини-биография.
   
3. **Начало валидации**:
   - Логируется начало процесса валидации для конкретного экземпляра `TinyPerson`.
   - Системный и пользовательский prompt добавляются в список сообщений для отправки в LLM.
   
4. **Общение с LLM**:
   - Отправляется первое сообщение в LLM для получения вопросов.
   - В цикле происходит общение с LLM до тех пор, пока не будет получен маркер завершения (`termination_mark`).
   - Вопросы, полученные от LLM, логируются и отправляются экземпляру `TinyPerson` через метод `listen_and_act`.
   - Ответы `TinyPerson` извлекаются и логируются.
   - Ответы добавляются в список сообщений для LLM.
   - Отправляется следующее сообщение в LLM.
   
5. **Извлечение результатов**:
   - После получения маркера завершения извлекается JSON из сообщения LLM.
   - Из JSON извлекаются оценка (`score`) и обоснование (`justification`).
   - Результаты валидации логируются.
   
6. **Завершение**:
   - Возвращается оценка и обоснование валидации.
   - Если валидация не удалась (нет маркера завершения), возвращается `None` для обоих значений.

Пример использования
-------------------------

```python
import os
import json
import chevron
import logging

from tinytroupe import openai_utils
from tinytroupe.agent import TinyPerson
from tinytroupe import config
import tinytroupe.utils as utils

def validate_tiny_person(person: TinyPerson, expectations: str = None) -> tuple[float, str] | tuple[None, None]:
    """
    Пример использования функции `validate_person` для проверки TinyPerson.

    Args:
        person (TinyPerson): Экземпляр TinyPerson для валидации.
        expectations (str, optional): Ожидания от TinyPerson. Defaults to None.

    Returns:
        tuple[float, str] | tuple[None, None]: Кортеж, содержащий оценку и обоснование, или None, если валидация не удалась.
    """
    # Путь к шаблону prompt для проверки персоны
    check_person_prompt_template_path = os.path.join(os.path.dirname(__file__), 'prompts/check_person.mustache')
    with open(check_person_prompt_template_path, 'r') as f:
        check_agent_prompt_template = f.read()

    # Рендеринг системного prompt с ожиданиями
    system_prompt = chevron.render(check_agent_prompt_template, {"expectations": expectations})

    # Формирование пользовательского prompt
    import textwrap
    user_prompt = textwrap.dedent("""
    Now, based on the following characteristics of the person being interviewed, and following the rules given previously, 
    create your questions and interview the person. Good luck!
    """)

    user_prompt += f"\n\nMini-biography of the person being interviewed: {person.minibio()}"

    logger = logging.getLogger("tinytroupe")
    logger.info(f"Starting validation of the person: {person.name}")

    # Инициализация сообщений для LLM
    current_messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
    message = openai_utils.client().send_message(current_messages)

    # Определение маркера завершения разговора
    termination_mark = "```json"

    while message is not None and termination_mark not in message["content"]:
        questions = message["content"]
        current_messages.append({"role": message["role"], "content": questions})
        logger.info(f"Question validation:\n{questions}")

        person.listen_and_act(questions)
        responses = person.pop_actions_and_get_contents_for("TALK", False)
        logger.info(f"Person reply:\n{responses}")

        current_messages.append({"role": "user", "content": responses})
        message = openai_utils.client().send_message(current_messages)

    if message is not None:
        json_content = utils.extract_json(message['content'])
        score = float(json_content["score"])
        justification = json_content["justification"]
        logger.info(f"Validation score: {score:.2f}; Justification: {justification}")

        return score, justification
    else:
        return None, None

# Пример использования
if __name__ == '__main__':
    # Создаем экземпляр TinyPerson (или используем существующий)
    class Config:
        name:str = 'ExamplePerson'

    person = TinyPerson(Config())

    # Запускаем валидацию
    score, justification = validate_tiny_person(person, expectations="Must be friendly and helpful.")

    if score is not None:
        print(f"Validation Score: {score}")
        print(f"Justification: {justification}")
    else:
        print("Validation failed.")