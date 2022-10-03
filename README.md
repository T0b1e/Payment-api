# Documentation

# About route

## Introduction

I have made payment api for easier way to record ledger in that time in google sheet, First of all when i planned first idea was making website of Led interface to show as dashboard how is it going and after i done that idea i had thinking that may took a while of less effiecntly so i decide to make it better by using API and connected with shortcut from any ios platfrom for instnce iphone ipad applewatch and ETC.  <br>

---

In this project API i had using flask, It seem it will be better to working with API and data in the same time.

---

## index : None <br>
    `/` 
    `requirment parameter: date (Int)(Reason for correctly sync date time at your time zone)`

---

## today : แสดงผลลัพธ์ค่าใช้จ่ายของแต่ละประเภทในวันนี้ <br>
    ` /today?todaysync=0` 
    `requirment parameter: date (Int)(Reason for correctly sync date time at your time zone)`

---

## yesterday : แสดงผลลัพธ์ค่าใช้จ่ายของแต่ละประเภทเมื่อวาน <br>
    ` /yesterday?today=0`
    `requirment parameter: date (Int)(Reason for correctly sync date time at your time zone)`

---

## everyday : แสดงผลลัพธ์ค่าใช้จ่ายของแต่ละประเภทภายในเดือนนี้ <br>
    `/everyday?today=0`
    `requirment parameter: date (Int)(Reason for correctly sync date time at your time zone)`

---

## custom : แสดงผลลัพธ์ค่าใช้จ่ายของแต่ละประเภทในวันที่ระบุ (1-31) <br>
    `/custom?day=0&today=0`
    `requirment parameter: day (Int)`

---

## upload : สำหรับอัพโหลดค่าต่างๆ โดยระบุประเภทที่เจาะจง รวมถึงงบประมาณการเงินที่ได้ใช้ลงไปเช่น รายรับ หรือรายจ่าย <br>
    `/upload?types=รายได้&money=0`

    `requirment parameter: 
    1. types (str) !! includeing
    "เงินเดือน" "รายได้" "เพื่อนคืนเงิน" "อื่นๆ" 

    "ข้าวเช้า" "ข้าวเที่ยง" "ข้าวเย็น" "ขนม/น้ำดื่ม"
    "เซเว่น" "ค่าเดินทาง" "อุปกรณ์การศึกษา/กีฬา"
    "ค่าสังสรรค์" "อุปกรณ์ไฟฟ้า" "ลงทุน (เงินส่วนตัว)"
    "อื่นๆ"  

    2. money (Int) !! 
    3. date (Int)(Reason for correctly sync date time at your time zone) !!`

---

## edit : สำหรับช่องที่ต้องการแก้ไขค่าช่องโดยทำการระบุวันที่ ที่ต้องการ และจำนวนเงินที่ต้องการแก้ไข <br>
    `/edit?dateType=custom&dateSpecific=1&types=รายได้&money=0&today=0`
    `/edit?dateType=today&dateSpecific=0&types=รายได้&money=0&today=0`
    
    `requirment parameter: 
    1. dateType (str) : today, custom           
    2. dateSpecific (str) : If you pick dateType as custom Else Error
    3. types (str) includeing
        "เงินเดือน" "รายได้" "เพื่อนคืนเงิน" "อื่นๆ" 
        "ข้าวเช้า" "ข้าวเที่ยง" "ข้าวเย็น" "ขนม/น้ำดื่ม"
        "เซเว่น" "ค่าเดินทาง" "อุปกรณ์การศึกษา/กีฬา"
        "ค่าสังสรรค์" "อุปกรณ์ไฟฟ้า" "ลงทุน (เงินส่วนตัว)"
        "อื่นๆ" 
    4. money (Int)
    5. date (Int)(Reason for correctly sync date time at your time zone)`
