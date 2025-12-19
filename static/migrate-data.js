const fs = require('fs');
const Database = require('./database');

async function migrateData() {
    console.log('Starting data migration...');
    
    const db = new Database();
    
    // Wait for database to initialize
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    try {
        // Read existing JSON database
        const jsonData = JSON.parse(fs.readFileSync('./database.json', 'utf8'));
        console.log('Found existing JSON database');
        
        // Migrate messages
        if (jsonData.messages && jsonData.messages.length > 0) {
            console.log(`Migrating ${jsonData.messages.length} messages...`);
            for (const message of jsonData.messages) {
                await new Promise((resolve, reject) => {
                    db.addMessage(message, (err) => {
                        if (err) reject(err);
                        else resolve();
                    });
                });
            }
            console.log('Messages migrated successfully');
        }
        
        // Migrate analytics
        if (jsonData.analytics) {
            console.log('Migrating analytics...');
            await new Promise((resolve, reject) => {
                db.updateAnalytics(jsonData.analytics, (err) => {
                    if (err) reject(err);
                    else resolve();
                });
            });
            console.log('Analytics migrated successfully');
        }
        
        // Migrate blog posts
        if (jsonData.blogPosts && jsonData.blogPosts.length > 0) {
            console.log(`Migrating ${jsonData.blogPosts.length} blog posts...`);
            for (const post of jsonData.blogPosts) {
                await new Promise((resolve, reject) => {
                    db.addBlogPost(post, (err) => {
                        if (err) reject(err);
                        else resolve();
                    });
                });
            }
            console.log('Blog posts migrated successfully');
        }
        
        // Migrate projects
        if (jsonData.projects && jsonData.projects.length > 0) {
            console.log(`Migrating ${jsonData.projects.length} projects...`);
            for (const project of jsonData.projects) {
                await new Promise((resolve, reject) => {
                    db.addProject(project, (err) => {
                        if (err) reject(err);
                        else resolve();
                    });
                });
            }
            console.log('Projects migrated successfully');
        }
        
        // Migrate articles
        if (jsonData.articles && jsonData.articles.length > 0) {
            console.log(`Migrating ${jsonData.articles.length} articles...`);
            for (const article of jsonData.articles) {
                await new Promise((resolve, reject) => {
                    db.addArticle(article, (err) => {
                        if (err) reject(err);
                        else resolve();
                    });
                });
            }
            console.log('Articles migrated successfully');
        }
        
        // Migrate subscribers
        if (jsonData.subscribers && jsonData.subscribers.length > 0) {
            console.log(`Migrating ${jsonData.subscribers.length} subscribers...`);
            for (const subscriber of jsonData.subscribers) {
                await new Promise((resolve, reject) => {
                    db.addSubscriber(subscriber, (err) => {
                        if (err && !err.message.includes('UNIQUE constraint failed')) {
                            reject(err);
                        } else {
                            resolve();
                        }
                    });
                });
            }
            console.log('Subscribers migrated successfully');
        }
        
        console.log('Data migration completed successfully!');
        console.log('You can now use the new persistent server.');
        
        // Create backup of original JSON file
        fs.copyFileSync('./database.json', './database.json.backup');
        console.log('Original database backed up to database.json.backup');
        
    } catch (error) {
        console.error('Migration error:', error);
    } finally {
        db.close();
    }
}

migrateData();