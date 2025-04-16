### Анализ кода модуля `llm.py`

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая структура функций и классов.
  - Использование декораторов для расширения функциональности.
  - Обработка исключений с логированием.
- **Минусы**:
  - Отсутствуют аннотации типов для всех переменных.
  - Не везде используется `logger` для логирования ошибок.
  - В некоторых местах можно улучшить читаемость кода.

**Рекомендации по улучшению**:

1. **Добавить аннотации типов**:
   - Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений, где они отсутствуют.
   - Пример:
     ```python
     def extract_json(text: str) -> dict:
         ...
     ```

2. **Улучшить логирование**:
   - Убедиться, что все ошибки логируются с использованием `logger.error` и передачей исключения `ex` и `exc_info=True`.
   - Пример:
     ```python
     except Exception as ex:
         logger.error(f"Error occurred while extracting JSON: {ex}", ex, exc_info=True)
     ```

3. **Использовать одинарные кавычки**:
   - Заменить двойные кавычки на одинарные, где это необходимо для соответствия стандартам.
   - Пример:
     ```python
     user_prompt = 'EXECUTE THE INSTRUCTIONS BELOW:\\n\\n ' + result
     ```

4. **Перефразировать docstrings**:
   - Сделать docstrings более подробными и понятными, следуя рекомендациям по стилю.
   - Вместо расплывчатых терминов, таких как "получаем" или "делаем", использовать более точные описания: "извлекаем", "проверяем", "выполняем".
  
5. **Упростить чтение файлов**:
   - Использовать `j_loads` или `j_loads_ns` для чтения JSON файлов.

6. **Документация**:
   -  Добавить заголовок файла с кратким описанием его содержимого
   -  Для всех классов и функций используйте docstring на русском языке

**Оптимизированный код**:

