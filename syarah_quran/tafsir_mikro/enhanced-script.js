// Enhanced JavaScript for better performance and mobile support

let currentLanguage = "en";
let allSurahs = []; // Store all surahs for filtering
let isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

// Debounce function to limit search function calls
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

function setLanguage(lang) {
    currentLanguage = lang;
    loadTranslations();
}

function loadTranslations() {
    fetch(`data/${currentLanguage}.json`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(translations => {
            document.querySelectorAll(".back-button").forEach(el => {
                el.innerHTML = `<i class="material-icons">arrow_back</i>${translations.backButton}`;
            });
            document.querySelectorAll(".surah-title").forEach(el => el.textContent = translations.surahTitle);
            document.querySelectorAll(".section-heading").forEach(el => {
                const text = el.textContent;
                if(text == "Key Themes"){
                  el.textContent = translations.keyThemes;
                }
                else if(text == "Detailed Explanation"){
                    el.textContent = translations.detailedExplanation;
                }
                else if(text == "YouTube Videos"){
                    el.textContent = translations.youtubeVideos;
                }
                else if(text == "Other Materials"){
                    el.textContent = translations.otherMaterials;
                }
            });
            document.querySelectorAll(".download-button").forEach(el => {
                const text = el.textContent;
                if(text == "Download Video"){
                    el.textContent = translations.downloadVideo;
                }
                else if(text == "PDF Explanation"){
                    el.textContent = translations.pdfExplanation;
                }
            });
        })
        .catch(error => {
            console.error("Error loading translations:", error);
        });
}

function createSurahGrid() {
    console.log("Creating surah grid");
    // Clear the existing grid
    const surahGrid = document.getElementById("surah-grid");
    if (!surahGrid) {
        console.error("Surah grid element not found");
        return;
    }

    surahGrid.innerHTML = "";

    // Fetch all surahs
    fetch("data/all_surahs.json")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Surahs data loaded successfully");
            allSurahs = data.children; // Store all surahs for filtering later
            displaySurahs(allSurahs);
            setupSearchFunctionality();
            updateDeviceWarning(); // Update device warning based on device type
        })
        .catch(error => {
            console.error("Error loading or processing data:", error);
        });
}

