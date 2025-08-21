let allSessions = [];

function createSessionGrid(sessionsToShow = null) {
    fetch("../../data/tutorial_sessions.json")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            allSessions = data.sessions;
            const sessionGrid = document.getElementById("session-grid");
            let sessions = sessionsToShow || allSessions;
            
            sessionGrid.innerHTML = '';
            
            // Sort sessions by session number to ensure correct order
            sessions.sort((a, b) => a.session_number - b.session_number);
            
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

                // Update the click event to point to the correct location:
                sessionDiv.addEventListener("click", () => {
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
            
            setupSearchFunctionality();
        })
        .catch(error => {
            console.error("Error loading or processing data:", error);
        });
}

function setupSearchFunctionality() {
    const searchInput = document.getElementById('session-search');
    const clearButton = document.getElementById('clear-search');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();
            filterSessions(searchTerm);
            
            clearButton.style.display = searchTerm ? 'flex' : 'none';
        });
    }
    
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            searchInput.value = '';
            filterSessions('');
            this.style.display = 'none';
            searchInput.focus();
        });
    }
}

function filterSessions(searchTerm) {
    if (!searchTerm) {
        createSessionGrid(allSessions);
        return;
    }
    
    // Handle duplicate titles for filtered results too
    const titleCount = {};
    const filteredSessions = allSessions.filter(session => {
        // Create display title for filtering
        let displayTitle;
        if (titleCount[session.title]) {
            titleCount[session.title]++;
            displayTitle = session.title + " (Sesi " + session.session_number + ")";
        } else {
            titleCount[session.title] = 1;
            displayTitle = session.title;
        }
        
        const titleMatch = displayTitle.toLowerCase().includes(searchTerm.toLowerCase());
        const numberMatch = session.session_number.toString().includes(searchTerm);
        return titleMatch || numberMatch;
    });
    
    createSessionGrid(filteredSessions);
}

// Initialize the grid with proper handling of duplicate titles
document.addEventListener('DOMContentLoaded', function() {
    createSessionGrid();
});