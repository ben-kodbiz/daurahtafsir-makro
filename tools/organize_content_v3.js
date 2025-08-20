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

// Source and destination paths
const sourceBasePath = '/data/work/dev/daurahtafsir-makro/syarah_hadis/syarah_kitab_bukhari';
const destBasePath = '/data/work/dev/daurahtafsir-makro/syarah_hadis/syarah_kitab_bukhari_new';

// Create destination directory if it doesn't exist
if (!fs.existsSync(destBasePath)) {
  fs.mkdirSync(destBasePath, { recursive: true });
}

// Process each mapped directory
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

// Copy index.html from source to destination
const sourceIndex = path.join(sourceBasePath, 'index.html');
const destIndex = path.join(destBasePath, 'index.html');

if (fs.existsSync(sourceIndex)) {
  const indexContent = fs.readFileSync(sourceIndex);
  fs.writeFileSync(destIndex, indexContent);
  console.log('Copied index.html');
}

console.log('Organization complete!');