from flask import Flask, request
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

def findValue():
    sheet = getValue()
    day = int(datetime.datetime.now().strftime("%d")) + 1
    pay = sheet.worksheet(str(datetime.datetime.now().strftime("%B")))

    Type_str = pay.col_values(33)[10:21]

    dailyPay = pay.cell(22, day).value # ค่าใช้จ่ายรายวัน
    remainPay = pay.cell(3, day).value # ค่าใช้จ่ายคงเหลือ
    maxType = pay.cell(Type_str.index(max(Type_str)) + 11, 1).value # ประเภทที่มีค่าใช้จ่ายเยอะที่สุด
    minType = pay.cell(Type_str.index(min(Type_str)) + 11, 1).value # ค่าใช้จ่ายน้อยสุด

    for x, y in dic.items():
        if maxType == x:
            maxType = y
        elif minType == x:
            minType = y

    avg_str = pay.row_values(22)[1:]
    avg_int = [float(y) for y in avg_str]
    sum_avg = sum(avg_int) / int(day) - 1 # ค่าใช้จ่ายเฉลี่ยในเดือนนี้

    return [day, dailyPay, remainPay, maxType, minType, sum_avg]
