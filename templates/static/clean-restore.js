const fs = require('fs');

// Clean restore from backup
try {
    console.log('Cleaning and restoring data...');
    
    // Read the backup file
    let backupData = fs.readFileSync('./database.json.backup', 'utf8');
    
    // Find the last valid closing brace for sessions array
    const lastValidEnd = backupData.lastIndexOf('    }\n  ]\n}');
    
    if (lastValidEnd !== -1) {
        // Cut off everything after the last valid session
        backupData = backupData.substring(0, lastValidEnd + 7); // +7 for '    }\n  ]\n}'
        
        // Try to parse to validate
        const parsed = JSON.parse(backupData);
        
        // Write clean version
        fs.writeFileSync('./database.json', JSON.stringify(parsed, null, 2));
        
        console.log('Data cleaned and restored successfully!');
        console.log(`Restored ${parsed.articles?.length || 0} articles`);
        console.log(`Restored ${parsed.messages?.length || 0} messages`);
        console.log(`Restored ${parsed.subscribers?.length || 0} subscribers`);
        
    } else {
        throw new Error('Could not find valid JSON structure');
    }
    
} catch (error) {
    console.error('Error:', error.message);
    
    // Create with essential data manually
    const essentialData = {
        "messages": [
            {
                "id": 1766050266790,
                "name": "John  Garang",
                "email": "j.garang@alustudent.com",
                "phone": "",
                "company": "Education Bridge",
                "service": "consultation",
                "budget": "under-1000",
                "timeline": "asap",
                "message": "cvbnm ",
                "date": "2025-12-18",
                "status": "read"
            }
        ],
        "analytics": {
            "visitors": 94,
            "pageViews": 94,
            "contactForms": 3,
            "subscribers": 3
        },
        "blogPosts": [],
        "projects": [],
        "articles": [
            {
                "id": 1766068053808,
                "title": "Addressing Entrepreneurial Gaps in South Sudan",
                "category": "academia",
                "excerpt": "South Sudanese students, particularly from low-income backgrounds, have limited access to entrepreneurial resources such as mentorship, funding, and business training.",
                "content": "This limits their ability to scale their ideas and sustain their businesses, exacerbating unemployment and poverty nationwide...",
                "image": "",
                "date": "2025-12-18",
                "slug": "addressing-entrepreneurial-gaps-in-south-sudan"
            },
            {
                "id": 1766047997042,
                "title": "The Making of a Dinka Woman: A Survival Manual Disguised as Culture",
                "category": "personal-writings",
                "excerpt": "Even though I don't agree with feminists in most cases, we can agree on one thing; the closest living thing to a donkey isn't four-legged. It's a Dinka woman.",
                "content": "Let's unpack this, shall we?...",
                "image": "The Making of a Dinka Woman: A Survival Manual Disguised as Culture.jpg",
                "date": "2025-12-18",
                "slug": "the-making-of-a-dinka-woman-a-survival-manual-disguised-as-culture"
            },
            {
                "id": 1766047903573,
                "title": "When an Educated Woman Says No",
                "category": "personal-writings",
                "excerpt": "Educated women can read through you like the book you never finished.",
                "content": "I can't date an educated woman...",
                "image": "When an Educated Woman Says No.jpg",
                "date": "2025-12-18",
                "slug": "when-an-educated-woman-says-no"
            },
            {
                "id": 1766047780288,
                "title": "Development Trajectory of South Sudan",
                "category": "academia",
                "excerpt": "South Sudan, the world's youngest nation, has already had a long political history...",
                "content": "Borrowing data from African Economic Outlook 2023...",
                "image": "Development Trajectory of South Sudan.jpg",
                "date": "2025-12-18",
                "slug": "development-trajectory-of-south-sudan"
            },
            {
                "id": 1766047225781,
                "title": "If Equality Means This, Burn the World Already",
                "category": "personal-writings",
                "excerpt": "When violence wears a skirt and puts on lipstick, it suddenly becomes excused.",
                "content": "Today in Awiel, Northern Bahr El Ghazal, South Sudan...",
                "image": "If Equality Means This, Burn the World Already.jpg",
                "date": "2025-12-18",
                "slug": "if-equality-means-this-burn-the-world-already"
            }
        ],
        "subscribers": [
            {
                "id": 1766053997665,
                "email": "Socialmedia@spp.org.za",
                "firstName": "John Ngor Deng",
                "lastName": "Garang",
                "date": "2025-12-18"
            },
            {
                "id": 1766054729249,
                "email": "ataakdengg@gmail.com",
                "firstName": "John",
                "lastName": "Garang",
                "date": "2025-12-18"
            },
            {
                "id": 1766054779855,
                "email": "a.garang@alustudent.com",
                "firstName": "John",
                "lastName": "Garang",
                "date": "2025-12-18"
            }
        ],
        "events": [],
        "sessions": []
    };
    
    fs.writeFileSync('./database.json', JSON.stringify(essentialData, null, 2));
    console.log('Created database with essential data');
}
