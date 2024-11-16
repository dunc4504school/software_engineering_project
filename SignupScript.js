// script.js
document.getElementById("signup-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const errorMessage = document.getElementById("error-message");

    if (!username || !email || !password || !confirmPassword) {
        errorMessage.textContent = "Please fill in all fields.";
        return;
    }

    if (password !== confirmPassword) {
        errorMessage.textContent = "Passwords do not match.";
        return;
    }

    errorMessage.textContent = "";
    alert("Sign-up successful!");

    // Redirect to the profile setup page after sign-up
    window.location.href = "profile.html"; // This is the profile setup page
});

