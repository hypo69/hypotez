### **Анализ кода модуля `vercel.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код разбит на логические функции, что облегчает его понимание и поддержку.
  - Используются регулярные выражения для извлечения данных из HTML и JavaScript.
  - Присутствует обработка исключений.
- **Минусы**:
  - Отсутствует документация docstring для функций и модуля.
  - Не используются логирование для отслеживания ошибок и хода выполнения программы.
  - Не все переменные аннотированы типами.
  - Использование `re.sub` с `re.escape` может быть избыточным.
  - Отсутствует описание модуля.

#### **Рекомендации по улучшению**:

1.  **Добавить docstring**:
    *   Добавить docstring для всех функций и для модуля с описанием назначения, аргументов, возвращаемых значений и возможных исключений.
    *   Описать, что делает модуль, какие классы содержит и примеры использования.

2.  **Логирование**:
    *   Добавить логирование с использованием модуля `logger` для отслеживания хода выполнения программы и записи ошибок.

3.  **Аннотация типов**:
    *   Добавить аннотацию типов для всех переменных.

4.  **Безопасность**:
    *   Убедиться, что использование `re.escape` необходимо в контексте `re.sub`. Если нет, упростить код.

5.  **Обработка исключений**:
    *   Добавить обработку исключений при запросах к внешним ресурсам (сайтам) и парсинге данных.

#### **Оптимизированный код**:

```python
"""
Модуль для получения информации о моделях Vercel AI SDK
=======================================================

Модуль содержит функции для извлечения информации о доступных моделях из Vercel AI SDK,
включая их параметры и имена.

Пример использования
----------------------

>>> model_info = get_model_info()
>>> if model_info:
>>>     model_names = get_model_names(model_info)
>>>     print_providers(model_names)
"""

import json
import re
from typing import Any, Dict, List

import quickjs
from curl_cffi import requests

from src.logger import logger # Добавлен импорт logger

session = requests.Session(impersonate="chrome107")


def get_model_info() -> Dict[str, Any]:
    """
    Получает информацию о моделях из Vercel AI SDK.

    Извлекает информацию о моделях из HTML-кода SDK, используя регулярные выражения,
    и возвращает ее в виде словаря.

    Returns:
        Dict[str, Any]: Словарь, содержащий информацию о моделях, или пустой словарь в случае ошибки.

    Raises:
        requests.exceptions.RequestException: При ошибке выполнения HTTP-запроса.
        quickjs.Error: При ошибке выполнения JavaScript-кода.
        json.JSONDecodeError: При ошибке декодирования JSON.

    """
    url: str = "https://sdk.vercel.ai"
    try:
        response = session.get(url)
        response.raise_for_status()  # Проверка на HTTP ошибки
        html: str = response.text
    except requests.exceptions.RequestException as ex:
        logger.error(f"Ошибка при выполнении запроса к {url}", ex, exc_info=True)
        return {}

    paths_regex: str = r"static\\/chunks.+?\\.js"
    separator_regex: str = r\'"\\]\\)<\\/script><script>self\\.__next_f\\.push\\(\\[.,"\'"

    paths: List[str] = re.findall(paths_regex, html)
    paths = [re.sub(separator_regex, "", path) for path in paths]
    paths = list(set(paths))

    urls: List[str] = [f"{url}/_next/{path}" for path in paths]
    scripts: List[str] = []
    for url_item in urls:
        try:
            script = session.get(url_item).text
            scripts.append(script)
        except requests.exceptions.RequestException as ex:
            logger.error(f"Ошибка при выполнении запроса к {url_item}", ex, exc_info=True)
            continue

    models_regex: str = r'let .="\\\\n\\\\nHuman:\\",r=(.+?),.=\''
    for script in scripts:
        matches = re.findall(models_regex, script)
        if matches:
            models_str: str = matches[0]
            stop_sequences_regex: str = r"(?<=stopSequences:{value:\\[)\\D(?<!\\])"
            models_str = re.sub(
                stop_sequences_regex, re.escape('"\\\\n\\\\nHuman:"'), models_str
            )

            context = quickjs.Context()  # type: ignore
            try:
                json_str: str = context.eval(f"({models_str})").json()  # type: ignore
                return json.loads(json_str)  # type: ignore
            except (quickjs.Error, json.JSONDecodeError) as ex:
                logger.error("Ошибка при выполнении JavaScript или декодировании JSON", ex, exc_info=True)
                return {}

    return {}


def convert_model_info(models: Dict[str, Any]) -> Dict[str, Any]:
    """
    Преобразует информацию о моделях в формат, удобный для дальнейшего использования.

    Извлекает ID и параметры по умолчанию для каждой модели.

    Args:
        models (Dict[str, Any]): Словарь с информацией о моделях.

    Returns:
        Dict[str, Any]: Преобразованный словарь с информацией о моделях.
    """
    model_info: Dict[str, Any] = {}
    for model_name, params in models.items():
        default_params: Dict[str, Any] = params_to_default_params(params["parameters"])
        model_info[model_name] = {"id": params["id"], "default_params": default_params}
    return model_info


def params_to_default_params(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Извлекает параметры по умолчанию из словаря параметров модели.

    Args:
        parameters (Dict[str, Any]): Словарь параметров модели.

    Returns:
        Dict[str, Any]: Словарь параметров по умолчанию.
    """
    defaults: Dict[str, Any] = {}
    for key, parameter in parameters.items():
        if key == "maximumLength":
            key = "maxTokens"
        defaults[key] = parameter["value"]
    return defaults


def get_model_names(model_info: Dict[str, Any]) -> List[str]:
    """
    Извлекает имена моделей из словаря информации о моделях.

    Args:
        model_info (Dict[str, Any]): Словарь с информацией о моделях.

    Returns:
        List[str]: Список имен моделей, отсортированный по алфавиту.
    """
    model_names = model_info.keys()
    model_names = [
        name
        for name in model_names
        if name not in ["openai:gpt-4", "openai:gpt-3.5-turbo"]
    ]
    model_names.sort()
    return model_names


def print_providers(model_names: List[str]) -> None:
    """
    Печатает строки кода для определения моделей и их провайдеров.

    Args:
        model_names (List[str]): Список имен моделей.
    """
    for name in model_names:
        split_name = re.split(r":|/", name)
        base_provider = split_name[0]
        variable_name = split_name[-1].replace("-", "_").replace(".", "")
        line = f'variable_name = Model(name="{name}", base_provider="{base_provider}", best_provider=Vercel,)\n'
        print(line)


def print_convert(model_names: List[str]) -> None:
    """
    Печатает строки кода для преобразования имен моделей в переменные.

    Args:
        model_names (List[str]): Список имен моделей.
    """
    for name in model_names:
        split_name = re.split(r":|/", name)
        key = split_name[-1]
        variable_name = split_name[-1].replace("-", "_").replace(".", "")
        # "claude-instant-v1": claude_instant_v1,
        line = f'        "{key}": {variable_name},\'\n'
        print(line)


def main() -> None:
    """
    Основная функция, которая выполняет извлечение, преобразование и печать информации о моделях.
    """
    model_info: Dict[str, Any] = get_model_info()
    model_info = convert_model_info(model_info)
    print(json.dumps(model_info, indent=2))

    model_names: List[str] = get_model_names(model_info)
    print("-------" * 40)
    print_providers(model_names)
    print("-------" * 40)
    print_convert(model_names)


if __name__ == "__main__":
    main()