## Как использовать модуль `credentials`
=========================================================================================

Описание
-------------------------
Модуль `credentials` предназначен для хранения глобальных настроек проекта, таких как пути, пароли, логины и параметры API. 
Он использует паттерн Singleton для обеспечения единственного экземпляра настроек в течение всего времени работы приложения.

Шаги выполнения
-------------------------
1. **Инициализация**: При первом обращении к модулю создаётся экземпляр класса `ProgramSettings`, который хранит все настройки.
2. **Загрузка настроек**:  При инициализации `ProgramSettings` происходит загрузка конфигурации из файла `src/config.json`.
3. **Загрузка учетных данных**: Из файла `src/secrets/credentials.kdbx` загружаются учетные данные, такие как ключи API, пароли, логины и т.д., с помощью KeePass.
4. **Доступ к настройкам**: После загрузки, все настройки доступны через экземпляр `ProgramSettings` (глобальная переменная `gs`).

Пример использования
-------------------------

```python
from src.credentials import gs

# Доступ к настройкам
print(gs.base_dir)  # Путь к корневой директории проекта
print(gs.credentials.aliexpress.api_key)  # Алиэкспресс API ключ
print(gs.credentials.openai.owner.api_key) # OpenAI API ключ

# Доступ к параметрам конфигурации
print(gs.config.timestamp_format)  # Формат даты и времени
print(gs.config.project_name)  # Имя проекта
```

### Дополнительные сведения
- Для получения более подробной информации о работе с `ProgramSettings` и настройками проекта, ознакомьтесь с документацией по KeePass: [https://github.com/hypo69/hypotez/blob/master/src/keepass.md](https://github.com/hypo69/hypotez/blob/master/src/keepass.md).
- Для детального описания класса `ProgramSettings`  обратитесь к документации: [https://github.com/hypo69/hypotez/blob/master/src/credentials.md#programsettings](https://github.com/hypo69/hypotez/blob/master/src/credentials.md#programsettings).