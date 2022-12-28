import pandas as pd

data = pd.read_excel(io="src/excel/Payments (22_12_2022).xlsx", sheet_name='December', nrows=24).fillna(value=0)

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

def defaults():
    lists = []
    for x in range(0, 31):
        lists.append([])
        lists[x].append(x + 1)
        for y in range(0, 16):
            lists[x].append(0.0)

    return lists

# rawData()
# print(rawData())
# [23 rows x 33 columns] 17 - 30
