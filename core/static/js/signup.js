const signupForm = document.getElementById("signupForm");
const username = document.getElementById("signupUsername");
const email = document.getElementById("signupEmail");
const password = document.getElementById("signupPassword");
const confirmPassword = document.getElementById("signupConfirmPassword");
const signupError = document.getElementById("signupError");

signupForm.addEventListener("submit", function (event) {
    signupError.textContent = "";

    const usernameValue = username.value.trim();
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();
    const confirmPasswordValue = confirmPassword.value.trim();

    const usernameRegex = /^[a-zA-Z0-9_]+$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const hasLetter = /[A-Za-z]/.test(passwordValue);
    const hasNumber = /[0-9]/.test(passwordValue);

    if (
        usernameValue === "" ||
        emailValue === "" ||
        passwordValue === "" ||
        confirmPasswordValue === ""
    ) {
        event.preventDefault();
        signupError.textContent = "All fields are required.";
        return;
    }

    if (usernameValue.length < 3 || usernameValue.length > 20) {
        event.preventDefault();
        signupError.textContent = "Username must be between 3 and 20 characters.";
        return;
    }

    if (!usernameRegex.test(usernameValue)) {
        event.preventDefault();
        signupError.textContent = "Username can contain only letters, numbers, and underscore.";
        return;
    }

    if (!emailRegex.test(emailValue)) {
        event.preventDefault();
        signupError.textContent = "Enter a valid email address.";
        return;
    }

    if (passwordValue.length < 8) {
        event.preventDefault();
        signupError.textContent = "Password must be at least 8 characters long.";
        return;
    }

    if (!hasLetter || !hasNumber) {
        event.preventDefault();
        signupError.textContent = "Password must contain both letters and numbers.";
        return;
    }

    if (passwordValue !== confirmPasswordValue) {
        event.preventDefault();
        signupError.textContent = "Passwords do not match.";
        return;
    }
});