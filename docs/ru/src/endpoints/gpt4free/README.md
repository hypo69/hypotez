# Документация для проекта `gpt4free`

## Обзор

Этот документ предоставляет обзор проекта `gpt4free`, включая информацию об установке, использовании, структуре, лицензировании и способах внесения вклада. `gpt4free` представляет собой API-пакет для работы с различными AI-провайдерами, демонстрирующий такие возможности, как балансировка нагрузки, управление потоком запросов, а также поддержку генерации текста и изображений.

## Подробнее

Проект `gpt4free` разработан как Proof-of-Concept (PoC) для демонстрации возможностей API-пакета с мультипровайдерными запросами. Он предоставляет удобный способ интеграции с различными AI-провайдерами, предлагая функции балансировки нагрузки и управления потоком запросов. Это позволяет разработчикам легко использовать различные AI-модели и сервисы, упрощая процесс разработки AI-приложений.

## Содержание

- [🆕 Что нового](#-whats-new)
- [📚 Оглавление](#-table-of-contents)
- [⚡ Начало работы](#-getting-started)
  - [🛠 Установка](#-installation)
    - [🐳 Использование Docker](#-using-docker)
    - [🪟 Инструкция для Windows (.exe)](#-windows-guide-exe)
    - [🐍 Установка Python](#-python-installation)
- [💡 Использование](#-usage)
  - [📝 Генерация текста](#-text-generation)
  - [🎨 Генерация изображений](#-image-generation)
  - [🌐 Веб-интерфейс](#-web-interface)
  - [🖥️ Локальный вывод](docs/local.md)
  - [🤖 API вывода](#-interference-api)
  - [🛠️ Конфигурация](docs/configuration.md)
  - [📱 Запуск на смартфоне](#-run-on-smartphone)
  - [📘 Полная документация для Python API](#-full-documentation-for-python-api)
- [🚀 Провайдеры и модели](docs/providers-and-models.md)
- [🔗 На базе gpt4free](#-powered-by-gpt4free)
- [🤝 Вклад](#-contribute)
  - [Как создать нового провайдера?](#guide-how-do-i-create-a-new-provider)
  - [Как ИИ может помочь мне с написанием кода?](#guide-how-can-ai-help-me-with-writing-code)
- [🙌 Участники](#-contributors)
- [©️ Авторские права](#-copyright)
- [⭐ История звезд](#-star-history)
- [📄 Лицензия](#-license)

## ⚡️ Начало работы

### 🛠 Установка

#### 🐳 Использование Docker

1.  **Установите Docker:** [Скачайте и установите Docker](https://docs.docker.com/get-docker/).
2.  **Настройте директории:** Перед запуском контейнера убедитесь, что необходимые директории для данных существуют или могут быть созданы. Например, вы можете создать и установить владельца для этих директорий, выполнив:

```bash
mkdir -p ${PWD}/har_and_cookies ${PWD}/generated_images
sudo chown -R 1200:1201 ${PWD}/har_and_cookies ${PWD}/generated_images
```

3.  **Запустите Docker-контейнер:** Используйте следующие команды, чтобы получить последнее изображение и запустить контейнер (только x64):

```bash
docker pull hlohaus789/g4f
docker run -p 8080:8080 -p 7900:7900 \
  --shm-size="2g" \
  -v ${PWD}/har_and_cookies:/app/har_and_cookies \
  -v ${PWD}/generated_images:/app/generated_images \
  hlohaus789/g4f:latest
```

4.  **Запуск Slim Docker Image:** Используйте следующие команды для запуска Slim Docker Image. Эта команда также обновляет пакет `g4f` при запуске и устанавливает любые дополнительные зависимости: (x64 и arm64)

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
    *   **Чтобы использовать включенный клиент, перейдите по адресу:** [http://localhost:8080/chat/](http://localhost:8080/chat/)
    *   **Или установите базовый API для вашего клиента на:** [http://localhost:8080/v1](http://localhost:8080/v1)

6.  **(Необязательно) Вход в систему провайдера:**
    При необходимости вы можете получить доступ к рабочему столу контейнера здесь: [http://localhost:7900/?autoconnect=1&resize=scale&password=secret](http://localhost:7900/?autoconnect=1&resize=scale&password=secret) для целей входа в систему провайдера.

#### 🪟 Инструкция для Windows (.exe)

Чтобы обеспечить бесперебойную работу приложения, следуйте приведенным ниже инструкциям. Эти шаги предназначены для ознакомления с процессом установки в операционных системах Windows.

**Этапы установки:**

1.  **Скачайте приложение:** Посетите нашу [страницу релизов](https://github.com/xtekky/gpt4free/releases/tag/0.4.2.0) и скачайте самую последнюю версию приложения с именем `g4f.exe.zip`.
2.  **Размещение файла:** После скачивания найдите `.zip` файл в папке загрузок. Распакуйте его в выбранный каталог в вашей системе, затем запустите файл `g4f.exe`, чтобы запустить приложение.
3.  **Откройте GUI:** Приложение запускает веб-сервер с GUI. Откройте свой любимый браузер и перейдите по адресу [http://localhost:8080/chat/](http://localhost:8080/chat/), чтобы получить доступ к интерфейсу приложения.
4.  **Конфигурация брандмауэра (Hotfix):** После установки может потребоваться настроить параметры брандмауэра Windows, чтобы приложение работало правильно. Для этого перейдите к настройкам брандмауэра Windows и разрешите работу приложения.

Выполнив эти шаги, вы сможете успешно установить и запустить приложение в своей системе Windows. Если у вас возникнут какие-либо проблемы во время установки, обратитесь к нашему Issue Tracker или попробуйте связаться с нами через Discord для получения помощи.

#### 🐍 Установка Python

##### Предварительные требования:

1.  Установите Python 3.10+ с сайта [python.org](https://www.python.org/downloads/).
2.  Установите Google Chrome для определенных провайдеров.

##### Установка с помощью PyPI:

```bash
pip install -U g4f[all]
```

> Как установить только части или отключить части? **Используйте частичные требования:** [/docs/requirements](docs/requirements.md)

##### Установка из исходного кода:

```bash
git clone https://github.com/xtekky/gpt4free.git
cd gpt4free
pip install -r requirements.txt
```

> Как загрузить проект с помощью git и установить требования проекта? **Прочитайте этот учебник и выполните его шаг за шагом:** [/docs/git](docs/git.md)

## 💡 Использование

### 📝 Генерация текста

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

### 🎨 Генерация изображений

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

[![Image with cat](/docs/images/cat.jpeg)](docs/client.md)

### 🌐 Веб-интерфейс

**Запустите GUI с помощью Python:**

```python
from g4f.gui import run_gui

run_gui()
```

**Запустите через CLI (Для запуска Flask Server):**

```bash
python -m g4f.cli gui --port 8080 --debug
```

**Или запустите FastAPI Server:**

```bash
python -m g4f --port 8080 --debug
```

> **Узнайте больше о GUI:** Подробные инструкции о том, как настроить, конфигурировать и использовать GPT4Free GUI, см. в [Документации GUI](docs/gui.md). Это руководство включает пошаговые инструкции по выбору провайдера, управлению беседами, использованию расширенных функций, таких как распознавание речи, и многое другое.

### 🤖 API вывода

**API вывода** обеспечивает простую интеграцию со службами OpenAI через G4F, что позволяет развертывать эффективные решения ИИ.

*   **Документация**: [Interference API Docs](docs/interference-api.md)
*   **Endpoint**: `http://localhost:1337/v1`
*   **Swagger UI**: Изучите документацию OpenAPI через Swagger UI по адресу `http://localhost:1337/docs`
*   **Provider Selection**: [How to Specify a Provider?](docs/selecting_a_provider.md)

Этот API разработан для простой реализации и улучшенной совместимости с другими интеграциями OpenAI.

### 📱 Запуск на смартфоне

Запустите веб-интерфейс на своем смартфоне для удобного доступа в дороге. Ознакомьтесь со специальным руководством, чтобы узнать, как настроить и использовать GUI на своем мобильном устройстве: [Руководство по запуску на смартфоне](docs/guides/phone.md)

### 📘 Полная документация для Python API

*   **Client API from G4F:** [/docs/client](docs/client.md)
*   **AsyncClient API from G4F:** [/docs/async_client](docs/async_client.md)
*   **Requests API from G4F:** [/docs/requests](docs/requests.md)
*   **File API from G4F:** [/docs/file](docs/file.md)
*   **PydanticAI and LangChain Integration for G4F:** [/docs/pydantic_ai](docs/pydantic_ai.md)
*   **Legacy API with python modules:** [/docs/legacy](docs/legacy.md)
*   **G4F - Media Documentation** [/docs/media](/docs/media.md) *(New)*

## 🔗 На базе gpt4free

В этом разделе представлен список проектов и библиотек, использующих `gpt4free`.

|                                 🎁 Проекты                                  | ⭐ Звезды | 📚 Форки | 🛎 Проблемы | 📬 Pull requests |
| :-------------------------------------------------------------------------: | :-------: | :-------: | :--------: | :---------------: |
|               **[gpt4free](https://github.com/xtekky/gpt4free)**               |   <img alt="Stars" src="https://img.shields.io/github/stars/xtekky/gpt4free?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/xtekky/gpt4free?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/xtekky/gpt4free?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/xtekky/gpt4free?style=flat-square&labelColor=343b41" />   |
|           **[gpt4free-ts](https://github.com/xiangsx/gpt4free-ts)**           |   <img alt="Stars" src="https://img.shields.io/github/stars/xiangsx/gpt4free-ts?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/xiangsx/gpt4free-ts?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/xiangsx/gpt4free-ts?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/xiangsx/gpt4free-ts?style=flat-square&labelColor=343b41" />   |
| **[Free AI API's & Potential Providers List](https://github.com/zukixa/cool-ai-stuff/)** |   <img alt="Stars" src="https://img.shields.io/github/stars/zukixa/cool-ai-stuff?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/zukixa/cool-ai-stuff?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/zukixa/cool-ai-stuff?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/zukixa/cool-ai-stuff?style=flat-square&labelColor=343b41" />   |
|       **[ChatGPT-Clone](https://github.com/xtekky/chatgpt-clone)**        |   <img alt="Stars" src="https://img.shields.io/github/stars/xtekky/chatgpt-clone?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/xtekky/chatgpt-clone?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/xtekky/chatgpt-clone?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/xtekky/chatgpt-clone?style=flat-square&labelColor=343b41" />   |
|            **[Ai agent](https://github.com/Josh-XT/AGiXT)**            |   <img alt="Stars" src="https://img.shields.io/github/stars/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |
|      **[ChatGpt Discord Bot](https://github.com/mishalhossin/Discord-Chatbot-Gpt4Free)**      |   <img alt="Stars" src="https://img.shields.io/github/stars/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/mishalhossin/Coding-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |
|    **[chatGPT-discord-bot](https://github.com/Zero6992/chatGPT-discord-bot)**    |   <img alt="Stars" src="https://img.shields.io/github/stars/Zero6992/chatGPT-discord-bot?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/Zero6992/chatGPT-discord-bot?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/Zero6992/chatGPT-discord-bot?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/Zero6992/chatGPT-discord-bot?style=flat-square&labelColor=343b41" />   |
|         **[Nyx-Bot (Discord)](https://github.com/SamirXR/Nyx-Bot)**         |   <img alt="Stars" src="https://img.shields.io/github/stars/SamirXR/Nyx-Bot?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/SamirXR/Nyx-Bot?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/SamirXR/Nyx-Bot?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/SamirXR/Nyx-Bot?style=flat-square&labelColor=343b41" />   |
|      **[LangChain gpt4free](https://github.com/MIDORIBIN/langchain-gpt4free)**      |   <img alt="Stars" src="https://img.shields.io/github/stars/MIDORIBIN/langchain-gpt4free?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/MIDORIBIN/langchain-gpt4free?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/MIDORIBIN/langchain-gpt4free?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/MIDORIBIN/langchain-gpt4free?style=flat-square&labelColor=343b41" />   |
|    **[ChatGpt Telegram Bot](https://github.com/HexyeDEV/Telegram-Chatbot-Gpt4Free)**    |   <img alt="Stars" src="https://img.shields.io/github/stars/HexyeDEV/Telegram-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/HexyeDEV/Telegram-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/HexyeDEV/Telegram-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/HexyeDEV/Telegram-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />   |
|         **[ChatGpt Line Bot](https://github.com/Lin-jun-xiang/chatgpt-line-bot)**         |   <img alt="Stars" src="https://img.shields.io/github/stars/Lin-jun-xiang/chatgpt-line-bot?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/Lin-jun-xiang/chatgpt-line-bot?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/Lin-jun-xiang/chatgpt-line-bot?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/Lin-jun-xiang/chatgpt-line-bot?style=flat-square&labelColor=343b41" />   |
|    **[Action Translate Readme](https://github.com/Lin-jun-xiang/action-translate-readme)**    |   <img alt="Stars" src="https://img.shields.io/github/stars/Lin-jun-xiang/action-translate-readme?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/Lin-jun-xiang/action-translate-readme?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/Lin-jun-xiang/action-translate-readme?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/Lin-jun-xiang/action-translate-readme?style=flat-square&labelColor=343b41" />   |
|     **[Langchain Document GPT](https://github.com/Lin-jun-xiang/docGPT-streamlit)**     |   <img alt="Stars" src="https://img.shields.io/github/stars/Lin-jun-xiang/docGPT-streamlit?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/Lin-jun-xiang/docGPT-streamlit?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/Lin-jun-xiang/docGPT-streamlit?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/Lin-jun-xiang/docGPT-streamlit?style=flat-square&labelColor=343b41" />   |
|          **[python-tgpt](https://github.com/Simatwa/python-tgpt)**          |   <img alt="Stars" src="https://img.shields.io/github/stars/Simatwa/python-tgpt?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/Simatwa/python-tgpt?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/Simatwa/python-tgpt?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/Simatwa/python-tgpt?style=flat-square&labelColor=343b41" />   |
|             **[GPT4js](https://github.com/zachey01/gpt4free.js)**             |   <img alt="Stars" src="https://img.shields.io/github/stars/zachey01/gpt4free.js?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/zachey01/gpt4free.js?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/zachey01/gpt4free.js?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/zachey01/gpt4free.js?style=flat-square&labelColor=343b41" />   |
|       **[VividNode (pyqt-openai)](https://github.com/yjg30737/pyqt-openai)**       |   <img alt="Stars" src="https://img.shields.io/github/stars/yjg30737/pyqt-openai?style=flat-square&labelColor=343b41" />   |   <img alt="Forks" src="https://img.shields.io/github/forks/yjg30737/pyqt-openai?style=flat-square&labelColor=343b41" />   |   <img alt="Issues" src="https://img.shields.io/github/issues/yjg30737/pyqt-openai?style=flat-square&labelColor=343b41" />   |   <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/yjg30737/pyqt-openai?style=flat-square&labelColor=343b41" />   |

## 🤝 Вклад

Мы приветствуем вклад сообщества. Если вы добавляете новых провайдеров или функции, или просто исправляете опечатки и вносите небольшие улучшения, ваш вклад ценится. Создание pull request - это все, что нужно - наш сопроцессор обработает процесс проверки кода. После того, как все изменения будут внесены, мы объединим pull request в основную ветку и выпустим обновления позднее.

###### Руководство: Как создать нового провайдера?

*   **Прочитайте:** [Руководство по созданию провайдера](docs/guides/create_provider.md)

###### Руководство: Как ИИ может помочь мне с написанием кода?

*   **Прочитайте:** [Руководство по помощи ИИ](docs/guides/help_me.md)

## 🙌 Участники

Список всех участников доступен [здесь](https://github.com/xtekky/gpt4free/graphs/contributors)

[![](https://avatars.githubusercontent.com/u/98614666?v=4&s=45)](https://github.com/xtekky)
[![](https://avatars.githubusercontent.com/u/983577?v=4&s=45)](https://github.com/hlohaus)
[![](https://avatars.githubusercontent.com/u/166700875?v=4&s=45)](https://github.com/kqlio67)
[![](https://avatars.githubusercontent.com/u/36830534?v=4&s=45)](https://github.com/bagusindrayana)
[![](https://avatars.githubusercontent.com/u/22415463?v=4&s=45)](https://github.com/sudouser777)
[![](https://avatars.githubusercontent.com/u/139662282?v=4&s=45)](https://github.com/thatlukinhasguy1)
[![](https://avatars.githubusercontent.com/u/36051603?v=4&s=45)](https://github.com/Commenter123321)
[![](https://avatars.githubusercontent.com/u/20585236?v=4&s=45)](https://github.com/DanielShemesh)
[![](https://avatars.githubusercontent.com/u/73485421?v=4&s=45)](https://github.com/Luneye)
[![](https://avatars.githubusercontent.com/u/185073927?v=4&s=45)](https://github.com/foxfire52)
[![](https://avatars.githubusercontent.com/u/100193740?v=4&s=45)](https://github.com/ezerinz)
[![](https://avatars.githubusercontent.com/u/69082498?v=4&s=45)](https://github.com/enganese)
[![](https://avatars.githubusercontent.com/u/63782903?v=4&s=45)](https://github.com/Lin-jun-xiang)
[![](https://avatars.githubusercontent.com/u/139914347?v=4&s=45)](https://github.com/nullstreak)
[![](https://avatars.githubusercontent.com/u/81074936?v=4&s=45)](https://github.com/valerii-chirkov)
[![](https://avatars.githubusercontent.com/u/25425217?v=4&s=45)](https://github.com/MIDORIBIN)
[![](https://avatars.githubusercontent.com/u/2671466?v=4&s=45)](https://github.com/repollo)
[![](https://avatars.githubusercontent.com/u/54535414?v=4&s=45)](https://github.com/hpsj)
[![](https://avatars.githubusercontent.com/u/63543716?v=4&s=45)](https://github.com/taiyi747)
[![](https://avatars.githubusercontent.com/u/56563509?v=4&s=45)](https://github.com/zukixa)
[![](https://avatars.githubusercontent.com/u/55257054?v=4&s=45)](https://github.com/ostix360)
[![](https://avatars.githubusercontent.com/u/143020293?v=4&s=45)](https://github.com/WdR-Tech)
[![](https://avatars.githubusercontent.com/u/65314629?v=4&s=45)](https://github.com/HexyeDEV)
[![](https://avatars.githubusercontent.com/u/71867245?v=4&s=45)](https://github.com/9fo)
[![](https://avatars.githubusercontent.com/u/77636021?v=4&s=45)](https://github.com/devAdityaa)
[![](https://avatars.githubusercontent.com/u/109844019?v=4&s=45)](https://github.com/24rr)
[![](https://avatars.githubusercontent.com/u/47846202?v=4&s=45)](https://github.com/zeng-rr)
[![](https://avatars.githubusercontent.com/u/182319878?v=4&s=45)](https://github.com/rkihacker)
[![](https://avatars.githubusercontent.com/u/44613678?v=4&s=45)](https://github.com/naa7)
[![](https://avatars.githubusercontent.com/u/13617054?v=4&s=45)](https://github.com/ramon-