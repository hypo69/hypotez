### **Анализ кода модуля `vercel.py`**

## \file /hypotez/src/endpoints/gpt4free/etc/tool/vercel.py

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код разбит на отдельные функции, что облегчает понимание и поддержку.
  - Используются аннотации типов для параметров и возвращаемых значений функций.
  - Присутствует логика извлечения и преобразования информации о моделях с использованием регулярных выражений и `quickjs`.
- **Минусы**:
  - Отсутствуют docstring для функций, что затрудняет понимание их назначения и использования.
  - Не используются `j_loads` или `j_loads_ns` для чтения JSON данных.
  - Не обрабатываются возможные исключения при выполнении запросов и обработке данных.
  - Используется устаревшая библиотека `curl_cffi` вместо `httpx`.

**Рекомендации по улучшению:**

1.  **Добавить docstring**: Добавить docstring для каждой функции, описывающие ее назначение, параметры, возвращаемые значения и возможные исключения.
2.  **Обработка исключений**: Добавить блоки `try...except` для обработки возможных исключений при выполнении HTTP-запросов, обработке регулярных выражений и преобразовании данных. Использовать `logger.error` для логирования ошибок.
3.  **Заменить `curl_cffi` на `httpx`**: `curl_cffi` считается устаревшей, рекомендуется использовать `httpx` для выполнения HTTP-запросов.
4.  **Использовать `j_loads`**: Использовать `j_loads` для загрузки JSON данных, чтобы обеспечить консистентность в проекте.
5.  **Улучшить читаемость регулярных выражений**: Добавить комментарии к регулярным выражениям, чтобы объяснить их назначение.
6.  **Удалить неиспользуемые импорты**: Убрать неиспользуемые импорты, если таковые имеются.
7.  **Добавить логирование**: Добавить логирование для отслеживания процесса выполнения и выявления возможных проблем.
8.  **Упростить код**: Упростить код, где это возможно, чтобы улучшить его читаемость и производительность.
9. **Перевести все комментарии на русский язык**

**Оптимизированный код:**

```python
import json
import re
from typing import Any

import httpx
import quickjs

from src.logger import logger  # Import logger
from src.utils.json_utils import j_loads  # Import j_loads

# Сессия для выполнения HTTP запросов с impersonate chrome107
session = httpx.Client(
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"},
    timeout=30,
)


def get_model_info() -> dict[str, Any]:
    """
    Извлекает информацию о моделях с сайта sdk.vercel.ai.

    Returns:
        dict[str, Any]: Словарь с информацией о моделях.
    """
    url = "https://sdk.vercel.ai"
    try:
        response = session.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        html = response.text
    except httpx.HTTPStatusError as ex:
        logger.error(f"Ошибка при получении данных с {url}", ex, exc_info=True)
        return {}
    except httpx.RequestError as ex:
        logger.error(f"Ошибка при подключении к {url}", ex, exc_info=True)
        return {}

    # Регулярное выражение для поиска путей к JavaScript файлам
    paths_regex = r"static\\/chunks.+?\\.js"
    # Регулярное выражение для удаления разделителя
    separator_regex = r\'"\\]\\)<\\/script><script>self\\.__next_f\\.push\\(\\[.,"\'

    paths = re.findall(paths_regex, html)
    paths = [re.sub(separator_regex, "", path) for path in paths]
    paths = list(set(paths))

    urls = [f"{url}/_next/{path}" for path in paths]
    scripts = []
    for url in urls:
        try:
            response = session.get(url)
            response.raise_for_status()
            scripts.append(response.text)
        except httpx.HTTPStatusError as ex:
            logger.error(f"Ошибка при получении данных с {url}", ex, exc_info=True)
            continue
        except httpx.RequestError as ex:
            logger.error(f"Ошибка при подключении к {url}", ex, exc_info=True)
            continue

    # Регулярное выражение для поиска информации о моделях
    models_regex = r"let .=\"\\\\n\\\\nHuman:\\\",r=(.+?),.=\'"
    for script in scripts:
        matches = re.findall(models_regex, script)
        if matches:
            models_str = matches[0]
            # Регулярное выражение для удаления stopSequences
            stop_sequences_regex = r"(?<=stopSequences:{value:\\[)\\D(?<!\\])"
            models_str = re.sub(
                stop_sequences_regex, re.escape('"\\\\n\\\\nHuman:"'), models_str
            )

            context = quickjs.Context()  # type: ignore
            try:
                json_str: str = context.eval(f"({models_str})").json()  # type: ignore
                return j_loads(json_str)  # type: ignore # Use j_loads here
            except quickjs.JSError as ex:
                logger.error(f"Ошибка при выполнении JavaScript кода", ex, exc_info=True)
                return {}

    return {}


def convert_model_info(models: dict[str, Any]) -> dict[str, Any]:
    """
    Преобразует информацию о моделях в более удобный формат.

    Args:
        models (dict[str, Any]): Словарь с информацией о моделях.

    Returns:
        dict[str, Any]: Преобразованный словарь с информацией о моделях.
    """
    model_info: dict[str, Any] = {}
    for model_name, params in models.items():
        default_params = params_to_default_params(params["parameters"])
        model_info[model_name] = {"id": params["id"], "default_params": default_params}
    return model_info


def params_to_default_params(parameters: dict[str, Any]) -> dict[str, Any]:
    """
    Преобразует параметры модели в параметры по умолчанию.

    Args:
        parameters (dict[str, Any]): Словарь с параметрами модели.

    Returns:
        dict[str, Any]: Словарь с параметрами по умолчанию.
    """
    defaults: dict[str, Any] = {}
    for key, parameter in parameters.items():
        if key == "maximumLength":
            key = "maxTokens"
        defaults[key] = parameter["value"]
    return defaults


def get_model_names(model_info: dict[str, Any]) -> list[str]:
    """
    Извлекает имена моделей из информации о моделях.

    Args:
        model_info (dict[str, Any]): Словарь с информацией о моделях.

    Returns:
        list[str]: Список имен моделей.
    """
    model_names = model_info.keys()
    model_names = [
        name
        for name in model_names
        if name not in ["openai:gpt-4", "openai:gpt-3.5-turbo"]
    ]
    model_names.sort()
    return model_names


def print_providers(model_names: list[str]):
    """
    Печатает строку провайдеров моделей.

    Args:
        model_names (list[str]): Список имен моделей.
    """
    for name in model_names:
        split_name = re.split(r":|/", name)
        base_provider = split_name[0]
        variable_name = split_name[-1].replace("-", "_").replace(".", "")
        line = f'\'{variable_name} = Model(name="{name}", base_provider="{base_provider}", best_provider=Vercel,)\\n\''
        print(line)


def print_convert(model_names: list[str]):
    """
    Печатает строку для преобразования моделей.

    Args:
        model_names (list[str]): Список имен моделей.
    """
    for name in model_names:
        split_name = re.split(r":|/", name)
        key = split_name[-1]
        variable_name = split_name[-1].replace("-", "_").replace(".", "")
        # "claude-instant-v1": claude_instant_v1,
        line = f'        "{key}": {variable_name},\''
        print(line)


def main():
    """
    Основная функция для извлечения, преобразования и печати информации о моделях.
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