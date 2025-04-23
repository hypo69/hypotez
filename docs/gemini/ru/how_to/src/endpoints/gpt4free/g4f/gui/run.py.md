### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предназначен для запуска графического интерфейса (GUI) для библиотеки `g4f` (GPT4Free). Он обрабатывает аргументы командной строки, устанавливает настройки отладки, загружает файлы cookie, определяет список используемых браузеров для cookie и отключает указанных провайдеров. После этого запускается сам графический интерфейс.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули для разбора аргументов командной строки (`gui_parser`), чтения файлов cookie (`read_cookie_files`), запуска графического интерфейса (`run_gui`) и управления провайдерами (`ProviderUtils`).
2. **Функция `run_gui_args(args)`**:
   - Принимает аргументы командной строки `args`.
   - Если установлен флаг отладки (`args.debug`), включается логирование отладочной информации `g4f.debug.logging = True`.
   - Если не указано игнорировать файлы cookie (`not args.ignore_cookie_files`), файлы cookie считываются функцией `read_cookie_files()`.
   - Извлекаются значения хоста (`args.host`) и порта (`args.port`) для GUI.
   - Определяется список браузеров, из которых будут использоваться cookie, на основе аргумента `args.cookie_browsers`.
   - Отключаются указанные провайдеры, если они есть в `args.ignored_providers`.
   - Запускается графический интерфейс с указанными хостом, портом и флагом отладки: `run_gui(host, port, debug)`.
3. **Основной блок `if __name__ == "__main__":`**:
   - Создается парсер аргументов командной строки `parser = gui_parser()`.
   - Аргументы командной строки разбираются с помощью `args = parser.parse_args()`.
   - Функция `run_gui_args(args)` вызывается для запуска GUI с переданными аргументами.

Пример использования
-------------------------

```python
# В данном случае предполагается, что у вас есть файл gui_parser.py, который определяет парсер аргументов командной строки.
# Также предполагается, что у вас есть функции read_cookie_files() и run_gui(), которые выполняют соответствующие действия.
# Пример запуска из командной строки: python run.py --host 127.0.0.1 --port 5000 --debug --cookie_browsers Chrome Firefox --ignored_providers Bing

from .gui_parser import gui_parser
from ..cookies import read_cookie_files
from ..gui import run_gui
from ..Provider import ProviderUtils

import g4f.cookies
import g4f.debug

def run_gui_args(args):
    if args.debug:
        g4f.debug.logging = True
    if not args.ignore_cookie_files:
        read_cookie_files()
    host = args.host
    port = args.port
    debug = args.debug
    g4f.cookies.browsers = [g4f.cookies[browser] for browser in args.cookie_browsers]
    if args.ignored_providers:
        for provider in args.ignored_providers:
            if provider in ProviderUtils.convert:
                ProviderUtils.convert[provider].working = False

    run_gui(host, port, debug)

if __name__ == "__main__":
    parser = gui_parser()
    args = parser.parse_args()
    run_gui_args(args)