// Функция загрузки случайных вопросов для экзамена
async function startExam() {
    try {
        showScreen('examScreen');

        // Загружаем вопросы с API
        const response = await fetch('/api/tickets/');
        const data = await response.json();

        if (data.tickets && data.tickets.length > 0) {
            // Перемешиваем билеты и берём первые 10
            const shuffled = data.tickets.sort(() => 0.5 - Math.random());
            const examQuestions = shuffled.slice(0, 10);

            // Запускаем экзамен
            currentExam = {
                questions: examQuestions,
                currentQuestion: 0,
                correctAnswers: 0,
                streak: 0
            };

            showNextQuestion();
        } else {
            alert('Ошибка: не удалось загрузить вопросы');
        }
    } catch (error) {
        console.error('Ошибка загрузки экзамена:', error);
        alert('Ошибка подключения к серверу');
    }
}

// Функция отображения вопроса
function showNextQuestion() {
    if (!currentExam || currentExam.currentQuestion >= currentExam.questions.length) {
        showExamResults();
        return;
    }

    const question = currentExam.questions[currentExam.currentQuestion];

    // Обновляем интерфейс
    document.getElementById('questionNumber').textContent = `Вопрос ${currentExam.currentQuestion + 1}`;
    document.getElementById('questionText').textContent = question.question;
    document.getElementById('questionProgress').textContent = `${currentExam.currentQuestion + 1}/${currentExam.questions.length}`;

    // Создаём варианты ответов (правильный + 3 неправильных)
    const options = [
        question.answer, // правильный ответ
        "Неправильный вариант 1",
        "Неправильный вариант 2",
        "Неправильный вариант 3"
    ];

    // Перемешиваем варианты
    const shuffledOptions = options.sort(() => 0.5 - Math.random());
    currentExam.correctIndex = shuffledOptions.indexOf(question.answer);

    // Отображаем кнопки ответов
    const optionsContainer = document.getElementById('examOptions');
    optionsContainer.innerHTML = '';

    shuffledOptions.forEach((option, index) => {
        const button = document.createElement('button');
        button.className = 'exam-option';
        button.textContent = option;
        button.onclick = () => selectAnswer(index);
        optionsContainer.appendChild(button);
    });

    // Запускаем таймер (30 секунд)
    startTimer(30);
}

// Добавь в HTML элементы для экзамена
function selectAnswer(selectedIndex) {
    const isCorrect = selectedIndex === currentExam.correctIndex;

    if (isCorrect) {
        currentExam.correctAnswers++;
        currentExam.streak++;
    } else {
        currentExam.streak = 0;
    }

    currentExam.currentQuestion++;
    setTimeout(showNextQuestion, 1000);
}