function displaySurahs(surahs) {
    console.log(`Displaying ${surahs.length} surahs`);
    const surahGrid = document.getElementById("surah-grid");

    if (!surahGrid) {
        console.error("Surah grid element not found in displaySurahs");
        return;
    }

    // Clear the grid before displaying new results
    surahGrid.innerHTML = "";

    // Display message if no surahs match the search
    if (surahs.length === 0) {
        const noResults = document.createElement("div");
        noResults.classList.add("no-results", "enhanced");
        noResults.innerHTML = `<i class="material-icons">search_off</i><p>No surahs found matching your search.</p>`;
        surahGrid.appendChild(noResults);
        return;
    }

    surahs.forEach(surah => {
        const surahDiv = document.createElement("div");
        surahDiv.classList.add("surah-item", "enhanced");
        surahDiv.setAttribute("data-surah-number", surah.number);
        surahDiv.setAttribute("data-surah-name", surah.englishName.toLowerCase());
        surahDiv.setAttribute("data-surah-arabic", surah.name);

        const surahNumber = document.createElement("span");
        surahNumber.classList.add("surah-number", "enhanced");
        surahNumber.textContent = surah.number;

        const surahName = document.createElement("span");
        surahName.classList.add("surah-name", "enhanced");
        surahName.textContent = surah.englishName;

        const surahArabicName = document.createElement("span");
        surahArabicName.classList.add("surah-arabic-name", "enhanced");
        surahArabicName.textContent = surah.name;

        const tooltip = document.createElement("div");
        tooltip.classList.add("tooltip", "enhanced");
        tooltip.innerHTML = `
            <span class="tooltip-name enhanced">${surah.englishName}</span>
            <span class="tooltip-number enhanced">(${surah.number})</span>
            <span class="tooltip-type enhanced">(${surah.revelationType})</span>
            <span class="tooltip-translation enhanced">${surah.englishNameTranslation}</span>
            <span class="tooltip-ayahs enhanced">(${surah.numberOfAyahs} Ayahs)</span>
        `;
        document.body.appendChild(tooltip);

        // For mobile devices, show tooltip on click instead of hover
        if (isMobile) {
            surahDiv.addEventListener("click", function(event) {
                // If this is a navigation click (not a tooltip click), proceed with navigation
                if (!tooltip.contains(event.target)) {
                    // Hide all other tooltips
                    document.querySelectorAll(".tooltip.enhanced").forEach(t => {
                        t.style.display = "none";
                    });
                    
                    // Toggle this tooltip
                    if (tooltip.style.display === "block") {
                        tooltip.style.display = "none";
                    } else {
                        const rect = surahDiv.getBoundingClientRect();
                        tooltip.style.display = "block";
                        tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10 + window.scrollY}px`;
                        tooltip.style.left = `${rect.left + rect.width / 2 + window.scrollX}px`;
                        tooltip.style.transform = "translateX(-50%)";
                    }
                }
            });
            
            // Hide tooltip when clicking elsewhere
            document.addEventListener("click", function(event) {
                if (!surahDiv.contains(event.target) && !tooltip.contains(event.target)) {
                    tooltip.style.display = "none";
                }
            });
        } else {
            // Desktop behavior - show tooltip on hover
            surahDiv.addEventListener("mouseover", (event) => {
                tooltip.style.display = "block";
                const surahDivRect = surahDiv.getBoundingClientRect();
                tooltip.style.top = `${surahDivRect.top - tooltip.offsetHeight - 5 + window.scrollY}px`;
                tooltip.style.left = `${surahDivRect.left + surahDivRect.width / 2}px`;
                tooltip.style.transform = "translateX(-50%)";
            });

            surahDiv.addEventListener("mouseout", () => {
                tooltip.style.display = "none";
            });
        }

        surahDiv.addEventListener("click", function(event) {
            // If this is a tooltip click, don't navigate
            if (!tooltip.contains(event.target)) {
                window.location.href = `surah_${surah.number}.html`;
            }
        });

        surahDiv.appendChild(surahNumber);
        surahDiv.appendChild(surahName);
        surahDiv.appendChild(surahArabicName);

        surahGrid.appendChild(surahDiv);
    });
}

function setupSearchFunctionality() {
    const searchInput = document.getElementById("surah-search");
    const clearButton = document.getElementById("clear-search");

    if (!searchInput || !clearButton) {
        console.error("Search elements not found in the DOM");
        return;
    }

    console.log("Setting up search functionality");

    // Show/hide clear button based on input content
    searchInput.addEventListener("input", function() {
        console.log("Search input changed:", this.value);
        if (this.value.length > 0) {
            clearButton.style.display = "flex";
        } else {
            clearButton.style.display = "none";
        }

        // Filter surahs based on search input (debounced)
        debouncedFilterSurahs(this.value.toLowerCase());
    });

    // Clear search input when clear button is clicked
    clearButton.addEventListener("click", function() {
        console.log("Clear button clicked");
        searchInput.value = "";
        clearButton.style.display = "none";
        filterSurahs("");
    });
}

// Debounced version of filterSurahs
const debouncedFilterSurahs = debounce(function(searchTerm) {
    filterSurahs(searchTerm);
}, 300);

function filterSurahs(searchTerm) {
    console.log("Filtering surahs with term:", searchTerm);
    if (!allSurahs || allSurahs.length === 0) {
        console.error("No surahs available for filtering");
        return;
    }

    if (!searchTerm) {
        // If search term is empty, show all surahs
        console.log("Empty search term, showing all surahs");
        displaySurahs(allSurahs);
        return;
    }

    // Filter surahs based on number, English name, or Arabic name
    const filteredSurahs = allSurahs.filter(surah => {
        const numberMatch = surah.number.toString().includes(searchTerm);
        const nameMatch = surah.englishName.toLowerCase().includes(searchTerm);
        const arabicMatch = surah.name.includes(searchTerm);
        const translationMatch = surah.englishNameTranslation.toLowerCase().includes(searchTerm);

        return numberMatch || nameMatch || arabicMatch || translationMatch;
    });

    console.log(`Found ${filteredSurahs.length} surahs matching "${searchTerm}"`);

    // Display filtered surahs
    displaySurahs(filteredSurahs);
}

// Update device warning based on device type
function updateDeviceWarning() {
    const deviceWarning = document.querySelector(".device-warning");
    if (deviceWarning && isMobile) {
        deviceWarning.innerHTML = `
            <i class="material-icons">smartphone</i>
            <span>Mobile optimized version. Enjoy your learning experience!</span>
        `;
        deviceWarning.style.backgroundColor = "#e8f5e9";
        deviceWarning.style.color = "#2e7d32";
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    loadTranslations();
    createSurahGrid();
    
    // Add enhanced classes to existing elements
    enhanceExistingElements();
});

// Function to add enhanced classes to existing elements
function enhanceExistingElements() {
    // Add enhanced classes to search elements
    const searchBox = document.querySelector(".search-box");
    if (searchBox) searchBox.classList.add("enhanced");
    
    const searchIcon = document.querySelector(".search-icon");
    if (searchIcon) searchIcon.classList.add("enhanced");
    
    const searchInput = document.getElementById("surah-search");
    if (searchInput) searchInput.classList.add("enhanced");
    
    const clearButton = document.getElementById("clear-search");
    if (clearButton) clearButton.classList.add("enhanced");
    
    // Add enhanced classes to surah grid
    const surahGrid = document.getElementById("surah-grid");
    if (surahGrid) surahGrid.classList.add("enhanced");
    
    // Add enhanced classes to widgets
    document.querySelectorAll(".widget").forEach(widget => {
        widget.classList.add("enhanced");
        const icon = widget.querySelector(".widget-icon");
        const label = widget.querySelector(".widget-label");
        if (icon) icon.classList.add("enhanced");
        if (label) label.classList.add("enhanced");
    });
    
    // Add enhanced classes to current page widget
    document.querySelectorAll(".widget.current-page").forEach(widget => {
        widget.classList.add("enhanced");
    });
    
    // Add enhanced class to no results if it exists
    const noResults = document.querySelector(".no-results");
    if (noResults) noResults.classList.add("enhanced");
}