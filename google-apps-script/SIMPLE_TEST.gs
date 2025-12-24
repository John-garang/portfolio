function doPost(e) {
  // Create a test entry regardless of input
  try {
    const sheet = SpreadsheetApp.openById('1oil4zOqJeJY8pyYUjPPG62fbDKEk2onf3NfG-OyhhfA').getSheetByName('Sheet1');
    
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Timestamp', 'Name', 'Email', 'Phone', 'Company', 'Service', 'Budget', 'Timeline', 'Message']);
    }
    
    sheet.appendRow([new Date(), 'Form Submitted', 'test@example.com', '', '', '', '', '', 'Form submission received']);
    
    return ContentService.createTextOutput('SUCCESS');
  } catch (error) {
    return ContentService.createTextOutput('ERROR: ' + error.toString());
  }
}

function doGet() {
  return ContentService.createTextOutput('Apps Script is working');
}