import os
import librosa
import numpy as np
import pickle
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Пути к данным
AUDIO_PATH = "audio"
FEATURES_PATH = "features.pkl"
SR = 16000  # Частота дискретизации
N_MELS = 40  # Количество мел-банков


# Функция аугментации
def augment_audio(y, sr):
    if np.random.rand() < 0.5:
        y = y + 0.005 * np.random.randn(len(y))  # Добавление шума
    if np.random.rand() < 0.5:
        shift = np.random.randint(sr // 10)  # Сдвиг до 0.1 сек
        y = np.roll(y, shift)
    return y


# Функция извлечения признаков
def extract_melspectrogram(file_path, sr=SR, n_mels=N_MELS, augment=False):
    y, _ = librosa.load(file_path, sr=sr)
    if augment:
        y = augment_audio(y, sr)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
    mel_db = librosa.power_to_db(mel_spec, ref=np.max)
    return np.mean(mel_db, axis=1)  # Усреднение по времени


# Загрузка и обработка данных
data = {}
for file in os.listdir(AUDIO_PATH):
    if file.endswith(".wav"):
        name = file.split("_")[0]
        file_path = os.path.join(AUDIO_PATH, file)
        mel_features = extract_melspectrogram(file_path)
        aug_features = extract_melspectrogram(file_path, augment=True)  # Аугментированные данные

        if name not in data:
            data[name] = []
        data[name].extend([mel_features, aug_features])

# Сохранение данных
with open(FEATURES_PATH, "wb") as f:
    pickle.dump(data, f)

# Формирование массивов
X, y = [], []
for name, features in data.items():
    for feature in features:
        X.append(feature)
        y.append(name)
X, y = np.array(X), np.array(y)

# Нормализация
X = (X - np.mean(X, axis=0)) / (np.std(X, axis=0) + 1e-6)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_test = torch.tensor(X_train, dtype=torch.float32), torch.tensor(X_test, dtype=torch.float32)
y_train, y_test = torch.tensor(y_train, dtype=torch.long), torch.tensor(y_test, dtype=torch.long)


# Улучшенная нейросеть
class VoiceClassifier(nn.Module):
    def __init__(self, input_size, num_classes):
        super(VoiceClassifier, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.3)  # Dropout 30%
        self.fc2 = nn.Linear(128, 64)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.3)
        self.fc3 = nn.Linear(64, 32)
        self.relu3 = nn.ReLU()
        self.fc4 = nn.Linear(32, num_classes)

    def forward(self, x):
        x = self.dropout1(self.relu1(self.fc1(x)))
        x = self.dropout2(self.relu2(self.fc2(x)))
        x = self.relu3(self.fc3(x))
        x = self.fc4(x)
        return x


# Создание модели
model = VoiceClassifier(input_size=X_train.shape[1], num_classes=len(label_encoder.classes_))
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)  # L2-регуляризация

# Обучение
epochs = 200
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

    with torch.no_grad():
        train_acc = (torch.argmax(model(X_train), dim=1) == y_train).float().mean().item()
        test_acc = (torch.argmax(model(X_test), dim=1) == y_test).float().mean().item()

    if (epoch + 1) % 10 == 0:
        print(
            f"Эпоха [{epoch + 1}/{epochs}], Потери: {loss.item():.4f}, Train Acc: {train_acc:.2f}, Test Acc: {test_acc:.2f}")

# Сохранение
torch.save(model.state_dict(), "model_nn.pth")
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("Обучение завершено, модель сохранена!")

