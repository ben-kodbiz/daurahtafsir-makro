const fs = require('fs');
const path = require('path');

// Mapping of backup directories to new directories
const directoryMapping = {
  // Iman
  'sahih_bukhari_kitab_iman': 'sahih_bukhari_kitab_iman_lembah_klang',
  
  // Azan
  'sahih_bukhari_kitab_azan_edisi2': 'sahih_bukhari_kitab_azan',
  
  // Solat-related
  'sahih_bukhari_kitab_solat': 'sahih_bukhari_kitab_solat_jumaat',
  'sahih_bukhari_kitab_solat_jumaat': 'sahih_bukhari_kitab_solat_jumaat',
  'sahih_bukhari_kitab_solat_dua_hari_raya': 'sahih_bukhari_kitab_solat_dua_hari_raya',
  'sahih_bukhari_kitab_solat_gerhana': 'sahih_bukhari_kitab_solat_gerhana',
  'sahih_bukhari_kitab_solat_malam': 'sahih_bukhari_kitab_solat_malam',
  'sahih_bukhari_kitab_solat_witir': 'sahih_bukhari_kitab_solat_witir',
  'sahih_bukhari_kitab_mengqasarkan_solat': 'sahih_bukhari_kitab_mengqasarkan_solat',
  'sahih_bukhari_kitab_perbuatan_dalam_solat': 'sahih_bukhari_kitab_perbuatan_dalam_solat',
  
  // Jihad (which might be Perang)
  'sahih_bukhari_kitab_jihad': 'sahih_bukhari_kitab_jihad',
  
  // Perang (if it exists separately)
  'sahih_bukhari_kitab_perang': 'sahih_bukhari_kitab_jihad'
};

// Paths
const backupPath = '/data/work/dev/daurahtafsir-makro/backup/syarah_kitab_bukhari_backup';
const newPath = '/data/work/dev/daurahtafsir-makro/syarah_hadis/syarah_kitab_bukhari';

// Process each mapping
Object.keys(directoryMapping).forEach(backupDir => {
  const backupDirPath = path.join(backupPath, backupDir);
  const newDirName = directoryMapping[backupDir];
  const newDirPath = path.join(newPath, newDirName);
  
  // Check if backup directory exists
  if (fs.existsSync(backupDirPath)) {
    // Check if new directory exists
    if (fs.existsSync(newDirPath)) {
      // Get all files from backup directory
      const files = fs.readdirSync(backupDirPath);
      
      // Copy each file to the new directory
      files.forEach(file => {
        const sourceFile = path.join(backupDirPath, file);
        const destFile = path.join(newDirPath, file);
        
        // Only copy if file doesn't already exist in destination
        if (!fs.existsSync(destFile)) {
          const fileContent = fs.readFileSync(sourceFile);
          fs.writeFileSync(destFile, fileContent);
          console.log(`Copied ${file} from ${backupDir} to ${newDirName}`);
        }
      });
      
      console.log(`Processed ${files.length} files from ${backupDir} to ${newDirName}`);
    } else {
      console.log(`New directory ${newDirName} does not exist`);
    }
  } else {
    console.log(`Backup directory ${backupDir} does not exist`);
  }
});

console.log('Copy operation complete!');