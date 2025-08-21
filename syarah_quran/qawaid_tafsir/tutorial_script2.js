function createSessionGrid() {
    fetch("../../data/tutorial_sessions.json")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const sessionGrid = document.getElementById("session-grid");
            const sessions = data.sessions;
            
            // Handle duplicate titles by appending session number
            const titleCount = {};
            sessions.forEach(session => {
                if (titleCount[session.title]) {
                    titleCount[session.title]++;
                    // Create unique title by appending session number
                    session.displayTitle = session.title + " (Sesi " + session.session_number + ")";
                } else {
                    titleCount[session.title] = 1;
                    session.displayTitle = session.title;
                }
            });
            
            sessions.forEach(session => {
                const sessionDiv = document.createElement("div");
                 sessionDiv.classList.add("session-item");
                 sessionDiv.addEventListener("click", () => {
                     // Replace this with your desired action
                    console.log("clicked session number " + session.session_number);
                     window.location.href = `session_${session.session_number}.html`;
                });

                const sessionNumber = document.createElement("span");
                sessionNumber.classList.add("session-number");
                sessionNumber.textContent = session.session_number;

                const sessionTitle = document.createElement("span");
                sessionTitle.classList.add("session-title");
                sessionTitle.textContent = session.displayTitle;

                sessionDiv.appendChild(sessionNumber);
                sessionDiv.appendChild(sessionTitle);
                sessionGrid.appendChild(sessionDiv);
            });

        })
        .catch(error => {
             console.error("Error loading or processing data:", error);
        });
}

// Initialize the grid with proper handling of duplicate titles
document.addEventListener('DOMContentLoaded', function() {
    createSessionGrid();
});