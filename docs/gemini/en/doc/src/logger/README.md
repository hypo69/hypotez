# Документация для модуля `src.logger`

``````rst
.. module:: src.logger
``````

<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/README.MD'>[Root ↑]</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/README.MD'>src</A> /

</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/logger/readme.ru.md'>Русский</A>
</TD>
</TABLE>

### Обзор модуля `src.logger`

Модуль `src.logger` предоставляет гибкую систему логирования, поддерживающую логирование в консоль, файлы и JSON. В нём используется паттерн проектирования Singleton для гарантии того, что в приложении будет использоваться только один экземпляр логгера. Логгер поддерживает различные уровни логирования (например, `INFO`, `ERROR`, `DEBUG`) и включает цветной вывод для консольных логов. Также можно настраивать форматы вывода логов и управлять логированием в разные файлы.

---

### Классы:
- **SingletonMeta**: Метакласс, реализующий паттерн Singleton для логгера.
- **JsonFormatter**: Пользовательский форматер, выводящий логи в формате JSON.
- **Logger**: Основной класс логгера, поддерживающий логирование в консоль, файлы и JSON.

---

### Функции:

#### `__init__`
Инициализирует экземпляр Logger с заполнителями для различных типов логгеров (консольный, файловый и JSON).

#### `_configure_logger(name: str, log_path: str, level: Optional[int] = logging.DEBUG, formatter: Optional[logging.Formatter] = None, mode: Optional[str] = 'a') -> logging.Logger`
Настраивает и возвращает экземпляр логгера.

**Параметры:**
- `name`: Имя логгера.
- `log_path`: Путь к файлу логов.
- `level`: Уровень логирования, например, `logging.DEBUG`. По умолчанию `logging.DEBUG`.
- `formatter`: Пользовательский форматер (необязательный).
- `mode`: Режим файла, например, `'a'` для добавления (по умолчанию).

**Возвращает**: Настроенный экземпляр `logging.Logger`.

#### `initialize_loggers(info_log_path: Optional[str] = '', debug_log_path: Optional[str] = '', errors_log_path: Optional[str] = '', json_log_path: Optional[str] = '')`
Инициализирует логгеры для консольного и файлового логирования (info, debug, error и JSON).

**Параметры:**
- `info_log_path`: Путь для файла info логов (необязательный).
- `debug_log_path`: Путь для файла debug логов (необязательный).
- `errors_log_path`: Путь для файла error логов (необязательный).
- `json_log_path`: Путь для файла JSON логов (необязательный).

#### `log(level, message, ex=None, exc_info=False, color=None)`
Записывает сообщение в лог на указанном уровне (например, `INFO`, `DEBUG`, `ERROR`) с необязательным исключением и цветовым форматированием.

**Параметры:**
- `level`: Уровень логирования (например, `logging.INFO`, `logging.DEBUG`).
- `message`: Сообщение лога.
- `ex`: Необязательное исключение для логирования.
- `exc_info`: Следует ли включать информацию об исключении (по умолчанию `False`).
- `color`: Кортеж с цветами текста и фона для вывода в консоль (необязательный).

#### `info(message, ex=None, exc_info=False, colors: Optional[tuple] = None)`
Записывает информационное сообщение.

**Параметры:**
- `message`: Информационное сообщение для логирования.
- `ex`: Необязательное исключение для логирования.
- `exc_info`: Следует ли включать информацию об исключении (по умолчанию `False`).
- `colors`: Кортеж значений цвета для сообщения (необязательный).

#### `success(message, ex=None, exc_info=False, colors: Optional[tuple] = None)`
Записывает сообщение об успехе.

**Параметры**:
- Такие же, как у `info`.

#### `warning(message, ex=None, exc_info=False, colors: Optional[tuple] = None)`
Записывает предупреждающее сообщение.

**Параметры**:
- Такие же, как у `info`.

#### `debug(message, ex=None, exc_info=True, colors: Optional[tuple] = None)`
Записывает отладочное сообщение.

**Параметры**:
- Такие же, как у `info`.

#### `error(message, ex=None, exc_info=True, colors: Optional[tuple] = None)`
Записывает сообщение об ошибке.

**Параметры**:
- Такие же, как у `info`.

#### `critical(message, ex=None, exc_info=True, colors: Optional[tuple] = None)`
Записывает критическое сообщение.

**Параметры**:
- Такие же, как у `info`.

---

### Параметры для Logger
Класс `Logger` принимает несколько необязательных параметров для настройки поведения логирования.

- **Level**: Контролирует серьёзность захватываемых логов. Общие уровни включают:
  - `logging.DEBUG`: Подробная информация, полезная для диагностики проблем.
  - `logging.INFO`: Общая информация, такая как успешные операции.
  - `logging.WARNING`: Предупреждения, не обязательно требующие немедленных действий.
  - `logging.ERROR`: Сообщения об ошибках.
  - `logging.CRITICAL`: Критические ошибки, требующие немедленного внимания.

- **Formatter**: Определяет, как форматируются сообщения логов. По умолчанию сообщения форматируются как `'%(asctime)s - %(levelname)s - %(message)s'`. Вы можете предоставить пользовательский форматер для разных форматов, таких как JSON.

- **Color**: Цвета для сообщений логов в консоли. Цвета указываются как кортеж с двумя элементами:
  - **Цвет текста**: Указывает цвет текста (например, `colorama.Fore.RED`).
  - **Цвет фона**: Указывает цвет фона (например, `colorama.Back.WHITE`).

Цвет можно настраивать для разных уровней логов (например, зелёный для info, красный для ошибок и т. д.).

---

### Конфигурация файлового логирования (`config`)
Чтобы записывать сообщения в файл, можно указать пути к файлам в конфигурации.

```python
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
```

Пути к файлам, указанные в `config`, используются для записи логов в соответствующие файлы для каждого уровня логов.

---

### Пример использования

#### 1. Инициализация Logger:
```python
logger: Logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)
```

#### 2. Запись сообщений на разных уровнях:
```python
logger.info('Это информационное сообщение')
logger.success('Это сообщение об успехе')
logger.warning('Это предупреждающее сообщение')
logger.debug('Это отладочное сообщение')
logger.error('Это сообщение об ошибке')
logger.critical('Это критическое сообщение')
```

#### 3. Настройка цветов:
```python
logger.info('Это сообщение будет зелёным', colors=(colorama.Fore.GREEN, colorama.Back.BLACK))
logger.error('Это сообщение будет иметь красный фон', colors=(colorama.Fore.WHITE, colorama.Back.RED))
```

---

Этот модуль предоставляет полную и гибкую систему логирования для Python-приложений. Можно настроить логирование в консоль и файлы с разными форматами и цветами, управлять уровнями логирования и корректно обрабатывать исключения. Конфигурация для файлового логирования хранится в словаре `config`, что позволяет легко её настраивать.