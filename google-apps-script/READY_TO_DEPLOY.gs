function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const formType = data.formType;
    
    if (formType === 'contact') {
      return handleContactForm(data);
    } else if (formType === 'newsletter') {
      return handleNewsletterForm(data);
    }
    
    return ContentService
      .createTextOutput(JSON.stringify({success: false, message: 'Unknown form type'}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({success: false, message: error.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function handleContactForm(data) {
  const spreadsheetId = '1oil4zOqJeJY8pyYUjPPG62fbDKEk2onf3NfG-OyhhfA';
  const sheet = SpreadsheetApp.openById(spreadsheetId).getActiveSheet();
  
  // Add headers if sheet is empty
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, 9).setValues([[
      'Timestamp', 'Name', 'Email', 'Phone', 'Company', 'Service', 'Budget', 'Timeline', 'Message'
    ]]);
  }
  
  // Add form data
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
  
  // Send email notification
  sendContactNotification(data);
  
  return ContentService
    .createTextOutput(JSON.stringify({success: true, message: 'Contact form submitted successfully'}))
    .setMimeType(ContentService.MimeType.JSON);
}

function handleNewsletterForm(data) {
  const spreadsheetId = '1jf4RPFx6nzN6ejvWjRN6aAOhTPoo9YmyIPEaKPo0WMk';
  const sheet = SpreadsheetApp.openById(spreadsheetId).getActiveSheet();
  
  // Add headers if sheet is empty
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, 2).setValues([['Timestamp', 'Email']]);
  }
  
  // Check for duplicate email
  const emails = sheet.getRange(2, 2, sheet.getLastRow() - 1, 1).getValues().flat();
  if (emails.includes(data.email)) {
    return ContentService
      .createTextOutput(JSON.stringify({success: false, message: 'Email already subscribed'}))
      .setMimeType(ContentService.MimeType.JSON);
  }
  
  // Add email
  sheet.appendRow([new Date(), data.email]);
  
  return ContentService
    .createTextOutput(JSON.stringify({success: true, message: 'Successfully subscribed to newsletter'}))
    .setMimeType(ContentService.MimeType.JSON);
}

function sendContactNotification(data) {
  const subject = `New Contact Form Submission from ${data.name}`;
  const body = `
New contact form submission:

Name: ${data.name}
Email: ${data.email}
Phone: ${data.phone}
Company: ${data.company}
Service: ${data.service}
Budget: ${data.budget}
Timeline: ${data.timeline}

Message:
${data.message}

Submitted at: ${new Date()}
  `;
  
  MailApp.sendEmail('dengjohn200@gmail.com', subject, body);
}