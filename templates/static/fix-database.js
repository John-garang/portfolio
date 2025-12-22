const fs = require('fs');

// Fix corrupted database.json
try {
    const data = fs.readFileSync('./database.json', 'utf8');
    
    // Find the last valid closing brace
    let lastValidIndex = data.lastIndexOf('}\n  ]\n}');
    if (lastValidIndex === -1) {
        lastValidIndex = data.lastIndexOf('}');
    }
    
    if (lastValidIndex !== -1) {
        const cleanData = data.substring(0, lastValidIndex + 1);
        
        // Try to parse to validate
        const parsed = JSON.parse(cleanData);
        
        // Write clean version
        fs.writeFileSync('./database.json', JSON.stringify(parsed, null, 2));
        console.log('Database fixed successfully!');
    } else {
        console.log('Could not find valid JSON structure');
    }
} catch (error) {
    console.error('Error fixing database:', error.message);
    
    // Create minimal database if completely corrupted
    const minimalDb = {
        messages: [],
        analytics: { visitors: 0, pageViews: 0, contactForms: 0, subscribers: 0 },
        blogPosts: [],
        projects: [],
        articles: [],
        comments: [],
        subscribers: [],
        events: [],
        sessions: []
    };
    
    fs.writeFileSync('./database.json', JSON.stringify(minimalDb, null, 2));
    console.log('Created new minimal database');
}
