const now = new Date();

// Define an array of month names
const MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

const month = MONTH_NAMES[now.getMonth()];
const day = now.getDate() + 1;

// Main Function
function doGet(e) {
  try {
    // Each Param
    const params = e.parameter;
    const action = params.action;
    const walletName = params.wallet_id;
    const types = params.types;
    const rawAmount = parseFloat(params.rawAmount) || 0;

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(month);

    let resText = "";

    // Handle different actions based on the request parameter
    if (action === "income" || action === "expense") {
      resText = JSON.stringify(handleTransaction(sheet, walletName, types, rawAmount, day, action));

    } else if (action === "transfer") {
      const destination = parseFloat(params.destination);
      const destinationWalletName = params.destination_wallet_id;
      resText = JSON.stringify(handleTransfer(sheet, walletName, destinationWalletName, destination, day, action));

    } else if (action === "modify") {
      const newDate = new Date(params.date);
      const newDay = newDate.getDate() + 1;
      const newType = params.newType;
      resText = JSON.stringify(handleModify(sheet, walletName, newType, rawAmount, newDay, action));
    }

    // Create and return the response
    const response = {
      statusCode: 200,
      resText
    };

    return ContentService
      .createTextOutput(JSON.stringify(response))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {

    const response = {
      statusCode: 500,
      errorMessage: error.toString(),
    };

    return ContentService
      .createTextOutput(JSON.stringify(response))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Function to log data to a spreadsheet
function logTemp(kwargs) {
  const ss = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(`History${month.substring(0, 3)}`);
  console.log(1);
  var values = ss.getRange(1, day, ss.getLastRow(), 1).getValues();
  var lastRow = values.filter(String).length;
  ss.getRange(lastRow + 1, day).setValue(JSON.stringify(kwargs));
}

function getCellValue(sheet, row, day) {
  return sheet.getRange(row, day).getValue();
}

function setCellValue(sheet, row, day, value) {
  sheet.getRange(row, day).setValue(value);
}

// Function to find the row corresponding to a specific action and type
function findRow(action, types) {
  switch (action) {
    case "income":
      return findIncomeTypeRow(types);
    case "expense":
      return findExpenseTypeRow(types);
    default:
      return null;
  }
}

// Function to handle income and expense transactions
function handleTransaction(sheet, walletName, types, rawAmount, day, action) {
  const typeRow = findRow(action, types);
  const walletRow = findWalletRow(walletName);

  if (!isNaN(typeRow) && !isNaN(walletRow)) {
    const currentTypeValue = getCellValue(sheet, typeRow, day);
    const currentWalletValue = getCellValue(sheet, walletRow, day);

    const updatedTypeValue = isNaN(currentTypeValue) ? 0 : currentTypeValue + rawAmount;
    const updatedWalletValue = isNaN(currentWalletValue) ? 0 : action === 'income' ? currentWalletValue + rawAmount : currentWalletValue - rawAmount;

    setCellValue(sheet, typeRow, day, updatedTypeValue);
    setCellValue(sheet, walletRow, day, updatedWalletValue);

    logTemp({
      "action": action,
      "date": day,
      "amount": rawAmount,
      [`old ${types} amount`]: currentTypeValue || 0,
      [`new ${types} amount`]: updatedTypeValue,
      [`old ${walletName} amount`]: currentWalletValue,
      [`new ${walletName} amount`]: updatedWalletValue,
    });

    return {
      "action": action,
      "date": day,
      "amount": rawAmount,
      [`old ${types} amount`]: currentTypeValue || 0,
      [`new ${types} amount`]: updatedTypeValue,
      [`old ${walletName} amount`]: currentWalletValue,
      [`new ${walletName} amount`]: updatedWalletValue,
    };
  } else {
    Logger.log("Invalid typeRow or walletRow provided.");
  }
}

// Function to handle transfer transactions
function handleTransfer(sheet, walletName, destinationWalletName, destination, day) {
  const walletOriginRow = findWalletRow(walletName);
  const walletDestinationRow = findWalletRow(destinationWalletName);

  const currentWalletOriginValue = getCellValue(sheet, walletOriginRow, day);
  const currentWalletDestinationValue = getCellValue(sheet, walletDestinationRow, day);

  if (walletOriginRow !== null && walletDestinationRow !== null && day) {
    sheet.getRange(walletOriginRow, day).setValue(currentWalletOriginValue - destination);
    sheet.getRange(walletDestinationRow, day).setValue(currentWalletDestinationValue + destination);
  }

  logTemp({
    "action": "transfer",
    "day": day,
    "walletName": walletName,
    "typesv": types,
    "rawAmount": rawAmount,
    "CurrentWallet": walletName,
    "currentValue": currentWalletOriginValue - destination,
    "DestinationWallet": destinationWalletName,
    "destinationValue": currentWalletDestinationValue + destination,
    "after passing through updated": ""
  });

  return {
    "action": "transfer",
    "date": day,
    "amount": rawAmount,
    [`old ${walletName} amount`]: currentWalletOriginValue || 0,
    [`new ${destinationWalletName} amount`]: currentWalletOriginValue - destination,
    [`old ${walletName} amount`]: currentWalletDestinationValue || 0,
    [`new ${destinationWalletName} amount`]: currentWalletDestinationValue + destination,
  };
}

// Function to handle modifications to transactions
function handleModify(sheet, walletName, newType, rawAmount, newDate) {
  const incomeTypeRow = findIncomeTypeRow(newType);
  const expenseTypeRow = findExpenseTypeRow(newType);
  const walletRow = findWalletRow(walletName);

  if (incomeTypeRow !== null && newDate) {
    const currentWalletOriginValue = getCellValue(sheet, walletRow, newDate);
    const updatedWalletValue = currentWalletOriginValue + rawAmount;

    sheet.getRange(walletRow, newDate).setValue(updatedWalletValue);
    sheet.getRange(incomeTypeRow, newDate).setValue(rawAmount);

    logTemp({
      "action": "modify",
      "day": day,
      "walletName": walletName,
      "AfterChangeValue": rawAmount,
      "currentWallet": walletName,
      "BeforeChangeValue": currentWalletOriginValue,
      "New Type": newType
    });

    return {
      "action": "modify",
      "date": newDate,
      "amount": rawAmount,
      [`old ${walletName} amount`]: currentWalletOriginValue || 0,
      [`new ${walletName} amount`]: updatedWalletValue,
      [`new ${newType} amount`]: rawAmount,
    };
  } else if (expenseTypeRow !== null && newDate) {
    const currentWalletOriginValue = getCellValue(sheet, walletRow, newDate);
    const updatedWalletValue = currentWalletOriginValue - rawAmount;

    sheet.getRange(walletRow, newDate).setValue(updatedWalletValue);
    sheet.getRange(expenseTypeRow, newDate).setValue(rawAmount);

    logTemp({
      "action": "modify",
      "day": day,
      "walletName": walletName,
      "types": types,
      "rawAmount": rawAmount,
      "currentTypeValue": currentTypeValue,
      "currentWalletValue": currentWalletValue,
      "updatedTypeValue": updatedTypeValue,
      "updatedWalletValue": updatedWalletValue
    });

    return {
      "action": "modify",
      "date": newDate,
      "amount": rawAmount,
      [`old ${walletName} amount`]: currentWalletOriginValue || 0,
      [`new ${walletName} amount`]: updatedWalletValue,
      [`new ${newType} amount`]: rawAmount,
    };
  }
}

// Function to find the row corresponding to a specific wallet name
function findWalletRow(walletName) {
  switch (walletName) {
    case "Wallet": return 3;
    case "SCB": return 4;
    case "BLB": return 5;
    case "True Wallet": return 6;
    case "BLANK": return 7;
    case "Red Card": return 8;
    case "MRT Card": return 9;
    case "BTS Card": return 10;
    default: return null;
  }
}

// Function to find the row corresponding to a specific income type
function findIncomeTypeRow(incomeType) {
  switch (incomeType) {
    case "เงินเดือน": return 13;
    case "รายได้": return 14;
    case "ได้รับ": return 15;
    case "อื่นๆ": return 16;
    default: return null;
  }
}

// Function to find the row corresponding to a specific expense type
function findExpenseTypeRow(expenseType) {
  switch (expenseType) {
    case "ข้าวเช้า": return 19;
    case "ข้าวเที่ยง": return 20;
    case "ข้าวเย็น": return 21;
    case "ขนม/น้ำดื่ม": return 22;
    case "เซเว่น": return 23;
    case "ค่าเดินทาง": return 24;
    case "อุปกรณ์การศึกษา/กีฬา": return 25;
    case "ค่าสังสรรค์": return 26;
    case "อุปกรณ์ไฟฟ้า": return 27;
    case "ลงทุน": return 28;
    case "อื่นๆ": return 29;
    default: return null;
  }
}

// Function to testing production
function testDoGet() {
  const e = {
    parameter: { 'action': 'income', 'wallet_id': 'SCB', 'types': 'เงินเดือน', 'rawAmount': 123.0 }
  };

  doGet(e);
}
