# Google Apps Script Setup Instructions

## Step 1: Create Google Sheets
1. Create two Google Sheets:
   - **Contact Form Submissions** - for contact form data
   - **Newsletter Subscriptions** - for newsletter emails

2. Note the Spreadsheet IDs from the URLs:
   - URL format: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
   - Copy the SPREADSHEET_ID part

## Step 2: Create Apps Script Project
1. Go to [script.google.com](https://script.google.com)
2. Click "New Project"
3. Replace the default code with the content from `Code.gs`
4. Update the spreadsheet IDs:
   ```javascript
   const spreadsheetId = 'YOUR_CONTACT_SPREADSHEET_ID'; // Line 25
   const spreadsheetId = 'YOUR_NEWSLETTER_SPREADSHEET_ID'; // Line 44
   ```

## Step 3: Deploy as Web App
1. Click "Deploy" > "New deployment"
2. Choose type: "Web app"
3. Set execute as: "Me"
4. Set access: "Anyone"
5. Click "Deploy"
6. Copy the Web App URL

## Step 4: Update JavaScript Handler
1. Open `static/google-forms-handler.js`
2. Replace `YOUR_APPS_SCRIPT_WEB_APP_URL` with your Web App URL:
   ```javascript
   const APPS_SCRIPT_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';
   ```

## Step 5: Test Forms
1. Test contact form submission
2. Test newsletter subscription
3. Check Google Sheets for data
4. Check email notifications

## Features Included
- ✅ Contact form submissions stored in Google Sheets
- ✅ Newsletter subscriptions with duplicate prevention
- ✅ Email notifications for contact forms
- ✅ Loading states and user feedback
- ✅ Error handling and validation
- ✅ Responsive notification system

## Form Fields Captured

### Contact Form:
- Timestamp
- Full Name
- Email
- Phone
- Company
- Service Interest
- Budget Range
- Timeline
- Message

### Newsletter:
- Timestamp
- Email Address

## Security Notes
- Apps Script runs with your Google account permissions
- Form submissions are stored in your Google Drive
- Email notifications sent from your Gmail account
- No sensitive data exposed to client-side code