```python
"""
Модуль содержит утилиты для работы с LLM (Large Language Models).
==================================================================

Этот модуль предоставляет функции для составления запросов к LLM, извлечения информации из ответов моделей,
управления повторными вызовами при ошибках и обработки переменных шаблонов для RAI (Responsible AI).
"""

import re
import json
import os
import chevron
from typing import Collection, Optional, List, Dict, Any
import copy
import functools
import inspect
from tinytroupe.openai_utils import LLMRequest

from tinytroupe.utils import logger
from tinytroupe.utils.rendering import break_text_at_length


################################################################################
# Model input utilities
################################################################################


def compose_initial_LLM_messages_with_templates(
    system_template_name: str,
    user_template_name: Optional[str] = None,
    base_module_folder: Optional[str] = None,
    rendering_configs: Dict[str, Any] = {},
) -> list:
    """
    Составляет начальные сообщения для вызова LLM-модели, предполагая, что всегда используется
    системное сообщение (общее описание задачи) и опциональное пользовательское сообщение (специфическое описание задачи).
    Эти сообщения составляются с использованием указанных шаблонов и конфигураций рендеринга.

    Args:
        system_template_name (str): Имя шаблона системного сообщения.
        user_template_name (Optional[str]): Имя шаблона пользовательского сообщения. По умолчанию `None`.
        base_module_folder (Optional[str]): Базовая папка модуля. По умолчанию `None`.
        rendering_configs (Dict[str, Any]): Конфигурации рендеринга. По умолчанию `{}`.

    Returns:
        list: Список сообщений для LLM.
    """
    # ../ to go to the base library folder, because that's the most natural reference point for the user
    # ../ - для перехода в базовую папку библиотеки, так как это наиболее естественная точка отсчета для пользователя
    if base_module_folder is None:
        sub_folder =  '../prompts/'
    else:
        sub_folder = f'../{base_module_folder}/prompts/'

    base_template_folder = os.path.join(os.path.dirname(__file__), sub_folder)

    system_prompt_template_path = os.path.join(base_template_folder, f'{system_template_name}')
    user_prompt_template_path = os.path.join(base_template_folder, f'{user_template_name}')

    messages = []

    messages.append({'role': 'system',
                         'content': chevron.render(
                             open(system_prompt_template_path).read(),
                             rendering_configs)})

    # optionally add a user message
    # опционально добавить пользовательское сообщение
    if user_template_name is not None:
        messages.append({'role': 'user',
                            'content': chevron.render(
                                    open(user_prompt_template_path).read(),
                                    rendering_configs)})
    return messages


def llm(**model_overrides: Dict[str, Any]):
    """
    Декоратор, преобразующий декорируемую функцию в функцию, основанную на LLM.
    Декорируемая функция должна либо возвращать строку (инструкцию для LLM),
    либо параметры функции будут использоваться в качестве инструкции для LLM.
    Ответ LLM приводится к аннотированному типу возвращаемого значения функции, если он присутствует.

    Args:
        **model_overrides (Dict[str, Any]): Переопределения параметров модели.

    Returns:
        decorator: Декоратор для преобразования функции в LLM-функцию.

    Usage example:
    @llm(model='gpt-4-0613', temperature=0.5, max_tokens=100)
    def joke():
        return "Tell me a joke."
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            sig = inspect.signature(func)
            return_type = sig.return_annotation if sig.return_annotation != inspect.Signature.empty else str
            system_prompt = func.__doc__.strip() if func.__doc__ else 'You are an AI system that executes a computation as requested.'

            if isinstance(result, str):
                user_prompt = 'EXECUTE THE INSTRUCTIONS BELOW:\\n\\n ' + result
            else:
                user_prompt = f'Execute your function as best as you can using the following parameters: {kwargs}'

            llm_req = LLMRequest(system_prompt=system_prompt,
                                 user_prompt=user_prompt,
                                 output_type=return_type,
                                 **model_overrides)
            return llm_req.call()
        return wrapper
    return decorator


################################################################################
# Model output utilities
################################################################################
def extract_json(text: str) -> dict:
    """
    Извлекает JSON-объект из строки, игнорируя: любой текст до первой
    открывающей фигурной скобки; и любые открывающие (```json) или закрывающие (```) теги Markdown.

    Args:
        text (str): Строка для извлечения JSON.

    Returns:
        dict: Извлеченный JSON-объект.
    """
    try:
        # remove any text before the first opening curly or square braces, using regex. Leave the braces.
        # удалить любой текст перед первой открывающей фигурной или квадратной скобкой, используя regex. Оставить скобки.
        text = re.sub(r'^.*?({|\\[)', r'\\1', text, flags=re.DOTALL)

        # remove any trailing text after the LAST closing curly or square braces, using regex. Leave the braces.
        # удалить любой текст после ПОСЛЕДНЕЙ закрывающей фигурной или квадратной скобки, используя regex. Оставить скобки.
        text  =  re.sub(r'(}|\\])(?!.*(\\]|\\})).*$', r'\\1', text, flags=re.DOTALL)

        # remove invalid escape sequences, which show up sometimes
        # удалить недопустимые escape-последовательности, которые иногда появляются
        text = re.sub('\\\\\'', '\'', text)  # replace \\' with just '
        text = re.sub('\\\\,', ',', text)

        # use strict=False to correctly parse new lines, tabs, etc.
        # использовать strict=False для корректного разбора новых строк, табуляции и т.д.
        parsed = json.loads(text, strict=False)

        # return the parsed JSON object
        # вернуть разобранный JSON-объект
        return parsed

    except Exception as ex:
        logger.error(f'Error occurred while extracting JSON: {ex}', ex, exc_info=True)
        return {}


def extract_code_block(text: str) -> str:
    """
    Извлекает блок кода из строки, игнорируя любой текст перед первым
    открывающим тройным обратным апострофом и любой текст после закрывающего тройного обратного апострофа.

    Args:
        text (str): Строка для извлечения блока кода.

    Returns:
        str: Извлеченный блок кода.
    """
    try:
        # remove any text before the first opening triple backticks, using regex. Leave the backticks.
        # удалить любой текст перед первым открывающим тройным обратным апострофом, используя regex. Оставить апострофы.
        text = re.sub(r'^.*?(```)', r'\\1', text, flags=re.DOTALL)

        # remove any trailing text after the LAST closing triple backticks, using regex. Leave the backticks.
        # удалить любой текст после ПОСЛЕДНЕГО закрывающего тройного обратного апострофа, используя regex. Оставить апострофы.
        text  =  re.sub(r'(```)(?!.*```).*$', r'\\1', text, flags=re.DOTALL)

        return text

    except Exception as ex:
        logger.error(f'Error occurred while extracting code block: {ex}', ex, exc_info=True)
        return ''


################################################################################
# Model control utilities
################################################################################


