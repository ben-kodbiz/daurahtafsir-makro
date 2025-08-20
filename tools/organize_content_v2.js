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

// Get all existing directories
const sourceBasePath = '/data/work/dev/daurahtafsir-makro/syarah_hadis/syarah_kitab_bukhari';
const destBasePath = '/data/work/dev/daurahtafsir-makro/syarah_hadis/syarah_kitab_bukhari_new';

const existingDirectories = fs.readdirSync(sourceBasePath, { withFileTypes: true })
  .filter(dirent => dirent.isDirectory() && dirent.name.startsWith('sahih_bukhari_kitab_') && dirent.name !== 'sahih_bukhari_kitab_bukhari_new')
  .map(dirent => dirent.name);

console.log(`Found ${existingDirectories.length} existing kitab directories`);

// Create a mapping of existing directories to JSON titles
const directoryMapping = {};

// For each existing directory, try to find a matching JSON title
existingDirectories.forEach(dir => {
  const dirName = dir.replace('sahih_bukhari_kitab_', '');
  
  // Try to find an exact match first
  for (let i = 0; i < kitabData.length; i++) {
    const kitab = kitabData[i];
    const normalizedTitle = kitab.title
      .replace(/^\\d+\\.\\s*/, '')
      .replace(/\\s+/g, '_')
      .replace(/[^\\w\\-_]/g, '')
      .toLowerCase();
      
    if (normalizedTitle === dirName) {
      directoryMapping[dir] = {
        jsonIndex: i,
        title: kitab.title,
        url: kitab.url,
        matchedType: 'exact'
      };
      return;
    }
  }
  
  // Try partial matching
  for (let i = 0; i < kitabData.length; i++) {
    const kitab = kitabData[i];
    const normalizedTitle = kitab.title
      .replace(/^\\d+\\.\\s*/, '')
      .replace(/\\s+/g, '_')
      .replace(/[^\\w\\-_]/g, '')
      .toLowerCase();
      
    if (normalizedTitle.includes(dirName) || dirName.includes(normalizedTitle)) {
      directoryMapping[dir] = {
        jsonIndex: i,
        title: kitab.title,
        url: kitab.url,
        matchedType: 'partial'
      };
      return;
    }
  }
  
  // If no match found, mark as unmatched
  directoryMapping[dir] = {
    jsonIndex: -1,
    title: dir,
    url: '',
    matchedType: 'unmatched'
  };
});

// Show matching results
console.log('\nDirectory mapping results:');
Object.keys(directoryMapping).forEach(dir => {
  const mapping = directoryMapping[dir];
  if (mapping.matchedType === 'exact') {
    console.log(`${dir} -> ${mapping.title} (EXACT MATCH)`);
  } else if (mapping.matchedType === 'partial') {
    console.log(`${dir} -> ${mapping.title} (PARTIAL MATCH)`);
  } else {
    console.log(`${dir} -> UNMATCHED`);
  }
});

// Now create the new structure based on JSON order
kitabData.forEach((kitab, index) => {
  const normalizedTitle = kitab.title
    .replace(/^\\d+\\.\\s*/, '')
    .replace(/\\s+/g, '_')
    .replace(/[^\\w\\-_]/g, '')
    .toLowerCase();
    
  const newDirName = `sahih_bukhari_${normalizedTitle}`;
  const newDirPath = path.join(destBasePath, newDirName);
  
  // Create the directory
  fs.mkdirSync(newDirPath, { recursive: true });
  
  // Try to find an existing directory that matches this kitab
  let foundDir = null;
  for (const [existingDir, mapping] of Object.entries(directoryMapping)) {
    if (mapping.jsonIndex === index) {
      foundDir = existingDir;
      break;
    }
  }
  
  // If we found a matching existing directory, copy its contents
  if (foundDir) {
    const sourceDir = path.join(sourceBasePath, foundDir);
    const files = fs.readdirSync(sourceDir);
    files.forEach(file => {
      const sourceFile = path.join(sourceDir, file);
      const destFile = path.join(newDirPath, file);
      
      // Copy file
      const fileContent = fs.readFileSync(sourceFile);
      fs.writeFileSync(destFile, fileContent);
    });
    
    console.log(`Copied ${files.length} files from ${foundDir} to ${newDirName}`);
  } else {
    console.log(`Created empty directory for ${newDirName} (no existing content)`);
  }
});

// Copy index.html from source to destination
const sourceIndex = path.join(sourceBasePath, 'index.html');
const destIndex = path.join(destBasePath, 'index.html');

if (fs.existsSync(sourceIndex)) {
  const indexContent = fs.readFileSync(sourceIndex);
  fs.writeFileSync(destIndex, indexContent);
  console.log('Copied index.html');
}

console.log('\nReorganization complete!');