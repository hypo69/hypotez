# gpt4free

[![xtekky%2Fgpt4free | Trendshift](https://trendshift.io/api/badge/repositories/1692)](https://trendshift.io/repositories/1692)

---

<p align="center">
  <span style="background: linear-gradient(45deg, #12c2e9, #c471ed, #f64f59); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
    <strong>Автор: <a href="https://github.com/xtekky">@xtekky</a></strong>
  </span>
</p>

[В начало](#top)

> [!IMPORTANT]
> Используя этот репозиторий или любой связанный с ним код, вы соглашаетесь с [юридическим уведомлением](LEGAL_NOTICE.md). Автор **не несет ответственности за использование этого репозитория и не поддерживает его**, а также не несет ответственности за какие-либо копии, форки, повторные загрузки, сделанные другими пользователями, или что-либо еще, связанное с GPT4Free. Это единственная учетная запись и репозиторий автора. Чтобы предотвратить выдачу себя за другого или безответственные действия, пожалуйста, соблюдайте лицензию GNU GPL, которую использует этот репозиторий.

> [!WARNING]
> _"gpt4free"_ служит **PoC** (доказательством концепции), демонстрирующим разработку API-пакета с запросами от нескольких провайдеров, с такими функциями, как тайм-ауты, балансировка нагрузки и управление потоком.

> [!NOTE]
> <sup><strong>Последняя версия:</strong></sup><br> [![PyPI version](https://img.shields.io/pypi/v/g4f?color=blue)](https://pypi.org/project/g4f) [![Docker version](https://img.shields.io/docker/v/hlohaus789/g4f?label=docker&color=blue)](https://hub.docker.com/r/hlohaus789/g4f)  
> <sup><strong>Статистика:</strong></sup><br> [![Downloads](https://static.pepy.tech/badge/g4f)](https://pepy.tech/project/g4f) [![Downloads](https://static.pepy.tech/badge/g4f/month)](https://pepy.tech/project/g4f)

```sh
pip install -U g4f[all]
```

```sh
docker pull hlohaus789/g4f
```

## 🆕 Что нового

![1000032415](https://github.com/user-attachments/assets/4caab977-eb05-48ed-b750-3ad082bcfcae)

*   **Изучите последние функции и обновления**
    Подробную информацию можно найти на нашей [странице релизов](https://github.com/xtekky/gpt4free/releases).

*   **Будьте в курсе новостей в нашем Telegram-канале** 📨
    Присоединяйтесь к нам в [telegram.me/g4f_channel](https://telegram.me/g4f_channel).

*   **Подпишитесь на наш новостной канал Discord** 💬🆕️
    Будьте в курсе обновлений через наш [новостной канал: discord.gg/5E39JUWUFa](https://discord.gg/5E39JUWUFa).

*   **Получите поддержку в нашем Discord-сообществе** 🤝💻
    Обратитесь за помощью в нашу [группу поддержки: discord.gg/qXA4Wf4Fsm](https://discord.gg/qXA4Wf4Fsm).

## 🔻 Снятие сайта

Ваш сайт находится в этом репозитории, и вы хотите его снять? Отправьте электронное письмо по адресу takedown@g4f.ai с доказательством того, что он принадлежит вам, и он будет удален как можно быстрее. Чтобы предотвратить воспроизведение, пожалуйста, защитите свой API. 😉

## 🚀 GPT4Free на HuggingFace

[![HuggingSpace](https://github.com/user-attachments/assets/1d859e8a-d6fa-416f-a213-ccc26aa11e90)](https://huggingface.co/spaces/roxky/g4f-new)

**Это API-пакет для мультипровайдерских AI-запросов, демонстрирующий такие функции, как:**

*   Балансировка нагрузки и управление потоком запросов.
*   Бесшовная интеграция с несколькими AI-провайдерами.
*   Комплексная поддержка генерации текста и изображений.

> Изучите [посетите GPT4Free в HuggingFace Space](https://huggingface.co/spaces/roxky/g4f-new) для размещенной версии или [Duplicate GPT4Free Space](https://huggingface.co/spaces/roxky/g4f-new?duplicate=true) для личного использования.

---

## 📚 Содержание

*   [🆕 Что нового](#-whats-new)
*   [📚 Содержание](#-table-of-contents)
*   [⚡️ Начало работы](#-getting-started)
    *   [🛠 Установка](#-installation)
        *   [🐳 Использование Docker](#-using-docker)
        *   [🪟 Руководство по Windows (.exe)](#-windows-guide-exe)
        *   [🐍 Установка Python](#-python-installation)
*   [💡 Использование](#-usage)
    *   [📝 Генерация текста](#-text-generation)
    *   [🎨 Генерация изображений](#-image-generation)
    *   [🌐 Веб-интерфейс](#-web-interface)
    *   [🖥️ Локальный вывод](docs/local.md)
    *   [🤖 API для вывода](#-interference-api)
    *   [🛠️ Конфигурация](docs/configuration.md)
    *   [📱 Запуск на смартфоне](#-run-on-smartphone)
    *   [📘 Полная документация для Python API](#-full-documentation-for-python-api)
*   [🚀 Провайдеры и модели](docs/providers-and-models.md)
*   [🔗 Работает на gpt4free](#-powered-by-gpt4free)
*   [🤝 Вклад](#-contribute)
    *   [Как создать нового провайдера?](#guide-how-do-i-create-a-new-provider)
    *   [Как AI может помочь мне в написании кода?](#guide-how-can-ai-help-me-with-writing-code)
*   [🙌 Участники](#-contributors)
*   [©️ Авторское право](#-copyright)
*   [⭐ История звезд](#-star-history)
*   [📄 Лицензия](#-license)

---

## ⚡️ Начало работы

## 🛠 Установка

### 🐳 Использование Docker

1.  **Установите Docker:** [Загрузите и установите Docker](https://docs.docker.com/get-docker/).
2.  **Настройте каталоги:** Перед запуском контейнера убедитесь, что необходимые каталоги данных существуют или могут быть созданы. Например, вы можете создать и установить права собственности на эти каталоги, выполнив:

```bash
mkdir -p ${PWD}/har_and_cookies ${PWD}/generated_images
sudo chown -R 1200:1201 ${PWD}/har_and_cookies ${PWD}/generated_images
```

3.  **Запустите Docker-контейнер:** Используйте следующие команды, чтобы загрузить последнее изображение и запустить контейнер (только x64):

```bash
docker pull hlohaus789/g4f
docker run -p 8080:8080 -p 7900:7900 \
  --shm-size="2g" \
  -v ${PWD}/har_and_cookies:/app/har_and_cookies \
  -v ${PWD}/generated_images:/app/generated_images \
  hlohaus789/g4f:latest
```

4.  **Запуск Slim Docker Image:** И используйте следующие команды для запуска Slim Docker Image. Эта команда также обновляет пакет `g4f` при запуске и устанавливает любые дополнительные зависимости: (x64 и arm64)

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

5.  **Получите доступ к клиентскому интерфейсу:**
    *   **Чтобы использовать включенный клиент, перейдите по адресу:** [http://localhost:8080/chat/](http://localhost:8080/chat/)
    *   **Или установите базовый API для своего клиента на:** [http://localhost:8080/v1](http://localhost:8080/v1)

6.  **(Необязательно) Вход в систему провайдера:**
    При необходимости вы можете получить доступ к рабочему столу контейнера здесь: http://localhost:7900/?autoconnect=1&resize=scale&password=secret для целей входа в систему провайдера.

---

### 🪟 Руководство по Windows (.exe)

Чтобы обеспечить бесперебойную работу нашего приложения, пожалуйста, следуйте приведенным ниже инструкциям. Эти шаги предназначены для того, чтобы помочь вам в процессе установки в операционных системах Windows.

**Этапы установки:**

1.  **Загрузите приложение**: Посетите нашу [страницу релизов](https://github.com/xtekky/gpt4free/releases/tag/0.4.2.0) и загрузите последнюю версию приложения под названием `g4f.exe.zip`.
2.  **Размещение файлов**: После загрузки найдите `.zip` файл в папке загрузок. Распакуйте его в выбранный вами каталог в вашей системе, затем выполните файл `g4f.exe`, чтобы запустить приложение.
3.  **Откройте GUI**: Приложение запускает веб-сервер с графическим интерфейсом. Откройте свой любимый браузер и перейдите по адресу [http://localhost:8080/chat/](http://localhost:8080/chat/), чтобы получить доступ к интерфейсу приложения.
4.  **Конфигурация брандмауэра (Hotfix)**: После установки может потребоваться настройка параметров брандмауэра Windows, чтобы разрешить правильную работу приложения. Для этого откройте параметры брандмауэра Windows и разрешите работу приложения.

Выполнив эти шаги, вы сможете успешно установить и запустить приложение в своей системе Windows. Если вы столкнетесь с какими-либо проблемами в процессе установки, пожалуйста, обратитесь к нашему трекеру проблем или попробуйте связаться с нами через Discord для получения помощи.

---

### 🐍 Установка Python

#### Предварительные условия:

1.  Установите Python 3.10+ с [python.org](https://www.python.org/downloads/).
2.  Установите Google Chrome для некоторых провайдеров.

#### Установите с помощью PyPI:

```bash
pip install -U g4f[all]
```

> Как установить только части или отключить части? **Используйте частичные требования:** [/docs/requirements](docs/requirements.md)

#### Установите из исходного кода:

```bash
git clone https://github.com/xtekky/gpt4free.git
cd gpt4free
pip install -r requirements.txt
```

> Как загрузить проект с помощью git и установить требования проекта? **Прочитайте этот учебник и следуйте ему шаг за шагом:** [/docs/git](docs/git.md)

---

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

**Запустите графический интерфейс с помощью Python:**

```python
from g4f.gui import run_gui

run_gui()
```

**Запустите через CLI (Чтобы запустить Flask Server):**

```bash
python -m g4f.cli gui --port 8080 --debug
```

**Или запустите FastAPI Server:**

```bash
python -m g4f --port 8080 --debug
```

> **Узнайте больше о графическом интерфейсе:** Подробные инструкции по настройке, конфигурированию и использованию GPT4Free GUI см. в [документации по GUI](docs/gui.md). Это руководство содержит пошаговые инструкции по выбору провайдера, управлению беседами, использованию расширенных функций, таких как распознавание речи, и многое другое.

---

### 🤖 Interference API

**Interference API** обеспечивает бесшовную интеграцию со службами OpenAI через G4F, что позволяет развертывать эффективные AI-решения.

*   **Документация**: [Interference API Docs](docs/interference-api.md)
*   **Конечная точка**: `http://localhost:1337/v1`
*   **Swagger UI**: Изучите документацию OpenAPI через Swagger UI по адресу `http://localhost:1337/docs`
*   **Выбор провайдера**: [Как указать провайдера?](docs/selecting_a_provider.md)

Этот API разработан для простой реализации и улучшенной совместимости с другими интеграциями OpenAI.

---

### 📱 Запуск на смартфоне

Запустите веб-интерфейс на своем смартфоне для легкого доступа в дороге. Ознакомьтесь со специальным руководством, чтобы узнать, как настроить и использовать графический интерфейс на своем мобильном устройстве: [Руководство по запуску на смартфоне](docs/guides/phone.md)

---

#### **📘 Полная документация для Python API**

*   **Client API из G4F:** [/docs/client](docs/client.md)
*   **AsyncClient API из G4F:** [/docs/async_client](docs/async_client.md)
*   **Requests API из G4F:** [/docs/requests](docs/requests.md)
*   **File API из G4F:** [/docs/file](docs/file.md)
*   **PydanticAI и LangChain Integration для G4F:** [/docs/pydantic_ai](docs/pydantic_ai.md)
*   **Legacy API с python-модулями:** [/docs/legacy](docs/legacy.md)
*   **G4F - Медиа-документация** [/docs/media](/docs/media.md) *(Новое)*

---

## 🔗 Работает на gpt4free

<table>
  <thead align="center">
    <tr border: none;>
      <td>
        <b>🎁 Проекты</b>
      </td>
      <td>
        <b>⭐ Звезды</b>
      </td>
      <td>
        <b>📚 Форки</b>
      </td>
      <td>
        <b>🛎 Проблемы</b>
      </td>
      <td>
        <b>📬 Запросы на включение</b>
      </td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <a href="https://github.com/xtekky/gpt4free">
          <b>gpt4free</b>
        </a>
      </td>
      <td>
        <a href="https://github.com/xtekky/gpt4free/stargazers">
          <img alt="Stars" src="https://img.shields.io/github/stars/xtekky/gpt4free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/xtekky/gpt4free/network/members">
          <img alt="Forks" src="https://img.shields.io/github/forks/xtekky/gpt4free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/xtekky/gpt4free/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/xtekky/gpt4free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/xtekky/gpt4free/pulls">
          <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/xtekky/gpt4free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
    </tr>
    <td>
      <a href="https://github.com/xiangsx/gpt4free-ts">
        <b>gpt4free-ts</b>
      </a>
    </td>
    <td>
      <a href="https://github.com/xiangsx/gpt4free-ts/stargazers">
        <img alt="Stars" src="https://img.shields.io/github/stars/xiangsx/gpt4free-ts?style=flat-square&labelColor=343b41" />
      </a>
    </td>
    <td>
      <a href="https://github.com/xiangsx/gpt4free-ts/network/members">
        <img alt="Forks" src="https://img.shields.io/github/forks/xiangsx/gpt4free-ts?style=flat-square&labelColor=343b41" />
      </a>
    </td>
    <td>
      <a href="https://github.com/xiangsx/gpt4free-ts/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/xiangsx/gpt4free-ts?style=flat-square&labelColor=343b41" />
      </a>
    </td>
    <td>
      <a href="https://github.com/xiangsx/gpt4free-ts/pulls">
        <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/xiangsx/gpt4free-ts?style=flat-square&labelColor=343b41" />
      </a>
    </td>
    </tr>
    <tr>
      <td>
        <a href="https://github.com/zukixa/cool-ai-stuff/">
          <b>Free AI API\'s & Potential Providers List</b>
        </a>
      </td>
      <td>
        <a href="https://github.com/zukixa/cool-ai-stuff/stargazers">
          <img alt="Stars" src="https://img.shields.io/github/stars/zukixa/cool-ai-stuff?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/zukixa/cool-ai-stuff/network/members">
          <img alt="Forks" src="https://img.shields.io/github/forks/zukixa/cool-ai-stuff?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/zukixa/cool-ai-stuff/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/zukixa/cool-ai-stuff?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/zukixa/cool-ai-stuff/pulls">
          <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/zukixa/cool-ai-stuff?style=flat-square&labelColor=343b41" />
        </a>
      </td>
    </tr>
    <tr>
    <tr>
      <td>
        <a href="https://github.com/xtekky/chatgpt-clone">
          <b>ChatGPT-Clone</b>
        </a>
      </td>
      <td>
        <a href="https://github.com/xtekky/chatgpt-clone/stargazers">
          <img alt="Stars" src="https://img.shields.io/github/stars/xtekky/chatgpt-clone?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/xtekky/chatgpt-clone/network/members">
          <img alt="Forks" src="https://img.shields.io/github/forks/xtekky/chatgpt-clone?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/xtekky/chatgpt-clone/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/xtekky/chatgpt-clone?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/xtekky/chatgpt-clone/pulls">
          <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/xtekky/chatgpt-clone?style=flat-square&labelColor=343b41" />
        </a>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://github.com/mishalhossin/Discord-Chatbot-Gpt4Free">
          <b>Ai agent</b>
        </a>
      </td>
      <td>
        <a href="https://github.com/Josh-XT/AGiXT/stargazers">
          <img alt="Stars" src="https://img.shields.io/github/stars/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/Josh-XT/AGiXT/network/members">
          <img alt="Forks" src="https://img.shields.io/github/forks/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/Josh-XT/AGiXT/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/Josh-XT/AGiXT/pulls">
          <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://github.com/mishalhossin/Discord-Chatbot-Gpt4Free">
          <b>ChatGpt Discord Bot</b>
        </a>
      </td>
      <td>
        <a href="https://github.com/mishalhossin/Discord-Chatbot-Gpt4Free/stargazers">
          <img alt="Stars" src="https://img.shields.io/github/stars/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/mishalhossin/Discord-Chatbot-Gpt4Free/network/members">
          <img alt="Forks" src="https://img.shields.io/github/forks/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/mishalhossin/Discord-Chatbot-Gpt4Free/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/mishalhossin/Coding-Chatbot-Gpt4Free/pulls">
          <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/mishalhossin/Discord-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
    <tr>
    <tr>
      <td>
        <a href="https://github.com/Zero6992/chatGPT-discord-bot">
          <b>chatGPT-discord-bot</b>
        </a>
      </td>
      <td>
        <a href="https://github.com/Zero6992/chatGPT-discord-bot/stargazers">
          <img alt="Stars" src="https://img.shields.io/github/stars/Zero6992/chatGPT-discord-bot?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/Zero6992/chatGPT-discord-bot/network/members">
          <img alt="Forks" src="https://img.shields.io/github/forks/Zero6992/chatGPT-discord-bot?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/Zero6992/chatGPT-discord-bot/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/Zero6992/chatGPT-discord-bot?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/Zero6992/chatGPT-discord-bot/pulls">
          <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/Zero6992/chatGPT-discord-bot?style=flat-square&labelColor=343b41" />
        </a>
      </td>
    <tr>
      <td>
        <a href="https://github.com/SamirXR/Nyx-Bot">
          <b>Nyx-Bot (Discord)</b>
        </a>
      </td>
      <td>
        <a href="https://github.com/SamirXR/Nyx-Bot/stargazers">
          <img alt="Stars" src="https://img.shields.io/github/stars/SamirXR/Nyx-Bot?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/SamirXR/Nyx-Bot/network/members">
          <img alt="Forks" src="https://img.shields.io/github/forks/SamirXR/Nyx-Bot?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/SamirXR/Nyx-Bot/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/SamirXR/Nyx-Bot?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/SamirXR/Nyx-Bot/pulls">
          <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/SamirXR/Nyx-Bot?style=flat-square&labelColor=343b41" />
        </a>
      </td>
    </tr>
    </tr>
    <tr>
      <td>
        <a href="https://github.com/MIDORIBIN/langchain-gpt4free">
          <b>LangChain gpt4free</b>
        </a>
      </td>
      <td>
        <a href="https://github.com/MIDORIBIN/langchain-gpt4free/stargazers">
          <img alt="Stars" src="https://img.shields.io/github/stars/MIDORIBIN/langchain-gpt4free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/MIDORIBIN/langchain-gpt4free/network/members">
          <img alt="Forks" src="https://img.shields.io/github/forks/MIDORIBIN/langchain-gpt4free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/MIDORIBIN/langchain-gpt4free/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/MIDORIBIN/langchain-gpt4free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/MIDORIBIN/langchain-gpt4free/pulls">
          <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/MIDORIBIN/langchain-gpt4free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://github.com/HexyeDEV/Telegram-Chatbot-Gpt4Free">
          <b>ChatGpt Telegram Bot</b>
        </a>
      </td>
      <td>
        <a href="https://github.com/HexyeDEV/Telegram-Chatbot-Gpt4Free/stargazers">
          <img alt="Stars" src="https://img.shields.io/github/stars/HexyeDEV/Telegram-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/HexyeDEV/Telegram-Chatbot-Gpt4Free/network/members">
          <img alt="Forks" src="https://img.shields.io/github/forks/HexyeDEV/Telegram-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/HexyeDEV/Telegram-Chatbot-Gpt4Free/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/HexyeDEV/Telegram-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/HexyeDEV/Telegram-Chatbot-Gpt4Free/pulls">
          <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/HexyeDEV/Telegram-Chatbot-Gpt4Free?style=flat-square&labelColor=343b41" />
        </a>
      </td>
    </tr>
    <tr>
      <td>
        <a href="https://github.com/Lin-jun-xiang/chatgpt-line-bot">
          <b>ChatGpt Line Bot</b>
        </a>
      </td>
      <td>
        <a href="https://github.com/Lin-jun-xiang/chatgpt-line-bot/stargazers">
          <img alt="Stars" src="https://img.shields.io/github/stars/Lin-jun-xiang/chatgpt-line-bot?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/Lin-jun-xiang/chatgpt-line-bot/network/members">
          <img alt="Forks" src="https://img.shields.io/github/forks/Lin-jun-xiang/chatgpt-line-bot?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/Lin-jun-xiang/chatgpt-line-bot/issues">
          <img alt="Issues" src="https://img.shields.io/github/issues/Lin-jun-xiang/chatgpt-line-bot?style=flat-square&labelColor=343b41" />
        </a>
      </td>
      <td>
        <a href="https://github.com/Lin-jun-xiang/chatgpt-line-bot/pulls">
          <img alt="Pull Requests" src="https://img.shields.io/github/