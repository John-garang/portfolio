const fs = require('fs');

// Restore data from backup
try {
    console.log('Restoring data from backup...');
    
    // Read the backup file
    const backupData = fs.readFileSync('./database.json.backup', 'utf8');
    
    // Write it to the current database
    fs.writeFileSync('./database.json', backupData);
    
    console.log('Data restored successfully!');
    console.log('Your articles, messages, and subscribers are back.');
    
} catch (error) {
    console.error('Error restoring data:', error.message);
}
