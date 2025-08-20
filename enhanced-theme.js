// Enhanced theme.js with better mobile support

// Load theme preference from localStorage on page load
document.addEventListener('DOMContentLoaded', function() {
    loadTheme();
});

// Function to load theme from localStorage
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light-theme';
    const htmlElement = document.documentElement;

    // Remove all theme classes
    htmlElement.classList.remove('light-theme', 'dark-theme', 'sepia-theme');

    // Add the saved theme class
    htmlElement.classList.add(savedTheme);
    console.log(`${savedTheme} loaded from localStorage`);
    
    // Update theme toggle icon based on current theme
    updateThemeToggleIcon(savedTheme);
}

// Function to toggle between themes
function toggleTheme() {
    console.log("toggleTheme function called");
    const htmlElement = document.documentElement;
    let newTheme = 'light-theme';

    if (htmlElement.classList.contains('light-theme')) {
        htmlElement.classList.remove('light-theme');
        htmlElement.classList.add('dark-theme');
        newTheme = 'dark-theme';
        console.log("Dark theme activated");
    } else if (htmlElement.classList.contains('dark-theme')) {
        htmlElement.classList.remove('dark-theme');
        htmlElement.classList.add('sepia-theme');
        newTheme = 'sepia-theme';
        console.log("Sepia theme activated");
    } else if (htmlElement.classList.contains('sepia-theme')) {
        htmlElement.classList.remove('sepia-theme');
        htmlElement.classList.add('light-theme');
        newTheme = 'light-theme';
        console.log("Light theme activated");
    } else {
        htmlElement.classList.add('light-theme');
        newTheme = 'light-theme';
        console.log("Light theme activated");
    }

    // Save theme preference to localStorage
    localStorage.setItem('theme', newTheme);
    
    // Update theme toggle icon
    updateThemeToggleIcon(newTheme);
}

// Function to update theme toggle icon based on current theme
function updateThemeToggleIcon(theme) {
    const themeIcon = document.querySelector('.theme-icon');
    if (!themeIcon) return;
    
    switch(theme) {
        case 'light-theme':
            themeIcon.textContent = 'brightness_4'; // Moon icon for light theme
            break;
        case 'dark-theme':
            themeIcon.textContent = 'brightness_5'; // Sun icon for dark theme
            break;
        case 'sepia-theme':
            themeIcon.textContent = 'brightness_6'; // Sun icon for sepia theme
            break;
        default:
            themeIcon.textContent = 'brightness_4';
    }
}