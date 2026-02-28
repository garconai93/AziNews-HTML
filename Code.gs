// Google Apps Script pentru AziNews Newsletter
// Deploy as Web App cu "Anyone" access

function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Newsletter');
  if (!sheet) {
    sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet('Newsletter');
    sheet.appendRow(['Email', 'Data', 'Ora']);
  }
  
  var email;
  try {
    var data = JSON.parse(e.postData.contents);
    email = data.email;
  } catch (err) {
    // Fallback for form data
    email = e.parameter.email;
  }
  
  var now = new Date();
  sheet.appendRow([email, now.toDateString(), now.toTimeString()]);
  
  return ContentService.createTextOutput(JSON.stringify({success: true}))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet() {
  return ContentService.createTextOutput(JSON.stringify({status: 'ok'}))
    .setMimeType(ContentService.MimeType.JSON);
}
