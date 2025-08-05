## \file hypotez/src/credentials.ru.md
<!-- Русский -->

# Как использовать этот блок кода

Этот документ предоставляет обзор класса `ProgramSettings` и его использования для загрузки и управления учетными данными и настройками в проекте.

## Обзор

`ProgramSettings` загружает и сохраняет учетные данные (ключи API, пароли и т.д.) из базы данных KeePass (`credentials.kdbx`). Он также определяет корневой каталог проекта и предоставляет глобальный экземпляр для доступа к настройкам из любой части кода.

## Шаги выполнения

1.  **Определение корневой директории проекта**:

    *   Функция `set_project_root` определяет корневую директорию проекта, начиная с текущей директории файла.
    *   Функция ищет вверх по директориям, пока не найдет директорию, содержащую один из маркерных файлов (`pyproject.toml`, `requirements.txt`, `.git`).
    *   Если корневая директория найдена, она добавляется в `sys.path`.
2.  **Загрузка конфигурации**:

    *   Настройки по умолчанию загружаются из файла `config.json`, расположенного в директории `src`.
    *   Этот файл содержит различные параметры конфигурации, такие как информация об авторе, доступные режимы, пути и детали проекта.
    *   Функция `j_loads_ns` используется для загрузки конфигурации из `config.json`.
3.  **Управление учетными данными с использованием KeePass**:

    *   Учетные данные безопасно управляются с использованием базы данных KeePass (`credentials.kdbx`).
    *   Мастер-пароль для этой базы данных обрабатывается по-разному в зависимости от среды:
        *   В режиме разработки пароль считывается из файла `password.txt`, расположенного в директории `secrets`.
        *   В режиме продакшн пароль вводится через консоль.
    *   Метод `_open_kp` открывает базу данных KeePass.
    *   Методы `_load_*_credentials` загружают данные из соответствующих групп и записей в базе данных KeePass и сохраняют их в атрибуты объекта `self.credentials`.
4.  **Инициализация глобального экземпляра `ProgramSettings`**:

    *   Глобальный экземпляр `ProgramSettings` (`gs`) создается для обеспечения доступа к настройкам и учетным данным проекта из любого места в коде.

## Пример использования

```python
from src import gs

# Пример использования
api_key = gs.credentials.openai.api_key
```

## Подробности

### Функция `set_project_root`

Определение корневой директории проекта.

```python
def set_project_root(marker_files=('__root__','.git')) -> Path:
    """
    Находит корневую директорию проекта, начиная с текущей директории файла,
    ища вверх и останавливаясь на первой директории, содержащей любой из маркерных файлов.
    
    Args:
        marker_files (tuple): Имена файлов или директорий для идентификации корневой директории проекта.
    
    Returns:
        Path: Путь к корневой директории, если найдена, иначе директория, где находится скрипт.
    """
    __root__:Path
    current_path:Path = Path(__file__).resolve().parent
    __root__ = current_path
    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in marker_files):
            __root__ = parent
            break
    if __root__ not in sys.path:
        sys.path.insert(0, str(__root__))
    return __root__
```

### Загрузка конфигурации из `config.json`

Загрузка настроек проекта из файла `config.json`.

```python
self.config = j_loads_ns(self.base_dir / 'src' / 'config.json')
if not self.config:
    logger.error('Ошибка при загрузке настроек')
    ...
    return

self.config.project_name = self.base_dir.name
```

### Открытие базы данных KeePass

Открытие базы данных KeePass для загрузки учетных данных.

```python
def _open_kp(self, retry: int = 3) -> PyKeePass | None:
    """ Открывает базу данных KeePass
    Args:
        retry (int): Количество попыток
    """
    while retry > 0:
        try:
            password:str = Path( self.path.secrets / 'password.txt').read_text(encoding="utf-8") or None
            kp = PyKeePass(str(self.path.secrets / 'credentials.kdbx'), 
                           password = password or getpass.getpass(print('Введите мастер-пароль KeePass: ').lower()))
            return kp
        except Exception as ex:
            print(f"Не удалось открыть базу данных KeePass. Исключение: {ex}, осталось попыток: {retry-1}.")
            ...
            retry -= 1
            if retry < 1:
                logger.critical('Не удалось открыть базу данных KeePass после нескольких попыток', exc_info=True)
                ...
                sys.exit()
```

### Структура базы данных `credentials.kdbx`

Дерево базы данных `credentials.kdbx`:

```
credentials.kdbx
├── suppliers
│   └── aliexpress
│       └── api
│           └── entry (Aliexpress API credentials)
├── openai
│   ├── entry (OpenAI API keys)
│   └── assistants
│       └── entry (OpenAI assistant IDs)
├── gemini
│   └── entry (GoogleAI credentials)
├── telegram
│   └── entry (Telegram credentials)
├── discord
│   └── entry (Discord credentials)
├── prestashop
│   ├── entry (PrestaShop credentials)
│   └── clients
│       └── entry (PrestaShop client credentials)
│   └── translation
│       └── entry (PrestaShop translation credentials)
├── smtp
│   └── entry (SMTP credentials)
├── facebook
│   └── entry (Facebook credentials)
└── google
    └── gapi
        └── entry (Google API credentials)
```

### Глобальный экземпляр `ProgramSettings`

Глобальный экземпляр `ProgramSettings` для доступа к настройкам и учетным данным.

```python
# Global instance of ProgramSettings
gs: ProgramSettings = ProgramSettings()