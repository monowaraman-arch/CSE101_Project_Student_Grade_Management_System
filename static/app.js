const searchInput = document.querySelector("#liveSearch");
const studentRows = document.querySelectorAll("[data-student-row]");

if (searchInput && studentRows.length > 0) {
    searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim().toLowerCase();

        studentRows.forEach((row) => {
            const text = row.dataset.search.toLowerCase();
            row.hidden = query !== "" && !text.includes(query);
        });
    });
}

document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
        const message = form.dataset.confirm || "Are you sure?";

        if (!window.confirm(message)) {
            event.preventDefault();
        }
    });
});

const focusedRow = document.querySelector(".is-focused");

if (focusedRow) {
    focusedRow.scrollIntoView({ block: "center", behavior: "smooth" });
}

const studentSelect = document.querySelector("#student_select");
const quizInput = document.querySelector("#quiz_number");

function syncNextTestHint() {
    if (!studentSelect || !quizInput) {
        return;
    }

    const selectedOption = studentSelect.selectedOptions[0];
    const nextTest = selectedOption?.dataset.nextTest;

    if (nextTest) {
        quizInput.placeholder = `Next ${nextTest}`;
    }
}

if (studentSelect && quizInput) {
    studentSelect.addEventListener("change", syncNextTestHint);
    syncNextTestHint();
}
