### **Анализ кода модуля `magenta.py`**

## \file /src/ai/magenta/magenta.py

Модуль предоставляет класс `MagentaMusic` для генерации музыки с использованием Magenta.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Класс `MagentaMusic` хорошо структурирован и предоставляет методы для генерации мелодий, добавления аккордов и барабанов, установки темпа и сохранения MIDI-файла.
    - Использование `os.makedirs` с `exist_ok=True` позволяет избежать ошибок, если директория уже существует.
    - Пример использования в `if __name__ == '__main__'` демонстрирует основные возможности класса.
- **Минусы**:
    - Отсутствуют аннотации типов для параметров и возвращаемых значений функций.
    - Отсутствует логирование.
    - Отсутствует обработка исключений.
    - Не все строки документированы.
    - Жестко заданные значения (например, аккорды, барабанные паттерны).

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех параметров функций и возвращаемых значений.
2.  **Добавить логирование**:
    - Добавить логирование для отслеживания процесса генерации музыки и выявления возможных ошибок.
3.  **Обработка исключений**:
    - Добавить блоки `try...except` для обработки возможных исключений, таких как отсутствие MIDI-файла или ошибки при генерации музыки.
4.  **Улучшить документацию**:
    - Добавить более подробные комментарии и docstring для каждой функции и метода.
    - Описать возможные исключения, которые могут быть выброшены.
5.  **Избавиться от жестко заданных значений**:
    - Аккорды и барабанные паттерны должны быть параметрами, передаваемыми в класс, а не жестко заданными значениями.
6.  **Использовать `j_loads` или `j_loads_ns`**:
    - Если в коде есть чтение JSON или конфигурационных файлов, заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
7.  **Следовать PEP8**:
    - Проверить и исправить код в соответствии со стандартами PEP8.
8. **Использовать logger из `src.logger`**:
    - Для логирования использовать модуль `logger` из `src.logger.logger`.

**Оптимизированный код:**

