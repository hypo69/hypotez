## \file /src/___beeryakov/_experiments/create_translated_src.py
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



""" Переводчик комментариев кода.  """
...
import os
import shutil
import chardet

def detect_language(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        if encoding and 'utf-8' in encoding.lower():
            return 'utf-8'
        return

def copy_and_print_russian_text(src_dir, dest_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_path = os.path.join(root, file)
            dest_path = os.path.join(dest_dir, os.path.relpath(src_path, src_dir))
            
            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))
            
            shutil.copyfile(src_path, dest_path)
            
            language = detect_language(src_path)
            if language == 'utf-8':
                with open(src_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    print("Russian Text in", src_path)
                    print(text)

def main():
    # Путь к исходной папке
    src_folder = 'src'

    # Путь к папке, в которую будем копировать файлы
    dest_folder = 'src_en'

    # Вызываем функцию для копирования и вывода текста на русском языке
    copy_and_print_russian_text(src_folder, dest_folder)

if __name__ == "__main__":
    main()

