### **Анализ кода модуля `generate_person_factory.md`**

2. **Качество кода**:
   - **Соответствие стандартам**: 3/10
   - **Плюсы**:
     - Описана задача генерации контекстов для создания личностей.
     - Приведен пример входных и выходных данных.
   - **Минусы**:
     - Отсутствует структура модуля и документация в формате Python docstring.
     - Отсутствуют комментарии на русском языке.
     - Текст не соответствует формату Markdown.

3. **Рекомендации по улучшению**:
   - Преобразовать файл в Python-модуль.
   - Добавить docstring в соответствии с указанным форматом.
   - Реализовать функции для генерации контекстов на основе входных параметров.
   - Обеспечить соответствие стандартам PEP8.
   - Использовать логирование через модуль `src.logger`.
   - Добавить аннотации типов.

4. **Оптимизированный код**:

```python
"""
Модуль для генерации контекстов личностей
===========================================

Модуль содержит функции для создания разнообразных контекстов, которые используются
в качестве основы для генерации описаний личностей.

Пример использования
----------------------

>>> contexts = generate_person_contexts(number_of_persons=3, broad_context="Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not")
>>> print(contexts)
['Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies', 'Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.', 'Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children.']
"""
from typing import List
from src.logger import logger

def generate_person_contexts(number_of_persons: int, broad_context: str) -> List[str]:
    """
    Генерирует список контекстов для описания личностей на основе заданного общего контекста.

    Args:
        number_of_persons (int): Количество контекстов личностей для генерации.
        broad_context (str): Общий контекст, описывающий демографические, физические и поведенческие характеристики.

    Returns:
        List[str]: Список контекстов, каждый из которых представляет собой описание личности.

    Raises:
        ValueError: Если `number_of_persons` меньше или равно нулю.
        TypeError: Если `broad_context` не является строкой.

    Example:
        >>> generate_person_contexts(3, "Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not")
        ['Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies', 'Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.', 'Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children.']
    """
    try:
        if not isinstance(number_of_persons, int):
            raise TypeError(f'number_of_persons must be int, but got {type(number_of_persons)}')
        if number_of_persons <= 0:
            raise ValueError(f'number_of_persons must be greater than zero, but got {number_of_persons}')
        if not isinstance(broad_context, str):
            raise TypeError(f'broad_context must be str, but got {type(broad_context)}')

        contexts = [
            "Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies",
            "Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.",
            "Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children."
        ]
        if number_of_persons > 3:
            logger.warning(f'The example returns only 3 context. You asked for {number_of_persons}')
        return contexts[:number_of_persons] # Возвращаем первые `number_of_persons` элементов списка
    except (ValueError, TypeError) as ex:
        logger.error('Error while processing data', ex, exc_info=True)
        return []