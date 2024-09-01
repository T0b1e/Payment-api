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
    let types = params.types;

    types = types === "snacks" ? "ขนม/น้ำดื่ม" :
            types === "sports" ? "อุปกรณ์การศึกษา/กีฬา" :
            types === "furnitures" ? "หอพัก/เฟอร์นิเจอร์" :
            types === "clothings" ? "เครื่องนุ่งห่ม/เครื่องสำอาง" :
            types === "investment" ? "ลงทุน (เงินส่วนตัว)":
            types;

    const rawAmount = parseFloat(params.rawAmount) || 0;
    const description = params.descriptions;

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(month);

    let resText = "";

    if (action === "income" || action === "expense") {
      resText = JSON.stringify(handleTransaction(sheet, walletName, walletAfterAdded, types, rawAmount, day, action, description));
    } 
    
    const response =  resText ? JSON.parse(resText) : ""

    console.log(response)

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

function handleTransaction(sheet, walletName, walletAfterAdded, types, rawAmount, day, action, description) {
    const typeRow = findRow(action, types);
    const walletRow = findWalletRow(walletName);

    if (typeRow !== null && walletRow !== null) {

        const updatedTypeValue = rawAmount;
        const updatedWalletValue = walletAfterAdded;

        // sheet.getRange(typeRow, day).setValue(updatedTypeValue);
        // sheet.getRange(typeRow + 1, day).setValue(description);
        sheet.getRange(typeRow, day).setValue(updatedTypeValue).offset(1, 0).setValue(description);
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
    case "รายได้": return 15;
    case "ได้รับ": return 17;
    case "อื่นๆ": return 19;
    default: return null;
  }
}

function findExpenseTypeRow(expenseType) {
  switch (expenseType) {
    case "ข้าวเช้า": return 23;
    case "ข้าวเที่ยง": return 25;
    case "ข้าวเย็น": return 27;
    case "ขนม/น้ำดื่ม": return 29;
    case "ร้านสะดวกซื้อ": return 31;
    case "ค่าเดินทาง": return 33;
    case "อุปกรณ์การศึกษา/กีฬา": return 35;
    case "ของเล่น": return 37;
    case "ค่าสังสรรค์": return 39;
    case "อุปกรณ์ไฟฟ้า": return 41;
    case "หอพัก/เฟอร์นิเจอร์": return 43;
    case "เครื่องนุ่งห่ม/เครื่องสำอาง": return 45;
    case "ลงทุน": return 47;
    case "อื่นๆ": return 49;
    default: return null;
  }
}

function testDoGet() {
      e = {
        'parameter': {
            'action': 'income',
            'wallet_id': 'BLB',
            'types': 'ได้รับ',
            'rawAmount': 100.0,
            'wallet_after_balance': 1500.0,
            'descriptions': 'test test',
        }
    }
  doGet(e);
}




