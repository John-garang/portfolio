const CONTACT_SHEET_ID = '1oil4zOqJeJY8pyYUjPPG62fbDKEk2onf3NfG-OyhhfA';
const NEWSLETTER_SHEET_ID = '1jf4RPFx6nzN6ejvWjRN6aAOhTPoo9YmyIPEaKPo0WMk';
const ADMIN_EMAIL = 'dengjohn200@gmail.com';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);

    if (data.formType === 'contact') {
      return handleContactForm(data);
    } 
    if (data.formType === 'newsletter') {
      return handleNewsletterForm(data);
    }

    return jsonResponse(false, 'Unknown form type');

  } catch (error) {
    return jsonResponse(false, error.message);
  }
}

function handleContactForm(data) {
  const sheet = SpreadsheetApp.openById(CONTACT_SHEET_ID).getActiveSheet();

  if (sheet.getLastRow() < 1) {
    sheet.appendRow([
      'Timestamp', 'Name', 'Email', 'Phone', 'Company',
      'Service', 'Budget', 'Timeline', 'Message'
    ]);
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

  sendContactNotification(data);

  return jsonResponse(true, 'Contact form submitted successfully');
}

function handleNewsletterForm(data) {
  const sheet = SpreadsheetApp.openById(NEWSLETTER_SHEET_ID).getActiveSheet();

  if (sheet.getLastRow() < 1) {
    sheet.appendRow(['Timestamp', 'Email']);
  }

  const lastRow = sheet.getLastRow();
  const emails = lastRow > 1
    ? sheet.getRange(2, 2, lastRow - 1, 1).getValues().flat()
    : [];

  if (emails.includes(data.email)) {
    return jsonResponse(false, 'Email already subscribed');
  }

  sheet.appendRow([new Date(), data.email]);
  return jsonResponse(true, 'Successfully subscribed');
}

function sendContactNotification(data) {
  MailApp.sendEmail(
    ADMIN_EMAIL,
    `New Contact Form Submission from ${data.name}`,
    `Name: ${data.name}\nEmail: ${data.email}\n\nMessage:\n${data.message}`
  );
}

function jsonResponse(success, message) {
  return ContentService
    .createTextOutput(JSON.stringify({ success, message }))
    .setMimeType(ContentService.MimeType.JSON)
    .setHeader('Access-Control-Allow-Origin', '*');
}