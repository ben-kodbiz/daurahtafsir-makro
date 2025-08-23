        function displaySessions(sessionsToShow) {
            const grid = document.getElementById('md-video-grid');
            grid.innerHTML = '';

            if (sessionsToShow.length === 0) {
                grid.innerHTML = '<div class="md-no-results"><i class="material-icons">search_off</i><p>No sessions found</p></div>';
                return;
            }

            let gridHTML = '';
            sessionsToShow.forEach(session => {
                gridHTML += `
                <div class="md-grid-item" data-session="${session.number}">
                    <div class="md-thumbnail-container elevation-2">
                        <img src="https://img.youtube.com/vi/${session.videoId}/mqdefault.jpg" 
                             alt="${session.title}" 
                             class="md-thumbnail" 
                             onerror="this.src='https://placehold.co/320x180?text=No+Thumbnail'">
                        <div class="md-play-overlay">
                            <i class="material-icons md-play-icon">play_arrow</i>
                        </div>
                    </div>
                    <div class="md-session-info">
                        <div class="md-session-chip">
                            <i class="material-icons md-chip-icon">confirmation_number</i>
                            <span class="md-chip-text">Sesi ${session.number}</span>
                        </div>
                        <h3 class="md-session-title">${session.title}</h3>
                        <a href="session${session.number}.html" class="md-watch-button">
                            <i class="material-icons md-button-icon">play_circle_outline</i>
                            <span>Tonton Video</span>
                        </a>
                    </div>
                </div>`;
            });
            grid.innerHTML = gridHTML;
        }

        function filterSessions(searchTerm) {
            if (!searchTerm) return sessions;
            
            return sessions.filter(session => 
                session.number.toString().includes(searchTerm) ||
                session.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                session.description.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }