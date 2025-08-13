# # \file /src/logger/beeper.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. module:: src.logger 
	:platform: Windows, Unix
	:synopsis: Бииип"""



import asyncio
import winsound, time
from enum import Enum
from typing import Union

# Notes and frequencies
note_freq = {
    'C3': 130.81, 'C# 3 ': 138.59,' d3 ': 146.83,' D#3 ': 155.56,' e3 ': 164.81,' f3 ': 174.61,
    'F# 3 ': 185.00,' G3 ': 196.00,' G#3 ': 207.65,' A3 ': 220.00,' A#3 ': 233.08,' B3 ': 246.94,

    'C4': 261.63, 'C# 4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63, 'F4': 349.23,
    'F# 4 ': 369.99,' G4 ': 392.00,' G#4 ': 415.30,' A4 ': 440.00,' A#4 ': 466.16,' B4 ': 493.88,

    'C5': 523.25, 'C# 5': 554.37, 'D5': 587.33, 'D#5': 622.25, 'E5': 659.26, 'F5': 698.46,
    'F# 5': 739.99, 'G5': 783.99, 'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77,

    'C6': 1046.50, 'C# 6': 1108.73, 'D6': 1174.66, 'D#6': 1244.51, 'E6': 1318.51, 'F6': 1396.91,
    'F# 6 ': 1479.98,' G6 ': 1567.98,' G#6 ': 1661.22,' A6 ': 1760.00,' A#6 ': 1864.66,' B6 ': 1975.53,

    'C7': 2093.00, 'C# 7 ': 2217.46,' D7 ': 2349.32,' D 7 ': 2489.02,' e7 ': 2637.02,' f7 ': 2793.83,
    'F# 7 ': 2959.96,' G7 ': 3135.96,' G#7 ': 3322.44,' A7 ': 3520.00,' A#7 ': 3729.31,' B7 ': 3951.07,
}
... 
class BeepLevel(Enum):
    """Class Transportant types of events
    @details to different events correspond to different melodies
    The levels of events
    - Success
    - Info
    - Attenation
    - Warning
    - Debug
    - Error
    - Long_error
    - Critical
    - Bell"""
    SUCCESS = [('D5', 100), ('A5', 100), ('D6', 100)]
    # Info = [('C6', 150), ('E6', 150), ('G6', 150), ('C7', 150)],
    INFO_LONG = [('C6', 150), ('E6', 150)],
    INFO = [('C6', 8)],
    # ATTENTION = [('G5', 120), ('F5', 120), ('E5', 120), ('D5', 120), ('C5', 120)],
    ATTENTION = [ ('G5', 600) ],
    WARNING = [('F5', 100), ('G5', 100), ('A5', 100), ('F6', 100)],
    DEBUG = [('E6', 150), ('D4', 500)],
    # ERROR =[('G5', 40), ('C7', 100)],
    ERROR = [ ('C7', 1000) ],
    LONG_ERROR = [('C7', 50), ('C7', 250)],
    CRITICAL = [('G5', 40), ('C7', 100)],
    BELL = [('G6', 200), ('C7', 200), ('E7', 200)],
...    

class BeepHandler:
    def emit(self, record):
        try:
            level = record["level"].name
            if level == 'ERROR':
                self.play_sound(880, 500)  # Lose "BIP" for errors
            elif level == 'WARNING':
                self.play_sound(500, 300)  # Lose another sound for warning
            elif level == 'INFO':
                self.play_sound(300, 200)  # And so on...
            else:
                self.play_default_sound()  # Default sound for other levels of logging
        except Exception as ex:
            print(f'Ошибка воспроизведения звука: {ex}' )

    def beep(self, level: BeepLevel | str = BeepLevel.INFO, frequency: int = 400, duration: int = 1000):
        Beeper.beep(level, frequency, duration)

...

# None


def silent_mode(func):
    """Function-decorator to manage the mode of "silence".
    
    @details accepts one argument - a function that needs to be decorated.
    
    @param FUNC: Function for decoration.
    
    @return: A wrapped function that adds a check of the "Disorder" mode."""
    def wrapper(*args, **kwargs):
        """The internal feature of the unit to verify the "silence" mode before the function.
        
        @details If the "Silent" mode is included, displays a message about the passage of sound reproduction and completes the execution of the BEEP function.
        Otherwise, it causes an original function conveyed as an argument (FUNC (*args, ** kwargs)).
        
        @param Args: Positional arguments transferred to a wrapped function.
        @param kwargs: named arguments transferred to a wrapped function.
        
        @return: The result of the execution of the wrapped function or NONE if the "silence" mode is included."""
        if Beeper.silent:
            print("Silent mode is enabled. Skipping beep.")
            return
        return func(*args, **kwargs)
    return wrapper
...


class Beeper():
    """Sound signal class"""

    silent = False
    
    @staticmethod
    @silent_mode
    async def beep(level: BeepLevel | str = BeepLevel.INFO, frequency: int = 400, duration: int = 1000) -> None:
        """Sound notification signal 
        @details gives me the opportunity to determine what is happening in the system
        @param mode `beeplevel | Str`: Type of event: `info`,` Atting`, `Warning`,` Debug`, `Error`,` LONG_error`, `CRITICAL`,` BELLL`  
        /t /t or `beep.sucess`,` beep.info`, `beep.atting`,` beep.warning`, `beep.debug`,` bep.error`, `beep.long_error`,` beep.critical`,,, `beep.critical`,, `Beep.bell`
        @param frequency signal frequency in values from 37 to 32000
        @param duraation signal duration"""
        
        if isinstance(level, str):
            if level == 'success':
                melody = BeepLevel.SUCCESS.value[0]
            # ... other conditions ...
        elif isinstance(level, BeepLevel):
            melody = level.value[0]

        for note, duration in melody:
            frequency = note_freq[note]
            try:
                winsound.Beep(int(frequency), duration)
            except Exception as ex:
                print(f'''Not bibika: | 
                              Error - {ex}, 
                              note - {note},
                              Duration - {duration}
                                Melody - {melody}''')
                return
            time.sleep(0.0)
...


