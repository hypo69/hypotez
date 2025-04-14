### Анализ кода модуля `README.md`

**Качество кода:**

- **Соответствие стандартам**: 8/10
- **Плюсы**:
    - Хорошая структурированность и организация контента.
    - Наличие подробных инструкций по установке и использованию.
    - Использование Markdown для оформления, что обеспечивает читаемость.
    - Акцент на важность соблюдения лицензионных соглашений.
- **Минусы**:
    - Отсутствие информации о структуре и связях внутри проекта.
    - Не все разделы документации имеют одинаковый уровень детализации.
    - Некоторые формулировки могут быть улучшены для большей ясности.

**Рекомендации по улучшению:**

1.  **Добавить информацию о структуре проекта**:

    *   Включить раздел с описанием основных модулей и их взаимодействием.
    *   Добавить диаграммы или блок-схемы для визуализации архитектуры проекта.
2.  **Улучшить единообразие в детализации разделов**:

    *   Пересмотреть и дополнить разделы, содержащие меньше информации, чтобы обеспечить одинаковый уровень детализации во всей документации.
    *   Добавить примеры кода и сценарии использования для каждого раздела.
3.  **Пересмотреть формулировки**:

    *   Использовать более конкретные термины, чтобы избежать двусмысленности.
    *   Убедиться, что все инструкции понятны для пользователей с разным уровнем подготовки.
4.  **Добавить примеры использования API**:

    *   Включить больше примеров кода, демонстрирующих, как использовать API для различных задач.
    *   Добавить примеры запросов и ответов для облегчения интеграции.
5.  **Локализация документации**:

    *   Перевести документацию на другие языки, чтобы расширить аудиторию пользователей.
    *   Обеспечить поддержку нескольких языков для комментариев и docstring в коде.

**Оптимизированный код:**

