import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Загружаем признаки
FEATURES_PATH = "features.pkl"

with open(FEATURES_PATH, "rb") as f:
    data = pickle.load(f)

X = []  # признаки
y = []  # метки (имена друзей)

for name, features in data.items():
    for feature in features:
        X.append(feature)
        y.append(name)

X = np.array(X)
y = np.array(y)

# Нормализация данных
X = (X - np.mean(X, axis=0)) / (np.std(X, axis=0) + 1e-6)

# Кодируем имена в числа
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Разделяем на train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Инициализация модели
model = SVC(kernel="linear", probability=True)

best_accuracy = 0.0
best_model = None

# Количество эпох
epochs = 10
for epoch in range(1, epochs + 1):
    model.fit(X_train, y_train)

    # Проверяем точность
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)

    print(f"Эпоха [{epoch}/{epochs}], Train Acc: {train_acc:.2f}, Test Acc: {test_acc:.2f}")

    # Сохраняем лучшую модель
    if test_acc > best_accuracy:
        best_accuracy = test_acc
        best_model = model

# Сохраняем лучшую модель и кодировщик
with open("model_svm.pkl", "wb") as f:
    pickle.dump(best_model, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print(f"Обучение завершено! Лучшая точность на тесте: {best_accuracy:.2f}")