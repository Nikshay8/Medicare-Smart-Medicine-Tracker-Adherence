const editMedicineForm = document.getElementById("editMedicineForm");
const editMedicineName = document.getElementById("editMedicineName");
const editMedicineHour = document.getElementById("editMedicineHour");
const editMedicineMinute = document.getElementById("editMedicineMinute");
const editMedicinePeriod = document.getElementById("editMedicinePeriod");
const editMedicineError = document.getElementById("editMedicineError");

editMedicineForm.addEventListener("submit", function (event) {
    editMedicineError.textContent = "";

    const nameValue = editMedicineName.value.trim();
    const hourValue = editMedicineHour.value;
    const minuteValue = editMedicineMinute.value;
    const periodValue = editMedicinePeriod.value;

    const medicineNameRegex = /^[a-zA-Z0-9\s]+$/;

    if (nameValue === "" || hourValue === "" || minuteValue === "" || periodValue === "") {
        event.preventDefault();
        editMedicineError.textContent = "All fields are required.";
        return;
    }

    if (nameValue.length < 2 || nameValue.length > 50) {
        event.preventDefault();
        editMedicineError.textContent = "Medicine name must be between 2 and 50 characters.";
        return;
    }

    if (nameValue.replace(/\s/g, "").length === 0) {
        event.preventDefault();
        editMedicineError.textContent = "Medicine name cannot contain only spaces.";
        return;
    }

    if (/^\d+$/.test(nameValue)) {
        event.preventDefault();
        editMedicineError.textContent = "Medicine name cannot be only numbers.";
        return;
    }

    if (!medicineNameRegex.test(nameValue)) {
        event.preventDefault();
        editMedicineError.textContent = "Medicine name can contain only letters, numbers, and spaces.";
        return;
    }
});