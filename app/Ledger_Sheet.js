const now = new Date();

const MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

const month = MONTH_NAMES[now.getMonth()];
const day = now.getDate() + 1;

const timeFormat = new Intl.DateTimeFormat('en-TH', {
  hour: 'numeric',
  minute: 'numeric',
  second: 'numeric',
  hour12: false, 
});

function doGet(e) {
  try {

    const params = e.parameter;
    const action = params.action;
    const walletName = params.wallet_id;
    const walletAfterAdded = params.wallet_after_balance;
    const types = params.types;
    const rawAmount = parseFloat(params.rawAmount) || 0;

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(month);

    let resText = "";

    if (action === "income" || action === "expense") {
      resText = JSON.stringify(handleTransaction(sheet, walletName, walletAfterAdded, types, rawAmount, day, action));
    } 
    
    const response =  resText ? JSON.parse(resText) : ""

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

function getCellValue(sheet, row, day) {
  return sheet.getRange(row, day).getValue();
}

function setCellValue(sheet, row, day, value) {
  sheet.getRange(row, day).setValue(value);
}

function handleTransaction(sheet, walletName, walletAfterAdded, types, rawAmount, day, action) {
    const typeRow = findRow(action, types);
    const walletRow = findWalletRow(walletName);

    if (typeRow !== null && walletRow !== null) {

        const updatedTypeValue = rawAmount;
        const updatedWalletValue = walletAfterAdded;

        sheet.getRange(typeRow, day).setValue(updatedTypeValue);
        sheet.getRange(walletRow, day).setValue(updatedWalletValue);

        return {
            "Date": day,
            "Types": types,
            "Amount": rawAmount,
            "Updated Deposit": updatedTypeValue,
            "Wallet": walletName,
            "Updated Wallet": updatedWalletValue,
        };

    } else {

        console.log("Invalid typeRow or walletRow provided.");
        return null;
    }
}

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

function findIncomeTypeRow(incomeType) {
  switch (incomeType) {
    case "เงินเดือน": return 13;
    case "รายได้": return 14;
    case "ได้รับ": return 15;
    case "อื่นๆ": return 16;
    default: return null;
  }
}

function findExpenseTypeRow(expenseType) {
  switch (expenseType) {
    case "ข้าวเช้า": return 19;
    case "ข้าวเที่ยง": return 20;
    case "ข้าวเย็น": return 21;
    case "ขนม/น้ำดื่ม": return 22;
    case "ร้านสะดวกซื้อ": return 23;
    case "ค่าเดินทาง": return 24;
    case "อุปกรณ์การศึกษา/กีฬา": return 25;
    case "ของเล่น": return 26;
    case "ค่าสังสรรค์": return 27;
    case "อุปกรณ์ไฟฟ้า": return 28;
    case "หอพัก/เฟอร์นิเจอร์": return 29;
    case "เครื่องนุ่งห่ม/เครื่องสำอาง": return 30;
    case "ลงทุน": return 31;
    case "อื่นๆ": return 32;
    default: return null;
  }
}

function testDoGet() {
      e = {
        'parameter': {
            'action': 'income',
            'wallet_id': 'SCB',
            'types': 'เงินเดือน',
            'rawAmount': 100.0,
            'wallet_after_balance': 1500.0,
        }
    }
  doGet(e);
}




