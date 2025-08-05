## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код демонстрирует процесс преобразования HTML-файла в текстовый файл. Он считывает HTML-код из файла, преобразует его в текст и затем сохраняет текст в новый файл.

Шаги выполнения
-------------------------
1. **Считывание HTML-кода:**
   - Задается путь к файлу `index.html`, расположенному в директории `html2text` на Google Drive.
   - Функция `read_text_file` считывает содержимое файла и возвращает его в виде строки.
2. **Преобразование HTML в текст:**
   - Функция `html2text` преобразует полученный HTML-код в текст, удаляя все теги и форматирование.
3. **Сохранение текста в файл:**
   - Задается путь к файлу `index.txt`, расположенному в директории `html2text` на Google Drive.
   - Функция `save_text_file` сохраняет полученный текстовый файл в указанном месте.

Пример использования
-------------------------

```python
    ## \file /src/utils/convertors/_experiments/html2text.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.utils.convertors._experiments 
\t:platform: Windows, Unix
\t:synopsis:

"""


"""
\t:platform: Windows, Unix
\t:synopsis:

"""

"""
\t:platform: Windows, Unix
\t:synopsis:

"""

"""
\t:platform: Windows, Unix
\t:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  

""" module: src.utils.convertors._experiments """


""" HERE SHOULD BE A DESCRIPTION OF THE MODULE OPERATION ! """

import header
from src import gs
from src.utils.convertors import html2text, html2text_file
from src.utils.file import read_text_file, save_text_file

html = read_text_file(gs.path.google_drive / 'html2text' / 'index.html')
text_from_html = html2text(html)
save_text_file(text_from_html, gs.path.google_drive / 'html2text' / 'index.txt')
...
```