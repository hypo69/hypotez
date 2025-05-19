import os
import librosa
import numpy as np
import pickle

AUDIO_PATH = "audio"
FEATURES_PATH = "features.pkl"
N_MELS = 40  # Должно совпадать с размерностью входа в модель
SR = 16000  # Частота дискретизации


def extract_melspectrogram(file_path, sr=SR, n_mels=N_MELS):
    y, _ = librosa.load(file_path, sr=sr)
    y, _ = librosa.effects.trim(y)  # Удаляем тишину в начале и конце

    if len(y) == 0:
        return None  # Пропускаем пустые файлы

    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
    mel_db = librosa.power_to_db(mel_spec, ref=np.max)  # Преобразуем в dB

    feature = np.mean(mel_db, axis=1)  # Усредняем по времени (по столбцам)

    # Нормализация (z-score)
    feature = (feature - np.mean(feature)) / (np.std(feature) + 1e-6)

    return feature


data = {}

total_files = 0
for file in os.listdir(AUDIO_PATH):
    if file.endswith(".wav"):
        name = file.split("_")[0]  # Получаем имя друга
        file_path = os.path.join(AUDIO_PATH, file)

        mel_features = extract_melspectrogram(file_path)

        if mel_features is None:
            print(f"Пропущен пустой файл: {file}")
            continue

        if name not in data:
            data[name] = []
        data[name].append(mel_features)
        total_files += 1

# Сохраняем данные
with open(FEATURES_PATH, "wb") as f:
    pickle.dump(data, f)

print(f"Извлечены признаки и сохранены в {FEATURES_PATH}")
for speaker, samples in data.items():
    print(f"{speaker}: {len(samples)} записей")
