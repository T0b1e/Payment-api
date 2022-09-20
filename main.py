import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime 



def getValue():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("keys.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open('Payments')

    return sheet

dic = {
    "ข้าวเช้า"    :"breakfast",
    "ข้าวเที่ยง"   :"lunch",
    "ข้าวเย็น"    :"dinner",
    "ขนม/น้ำดื่ม" :"snack",
    "เซเว่น"     :"seven-eleven",
    "ค่าเดินทาง"  :"travel",
    "อุปกรณ์การศึกษา/กีฬา":"education",
    "ค่าสังสรรค์"  :"entertainment",
    "อุปกรณ์ไฟฟ้า" :"tools",
    "ลงทุน (เงินส่วนตัว)":"invest",
    "อื่นๆ"       :"etc."
}

def dataNow():
    sheet = getValue()
    pay = sheet.worksheet(str(datetime.datetime.now().strftime("%B")))
    return pay

def everydayValue():
    data = dataNow()

    rawData = []
    sumList = []

    for a in range(11, 22):

        rawData.append(data.row_values(a)[1:])
    
    for x in rawData:   

        sumList.append(sum([float(y.replace(',', '')) for y in x if y != '']))

    return sumList


