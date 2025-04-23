### **Инструкция: Функция `_remove_outer_quotes`**

=========================================================================================

Описание
-------------------------
Функция `_remove_outer_quotes` удаляет внешние кавычки из входной строки, если строка начинается с определенных префиксов, указанных в `Config.remove_prefixes`. Если строка начинается с ````python` или ````mermaid`, то она возвращается без изменений.

Шаги выполнения
-------------------------
1. **Удаление пробельных символов**: Сначала удаляются пробельные символы в начале и конце входной строки `response`.
2. **Проверка на кодовые блоки**: Если строка начинается с ````python` или ````mermaid`, то она возвращается без изменений, так как это указывает на блок кода.
3. **Удаление префиксов**: Для каждого префикса в `Config.remove_prefixes` выполняется проверка, начинается ли строка с этого префикса (без учета регистра). Если да, то префикс удаляется.
4. **Удаление суффикса**: Если после удаления префикса строка заканчивается на `````, этот суффикс также удаляется.
5. **Возврат результата**: Если ни одно из условий не выполнено, возвращается исходная строка без изменений.

Пример использования
-------------------------

```python
from pathlib import Path
from typing import Iterator, List, Optional
from types import SimpleNamespace
import re

from src.logger.logger import logger
from src.utils.jjson import j_loads_ns

class Config:
    ENDPOINT: Path = Path(__file__).parent
    config: SimpleNamespace = j_loads_ns(ENDPOINT / 'code_assistant.json')
    remove_prefixes: list = config.remove_prefixes

def _remove_outer_quotes(response: str) -> str:
    """
    Удаляет внешние кавычки в начале и в конце строки, если они присутствуют.

    Args:
        response (str): Ответ модели, который необходимо обработать.

    Returns:
        str: Очищенный контент как строка.

    Example:
        >>> _remove_outer_quotes('```md some content ```')
        'some content'
        >>> _remove_outer_quotes('some content')
        'some content'
        >>> _remove_outer_quotes('```python def hello(): print("Hello") ```')
        '```python def hello(): print("Hello") ```'
    """
    try:
        response = response.strip()
    except Exception as ex:
        logger.error('Exception in `_remove_outer_quotes()`', ex, False)
        return ''

    # Если строка начинается с '```python' или '```mermaid', возвращаем её без изменений. Это годный код
    if response.startswith(('```python', '```mermaid')) or not response:
        return response

    for prefix in Config.remove_prefixes:
        # Сравнение с префиксом без учёта регистра
        if response.lower().startswith(prefix.lower()):
            # Удаляем префикс и суффикс "```", если он есть
            cleaned_response = response[len(prefix) :].strip()
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[: -len('```')].strip()
            return cleaned_response

    # Возврат строки без изменений, если условия не выполнены
    return response

# Пример использования
response1 = '```md some content ```'
response2 = 'some content'
response3 = '```python def hello(): print("Hello") ```'

Config.remove_prefixes = ['```md']

print(_remove_outer_quotes(response1))
print(_remove_outer_quotes(response2))
print(_remove_outer_quotes(response3))