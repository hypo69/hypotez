### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет функцию `gui_parser`, которая создает и настраивает парсер аргументов командной строки с использованием модуля `argparse`. Парсер предназначен для обработки аргументов, необходимых для запуска графического интерфейса (GUI) приложения. Он позволяет указать хост, порт, включить режим отладки, игнорировать файлы cookie, а также указать список игнорируемых провайдеров и браузеров для работы с cookie.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `ArgumentParser` из `argparse`, `browsers` из `..cookies` и `Provider` из `..`.
2. **Определение функции `gui_parser`**: Функция `gui_parser` создает экземпляр `ArgumentParser` с описанием "Run the GUI".
3. **Добавление аргументов**:
   - `--host`: Указывает имя хоста для запуска GUI. По умолчанию "0.0.0.0".
   - `--port` или `-p`: Указывает порт для запуска GUI. По умолчанию 8080.
   - `--debug` или `-d` или `-debug`: Включает режим отладки.
   - `--ignore-cookie-files`: Указывает, следует ли игнорировать файлы cookie.
   - `--ignored-providers`: Список провайдеров, которые следует игнорировать при обработке запросов. Варианты выбора берутся из списка доступных провайдеров.
   - `--cookie-browsers`: Список браузеров, из которых следует извлекать cookie. Варианты выбора берутся из списка поддерживаемых браузеров.
4. **Возврат парсера**: Функция возвращает настроенный объект `ArgumentParser`.

Пример использования
-------------------------

```python
from argparse import ArgumentParser

from ..cookies import browsers
from .. import Provider

def gui_parser():
    """
    Создает парсер аргументов командной строки для запуска GUI.

    Args:
        None

    Returns:
        ArgumentParser: Объект парсера аргументов.
    """
    parser = ArgumentParser(description="Run the GUI")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="hostname")
    parser.add_argument("--port", "-p", type=int, default=8080, help="port")
    parser.add_argument("--debug", "-d", "-debug", action="store_true", help="debug mode")
    parser.add_argument("--ignore-cookie-files", action="store_true", help="Don't read .har and cookie files.")
    parser.add_argument("--ignored-providers", nargs="+", choices=[provider.__name__ for provider in Provider.__providers__ if provider.working],
                            default=[], help="List of providers to ignore when processing request. (incompatible with --reload and --workers)")
    parser.add_argument("--cookie-browsers", nargs="+", choices=[browser.__name__ for browser in browsers],\
                            default=[], help="List of browsers to access or retrieve cookies from.")
    return parser

if __name__ == '__main__':
    parser = gui_parser()
    args = parser.parse_args()
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Debug: {args.debug}")
    print(f"Ignore cookie files: {args.ignore_cookie_files}")
    print(f"Ignored providers: {args.ignored_providers}")
    print(f"Cookie browsers: {args.cookie_browsers}")