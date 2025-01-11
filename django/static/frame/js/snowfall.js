const snowflakesContainer = document.getElementById('snowflakes');
const ground = document.getElementById('ground'); // Контейнер для снега на земле
const snowflakesCount = 50; // Количество снежинок
const snowflakeSymbols = ['❄', '✻', '✼', '*']; // Символы снежинок

// Функция создания падающей снежинки
function createSnowflake() {
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');
    snowflake.textContent = snowflakeSymbols[Math.floor(Math.random() * snowflakeSymbols.length)];
    snowflake.style.left = Math.random() * window.innerWidth + 'px';
    snowflake.style.fontSize = 10 + Math.random() * 20 + 'px'; // Размер снежинок
    snowflake.style.opacity = Math.random();
    snowflakesContainer.appendChild(snowflake);

    // Анимация падения
    const fallDuration = 2 + Math.random() * 5; // Скорость падения
    snowflake.style.animation = `fall ${fallDuration}s linear forwards`;

    // Проверка на достижение земли
    const checkGroundInterval = setInterval(() => {
        const snowflakeRect = snowflake.getBoundingClientRect();
        const groundRect = ground.getBoundingClientRect();

        if (snowflakeRect.bottom >= groundRect.top) {
            clearInterval(checkGroundInterval); // Остановка проверки
            addToGround(snowflake); // Добавление на землю
        }
    }, 100);

    // Удаление снежинки, если она тает
    setTimeout(() => {
        meltSnowflake(snowflake);
    }, (fallDuration + 2) * 1000); // Учитываем время падения + 2 секунды на таяние
}

// Функция таяния снежинки
function meltSnowflake(snowflake) {
    snowflake.style.opacity = 0; // Плавное исчезновение
    snowflake.style.transform = 'scale(0)'; // Уменьшение размера
    setTimeout(() => snowflake.remove(), 2000); // Удаление после завершения эффекта
}

// Добавление снежинки на землю
function addToGround(snowflake) {
    const newSnowflake = document.createElement('div');
    newSnowflake.classList.add('ground-snowflake');
    newSnowflake.textContent = snowflake.textContent;
    newSnowflake.style.left = snowflake.style.left;
    newSnowflake.style.fontSize = snowflake.style.fontSize;
    newSnowflake.style.bottom = Math.random() * 20 + 'px';

    ground.appendChild(newSnowflake);
    setTimeout(() => meltSnowflake(newSnowflake), 10000);
}

// Запуск создания снежинок
function startSnowfall() {
    setInterval(createSnowflake, 200);
}

// Анимация через CSS
const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = `
    @keyframes fall {
        0% {
            transform: translateY(0);
        }
        100% {
            transform: translateY(100vh);
        }
    }
`;
document.head.appendChild(styleSheet);

// Запускаем снег
startSnowfall();