### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для получения списка путей к изображениям, сгенерированных ИИ, в определенной директории (`kazarinov/converted_images/pastel`). Он использует функции `recursively_get_filepath` для рекурсивного поиска файлов с расширениями `.jpeg`, `.jpg` и `.png` в указанной директории и поддиректориях. Затем, с помощью функции `pprint`, найденные пути к изображениям выводятся в консоль.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модуль `header` (предположительно, для обработки заголовков запросов).
   - Импортируется модуль `gs` (предположительно, содержащий глобальные пути).
   - Импортируются функции `read_text_file` и `save_text_file` из модуля `src.utils.file` (для чтения и сохранения текстовых файлов соответственно).
   - Импортируется функция `recursively_get_filepath` из модуля `src.utils.file` (для рекурсивного поиска файлов в директории).
   - Импортируется функция `pprint` из модуля `src.utils.printer` (для форматированного вывода данных).

2. **Определение пути к директории с изображениями**:
   - Переменной `images_path` присваивается результат вызова функции `recursively_get_filepath`. Функция принимает два аргумента:
     - Путь к директории, в которой нужно искать изображения: `gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel'`. Здесь `gs.path.external_data` – это базовый путь, к которому добавляются поддиректории.
     - Список расширений файлов, которые нужно искать: `['*.jpeg', '*.jpg', '*.png']`.

3. **Вывод списка путей к изображениям**:
   - Функция `pprint(images_path)` выводит список путей к найденным изображениям в консоль в удобном для чтения формате.

Пример использования
-------------------------

```python
## \file /src/endpoints/kazarinov/_experiments/get_images.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3
"""
Список картинок, сгенерированный ИИ
====================================

.. module:: src.endpoints.kazarinov._experiments 
	:platform: Windows, Unix
	:synopsis:

"""


import header
from src import gs
from src.utils.file import read_text_file, save_text_file, recursively_get_filepath
from src.utils.printer import pprint
from pathlib import Path

# Для тестирования
class gs:
    class path:
        external_data = Path('./data')  # Замените на реальный путь при необходимости

# Создаем структуру директорий для тестирования
(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel').mkdir(parents=True, exist_ok=True)
# Создаем несколько файлов для тестирования
(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel' / 'image1.jpeg').touch()
(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel' / 'image2.jpg').touch()
(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel' / 'image3.png').touch()
(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel' / 'not_an_image.txt').touch()

images_path = recursively_get_filepath(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel', ['*.jpeg','*.jpg','*.png'])
pprint(images_path)
...