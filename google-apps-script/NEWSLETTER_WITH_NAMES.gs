function doPost(e) {
  try {
    const contactSheet = SpreadsheetApp.openById('1oil4zOqJeJY8pyYUjPPG62fbDKEk2onf3NfG-OyhhfA').getSheetByName('Sheet1');
    const newsletterSheet = SpreadsheetApp.openById('1jf4RPFx6nzN6ejvWjRN6aAOhTPoo9YmyIPEaKPo0WMk').getSheetByName('Sheet1');
    
    // Get form data
    const params = e ? e.parameter : {};
    
    if (params.formType === 'contact') {
      // Setup contact sheet headers
      if (contactSheet.getLastRow() === 0) {
        contactSheet.appendRow(['Timestamp', 'Name', 'Email', 'Phone', 'Company', 'Service', 'Budget', 'Timeline', 'Message']);
      }
      
      // Add contact data
      contactSheet.appendRow([
        new Date(),
        params.name || '',
        params.email || '',
        params.phone || '',
        params.company || '',
        params.service || '',
        params.budget || '',
        params.timeline || '',
        params.message || ''
      ]);
      
      // Send email notification
      if (params.email) {
        MailApp.sendEmail('dengjohn200@gmail.com', 'New Contact Form Submission', 
          `Name: ${params.name}\nEmail: ${params.email}\nMessage: ${params.message}`);
      }
      
    } else if (params.formType === 'newsletter') {
      // Setup newsletter sheet headers
      if (newsletterSheet.getLastRow() === 0) {
        newsletterSheet.appendRow(['Timestamp', 'Name', 'Email']);
      }
      
      // Add newsletter data
      newsletterSheet.appendRow([new Date(), params.name || '', params.email || '']);
    }
    
    return ContentService.createTextOutput('SUCCESS');
  } catch (error) {
    return ContentService.createTextOutput('ERROR: ' + error.toString());
  }
}

function doGet() {
  return ContentService.createTextOutput('Apps Script Working');
}