const medicineForm = document.getElementById("medicineForm");
const medicineName = document.getElementById("medicineName");
const medicineHour = document.getElementById("medicineHour");
const medicineMinute = document.getElementById("medicineMinute");
const medicinePeriod = document.getElementById("medicinePeriod");
const medicineError = document.getElementById("medicineError");

medicineForm.addEventListener("submit", function (event) {
    medicineError.textContent = "";

    const nameValue = medicineName.value.trim();
    const hourValue = medicineHour.value;
    const minuteValue = medicineMinute.value;
    const periodValue = medicinePeriod.value;

    const medicineNameRegex = /^[a-zA-Z0-9\s]+$/;

    if (nameValue === "" || hourValue === "" || minuteValue === "" || periodValue === "") {
        event.preventDefault();
        medicineError.textContent = "All fields are required.";
        return;
    }

    if (nameValue.length < 2 || nameValue.length > 50) {
        event.preventDefault();
        medicineError.textContent = "Medicine name must be between 2 and 50 characters.";
        return;
    }

    if (nameValue.replace(/\s/g, "").length === 0) {
        event.preventDefault();
        medicineError.textContent = "Medicine name cannot contain only spaces.";
        return;
    }

    if (/^\d+$/.test(nameValue)) {
        event.preventDefault();
        medicineError.textContent = "Medicine name cannot be only numbers.";
        return;
    }

    if (!medicineNameRegex.test(nameValue)) {
        event.preventDefault();
        medicineError.textContent = "Medicine name can contain only letters, numbers, and spaces.";
        return;
    }

    if (hourValue === "" || minuteValue === "" || periodValue === "") {
        event.preventDefault();
        medicineError.textContent = "Please select a valid medicine time.";
        return;
    }
});