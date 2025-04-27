# Beeper Module

## Overview

This module implements a `Beeper` class that provides audio notifications based on different event levels. It uses the `winsound` library to play beeps of varying frequencies and durations, allowing for different sounds to indicate various events like success, information, warning, error, and critical alerts.

## Details

The module utilizes a predefined dictionary `note_freq` that maps note names to corresponding frequencies. These frequencies are used to generate different beeps. The `BeepLevel` Enum class defines different event levels with associated melodies (lists of notes and durations) for each level.

The `BeepHandler` class provides a method to play sounds based on the log record's level. It uses the `BeepLevel` Enum to determine the appropriate melody to play for each level. 

The `Beeper` class provides a static method `beep` which allows for customizable audio notifications based on the provided event level, frequency, and duration. It also incorporates a `silent_mode` decorator that enables the user to mute all sound notifications.

## Classes

### `BeepLevel`

**Description**:  Enum class defining different event levels with associated melodies.

**Attributes**:

- `SUCCESS`: Melody for successful events.
- `INFO`: Melody for informational events.
- `ATTENTION`: Melody for attention-grabbing events.
- `WARNING`: Melody for warnings.
- `DEBUG`: Melody for debugging messages.
- `ERROR`: Melody for errors.
- `LONG_ERROR`: Melody for long error messages.
- `CRITICAL`: Melody for critical errors.
- `BELL`: Melody for a general alert sound.

### `BeepHandler`

**Description**: Class for handling audio notifications based on log record level.

**Attributes**:

- None.

**Methods**:

- `emit(self, record)`: Plays a sound based on the log record's level.

### `Beeper`

**Description**: Class for managing and generating audio notifications.

**Attributes**:

- `silent`: Boolean flag to enable/disable silent mode.

**Methods**:

- `beep(level: BeepLevel | str = BeepLevel.INFO, frequency: int = 400, duration: int = 1000) -> None`: Plays a beep based on the given level, frequency, and duration.

## Functions

### `silent_mode(func)`

**Purpose**: Decorator function to manage silent mode.

**Parameters**:

- `func`: Function to be decorated.

**Returns**:

- Wrapped function, including silent mode check.

**Raises Exceptions**:

- None.

**Inner Functions**:

- `wrapper(*args, **kwargs)`: Internal wrapper function to check silent mode before executing the function.

**How the Function Works**:

The `silent_mode` decorator is used to wrap functions that generate audio notifications. When the `silent` attribute of the `Beeper` class is set to `True`, the `wrapper` function checks this attribute and if it's `True`, prints a message indicating that silent mode is active and skips the execution of the decorated function. Otherwise, it executes the decorated function with the provided arguments.

**Examples**:

```python
@silent_mode
def my_function():
    # ... some code ...
```

## Parameter Details

- `level (BeepLevel | str)`: Specifies the event level. It can be a `BeepLevel` Enum value or a string representation of the level: `'success'`, `'info'`, `'attention'`, `'warning'`, `'debug'`, `'error'`, `'long_error'`, `'critical'`, or `'bell'`.
- `frequency (int)`: The frequency of the beep in Hz, ranging from 37 to 32000.
- `duration (int)`: The duration of the beep in milliseconds.
- `record (dict)`: Log record containing information about the event, including the event level.

## Examples

```python
from src.logger.beeper import Beeper, BeepLevel

# Play a beep for success
Beeper.beep(BeepLevel.SUCCESS)

# Play a beep for warning
Beeper.beep('warning', frequency=500, duration=300)

# Play a beep for error
Beeper.beep('error')

# Enable silent mode
Beeper.silent = True

# Play a beep (will be skipped because silent mode is enabled)
Beeper.beep('info')
```

## Conclusion

The `beeper` module offers a convenient way to provide audio feedback in applications. It allows developers to customize beeps based on different event levels, frequencies, and durations, making it easy to incorporate audio alerts into a project. The silent mode feature provides an option to mute all sound notifications when necessary.