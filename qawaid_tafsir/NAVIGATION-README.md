# Qawaid Tafsir Navigation Implementation

This document describes the implementation of navigation buttons ("Sesi Sebelumnya" and "Sesi Seterusnya") in the Qawaid Tafsir module session files.

## Overview

All session files in the Qawaid Tafsir module (session_1.html through session_80.html) have been updated to include navigation buttons that allow users to easily move between consecutive sessions.

## Features

### 1. Bidirectional Navigation
- **"Sesi Sebelumnya"** (Previous Session): Navigates to the previous session
- **"Sesi Seterusnya"** (Next Session): Navigates to the next session

### 2. Intelligent Button States
- **First Session** (session_1.html): 
  - "Sesi Sebelumnya" button is disabled (grayed out)
  - "Sesi Seterusnya" button is enabled and links to session_2.html

- **Middle Sessions** (session_2.html through session_79.html):
  - Both buttons are enabled
  - "Sesi Sebelumnya" links to the previous session
  - "Sesi Seterusnya" links to the next session

- **Last Session** (session_80.html):
  - "Sesi Sebelumnya" button is enabled and links to session_79.html
  - "Sesi Seterusnya" button is disabled (grayed out)

### 3. Consistent Design
- Buttons use the same styling as other interactive elements in the unified theme
- Icons from Material Design Icons for visual cues
- Responsive design that works on all device sizes
- Smooth hover effects and transitions

## Implementation Details

### HTML Structure
```html
<!-- Navigation Buttons -->
<div class="navigation-buttons" style="display: flex; justify-content: space-between; margin-top: 20px; padding: 0 20px;">
    <div data-prev-button style="flex: 1; margin-right: 10px;"></div>
    <div data-next-button style="flex: 1; margin-left: 10px;"></div>
</div>
```

### JavaScript Logic
The navigation buttons are dynamically generated using JavaScript:

```javascript
// Session navigation data
const totalSessions = 80;
const currentSession = [CURRENT_SESSION_NUMBER];

// Update navigation buttons
document.addEventListener('DOMContentLoaded', function() {
    const prevButtonContainer = document.querySelector('[data-prev-button]');
    const nextButtonContainer = document.querySelector('[data-next-button]');
    
    if (prevButtonContainer) {
        if (currentSession > 1) {
            prevButtonContainer.innerHTML = `
                <a href="session_${currentSession - 1}.html" class="watch-btn" style="display: flex; align-items: center;">
                    <i class="material-icons">arrow_back</i>
                    <span style="margin-left: 8px;">Sesi Sebelumnya</span>
                </a>
            `;
        } else {
            prevButtonContainer.innerHTML = `
                <button class="watch-btn" style="display: flex; align-items: center; opacity: 0.5;" disabled>
                    <i class="material-icons">arrow_back</i>
                    <span style="margin-left: 8px;">Sesi Sebelumnya</span>
                </button>
            `;
        }
    }
    
    if (nextButtonContainer) {
        if (currentSession < totalSessions) {
            nextButtonContainer.innerHTML = `
                <a href="session_${currentSession + 1}.html" class="watch-btn" style="display: flex; align-items: center;">
                    <span style="margin-right: 8px;">Sesi Seterusnya</span>
                    <i class="material-icons">arrow_forward</i>
                </a>
            `;
        } else {
            nextButtonContainer.innerHTML = `
                <button class="watch-btn" style="display: flex; align-items: center; opacity: 0.5;" disabled>
                    <span style="margin-right: 8px;">Sesi Seterusnya</span>
                    <i class="material-icons">arrow_forward</i>
                </button>
            `;
        }
    }
});
```

## Benefits

1. **Improved User Experience**: Users can easily navigate between sessions without returning to the main index
2. **Consistent Navigation**: All sessions have the same navigation pattern
3. **Accessibility**: Clear visual indicators for enabled/disabled states
4. **Responsive Design**: Works well on mobile, tablet, and desktop devices
5. **Performance**: Lightweight implementation with minimal impact on page load

## Maintenance

The `update_sessions_with_navigation.sh` script can be used to update all session files if needed:
```bash
cd qawaid_tafsir
./update_sessions_with_navigation.sh
```

Backups of original files are automatically created with the `.backup` extension.