function doPost() {
  const sheet = SpreadsheetApp.openById('1oil4zOqJeJY8pyYUjPPG62fbDKEk2onf3NfG-OyhhfA').getSheetByName('Sheet1');
  sheet.appendRow([new Date(), 'Test Entry', 'working@test.com']);
  return ContentService.createTextOutput('OK');
}

function doGet() {
  return ContentService.createTextOutput('Working');
}