```markdown
<a href="https://trendshift.io/repositories/1692" target="_blank"><img src="https://trendshift.io/api/badge/repositories/1692" alt="xtekky%2Fgpt4free | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

---

<p align="center">
  <span style="background: linear-gradient(45deg, #12c2e9, #c471ed, #f64f59); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
    <strong>Written by <a href="https://github.com/xtekky">@xtekky</a></strong>
  </span>
</p>

<div id="top"></div>

> [!IMPORTANT]
> By using this repository or any code related to it, you agree to the [legal notice](LEGAL_NOTICE.md). The author is **not responsible for the usage of this repository nor endorses it**, nor is the author responsible for any copies, forks, re-uploads made by other users, or anything else related to GPT4Free. This is the author's only account and repository. To prevent impersonation or irresponsible actions, please comply with the GNU GPL license this Repository uses.

> [!WARNING]
> _"gpt4free"_ serves as a **PoC** (proof of concept), demonstrating the development of an API package with multi-provider requests, with features like timeouts, load balance and flow control.

> [!NOTE]
> <sup>**Latest version:**</sup><br> [![PyPI version](https://img.shields.io/pypi/v/g4f?color=blue)](https://pypi.org/project/g4f) [![Docker version](https://img.shields.io/docker/v/hlohaus789/g4f?label=docker&color=blue)](https://hub.docker.com/r/hlohaus789/g4f)  
> <sup>**Stats:**</sup><br> [![Downloads](https://static.pepy.tech/badge/g4f)](https://pepy.tech/project/g4f) [![Downloads](https://static.pepy.tech/badge/g4f/month)](https://pepy.tech/project/g4f)

```sh
pip install -U g4f[all]
```

```sh
docker pull hlohaus789/g4f
```

## 🆕 Что нового

![1000032415](https://github.com/user-attachments/assets/4caab977-eb05-48ed-b750-3ad082bcfcae)

-   **Explore the latest features and updates**  
    Find comprehensive details on our [Releases Page](https://github.com/xtekky/gpt4free/releases).

-   **Stay updated with our Telegram Channel** 📨  
    Join us at [telegram.me/g4f_channel](https://telegram.me/g4f_channel).

-   **Subscribe to our Discord News Channel** 💬🆕️  
    Stay informed about updates via our [News Channel: discord.gg/5E39JUWUFa](https://discord.gg/5E39JUWUFa).

-   **Get support in our Discord Community** 🤝💻  
    Reach out for help in our [Support Group: discord.gg/qXA4Wf4Fsm](https://discord.gg/qXA4Wf4Fsm).

## 🔻 Site Takedown

Is your site on this repository and you want to take it down? Send an email to takedown@g4f.ai with proof it is yours and it will be removed as fast as possible. To prevent reproduction please secure your API. 😉

## 🚀 GPT4Free on HuggingFace

[![HuggingSpace](https://github.com/user-attachments/assets/1d859e8a-d6fa-416f-a213-ccc26aa11e90)](https://huggingface.co/spaces/roxky/g4f-new)
**Is a proof-of-concept API package for multi-provider AI requests. It showcases features such as:**

-   Load balancing and request flow control.
-   Seamless integration with multiple AI providers.
-   Comprehensive text and image generation support.

> Explore the [Visit GPT4Free on HuggingFace Space](https://huggingface.co/spaces/roxky/g4f-new) for a hosted version or [Duplicate GPT4Free Space](https://huggingface.co/spaces/roxky/g4f-new?duplicate=true) it for personal use.

---

## 📚 Table of Contents

-   [🆕 What's New](#-whats-new)
-   [📚 Table of Contents](#-table-of-contents)
-   [⚡ Getting Started](#-getting-started)
    -   [🛠 Installation](#-installation)
        -   [🐳 Using Docker](#-using-docker)
        -   [🪟 Windows Guide (.exe)](#-windows-guide-exe)
        -   [🐍 Python Installation](#-python-installation)
-   [💡 Usage](#-usage)
    -   [📝 Text Generation](#-text-generation)
    -   [🎨 Image Generation](#-image-generation)
    -   [🌐 Web Interface](#-web-interface)
    -   [🖥️ Local Inference](docs/local.md)
    -   [🤖 Interference API](#-interference-api)
    -   [🛠️ Configuration](docs/configuration.md)
    -   [📱 Run on Smartphone](#-run-on-smartphone)
    -   [📘 Full Documentation for Python API](#-full-documentation-for-python-api)
-   [🚀 Providers and Models](docs/providers-and-models.md)
-   [🔗 Powered by gpt4free](#-powered-by-gpt4free)
-   [🤝 Contribute](#-contribute)
    -   [How do i create a new Provider?](#guide-how-do-i-create-a-new-provider)
    -   [How can AI help me with writing code?](#guide-how-can-ai-help-me-with-writing-code)
-   [🙌 Contributors](#-contributors)
-   [©️ Copyright](#-copyright)
-   [⭐ Star History](#-star-history)
-   [📄 License](#-license)

---

## ⚡️ Getting Started

## 🛠 Installation

### 🐳 Using Docker

1.  **Install Docker:** [Download and install Docker](https://docs.docker.com/get-docker/).
2.  **Set Up Directories:** Before running the container, make sure the necessary data directories exist or can be created. For example, you can create and set ownership on these directories by running:

```bash
mkdir -p ${PWD}/har_and_cookies ${PWD}/generated_images
sudo chown -R 1200:1201 ${PWD}/har_and_cookies ${PWD}/generated_images
```

1.  **Run the Docker Container:** Use the following commands to pull the latest image and start the container (Only x64):

```bash
docker pull hlohaus789/g4f
docker run -p 8080:8080 -p 7900:7900 \
  --shm-size="2g" \
  -v ${PWD}/har_and_cookies:/app/har_and_cookies \
  -v ${PWD}/generated_images:/app/generated_images \
  hlohaus789/g4f:latest
