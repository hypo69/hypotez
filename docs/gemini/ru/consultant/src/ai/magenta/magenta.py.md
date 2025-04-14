### **Анализ кода модуля `magenta.py`**

## Качество кода:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на логические блоки, каждый из которых выполняет определенную функцию.
    - Использование класса `MagentaMusic` позволяет инкапсулировать логику генерации музыки.
    - Наличие примера использования в `if __name__ == '__main__':` упрощает понимание работы кода.
- **Минусы**:
    - Отсутствуют аннотации типов для параметров функций и переменных класса.
    - Отсутствует документация в формате docstring для класса и его методов.
    - Используются магические числа (например, `16`, `8`) без объяснения их значения.
    - Не обрабатываются возможные исключения при работе с файлами.
    - Не используется модуль `logger` для логирования.
    - В коде используются двойные кавычки вместо одинарных.

## Рекомендации по улучшению:

1.  **Добавить docstring**: Необходимо добавить docstring для класса `MagentaMusic` и всех его методов, следуя указанному формату. Это улучшит читаемость и понимание кода.

2.  **Добавить аннотации типов**: Добавить аннотации типов для параметров функций и переменных класса.

3.  **Использовать константы**: Заменить магические числа константами с понятными именами.

4.  **Обработка исключений**: Добавить обработку исключений при работе с файлами, чтобы предотвратить аварийное завершение программы.

5.  **Логирование**: Использовать модуль `logger` для логирования информации о процессе генерации музыки, а также для записи ошибок.

6.  **Использовать одинарные кавычки**: Заменить двойные кавычки на одинарные в Python-коде.

7.  **Улучшить читаемость**: Улучшить читаемость кода, добавив пробелы вокруг операторов и привести код в соответствие со стандартами PEP8.

## Оптимизированный код:

