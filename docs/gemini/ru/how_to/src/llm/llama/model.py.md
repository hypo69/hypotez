## \file /src/ai/llama/model.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.ai.llama
    :platform: Windows, Unix
    :synopsis:

"""

from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
    filename="Meta-Llama-3.1-8B-Instruct-IQ4_XS.gguf",
)

output = llm(
    "Once upon a time,",
    max_tokens=512,
    echo=True
)
print(output)

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода инициализирует и использует модель Llama для генерации текста. Он загружает предварительно обученную модель из репозитория Hugging Face и генерирует текст на основе заданного промпта.

Шаги выполнения
-------------------------
1. **Импорт класса Llama**: Импортирует класс `Llama` из библиотеки `llama_cpp`, который используется для работы с моделью Llama.
2. **Загрузка предварительно обученной модели**: Функция `Llama.from_pretrained` загружает предварительно обученную модель Llama из репозитория Hugging Face. Указываются `repo_id` (идентификатор репозитория) и `filename` (имя файла модели).
3. **Инициализация модели**: Создается экземпляр модели `Llama` с загруженными параметрами.
4. **Генерация текста**: Метод `llm()` вызывается с промптом "Once upon a time," для генерации текста. Указываются параметры `max_tokens` (максимальное количество токенов в сгенерированном тексте) и `echo` (если `True`, промпт включается в выходные данные).
5. **Вывод результата**: Сгенерированный текст выводится на консоль с использованием функции `print()`.

Пример использования
-------------------------

```python
from llama_cpp import Llama

# Загрузка модели
llm = Llama.from_pretrained(
    repo_id="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
    filename="Meta-Llama-3.1-8B-Instruct-IQ4_XS.gguf",
)

# Генерация текста
output = llm(
    "The weather is nice today, so",
    max_tokens=512,
    echo=True
)

# Вывод результата
print(output)