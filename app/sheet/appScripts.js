// Get the current date
const now = new Date();

// Define an array of month names
const MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

// Get the current month and day
const month = MONTH_NAMES[now.getMonth()];
const day = now.getDate() + 1;

// Function to handle HTTP GET requests
function doGet(e) {
  try {
    // Extract parameters from the request
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
      const destinationWalletName = params.destination_wallet_id;
      resText = JSON.stringify(handleTransfer(sheet, walletName, destinationWalletName, rawAmount, day, action));

    } else if (action === "modify") {
      // const newDate = new Date(params.date); // ON FIXING
      // const newDay = newDate.getDate() + 1;
      // const newType = params.newType;
      // resText = JSON.stringify(handleModify(sheet, walletName, newType, rawAmount, newDay, action));
      resText = JSON.stringify("On Fixing Process");

    } else if (action === "check") {
      const newDate = new Date(params.date);
      const newDay = newDate.getDate() + 1;
      resText = JSON.stringify(checkWalletValue(sheet, walletName, newDay));
    }

    // Create and return the response
    const response = {
      statusCode: resText ? "\u2705" : "\u274C", 
      resText: resText ? JSON.parse(resText) : "",  
    };

    // console.log(response)

    return ContentService
      .createTextOutput(JSON.stringify(response))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    const response = {
      statusCode: "\u274C", 
      errorMessage: error.toString(),
    };

    return ContentService
      .createTextOutput(JSON.stringify(response))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Function to log data to a spreadsheet
function logTemp(kwargs) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(`History${month.substring(0, 3)}`);
    var values = ss.getRange(1, day, ss.getLastRow(), 1).getValues();
    var lastRow = values.filter(String).length;
    ss.getRange(lastRow + 1, day).setValue(JSON.stringify(kwargs));
  } catch (error) {
    Logger.log("Error occurred while logging data: " + error);
  }
}

// Function to get the value of a cell in a spreadsheet
function getCellValue(sheet, row, day) {
  return sheet.getRange(row, day).getValue();
}

// Function to set the value of a cell in a spreadsheet
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

function checkWalletValue(sheet, walletName = null, newDay) {

  if (walletName) {
    const walletRow = findWalletRow(walletName);
    if (!isNaN(walletRow)) {
      const walletValue = getCellValue(sheet, walletRow, newDay);
      return {
        wallet: walletName,
        value: walletValue
      };
    } else {
      return {
        error: "Invalid wallet name"
      };
    }
  } else {
    const walletValues = {};
    const walletNames = ["Wallet", "SCB", "BLB", "True Wallet", "BLANK", "Red Card", "MRT Card", "BTS Card"];
    for (let name of walletNames) {
      const walletRow = findWalletRow(name);
      const walletValue = getCellValue(sheet, walletRow, newDay);
      walletValues[name] = walletValue;
    }
    return walletValues;
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
      "date": day,
      "action": action,
      "types": types,
      "amount": rawAmount,
      "updatedDeposit": parseFloat(updatedTypeValue).toFixed(2),
      "wallet": walletName,
      "updatedWallet": parseFloat(updatedWalletValue).toFixed(2),
    });

    return {
      "Date": day,
      "Types": types,
      "Amount": rawAmount,
      "Updated Deposit": updatedTypeValue,
      "Wallet": walletName,
      "Updated Wallet": updatedWalletValue,
    };
  } else {
    Logger.log("Invalid typeRow or walletRow provided.");
  }
}

function handleTransfer(sheet, walletName, destinationWalletName, rawAmount, day, action) {
  const walletOriginRow = findWalletRow(walletName);
  const walletDestinationRow = findWalletRow(destinationWalletName);

  const currentWalletOriginValue = getCellValue(sheet, walletOriginRow, day);
  const currentWalletDestinationValue = getCellValue(sheet, walletDestinationRow, day);

  if (walletOriginRow !== walletDestinationRow) {
    sheet.getRange(walletOriginRow, day).setValue(currentWalletOriginValue - rawAmount);
    sheet.getRange(walletDestinationRow, day).setValue(currentWalletDestinationValue + rawAmount);


    logTemp({
      "day": day,
      "action": "transfer",
      "amount": rawAmount,
      "currentWallet": walletName,
      "currentValue": currentWalletOriginValue - rawAmount,
      "destinationWallet": destinationWalletName,
      "destinationValue": currentWalletDestinationValue + rawAmount,
    });

    return {
      "Day": day,
      "Amount": rawAmount,
      "Origin Wallet": walletName,
      "Updated Origin Value": currentWalletOriginValue - rawAmount,
      "Destination Wallet": destinationWalletName,
      "Updated Destination Value": currentWalletDestinationValue + rawAmount,
    };

  } else {
    Logger.log("Error: Invalid wallet or day");
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

// Function to test the doGet function
function testDoGet() {
  const e = {
    //handleTransfer(sheet, walletName, destinationWalletName, rawAmount, day)
    parameter: { 'action': 'check', 'wallet_id': 'SCB', 'date': '2023-11-01'}
  };

  // date 1 Mon Jan 01 00:00:00 GMT+07:00 2001
  // date 12 Sat Dec 01 00:00:00 GMT+07:00 2001

  doGet(e);
}


// ##########################################################


// Function to handle modifications to transactions
/* Fr this part need ID for modify else gonna be thought
// ain't sure what exactly this part should do

// Replace Old Value
// Change That Transaction Amount

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
      "day": day,
      "action": "modify",
      "New Type": newType,
      "amount": rawAmount,
      "wallet": walletName,
      "BeforeChangeValue": currentWalletOriginValue,
      "AfterChangeValue": updatedWalletValue,
    });

    return {
      "day": day,
      "action": "modify",
      "New Type": newType,
      "amount": rawAmount,
      "wallet": walletName,
      "before change value": currentWalletOriginValue,
      "after change value": updatedWalletValue,
    };

  } else if (expenseTypeRow !== null && newDate) {
    const currentWalletOriginValue = getCellValue(sheet, walletRow, newDate);
    const updatedWalletValue = currentWalletOriginValue - rawAmount;

    sheet.getRange(walletRow, newDate).setValue(updatedWalletValue);
    sheet.getRange(expenseTypeRow, newDate).setValue(rawAmount);

    logTemp({
      "day": day,
      "action": "modify",
      "walletName": walletName,
      "newType": newType,
      "amount": rawAmount,
      "currentWalletValue": currentWalletOriginValue || 0,
      "updatedWalletValue": updatedWalletValue,
    });

    return {
      "day": day,
      "action": "modify",
      "wallet": walletName,
      "newType": newType,
      "old wallet amount": currentWalletOriginValue || 0,
      "amount": rawAmount,
      "new wallet amount": updatedWalletValue,
      "new amount": rawAmount,
    };
  }
}
*/



