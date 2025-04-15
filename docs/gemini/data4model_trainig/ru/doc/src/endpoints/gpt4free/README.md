# Документация для разработчика по проекту gpt4free

## Обзор

Этот документ предназначен для разработчиков, желающих понять структуру и функциональность проекта `gpt4free`. Здесь представлено описание основных компонентов, способов установки и использования, а также информация о лицензировании и вкладе в проект.

## Содержание

- [Обзор](#обзор)
- [Содержание](#содержание)
- [Введение](#введение)
- [Что нового](#что-нового)
- [Установка](#установка)
  - [Использование Docker](#использование-docker)
  - [Установка на Windows (.exe)](#установка-на-windows-exe)
  - [Установка с помощью Python](#установка-с-помощью-python)
- [Использование](#использование)
  - [Генерация текста](#генерация-текста)
  - [Генерация изображений](#генерация-изображений)
  - [Веб-интерфейс](#веб-интерфейс)
  - [API для интеграции](#api-для-интеграции)
  - [Запуск на смартфоне](#запуск-на-смартфоне)
- [Полная документация по Python API](#полная-документация-по-python-api)
- [Проект powered by gpt4free](#проект-powered-by-gpt4free)
- [Вклад в проект](#вклад-в-проект)
- [Авторы](#авторы)
- [Лицензия](#лицензия)
- [История звезды](#история-звезды)

## Введение

Проект `gpt4free` представляет собой API-пакет для выполнения запросов к различным AI-провайдерам. Он включает в себя такие функции, как балансировка нагрузки, контроль потока запросов, поддержку генерации текста и изображений. Проект предоставляет возможности для интеграции с OpenAI и поддерживает развертывание эффективных AI-решений.

## Что нового

В этом разделе представлена информация о последних обновлениях и новых функциях проекта. Для получения подробной информации рекомендуется посетить страницу [Releases Page](https://github.com/xtekky/gpt4free/releases). Также можно подписаться на новости в Telegram канале [telegram.me/g4f_channel](https://telegram.me/g4f_channel) или Discord канале [News Channel: discord.gg/5E39JUWUFa](https://discord.gg/5E39JUWUFa).

## Установка

### Использование Docker

#### Необходимые компоненты

- Установленный Docker.

#### Порядок установки

1.  **Установите Docker**: Скачайте и установите Docker с официального сайта [Docker](https://docs.docker.com/get-docker/).

2.  **Настройте директории**: Убедитесь, что необходимые директории для данных существуют или могут быть созданы. Например:

    ```bash
    mkdir -p ${PWD}/har_and_cookies ${PWD}/generated_images
    sudo chown -R 1200:1201 ${PWD}/har_and_cookies ${PWD}/generated_images
    ```

3.  **Запустите Docker-контейнер**: Используйте следующие команды для загрузки последнего образа и запуска контейнера (только x64):

    ```bash
    docker pull hlohaus789/g4f
    docker run -p 8080:8080 -p 7900:7900 \
      --shm-size="2g" \
      -v ${PWD}/har_and_cookies:/app/har_and_cookies \
      -v ${PWD}/generated_images:/app/generated_images \
      hlohaus789/g4f:latest
    ```

4.  **Запуск Slim Docker Image**: Для запуска Slim Docker Image используйте следующие команды. Эта команда также обновляет пакет `g4f` при запуске и устанавливает дополнительные зависимости (x64 и arm64):

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

5.  **Доступ к клиентскому интерфейсу**:

    -   Для использования включенного клиента перейдите по адресу: [http://localhost:8080/chat/](http://localhost:8080/chat/)
    -   Или установите API base для вашего клиента на: [http://localhost:8080/v1](http://localhost:8080/v1)

6.  **(Опционально) Логин провайдера**:
    При необходимости вы можете получить доступ к рабочему столу контейнера здесь: [http://localhost:7900/?autoconnect=1&resize=scale&password=secret](http://localhost:7900/?autoconnect=1&resize=scale&password=secret) для целей логина провайдера.

### Установка на Windows (.exe)

#### Порядок установки

1.  **Скачайте приложение**: Посетите страницу [releases page](https://github.com/xtekky/gpt4free/releases/tag/0.4.2.0) и скачайте последнюю версию приложения, названную `g4f.exe.zip`.

2.  **Разместите файл**: После загрузки найдите `.zip` файл в папке загрузок. Распакуйте его в выбранную директорию и запустите `g4f.exe` для запуска приложения.

3.  **Откройте GUI**: Приложение запустит веб-сервер с графическим интерфейсом. Откройте браузер и перейдите по адресу [http://localhost:8080/chat/](http://localhost:8080/chat/) для доступа к интерфейсу приложения.

4.  **Настройка брандмауэра (Hotfix)**: После установки может потребоваться настройка брандмауэра Windows для корректной работы приложения.

### Установка с помощью Python

#### Необходимые компоненты

1.  Python 3.10 или выше.
2.  Google Chrome (для некоторых провайдеров).

#### Установка с помощью PyPI

```bash
pip install -U g4f[all]
```

#### Установка из исходного кода

```bash
git clone https://github.com/xtekky/gpt4free.git
cd gpt4free
pip install -r requirements.txt
```

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

#### Запуск GUI через Python

```python
from g4f.gui import run_gui

run_gui()
```

#### Запуск через CLI

```bash
python -m g4f.cli gui --port 8080 --debug
```

#### Запуск FastAPI сервера

```bash
python -m g4f --port 8080 --debug
```

### API для интеграции

API предоставляет возможность интеграции с сервисами OpenAI через G4F.

-   **Документация**: [Interference API Docs](docs/interference-api.md)
-   **Endpoint**: `http://localhost:1337/v1`
-   **Swagger UI**: [http://localhost:1337/docs](http://localhost:1337/docs)

### Запуск на смартфоне

Инструкции по настройке и использованию GUI на мобильных устройствах можно найти в [Run on Smartphone Guide](docs/guides/phone.md).

## Полная документация по Python API

-   **Client API from G4F:** [/docs/client](docs/client.md)
-   **AsyncClient API from G4F:** [/docs/async_client](docs/async_client.md)
-   **Requests API from G4F:** [/docs/requests](docs/requests.md)
-   **File API from G4F:** [/docs/file](docs/file.md)
-   **PydanticAI and LangChain Integration for G4F:** [/docs/pydantic_ai](docs/pydantic_ai.md)
-   **Legacy API with python modules:** [/docs/legacy](docs/legacy.md)
-   **G4F - Media Documentation** [/docs/media](/docs/media.md) *(New)*

## Проект powered by gpt4free

В этом разделе представлена таблица проектов, использующих `gpt4free`.

## Вклад в проект

Приветствуются любые вклады в проект. Для внесения изменений создайте pull request.

#### Руководства

-   [Create Provider Guide](docs/guides/create_provider.md)
-   [AI Assistance Guide](docs/guides/help_me.md)

## Авторы

Список всех авторов доступен [здесь](https://github.com/xtekky/gpt4free/graphs/contributors).

## Лицензия

Проект лицензирован под GNU GPL v3. Дополнительную информацию можно найти в файле [LICENSE](https://github.com/xtekky/gpt4free/blob/main/LICENSE).

## История звезды

График истории звезд проекта.
```
<a href="https://github.com/xtekky/gpt4free/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=xtekky/gpt4free&type=Date">
</a>