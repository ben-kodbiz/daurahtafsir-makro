const fs = require('fs');
const path = require('path');

// Manual mapping based on our earlier analysis
const directoryMapping = {
  'sahih_bukhari_kitab_adab_kesopanan': '79. Kitab Adab Kesopanan',
  'sahih_bukhari_kitab_al_maghaazi': '65. Kitab Al-Maghaazi',
  'sahih_bukhari_kitab_aqiqah': '72. Kitab Aqiqah',
  'sahih_bukhari_kitab_azan_edisi2': '11. Kitab Azan',
  'sahih_bukhari_kitab_berpegang_teguh': '98. Kitab Berpegang Teguh',
  'sahih_bukhari_kitab_cita_cita': '96. Kitab Cita-Cita',
  'sahih_bukhari_kitab_diyat': '89. Kitab Diyat',
  'sahih_bukhari_kitab_doa_doa': '81. Kitab Doa-Doa',
  'sahih_bukhari_kitab_faraid': '87. Kitab Faraid',
  'sahih_bukhari_kitab_fardhil_khumus': '58. Kitab Fardhil Khumus',
  'sahih_bukhari_kitab_fitan': '94. Kitab Fitnah-Fitnah',
  'sahih_bukhari_kitab_hadith_ahad': '97. Kitab Hadith Ahad',
  'sahih_bukhari_kitab_haidh': '7. Kitab Haidh',
  'sahih_bukhari_kitab_hibah': 'Kitab Hibah',
  'sahih_bukhari_kitab_hudud': '88. Kitab Hudud',
  'sahih_bukhari_kitab_ilmu': '4. Kitab Ilmu',
  'sahih_bukhari_kitab_iman': '3. Kitab Iman (Lembah Klang)',
  'sahih_bukhari_kitab_jenazah': '24. Kitab Jenazah',
  'sahih_bukhari_kitab_jihad': '57. Kitab Jihad',
  'sahih_bukhari_kitab_jizyah_wal_muwaadaah': '59. Kitab Jizyah Wal Muwaada’ah',
  'sahih_bukhari_kitab_jual_beli': '35. Kitab Jual Beli',
  'sahih_bukhari_kitab_kelebihan_madinah': '30. Kitab Kelebihan Madinah',
  'sahih_bukhari_kitab_kelebihan_para_sahabat': '63. Kitab Kelebihan Para Sahabat',
  'sahih_bukhari_kitab_kolam': '83. Kitab Kolam',
  'sahih_bukhari_kitab_makanan': '71. Kitab Makanan',
  'sahih_bukhari_kitab_manaqib': '62. Kitab Manaqib',
  'sahih_bukhari_kitab_mandi_janabah': '6. Kitab Mandi Janabah',
  'sahih_bukhari_kitab_melembutkan_hati': '82. Kitab Melembutkan Hati',
  'sahih_bukhari_kitab_meminta_pemberontak': '90. Kitab Meminta Pemberontak..',
  'sahih_bukhari_kitab_mengqasarkan_solat': '19. Kitab Mengqasarkan Solat',
  'sahih_bukhari_kitab_minta_izin': '80. Kitab Minta Izin',
  'sahih_bukhari_kitab_minuman': '75. Kitab Minuman',
  'sahih_bukhari_kitab_nafqah': '70. Kitab Nafqah (Perbelanjaan Keluarga)',
  'sahih_bukhari_kitab_orang_sakit': '76. Kitab Orang-Orang Sakit',
  'sahih_bukhari_kitab_pakaian': '78. Kitab Pakaian',
  'sahih_bukhari_kitab_paksaan': '91. Kitab Paksaan',
  'sahih_bukhari_kitab_pemerintahan': '95. Kitab Pemerintahan',
  'sahih_bukhari_kitab_penafsiran_mimpi': '93. Kitab Penafsiran Mimpi',
  'sahih_bukhari_kitab_perbuatan_dalam_solat': '22. Kitab Perbuatan Dalam Solat',
  'sahih_bukhari_kitab_permulaan_kejadian': '60. Kitab Permulaan Kejadian',
  'sahih_bukhari_kitab_perubatan': '77. Kitab Perubatan',
  'sahih_bukhari_kitab_puasa': '31. Kitab Puasa',
  'sahih_bukhari_kitab_qurban': '74. Kitab Qurban',
  'sahih_bukhari_kitab_sembahyang': '9. Kitab Sembahyang',
  'sahih_bukhari_kitab_sembahyang_khauf': '13. Kitab Sembahyang Khauf.',
  'sahih_bukhari_kitab_sembelihan_perburuan': '73. Kitab Sembelihan & Perburuan',
  'sahih_bukhari_kitab_solat': '12. Kitab Solat Jumaat',
  'sahih_bukhari_kitab_solat_dua_hari_raya': '14. Kitab Solat Dua Hari Raya',
  'sahih_bukhari_kitab_solat_gerhana': '17. Kitab Solat Gerhana',
  'sahih_bukhari_kitab_solat_jumaat': '12. Kitab Solat Jumaat',
  'sahih_bukhari_kitab_solat_malam': '20. Kitab Solat Malam',
  'sahih_bukhari_kitab_solat_witir': '15. Kitab Solat Witir',
  'sahih_bukhari_kitab_sujud_sahwi': '23. Kitab Sujud Sahwi',
  'sahih_bukhari_kitab_taqdir': '84. Kitab Taqdir',
  'sahih_bukhari_kitab_tauhid': '99. Kitab Tauhid',
  'sahih_bukhari_kitab_tayammum': '8. Kitab Tayammum',
  'sahih_bukhari_kitab_wahyu': '2. Kitab Wahyu (Kota Bharu)',
  'sahih_bukhari_kitab_waktu_sembahyang': '10. Kitab Waktu-waktu Sembahyang',
  'sahih_bukhari_kitab_wasiat': '56. Kitab Wasiat',
  'sahih_bukhari_kitab_wudhu': '5. Kitab Wudhu'
};

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

