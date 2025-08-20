const fs = require('fs');
const path = require('path');

// Kitab data from JSON
const kitabData = [
  {
    "title": "Kitab-Kitab Hadith (PDF)",
    "url": "https://syarahanhadits.school.blog/kitab-kitab-syarah-hadith-pdf/"
  },
  {
    "title": "2. Kitab Wahyu (Kota Bharu)",
    "url": "https://syarahanhadits.school.blog/sahih-al-bukhari-kitab-wahyu/"
  },
  {
    "title": "3. Kitab Iman (Lembah Klang)",
    "url": "https://syarahanhadits.school.blog/kitab-iman-kl/"
  },
  {
    "title": "2. Kitab Wahyu (Lembah Klang)",
    "url": "https://syarahanhadits.school.blog/sahih-bukhari-lembah-klang-kitab-wahyu/"
  },
  {
    "title": "3. Kitab Iman ( Kota Bharu)",
    "url": "https://syarahanhadits.school.blog/kitab-iman-kb-sb/"
  },
  {
    "title": "4. Kitab Ilmu",
    "url": "https://syarahanhadits.school.blog/kitab-ilmu/"
  },
  {
    "title": "4. Kitab Ilmu (Atas Talian)",
    "url": "https://syarahanhadits.school.blog/kitab-ilmu-atas-talian/"
  },
  {
    "title": "5. Kitab Wudhu’",
    "url": "https://syarahanhadits.school.blog/kitab-wudhu-sb/"
  },
  {
    "title": "6. Kitab Mandi Janabah",
    "url": "https://syarahanhadits.school.blog/kitab-mandi-janabah-sb/"
  },
  {
    "title": "7. Kitab Haidh",
    "url": "https://syarahanhadits.school.blog/kitab-haid/"
  },
  {
    "title": "8. Kitab Tayammum",
    "url": "https://syarahanhadits.school.blog/kitab-tayammum/"
  },
  {
    "title": "9. Kitab Sembahyang",
    "url": "https://syarahanhadits.school.blog/kitab-sembahyang-sb/"
  },
  {
    "title": "10. Kitab Waktu-waktu Sembahyang",
    "url": "https://syarahanhadits.school.blog/kitab-waktu2-sembahyang/"
  },
  {
    "title": "11. Kitab Azan",
    "url": "https://syarahanhadits.school.blog/kitab-azan/"
  },
  {
    "title": "12. Kitab Solat Jumaat",
    "url": "https://syarahanhadits.school.blog/kitab-jumaat/"
  },
  {
    "title": "13. Kitab Sembahyang Khauf.",
    "url": "https://syarahanhadits.school.blog/kitab-sembahyang-khauf/"
  },
  {
    "title": "14. Kitab Solat Dua Hari Raya",
    "url": "https://syarahanhadits.school.blog/kitab-sembahyang-dua-hari-raya/"
  },
  {
    "title": "15. Kitab Solat Witir",
    "url": "https://syarahanhadits.school.blog/solat-witr/"
  },
  {
    "title": "17. Kitab Solat Gerhana",
    "url": "https://syarahanhadits.school.blog/kitab-solat-gerhana/"
  },
  {
    "title": "19. Kitab Mengqasarkan Solat",
    "url": "https://syarahanhadits.school.blog/kitab-mengqasarkan-solat/"
  },
  {
    "title": "20. Kitab Solat Malam",
    "url": "https://syarahanhadits.school.blog/kitab-solat-malam/"
  },
  {
    "title": "22. Kitab Perbuatan Dalam Solat",
    "url": "https://syarahanhadits.school.blog/perbuatan-dalam-solat/"
  },
  {
    "title": "23. Kitab Sujud Sahwi",
    "url": "https://syarahanhadits.school.blog/kitab-sujud-sahwi/"
  },
  {
    "title": "24. Kitab Jenazah",
    "url": "https://syarahanhadits.school.blog/kitab-solat-jenazah/"
  },
  {
    "title": "26. Kitab Manaasik",
    "url": "https://syarahanhadits.school.blog/kitab-manasik/"
  },
  {
    "title": "30. Kitab Kelebihan Madinah",
    "url": "https://syarahanhadits.school.blog/kitab-kelebihan-madinah/"
  },
  {
    "title": "31. Kitab Puasa",
    "url": "https://syarahanhadits.school.blog/kitab-puasa/"
  },
  {
    "title": "35. Kitab Jual Beli",
    "url": "https://syarahanhadits.school.blog/kitab-jual-beli-2/"
  },
  {
    "title": "56. Kitab Wasiat",
    "url": "https://syarahanhadits.school.blog/kitab-wasiat/"
  },
  {
    "title": "57. Kitab Jihad",
    "url": "https://syarahanhadits.school.blog/kitab-jihad/"
  },
  {
    "title": "58. Kitab Fardhil Khumus",
    "url": "https://syarahanhadits.school.blog/sahih-bukhari-kota-bharu-kitab-fardhil-khumus/"
  },
  {
    "title": "59. Kitab Jizyah Wal Muwaada’ah",
    "url": "https://syarahanhadits.school.blog/kitab-jizyah-wal-muwaadaah/"
  },
  {
    "title": "60. Kitab Permulaan Kejadian",
    "url": "https://syarahanhadits.school.blog/sahih-al-bukhari-kitab-permulaan-kejadian/"
  },
  {
    "title": "61. Kitab Nabi-Nabi",
    "url": "https://syarahanhadits.school.blog/kitab-kenabian/"
  },
  {
    "title": "62. Kitab Manaqib",
    "url": "https://syarahanhadits.school.blog/kitab-manakib/"
  },
  {
    "title": "63. Kitab Kelebihan Para Sahabat",
    "url": "https://syarahanhadits.school.blog/sahih-bukhari-kota-bharu-kitab-kelebihan-para-sahabat-nabi-saw/"
  },
  {
    "title": "65. Kitab Al-Maghaazi",
    "url": "https://syarahanhadits.school.blog/sahih-bukhari-kitab-al-maghaazi/"
  },
  {
    "title": "70. Kitab Nafqah (Perbelanjaan Keluarga)",
    "url": "https://syarahanhadits.school.blog/kitab-nafkah/"
  },
  {
    "title": "71. Kitab Makanan",
    "url": "https://syarahanhadits.school.blog/kitab-makanan/"
  },
  {
    "title": "72. Kitab Aqiqah",
    "url": "https://syarahanhadits.school.blog/kitab-aqiqah/"
  },
  {
    "title": "73. Kitab Sembelihan & Perburuan",
    "url": "https://syarahanhadits.school.blog/kitab-sembelihan-perburuan/"
  },
  {
    "title": "74. Kitab Qurban",
    "url": "https://syarahanhadits.school.blog/kitab-qurban/"
  },
  {
    "title": "75. Kitab Minuman",
    "url": "https://syarahanhadits.school.blog/kitab-minuman/"
  },
  {
    "title": "76. Kitab Orang-Orang Sakit",
    "url": "https://syarahanhadits.school.blog/kitab-orang-sakit/"
  },
  {
    "title": "77. Kitab Perubatan",
    "url": "https://syarahanhadits.school.blog/kitab-perubatan/"
  },
  {
    "title": "78. Kitab Pakaian",
    "url": "https://syarahanhadits.school.blog/kitab-pakaian/"
  },
  {
    "title": "79. Kitab Adab Kesopanan",
    "url": "https://syarahanhadits.school.blog/kitab-adab-kesopanan/"
  },
  {
    "title": "80. Kitab Minta Izin",
    "url": "https://syarahanhadits.school.blog/kitab-minta-izin/"
  },
  {
    "title": "81. Kitab Doa-Doa",
    "url": "https://syarahanhadits.school.blog/kitab-doa/"
  },
  {
    "title": "82. Kitab Melembutkan Hati",
    "url": "https://syarahanhadits.school.blog/kitab-melembutkan-hati/"
  },
  {
    "title": "83. Kitab Kolam",
    "url": "https://syarahanhadits.school.blog/kitab-kolam/"
  },
  {
    "title": "84. Kitab Taqdir",
    "url": "https://syarahanhadits.school.blog/kitab-taqdir/"
  },
  {
    "title": "85. Kitab Sumpah & Nazar",
    "url": "https://syarahanhadits.school.blog/kitab-sumpah-nazar/"
  },
  {
    "title": "87. Kitab Faraid",
    "url": "https://syarahanhadits.school.blog/kitab-faraid/"
  },
  {
    "title": "88. Kitab Hudud",
    "url": "https://syarahanhadits.school.blog/kitab-hudud/"
  },
  {
    "title": "89. Kitab Diyat",
    "url": "https://syarahanhadits.school.blog/kitab-diyat/"
  },
  {
    "title": "90. Kitab Meminta Pemberontak..",
    "url": "https://syarahanhadits.school.blog/kitab-meminta-pemberontak/"
  },
  {
    "title": "91. Kitab Paksaan",
    "url": "https://syarahanhadits.school.blog/4246-2/"
  },
  {
    "title": "92. Kitab Helah-Helah",
    "url": "https://syarahanhadits.school.blog/4260-2/"
  },
  {
    "title": "93. Kitab Penafsiran Mimpi",
    "url": "https://syarahanhadits.school.blog/kitab-penafsiran-mimpi/"
  },
  {
    "title": "94. Kitab Fitnah-Fitnah",
    "url": "https://syarahanhadits.school.blog/kitab-fitan/"
  },
  {
    "title": "95. Kitab Pemerintahan",
    "url": "https://syarahanhadits.school.blog/kitab-pemerintahan/"
  },
  {
    "title": "96. Kitab Cita-Cita",
    "url": "https://syarahanhadits.school.blog/kitab-solat-khauf/"
  },
  {
    "title": "97. Kitab Hadith Ahad",
    "url": "https://syarahanhadits.school.blog/kitab-hadith-ahad/"
  },
  {
    "title": "98. Kitab Berpegang Teguh",
    "url": "https://syarahanhadits.school.blog/kitab-berpegang-teguh/"
  },
  {
    "title": "99. Kitab Tauhid",
    "url": "https://syarahanhadits.school.blog/kitab-tauhid/"
  }
];

