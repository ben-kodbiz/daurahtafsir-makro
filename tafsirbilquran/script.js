function createSessionGrid() {
    const sessionGrid = document.getElementById("session-grid");
    const sessionFiles = [];
    for (let i = 1; i <= 80; i++) {
        sessionFiles.push(`session_${i}.html`);
    }

    sessionFiles.forEach(filename => {
        const sessionNumber = filename.match(/session_(\d+)\.html/)[1];
        const sessionDiv = document.createElement("div");
        sessionDiv.classList.add("session-item");
        sessionDiv.addEventListener("click", () => {
            window.location.href = filename;
        });
        const sessionNumberSpan = document.createElement("span");
        sessionNumberSpan.classList.add("session-number");
        sessionNumberSpan.textContent = sessionNumber;

         const sessionTitleSpan = document.createElement("span");
        sessionTitleSpan.classList.add("session-title");
        sessionTitleSpan.textContent = `Session ${sessionNumber}`;

        sessionDiv.appendChild(sessionNumberSpan);
        sessionDiv.appendChild(sessionTitleSpan);
        sessionGrid.appendChild(sessionDiv);
    });
}
createSessionGrid();