def repeat_on_error(retries: int, exceptions: list):
    """
    Декоратор, который повторяет вызов указанной функции, если возникает исключение
    из числа указанных, до указанного количества повторных попыток.
    Если это количество повторных попыток превышено, исключение вызывается.
    Если исключение не возникает, функция возвращается в обычном режиме.

    Args:
        retries (int): Количество повторных попыток.
        exceptions (list): Список классов исключений для перехвата.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as ex:
                    logger.debug(f'Exception occurred: {ex}')
                    if i == retries - 1:
                        raise ex
                    else:
                        logger.debug(f'Retrying ({i+1}/{retries})...')
                        continue
        return wrapper
    return decorator


################################################################################
# Prompt engineering
################################################################################


def add_rai_template_variables_if_enabled(template_variables: dict) -> dict:
    """
    Добавляет переменные шаблона RAI в указанный словарь, если включены дисклеймеры RAI.
    Они могут быть настроены в файле config.ini. Если включены, переменные будут загружать
    дисклеймеры RAI из соответствующих файлов в каталоге prompts. В противном случае переменные будут установлены в None.

    Args:
        template_variables (dict): Словарь переменных шаблона, в который нужно добавить переменные RAI.

    Returns:
        dict: Обновленный словарь переменных шаблона.
    """
    from tinytroupe import config  # avoids circular import

    rai_harmful_content_prevention = config['Simulation'].getboolean(
        'RAI_HARMFUL_CONTENT_PREVENTION', True
    )
    rai_copyright_infringement_prevention = config['Simulation'].getboolean(
        'RAI_COPYRIGHT_INFRINGEMENT_PREVENTION', True
    )

    # Harmful content
    # Вредный контент
    with open(os.path.join(os.path.dirname(__file__), 'prompts/rai_harmful_content_prevention.md'), 'r') as f:
        rai_harmful_content_prevention_content = f.read()

    template_variables['rai_harmful_content_prevention'] = rai_harmful_content_prevention_content if rai_harmful_content_prevention else None

    # Copyright infringement
    # Нарушение авторских прав
    with open(os.path.join(os.path.dirname(__file__), 'prompts/rai_copyright_infringement_prevention.md'), 'r') as f:
        rai_copyright_infringement_prevention_content = f.read()

    template_variables['rai_copyright_infringement_prevention'] = rai_copyright_infringement_prevention_content if rai_copyright_infringement_prevention else None

    return template_variables


################################################################################
# Truncation
################################################################################


def truncate_actions_or_stimuli(list_of_actions_or_stimuli: Collection[dict], max_content_length: int) -> Collection[str]:
    """
    Усекает контент действий или стимулов до указанной максимальной длины. Не изменяет исходный список.

    Args:
        list_of_actions_or_stimuli (Collection[dict]): Список действий или стимулов для усечения.
        max_content_length (int): Максимальная длина контента.

    Returns:
        Collection[str]: Усеченный список действий или стимулов. Это новый список, а не ссылка на исходный список,
        чтобы избежать неожиданных побочных эффектов.
    """
    cloned_list = copy.deepcopy(list_of_actions_or_stimuli)

    for element in cloned_list:
        # the external wrapper of the LLM message: {'role': ..., 'content': ...}
        # внешний обертка сообщения LLM: {'role': ..., 'content': ...}
        if 'content' in element:
            msg_content = element['content']

            # now the actual action or stimulus content
            # теперь фактическое содержание действия или стимула

            # has action, stimuli or stimulus as key?
            # есть ли action, stimuli или stimulus в качестве ключа?
            if 'action' in msg_content:
                # is content there?
                # есть ли там контент?
                if 'content' in msg_content['action']:
                    msg_content['action']['content'] = break_text_at_length(msg_content['action']['content'], max_content_length)
            elif 'stimulus' in msg_content:
                # is content there?
                # есть ли там контент?
                if 'content' in msg_content['stimulus']:
                    msg_content['stimulus']['content'] = break_text_at_length(msg_content['stimulus']['content'], max_content_length)
            elif 'stimuli' in msg_content:
                # for each element in the list
                # для каждого элемента в списке
                for stimulus in msg_content['stimuli']:
                    # is content there?
                    # есть ли там контент?
                    if 'content' in stimulus:
                        stimulus['content'] = break_text_at_length(stimulus['content'], max_content_length)

    return cloned_list