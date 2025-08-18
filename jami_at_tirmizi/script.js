// Jami at-Tirmizi - Kitab Thaharah Session Grid Script

let sessionsData = [];

// Load sessions data from JSON
async function loadSessionsData() {
    try {
        const timestamp = new Date().getTime();
        const response = await fetch(`jami_at_tirmizi.json?t=${timestamp}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        sessionsData = data.sessions;
        console.log(`Loaded ${sessionsData.length} sessions`);
        return true;
    } catch (error) {
        console.error('Error loading sessions data:', error);
        return false;
    }
}

// Create session grid
function createSessionGrid() {
    const grid = document.getElementById('session-grid');
    if (!grid) {
        console.error('Session grid element not found');
        return;
    }

    grid.innerHTML = '';

    sessionsData.forEach(session => {
        const sessionItem = document.createElement('div');
        sessionItem.className = 'session-item';
        sessionItem.onclick = () => openSession(session.session_number);

        sessionItem.innerHTML = `
            <div class="session-number">${session.session_number}</div>
            <div class="session-title">${session.title}</div>
        `;

        grid.appendChild(sessionItem);
    });

    console.log(`Created ${sessionsData.length} session items`);
}

// Open specific session
function openSession(sessionNumber) {
    const filename = `sesi_${sessionNumber}.html`;
    window.location.href = filename;
}

// Initialize the application
async function init() {
    console.log('Initializing Jami at-Tirmizi application...');
    
    const success = await loadSessionsData();
    if (success) {
        createSessionGrid();
        console.log('Application initialized successfully');
    } else {
        console.error('Failed to initialize application');
        // Show error message to user
        const grid = document.getElementById('session-grid');
        if (grid) {
            grid.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #666;">
                    <i class="material-icons" style="font-size: 48px; margin-bottom: 16px;">error_outline</i>
                    <h3>Failed to load sessions</h3>
                    <p>Please check your internet connection and try again.</p>
                    <button onclick="location.reload()" style="margin-top: 16px; padding: 8px 16px; background: #3f51b5; color: white; border: none; border-radius: 4px; cursor: pointer;">Retry</button>
                </div>
            `;
        }
    }
}

// Start the application when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Export for debugging
window.sessionsData = sessionsData;
window.loadSessionsData = loadSessionsData;
window.createSessionGrid = createSessionGrid;