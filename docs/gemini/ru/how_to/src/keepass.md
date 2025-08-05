### Как использовать этот блок кода

Описание
-------------------------
Этот код предназначен для работы с базой данных KeePass, в которой хранятся зашифрованные учетные данные. Он использует библиотеку `pykeepass` для доступа к файлу `credentials.kdbx` и извлекает различные API-ключи, токены и другие параметры для разных сервисов, таких как AliExpress, OpenAI, Gemini, Telegram, Discord, PrestaShop, SMTP, Facebook и Google API. Все извлеченные данные сохраняются в объекте `ProgramSettings.credentials` в виде атрибутов `SimpleNamespace`.

Шаги выполнения
-------------------------
1. **Открытие базы данных KeePass:**
   - Функция `_open_kp` пытается открыть файл базы данных `credentials.kdbx`.
   - Она читает пароль из файла `password.txt`, если он существует, или запрашивает его у пользователя через консоль.
   - В случае неудачи, попытка открытия повторяется несколько раз. Если все попытки неудачны, программа завершается.

2. **Загрузка учетных данных:**
   - После успешного открытия базы данных вызывается функция `_load_credentials`.
   - Эта функция вызывает методы загрузки для каждой категории учетных данных (Aliexpress, OpenAI, Gemini, Telegram, Discord, PrestaShop, SMTP, Facebook, Google API).
   - Каждый метод загрузки выполняет следующие действия:
     - Использует `kp.find_groups` для поиска нужной группы в базе данных KeePass.
     - Извлекает данные из кастомных свойств записи (`entry.custom_properties`) и пароля записи (`entry.password`).
     - Сохраняет извлеченные данные в `ProgramSettings.credentials` в виде атрибутов `SimpleNamespace`.

3. **Извлечение API и ключей для сервисов:**
   - **Aliexpress:** Из группы `suppliers/aliexpress/api` извлекаются `api_key`, `secret`, `tracking_id`, `email` и `password`.
   - **OpenAI:** Из группы `openai` извлекаются `api_key`, `project_api`. Из группы `openai/assistants` извлекается `assistant_id`.
   - **Gemini:** Из группы `gemini` извлекается `api_key`.
   - **Telegram:** Из группы `telegram` извлекается `token`.
   - **Discord:** Из группы `discord` извлекаются `application_id`, `public_key` и `bot_token`.
   - **PrestaShop:** Из группы `prestashop/clients` извлекаются `api_key`, `api_domain`, `db_server`, `db_user`, `db_password`. Из группы `prestashop/translation` извлекаются `server`, `port`, `database`, `user`, `password`.
   - **SMTP:** Из группы `smtp` извлекаются `server`, `port`, `user` и `password`.
   - **Facebook:** Из группы `facebook` извлекаются `app_id`, `app_secret` и `access_token`.
   - **Google API:** Из группы `google/gapi` извлекается `api_key`.

Пример использования
-------------------------

```python
# Пример использования API-ключа OpenAI, после извлечения из KeePass
from src.config import ProgramSettings

# Получение API-ключа OpenAI из ProgramSettings
openai_api_key = ProgramSettings.credentials.openai.api_key

# Использование API-ключа в коде
print(f"API-ключ OpenAI: {openai_api_key}")
```