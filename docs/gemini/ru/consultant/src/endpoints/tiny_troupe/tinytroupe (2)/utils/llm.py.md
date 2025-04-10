### **Анализ кода модуля `llm.py`**

**Расположение файла в проекте:** `hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/utils/llm.py`

**Описание модуля:**
Модуль содержит утилиты для работы с большими языковыми моделями (LLM), включая функции для составления запросов, извлечения данных из ответов и управления повторными попытками при ошибках.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура модуля, разделение на логические блоки (Model input utilities, Model output utilities, Model control utilities, Prompt engineering, Truncation).
    - Использование декораторов для упрощения работы с LLM.
    - Реализация повторных попыток при ошибках.
    - Документирование основных функций.
- **Минусы**:
    - Отсутствуют аннотации типов для некоторых параметров и возвращаемых значений.
    - Не все функции имеют подробные docstring.
    - В некоторых местах используются устаревшие конструкции (например, `Union` вместо `|`).
    - Не везде используется `logger` для логирования ошибок.
    - В функциях `extract_json` и `extract_code_block` обработка исключений не содержит информации об ошибке, что затрудняет отладку.
    - В функции `add_rai_template_variables_if_enabled` файлы открываются и читаются напрямую, что не соответствует требованию использования `j_loads` или `j_loads_ns`.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Для всех параметров функций и возвращаемых значений добавить аннотации типов.
    - Заменить `Union` на `|` в аннотациях типов.
2.  **Улучшить документацию**:
    - Добавить подробные docstring для всех функций, включая описание параметров, возвращаемых значений и возможных исключений.
    - Перевести docstring на русский язык.
    - Использовать более конкретные глаголы в описаниях (например, "извлекает" вместо "получает").
3.  **Логирование**:
    - Использовать `logger.error` с передачей информации об исключении (`ex`) и трассировкой (`exc_info=True`) во всех блоках `except`.
4.  **Обработка файлов конфигурации**:
    - Заменить прямое открытие и чтение файлов в функции `add_rai_template_variables_if_enabled` на использование `j_loads` или `j_loads_ns`.
5.  **Улучшить обработку исключений**:
    - В функциях `extract_json` и `extract_code_block` добавить логирование ошибок с использованием `logger.error`, чтобы было проще отлаживать проблемы.
6.  **Использовать одинарные кавычки**:
    - Привести весь код к использованию одинарных кавычек.
7. **Удалить неиспользуемые импорты**:
    - Убрать из импортов `functools`

**Оптимизированный код:**

