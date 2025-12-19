# How to Start the Server for Admin Dashboard

## The Issue
The admin dashboard cannot fetch data from the database because the Node.js server is not running.

## Solution

### Option 1: Start the server manually
Open a terminal in the Portfolio directory and run:
```bash
npm start
```

Or for development with auto-reload:
```bash
npm run dev
```

### Option 2: Use the batch file (if on Windows)
Double-click on `start-persistent-server.bat` in the Portfolio folder

## Verify the Server is Running
1. Open your browser
2. Go to `https://portfolio-backend-1-53hz.onrender.com/api/articles`
3. You should see JSON data with your articles

## Then Access the Admin Dashboard
1. Make sure the server is running (see above)
2. Open `admin-login.html` in your browser
3. Login with your credentials
4. The dashboard should now load data successfully

## Troubleshooting
- If port 3000 is already in use, you'll see an error. Close any other applications using that port.
- Make sure you have Node.js installed (`node --version` to check)
- Make sure dependencies are installed (`npm install` if needed)
