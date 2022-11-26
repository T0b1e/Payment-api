import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime 

def getValue():

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("keys.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open('Payments')

    # sb = sheet.share('narongkorn@tobpayment.iam.gserviceaccount.com', perm_type='user', role='editor')
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
    pay = sheet.worksheet(str(datetime.datetime.now().strftime("%B"))) # Current month

    return pay

# getValue()

def everydayValue():

    data = dataNow()

    rawData = []
    sumList = []

    for a in range(11, 22):

        rawData.append(data.row_values(a)[1:])
    
    for x in rawData:   

        sumList.append(round(sum([float(y.replace(',', '')) for y in x if y != '']), 2))

    return sumList


def historyData(method, types, money, times): # upload?types=ข้าวเช้า&money=20

    day = int(datetime.datetime.now().strftime("%d")) + 1

    sheet = getValue()
    pays = sheet.worksheet(f'History{str(datetime.datetime.now().strftime("%B"))[:3]}')
    data = pays.col_values(day)
    count = 1
    
    for x in data:
        if x != None or '': # มีข้อมูลด้านใน
            count += 1
        else: # ไม่มีข้อมูลด้านใน
            break

    sentence = f'[{times}, {method}, "{types}", {money}]'
    pays.update_cell(count, day, sentence)
        

    return None

def appendSum():

    sheet = getValue()
    getData = dataNow() # Current month value
    updateSheet = sheet.worksheet(f'SumDaily{str(datetime.datetime.now().strftime("%B"))[:3]}') # Update Sheet

    sums = getData.row_values(22)[1:]
    remain = getData.row_values(23)[1:]
    count = 0

    for x in range(2, 33):
        updateSheet.update_cell(x, 2, 0 if sums[count] == None else sums[count])
        updateSheet.update_cell(x, 3, 0 if remain[count] == None else remain[count])
        count += 1
    
# appendSum()