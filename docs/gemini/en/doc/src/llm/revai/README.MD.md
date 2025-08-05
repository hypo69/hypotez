# Revai API Integration 

## Overview

This module provides a concise overview of how to integrate Revai API, a powerful tool for audio transcription and analysis, into your project. 

## Details 

Revai API is a comprehensive service for processing audio recordings, including transcription, translation, and speaker identification. This module outlines the core functionalities and resources needed to utilize Revai in your application.

### Core Features:

* **Transcription:** Convert audio files into text with high accuracy.
* **Translation:** Translate transcribed text into various languages.
* **Speaker Identification:** Identify and distinguish individual speakers in audio recordings.
* **Customization:** Customize transcription and translation settings for your specific needs.

### Integration Guide: 

The module utilizes the official Revai Python SDK, providing a simplified interface to interact with the API. You can leverage the SDK to:

1. **Authentication:** Securely access the Revai API with your API credentials.
2. **Job Creation:** Submit audio files to the API for transcription or translation.
3. **Job Management:** Monitor the progress of jobs and access results.
4. **Result Retrieval:** Retrieve transcribed text, translations, or speaker information from completed jobs.

## Example:

```python
# Importing necessary libraries
from src.llm.revai import RevaiClient

# Initialize RevaiClient with API credentials
client = RevaiClient(api_key='YOUR_API_KEY')

# Example: Transcribing an audio file
job = client.submit_job(audio_file='path/to/audio.mp3')
print(f'Job ID: {job.id}')

# Example: Retrieving transcription results
result = client.get_job_result(job_id=job.id)
print(f'Transcription: {result.transcription}')

# Example: Using speaker identification
speakers = client.get_speakers(job_id=job.id)
for speaker in speakers:
    print(f'Speaker ID: {speaker.id}')
    print(f'Speaker Name: {speaker.name}')
    print(f'Speaker Transcript: {speaker.transcript}')
```

## Documentation 

### `RevaiClient` Class

**Description**:  A class that provides an interface for interacting with the Revai API.

**Attributes**:

* **api_key (str):** Your Revai API key.
* **base_url (str):** The base URL for the Revai API.

**Methods**:

* **submit_job(audio_file: str, config: dict = None) -> Job:** Submits an audio file for processing.
* **get_job_result(job_id: str) -> JobResult:** Retrieves results for a completed job.
* **get_speakers(job_id: str) -> List[Speaker]:** Retrieves speaker information for a completed job.

### `Job` Class

**Description**:  Represents a job submitted to the Revai API.

**Attributes**:

* **id (str):** The unique ID for the job.
* **status (str):** The current status of the job (e.g., 'in_progress', 'completed', 'failed').

### `JobResult` Class

**Description**:  Contains the results of a completed job.

**Attributes**:

* **transcription (str):** The transcribed text.
* **translation (str):** The translated text, if translation was requested.
* **speakers (List[Speaker]):** A list of speakers identified in the audio.

### `Speaker` Class

**Description**:  Represents a speaker identified in an audio recording.

**Attributes**:

* **id (str):** The unique ID for the speaker.
* **name (str):** The name of the speaker, if identified.
* **transcript (str):** The transcript for the speaker.

## Using Revai in Hypotez:

The Revai API integration is designed to work seamlessly within the Hypotez project. You can leverage its capabilities to:

* **Analyze audio recordings:** Transcribe meeting recordings, interviews, or any other audio content.
* **Enhance data analysis:** Extract insights from spoken language for data analysis and decision-making.
* **Improve user experience:** Provide automated transcription and translation services within your applications.

By integrating the Revai API, you can unlock the potential of audio data, adding a new dimension to your project's capabilities.