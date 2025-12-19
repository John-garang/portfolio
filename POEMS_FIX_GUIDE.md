# Poems Dashboard Issue - Fix Guide

## Problem Identified
The server is **NOT running** on port 3000. The dashboard tries to load poems but fails because there's no server to respond.

## Evidence
- `netstat` shows `SYN_SENT` status (connection attempts failing)
- No `LISTENING` status on port 3000
- Database.json has empty poems array: `"poems": []`

## Solution

### Step 1: Start the Server
Run one of these commands in the Portfolio directory:

```bash
# Option 1: Start server normally
node server.js

# Option 2: Use the batch file
start-server-and-test.bat

# Option 3: Use persistent server
start-persistent-server.bat
```

### Step 2: Verify Server is Running
Open a new terminal and run:
```bash
netstat -ano | findstr :3000 | findstr LISTENING
```

You should see output like:
```
TCP    0.0.0.0:3000           0.0.0.0:0              LISTENING       12345
```

### Step 3: Test the Poems API
1. Open `test-poems-fix.html` in your browser
2. Click "Test GET /api/poems" - should return empty array `[]`
3. Click "Add Test Poem" - should add a poem successfully
4. Click "Test GET /api/poems" again - should show the poem

### Step 4: Access the Dashboard
Once the server is running:
1. Open `admin-login.html`
2. Login with credentials (default: admin/admin123)
3. Navigate to the Poems section
4. You should now see the poems interface working

## Why the Dashboard Failed
The dashboard JavaScript tries to fetch from `https://portfolio-backend-1-53hz.onrender.com/api/poems` but:
- Server wasn't running → Connection refused
- Browser shows network errors in console
- Dashboard appears broken/empty

## Quick Fix Commands
```bash
# Kill any stuck processes on port 3000
netstat -ano | findstr :3000
# Note the PID and kill it:
taskkill /PID <PID> /F

# Start fresh server
node server.js
```

## Files Created for Testing
- `test-poems-fix.html` - Simple API test page
- `start-server-and-test.bat` - Automated server startup and test
- `POEMS_FIX_GUIDE.md` - This guide

## Expected Behavior After Fix
✅ Server running on port 3000
✅ Dashboard loads without errors
✅ Poems section shows "No poems yet" or existing poems
✅ Can add/edit/delete poems through dashboard
