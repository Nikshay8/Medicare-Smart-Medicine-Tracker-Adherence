const loginForm = document.getElementById("loginForm");
const loginUsername = document.getElementById("loginUsername");
const loginPassword = document.getElementById("loginPassword");
const loginError = document.getElementById("loginError");

loginForm.addEventListener("submit", function(event) {
    loginError.textContent = "";

    const username = loginUsername.value.trim();
    const password = loginPassword.value.trim();

    const usernameRegex = /^[a-zA-Z0-9_]+$/;

    if (username === "" || password === "") {
        event.preventDefault();
        loginError.textContent = "All fields are required.";
        return;
    }

    if (username.length < 3 || username.length > 20) {
        event.preventDefault();
        loginError.textContent = "Username must be between 3 and 20 characters.";
        return;
    }

    if (!usernameRegex.test(username)) {
        event.preventDefault();
        loginError.textContent = "Invalid username format.";
        return;
    }

    if (password.length < 8) {
        event.preventDefault();
        loginError.textContent = "Password must be at least 8 characters.";
        return;
    }
});