```python
import re
import json
import os
import chevron
from typing import Collection, Optional, List, Dict, Any
import copy
import inspect
from src.endpoints.tiny_troupe.tinytroupe__2_.utils.openai_utils import LLMRequest # Исправлен импорт
from src.logger import logger
from src.endpoints.tiny_troupe.tinytroupe__2_.utils.rendering import break_text_at_length

"""
Модуль для работы с большими языковыми моделями (LLM)
=======================================================

Модуль содержит утилиты для взаимодействия с LLM, включая функции для:
- Составления запросов на основе шаблонов.
- Извлечения данных из ответов LLM (JSON, код).
- Управления повторными попытками при возникновении ошибок.
- Добавления переменных для управления ответственностью ИИ (RAI).
- Усечения длинных текстов.

Пример использования:
----------------------
>>> from src.endpoints.tiny_troupe.tinytroupe__2_.utils.llm import compose_initial_LLM_messages_with_templates
>>> messages = compose_initial_LLM_messages_with_templates('system_template.md', 'user_template.md', rendering_configs={'variable': 'value'})
>>> print(messages)
"""

################################################################################
# Model input utilities
################################################################################

def compose_initial_LLM_messages_with_templates(system_template_name: str, user_template_name: Optional[str] = None,
                                                base_module_folder: Optional[str] = None,
                                                rendering_configs: Dict[str, Any] = {}) -> List[Dict[str, str]]:
    """
    Составляет начальные сообщения для вызова LLM, предполагая наличие системного (общее описание задачи)
    и необязательного пользовательского сообщения (специфическое описание задачи).
    Сообщения составляются с использованием указанных шаблонов и конфигураций рендеринга.

    Args:
        system_template_name (str): Имя файла шаблона системного сообщения.
        user_template_name (Optional[str], optional): Имя файла шаблона пользовательского сообщения. По умолчанию None.
        base_module_folder (Optional[str], optional): Базовая папка модуля. По умолчанию None.
        rendering_configs (Dict[str, Any], optional): Конфигурации рендеринга. По умолчанию {}.

    Returns:
        List[Dict[str, str]]: Список сообщений для LLM, где каждое сообщение - словарь с ключами "role" и "content".

    Example:
        >>> messages = compose_initial_LLM_messages_with_templates('system_template.md', 'user_template.md', rendering_configs={'variable': 'value'})
        >>> print(messages)
        [{'role': 'system', 'content': 'System message content'}, {'role': 'user', 'content': 'User message content'}]
    """
    # определяем подпапку
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

    # опционально добавляем пользовательское сообщение
    if user_template_name is not None:
        messages.append({'role': 'user',
                            'content': chevron.render(
                                    open(user_prompt_template_path).read(),
                                    rendering_configs)})
    return messages


def llm(**model_overrides: Dict[str, Any]):
    """
    Декоратор, который превращает декорируемую функцию в функцию, основанную на LLM.
    Декорируемая функция должна либо возвращать строку (инструкцию для LLM),
    либо параметры функции будут использоваться в качестве инструкции для LLM.
    Ответ LLM приводится к аннотированному типу возврата функции, если он присутствует.

    Args:
        **model_overrides (Dict[str, Any]): Переопределения параметров модели LLM.

    Returns:
        Callable: Декоратор, который принимает функцию и возвращает обертку над ней.

    Usage example:
    @llm(model='gpt-4-0613', temperature=0.5, max_tokens=100)
    def joke() -> str:
        return 'Tell me a joke.'
    """
    def decorator(func):
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
    Извлекает JSON-объект из строки, игнорируя: любой текст до первой открывающей фигурной скобки;
    и любые открывающие (```json) или закрывающие (```) теги Markdown.

    Args:
        text (str): Строка, из которой нужно извлечь JSON.

    Returns:
        dict: Извлеченный JSON-объект или пустой словарь в случае ошибки.
    
    Raises:
        json.JSONDecodeError: Если не удается декодировать JSON.

    Example:
        >>> extract_json('```json\\n{\'key\': \'value\'}\\n```')
        {'key': 'value'}
    """
    try:
        # удаляем любой текст перед первой открывающей фигурной или квадратной скобкой, используя regex. Оставляем скобки.
        text = re.sub(r'^.*?({|\[)', r'\1', text, flags=re.DOTALL)

        # удаляем любой завершающий текст после ПОСЛЕДНЕЙ закрывающей фигурной или квадратной скобки, используя regex. Оставляем скобки.
        text  =  re.sub(r'(}|\])(?!.*(\]|}))', r'\1', text, flags=re.DOTALL)

        # удаляем недопустимые escape-последовательности, которые иногда появляются
        text = re.sub('\\\\\'', '\'', text) # заменяем \\\' на просто \'
        text = re.sub('\\\\,', ',', text)

        # используем strict=False для правильного разбора новых строк, табуляции и т.д.
        parsed = json.loads(text, strict=False)

        # возвращаем разобранный JSON-объект
        return parsed

    except json.JSONDecodeError as ex:
        logger.error('Ошибка при извлечении JSON', ex, exc_info=True)
        return {}


def extract_code_block(text: str) -> str:
    """
    Извлекает блок кода из строки, игнорируя любой текст перед первыми открывающими тройными обратными кавычками
    и любой текст после закрывающих тройных обратных кавычек.

    Args:
        text (str): Строка, из которой нужно извлечь блок кода.

    Returns:
        str: Извлеченный блок кода или пустая строка в случае ошибки.
    
    Example:
        >>> extract_code_block('```python\\nprint(\'Hello\')\\n```')
        '```python\\nprint(\'Hello\')\\n```'
    """
    try:
        # удаляем любой текст перед первыми открывающими тройными обратными кавычками, используя regex. Оставляем кавычки.
        text = re.sub(r'^.*?(```)', r'\1', text, flags=re.DOTALL)

        # удаляем любой завершающий текст после ПОСЛЕДНИХ закрывающих тройных обратных кавычек, используя regex. Оставляем кавычки.
        text  =  re.sub(r'(```)(?!.*```).*$', r'\1', text, flags=re.DOTALL)

        return text

    except Exception as ex:
        logger.error('Ошибка при извлечении блока кода', ex, exc_info=True)
        return ''

################################################################################
# Model control utilities
################################################################################
def repeat_on_error(retries: int, exceptions: List[Exception]):
    """
    Декоратор, который повторяет вызов указанной функции, если возникает исключение из числа указанных,
    до указанного количества повторных попыток. Если это количество попыток превышено, исключение вызывается.
    Если исключение не возникает, функция возвращается нормально.

    Args:
        retries (int): Количество повторных попыток.
        exceptions (List[Exception]): Список классов исключений, которые нужно перехватывать.

    Returns:
        Callable: Декоратор, который принимает функцию и возвращает обертку над ней.
    
    Raises:
        Exception: Если количество повторных попыток превышено.
    
    Example:
        >>> @repeat_on_error(retries=3, exceptions=[ValueError])
        ... def my_function(x):
        ...     if x < 0:
        ...         raise ValueError('x должен быть положительным')
        ...     return x * 2
        >>> my_function(5)
        10
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as ex:
                    logger.debug(f'Произошло исключение: {ex}')
                    if i == retries - 1:
                        raise ex
                    else:
                        logger.debug(f'Повторная попытка ({i+1}/{retries})...')
                        continue
        return wrapper
    return decorator

################################################################################
# Prompt engineering
################################################################################
def add_rai_template_variables_if_enabled(template_variables: Dict[str, Any]) -> Dict[str, Any]:
    """
    Добавляет переменные шаблона RAI в указанный словарь, если включены отказы от ответственности RAI.
    Они могут быть настроены в файле config.ini. Если они включены, переменные будут загружать отказы от ответственности RAI
    из соответствующих файлов в каталоге prompts. В противном случае переменные будут установлены в None.

    Args:
        template_variables (Dict[str, Any]): Словарь переменных шаблона, в который нужно добавить переменные RAI.

    Returns:
        Dict[str, Any]: Обновленный словарь переменных шаблона.
    """
    from src.config import config # избегаем циклический импорт
    rai_harmful_content_prevention = config['Simulation'].getboolean(
        'RAI_HARMFUL_CONTENT_PREVENTION', True
    )
    rai_copyright_infringement_prevention = config['Simulation'].getboolean(
        'RAI_COPYRIGHT_INFRINGEMENT_PREVENTION', True
    )

    # Harmful content
    # открываем и читаем содержимое файла с использованием j_loads
    template_variables['rai_harmful_content_prevention'] = j_loads(os.path.join(os.path.dirname(__file__), 'prompts/rai_harmful_content_prevention.md')) if rai_harmful_content_prevention else None

    # Copyright infringement
    # открываем и читаем содержимое файла с использованием j_loads
    template_variables['rai_copyright_infringement_prevention'] = j_loads(os.path.join(os.path.dirname(__file__), 'prompts/rai_copyright_infringement_prevention.md')) if rai_copyright_infringement_prevention else None

    return template_variables

################################################################################
# Truncation
################################################################################
def truncate_actions_or_stimuli(list_of_actions_or_stimuli: Collection[Dict[str, Any]], max_content_length: int) -> Collection[Dict[str, Any]]:
    """
    Усекает содержимое действий или стимулов до указанной максимальной длины. Не изменяет исходный список.

    Args:
        list_of_actions_or_stimuli (Collection[Dict[str, Any]]): Список действий или стимулов для усечения.
        max_content_length (int): Максимальная длина содержимого.

    Returns:
        Collection[Dict[str, Any]]: Усеченный список действий или стимулов. Это новый список, а не ссылка на исходный список,
        чтобы избежать непредвиденных побочных эффектов.
    """
    cloned_list = copy.deepcopy(list_of_actions_or_stimuli)

    for element in cloned_list:
        # внешняя обертка сообщения LLM: {'role': ..., 'content': ...}
        if 'content' in element:
            msg_content = element['content']

            # теперь фактическое содержание действия или стимула

            # имеет действие, стимулы или стимул в качестве ключа?
            if 'action' in msg_content:
                # есть ли там содержание?
                if 'content' in msg_content['action']:
                    msg_content['action']['content'] = break_text_at_length(msg_content['action']['content'], max_content_length)
            elif 'stimulus' in msg_content:
                # есть ли там содержание?
                if 'content' in msg_content['stimulus']:
                    msg_content['stimulus']['content'] = break_text_at_length(msg_content['stimulus']['content'], max_content_length)
            elif 'stimuli' in msg_content:
                # для каждого элемента в списке
                for stimulus in msg_content['stimuli']:
                    # есть ли там содержание?
                    if 'content' in stimulus:
                        stimulus['content'] = break_text_at_length(stimulus['content'], max_content_length)

    return cloned_list

def j_loads(path: str) -> str:
    """
    Функция обертка для json.load, открывает файл, считывает и декодирует JSON.
    """
    with open(path, 'r') as f:
        return json.load(f)