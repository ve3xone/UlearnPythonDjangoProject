document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("mainContent");
    const toggleButton = document.querySelector(".menu-toggle");

    // Проверяем сохранённое состояние из localStorage
    const savedState = localStorage.getItem("sidebarState");

    // Флаг для отслеживания действий пользователя
    let isUserToggled = false;

    // Устанавливаем начальное состояние панели на основе localStorage
    if (savedState === "closed") {
        sidebar.classList.add("closed");
        mainContent.classList.add("full-width");
        isUserToggled = true;
    } else {
        sidebar.classList.remove("closed");
        mainContent.classList.remove("full-width");
        isUserToggled = false;
    }

    // Открытие/закрытие меню по клику на кнопку
    toggleButton.addEventListener("click", function () {
        event.stopPropagation(); // Предотвращаем всплытие клика
        const isMobile = window.innerWidth <= 768;
    
        if (isMobile) {
            sidebar.classList.toggle("open");
            
            //Убераем скролл
            document.body.classList.toggle("no-scroll", sidebar.classList.contains("open"));
        } else {
            sidebar.classList.toggle("closed");
            mainContent.classList.toggle("full-width");
        
            // Сохраняем текущее состояние в localStorage
            if (sidebar.classList.contains("closed")) {
                localStorage.setItem("sidebarState", "closed");
            } else {
                localStorage.setItem("sidebarState", "open");
            }
        }
    
        // Пользователь изменил состояние вручную
        isUserToggled = true;
    });

    // Управление состоянием при изменении размера окна
    window.addEventListener("resize", function () {
        const isMobile = window.innerWidth <= 768;

        if (!isUserToggled) {
            // Если пользователь не менял состояние вручную, управляем по умолчанию
            if (isMobile) {
                sidebar.classList.add("closed");
                sidebar.classList.remove("open");
                mainContent.classList.add("full-width");
            } else {
                sidebar.classList.remove("closed");
                sidebar.classList.remove("open");
                mainContent.classList.remove("full-width");
            }
        }
        else {
            if (!isMobile) {
                document.body.classList.remove("no-scroll");
            }
            else{
                document.body.classList.add("no-scroll");
            }
        }
    });

    // Установка начального состояния для мобильных устройств
    if (window.innerWidth <= 768) {
        sidebar.classList.add("closed");
        mainContent.classList.add("full-width");
    }
    sidebar.classList.add("loaded"); // После всех операций

    // Закрытие sidebar при клике вне его
    document.addEventListener("click", function (event) {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnToggleButton = toggleButton.contains(event.target);
        const isMobile = window.innerWidth <= 768;

        if (!isClickInsideSidebar && !isClickOnToggleButton && isMobile) {
            sidebar.classList.add("closed");
            sidebar.classList.remove("open");
            mainContent.classList.add("full-width");
            document.body.classList.remove("no-scroll");
        }
    });
});