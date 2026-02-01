const CONTACT_SHEET_ID = '1oil4zOqJeJY8pyYUjPPG62fbDKEk2onf3NfG-OyhhfA';
const NEWSLETTER_SHEET_ID = '1jf4RPFx6nzN6ejvWjRN6aAOhTPoo9YmyIPEaKPo0WMk';
const ADMIN_EMAIL = 'dengjohn200@gmail.com';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    if (data.formType === 'contact') return handleContactForm(data);
    if (data.formType === 'newsletter') return handleNewsletterForm(data);
    return jsonResponse(false, 'Unknown form type');
  } catch (error) {
    Logger.log('doPost error: ' + error.toString());
    return jsonResponse(false, error.message);
  }
}

function doOptions() {
  return ContentService.createTextOutput()
    .setMimeType(ContentService.MimeType.JSON)
    .setHeader('Access-Control-Allow-Origin', '*')
    .setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS')
    .setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

function handleContactForm(data) {
  const sheet = SpreadsheetApp.openById(CONTACT_SHEET_ID).getSheetByName('Sheet1');
  
  if (sheet.getLastRow() === 0 || sheet.getRange(1, 1).getValue() !== 'Timestamp') {
    sheet.clear();
    sheet.appendRow(['Timestamp', 'Name', 'Email', 'Phone', 'Company', 'Service', 'Budget', 'Timeline', 'Message']);
  }

  sheet.appendRow([
    new Date(), data.name || '', data.email || '', data.phone || '',
    data.company || '', data.service || '', data.budget || '',
    data.timeline || '', data.message || ''
  ]);

  sendContactNotification(data);
  return jsonResponse(true, 'Contact form submitted successfully');
}

function handleNewsletterForm(data) {
  const sheet = SpreadsheetApp.openById(NEWSLETTER_SHEET_ID).getSheetByName('Sheet1');
  
  if (sheet.getLastRow() === 0 || sheet.getRange(1, 1).getValue() !== 'Timestamp') {
    sheet.clear();
    sheet.appendRow(['Timestamp', 'Email']);
  }

  const lastRow = sheet.getLastRow();
  const emails = lastRow > 1
    ? sheet.getRange(2, 2, lastRow - 1, 1).getValues().flat().map(email => email.toLowerCase())
    : [];

  if (emails.includes(data.email.toLowerCase())) {
    return jsonResponse(false, 'Email already subscribed');
  }

  sheet.appendRow([new Date(), data.email]);
  return jsonResponse(true, 'Successfully subscribed');
}

function sendContactNotification(data) {
  const body = `Name: ${data.name}
Email: ${data.email}
Phone: ${data.phone || 'N/A'}
Company: ${data.company || 'N/A'}
Service: ${data.service || 'N/A'}
Budget: ${data.budget || 'N/A'}
Timeline: ${data.timeline || 'N/A'}

Message:
${data.message}`;

  MailApp.sendEmail(ADMIN_EMAIL, `New Contact Form Submission from ${data.name}`, body);
}

function jsonResponse(success, message) {
  return ContentService
    .createTextOutput(JSON.stringify({ success, message }))
    .setMimeType(ContentService.MimeType.JSON)
    .setHeader('Access-Control-Allow-Origin', '*');
}