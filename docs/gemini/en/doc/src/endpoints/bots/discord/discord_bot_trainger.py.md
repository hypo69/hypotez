# Discord Bot Trainer for Hypotez

## Overview

This module provides a Discord bot capable of training, testing, and interacting with a machine learning model for text processing. It utilizes the `discord.py` library to handle interaction with Discord servers and integrate with various APIs for model training and testing.

## Details

The Discord bot utilizes the `commands.Bot` class from `discord.ext` to handle command parsing and execution. It leverages a `Model` object, which is responsible for interacting with the machine learning model used for text processing. The bot responds to various commands, enabling users to:

- **Train the model:**  Train the model using provided data from a text file or attachment.
- **Test the model:** Test the model with specific data and retrieve predictions.
- **Select a dataset:** Select a dataset from a specific directory for training the model.
- **Archive files:** Archive files in a specified directory.
- **Correct previous responses:** Correct the bot's previous responses by providing the message ID and correction.
- **Provide feedback:** Submit feedback about the model's responses.
- **Retrieve files:** Attach files from the specified path.
- **Interact with the model:**  Send messages and receive responses from the trained model. 

## Classes

### `Model`

**Description**: This class represents the machine learning model responsible for text processing tasks. It handles model training, testing, and interaction with the user.

**Attributes**:

- `model_name` (str): The name of the machine learning model used for text processing (e.g., "GPT-3").
- `api_key` (str): The API key for accessing the model's services.
- `parameters` (dict): A dictionary containing parameters for the model (e.g., temperature, max_tokens).

**Methods**:

- `train(data: str, data_dir: str, positive: bool)`: Trains the model with provided data from a text file or directory.
- `predict(test_data: dict)`: Predicts outputs based on the given test data.
- `handle_errors(predictions: list, test_data: dict)`: Handles errors during model prediction and logs them for future analysis.
- `select_dataset_and_archive(path_to_dir_positive: str, positive: bool)`: Selects a dataset from a directory and archives it for future use.
- `archive_files(directory: str)`: Archives files in the specified directory.
- `save_job_id(job_id: str, job_status: str)`: Saves the job ID and status for tracking model training progress.
- `send_message(message: str)`: Sends a message to the model and receives a response. 

## Functions

### `store_correction(original_text: str, correction: str)`

**Purpose**: This function stores the correction for future reference or retraining.

**Parameters**:

- `original_text` (str): The original text of the message that was corrected.
- `correction` (str): The provided correction to the original text.

**Returns**:

- `None`

**Raises Exceptions**:

- `None`

**How the Function Works**:

- The function opens a file named "corrections_log.txt" in append mode.
- It writes the original text and the correction to the file, separated by a newline character.
- This allows storing corrections for potential future retraining of the model or analysis.

### `recognizer(audio_url: str, language: str = 'ru-RU') -> str` 

**Purpose**: This function downloads an audio file from a provided URL, recognizes speech in the audio using Google Speech Recognition, and returns the recognized text.

**Parameters**:

- `audio_url` (str): The URL of the audio file to download and recognize speech from.
- `language` (str): The language of the audio file. Defaults to "ru-RU" (Russian).

**Returns**:

- `str`: The recognized text from the audio file.

**Raises Exceptions**:

- `sr.UnknownValueError`: If Google Speech Recognition could not understand the audio.
- `sr.RequestError`: If there was an error requesting results from the Google Speech Recognition service.

**How the Function Works**:

1. **Download audio:** The function downloads the audio file from the provided URL and saves it to a temporary file.
2. **Convert to WAV:** If the downloaded file is not in WAV format, it is converted to WAV for compatibility with the Speech Recognition library.
3. **Speech recognition:** The function uses the SpeechRecognition library to recognize speech from the WAV file using Google Speech Recognition.
4. **Return recognized text:** The recognized text is returned as a string.

### `text_to_speech_and_play(text: str, channel: discord.VoiceChannel)`

**Purpose**: This function converts text to speech using Google Text-to-Speech (gTTS) and plays the audio in a Discord voice channel.

**Parameters**:

- `text` (str): The text to convert to speech.
- `channel` (discord.VoiceChannel): The Discord voice channel where the audio will be played.

**Returns**:

- `None`

**How the Function Works**:

1. **Text-to-speech:** The function uses the gTTS library to convert the input text into speech.
2. **Save audio:** The synthesized speech is saved as an MP3 file to a temporary location.
3. **Connect to voice channel:** If the bot is not already connected to the voice channel, it connects.
4. **Play audio:** The bot plays the MP3 audio file in the voice channel using `discord.FFmpegPCMAudio`.
5. **Wait for playback:** The function waits until the audio playback is complete.
6. **Disconnect:** The bot disconnects from the voice channel after playback.

## Examples

**Example 1: Training the model with a text file**

```python
!train data=data.txt  # Train the model with the data in 'data.txt'
```

**Example 2: Testing the model with specific data**

```python
!test test_data='{"text": "Hello, world!"}'
```

**Example 3: Selecting a dataset for training**

```python
!select_dataset path_to_dir_positive=dataset_dir positive=True
```

**Example 4: Submitting feedback**

```python
!feedback "The model's response was accurate and helpful."
```

**Example 5: Retrieving a file**

```python
!getfile file_path=my_file.txt
```

**Example 6: Sending a message to the model**

```python
!send_message "What is the capital of France?"
```