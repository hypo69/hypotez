## \file /src/___beeryakov/_experiments/file_counter_ru.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.___beeryakov._experiments 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.___beeryakov._experiments """


import os

def count_lines_in_files(directory):
    """
     Рекурсивно подсчитывает количество строк в текстовых файлах в указанной директории и ее поддиректориях, а также количество классов и функций.
    
    @param directory: Путь к директории
    @return: Общее количество строк в текстовых файлах, количество классов и количество функций
    """
    total_lines = 0
    total_classes = 0
    total_functions = 0
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.iStringFormatterile(filepath):
            # Проверка, является ли файл текстовым и не является ли файл из папок __pycache__ и firefox_profiles
            if not is_binary(filepath) and not filepath.endswith(('__pycache__', 'firefox_profiles')) and filename != '__init__.py':
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    lines_in_file = sum(1 for line in file)
                    total_lines += lines_in_file
                    total_classes_in_file, total_functions_in_file = count_classes_and_functions(filepath)
                    total_classes += total_classes_in_file
                    total_functions += total_functions_in_file
        elif os.path.isdir(filepath):
            # Если это директория, рекурсивно вызываем функцию для подсчета строк, классов и функций в ней
            nested_lines, nested_classes, nested_functions = count_lines_in_files(filepath)
            total_lines += nested_lines
            total_classes += nested_classes
            total_functions += nested_functions
    return total_lines, total_classes, total_functions

def is_binary(filepath):
    """
     Проверяет, является ли файл бинарным.
    
    @param filepath: Путь к файлу
    @return: True, если файл бинарный, иначе False
    """
    try:
        with open(filepath, 'rb') as file:
            # Читаем первые 512 байт файла для проверки наличия нулевых байтов
            chunk = file.read(512)
            return b'\0' in chunk
    except Exception as e:
        # Если возникает ошибка при чтении файла, считаем его бинарным
        print(f"Ошибка при чтении файла '{filepath}': {e}")
        return True

def count_classes_and_functions(filepath):
    """
     Подсчитывает количество классов и функций в файле.
    
    @param filepath: Путь к файлу
    @return: Количество классов и количество функций
    """
    total_classes = 0
    total_functions = 0
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            # Проверка, начинается ли строка с ключевого слова "class"
            if line.strip().startswith('class'):
                total_classes += 1
            # Проверка, начинается ли строка с ключевого слова "def"
            elif line.strip().startswith('def'):
                total_functions += 1
    return total_classes, total_functions

if __name__ == "__main__":
    src_directory = 'src'
    print(f"Подсчет строк, классов и функций в файлах в директории: {src_directory}")
    total_lines, total_classes, total_functions = count_lines_in_files(src_directory)
    print(f"Всего строк в текстовых файлах в '{src_directory}': {total_lines}")
    print(f"Всего классов: {total_classes}")
    print(f"Всего функций: {total_functions}")

