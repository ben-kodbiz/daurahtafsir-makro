let currentLanguage = "en";

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
    fetch("data/all_surahs.json")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const surahGrid = document.getElementById("surah-grid");
             const surahs = data.children;
            surahs.forEach(surah => {
                const surahDiv = document.createElement("div");
                 surahDiv.classList.add("surah-item");
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

        })
        .catch(error => {
             console.error("Error loading or processing data:", error);
        });

}

// Load translations on page load
loadTranslations();
createSurahGrid();