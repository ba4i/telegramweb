# ntapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg, Sum, Count
from django.views.decorators.http import require_http_methods
from .models import Ticket, ExamResult, UserProfile, Leaderboard
import json
import random
from datetime import datetime, timedelta


def miniapp_view(request):
    """Главная страница Mini App"""
    return render(request, 'miniapp/index.html')


@csrf_exempt
def api_tickets(request):
    """API для получения билетов для экзамена - улучшенная версия"""
    try:
        # Получаем все валидные билеты (фильтруем плохие)
        all_tickets = Ticket.objects.filter(
            question__isnull=False
        ).exclude(
            Q(question__exact='') |
            Q(question__exact='a') |
            Q(question__icontains='question') |
            Q(question__len__lt=15)  # Очень короткие вопросы
        )

        if not all_tickets.exists():
            return JsonResponse({"error": "Билеты не найдены в базе данных"}, status=404)

        # Берем случайные 10 билетов для экзамена
        exam_tickets = list(all_tickets)
        random.shuffle(exam_tickets)
        exam_tickets = exam_tickets[:10]

        # Формируем ответ с вариантами для каждого вопроса
        tickets_data = []
        for ticket in exam_tickets:
            # Обрезаем длинные ответы для читаемости
            correct_answer = ticket.answer.strip()
            if len(correct_answer) > 150:
                correct_answer = correct_answer[:150] + "..."

            # Создаем разнообразные неправильные варианты ответов
            wrong_answers = [
                "Неверное утверждение по теории чисел",
                "Ошибочное математическое определение",
                "Неправильная алгебраическая концепция",
                "Некорректная формулировка теоремы"
            ]

            # Выбираем случайно 3 неправильных варианта
            selected_wrong = random.sample(wrong_answers, 3)

            tickets_data.append({
                "id": ticket.id,
                "number": ticket.number,
                "question": ticket.question,
                "correct_answer": correct_answer,
                "wrong_answers": selected_wrong,
                "theme": ticket.theme or "",
                "source": ticket.source or ""
            })

        return JsonResponse({
            "tickets": tickets_data,
            "count": len(tickets_data),
            "success": True
        })

    except Exception as e:
        return JsonResponse({
            "error": f"Ошибка сервера при загрузке билетов: {str(e)}",
            "success": False
        }, status=500)


