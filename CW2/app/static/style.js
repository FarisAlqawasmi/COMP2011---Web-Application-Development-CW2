document.addEventListener("DOMContentLoaded", function () {
    // Confirmation before logging out
    const logoutLink = document.querySelector("a[href='/logout']");
    if (logoutLink) {
        logoutLink.addEventListener("click", function (e) {
            const confirmLogout = confirm("Are you sure you want to log out?");
            if (!confirmLogout) {
                e.preventDefault();
            }
        });
    }

    // Confirmation before deleting the account
    const deleteAccountButton = document.querySelector(".delete-account-btn");
    if (deleteAccountButton) {
        deleteAccountButton.addEventListener("click", function (event) {
            const confirmDelete = confirm(deleteAccountButton.getAttribute("data-confirm"));
            if (confirmDelete) {
                const form = deleteAccountButton.closest("form");
                form.submit();
            } else {
                event.preventDefault();
            }
        });
    }

    // Highlight leaderboard entries
    const leaderboardItems = document.querySelectorAll("ol li");
    leaderboardItems.forEach((item) => {
        item.addEventListener("mouseenter", () => {
            item.style.backgroundColor = "#e0f7fa";
        });
        item.addEventListener("mouseleave", () => {
            item.style.backgroundColor = "";
        });
    });

    // Handle flash messages
    const flashMessagesContainer = document.querySelector(".flash-messages");
    if (flashMessagesContainer) {
        const flashMessages = flashMessagesContainer.querySelectorAll(".alert");
        flashMessages.forEach((message) => {
            setTimeout(() => {
                message.style.transition = "opacity 0.5s";
                message.style.opacity = "0";
                setTimeout(() => {
                    if (message && message.parentNode) {
                        message.parentNode.remove();
                    }
                }, 500);
            }, 3000);
        });
    }

    // Handle achievement-specific notifications
    const achievementNotificationsContainer = document.querySelector(".achievement-notifications");
    if (achievementNotificationsContainer) {
        const achievementNotifications = achievementNotificationsContainer.querySelectorAll(".alert");
        achievementNotifications.forEach((notification) => {
            notification.style.backgroundColor = "#e0ffe0";
            notification.style.color = "#155724";
            notification.style.fontWeight = "bold";

            setTimeout(() => {
                notification.style.transition = "opacity 0.5s";
                notification.style.opacity = "0";
                setTimeout(() => {
                    if (notification && notification.parentNode) {
                        notification.parentNode.remove();
                    }
                }, 500);
            }, 3000);
        });
    }

    // Clear the answer input field on page load
    const answerInput = document.getElementById("answer");
    if (answerInput) {
        answerInput.value = "";
    }

    // Hamburger menu toggle with overlay
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");
    const overlay = document.querySelector(".nav-overlay");

    if (menuToggle && navLinks && overlay) {
        // Toggle menu and overlay
        const toggleMenu = (isActive) => {
            navLinks.classList.toggle("active", isActive);
            menuToggle.classList.toggle("active", isActive);
            overlay.classList.toggle("active", isActive);
            menuToggle.setAttribute("aria-expanded", isActive); // Accessibility
        };

        // Open/close menu when the hamburger icon is clicked
        menuToggle.addEventListener("click", () => {
            toggleMenu(!navLinks.classList.contains("active"));
        });

        // Close menu when overlay is clicked
        overlay.addEventListener("click", () => {
            toggleMenu(false);
        });
    } else {
        console.error("Hamburger menu elements not found in DOM.");
    }
});