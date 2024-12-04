document.addEventListener("DOMContentLoaded", function () {
    // Confirmation before logging out
    const logoutLink = document.querySelector("a[href='/logout']");
    if (logoutLink) {
        logoutLink.addEventListener("click", function (e) {
            // Clear active states on logout
            document.querySelectorAll(".active").forEach(el => el.classList.remove("active"));
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
                message.style.transition = "opacity 0.5s"; // Fade-out effect
                message.style.opacity = "0"; // Make the message transparent
                setTimeout(() => {
                    if (message && message.parentNode) {
                        message.parentNode.remove(); // Remove the message element
                    }
                }, 500); // Wait for fade-out to complete
            }, 3000); // Message visible for 3 seconds
        });
    }

    // Handle achievement-specific notifications
    const achievementNotificationsContainer = document.querySelector(".achievement-notifications");
    if (achievementNotificationsContainer) {
        const achievementNotifications = achievementNotificationsContainer.querySelectorAll(".alert");
        achievementNotifications.forEach((notification) => {
            notification.style.backgroundColor = "#e0ffe0"; // Light green background
            notification.style.color = "#155724"; // Dark green text
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
        answerInput.value = ""; // Clear the input field
    }

    // Hamburger menu toggle with overlay
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");
    const overlay = document.querySelector(".nav-overlay");

    if (menuToggle && navLinks && overlay) {
        menuToggle.addEventListener("click", function () {
            menuToggle.classList.toggle("active");
            navLinks.classList.toggle("active");
            overlay.classList.toggle("active");
        });

        overlay.addEventListener("click", function () {
            menuToggle.classList.remove("active");
            navLinks.classList.remove("active");
            overlay.classList.remove("active");
        });
    }
});