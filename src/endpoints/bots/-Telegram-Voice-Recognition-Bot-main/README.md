# 🤖 Telegram Voice Recognition Bot

Этот проект представляет собой Telegram-бота для распознавания говорящих по голосовым сообщениям с использованием нейросетевой модели.

## 📌 Функции
- 📥 Принимает голосовые сообщения
- 🔍 Анализирует голос и определяет говорящего
- 📃 Показывает список известных говорящих (`/speakers`)
- 🚀 Работает на основе MFCC-фич и нейросети, обученной на PyTorch

## 🛠️ Установка

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/ваш-логин/ваш-репозиторий.git
cd ваш-репозиторий
```

### 2. Установите зависимости
```bash
pip install -r requirements.txt
```

### 3. Создайте `.env` файл и добавьте токен бота
```ini
TOKEN="ваш_токен_бота"
```

### 4. Запустите бота
```bash
python bot.py
```

## 📂 Структура проекта
```
📁 ваш-репозиторий/
├── audio/                 # Папка для загружаемых голосовых сообщений
├── model_nn.pth           # Файл с обученной моделью
├── label_encoder.pkl      # Кодировщик меток (LabelEncoder)
├── bot.py                 # Основной код бота
├── train_nn.py            # Код для обучения нейросети
├── requirements.txt       # Зависимости проекта
├── .gitignore             # Исключенные файлы (например, .env)
└── README.md              # Описание проекта
```

## 🧠 Как работает
1. Пользователь отправляет голосовое сообщение боту.
2. Бот скачивает аудиофайл и конвертирует его в `.wav`.
3. Из аудио извлекаются MFCC-признаки.
4. Нейросеть анализирует голос и определяет, кому он принадлежит.
5. Бот отправляет пользователю имя говорящего.

## 🚀 Улучшения
- 🔄 Добавление новых голосов без переобучения модели
- 🎤 Улучшение предобработки аудио
- 📊 Добавление статистики по предсказаниям

## 📜 Лицензия
Этот проект распространяется под лицензией MIT.

