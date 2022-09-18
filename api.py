from main import *
from flask import Flask

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
                    'remain': pay.cell(23, day).value}, 200

    except TypeError:

        return {'Attemp': 0,
                'remain': 0}, 404

# flask --app api run