```python
# -*- coding: utf-8 -*-
"""
Модуль для работы с Magenta Music
====================================

Модуль содержит класс :class:`MagentaMusic`, который используется для генерации музыки с использованием библиотеки Magenta.

Пример использования
----------------------

>>> music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn',
...                                temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)
>>> music_generator.generate_full_music()
"""

import os
from pathlib import Path
import magenta.music as mm
from magenta.models.melody_rnn import melody_rnn_sequence_generator
import tensorflow as tf  # Import TensorFlow

from src.logger import logger

class MagentaMusic:
    """
    Класс для генерации музыки с использованием библиотеки Magenta.
    """
    def __init__(self, output_dir: str = 'generated_music_advanced', model_name: str = 'attention_rnn', temperature: float = 1.2,
                 num_steps: int = 256, primer_midi_file: str = 'primer.mid', tempo: int = 100) -> None:
        """
        Инициализирует экземпляр класса MagentaMusic.

        Args:
            output_dir (str, optional): Директория для сохранения сгенерированной музыки. По умолчанию 'generated_music_advanced'.
            model_name (str, optional): Название модели для генерации мелодии. По умолчанию 'attention_rnn'.
            temperature (float, optional): Температура для генерации мелодии. По умолчанию 1.2.
            num_steps (int, optional): Количество шагов для генерации мелодии. По умолчанию 256.
            primer_midi_file (str, optional): Путь к MIDI-файлу затравки. По умолчанию 'primer.mid'.
            tempo (int, optional): Темп музыки. По умолчанию 100.
        """
        self.output_dir: str = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.model_name: str = model_name
        self.temperature: float = temperature
        self.num_steps: int = num_steps
        self.primer_midi_file: str = primer_midi_file
        self.tempo: int = tempo
        self.melody_rnn = melody_rnn_sequence_generator.MelodyRnnSequenceGenerator(
            model_name=self.model_name
        )
        self.primer_sequence = self._load_primer_sequence()

    def _load_primer_sequence(self) -> mm.NoteSequence:
        """
        Загружает MIDI-файл затравки или создаёт пустую NoteSequence, если файл не найден.

        Returns:
            mm.NoteSequence: Загруженная NoteSequence или пустая NoteSequence, если файл не найден.
        """
        try:
            if os.path.exists(self.primer_midi_file):
                primer_sequence = mm.midi_file_to_sequence_proto(self.primer_midi_file)
                logger.info(f"Используем primer из {self.primer_midi_file}")
                return primer_sequence
            else:
                logger.info("Не найдена primer, начинаем с пустой мелодии")
                return mm.NoteSequence(notes=[])
        except Exception as ex:
            logger.error(f'Error while loading primer sequence from {self.primer_midi_file}', ex, exc_info=True)
            return mm.NoteSequence(notes=[])

    def generate_melody(self) -> mm.NoteSequence:
        """
        Генерирует мелодию с заданными параметрами.

        Returns:
            mm.NoteSequence: Сгенерированная мелодия.
        """
        melody_sequence = self.melody_rnn.generate(
            temperature=self.temperature,
            steps=self.num_steps,
            primer_sequence=self.primer_sequence
        )
        return melody_sequence

    def add_chords(self, melody_sequence: mm.NoteSequence) -> mm.NoteSequence:
        """
        Добавляет аккорды к мелодии.

        Args:
            melody_sequence (mm.NoteSequence): Мелодия, к которой нужно добавить аккорды.

        Returns:
            mm.NoteSequence: Мелодия с добавленными аккордами.
        """
        chords = [
            'C', 'G', 'Am', 'F',
            'Dm', 'G', 'C', 'G',
            'C', 'F', 'Dm', 'G',
            'Am', 'G', 'F', 'E'
        ] * (self.num_steps // 16)

        chord_sequence = mm.ChordSequence(chords)
        melody_with_chords_sequence = mm.sequences_lib.concatenate_sequences(melody_sequence, chord_sequence)
        return melody_with_chords_sequence

    def add_drums(self, melody_with_chords_sequence: mm.NoteSequence) -> mm.NoteSequence:
        """
        Добавляет барабаны к мелодии.

        Args:
            melody_with_chords_sequence (mm.NoteSequence): Мелодия с аккордами, к которой нужно добавить барабаны.

        Returns:
            mm.NoteSequence: Мелодия с аккордами и барабанами.
        """
        drum_pattern = mm.DrumTrack(
            [36, 0, 42, 0, 38, 0, 46, 0, 36, 0, 42, 0, 38, 0, 45, 0],
            start_step=0,
            steps_per_bar=self.num_steps // 8,
            steps_per_quarter=8,
        )
        music_sequence = mm.sequences_lib.concatenate_sequences(melody_with_chords_sequence, drum_pattern)
        return music_sequence

    def set_tempo(self, music_sequence: mm.NoteSequence) -> mm.NoteSequence:
        """
        Устанавливает темп для музыкальной последовательности.

        Args:
            music_sequence (mm.NoteSequence): Музыкальная последовательность.

        Returns:
            mm.NoteSequence: Музыкальная последовательность с установленным темпом.
        """
        music_sequence.tempos[0].qpm = self.tempo
        return music_sequence

    def save_midi(self, music_sequence: mm.NoteSequence, filename: str = 'full_music_advanced.mid') -> None:
        """
        Сохраняет музыкальную последовательность в MIDI-файл.

        Args:
            music_sequence (mm.NoteSequence): Музыкальная последовательность.
            filename (str, optional): Имя файла для сохранения. По умолчанию 'full_music_advanced.mid'.
        """
        midi_file = os.path.join(self.output_dir, filename)
        try:
            mm.sequence_proto_to_midi_file(music_sequence, midi_file)
            logger.info(f"Полная композиция сгенерирована и сохранена в: {midi_file}")
        except Exception as ex:
            logger.error(f'Error while saving midi file to {midi_file}', ex, exc_info=True)

    def generate_full_music(self) -> None:
        """
        Генерирует полную музыкальную композицию.
        """
        melody_sequence = self.generate_melody()
        melody_with_chords_sequence = self.add_chords(melody_sequence)
        music_sequence = self.add_drums(melody_with_chords_sequence)
        music_sequence = self.set_tempo(music_sequence)
        self.save_midi(music_sequence)


if __name__ == '__main__':
    # Пример использования класса
    music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn',
                                    temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)
    music_generator.generate_full_music()

    # Другой пример с другими параметрами
    music_generator2 = MagentaMusic(output_dir='my_music2', model_name='basic_rnn',
                                    temperature=0.9, num_steps=150, primer_midi_file='primer2.mid', tempo=120)
    music_generator2.generate_full_music()