```python
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с Magenta Music
==================================

Модуль содержит класс :class:`MagentaMusic`, который используется для генерации музыки с использованием Magenta.

Пример использования
----------------------

>>> music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn',
                                    temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)
>>> music_generator.generate_full_music()
"""

import os
from pathlib import Path
import magenta.music as mm
from magenta.models.melody_rnn import melody_rnn_sequence_generator
import tensorflow as tf  # Import TensorFlow
from typing import List
from src.logger import logger


class MagentaMusic:
    """
    Класс для генерации музыки с использованием Magenta.
    """

    def __init__(
        self,
        output_dir: str = "generated_music_advanced",
        model_name: str = "attention_rnn",
        temperature: float = 1.2,
        num_steps: int = 256,
        primer_midi_file: str | Path = "primer.mid",
        tempo: int = 100,
        chords: List[str] = None,
        drum_pattern: List[int] = None,
    ) -> None:
        """
        Инициализация класса MagentaMusic.

        Args:
            output_dir (str): Директория для сохранения сгенерированной музыки.
            model_name (str): Имя модели для генерации мелодии.
            temperature (float): Температура для генерации мелодии.
            num_steps (int): Количество шагов для генерации мелодии.
            primer_midi_file (str | Path): Путь к MIDI-файлу затравки.
            tempo (int): Темп музыки.
            chords (List[str]): Список аккордов для добавления к мелодии.
            drum_pattern (List[int]): Барабанный паттерн для добавления к мелодии.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.model_name = model_name
        self.temperature = temperature
        self.num_steps = num_steps
        self.primer_midi_file = primer_midi_file
        self.tempo = tempo
        self.chords = chords or [
            "C",
            "G",
            "Am",
            "F",
            "Dm",
            "G",
            "C",
            "G",
            "C",
            "F",
            "Dm",
            "G",
            "Am",
            "G",
            "F",
            "E",
        ] * (
            self.num_steps // 16
        )  # Аккорды по умолчанию
        self.drum_pattern = drum_pattern or [
            36,
            0,
            42,
            0,
            38,
            0,
            46,
            0,
            36,
            0,
            42,
            0,
            38,
            0,
            45,
            0,
        ]  # Барабанный паттерн по умолчанию
        try:
            self.melody_rnn = (
                melody_rnn_sequence_generator.MelodyRnnSequenceGenerator(
                    model_name=self.model_name
                )
            )
            self.primer_sequence = self._load_primer_sequence()
        except Exception as ex:
            logger.error(
                "Ошибка при инициализации MagentaMusic", ex, exc_info=True
            )

    def _load_primer_sequence(self) -> mm.NoteSequence:
        """
        Загружает MIDI-файл затравки или создаёт пустую NoteSequence, если файл не найден.

        Returns:
            mm.NoteSequence: MIDI-последовательность затравки.
        """
        try:
            if os.path.exists(self.primer_midi_file):
                primer_sequence = mm.midi_file_to_sequence_proto(
                    self.primer_midi_file
                )
                print(f"Используем primer из {self.primer_midi_file}")
                return primer_sequence
            else:
                print("Не найдена primer, начинаем с пустой мелодии")
                return mm.NoteSequence(notes=[])
        except Exception as ex:
            logger.error(
                "Ошибка при загрузке primer sequence", ex, exc_info=True
            )
            return mm.NoteSequence(notes=[])

    def generate_melody(self) -> mm.NoteSequence:
        """
        Генерирует мелодию с заданными параметрами.

        Returns:
            mm.NoteSequence: Сгенерированная мелодия.
        """
        try:
            melody_sequence = self.melody_rnn.generate(
                temperature=self.temperature,
                steps=self.num_steps,
                primer_sequence=self.primer_sequence,
            )
            return melody_sequence
        except Exception as ex:
            logger.error("Ошибка при генерации мелодии", ex, exc_info=True)
            return mm.NoteSequence(notes=[])

    def add_chords(self, melody_sequence: mm.NoteSequence) -> mm.NoteSequence:
        """
        Добавляет аккорды к мелодии.

        Args:
            melody_sequence (mm.NoteSequence): Мелодия, к которой нужно добавить аккорды.

        Returns:
            mm.NoteSequence: Мелодия с добавленными аккордами.
        """

        chord_sequence = mm.ChordSequence(self.chords)
        melody_with_chords_sequence = mm.sequences_lib.concatenate_sequences(
            melody_sequence, chord_sequence
        )
        return melody_with_chords_sequence

    def add_drums(
        self, melody_with_chords_sequence: mm.NoteSequence
    ) -> mm.NoteSequence:
        """
        Добавляет барабаны к мелодии.

        Args:
            melody_with_chords_sequence (mm.NoteSequence): Мелодия с аккордами, к которой нужно добавить барабаны.

        Returns:
            mm.NoteSequence: Мелодия с добавленными аккордами и барабанами.
        """
        drum_pattern = mm.DrumTrack(
            self.drum_pattern,
            start_step=0,
            steps_per_bar=self.num_steps // 8,
            steps_per_quarter=8,
        )
        music_sequence = mm.sequences_lib.concatenate_sequences(
            melody_with_chords_sequence, drum_pattern
        )
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

    def save_midi(
        self, music_sequence: mm.NoteSequence, filename: str = "full_music_advanced.mid"
    ) -> None:
        """
        Сохраняет музыкальную последовательность в MIDI-файл.

        Args:
            music_sequence (mm.NoteSequence): Музыкальная последовательность для сохранения.
            filename (str): Имя файла для сохранения.
        """
        try:
            midi_file = os.path.join(self.output_dir, filename)
            mm.sequence_proto_to_midi_file(music_sequence, midi_file)
            print(f"Полная композиция сгенерирована и сохранена в: {midi_file}")
            logger.info(
                f"Полная композиция сгенерирована и сохранена в: {midi_file}"
            )
        except Exception as ex:
            logger.error(
                f"Ошибка при сохранении MIDI-файла {filename}",
                ex,
                exc_info=True,
            )

    def generate_full_music(self) -> None:
        """
        Генерирует полную музыкальную композицию.
        """
        try:
            melody_sequence = self.generate_melody()
            melody_with_chords_sequence = self.add_chords(melody_sequence)
            music_sequence = self.add_drums(melody_with_chords_sequence)
            music_sequence = self.set_tempo(music_sequence)
            self.save_midi(music_sequence)
        except Exception as ex:
            logger.error(
                "Ошибка при генерации полной музыкальной композиции",
                ex,
                exc_info=True,
            )


if __name__ == "__main__":
    # Пример использования класса
    music_generator = MagentaMusic(
        output_dir="my_music",
        model_name="attention_rnn",
        temperature=1.1,
        num_steps=200,
        primer_midi_file="primer.mid",
        tempo=110,
    )
    music_generator.generate_full_music()

    # Другой пример с другими параметрами
    music_generator2 = MagentaMusic(
        output_dir="my_music2",
        model_name="basic_rnn",
        temperature=0.9,
        num_steps=150,
        primer_midi_file="primer2.mid",
        tempo=120,
    )
    music_generator2.generate_full_music()