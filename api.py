from main import *
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    data = findValue()
    return {"date": data[0],
            "daily": data[1],
            "avg": data[5],
            "remain": data[2],
            "max": data[3],
            "min": data[4]}

@app.route("/daily")
def daily():
    data = findValue()
    return {"daily": data[1]}

@app.route("/average")
def avg():
    data = findValue()
    return {"avg": data[5]}

@app.route("/remain")
def remain():
    data = findValue()
    return {"remain": data[2]}

@app.route("/max")
def maxs():
    data = findValue()
    return {"max": data[3]}
    # {"max":"\u0e04\u0e48\u0e32\u0e40\u0e14\u0e34\u0e19\u0e17\u0e32\u0e07"}

@app.route("/min")
def mins():
    data = findValue()
    return {"min": data[4]}

@app.route("/upload", methods = ['GET'])
def upload():

    sheet = getValue()
    day = int(datetime.datetime.now().strftime("%d")) + 1
    pay = sheet.worksheet(str(datetime.datetime.now().strftime("%B")))

    data = request.args.get('types')

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

    text=""
    numbers=""
    res=[]

    for i in data:
        if(i.isdigit()):
            numbers+=i
        else:
            text+=i
    res.append(text)
    res.append(numbers)

    for x, y in dic.items():
        
        if res[0] == x:
            types = y[1]

    record = pay.cell(types, day).value

    if record == None :
        new_record = res[1]
        pay.update_cell(types, day,res[1])
    else:
        new_record =  int(record) + int(res[1])
        pay.update_cell(types, day, new_record)

    return {'message': True}, 200

# flask --app api run