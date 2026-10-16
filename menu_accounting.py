# [1 = รายรับ - รายจ่าย, 2 = บันทึก Diary,  นอกนั้นออกจากโปรแกรม]
from accounting_prem import add_transaction, update_averrage
from diary_prem import update_diary
from setup import setup


def menu():
    work = setup()

    while True:
        print("1 = รายรับ - รายจ่าย, 2 = บันทึก Diary,  พิมพ์อะไรก็ได้เพื่อออกจากระบบ")
        key_word = int(input("ต้องการทำรายการอะไร?: "))

        if key_word == 1:
            work_sheet2 = work.worksheet("รายรับรายจ่าย2")
            work_sheet3 = work.worksheet("เฉลี่ย")

            add_transaction(work_sheet2)
            update_averrage(work_sheet2, work_sheet3)

        elif key_word == 2:
            work_sheet4 = work.worksheet("Diary")

            update_diary(work_sheet4)

        else:
            print("ออกจากระบบแล้วครับ")
            break


# key_continue = str(input("ต้องการทำรายการอะไรเพิ่มมั้ย (Y/N)? :"))


menu()