```

1.  **Running the Slim Docker Image:** And use the following commands to run the Slim Docker image. This command also updates the `g4f` package at startup and installs any additional dependencies: (x64 and arm64)

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

1.  **Access the Client Interface:**

    *   **To use the included client, navigate to:** [http://localhost:8080/chat/](http://localhost:8080/chat/)
    *   **Or set the API base for your client to:** [http://localhost:8080/v1](http://localhost:8080/v1)

2.  **(Optional) Provider Login:**  
    If required, you can access the container's desktop here: http://localhost:7900/?autoconnect=1&resize=scale&password=secret for provider login purposes.

---

### 🪟 Windows Guide (.exe)

To ensure the seamless operation of our application, please follow the instructions below. These steps are designed to guide you through the installation process on Windows operating systems.

**Installation Steps:**

1.  **Download the Application**: Visit our [releases page](https://github.com/xtekky/gpt4free/releases/tag/0.4.2.0) and download the most recent version of the application, named `g4f.exe.zip`.
2.  **File Placement**: After downloading, locate the `.zip` file in your Downloads folder. Unpack it to a directory of your choice on your system, then execute the `g4f.exe` file to run the app.
3.  **Open GUI**: The app starts a web server with the GUI. Open your favorite browser and navigate to [http://localhost:8080/chat/](http://localhost:8080/chat/) to access the application interface.
4.  **Firewall Configuration (Hotfix)**: Upon installation, it may be necessary to adjust your Windows Firewall settings to allow the application to operate correctly. To do this, access your Windows Firewall settings and allow the application.

By following these steps, you should be able to successfully install and run the application on your Windows system. If you encounter any issues during the installation process, please refer to our Issue Tracker or try to get contact over Discord for assistance.

---

### 🐍 Python Installation

#### Prerequisites:

1.  Install Python 3.10+ from [python.org](https://www.python.org/downloads/).
2.  Install Google Chrome for certain providers.

#### Install with PyPI:

```bash
pip install -U g4f[all]
```

> How do I install only parts or do disable parts? **Use partial requirements:** [/docs/requirements](docs/requirements.md)

#### Install from Source:

```bash
git clone https://github.com/xtekky/gpt4free.git
cd gpt4free
pip install -r requirements.txt
```

> How do I load the project using git and installing the project requirements? **Read this tutorial and follow it step by step:** [/docs/git](docs/git.md)

---

## 💡 Usage

### 📝 Text Generation

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

### 🎨 Image Generation

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

### 🌐 Web Interface

**Run the GUI using Python:**

```python
from g4f.gui import run_gui

run_gui()
```

**Run via CLI (To start the Flask Server):**

```bash
python -m g4f.cli gui --port 8080 --debug
```

**Or, start the FastAPI Server:**

```bash
python -m g4f --port 8080 --debug
```

> **Learn More About the GUI:** For detailed instructions on how to set up, configure, and use the GPT4Free GUI, refer to the [GUI Documentation](docs/gui.md) . This guide includes step-by-step details on provider selection, managing conversations, using advanced features like speech recognition, and more.

---

### 🤖 Interference API

The **Interference API** enables seamless integration with OpenAI's services through G4F, allowing you to deploy efficient AI solutions.

-   **Documentation**: [Interference API Docs](docs/interference-api.md)
-   **Endpoint**: `http://localhost:1337/v1`
-   **Swagger UI**: Explore the OpenAPI documentation via Swagger UI at `http://localhost:1337/docs`
-   **Provider Selection**: [How to Specify a Provider?](docs/selecting_a_provider.md)

This API is designed for straightforward implementation and enhanced compatibility with other OpenAI integrations.

---

### 📱 Run on Smartphone

Run the Web UI on your smartphone for easy access on the go. Check out the dedicated guide to learn how to set up and use the GUI on your mobile device: [Run on Smartphone Guide](docs/guides/phone.md)

---

#### **📘 Full Documentation for Python API**

-   **Client API from G4F:** [/docs/client](docs/client.md)
-   **AsyncClient API from G4F:** [/docs/async_client](docs/async_client.md)
-   **Requests API from G4F:** [/docs/requests](docs/requests.md)
-   **File API from G4F:** [/docs/file](docs/file.md)
-   **PydanticAI and LangChain Integration for G4F:** [/docs/pydantic_ai](docs/pydantic_ai.md)
-   **Legacy API with python modules:** [/docs/legacy](docs/legacy.md)
-   **G4F - Media Documentation** [/docs/media](/docs/media.md) *(New)*

---

## 🔗 Powered by gpt4free

<table>
  <thead align="center">
    <tr border: none;>
      <td>
        <b>🎁 Projects</b>
      </td>
      <td>
        <b>⭐ Stars</b>
      </td>
      <td>
        <b>📚 Forks</b>
      </td>
      <td>
        <b>🛎 Issues</b>
      </td>
      <td>
        <b>📬 Pull requests</b>
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
          <b>Free AI API's & Potential Providers List</b>
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
          <img alt="Issues" src="https://img.shields.io/github/issues/Lin-jun