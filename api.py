from main import *
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)   

# -*- coding: utf-8 -*-

day = int(datetime.now().strftime("%d")) # Becasue in first column we are already start with title TODAY
pay = dataNow()

# sheet = getValue()
# sumsSheet = sheet.worksheet(f'SumDaily{str(datetime.datetime.now().strftime("%B"))[:3]}')

### Specify Column

DIC = {
"เงินเดือน"   :["salary", 5],
"รายได้"   :["income", 6],
"เพื่อนคืนเงิน"   :["friend", 7],
"อื่นๆ"   :["salary_etc.", 8],
"ข้าวเช้า"    :["breakfast", 11],
"ข้าวเที่ยง"   :["lunch", 12],
"ข้าวเย็น"    :["dinner", 13],
"ขนม/น้ำดื่ม" :["snack", 14],
"เซเว่น"     :["seven-eleven", 15],
"ค่าเดินทาง"  :["travel", 16],
"อุปกรณ์การศึกษา/กีฬา":["education", 17],
"ค่าสังสรรค์"  :["entertainment", 18],
"อุปกรณ์ไฟฟ้า" :["tools", 19],
"ลงทุน (เงินส่วนตัว)":["invest", 20],
"อื่นๆ"       :["etc.", 21]
}

@app.route("/")
def index():
    return {'messgae': True}, 200


@app.route("/today", methods = ['GET']) # today?todaysync=0
def today():

    try:

        todayDateGet = int(request.args.get('today')[:2]) # 8 ต.ค. 2565 23:51

    except ValueError:

        todayDateGet = day

    except TypeError:

        todayDateGet = day

        # todayDateGet if todayDateGet  != day else todayDateGet 

    todayDateGet = int(todayDateGet)

    try:
        todayRaw = pay.col_values(todayDateGet + 1)[10:21] # todayRaw --> output Add 1 beacuse first column index is strated with title

        todayData = []

        for x in todayRaw:
            if x == "" or x == None:
                todayData.append(0)
            else:
                todayData.append(round(int(str(x).replace(',', '')), 2))
        
        return {
                "วัน"        : f'{todayDateGet}',
                "ข้าวเช้า"    : todayData[0],
                "ข้าวเที่ยง"   : todayData[1],
                "ข้าวเย็น"    : todayData[2],
                "ขนม/น้ำดื่ม" : todayData[3],
                "เซเว่น"     : todayData[4],
                "ค่าเดินทาง"  : todayData[5],
                "อุปกรณ์การศึกษา/กีฬา": todayData[6],
                "ค่าสังสรรค์"  : todayData[7],
                "อุปกรณ์ไฟฟ้า" : todayData[8],
                "ลงทุน (เงินส่วนตัว)": todayData[9],
                "อื่นๆ"       : todayData[10],
                "ยอดรวม": sum([i for i in todayData]),
                "คงเหลือ": pay.col_values(todayDateGet + 1)[22],
                }

    except TypeError:

        return {'message': 'ต้นเดือน'}, 401


@app.route("/yesterday", methods = ['GET']) # yesterday?today=0 get yesterday value
def yesterday():

    try:

        todayDateGet = int(request.args.get('today')[:2])

    except ValueError:

        todayDateGet = day

    except TypeError:

        todayDateGet = day

    todayDateGet = int(todayDateGet)
    
    todayRaw = pay.col_values(todayDateGet)[10:21] # todayRaw --> output
    todayData = []
    try:
        for x in todayRaw:
            if x == "" or None:
                todayData.append(0)
            else:
                todayData.append(round(int(str(x).replace(',', '')), 2))
        return {
                "วัน"        : f'{todayDateGet - 1}',
                "ข้าวเช้า"    : todayData[0],
                "ข้าวเที่ยง"   : todayData[1],
                "ข้าวเย็น"    : todayData[2],
                "ขนม/น้ำดื่ม" : todayData[3],
                "เซเว่น"     : todayData[4],
                "ค่าเดินทาง"  : todayData[5],
                "อุปกรณ์การศึกษา/กีฬา": todayData[6],
                "ค่าสังสรรค์"  : todayData[7],
                "อุปกรณ์ไฟฟ้า" : todayData[8],
                "ลงทุน (เงินส่วนตัว)": todayData[9],
                "อื่นๆ"       : todayData[10],
                "ยอดรวม": sum([i for i in todayData]),
                "คงเหลือ":  0 if pay.col_values(todayDateGet)[4] == "" else pay.col_values(todayDateGet)[4],
                }

    except ValueError:

        return {'message': 'ต้นเดือน'}, 401

@app.route("/everyday", methods = ['GET']) # everyday?today=0 to recieve end date
def everyday():

    try:

        todayDateGet = int(request.args.get('today')[:2])

    except ValueError:

        todayDateGet = day

    except TypeError:

        todayDateGet = day

    todayDateGet = int(todayDateGet)

    e = everydayValue()
    return {
            "วัน"        : f'1 --> {todayDateGet}',
            "ข้าวเช้า"    : e[0],
            "ข้าวเที่ยง"   : e[1],
            "ข้าวเย็น"    : e[2],
            "ขนม/น้ำดื่ม" : e[3],
            "เซเว่น"     : e[4],
            "ค่าเดินทาง"  : e[5],
            "อุปกรณ์การศึกษา/กีฬา": e[6],
            "ค่าสังสรรค์"  : e[7],
            "อุปกรณ์ไฟฟ้า" : e[8],
            "ลงทุน (เงินส่วนตัว)": e[9],
            "อื่นๆ"       : e[10],
            "ยอดรวม": round(sum([i for i in e]), 2),
            "คงเหลือ": pay.col_values(31)[22],
            }

