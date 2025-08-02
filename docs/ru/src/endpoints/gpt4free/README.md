# Документация для разработчика: gpt4free

## Обзор

Этот документ предоставляет обзор проекта gpt4free, включая информацию об установке, использовании, структуре, а также сведения о лицензировании и авторских правах.

## Содержание

- [🆕 Что нового](#-whats-new)
- [📚 Содержание](#-table-of-contents)
- [⚡ Начало работы](#-getting-started)
  - [🛠 Установка](#-installation)
    - [🐳 Использование Docker](#-using-docker)
    - [🪟 Руководство для Windows (.exe)](#-windows-guide-exe)
    - [🐍 Установка через Python](#-python-installation)
- [💡 Использование](#-usage)
  - [📝 Генерация текста](#-text-generation)
  - [🎨 Генерация изображений](#-image-generation)
  - [🌐 Веб-интерфейс](#-web-interface)
  - [🖥️ Локальный вывод](#-local-inference)
  - [🤖 API вывода](#-interference-api)
  - [🛠️ Конфигурация](#-configuration)
  - [📱 Запуск на смартфоне](#-run-on-smartphone)
  - [📘 Полная документация для Python API](#-full-documentation-for-python-api)
- [🚀 Провайдеры и модели](#-providers-and-models)
- [🔗 Работает на gpt4free](#-powered-by-gpt4free)
- [🤝 Вклад](#-contribute)
  - [Как создать нового провайдера?](#guide-how-do-i-create-a-new-provider)
  - [Как AI может помочь мне с написанием кода?](#guide-how-can-ai-help-me-with-writing-code)
- [🙌 Участники](#-contributors)
- [©️ Авторские права](#-copyright)
- [⭐ История звезд](#-star-history)
- [📄 Лицензия](#-license)

## Подробнее

Проект gpt4free представляет собой API-пакет для запросов к различным AI-провайдерам. Он предоставляет функции для балансировки нагрузки, управления потоком запросов, а также поддержку генерации текста и изображений. В данном документе описаны основные шаги по установке и использованию gpt4free, а также информация о лицензии и способах внесения вклада в проект.

## Начало работы

### Установка

#### Использование Docker

1.  **Установите Docker:**
    *   [Загрузите и установите Docker](https://docs.docker.com/get-docker/).

2.  **Настройте директории:**
    *   Убедитесь, что необходимые директории данных существуют или могут быть созданы.

    ```bash
    mkdir -p ${PWD}/har_and_cookies ${PWD}/generated_images
    sudo chown -R 1200:1201 ${PWD}/har_and_cookies ${PWD}/generated_images
    ```

3.  **Запустите Docker контейнер:**
    *   Используй следующие команды для скачивания последнего образа и запуска контейнера (только x64):

    ```bash
    docker pull hlohaus789/g4f
    docker run -p 8080:8080 -p 7900:7900 \
      --shm-size="2g" \
      -v ${PWD}/har_and_cookies:/app/har_and_cookies \
      -v ${PWD}/generated_images:/app/generated_images \
      hlohaus789/g4f:latest
    ```

4.  **Запуск Slim Docker Image:**
    *   Используй следующие команды для запуска Slim Docker Image. Эта команда также обновляет пакет `g4f` при запуске и устанавливает дополнительные зависимости (x64 и arm64):

    ```bash
    mkdir -p ${PWD}/har_and_cookies ${PWD}/generated_images
    chown -R 1000:1000 ${PWD}/har_and_cookies ${PWD}/generated_images
    docker run \
      -p 1337:1337 \
      -v ${PWD}/har_and_cookies:/app/har_and_cookies \
      -v ${PWD}/generated_images:/app/generated_images \
      hlohaus789/g4f:latest-slim \
      rm -r -f /app/g4f/ \
      && pip install -U g4f[slim] \
      && python -m g4f --debug
    ```

5.  **Доступ к клиентскому интерфейсу:**
    *   Чтобы использовать включенный клиент, перейдите по адресу: [http://localhost:8080/chat/](http://localhost:8080/chat/)
    *   Или установите базовый API для вашего клиента на: [http://localhost:8080/v1](http://localhost:8080/v1)

6.  **(Опционально) Вход в провайдер:**
    *   При необходимости вы можете получить доступ к рабочему столу контейнера здесь: [http://localhost:7900/?autoconnect=1&resize=scale&password=secret](http://localhost:7900/?autoconnect=1&resize=scale&password=secret) для целей входа в систему провайдера.

#### Руководство для Windows (.exe)

1.  **Скачайте приложение**:
    *   Посетите [страницу релизов](https://github.com/xtekky/gpt4free/releases/tag/0.4.2.0) и скачайте последнюю версию приложения с именем `g4f.exe.zip`.

2.  **Разместите файлы**:
    *   После скачивания найдите `.zip` файл в папке загрузок. Распакуйте его в выбранный каталог в вашей системе, затем запустите файл `g4f.exe`, чтобы запустить приложение.

3.  **Откройте GUI**:
    *   Приложение запускает веб-сервер с GUI. Откройте ваш любимый браузер и перейдите по адресу [http://localhost:8080/chat/](http://localhost:8080/chat/), чтобы получить доступ к интерфейсу приложения.

4.  **Настройте брандмауэр (Hotfix)**:
    *   При установке может потребоваться настроить параметры брандмауэра Windows, чтобы разрешить приложению работать правильно. Для этого откройте параметры брандмауэра Windows и разрешите приложению.

#### Установка через Python

1.  **Предварительные требования:**
    *   Установите Python 3.10+ с [python.org](https://www.python.org/downloads/).
    *   Установите Google Chrome для определенных провайдеров.

2.  **Установите с помощью PyPI:**

    ```bash
    pip install -U g4f[all]
    ```

    > Как установить только части или отключить части? **Используй частичные требования:** [/docs/requirements](docs/requirements.md)

3.  **Установите из исходного кода:**

    ```bash
    git clone https://github.com/xtekky/gpt4free.git
    cd gpt4free
    pip install -r requirements.txt
    ```

    > Как загрузить проект с помощью git и установить требования проекта? **Прочитайте этот учебник и следуйте ему шаг за шагом:** [/docs/git](docs/git.md)

## Использование

### Генерация текста

```python
from g4f.client import Client

client = Client()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
    web_search=False
)
print(response.choices[0].message.content)
```

```
Hello! How can I assist you today?
```

### Генерация изображений

```python
from g4f.client import Client

client = Client()
response = client.images.generate(
    model="flux",
    prompt="a white siamese cat",
    response_format="url"
)

print(f"Generated image URL: {response.data[0].url}")
```

### Веб-интерфейс

**Запустите GUI с помощью Python:**

```python
from g4f.gui import run_gui

run_gui()
```

**Запустите через CLI (чтобы запустить Flask Server):**

```bash
python -m g4f.cli gui --port 8080 --debug
```

**Или запустите FastAPI Server:**

```bash
python -m g4f --port 8080 --debug
```

> **Подробнее о GUI:** Для получения подробных инструкций о том, как настроить, конфигурировать и использовать GPT4Free GUI, обратитесь к [GUI Documentation](docs/gui.md). Это руководство включает пошаговые инструкции по выбору провайдера, управлению беседами, использованию расширенных функций, таких как распознавание речи, и многое другое.

### API вывода

**Interference API** обеспечивает интеграцию с сервисами OpenAI через G4F, что позволяет развертывать эффективные AI-решения.

*   **Документация**: [Interference API Docs](docs/interference-api.md)
*   **Endpoint**: `http://localhost:1337/v1`
*   **Swagger UI**: Доступ к документации OpenAPI через Swagger UI по адресу `http://localhost:1337/docs`
*   **Выбор провайдера**: [How to Specify a Provider?](docs/selecting_a_provider.md)

### Запуск на смартфоне

Запустите Web UI на своем смартфоне для удобного доступа в дороге. Ознакомьтесь со специальным руководством, чтобы узнать, как настроить и использовать GUI на мобильном устройстве: [Run on Smartphone Guide](docs/guides/phone.md)

### Полная документация для Python API

*   **Client API from G4F:** [/docs/client](docs/client.md)
*   **AsyncClient API from G4F:** [/docs/async_client](docs/async_client.md)
*   **Requests API from G4F:** [/docs/requests](docs/requests.md)
*   **File API from G4F:** [/docs/file](docs/file.md)
*   **PydanticAI and LangChain Integration for G4F:** [/docs/pydantic_ai](docs/pydantic_ai.md)
*   **Legacy API with python modules:** [/docs/legacy](docs/legacy.md)
*   **G4F - Media Documentation** [/docs/media](/docs/media.md) *(New)*

## Работает на gpt4free

В данном разделе представлена таблица проектов, использующих gpt4free, с указанием количества звезд, форков, проблем и pull-запросов.

## Вклад

Приветствуются вклады от сообщества. Добавление новых провайдеров или функций, исправление опечаток и небольшие улучшения.

###### Руководство: Как создать нового провайдера?

*   **Читать:** [Create Provider Guide](docs/guides/create_provider.md)

###### Руководство: Как AI может помочь мне с написанием кода?

*   **Читать:** [AI Assistance Guide](docs/guides/help_me.md)

## Участники

Список всех участников доступен [здесь](https://github.com/xtekky/gpt4free/graphs/contributors)

## Авторские права

Эта программа лицензирована в соответствии с [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.txt)

```
xtekky/gpt4free: Copyright (C) 2023 xtekky

Эта программа является свободным программным обеспечением: вы можете распространять и/или изменять ее
в соответствии с условиями GNU General Public License, опубликованной
Free Software Foundation, либо версии 3 Лицензии, либо
(по вашему выбору) любой более поздней версии.

Эта программа распространяется в надежде, что она будет полезной,
но БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ; даже без подразумеваемой гарантии
КОММЕРЧЕСКОЙ ПРИГОДНОСТИ или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННОЙ ЦЕЛИ. См.
GNU General Public License для получения более подробной информации.

Вы должны были получить копию GNU General Public License
вместе с этой программой. Если нет, см. <https://www.gnu.org/licenses/>.
```

## История звезд

График истории звезд репозитория.

## Лицензия

Проект лицензирован в соответствии с [GNU GPL v3.0](https://github.com/xtekky/gpt4free/blob/main/LICENSE).