# ntapp/models.py
from django.db import models
from django.db.models import Sum


class Ticket(models.Model):
    number = models.IntegerField()
    question = models.TextField()
    answer = models.TextField()
    theme = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Билет {self.number}: {self.question[:50]}"


class UserProfile(models.Model):
    user_id = models.CharField(max_length=100, unique=True)  # Telegram ID
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)

    total_score = models.IntegerField(default=0)  # Общие очки
    level = models.IntegerField(default=1)  # Уровень (1-20)
    experience = models.IntegerField(default=0)  # Опыт для следующего уровня

    exams_completed = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name or self.username or self.user_id} (Уровень {self.level})"

    @property
    def experience_for_next_level(self):
        """Опыт, необходимый для следующего уровня"""
        return self.level * 100

    @property
    def experience_progress_percent(self):
        """Прогресс к следующему уровню в процентах"""
        return min(100, (self.experience / self.experience_for_next_level) * 100)

    def add_experience(self, exp_points):
        """Добавляет опыт и проверяет повышение уровня"""
        self.experience += exp_points

        while self.experience >= self.experience_for_next_level and self.level < 20:
            self.experience -= self.experience_for_next_level
            self.level += 1

        self.save()
        return self.level


class ExamResult(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    time_spent = models.IntegerField()  # в секундах
    best_streak = models.IntegerField(default=0)

    # Система очков
    score_earned = models.IntegerField(default=0)  # Очки за экзамен
    time_bonus = models.IntegerField(default=0)  # Бонус за скорость
    streak_bonus = models.IntegerField(default=0)  # Бонус за стрик

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Экзамен {self.user_profile.first_name}: {self.correct_answers}/{self.total_questions} - {self.score_earned} очков"

    @property
    def percentage(self):
        return int((self.correct_answers / self.total_questions) * 100)

    def calculate_score(self):
        """Вычисляет очки за экзамен"""
        base_points = self.correct_answers * 10  # 10 очков за правильный ответ

        # Бонус за процент правильных ответов
        percentage_bonus = 0
        if self.percentage >= 90:
            percentage_bonus = 50  # Отличный результат
        elif self.percentage >= 70:
            percentage_bonus = 30  # Хороший результат
        elif self.percentage >= 50:
            percentage_bonus = 15  # Удовлетворительно

        # Бонус за скорость (если прошел быстро)
        expected_time = self.total_questions * 30  # 30 сек на вопрос
        if self.time_spent < expected_time * 0.7:  # Прошел за 70% времени
            self.time_bonus = 25
        elif self.time_spent < expected_time * 0.85:  # Прошел за 85% времени
            self.time_bonus = 10

        # Бонус за стрик
        if self.best_streak >= 7:
            self.streak_bonus = 40
        elif self.best_streak >= 5:
            self.streak_bonus = 25
        elif self.best_streak >= 3:
            self.streak_bonus = 15

        self.score_earned = base_points + percentage_bonus + self.time_bonus + self.streak_bonus
        return self.score_earned


class Leaderboard(models.Model):
    """Таблица лидеров (обновляется каждый день)"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rank = models.IntegerField()
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['user_profile', 'date']
        ordering = ['rank']

    def __str__(self):
        return f"#{self.rank} {self.user_profile.first_name} - {self.score} очков"
