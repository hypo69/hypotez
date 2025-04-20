## \file /src/utils/string/string_for_train.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Функция возвращает данные как одну строку.
===========================================
**Назначение**
Функция очищает введенные данные для подготовки датасета

Символы `"` экранированы и удалены повторяющиеся пробелы.
.. module:: src.utils.string.string_for_train
"""

import re

def string_for_train(data):
    """
    Очищает и форматирует данные для обучения. Удаляет повторяющиеся пробелы.

    Args:
        data (str or list): Входные данные, строка или список строк.

    Returns:
        str: Очищенная строка, готовая для использования в обучении.  Возвращает пустую строку, если входные данные некорректны.
    """
    if isinstance(data, str):
        cleaned_data = data.replace('"', '\\"')  # Экранирование кавычек
        cleaned_data = re.sub(r'\s+', ' ', cleaned_data).strip() # Удаление повторяющихся пробелов и обрезка пробелов с краёв
        return cleaned_data
    elif isinstance(data, list):
        cleaned_data = [item.replace('"', '\\"') for item in data]
        cleaned_data = ' '.join(cleaned_data) # объединение элементов списка в одну строку через пробел
        cleaned_data = re.sub(r'\s+', ' ', cleaned_data).strip() # Удаление повторяющихся пробелов и обрезка пробелов с краёв
        return cleaned_data
    else:
        return "" #Возврат пустой строки для некорректного типа данных