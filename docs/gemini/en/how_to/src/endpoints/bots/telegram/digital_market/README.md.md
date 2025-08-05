**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

## Digital Market Hook Bot - A Telegram Bot for an Online Store

**Digital Market Hook** is an educational project demonstrating a Telegram bot for a digital online store, built with modern Python technologies. The bot utilizes webhooks for seamless integration with three payment systems: YooKassa, Telegram-Stars, and Robocassa.  The project includes an admin panel, user profiles, and a product catalog categorized for efficient navigation.

## Project Overview

### Features

- **Telegram-based:** The bot operates within the Telegram messaging app, enabling easy interaction with users.
- **Webhooks:**  Leverages webhooks to enhance speed and efficiency for bot operations and Robocassa payment processing.
- **Multiple Payment Options:** Supports three payment methods:
    - **YooKassa:** Integrated via BotFather for streamlined payment processing.
    - **Telegram-Stars:**  Offers a dedicated integration for seamless payment transactions.
    - **Robocassa:**  Direct integration through webhooks, bypassing BotFather for efficient handling.
- **User Profiles:** Allows users to create and maintain profiles for personalized experiences within the store.
- **Product Catalog:** Offers a comprehensive product catalog with categorized listings for ease of browsing.
- **Admin Panel:** Provides a dedicated interface for managing the store, including product listings, orders, and user data.

### Technologies

- **aiogram 3.15.0:**  Asynchronous framework for building Telegram bots, ensuring smooth performance.
- **aiosqlite 0.20.0:**  Asynchronous driver for SQLite database management, optimizing database interactions.
- **loguru 0.7.2:**  Sophisticated logging library for detailed and organized tracking of bot activities.
- **pydantic-settings 2.7.0:**  Simplifies configuration management using Pydantic for clean and efficient settings handling.
- **SQLAlchemy 2.0.35:**  Versatile SQL library and Object-Relational Mapper (ORM) for Python, enabling database interaction.
- **pydantic >=2.4.1,<2.10:**  Data validation and configuration management library for ensuring data integrity.
- **alembic 1.14.0:**  Database migration tool for managing changes in the database schema without disrupting data.
- **aiohttp 3.10.11:**  Web server framework for handling webhooks within the bot, enabling seamless integration.

## Setting Up the Project

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Yakvenalex/DigitalMarketHookBot.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd DigitalMarketHookBot
   ```

3. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\\Scripts\\activate
   ```

4. **Obtain a Bot Token:** 
    - Use [@BotFather](https://t.me/BotFather) to generate a token for your Telegram bot.

5. **Get a YooKassa Payment Token:**
    - Utilize [@BotFather](https://t.me/BotFather) to obtain a YooKassa payment token (a test token will suffice).

6. **Register with YooKassa and Robocassa:** 
    - Create accounts with YooKassa and Robocassa, setting up online stores for payment processing.

7. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

8. **Create a `.env` File:**
   - Place a `.env` file in the project's root directory with the following environment variables:

   ```
   BOT_TOKEN=YOUR_BOT_TOKEN
   ADMIN_IDS=[ADMIN_TG1, ADMIN_TG2, ADMIN_TG3]
   PROVIDER_TOKEN=YOUR_YOO_KASSA_TOKEN
   SITE_URL=YOUR_WEBHOOK_SITE
   SITE_HOST=0.0.0.0
   SITE_PORT=8000
   MRH_LOGIN=YOUR_ROBOCASSA_LOGIN
   MRH_PASS_1=YOUR_ROBOCASSA_PASSWORD_1
   MRH_PASS_2=YOUR_ROBOCASSA_PASSWORD_2
   IN_TEST=1/0
   ```
   - The `IN_TEST` parameter set to `1` indicates that the ROBOCASSA payment should be in test mode. `0` enables production mode.

9. **Set Up a Tunnel for Webhooks:**
    - Use **Ngrok** to establish a secure tunnel between your local machine and the internet.
       - Download Ngrok from the [official website](https://ngrok.com/download).
       - Run Ngrok, specifying your server's local port (e.g., 8000):

         ```bash
         ngrok http 8000
         ```

       - Ngrok will provide a temporary public URL, which you can use for `SITE_URL`.

10. **Run the Bot:**

    ```bash
    python -m bot.main
    ```

## Using the Bot

Once the bot is running, you can interact with it on Telegram. The bot provides the functionality of a digital online store, with test payment options through YooKassa, Robocassa, and Telegram Stars. Telegram Stars payments have automated star refunds implemented immediately after payment completion.

### Testing Payment Data

- **Card:** 1111 1111 1111 1026
- **Expiration Date:** 12/26
- **CVC Code:** 000

## Author

**Alex Yakvenko** [Telegram](https://t.me/yakvenalexx) - Developer of this educational project.

## License

This project is licensed under the MIT License.

## Demonstration

To showcase the project's capabilities, I've prepared visual examples of its functionality:

### 1. Full Functionality Demonstration

Watch the **[project demo video](https://rutube.ru/video/f57c1617bd03368611ee8aeb44ccb2e5/)**, which highlights the bot's key features. You'll see the entire workflow from user interaction to successful payments through Robocassa.

### 2. Additional Payments

The second **[video](https://rutube.ru/video/bbf601d7f0dab962ba24cb57df706640/)** demonstrates handling additional payments. This video highlights the bot's response to various payment scenarios.

### 3. Try It Yourself!

To experience the bot firsthand, you can use the **[live bot](https://t.me/DigitalMarketAiogramHookBot)**. Interact with the bot, test its features, including payments, and see how user-friendly it is.

## Further Exploration

For a deeper dive into the code and project architecture, explore the source code and comments in the repository.

> **Note:** This project is designed for educational purposes and is not intended for use in real commercial projects without proper adaptation and testing.