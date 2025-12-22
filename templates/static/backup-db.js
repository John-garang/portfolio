const fs = require('fs');
const path = require('path');
const Database = require('./database');

function createBackup() {
    const db = new Database();
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupDir = path.join(__dirname, 'backups');
    
    // Create backups directory if it doesn't exist
    if (!fs.existsSync(backupDir)) {
        fs.mkdirSync(backupDir);
    }
    
    const backupData = {};
    
    console.log('Creating database backup...');
    
    // Get all data
    db.getMessages((err, messages) => {
        if (!err) backupData.messages = messages;
        
        db.getAnalytics((err, analytics) => {
            if (!err) backupData.analytics = analytics;
            
            db.getBlogPosts((err, blogPosts) => {
                if (!err) backupData.blogPosts = blogPosts;
                
                db.getProjects((err, projects) => {
                    if (!err) backupData.projects = projects;
                    
                    db.getArticles((err, articles) => {
                        if (!err) backupData.articles = articles;
                        
                        db.getSubscribers((err, subscribers) => {
                            if (!err) backupData.subscribers = subscribers;
                            
                            db.getRecentEvents(1000, (err, events) => {
                                if (!err) backupData.events = events;
                                
                                // Write backup file
                                const backupFile = path.join(backupDir, `backup-${timestamp}.json`);
                                fs.writeFileSync(backupFile, JSON.stringify(backupData, null, 2));
                                
                                console.log(`Backup created: ${backupFile}`);
                                
                                // Keep only last 10 backups
                                const backupFiles = fs.readdirSync(backupDir)
                                    .filter(file => file.startsWith('backup-') && file.endsWith('.json'))
                                    .sort()
                                    .reverse();
                                
                                if (backupFiles.length > 10) {
                                    const filesToDelete = backupFiles.slice(10);
                                    filesToDelete.forEach(file => {
                                        fs.unlinkSync(path.join(backupDir, file));
                                        console.log(`Deleted old backup: ${file}`);
                                    });
                                }
                                
                                db.close();
                            });
                        });
                    });
                });
            });
        });
    });
}

// Run backup if called directly
if (require.main === module) {
    createBackup();
}

module.exports = createBackup;
