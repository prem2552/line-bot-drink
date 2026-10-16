from gspread import Worksheet
from setup import today, time_now


def update_diary(sheet: Worksheet):
    key_dairy: str = "Y"

    while key_dairy != "N":
        subject_diary = str(input("วันนี้เขียนไรดี: "))
        information_diary = [today, time_now, subject_diary]
        sheet.append_row(information_diary)
        key_dairy = str(input("จดต่อมั้ย (Y / N) : "))
        key_dairy = key_dairy.upper()
