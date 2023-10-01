function doGet(e) {
    try {
      const params = e.parameter;
      const action = params.action;
      const walletName = params.wallet_id;
      const types = params.types;
      const rawAmount = parseFloat(params.rawAmount) || 0;
  
      const now = new Date();
      const monthNames = [
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
      ];
      const month = monthNames[now.getMonth()];
      const day = now.getDate() + 1;
  
      const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(month);
  
      if (action === "income" || action === "expense") {
        handleTransaction(sheet, walletName, types, rawAmount, day, action);
      } else if (action === "transfer") {
        const origin = params.origin;
        const destination = params.destination;
        const destinationWalletName = params.destination_wallet_id;
        handleTransfer(sheet, walletName, destinationWalletName, origin, destination, day);
      } else if (action === "modify") {
        const newDate = new Date(params.date);
        const newDay = newDate.getDate() + 1;
        const newType = params.newType; 
        handleModify(sheet, walletName, types, rawAmount, newDay);
      }
      const response = {
        statusCode: 200,
        message: "Request successfully processed.",
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
  
  function handleTransaction(sheet, walletName, types, rawAmount, day, action) {
    const typeRow = findRow(action, types);
    const walletRow = findWalletRow(walletName);
  
    if (!isNaN(typeRow) && !isNaN(walletRow)) {
      const currentTypeValue = getCellValue(sheet, typeRow, day);
      const currentWalletValue = getCellValue(sheet, walletRow, day);
  
      const updatedTypeValue = isNaN(currentTypeValue) ? 0 : currentTypeValue + rawAmount;
      const updatedWalletValue = isNaN(currentWalletValue) ? 0 : 
        action === 'income' ? currentWalletValue + rawAmount : currentWalletValue - rawAmount;
  
      setCellValue(sheet, typeRow, day, updatedTypeValue);
      setCellValue(sheet, walletRow, day, updatedWalletValue);
    } else {
      Logger.log("Invalid typeRow or walletRow provided.");
    }
  }
  
  function getCellValue(sheet, row, day) {
    return sheet.getRange(row, day).getValue();
  }
  
  function setCellValue(sheet, row, day, value) {
    sheet.getRange(row, day).setValue(value);
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
  
  function handleTransfer(sheet, walletName, destinationWalletName, origin, destination, day) {
    const walletOriginRow = findWalletRow(walletName);
    const walletDestinationRow = findWalletRow(destinationWalletName);
  
    // instead get value from API seem better
    if (walletOriginRow !== null && walletDestinationRow !== null && day) {
      sheet.getRange(walletOriginRow, day).setValue(origin);
      sheet.getRange(walletDestinationRow, day).setValue(destination);
    }
  }
  
  function handleModify(sheet, walletName, newType, rawAmount, newDate) {
    const incomeTypeRow = findIncomeTypeRow(newType);
    const expenseTypeRow = findExpenseTypeRow(newType);
    const walletRow = findWalletRow(walletName);
  
    if (incomeTypeRow !== null && newDate) {
      sheet.getRange(walletRow, newDate).setValue(rawAmount);
      sheet.getRange(incomeTypeRow, newDate).setValue(rawAmount);
    } else if (expenseTypeRow !== null && newDate) {
      sheet.getRange(walletRow, newDate).setValue(rawAmount);
      sheet.getRange(expenseTypeRow, newDate).setValue(rawAmount);
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
      case "เซเว่น": return 23;
      case "ค่าเดินทาง": return 24;
      case "อุปกรณ์การศึกษา/กีฬา": return 25;
      case "ค่าสังสรรค์": return 26;
      case "อุปกรณ์ไฟฟ้า": return 27;
      case "ลงทุน (เงินส่วนตัว)": return 28;
      case "อื่นๆ": return 29;
      default: return null;
    }
  }
  
  function testDoGet() {
    const e = {
      parameter: {'action': 'income', 'wallet_id': 'SCB', 'types': 'เงินเดือน', 'rawAmount': 123.0}
    };
  
    doGet(e); 
  }
  
  