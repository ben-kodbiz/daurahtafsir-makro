let allSessions = [];

function createSessionGrid(sessionsToShow = null) {
    fetch("../data/tutorial_sessions.json")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            allSessions = data.sessions;
            const sessionGrid = document.getElementById("session-grid");
            const sessions = sessionsToShow || allSessions;
            
            sessionGrid.innerHTML = '';
            
            sessions.forEach(session => {
                const sessionDiv = document.createElement("div");
                sessionDiv.classList.add("session-item");

                // Update the click event to point to the correct location:
                sessionDiv.addEventListener("click", () => {
                    window.location.href = `../qawaid_tafsir/session_${session.session_number}.html`;
                });

                const sessionNumber = document.createElement("span");
                sessionNumber.classList.add("session-number");
                sessionNumber.textContent = session.session_number;

                const sessionTitle = document.createElement("span");
                sessionTitle.classList.add("session-title");
                sessionTitle.textContent = session.title;

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
    
    const filteredSessions = allSessions.filter(session => {
        const titleMatch = session.title.toLowerCase().includes(searchTerm);
        const numberMatch = session.session_number.toString().includes(searchTerm);
        return titleMatch || numberMatch;
    });
    
    createSessionGrid(filteredSessions);
}

createSessionGrid();