### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Данный код предназначен для извлечения, преобразования и печати информации о моделях, доступных через Vercel AI SDK. Он получает данные о моделях из веб-страницы, извлекает необходимые параметры и формирует вывод в виде JSON, а также генерирует код для определения моделей и их привязки к провайдерам.

Шаги выполнения
-------------------------
1. **Получение информации о моделях**:
   - Функция `get_model_info()` отправляет GET-запрос к `https://sdk.vercel.ai`.
   - Извлекает пути к JavaScript файлам, содержащим информацию о моделях, используя регулярные выражения.
   - Получает содержимое каждого JavaScript файла и извлекает строку, содержащую информацию о моделях в формате, близком к JSON.
   - Использует `quickjs` для преобразования этой строки в JSON формат и возвращает словарь с информацией о моделях.

2. **Преобразование информации о моделях**:
   - Функция `convert_model_info()` принимает словарь с информацией о моделях и преобразует его в более удобный формат.
   - Извлекает `id` модели и параметры по умолчанию, используя функцию `params_to_default_params()`.
   - Возвращает новый словарь, где ключами являются имена моделей, а значениями - `id` и параметры по умолчанию.

3. **Преобразование параметров в параметры по умолчанию**:
   - Функция `params_to_default_params()` принимает словарь параметров модели и преобразует его в словарь параметров по умолчанию.
   - Переименовывает ключ `maximumLength` в `maxTokens`.
   - Возвращает словарь, где ключами являются имена параметров, а значениями - значения параметров по умолчанию.

4. **Получение списка имен моделей**:
   - Функция `get_model_names()` принимает словарь с информацией о моделях и извлекает список имен моделей.
   - Исключает модели `"openai:gpt-4"` и `"openai:gpt-3.5-turbo"` из списка.
   - Сортирует список имен моделей и возвращает его.

5. **Печать определений провайдеров**:
   - Функция `print_providers()` принимает список имен моделей и генерирует строки кода для определения моделей и их привязки к провайдерам.
   - Разделяет имя модели на части, чтобы извлечь базового провайдера и имя переменной.
   - Печатает строку кода, которая создает экземпляр класса `Model` с указанием имени, базового провайдера и провайдера Vercel.

6. **Печать соответствий моделей**:
   - Функция `print_convert()` принимает список имен моделей и генерирует строки кода для создания соответствий между ключами и переменными моделей.
   - Разделяет имя модели на части, чтобы извлечь ключ и имя переменной.
   - Печатает строку кода, которая создает соответствие между ключом и переменной модели.

7. **Основная функция `main()`**:
   - Вызывает `get_model_info()` для получения информации о моделях.
   - Вызывает `convert_model_info()` для преобразования информации о моделях.
   - Печатает информацию о моделях в формате JSON.
   - Вызывает `get_model_names()` для получения списка имен моделей.
   - Вызывает `print_providers()` для печати определений провайдеров.
   - Вызывает `print_convert()` для печати соответствий моделей.

Пример использования
-------------------------

```python
import json
import re
from typing import Any

import quickjs
from curl_cffi import requests

session = requests.Session(impersonate="chrome107")


def get_model_info() -> dict[str, Any]:
    url = "https://sdk.vercel.ai"
    response = session.get(url)
    html = response.text
    paths_regex = r"static\\/chunks.+?\\.js"
    separator_regex = r\'"\\]\\)<\\/script><script>self\\.__next_f\\.push\\(\\[.,"\'

    paths = re.findall(paths_regex, html)
    paths = [re.sub(separator_regex, "", path) for path in paths]
    paths = list(set(paths))

    urls = [f"{url}/_next/{path}" for path in paths]
    scripts = [session.get(url).text for url in urls]

    models_regex = r\'let .="\\\\n\\\\nHuman:\\",r=(.+?),.=\'
    for script in scripts:

        matches = re.findall(models_regex, script)
        if matches:
            models_str = matches[0]
            stop_sequences_regex = r"(?<=stopSequences:{value:\\[)\\D(?<!\\])"
            models_str = re.sub(
                stop_sequences_regex, re.escape('"\\\\n\\\\nHuman:"'), models_str
            )

            context = quickjs.Context()  # type: ignore
            json_str: str = context.eval(f"({models_str})").json()  # type: ignore
            return json.loads(json_str)  # type: ignore

    return {}


def convert_model_info(models: dict[str, Any]) -> dict[str, Any]:
    model_info: dict[str, Any] = {}
    for model_name, params in models.items():
        default_params = params_to_default_params(params["parameters"])
        model_info[model_name] = {"id": params["id"], "default_params": default_params}
    return model_info


def params_to_default_params(parameters: dict[str, Any]):
    defaults: dict[str, Any] = {}
    for key, parameter in parameters.items():
        if key == "maximumLength":
            key = "maxTokens"
        defaults[key] = parameter["value"]
    return defaults


def get_model_names(model_info: dict[str, Any]):
    model_names = model_info.keys()
    model_names = [
        name
        for name in model_names
        if name not in ["openai:gpt-4", "openai:gpt-3.5-turbo"]
    ]
    model_names.sort()
    return model_names


def print_providers(model_names: list[str]):
    for name in model_names:
        split_name = re.split(r":|/", name)
        base_provider = split_name[0]
        variable_name = split_name[-1].replace("-", "_").replace(".", "")
        line = f'    {variable_name} = Model(name="{name}", base_provider="{base_provider}", best_provider=Vercel,)\n'
        print(line)


def print_convert(model_names: list[str]):
    for name in model_names:
        split_name = re.split(r":|/", name)
        key = split_name[-1]
        variable_name = split_name[-1].replace("-", "_").replace(".", "")
        line = f'        "{key}": {variable_name},'
        print(line)


def main():
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