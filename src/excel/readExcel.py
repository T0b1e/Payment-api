import pandas as pd

data = pd.read_excel(io="src/excel/Payments (30_11_2022).xlsx", sheet_name='November', nrows=24).fillna(value=0)

def rawData():
    # print(data)
    # clear data
    newLists = []
    for x in range(0, 23):
        newLists.append([])
        for y in range(1, 32):
            newLists[x].append(data[y][x])
    
    # clear didn't use lists 23-31
    lists = []
    for a in range(0, 23):
        if a not in [2, 5, 7, 8, 20, 21, 22]:
            lists.append(newLists[a])
            
    # transpost data
    transpost = []
    for i in range(0, 31):
        transpost.append([])
        transpost[i].append(str(i+1))
        for j in range(0, 16):
           transpost[i].append(lists[j][i])

    return transpost

# rawData()
# print(rawData())
# [23 rows x 33 columns] 17 - 30


























'''pocket = []
for a in range(0, 24): # row
    pocket.append([])
    if a not in [4, 6, 7, 9, 10, 22]:
        for x in range(1, 32): # col
            print(data[x][a])
            if str(data[x][a]) == "NaN":
                pocket[a].append(0)
            else:
                pocket[a].append(data[x][a])

    else:
        pass

# 2022-12-01 00:00:00
date = []
for d in range(1, 32):
    date.append('2022-11-{:02} 00:00:00'.format(d))

newLists = []
for a in range(0, 31):
    newLists.append([])
    for b in range(0, 17):
        newLists[a].append(lists[b][a])'''