@app.route("/custom", methods = ['GET']) # custom?today=0
def custom():

    todayDateGet = int(request.args.get('today'))[:2] # Custom date Specific date

    data = pay.col_values(todayDateGet + 1)
    customRaw = data[10:21] # from ข้าวเช้า untile ยอดรวม
    output = pay.col_values(todayDateGet + 1)[4] # คงเหลือ
    today = []

    for x in customRaw:
        if x == "" or None:
            today.append(0)
        else:
            today.append(round(int(str(x).replace(',', '')), 2))
            
    return {
            "วัน"        : f'{todayDateGet}',
            "ข้าวเช้า"    : today[0],
            "ข้าวเที่ยง"   : today[1],
            "ข้าวเย็น"    : today[2],
            "ขนม/น้ำดื่ม" : today[3],
            "เซเว่น"     : today[4],
            "ค่าเดินทาง"  : today[5],
            "อุปกรณ์การศึกษา/กีฬา": today[6],
            "ค่าสังสรรค์"  : today[7],
            "อุปกรณ์ไฟฟ้า" : today[8],
            "ลงทุน (เงินส่วนตัว)": today[9],
            "อื่นๆ"       : today[10],
            "ยอดรวม": sum([i for i in today]),
            "คงเหลือ": output,
            }


@app.route("/upload", methods = ['GET']) # upload?today=0&types=ข้าวเช้า&money=0
def upload():

    try:

        dateAndTime = request.args.get('today')# 2 Oct BE 2565 19:22 Sync time

        todayDateGet = int(dateAndTime[:2]) # Should be not error as not any device
        timeGet = dateAndTime[14:] # It can be error if device input type isn't from iphone

        types = request.args.get('types')
        money = int(request.args.get('money'))

    except ValueError:

        todayDateGet = int(day)
        timeGet = str(datetime.now())[11:16]

        types = 'อื่นๆ'
        money = 0
    
    except TypeError:

        todayDateGet = int(day)
        timeGet = str(datetime.now())[11:16]

        types = 'อื่นๆ'
        money = 0

    historyData('upload', types, money, timeGet)

    for x, y in DIC.items():
        if types == x:
            types = y[1]

    record = pay.cell(types, todayDateGet + 1).value

    # print(dateAndTime, todayDateGet, timeGet, types, money)

    try:

        if record == None or '': # if there is blank cell
            pay.update_cell(types, todayDateGet + 1, money) # update money into nontype cell
            return {'Result': f'0 --> {money}',
                    'Remain': pay.cell(23, todayDateGet + 1).value}, 200

        elif money == 0:
            # pay.update_cell(types, day, money) # update money into nontype cell
            return {'Result': 'Noting new' if record == None else 'Noting change',
                    'Remain': pay.cell(23, todayDateGet + 1).value}, 200

        else:
            remain = round(float(pay.cell(23, todayDateGet + 1).value) - (float(record) + money), 2)

            pay.update_cell(types, todayDateGet + 1, int(record) + money)

            # sumsSheet.update_cell(todayDateGet + 1, 2, pay.cell(todayDateGet + 1, 2).value)
            # sumsSheet.update_cell(todayDateGet + 1, 3, remain)

            return {'Result': f'{record} --> {int(record) + money}',
                    'Remain':remain }, 200

    except TypeError:

        return {'Result': 0,
                'remain': 0}, 404

@app.route("/edit") # edit?dateType=custom&dateSpecific=1&types=ข้าวเช้า&money=0&today=0
def edit():

    try:

        dateAndTime = request.args.get('today') # it will get ignore if you using dateType as not custom
        todayDateGet = int(dateAndTime[:2])
        timeGet = dateAndTime[14:] # It can be error if device input type isn't from iphone
        
        ### If you picking CUSTOM
        dateType = request.args.get('dateType') # custom
        dateSpecific = int(request.args.get('dateSpecific')) + 1 # Specify date

        ### Information
        types = request.args.get('types')
        money = int(request.args.get('money'))

    except ValueError:

        todayDateGet = int(day)
        timeGet = str(datetime.now())[11:16]

        dateType = 'custom'
        dateSpecific = 1

        types = 'อื่นๆ'
        money = 0

    except TypeError:

        todayDateGet = int(day)
        timeGet = str(datetime.now())[11:16]

        dateType = 'custom'
        dateSpecific = 1

        types = 'อื่นๆ'
        money = 0

    historyData('edit', types, money, timeGet)

    for x, y in DIC.items():
         if types == x:
            types = y[1]

    if dateType == 'today':

        record = pay.cell(types, todayDateGet + 1).value

        if record ==  None:

            return {'message': 'There has no money yet on record yet'}

        else:

            pay.update_cell(types, todayDateGet + 1, money) 

    else: # Custom

        if dateSpecific != 0:
            record = pay.cell(types, dateSpecific).value

            if record == None:

                return {'message': 'There has no money on record yet'}
            
            else:

                pay.update_cell(types, dateSpecific, money) 

                day = dateSpecific - 1

    money = int(money)
    record = int(record)

    diff = money - record if money > record else record - money

    return {
            "วัน"        : f'{day}',
            "ผลลัพธ์" : f'เปลี่ยนค่าจาก {record} --> {money}' if record != None and money != None and money != 0 and record != money else 'ไม่มีการเปลี่ยนแปลง',
            "ผลต่าง": f' ผลต่าง {diff}' if diff != 0 else 'ไม่มีการเปลี่ยนแปลง',
            }

@app.errorhandler(404)
def page_not_found():
    return 'This page does not exist', 404

# flask --app api run