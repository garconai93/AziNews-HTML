function sendNewsletter() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Newsletter');
  if (!sheet) {
    Logger.log('Sheet not found');
    return;
  }
  
  var data = sheet.getDataRange().getValues();
  var subscribers = [];
  
  for (var i = 1; i < data.length; i++) {
    if (data[i][0] && data[i][0] != '') {
      subscribers.push(data[i][0]);
    }
  }
  
  Logger.log('Subscribers: ' + subscribers.length);
  
  var subject = '📰 AziNews - ' + new Date().toLocaleDateString('ro-RO', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  
  var body = '<html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">';
  body += '<h1 style="color: #58a6ff;">📰 AziNews</h1>';
  body += '<p>Here are the latest news from Romania:</p>';
  body += '<hr style="border: 1px solid #30363d;">';
  body += '<h2>Latest Headlines</h2>';
  body += '<ul>';
  body += '<li><a href="https://www.digi24.ro">Digi24 - Latest news</a></li>';
  body += '<li><a href="https://www.mediafax.ro">Mediafax - Latest news</a></li>';
  body += '</ul>';
  body += '<hr style="border: 1px solid #30363d;">';
  body += '<p style="color: #8b949e; font-size: 12px;">';
  body += 'Acest email a fost trimis la ' + subscribers.length + ' abonați.<br>';
  body += 'Dacă nu mai vrei să primești newsletter, <a href="https://azinews.ro">click aici</a>.';
  body += '</p></body></html>';
  
  var sentCount = 0;
  for (var i = 0; i < subscribers.length; i++) {
    try {
      GmailApp.sendEmail(subscribers[i], subject, '', { htmlBody: body, name: 'AziNews' });
      Logger.log('Sent to: ' + subscribers[i]);
      sentCount++;
    } catch (e) {
      Logger.log('Error: ' + e.message);
    }
  }
  
  return 'Sent to ' + sentCount + ' subscribers';
}

function testSend() {
  GmailApp.sendEmail('garconai93@gmail.com', 'Test AziNews', 'Test!');
}

function getSubscribers() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Newsletter');
  if (!sheet) return [];
  var data = sheet.getDataRange().getValues();
  var subscribers = [];
  for (var i = 1; i < data.length; i++) {
    if (data[i][0] && data[i][0] != '') subscribers.push(data[i][0]);
  }
  return subscribers;
}

function doPost(e) {
  if (!e) return ContentService.createTextOutput(JSON.stringify({error: 'No data'})).setMimeType(ContentService.MimeType.JSON);
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Newsletter');
  if (!sheet) {
    sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet('Newsletter');
    sheet.appendRow(['Email', 'Data', 'Ora']);
  }
  var email;
  try { 
    if (e.postData && e.postData.contents) {
      var data = JSON.parse(e.postData.contents); 
      email = data.email; 
    }
  } catch (err) { 
    if (e.parameter && e.parameter.email) email = e.parameter.email;
  }
  
  if (!email) return ContentService.createTextOutput(JSON.stringify({error: 'No email'})).setMimeType(ContentService.MimeType.JSON);
  
  var now = new Date();
  sheet.appendRow([email, now.toDateString(), now.toTimeString()]);
  return ContentService.createTextOutput(JSON.stringify({success: true})).setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  if (!e) e = {};
  return ContentService.createTextOutput(JSON.stringify({status: 'ok'})).setMimeType(ContentService.MimeType.JSON);
}
