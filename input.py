from main import *

# Select type insert money ask changed status

def inputData():
    sheet = getValue()
    pay = sheet.worksheet(str(datetime.datetime.now().strftime("%B")))

    paymentType = input('Type: ')

    if paymentType not in dic:
        print("No exits data")

    indexs = list(dic.keys()).index(paymentType) + 11
    day = int(datetime.datetime.now().strftime("%d")) + 1

    money = int(input('How much: '))
    check = input('Are you sure (Y/n): ').lower()

    if check == 'y':
        record = pay.cell(indexs, day).value
        pay.update_cell(indexs, day, money)
        new_record = pay.cell(indexs, day).value
        print(f'{record} --> {new_record}')
    else:
        pass

    print("Done")

inputData()