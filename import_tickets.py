import os
import django
import re
from PyPDF2 import PdfReader

# Укажи правильный модуль с настройками, если называется не number_theory_app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'number_theory_app.settings')
django.setup()

from ntapp.models import Ticket  # Если твое приложение называется иначе, замени ntapp

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text

def parse_tickets(text):
    # Каждое "N. Заголовок" считается номером и темой билета, остальной текст — ответ
    pattern = re.compile(r'(\d+)\.\s([^\n]+)\n([\s\S]*?)(?=\n\d+\.|\Z)', re.MULTILINE)
    tickets = []
    for match in pattern.finditer(text):
        number = match.group(1).strip()
        question = match.group(2).strip()
        answer = match.group(3).strip()
        tickets.append({
            'number': number,
            'question': question,
            'answer': answer,
            'theme': '',
            'source': 'pdf'
        })
    return tickets

def import_tickets_from_pdf(filename):
    print(f'Импорт из {filename}...')
    text = extract_text_from_pdf(filename)
    tickets = parse_tickets(text)
    for ticket in tickets:
        Ticket.objects.create(
            number=ticket['number'],
            question=ticket['question'],
            answer=ticket['answer'],
            theme=ticket['theme'],
            source=ticket['source']
        )
    print(f'Импортировано: {len(tickets)}')

if __name__ == '__main__':
    import_tickets_from_pdf('Bilety.pdf')  # замени на актуальное имя, если надо
    import_tickets_from_pdf('Teoriia-chisel-Bilety.pdf')
    # Можно добавить еще вызов для других файлов