@csrf_exempt
def api_exam_result(request):
    """API для сохранения результатов экзамена с начислением очков"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Получаем или создаем профиль пользователя
            user_id = data.get('user_id', 'anonymous')
            user_profile, created = UserProfile.objects.get_or_create(
                user_id=user_id,
                defaults={
                    'username': data.get('username', ''),
                    'first_name': data.get('first_name', 'Студент ВШЭ')
                }
            )

            # Создаем запись результата экзамена
            result = ExamResult.objects.create(
                user_profile=user_profile,
                total_questions=data.get('total_questions', 10),
                correct_answers=data.get('correct_answers', 0),
                time_spent=data.get('time_spent', 0),
                best_streak=data.get('best_streak', 0)
            )

            # Вычисляем очки за экзамен
            score_earned = result.calculate_score()
            result.save()

            # Обновляем профиль пользователя
            user_profile.total_score += score_earned
            user_profile.exams_completed += 1
            if result.best_streak > user_profile.best_streak:
                user_profile.best_streak = result.best_streak

            # Добавляем опыт (зависит от результата)
            exp_earned = max(10, result.correct_answers * 5 + (result.percentage // 10))
            old_level = user_profile.level
            user_profile.add_experience(exp_earned)

            level_up = user_profile.level > old_level

            user_profile.save()

            return JsonResponse({
                "success": True,
                "result": {
                    "score_earned": score_earned,
                    "time_bonus": result.time_bonus,
                    "streak_bonus": result.streak_bonus,
                    "exp_earned": exp_earned,
                    "new_level": user_profile.level,
                    "level_up": level_up,
                    "total_score": user_profile.total_score,
                    "experience": user_profile.experience,
                    "experience_for_next": user_profile.experience_for_next_level,
                    "experience_percent": user_profile.experience_progress_percent
                }
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": f"Ошибка сохранения результата: {str(e)}"
            }, status=500)

    return JsonResponse({"error": "Только POST запросы разрешены"}, status=405)


@csrf_exempt
def api_user_profile(request):
    """API для получения профиля пользователя"""
    user_id = request.GET.get('user_id', 'anonymous')

    try:
        user_profile = UserProfile.objects.get(user_id=user_id)

        # Статистика последних экзаменов
        recent_results = ExamResult.objects.filter(
            user_profile=user_profile
        ).order_by('-created_at')[:5]

        # Позиция в общем рейтинге
        rank = UserProfile.objects.filter(
            total_score__gt=user_profile.total_score
        ).count() + 1

        return JsonResponse({
            "profile": {
                "user_id": user_profile.user_id,
                "first_name": user_profile.first_name,
                "username": user_profile.username,
                "level": user_profile.level,
                "total_score": user_profile.total_score,
                "experience": user_profile.experience,
                "experience_for_next": user_profile.experience_for_next_level,
                "experience_percent": user_profile.experience_progress_percent,
                "exams_completed": user_profile.exams_completed,
                "best_streak": user_profile.best_streak,
                "rank": rank,
                "created_at": user_profile.created_at.isoformat()
            },
            "recent_results": [
                {
                    "score": result.score_earned,
                    "percentage": result.percentage,
                    "correct_answers": result.correct_answers,
                    "total_questions": result.total_questions,
                    "date": result.created_at.isoformat()
                }
                for result in recent_results
            ]
        })

    except UserProfile.DoesNotExist:
        # Возвращаем профиль для нового пользователя
        return JsonResponse({
            "profile": {
                "user_id": user_id,
                "first_name": "Новый игрок",
                "username": "",
                "level": 1,
                "total_score": 0,
                "experience": 0,
                "experience_for_next": 100,
                "experience_percent": 0,
                "exams_completed": 0,
                "best_streak": 0,
                "rank": 0
            },
            "recent_results": []
        })

    except Exception as e:
        return JsonResponse({
            "error": f"Ошибка получения профиля: {str(e)}"
        }, status=500)


@csrf_exempt
def api_leaderboard(request):
    """API для таблицы лидеров"""
    try:
        # Топ-20 игроков по общим очкам
        top_players = UserProfile.objects.filter(
            total_score__gt=0
        ).order_by('-total_score', '-level', '-exams_completed')[:20]

        leaderboard = []
        for idx, player in enumerate(top_players, 1):
            leaderboard.append({
                "rank": idx,
                "user_id": player.user_id,
                "first_name": player.first_name or "Игрок",
                "username": player.username,
                "level": player.level,
                "total_score": player.total_score,
                "exams_completed": player.exams_completed,
                "best_streak": player.best_streak,
                "created_at": player.created_at.isoformat()
            })

        return JsonResponse({
            "leaderboard": leaderboard,
            "total_players": UserProfile.objects.filter(total_score__gt=0).count()
        })

    except Exception as e:
        return JsonResponse({
            "error": f"Ошибка получения рейтинга: {str(e)}"
        }, status=500)


@csrf_exempt
def api_user_stats(request):
    """API для детальной статистики пользователя"""
    user_id = request.GET.get('user_id', 'anonymous')

    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
        user_results = ExamResult.objects.filter(user_profile=user_profile)

        if not user_results.exists():
            return JsonResponse({
                "total_exams": 0,
                "best_score": 0,
                "average_score": 0,
                "total_time": 0,
                "total_points_earned": 0,
                "average_streak": 0
            })

        # Вычисляем статистики
        total_exams = user_results.count()
        best_result = user_results.order_by('-correct_answers', '-score_earned').first()
        best_score = best_result.percentage if best_result else 0

        avg_correct = user_results.aggregate(Avg('correct_answers'))['correct_answers__avg'] or 0
        avg_total = user_results.aggregate(Avg('total_questions'))['total_questions__avg'] or 1
        average_score = int((avg_correct / avg_total) * 100)

        total_time = user_results.aggregate(Sum('time_spent'))['time_spent__sum'] or 0
        total_points = user_results.aggregate(Sum('score_earned'))['score_earned__sum'] or 0
        avg_streak = user_results.aggregate(Avg('best_streak'))['best_streak__avg'] or 0

        return JsonResponse({
            "total_exams": total_exams,
            "best_score": best_score,
            "average_score": average_score,
            "total_time": total_time,
            "total_points_earned": total_points,
            "average_streak": round(avg_streak, 1),
            "last_exam": user_results.last().created_at.isoformat() if user_results.exists() else None
        })

    except UserProfile.DoesNotExist:
        return JsonResponse({
            "total_exams": 0,
            "best_score": 0,
            "average_score": 0,
            "total_time": 0,
            "total_points_earned": 0,
            "average_streak": 0
        })

    except Exception as e:
        return JsonResponse({
            "error": f"Ошибка получения статистики: {str(e)}"
        }, status=500)


# Сохраняем старые функции для совместимости
@csrf_exempt
def api_themes(request):
    """API для получения тем"""
    themes = [
        {
            "id": 1,
            "title": "Основы теории множеств и кольца",
            "description": "Изучаем основные понятия теории множеств, групп и колец",
            "progress": 0,
            "color": "#3B82F6"
        },
        {
            "id": 2,
            "title": "Алгоритм деления и НОД",
            "description": "Деление с остатком и наибольший общий делитель",
            "progress": 0,
            "color": "#10B981"
        },
        {
            "id": 3,
            "title": "Алгоритм Евклида",
            "description": "Алгоритм нахождения НОД и его свойства",
            "progress": 0,
            "color": "#F59E0B"
        },
        {
            "id": 4,
            "title": "Простые числа",
            "description": "Определение простых чисел и основная теорема арифметики",
            "progress": 0,
            "color": "#EF4444"
        },
        {
            "id": 5,
            "title": "Сравнения по модулю",
            "description": "Арифметика сравнений и её свойства",
            "progress": 0,
            "color": "#8B5CF6"
        }
    ]
    return JsonResponse({"themes": themes})


@csrf_exempt
def api_questions(request, theme_id):
    """API для получения вопросов по теме"""
    # Примерные вопросы по темам из твоих материалов
    questions_by_theme = {
        1: [
            {
                "id": 1,
                "question": "Что такое кольцо в алгебре?",
                "options": [
                    "Множество с двумя операциями: сложением и умножением",
                    "Множество только с операцией сложения",
                    "Множество только с операцией умножения",
                    "Геометрическая фигура"
                ],
                "correct": 0,
                "explanation": "Кольцо - это алгебраическая структура, состоящая из множества с двумя бинарными операциями: сложением и умножением, удовлетворяющими определённым аксиомам."
            },
            {
                "id": 2,
                "question": "Что такое целостное кольцо?",
                "options": [
                    "Кольцо без делителей нуля",
                    "Кольцо с единицей",
                    "Коммутативное кольцо",
                    "Поле"
                ],
                "correct": 0,
                "explanation": "Целостное кольцо - это коммутативное кольцо без делителей нуля, то есть если произведение двух элементов равно нулю, то один из них обязательно равен нулю."
            }
        ],
        2: [
            {
                "id": 3,
                "question": "Что такое НОД двух чисел?",
                "options": [
                    "Наибольший общий делитель двух чисел",
                    "Наименьшее общее кратное",
                    "Произведение чисел",
                    "Сумма чисел"
                ],
                "correct": 0,
                "explanation": "НОД(a,b) - это наибольший положительный делитель, который делит оба числа a и b нацело."
            }
        ],
        # Можно добавить остальные темы...
    }

    theme_questions = questions_by_theme.get(theme_id, [])
    return JsonResponse({"questions": theme_questions})


@csrf_exempt
def api_save_progress(request):
    """API для сохранения прогресса пользователя (для совместимости)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Здесь можно сохранить дополнительный прогресс в базу данных
            # Основной прогресс уже сохраняется в api_exam_result
            return JsonResponse({
                "success": True,
                "message": "Прогресс сохранён успешно"
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": f"Ошибка сохранения прогресса: {str(e)}"
            })

    return JsonResponse({
        "success": False,
        "error": "Только POST запросы разрешены"
    })
