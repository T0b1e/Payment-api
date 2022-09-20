from main import *
from flask import Flask, request

app = Flask(__name__)

day = int(datetime.datetime.now().strftime("%d")) + 1
pay = dataNow()

@app.route("/")
def index():
    return {'messgae': True}, 200


@app.route("/today")
def today():
    todayRaw = pay.col_values(day)[10:21]
    today = []
    for x in todayRaw:
        if x == "":
            x = 0
            today.append(x)
        else:
            today.append(x)

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
            }

@app.route("/yesterday")
def yesterday():
    todayRaw = pay.col_values(day - 1)[10:21]
    today = []
    for x in todayRaw:
        if x == "":
            x = 0
            today.append(x)
        else:
            today.append(x)
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
            }

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
            }

@app.route("/custom", methods = ['GET'])
def custom():

    date = int(request.args.get('day'))

    customRaw = pay.col_values(date + 1)[10:21]
    today = []
    for x in customRaw:
        if x == "":
            x = 0
            today.append(x)
        else:
            today.append(x)
            
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

    for x, y in dic.items():
        if types == x:
            types = y[1]

    record = pay.cell(types, day).value

    try:

        if record == None : # if there is blank cell
            pay.update_cell(types, day, money) # update money into nontype cell
            return {'Attemp': f'0 --> {money}',
                    'remain': pay.cell(23, day).value}, 200

        elif money == 0 and record != None:
            # pay.update_cell(types, day, money) # update money into nontype cell
            return {'Attemp': f'{record} Noting change',
                    'remain': pay.cell(23, day).value}, 200

        else:
            pay.update_cell(types, day, int(record) + money)
            return {'Attemp': f'{record} --> {int(record) + money}',
                    'remain': pay.cell(23, day).value - (int(record) + money)}, 200

    except TypeError:

        return {'Attemp': 0,
                'remain': 0}, 404

# flask --app api run