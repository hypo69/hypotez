### **Инструкции по использованию блока кода**

=========================================================================================

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет функции для преобразования цветовых форматов: из HEX в DECIMAL, из DECIMAL в HEX и из HEX в RGB.

Шаги выполнения
-------------------------
1. **HEX в DECIMAL**: 
   - Функция `hex_color_to_decimal(letters: str) -> int` принимает строку с HEX-цветом.
   - Преобразует каждый символ HEX-цвета в его DECIMAL представление.

2. **DECIMAL в HEX**:
   - Функция `decimal_color_to_hex(number: int) -> str` принимает число в DECIMAL формате.
   - Преобразует число в HEX-цвет.

3. **HEX в RGB**:
   - Функция `hex_to_rgb (hex: str) -> tuple` принимает строку с HEX-цветом.
   - Удаляет символ `#`, если он присутствует.
   - Разделяет HEX-цвет на компоненты Red, Green, Blue.
   - Преобразует каждый компонент в DECIMAL формат и возвращает в виде кортежа.

Пример использования
-------------------------

```python
from src.goog.spreadsheet.bberyakov.helpers import hex_color_to_decimal, decimal_color_to_hex, hex_to_rgb

# HEX в DECIMAL
hex_color = "A"
decimal_value = hex_color_to_decimal(hex_color)
print(f"HEX {hex_color} в DECIMAL: {decimal_value}")  # Вывод: HEX A в DECIMAL: 1

# DECIMAL в HEX
decimal_number = 27
hex_color = decimal_color_to_hex(decimal_number)
print(f"DECIMAL {decimal_number} в HEX: {hex_color}")  # Вывод: DECIMAL 27 в HEX: AA

# HEX в RGB
hex_color = "#FFFFFF"
rgb_tuple = hex_to_rgb(hex_color)
print(f"HEX {hex_color} в RGB: {rgb_tuple}")  # Вывод: HEX #FFFFFF в RGB: (255, 255, 255)
```
```python
## \file /src/goog/spreadsheet/bberyakov/helpers.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.goog.spreadsheet.bberyakov 
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
  
""" module: src.goog.spreadsheet.bberyakov """


""" перевод цветовых форматов.
Перевод:
- HEX->DECIMAL
- DECIMAL->HEX
- HEX->RGB

 @section libs imports:
 
Author(s):
  - Created by hypotez
"""


def hex_color_to_decimal(letters: str) -> int:
    """Перевод HEX->DECIMAL
    
    Args:
        letters (str): [description]
    Returns:
        int: [description]

    Example:
        >>> print(number_to_letter(1))  # Output: 'a' 
        >>> print(number_to_letter(2))  # Output: 'b' 
        >>> print(number_to_letter(3))  # Output: 'c' 
        >>> print(number_to_letter(27)) # Output: 'aa' 
        >>> print(number_to_letter(28)) # Output: 'ab' 
        >>> print(number_to_letter(29)) # Output: 'ac' 
    """
    letters = letters.upper()

    def letter_to_number(letter: str) -> int:
        """Функция преобразует букву в число

        Args:
            letter (str): [description]
        Returns:
            int: [description]
        """
        """
        ord() function returns the Unicode code from a given character. 

        print(ord('a'))  # Output: 97 

        """
        # Функция преобразует букву в число
        return str (ord (letter.lower()) - 96).upper()
    # Функция преобразует HEX в DECIMAL, если длина 1, иначе вызывает рекурсивно
    return letter_to_number(letters) if len(letters) == 1 else (letter_to_number(letters[0]) * 26) + letter_to_number(letters[1])


def decimal_color_to_hex(number: int) -> str:
    """Функция преобразует DECIMAL в HEX

    Args:
        number (int): [description]
    Returns:
        str: [description]
    """
    # Если число меньше или равно 26, то возвращаем соответствующую букву, иначе вызываем функцию рекурсивно
    if number <= 26:
        return str (chr (number + 96)).upper()
    else:
        # Функция вычисляет частное и остаток от деления числа на 26
        quotient, remainder = divmod (number - 1, 26)
        # Функция рекурсивно вызывает себя, чтобы преобразовать частное в HEX, и добавляет к результату букву, соответствующую остатку
        return str ( decimal_color_to_hex (quotient) + chr (remainder + 97) ).upper()


def hex_to_rgb (hex: str) -> tuple:
    """Функция преобразует HEX в RGB

    Args:
        hex (str): [description]
    Returns:
        tuple: [description]
    """
    """
    #FFFFFF -> (255, 255, 255) 

    `hex`: color in hexadecimal
    """
    # Функция удаляет символ #, если он присутствует
    hex = hex[1:] if '#' in hex else hex
    # Функция возвращает кортеж с RGB-значениями
    return (int (hex[:2], 16), int (hex[2:4], 16), int (hex[4:], 16) )