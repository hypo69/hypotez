## \file /src/bots/openai_bots/discord_bot_trainger (9).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.bots.openai_bots 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.bots.openai_bots """


import discord
from discord.ext import commands
import json
from pathlib import Path
import tempfile
import header
from src import gs
from src.llm.openai.model.training import Model
from src.utils.jjson import j_loads_ns, j_loads_ns, j_dumps
from src.logger.logger import logger
from src.utils.printer import pprint
import speech_recognition as sr  # Библиотека для распознавания речи
import requests  # Для скачивания файлов

# Command prefix for the bot
PREFIX = '!'

# Create bot object
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # Необходимо для работы с аудиопотоками
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Create model object
model = Model()

@bot.event
async def on_ready():
    """Called when the bot is ready."""
    logger.info(f'Logged in as {bot.user}')

@bot.command(name='hi')
async def hi(ctx):
    """Welcome message."""
    logger.info(f'hi({ctx})')
    await ctx.send('HI!')
    return True

@bot.command(name='train')
async def train(ctx, data: str = None, data_dir: str = None, positive: bool = True, attachment: discord.Attachment = None):
    """Train the model with the provided data."""
    logger.info(f'train({ctx})')
    if attachment:
        file_path = f"/tmp/{attachment.filename}"
        await attachment.save(file_path)
        data = file_path

    job_id = model.train(data, data_dir, positive)
    if job_id:
        await ctx.send(f'Model training started. Job ID: {job_id}')
        model.save_job_id(job_id, "Training task started")
    else:
        await ctx.send('Failed to start training.')

@bot.command(name='test')
async def test(ctx, test_data: str):
    """Test the model with the provided test data."""
    logger.info(f'test({ctx})')
    try:
        test_data = j_loads(test_data)
        predictions = model.predict(test_data)
        if predictions:
            await ctx.send(f'Test complete. Predictions: {predictions}')
            model.handle_errors(predictions, test_data)
        else:
            await ctx.send('Failed to get predictions.')
    except json.JSONDecodeError:
        await ctx.send('Invalid test data format. Please provide a valid JSON string.')

@bot.command(name='archive')
async def archive(ctx, directory: str):
    """Archive files in the specified directory."""
    logger.info(f'archive({ctx})')
    try:
        await model.archive_files(directory)
        await ctx.send(f'Files in {directory} have been archived.')
    except Exception as ex:
        await ctx.send(f'An error occurred while archiving files: {ex}')

@bot.command(name='select_dataset')
async def select_dataset(ctx, path_to_dir_positive: str, positive: bool = True):
    """Select a dataset for training the model."""
    logger.info(f'select_dataset({ctx})')
    dataset = await model.select_dataset_and_archive(path_to_dir_positive, positive)
    if dataset:
        await ctx.send(f'Dataset selected and archived. Dataset: {dataset}')
    else:
        await ctx.send('Failed to select dataset.')

@bot.command(name='instruction')
async def instruction(ctx):
    """Display the instruction message from an external file."""
    logger.info(f'instruction({ctx})')
    try:
        instructions_path = Path("_docs/bot_instruction.md")
        if instructions_path.exists():
            with instructions_path.open("r") as file:
                instructions = file.read()
            await ctx.send(instructions)
        else:
            await ctx.send('Instructions file not found.')
    except Exception as ex:
        await ctx.send(f'An error occurred while reading the instructions: {ex}')

@bot.command(name='correct')
async def correct(ctx, message_id: int, *, correction: str):
    """Correct a previous response by providing the message ID and the correction."""
    logger.info(f'correct({ctx})')
    try:
        message = await ctx.fetch_message(message_id)
        if message:
            # Log or store the correction
            logger.info(f"Correction for message ID {message_id}: {correction}")
            store_correction(message.content, correction)
            await ctx.send(f"Correction received: {correction}")
        else:
            await ctx.send("Message not found.")
    except Exception as ex:
        await ctx.send(f'An error occurred: {ex}')

def store_correction(original_text: str, correction: str):
    """Store the correction for future reference or retraining."""
    logger.info('store_correction()')
    correction_file = Path("corrections_log.txt")
    with correction_file.open("a") as file:
        file.write(f"Original: {original_text}\nCorrection: {correction}\n\n")

@bot.command(name='feedback')
async def feedback(ctx, *, feedback_text: str):
    """Submit feedback about the model's response."""
    logger.info(f'feedback({ctx})')
    store_correction("Feedback", feedback_text)
    await ctx.send('Thank you for your feedback. We will use it to improve the model.')

@bot.command(name='getfile')
async def getfile(ctx, file_path: str):
    """Attach a file from the given path."""
    logger.info(f'getfile({ctx})')
    file_to_attach = Path(file_path)
    if file_to_attach.exists():
        await ctx.send("Here is the file you requested:", file=discord.File(file_to_attach))
    else:
        await ctx.send(f'File not found: {file_path}')

@bot.command(name='a')
async def upload_audio(ctx, attachment: discord.Attachment):
    """Upload an audio file for processing."""
    logger.info(f'upload_audio({ctx})')
    if attachment:
        file_path = Path(tempfile.gettempdir()) / attachment.filename
        await attachment.save(file_path)  # Save audio file
        
        # Process audio and send to model
        response = model.process_audio(file_path)
        logger.info(f"Start processing audio")
        await ctx.send(response)

@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice state changes to recognize audio from voice channels."""
    logger.info(f'on_voice_state_update()')
    if after.channel is not None and member != bot.user:
        channel = after.channel
        voice_client = await channel.connect()

        # Start listening to voice
        try:
            recognizer = sr.Recognizer()
            # Assuming you have already set up a way to capture audio in a specified way
            # Need to be implemented for handling live audio streams
            audio_data = ...  # Placeholder for your audio capturing logic

            # Process recognized audio
            text = recognizer.recognize_google(audio_data)
            logger.info(f'Recognized text: {text}')
            
            # # Send recognized text to the model
            # response = model.send_message(text)
            await channel.send(text)

        except Exception as ex:
            logger.error(f'Error processing voice message: {ex}')
            ...
        finally:
            await voice_client.disconnect()  
            
def recognizer(audio_url: str) -> str:
    """Download an audio file and recognize speech in it."""
    # Download audio file
    response = requests.get(audio_url)
    #audio_file_path = Path(tempfile.gettempdir()) / "recognized_audio.ogg"
    audio_file_path = gs.path.tmp / 'discord' /'audio' / "recognized_audio.ogg"

    with open(audio_file_path, 'wb') as f:
        f.write(response.content)

    # Initialize recognizer
    recognizer = sr.Recognizer()
    with sr.AudioFile(str(audio_file_path)) as source:
        audio_data = recognizer.record(source)
        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio_data)
            logger.info(f'Recognized text: {text}')
            return text
        except sr.UnknownValueError:
            logger.error("Google Speech Recognition could not understand audio")
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
            return "Could not request results from the speech recognition service."


    
@bot.event
async def on_message(message):
    """Handle incoming messages and provide responses from the model."""
    logger.info(f'on_message({pprint(message)})')
       
        
    if message.author == bot.user:
        return
    
    if message.attachments:
        if message.attachments[0].content_type == 'audio/ogg':
            message = recognizer(message.attachments[0])
        
    # Process commands
    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.process_commands(message)
        return

    # Generate a response from the model
    response = model.send_message(message.content)

    # Send the response
    sent_message = await message.channel.send(response)

    # Store the message ID for potential corrections
    logger.info(f"Sent message ID: {sent_message.id}")

if __name__ == "__main__":
    logger.info('Bot is starting...')
    bot.run(gs.credentials.discord.bot_token)