from main import *
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

day = int(datetime.now().strftime("%d")) # Becasue in first column we are already start with title TODAY
pay = dataNow()

@app.route("/")
def index():
    return {'messgae': True}, 200


@app.route("/today")
def today():
    try:
        todayRaw = pay.col_values(day + 1)[10:21] # todayRaw --> output
        today = []
        for x in todayRaw:
            if x == "" or x == None:
                x = 0
                today.append(0)
            else:
                today.append(round(int(str(x).replace(',', '')), 2))
        
        return {
                "วัน"        : f'{day}',
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
                "คงเหลือ": pay.col_values(day)[22],
                }

    except TypeError:

        return {'message': 'ต้นเดือน'}, 401


@app.route("/yesterday")
def yesterday():
    todayRaw = pay.col_values(day)[10:21] # todayRaw --> output
    today = []
    try:
        for x in todayRaw:
            if x == "" or None:
                today.append(0)
            else:
                today.append(round(int(str(x).replace(',', '')), 2))
        return {
                "วัน"        : f'{day - 1}',
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
                "คงเหลือ":  0 if pay.col_values(day)[4] == "" else pay.col_values(day)[4],
                }

    except TypeError:
        return {'message': 'ต้นเดือน'}, 401

@app.route("/everyday")
def everyday():
    e = everydayValue()
    return {
            "วัน"        : f'1 --> {day}',
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

@app.route("/custom", methods = ['GET'])
def custom():

    date = int(request.args.get('day'))

    data = pay.col_values(date + 1)
    customRaw = data[10:21]
    output = data[22]
    today = []

    for x in customRaw:
        if x == "" or None:
            x = 0
            today.append(0)
        else:
            x = x.replace(',', '')
            today.append(round(int(str(x).replace(',', '')), 2))
            
    return {
            "วัน"        : f'{date}',
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


@app.route("/upload", methods = ['GET'])
def upload():

    try:

        types = request.args.get('types')
        money = int(request.args.get('money'))

    except ValueError:

        types = 'อื่นๆ'
        money = 0

    dic = {
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

    historyData('upload', types, money)

    for x, y in dic.items():
        if types == x:
            types = y[1]

    record = pay.cell(types, day).value

    try:

        if record == None or '': # if there is blank cell
            pay.update_cell(types, day, money) # update money into nontype cell
            return {'Attemp': f'0 --> {money}',
                    'remain': pay.cell(23, day).value}, 200

        elif money == 0:
            # pay.update_cell(types, day, money) # update money into nontype cell
            return {'Attemp': 'Noting new' if record == None else 'Noting change',
                    'remain': pay.cell(23, day).value}, 200

        else:
            pay.update_cell(types, day, int(record) + money)
            return {'Attemp': f'{record} --> {int(record) + money}',
                    'remain': float(pay.cell(23, day).value) - (float(record) + money)}, 200

    except TypeError:

        return {'Attemp': 0,
                'remain': 0}, 404

@app.route("/edit")
def edit():

    dateType = request.args.get('dateType')
    dateSpecific = int(request.args.get('dateSpecific')) + 1
    types = request.args.get('types')
    money = int(request.args.get('money'))
    
    dic = {
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

    historyData('edit', types, money)

    for x, y in dic.items():
         if types == x:
            types = y[1]

    if dateType == 'today':

        record = pay.cell(types, day + 1).value

        if record ==  None:

            return {'message': 'There has no money yet on record yet'}

        else:

            pay.update_cell(types, day + 1, money) 

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
            "ผลลัพธ์" : f'เปลี่ยนค่าจาก {record} --> {money}' if record != None and money != None and money != 0 else 'ไม่มีการเปลี่ยนแปลง',
            "ผลต่าง": f' ผลต่าง {diff}' if diff != 0 else 'ไม่มีการเปลี่ยนแปลง',
            }



# flask --app api run