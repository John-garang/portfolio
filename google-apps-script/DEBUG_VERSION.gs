const CONTACT_SHEET_ID = '1oil4zOqJeJY8pyYUjPPG62fbDKEk2onf3NfG-OyhhfA';
const NEWSLETTER_SHEET_ID = '1jf4RPFx6nzN6ejvWjRN6aAOhTPoo9YmyIPEaKPo0WMk';
const ADMIN_EMAIL = 'dengjohn200@gmail.com';

function doPost(e) {
  try {
    // Log everything we receive
    Logger.log('Full event object: ' + JSON.stringify(e));
    Logger.log('e.parameter: ' + JSON.stringify(e.parameter));
    Logger.log('e.postData: ' + JSON.stringify(e.postData));
    
    let data = {};
    
    // Try different ways to get the data
    if (e.parameter && Object.keys(e.parameter).length > 0) {
      data = e.parameter;
      Logger.log('Using e.parameter');
    } else if (e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
      Logger.log('Using e.postData.contents');
    } else {
      Logger.log('No data found, creating test entry');
      // Create a test entry to verify the script works
      const sheet = SpreadsheetApp.openById(CONTACT_SHEET_ID).getSheetByName('Sheet1');
      if (sheet.getLastRow() === 0) {
        sheet.appendRow(['Timestamp', 'Name', 'Email', 'Phone', 'Company', 'Service', 'Budget', 'Timeline', 'Message']);
      }
      sheet.appendRow([new Date(), 'Test Entry', 'test@example.com', '', '', '', '', '', 'Apps Script is working']);
      return ContentService.createTextOutput(JSON.stringify({success: true, message: 'Test entry created'}));
    }
    
    Logger.log('Processing data: ' + JSON.stringify(data));
    
    if (data.formType === 'contact') {
      return handleContactForm(data);
    } 
    if (data.formType === 'newsletter') {
      return handleNewsletterForm(data);
    }

    return ContentService.createTextOutput(JSON.stringify({success: false, message: 'Unknown form type'}));

  } catch (error) {
    Logger.log('doPost error: ' + error.toString());
    return ContentService.createTextOutput(JSON.stringify({success: false, message: error.message}));
  }
}

function handleContactForm(data) {
  try {
    const sheet = SpreadsheetApp.openById(CONTACT_SHEET_ID).getSheetByName('Sheet1');
    
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Timestamp', 'Name', 'Email', 'Phone', 'Company', 'Service', 'Budget', 'Timeline', 'Message']);
    }

    sheet.appendRow([
      new Date(), 
      data.name || '', 
      data.email || '', 
      data.phone || '',
      data.company || '', 
      data.service || '', 
      data.budget || '',
      data.timeline || '', 
      data.message || ''
    ]);

    Logger.log('Contact form processed successfully');
    return ContentService.createTextOutput(JSON.stringify({success: true, message: 'Contact form submitted'}));
  } catch (error) {
    Logger.log('Contact form error: ' + error.toString());
    return ContentService.createTextOutput(JSON.stringify({success: false, message: error.message}));
  }
}

function handleNewsletterForm(data) {
  try {
    const sheet = SpreadsheetApp.openById(NEWSLETTER_SHEET_ID).getSheetByName('Sheet1');
    
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Timestamp', 'Email']);
    }

    sheet.appendRow([new Date(), data.email]);
    Logger.log('Newsletter processed successfully');
    return ContentService.createTextOutput(JSON.stringify({success: true, message: 'Newsletter subscribed'}));
  } catch (error) {
    Logger.log('Newsletter error: ' + error.toString());
    return ContentService.createTextOutput(JSON.stringify({success: false, message: error.message}));
  }
}