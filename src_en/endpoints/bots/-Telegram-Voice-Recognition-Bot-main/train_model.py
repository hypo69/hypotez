import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# We load the signs
FEATURES_PATH = "features.pkl"

with open(FEATURES_PATH, "rb") as f:
    data = pickle.load(f)

X = []  # Signs
y = []  # Tags (friends' names)

for name, features in data.items():
    for feature in features:
        X.append(feature)
        y.append(name)

X = np.array(X)
y = np.array(y)

# Data normalization
X = (X - np.mean(X, axis=0)) / (np.std(X, axis=0) + 1e-6)

# Coding names in numbers
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# We divide into Train/Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialization patterns
model = SVC(kernel="linear", probability=True)

best_accuracy = 0.0
best_model = None

# The number of eras
epochs = 10
for epoch in range(1, epochs + 1):
    model.fit(X_train, y_train)

    # Testing accuracy
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)

    print(f"Эпоха [{epoch}/{epochs}], Train Acc: {train_acc:.2f}, Test Acc: {test_acc:.2f}")

    # We keep the best model
    if test_acc > best_accuracy:
        best_accuracy = test_acc
        best_model = model

# We keep the best model and encoder
with open("model_svm.pkl", "wb") as f:
    pickle.dump(best_model, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print(f"Обучение завершено! Лучшая точность на тесте: {best_accuracy:.2f}")