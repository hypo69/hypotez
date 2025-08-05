**Instructions for Generating Audio with gpt4free**

=========================================================================================

**Description**
-------------------------
This code snippet demonstrates how to use the `gpt4free` library to generate and transcribe audio using PollinationsAI and Microsoft Phi-4 models. It utilizes the `AsyncClient` for asynchronous communication, enabling efficient handling of audio tasks.

**Execution Steps**
-------------------------
1. **Initialize AsyncClient:** Create an instance of `AsyncClient` specifying the `PollinationsAI` provider.
2. **Generate Audio:**
    - Utilize the `chat.completions.create` method to generate audio using the `openai-audio` model.
    - Provide the desired audio settings like voice ("alloy") and format ("mp3").
    - Save the generated audio file as "alloy.mp3".
3. **Transcribe Audio:**
    - Open an audio file ("audio.wav") in binary read mode (`rb`).
    - Use `chat.completions.create` to transcribe the audio using the `Microsoft_Phi_4` provider.
    - Specify the audio file in the `media` parameter and set `modalities` to "text".
    - Print the transcribed text from the response.

**Usage Example**
-------------------------

```python
import asyncio
from g4f.client import AsyncClient
import g4f.Provider
import g4f.models

async def main():
    client = AsyncClient(provider=g4f.Provider.PollinationsAI)

    # Generate audio with PollinationsAI
    response = await client.chat.completions.create(
        model="openai-audio",
        messages=[{"role": "user", "content": "Say good day to the world"}],
        audio={ "voice": "alloy", "format": "mp3" },
    )
    response.choices[0].message.save("alloy.mp3")

    # Transcribe a audio file
    with open("audio.wav", "rb") as audio_file:
        response = await client.chat.completions.create(
            messages="Transcribe this audio",
            provider=g4f.Provider.Microsoft_Phi_4,
            media=[[audio_file, "audio.wav"]],
            modalities=["text"],
        )
        print(response.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main())
```