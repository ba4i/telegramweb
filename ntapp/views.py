from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Ticket
import json


def miniapp_view(request):
    """Главная страница Mini App"""
    return render(request, 'miniapp/index.html')


@csrf_exempt
def api_tickets(request):
    """API для получения всех билетов"""
    tickets = []
    for ticket in Ticket.objects.all()[:10]:  # Ограничиваем количество
        tickets.append({
            "id": ticket.id,
            "number": ticket.number,
            "question": ticket.question,
            "answer": ticket.answer,
            "theme": ticket.theme or "",
            "source": ticket.source or ""
        })
    return JsonResponse({"tickets": tickets})


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
                    "Наибольшее общее делитель двух чисел",
                    "Наименьшее общее кратное",
                    "Произведение чисел",
                    "Сумма чисел"
                ],
                "correct": 0,
                "explanation": "НОД(a,b) - это наибольший положительный делитель, который делит оба числа a и b нацело."
            }
        ],
        # Добавь остальные темы...
    }

    theme_questions = questions_by_theme.get(theme_id, [])
    return JsonResponse({"questions": theme_questions})


@csrf_exempt
def api_save_progress(request):
    """API для сохранения прогресса пользователя"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Здесь можно сохранить прогресс в базу данных
            # Пока просто возвращаем успех
            return JsonResponse({"success": True, "message": "Прогресс сохранён"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Только POST запросы"})
