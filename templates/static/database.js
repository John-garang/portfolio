const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const DB_PATH = path.join(__dirname, 'portfolio_data.db');

class Database {
    constructor() {
        this.db = new sqlite3.Database(DB_PATH, (err) => {
            if (err) {
                console.error('Error opening database:', err);
            } else {
                console.log('Connected to SQLite database');
                this.initTables();
            }
        });
    }

    initTables() {
        const tables = [
            `CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT,
                message TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT DEFAULT 'new'
            )`,
            `CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY,
                visitors INTEGER DEFAULT 0,
                pageViews INTEGER DEFAULT 0,
                contactForms INTEGER DEFAULT 0,
                subscribers INTEGER DEFAULT 0
            )`,
            `CREATE TABLE IF NOT EXISTS blog_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                excerpt TEXT,
                date TEXT NOT NULL,
                status TEXT DEFAULT 'published'
            )`,
            `CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                image TEXT,
                link TEXT,
                date TEXT NOT NULL
            )`,
            `CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                excerpt TEXT,
                slug TEXT UNIQUE,
                date TEXT NOT NULL,
                status TEXT DEFAULT 'published'
            )`,
            `CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                firstName TEXT,
                lastName TEXT,
                date TEXT NOT NULL
            )`,
            `CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eventType TEXT,
                page TEXT,
                sessionId TEXT,
                timestamp TEXT,
                ip TEXT
            )`
        ];

        tables.forEach(sql => {
            this.db.run(sql, (err) => {
                if (err) console.error('Error creating table:', err);
            });
        });

        // Initialize analytics if empty
        this.db.get("SELECT COUNT(*) as count FROM analytics", (err, row) => {
            if (!err && row.count === 0) {
                this.db.run("INSERT INTO analytics (id, visitors, pageViews, contactForms, subscribers) VALUES (1, 0, 0, 0, 0)");
            }
        });
    }

    // Messages
    getMessages(callback) {
        this.db.all("SELECT * FROM messages ORDER BY id DESC", callback);
    }

    addMessage(message, callback) {
        const { name, email, subject, message: msg, date, status } = message;
        this.db.run(
            "INSERT INTO messages (name, email, subject, message, date, status) VALUES (?, ?, ?, ?, ?, ?)",
            [name, email, subject, msg, date, status],
            function(err) {
                callback(err, { id: this.lastID, ...message });
            }
        );
    }

    deleteMessage(id, callback) {
        this.db.run("DELETE FROM messages WHERE id = ?", [id], callback);
    }

    updateMessage(id, updates, callback) {
        const fields = Object.keys(updates).map(key => `${key} = ?`).join(', ');
        const values = Object.values(updates);
        this.db.run(`UPDATE messages SET ${fields} WHERE id = ?`, [...values, id], callback);
    }

    // Analytics
    getAnalytics(callback) {
        this.db.get("SELECT * FROM analytics WHERE id = 1", callback);
    }

    updateAnalytics(updates, callback) {
        const fields = Object.keys(updates).map(key => `${key} = ?`).join(', ');
        const values = Object.values(updates);
        this.db.run(`UPDATE analytics SET ${fields} WHERE id = 1`, values, callback);
    }

    incrementAnalytics(field, callback) {
        this.db.run(`UPDATE analytics SET ${field} = ${field} + 1 WHERE id = 1`, callback);
    }

    // Blog Posts
    getBlogPosts(callback) {
        this.db.all("SELECT * FROM blog_posts ORDER BY id DESC", callback);
    }

    addBlogPost(post, callback) {
        const { title, content, excerpt, date, status } = post;
        this.db.run(
            "INSERT INTO blog_posts (title, content, excerpt, date, status) VALUES (?, ?, ?, ?, ?)",
            [title, content, excerpt, date, status],
            function(err) {
                callback(err, { id: this.lastID, ...post });
            }
        );
    }

    deleteBlogPost(id, callback) {
        this.db.run("DELETE FROM blog_posts WHERE id = ?", [id], callback);
    }

    // Projects
    getProjects(callback) {
        this.db.all("SELECT * FROM projects ORDER BY id DESC", callback);
    }

    addProject(project, callback) {
        const { title, description, image, link, date } = project;
        this.db.run(
            "INSERT INTO projects (title, description, image, link, date) VALUES (?, ?, ?, ?, ?)",
            [title, description, image, link, date],
            function(err) {
                callback(err, { id: this.lastID, ...project });
            }
        );
    }

    deleteProject(id, callback) {
        this.db.run("DELETE FROM projects WHERE id = ?", [id], callback);
    }

    // Articles
    getArticles(callback) {
        this.db.all("SELECT * FROM articles ORDER BY id DESC", callback);
    }

    addArticle(article, callback) {
        const { title, content, excerpt, slug, date, status } = article;
        this.db.run(
            "INSERT INTO articles (title, content, excerpt, slug, date, status) VALUES (?, ?, ?, ?, ?, ?)",
            [title, content, excerpt, slug, date, status],
            function(err) {
                callback(err, { id: this.lastID, ...article });
            }
        );
    }

    updateArticle(id, article, callback) {
        const { title, content, excerpt, slug, status } = article;
        this.db.run(
            "UPDATE articles SET title = ?, content = ?, excerpt = ?, slug = ?, status = ? WHERE id = ?",
            [title, content, excerpt, slug, status, id],
            callback
        );
    }

    deleteArticle(id, callback) {
        this.db.run("DELETE FROM articles WHERE id = ?", [id], callback);
    }

    getArticleById(id, callback) {
        this.db.get("SELECT * FROM articles WHERE id = ?", [id], callback);
    }

    // Subscribers
    getSubscribers(callback) {
        this.db.all("SELECT * FROM subscribers ORDER BY id DESC", callback);
    }

    addSubscriber(subscriber, callback) {
        const { email, firstName, lastName, date } = subscriber;
        this.db.run(
            "INSERT INTO subscribers (email, firstName, lastName, date) VALUES (?, ?, ?, ?)",
            [email, firstName, lastName, date],
            function(err) {
                callback(err, { id: this.lastID, ...subscriber });
            }
        );
    }

    deleteSubscriber(id, callback) {
        this.db.run("DELETE FROM subscribers WHERE id = ?", [id], callback);
    }

    // Events
    addEvent(event, callback) {
        const { eventType, page, sessionId, timestamp, ip } = event;
        this.db.run(
            "INSERT INTO events (eventType, page, sessionId, timestamp, ip) VALUES (?, ?, ?, ?, ?)",
            [eventType, page, sessionId, timestamp, ip],
            callback
        );
    }

    getRecentEvents(limit, callback) {
        this.db.all("SELECT * FROM events ORDER BY id DESC LIMIT ?", [limit], callback);
    }

    close() {
        this.db.close((err) => {
            if (err) {
                console.error('Error closing database:', err);
            } else {
                console.log('Database connection closed');
            }
        });
    }
}

module.exports = Database;
