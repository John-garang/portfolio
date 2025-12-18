# Database Persistence Setup Guide

## Problem
Your current server uses a JSON file (`database.json`) for data storage, which gets reset every time the server restarts. This causes data loss and server instability.

## Solutions

### Solution 1: SQLite Database (Recommended)

#### Quick Setup
1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Run the migration script:**
   ```bash
   node migrate-data.js
   ```

3. **Start the persistent server:**
   ```bash
   node server-persistent.js
   ```

   Or use the batch file:
   ```bash
   start-persistent.bat
   ```

#### What Changed
- **Database**: JSON file → SQLite database (`portfolio_data.db`)
- **Persistence**: Data survives server restarts
- **Performance**: Better query performance and concurrent access
- **Backup**: Automatic backup system included

#### Files Created
- `database.js` - SQLite database class
- `server-persistent.js` - Updated server with SQLite
- `migrate-data.js` - Migrates existing JSON data
- `backup-db.js` - Creates regular backups
- `package.json` - Updated dependencies

### Solution 2: Docker Setup (Production)

#### Setup
1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

#### Benefits
- **Isolation**: Containerized environment
- **Persistence**: Volume mounting for data
- **Scalability**: Easy to scale and deploy
- **Health Checks**: Automatic restart on failure

## Migration Process

### Automatic Migration
The `migrate-data.js` script will:
1. Read your existing `database.json`
2. Transfer all data to SQLite database
3. Create a backup of the original file
4. Preserve all messages, articles, subscribers, etc.

### Manual Verification
After migration, verify your data:
1. Start the new server: `node server-persistent.js`
2. Visit admin dashboard: `http://localhost:3000/admin-dashboard.html`
3. Check all sections (messages, articles, subscribers)

## Backup System

### Automatic Backups
- Run: `npm run backup`
- Creates timestamped JSON backups
- Keeps last 10 backups automatically
- Stored in `backups/` directory

### Schedule Regular Backups
Add to your system's task scheduler:
```bash
# Daily backup at 2 AM
0 2 * * * cd /path/to/portfolio && npm run backup
```

## Troubleshooting

### Server Won't Start
1. Check if port 3000 is available
2. Verify all dependencies are installed: `npm install`
3. Check database permissions

### Data Not Persisting
1. Ensure you're using `server-persistent.js`
2. Check if `portfolio_data.db` file exists
3. Verify write permissions in the directory

### Migration Issues
1. Backup your `database.json` first
2. Check the migration logs for errors
3. Manually verify data after migration

## Performance Improvements

### Database Optimization
- SQLite provides better concurrent access
- Indexed queries for faster searches
- Reduced memory usage

### Server Stability
- Proper error handling
- Graceful shutdown procedures
- Health check endpoints

## Security Enhancements

### Data Protection
- Input sanitization maintained
- SQL injection prevention
- Rate limiting preserved

### Backup Security
- Regular automated backups
- Version control for data changes
- Recovery procedures documented

## Next Steps

1. **Test the new system** thoroughly
2. **Set up regular backups** (daily recommended)
3. **Monitor server logs** for any issues
4. **Consider Docker deployment** for production

## Support

If you encounter issues:
1. Check the server logs
2. Verify database file permissions
3. Ensure all dependencies are installed
4. Test with a fresh database if needed

The new system will solve your data persistence issues and provide a more stable, scalable solution for your portfolio website.