// Инициализация Telegram Web App
let tg = window.Telegram.WebApp;
tg.expand();

// Получение данных пользователя из Telegram
let user = tg.initDataUnsafe?.user;

// Загрузка данных с Django API
async function loadThemes() {
    try {
        const response = await fetch(window.API.themes);
        const data = await response.json();
        return data.themes;
    } catch (error) {
        console.error('Ошибка загрузки тем:', error);
        return [];
    }
}

async function loadQuestions(themeId) {
    try {
        const response = await fetch(window.API.questions + themeId + '/');
        const data = await response.json();
        return data.questions;
    } catch (error) {
        console.error('Ошибка загрузки вопросов:', error);
        return [];
    }
}

// Инициализация приложения
document.addEventListener('DOMContentLoaded', async function() {
    if (user) {
        document.getElementById('username').textContent =
            user.first_name || 'Студент ВШЭ';
    }

    const themes = await loadThemes();
    renderThemes(themes);
});

// ... остальной код приложения