// Source and destination paths
const sourceBasePath = '/data/work/dev/daurahtafsir-makro/syarah_hadis/syarah_kitab_bukhari';
const destBasePath = '/data/work/dev/daurahtafsir-makro/syarah_hadis/syarah_kitab_bukhari_new';

// Create destination directory if it doesn't exist
if (!fs.existsSync(destBasePath)) {
  fs.mkdirSync(destBasePath, { recursive: true });
}

// First, copy all existing directories that have mappings
console.log('Copying mapped directories...');
Object.keys(directoryMapping).forEach(sourceDir => {
  const sourcePath = path.join(sourceBasePath, sourceDir);
  
  // Check if source directory exists
  if (fs.existsSync(sourcePath)) {
    // Create directory name based on JSON title
    const jsonTitle = directoryMapping[sourceDir];
    const normalizedTitle = jsonTitle
      .replace(/^\d+\.\s*/, '') // Remove leading numbers with dot
      .replace(/\s+/g, '_') // Replace spaces with underscores
      .replace(/[^\w\-_]/g, '') // Remove special characters except hyphens and underscores
      .toLowerCase();
      
    const destDirName = `sahih_bukhari_${normalizedTitle}`;
    const destPath = path.join(destBasePath, destDirName);
    
    // Create destination directory
    fs.mkdirSync(destPath, { recursive: true });
    
    // Copy all files from source to destination
    const files = fs.readdirSync(sourcePath);
    files.forEach(file => {
      const sourceFile = path.join(sourcePath, file);
      const destFile = path.join(destPath, file);
      
      // Copy file
      const fileContent = fs.readFileSync(sourceFile);
      fs.writeFileSync(destFile, fileContent);
    });
    
    console.log(`Copied ${files.length} files from ${sourceDir} to ${destDirName}`);
  } else {
    console.log(`Source directory ${sourceDir} does not exist`);
  }
});

// Then, create directories for JSON entries that don't have existing content
console.log('Creating directories for unmapped JSON entries...');
kitabData.forEach(kitab => {
  // Check if this JSON entry was already handled in the mapping
  const isMapped = Object.values(directoryMapping).includes(kitab.title);
  
  if (!isMapped) {
    // Create directory name based on JSON title
    const normalizedTitle = kitab.title
      .replace(/^\d+\.\s*/, '') // Remove leading numbers with dot
      .replace(/\s+/g, '_') // Replace spaces with underscores
      .replace(/[^\w\-_]/g, '') // Remove special characters except hyphens and underscores
      .toLowerCase();
      
    const destDirName = `sahih_bukhari_${normalizedTitle}`;
    const destPath = path.join(destBasePath, destDirName);
    
    // Create empty directory
    fs.mkdirSync(destPath, { recursive: true });
    console.log(`Created empty directory for ${destDirName}`);
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

console.log('Organization complete!');