// Function to normalize title for directory name
function normalizeTitleForDirectory(title) {
  // Remove numbers and prefixes like "1. ", "2. ", etc.
  return title
    .replace(/^\\d+\\.\\s*/, '') // Remove leading numbers with dot
    .replace(/\\s+/g, '_') // Replace spaces with underscores
    .replace(/[^\\w\\-_]/g, '') // Remove special characters except hyphens and underscores
    .toLowerCase();
}

// Create mapping of titles to local directory paths
const titleToDirectoryMap = {};
kitabData.forEach(kitab => {
  const normalizedTitle = normalizeTitleForDirectory(kitab.title);
  const directoryName = `sahih_bukhari_${normalizedTitle}`;
  titleToDirectoryMap[kitab.title] = directoryName;
});

// Add special mappings for cases where the directory name differs
titleToDirectoryMap["3. Kitab Iman (Lembah Klang)"] = "sahih_bukhari_kitab_iman_lembah_klang";
titleToDirectoryMap["11. Kitab Azan"] = "sahih_bukhari_kitab_azan";
titleToDirectoryMap["12. Kitab Solat Jumaat"] = "sahih_bukhari_kitab_solat_jumaat";

// Print the mapping for verification
console.log("Title to Directory Mapping:");
Object.keys(titleToDirectoryMap).forEach(title => {
  console.log(`${title} -> ${titleToDirectoryMap[title]}`);
});

// Export the mapping for use in updating the index.html
console.log("\\nMapping Object for index.html:");
console.log(JSON.stringify(titleToDirectoryMap, null, 2));