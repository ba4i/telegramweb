# Number Theory Learning App

Интерактивная платформа для изучения теории чисел в формате Telegram MiniApp.

## 🚀 Быстрый старт

### 1. Создание Telegram бота

1. Откройте Telegram и найдите @BotFather
2. Отправьте команду `/newbot`
3. Выберите имя для бота (например: "Number Theory Learning")
4. Выберите username (например: "number_theory_learning_bot")
5. Скопируйте полученный токен

### 2. Настройка окружения

```bash
# Клонируйте или скачайте проект
git clone <repository-url>
cd number_theory_app

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Скопируйте настройки окружения
cp .env.example .env

# Отредактируйте .env файл с вашими настройками
nano .env
```

### 3. Настройка базы данных

```bash
# Для PostgreSQL (рекомендуется)
# Создайте базу данных number_theory_db
# Обновите настройки DB_* в .env файле

# Или используйте SQLite для тестирования
# Раскомментируйте строки SQLite в settings.py

# Выполните миграции
python manage.py makemigrations
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Загрузите начальные данные
python manage.py loaddata initial_data.json
```

### 4. Запуск разработки

#### Вариант A: Локально

```bash
# Терминал 1 - Django сервер
python manage.py runserver

# Терминал 2 - Туннель ngrok для доступа из Telegram
ngrok http 8000
# Скопируйте HTTPS URL (например: https://abc123.ngrok.io)

# Терминал 3 - Telegram бот
# Обновите WEBAPP_URL в .env на ngrok URL
python telegram_bot.py
```

#### Вариант B: Docker

```bash
# Запустите все сервисы
docker-compose up --build

# В отдельном терминале - ngrok
ngrok http 8000
# Обновите WEBAPP_URL в docker-compose.yml
```

### 5. Настройка бота в Telegram

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Нажмите кнопку "🚀 Начать изучение теории чисел"
4. Приложение должно открыться!

## 📂 Структура проекта

```
number_theory_app/
├── manage.py                 # Django управление
├── requirements.txt          # Python зависимости
├── .env.example             # Пример настроек
├── telegram_bot.py          # Telegram бот
├── Dockerfile               # Docker конфигурация
├── docker-compose.yml       # Docker Compose
├── number_theory_app/       # Django настройки
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── webapp/                  # Основное приложение
│   ├── models.py           # Модели БД
│   ├── views.py            # API endpoints
│   ├── urls.py             # URL маршруты
│   └── admin.py            # Django админка
├── static/                  # Статические файлы
│   ├── css/style.css       # Стили приложения
│   ├── js/app.js           # JavaScript логика
│   └── images/             # Изображения
└── templates/
    └── index.html          # Главная страница MiniApp
```

## 🌐 Деплой в продакшен

### Heroku

```bash
# Установите Heroku CLI
# Создайте приложение
heroku create your-app-name

# Добавьте PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Настройте переменные окружения
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set TELEGRAM_BOT_TOKEN="your-bot-token"
heroku config:set WEBAPP_URL="https://your-app-name.herokuapp.com"

# Деплой
git push heroku main

# Выполните миграции
heroku run python manage.py migrate

# Загрузите данные
heroku run python manage.py loaddata initial_data.json
```

### Railway/Render/VPS

Аналогично Heroku, но настройте переменные окружения через веб-интерфейс платформы.

## 📊 Администрирование

```bash
# Доступ к Django админке
# Перейдите на https://your-domain.com/admin/
# Войдите под суперпользователем

# В админке можно:
# - Управлять вопросами и темами
# - Просматривать статистику пользователей
# - Настраивать ачивки
# - Модерировать контент
```

## 🔧 API Endpoints

- `GET /` - Главная страница MiniApp
- `POST /api/profile/` - Создание/обновление профиля
- `GET /api/profile/?telegram_id=ID` - Получение профиля
- `GET /api/topics/` - Список тем
- `GET /api/topics/{id}/questions/` - Вопросы по теме
- `POST /api/answer/` - Отправка ответа
- `GET /api/statistics/` - Статистика пользователя

## 🎮 Функции приложения

### Для студентов:
- 📚 Изучение 5 тем теории чисел
- 🎯 Два режима: Учёба и Экзамен
- 🏆 Система уровней и ачивок
- 📊 Детальная статистика
- 🔥 Стрики и мотивация

### Для преподавателей:
- ➕ Добавление новых вопросов
- 📈 Аналитика прогресса студентов
- 🎛️ Настройка сложности
- 📋 Экспорт результатов

## 🔒 Безопасность

- Валидация Telegram WebApp данных
- CSRF защита для API
- Санитизация пользовательского ввода
- Rate limiting для предотвращения спама
- Secure headers

## 📞 Поддержка

При возникновении вопросов:
1. Проверьте логи: `docker-compose logs` или `heroku logs --tail`
2. Убедитесь, что все переменные окружения настроены
3. Проверьте, что ngrok запущен (для локальной разработки)
4. Обратитесь к разработчику: @yourusername

## 📄 Лицензия

MIT License - используйте свободно для образовательных целей.
