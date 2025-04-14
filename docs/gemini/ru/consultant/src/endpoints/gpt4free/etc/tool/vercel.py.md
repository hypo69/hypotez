### **Анализ кода модуля `vercel.py`**

## \file /hypotez/src/endpoints/gpt4free/etc/tool/vercel.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован, разбит на отдельные функции, каждая из которых выполняет свою задачу.
    - Используются аннотации типов.
    - Четкое разделение на этапы: получение информации о моделях, преобразование и вывод.
- **Минусы**:
    - Отсутствует документация в формате docstring для функций.
    - Не используется модуль `logger` для логирования.
    - Не все переменные аннотированы типами.
    - В регулярных выражениях можно добавить комментарии для пояснения их назначения.
    - Не обрабатываются возможные исключения при выполнении запросов к серверам.

**Рекомендации по улучшению:**

1.  **Добавить docstring для всех функций и классов**:
    - Описать назначение, аргументы, возвращаемые значения и возможные исключения.
2.  **Использовать модуль `logger` для логирования**:
    - Добавить логирование информации о процессе выполнения программы и ошибок.
3.  **Обработка исключений**:
    - Добавить блоки `try...except` для обработки возможных исключений при выполнении запросов к серверам и парсинге данных.
    - Логировать возникающие ошибки с использованием `logger.error`.
4.  **Комментарии в регулярных выражениях**:
    - Добавить комментарии для пояснения назначения регулярных выражений.
5.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это возможно.
6.  **Улучшить читаемость**:
    - Разбить длинные строки на несколько, чтобы улучшить читаемость кода.

**Оптимизированный код:**

```python
import json
import re
from typing import Any, List, Dict

import quickjs
from curl_cffi import requests

from src.logger import logger # Добавлен импорт модуля logger

session = requests.Session(impersonate="chrome107")


def get_model_info() -> Dict[str, Any]:
    """
    Получает информацию о моделях с сайта sdk.vercel.ai.

    Returns:
        Dict[str, Any]: Словарь с информацией о моделях.
    """
    url = "https://sdk.vercel.ai"
    try:
        response = session.get(url)
        response.raise_for_status()  # Проверка на успешный статус код
        html = response.text
    except requests.exceptions.RequestException as ex:
        logger.error(f"Ошибка при получении данных с {url}", ex, exc_info=True)
        return {}

    paths_regex = r"static\\/chunks.+?\\.js"
    separator_regex = r\'"\\]\\)<\\/script><script>self\\.__next_f\\.push\\(\\[.,"\'"

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
            logger.error(f"Ошибка при получении данных с {url_item}", ex, exc_info=True)
            continue

    models_regex = r'let .="\\\\n\\\\nHuman:\\",r=(.+?),.=\''
    for script in scripts:
        matches = re.findall(models_regex, script)
        if matches:
            models_str = matches[0]
            stop_sequences_regex = r"(?<=stopSequences:{value:\\[)\\D(?<!\\])"
            models_str = re.sub(
                stop_sequences_regex, re.escape('"\\\\n\\\\nHuman:"'), models_str
            )

            context = quickjs.Context()  # type: ignore
            try:
                json_str: str = context.eval(f"({models_str})").json()  # type: ignore
                return json.loads(json_str)  # type: ignore
            except quickjs.Error as ex:
                logger.error("Ошибка при выполнении JavaScript кода", ex, exc_info=True)
                return {}

    return {}


def convert_model_info(models: Dict[str, Any]) -> Dict[str, Any]:
    """
    Преобразует информацию о моделях в более удобный формат.

    Args:
        models (Dict[str, Any]): Словарь с информацией о моделях.

    Returns:
        Dict[str, Any]: Преобразованный словарь с информацией о моделях.
    """
    model_info: Dict[str, Any] = {}
    for model_name, params in models.items():
        default_params = params_to_default_params(params["parameters"])
        model_info[model_name] = {"id": params["id"], "default_params": default_params}
    return model_info


def params_to_default_params(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Извлекает параметры по умолчанию из информации о параметрах модели.

    Args:
        parameters (Dict[str, Any]): Словарь с информацией о параметрах модели.

    Returns:
        Dict[str, Any]: Словарь с параметрами по умолчанию.
    """
    defaults: Dict[str, Any] = {}
    for key, parameter in parameters.items():
        if key == "maximumLength":
            key = "maxTokens"
        defaults[key] = parameter["value"]
    return defaults


def get_model_names(model_info: Dict[str, Any]) -> List[str]:
    """
    Получает список имен моделей, исключая "openai:gpt-4" и "openai:gpt-3.5-turbo".

    Args:
        model_info (Dict[str, Any]): Словарь с информацией о моделях.

    Returns:
        List[str]: Список имен моделей.
    """
    model_names = model_info.keys()
    model_names = [
        name
        for name in model_names
        if name not in ["openai:gpt-4", "openai:gpt-3.5-turbo"]
    ]
    model_names.sort()
    return model_names


def print_providers(model_names: List[str]):
    """
    Выводит строки кода для определения моделей с указанием провайдера.

    Args:
        model_names (List[str]): Список имен моделей.
    """
    for name in model_names:
        split_name = re.split(r":|/", name)
        base_provider = split_name[0]
        variable_name = split_name[-1].replace("-", "_").replace(".", "")
        line = f'    {variable_name} = Model(name="{name}", base_provider="{base_provider}", best_provider=Vercel,)'
        print(line)


def print_convert(model_names: List[str]):
    """
    Выводит строки кода для создания словаря, связывающего имена моделей с переменными.

    Args:
        model_names (List[str]): Список имен моделей.
    """
    for name in model_names:
        split_name = re.split(r":|/", name)
        key = split_name[-1]
        variable_name = split_name[-1].replace("-", "_").replace(".", "")
        line = f'        "{key}": {variable_name},'
        print(line)


def main():
    """
    Основная функция, которая получает информацию о моделях, преобразует ее и выводит.
    """
    model_info = get_model_info()
    model_info = convert_model_info(model_info)
    print(json.dumps(model_info, indent=2))

    model_names = get_model_names(model_info)
    print("-------" * 40)
    print_providers(model_names)
    print("-------" * 40)
    print_convert(model_names)


if __name__ == "__main__":
    main()