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
    pay = sheet.worksheet(str(datetime.datetime.now().strftime("%B")))

    return pay

getValue()

def everydayValue():
    data = dataNow()

    rawData = []
    sumList = []

    for a in range(11, 22):

        rawData.append(data.row_values(a)[1:])
    
    for x in rawData:   

        sumList.append(sum([float(y.replace(',', '')) for y in x if y != '']))

    return sumList

 
def historyData(method, types, money): # upload?types=ข้าวเช้า&money=20

    import time

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

    sentence = f'[{time.strftime("%H:%M", time.localtime())}, {method}, {types}, {money}]'
    pays.update_cell(count, day, sentence)
        

    return None
