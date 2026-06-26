const caregiverForm = document.getElementById("caregiverForm");
const caregiverName = document.getElementById("caregiverName");
const caregiverEmail = document.getElementById("caregiverEmail");
const caregiverError = document.getElementById("caregiverError");

caregiverForm.addEventListener("submit", function (event) {
    caregiverError.textContent = "";

    const nameValue = caregiverName.value.trim();
    const emailValue = caregiverEmail.value.trim();

    const nameRegex = /^[a-zA-Z\s]+$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (nameValue === "" || emailValue === "") {
        event.preventDefault();
        caregiverError.textContent = "All fields are required.";
        return;
    }

    if (nameValue.length < 2 || nameValue.length > 50) {
        event.preventDefault();
        caregiverError.textContent = "Name must be between 2 and 50 characters.";
        return;
    }

    if (!nameRegex.test(nameValue)) {
        event.preventDefault();
        caregiverError.textContent = "Name can contain only letters and spaces.";
        return;
    }

    if (/^\d+$/.test(nameValue)) {
        event.preventDefault();
        caregiverError.textContent = "Name cannot be only numbers.";
        return;
    }

    if (!emailRegex.test(emailValue)) {
        event.preventDefault();
        caregiverError.textContent = "Enter a valid email address.";
        return;
    }
});