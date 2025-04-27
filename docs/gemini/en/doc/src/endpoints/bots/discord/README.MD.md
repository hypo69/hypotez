# Discord Bot for Hypotez

## Overview

This document provides a detailed description of the Discord bot implemented in the `src/endpoints/bots/discord` directory of the `hypotez` project. The bot utilizes the `discord.py` library and integrates various functionalities related to machine learning model management, audio processing, and user interaction within the Discord platform. 

## Table of Contents

- [Main Functions and Commands](#main-functions-and-commands)
- [Main Modules and Libraries](#main-modules-and-libraries)
- [Running the Bot](#running-the-bot)
- [Conclusion](#conclusion)

## Main Functions and Commands

### Bot Initialization

- The bot is initialized with the command prefix `!` and incorporates essential intents (permissions to access specific Discord events). This ensures proper bot functionality and access to necessary data from the Discord server. 

### Commands

The bot supports a range of commands for user interaction:

- `!hi`: Sends a welcoming message to the user.
- `!join`: Connects the bot to the user's current voice channel, enabling audio interaction.
- `!leave`: Disconnects the bot from the voice channel.
- `!train`: Initiates the training process for the machine learning model. Users can provide training data in the form of a file or text input. 
- `!test`: Evaluates the performance of the trained model using provided test data.
- `!archive`: Archives files located in a specified directory.
- `!select_dataset`: Allows users to choose a particular dataset for model training.
- `!instruction`: Retrieves and sends instructions from an external file to users.
- `!correct`: Enables users to correct a previously generated bot message.
- `!feedback`: Facilitates user feedback on the bot's performance.
- `!getfile`: Sends a requested file from a designated path.

### Message Handling

- The bot processes all incoming messages, excluding its own messages. 
- If a user uploads an audio file, the bot utilizes speech recognition to transcribe the audio into text.
- When a user is in a voice channel, the bot converts text to speech and plays the synthesized audio in the voice channel.

### Speech Recognition

- The `recognizer` function downloads an audio file, converts it to WAV format, and performs speech recognition using Google Speech Recognition. 

### Text to Speech

- The `text_to_speech_and_play` function converts text into speech using the `gTTS` library and plays the resulting audio in the active voice channel.

### Logging

- The `logger` module is employed for logging events and errors that occur during bot operation, aiding in debugging and understanding bot behavior.

## Main Modules and Libraries

The bot utilizes several key modules and libraries:

- `discord.py`: The core library for building Discord bots.
- `speech_recognition`: Enables speech recognition functionality.
- `pydub`: Facilitates audio file conversion between formats.
- `gtts`: Performs text-to-speech conversion.
- `requests`: Used for downloading files.
- `pathlib`: Provides tools for working with file paths.
- `tempfile`: Creates temporary files for processing data.
- `asyncio`: Enables asynchronous task execution, improving responsiveness.

## Running the Bot

- The bot is launched using a token stored in the `gs.credentials.discord.bot_token` variable. This token is a unique identifier required for the bot to connect to Discord.

## Conclusion

The Discord bot implemented in this directory aims to enhance interactive user experience on Discord, featuring voice command handling, training and testing a machine learning model, providing instructions, and gathering user feedback. This comprehensive approach leverages the bot as a valuable tool for various tasks within the Discord environment.