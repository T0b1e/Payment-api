** Documentation

About route

index : None (/)
    requirment parameter: None

today : แสดงผลลัพธ์ค่าใช้จ่ายของแต่ละประเภทในวันนี้ (/today)
    requirment parameter: None

yesterday : แสดงผลลัพธ์ค่าใช้จ่ายของแต่ละประเภทเมื่อวาน (/yesterday)
    requirment parameter: None

everyday : แสดงผลลัพธ์ค่าใช้จ่ายของแต่ละประเภทภายในเดือนนี้ (/everyday)
    requirment parameter: None

custom : แสดงผลลัพธ์ค่าใช้จ่ายของแต่ละประเภทในวันที่ระบุ 
(1-31) (/custom?day=0)
    requirment parameter: day (Int)

upload : สำหรับอัพโหลดค่าต่างๆ โดยระบุประเภทที่เจาะจง รวมถึงงบประมาณการเงินที่ได้ใช้ลงไปเช่น รายรับ หรือรายจ่าย (/upload?types=รายได้&money=0)
    requirment parameter: 1. types (str) includeing
    "เงินเดือน" "รายได้" "เพื่อนคืนเงิน" "อื่นๆ" 

    "ข้าวเช้า" "ข้าวเที่ยง" "ข้าวเย็น" "ขนม/น้ำดื่ม"
    "เซเว่น" "ค่าเดินทาง" "อุปกรณ์การศึกษา/กีฬา"
    "ค่าสังสรรค์" "อุปกรณ์ไฟฟ้า" "ลงทุน (เงินส่วนตัว)"
    "อื่นๆ"  

    2. money (Int)

edit : สำหรับช่องที่ต้องการแก้ไขค่าช่องโดยทำการระบุวันที่ ที่ต้องการ และจำนวนเงินที่ต้องการแก้ไข (/edit?dateType=custom&dateSpecific=1&types=รายได้&money=0), (/edit?dateType=today&dateSpecific=0&types=รายได้&money=0)
    requirment parameter: 1. dateType (str) : today, custom
                          2. dateSpecific (str) : If you pick dateType as custom Else Error
                          3. types (str) includeing
                            "เงินเดือน" "รายได้" "เพื่อนคืนเงิน" "อื่นๆ" 

                            "ข้าวเช้า" "ข้าวเที่ยง" "ข้าวเย็น" "ขนม/น้ำดื่ม"
                            "เซเว่น" "ค่าเดินทาง" "อุปกรณ์การศึกษา/กีฬา"
                            "ค่าสังสรรค์" "อุปกรณ์ไฟฟ้า" "ลงทุน (เงินส่วนตัว)"
                            "อื่นๆ" 
                            4. money (Int)

