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
                // If confirmed, submit the form programmatically
                const form = deleteAccountButton.closest("form");
                form.submit();
            } else {
                // Prevent form submission if the user cancels
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
            // Default behavior for normal flash messages
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
            // Add achievement-specific styles
            notification.style.backgroundColor = "#e0ffe0"; // Light green background
            notification.style.color = "#155724"; // Dark green text
            notification.style.fontWeight = "bold";

            // Fade-out effect and removal after 3 seconds
            setTimeout(() => {
                notification.style.transition = "opacity 0.5s"; // Fade-out effect
                notification.style.opacity = "0"; // Make the notification transparent
                setTimeout(() => {
                    if (notification && notification.parentNode) {
                        notification.parentNode.remove(); // Remove the notification element
                    }
                }, 500); // Wait for fade-out to complete
            }, 3000); // Notification visible for 3 seconds
        });
    }

    // Clear the answer input field on page load
    const answerInput = document.getElementById("answer");
    if (answerInput) {
        answerInput.value = ""; // Clear the input field
    }
});