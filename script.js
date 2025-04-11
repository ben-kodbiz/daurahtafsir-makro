let currentLanguage = "en";
let allSurahs = []; // Store all surahs for filtering

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
            document.querySelectorAll(".back-button").forEach(el => el.textContent = translations.backButton);
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
        noResults.classList.add("no-results");
        noResults.innerHTML = `<i class="material-icons">search_off</i><p>No surahs found matching your search.</p>`;
        surahGrid.appendChild(noResults);
        return;
    }

    surahs.forEach(surah => {
        const surahDiv = document.createElement("div");
        surahDiv.classList.add("surah-item");
        surahDiv.setAttribute("data-surah-number", surah.number);
        surahDiv.setAttribute("data-surah-name", surah.englishName.toLowerCase());
        surahDiv.setAttribute("data-surah-arabic", surah.name);

        const surahNumber = document.createElement("span");
        surahNumber.classList.add("surah-number");
        surahNumber.textContent = surah.number;

        const surahName = document.createElement("span");
        surahName.classList.add("surah-name");
        surahName.textContent = surah.englishName;

        const surahArabicName = document.createElement("span");
        surahArabicName.classList.add("surah-arabic-name");
        surahArabicName.textContent = surah.name;

        const tooltip = document.createElement("div");
        tooltip.classList.add("tooltip");
        tooltip.innerHTML = `
            <span class="tooltiptext">
                <span class="tooltip-name">${surah.englishName}</span>
                <span class="tooltip-number">(${surah.number})</span>
                <span class="tooltip-type">(${surah.revelationType})</span>
                <span class="tooltip-translation">${surah.englishNameTranslation}</span>
                <span class="tooltip-ayahs">(${surah.numberOfAyahs} Ayahs)</span>
            </span>
        `;
        document.body.appendChild(tooltip);

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

        surahDiv.addEventListener("click", () => {
            window.location.href = `surah_${surah.number}.html`;
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
            clearButton.style.display = "block";
        } else {
            clearButton.style.display = "none";
        }

        // Filter surahs based on search input
        const searchTerm = this.value.toLowerCase();
        filterSurahs(searchTerm);
    });

    // Clear search input when clear button is clicked
    clearButton.addEventListener("click", function() {
        console.log("Clear button clicked");
        searchInput.value = "";
        clearButton.style.display = "none";
        filterSurahs(""); // Show all surahs
    });
}

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

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    loadTranslations();
    createSurahGrid();
});