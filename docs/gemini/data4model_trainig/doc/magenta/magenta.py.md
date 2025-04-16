## Модуль интеграции Google Generative AI

Этот модуль представляет собой клиент для работы с Magenta, в частности для генерации музыки с использованием моделей машинного обучения.

#### Ключевые функции:

1. **Совместное создание музыки:**
   - Модуль помогает разработчикам и музыкантам в создании уникальных музыкальных композиций.
2.  **Гибкая настройка**:
    -   Используются различные параметры для управления характеристиками генерируемой музыки.
3.  **Простота использования**:
    -   Оптимизирован для быстрой интеграции и экспериментов с Magenta.

### Установка и настройка

1.  Убедитесь, что установлен TensorFlow (необходим для работы с Magenta):
    ```bash
    pip install tensorflow
    ```
2. Установите magenta:
    ```bash
    pip install magenta
    ```
3. Подготовьте MIDI-файлы для затравки (primer.mid и primer2.mid), или оставьте их пустыми.

### Использование

#### Инициализация класса MagentaMusic
Перед созданием музыки, необходимо инициализировать класс.
```python
    music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn',
                                    temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)
```
*Атрибуты класса:*
-   `output_dir` (str): Путь к директории для сохранения сгенерированной музыки.
-   `model_name` (str): Имя модели машинного обучения.
-   `temperature` (float): Параметр случайности для генерации мелодии.
-   `num_steps` (int): Количество шагов при генерации мелодии.
   -`primer_midi_file` (file): Файл MIDI для создания первой ноты композиции
    -`tempo` (float): Темп мелодии.
####  Генерация музыки
Чтобы создать и сохранить музыку, используйте метод класса  `generate_full_music()`
```python
 music_generator.generate_full_music()
```
Сгенерированные композиции будут сохранены в папках `my_music` и `my_music2`.

### Функция `_load_primer_sequence`

```python
def _load_primer_sequence(self):
    if os.path.exists(self.primer_midi_file):
        primer_sequence = mm.midi_file_to_sequence_proto(self.primer_midi_file)
        print(f"Используем primer из {self.primer_midi_file}")
        return primer_sequence
    else:
        print("Не найдена primer, начинаем с пустой мелодии")
        return mm.NoteSequence(notes=[])
```

**Назначение**: Загружает MIDI-файл затравки для создания первой ноты в композиции

**Как работает функция**:

1. Проверяет наличие MIDI файла.
2. Если файл найден - использует его для инициализации первой ноты
3. Если файл не найден - создает пустую ноту

### Функция `generate_melody`

```python
 def generate_melody(self):
        melody_sequence = self.melody_rnn.generate(
            temperature=self.temperature,
            steps=self.num_steps,
            primer_sequence=self.primer_sequence
        )
        return melody_sequence
```

**Назначение**: Генерирует мелодию

**Как работает функция**:

1. Использует библиотеку magenta для создания мелодии, принимает значения:
-`temperature`: для создания случайности, креативности мелодии
-`steps`: Количество шагов для создания
-`primer_sequence`: Начальная нота для создания мелодии

### Функция `add_chords`

```python
def add_chords(self, melody_sequence):
        chords = [
            "C", "G", "Am", "F",
            "Dm", "G", "C", "G",
            "C", "F", "Dm", "G",
            "Am", "G", "F", "E"
        ] * (self.num_steps // 16)

        chord_sequence = mm.ChordSequence(chords)
        melody_with_chords_sequence = mm.sequences_lib.concatenate_sequences(melody_sequence, chord_sequence)
        return melody_with_chords_sequence
```
**Назначение**: Добавляет аккорды в мелодию

**Как работает функция**:

1.  Задает последовательностей аккордов. Аккорды хардкожены, с ними ничего сделать нельзя, можно только изменить их.
2.  С помощью magenta собирает аккорды и мелодию вместе

### Функция `add_drums`

```python
 def add_drums(self, melody_with_chords_sequence):
        drum_pattern = mm.DrumTrack(
            [36, 0, 42, 0, 38, 0, 46, 0, 36, 0, 42, 0, 38, 0, 45, 0],
            start_step=0,
            steps_per_bar=self.num_steps // 8,
            steps_per_quarter=8,
        )
        music_sequence = mm.sequences_lib.concatenate_sequences(melody_with_chords_sequence, drum_pattern)
        return music_sequence
```
**Назначение**: Добавляет партию ударных в мелодию

**Как работает функция**:

1.  Задает паттерны ударных. Паттерны хардкожены, с ними ничего сделать нельзя, можно только изменить их.
2.  С помощью magenta собирает парию ударных и мелодию вместе

### Функция `set_tempo`

```python
def set_tempo(self, music_sequence):
        music_sequence.tempos[0].qpm = self.tempo
        return music_sequence
```

**Назначение**: Задает темп для мелодии

**Как работает функция**:

1.  Задает темп для музыкальной композиции

### Функция `save_midi`

```python
def save_midi(self, music_sequence, filename='full_music_advanced.mid'):
         midi_file = os.path.join(self.output_dir, filename)
         mm.sequence_proto_to_midi_file(music_sequence, midi_file)
         print(f"Полная композиция сгенерирована и сохранена в: {midi_file}")
```
**Назначение**: Сохраняет готовую мелодию в файл.
**Как работает функция**:

1.  Определяет имя для сохранения файла
2.  С помощью magenta сохраняет MIDI файл

## Предупреждения

Перед использованием модуля убедитесь, что установлена библиотека Magenta и TensorFlow.

Обязательно ознакомьтесь с документацией по моделям Magenta, чтобы понимать, как правильно настраивать и использовать их:
    [magenta](https://magenta.tensorflow.org/)
```python
## \\file /src/llm/magenta/magenta.py
# -*- coding: utf-8 -*-\n

#! .pyenv/bin/python3
```
Данный код нужно убрать
Значения "magic string" стоит вынести в config, либо в константы
Перед началом работы - надо создать файлы `primer.mid` и `primer2.mid`

Полезно было бы добавить обработку исключений

В целом - сейчас этот код является простой оберткой для magenta
```
if __name__ == '__main__':
    # Пример использования класса
    music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn',
                                    temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)
    music_generator.generate_full_music()

    # Другой пример с другими параметрами
    music_generator2 = MagentaMusic(output_dir='my_music2', model_name='basic_rnn',
                                    temperature=0.9, num_steps=150, primer_midi_file='primer2.mid', tempo=120)
    music_generator2.generate_full_music()
```
В коде нету информации, о том, где эти файлы окажутся - то есть их нужно положить в корень проекта (что не очевидно), либо поменять это поведение

Не забудьте указать используемые модели!
```python
response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
```

```python
  openai.API_KEY = "YOUR_API_KEYS_OPENAI"
```

Нужно предостерегать от того, чтобы не лить ключи!

Обязательно расскажите, что нужно создать Midi файл

## Дополнительная информация
Сделайте описание более живым, как будто вы общаетесь с другим разработчиком