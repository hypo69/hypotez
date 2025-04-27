# Movie Telegram Bot

## Overview

This module contains the core logic for a Telegram bot that helps users find links to watch movies and TV shows for free. The bot leverages the Aiogram library for Telegram bot development, Google services for associative search, the Kinopoisk library, and the [w2.kpfr/wiki](https://w2.kpfr.wiki/) service.

## Details

The bot is designed to provide a user-friendly interface for searching for movie and TV show links. It features:

- **Associative Search**: Uses Google services to find relevant results based on user queries.
- **Kinopoisk Integration**: Leverages the Kinopoisk library for movie and TV show data.
- **w2.kpfr/wiki Service**:  Utilizes the [w2.kpfr/wiki](https://w2.kpfr.wiki/) service for additional information and links.
- **Anti-Flooding Protection**: Implements middlewares to prevent excessive bot usage.
- **BeautifulSoup Parsing**: Uses BeautifulSoup for HTML parsing to extract relevant data.

## Quick Start

1. **Clone the Project**: Clone the project repository to your computer.
2. **Create .env File**: Create a file named `.env` in the project root and add the following line:
   ```
   TOKEN=123456789 # Replace with your Telegram bot token 
   ```
3. **Create and Activate a Virtual Environment**: If you don't have a virtual environment, create and activate one:
   ```shell
   python -m venv venv
   ```
   ```shell
   venv\Scripts\activate.bat
   ```
4. **Upgrade pip and Install Dependencies**: Update pip and install the required dependencies:
   ```shell
   pip install --upgrade pip
   ```
   ```shell
   pip install -r requirements.txt
   ```
5. **Run the Bot**: Start the bot by running `run.py`:
   ```shell
   python run.py
   ```

## Bot Links

- **Bot Link**: https://t.me/Guarava_bot
- **Contact**: https://t.me/qdi2k