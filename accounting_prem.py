from gspread import Worksheet
from setup import today


def add_transaction(sheet: Worksheet):
    keyword: str = "Y"

    while keyword != "N":
        current_value: str = sheet.col_values(4)[-1]

        subject = str(input("subject : "))
        amount = int(input("amount : "))
        sum_expenses = int(current_value) + amount

        information = [today, subject, amount, sum_expenses]
        sheet.append_row(information)
        keyword = str(input("continue? (Y / N) : "))
        keyword = keyword.upper()


def update_averrage(sheet2: Worksheet, sheet3: Worksheet):
    list_of_list = sheet2.get_all_values()[1:]
    result_dict: dict[str, list[int]] = {}
    result: list[list] = (
        []
    )  # ex --> [["18/03/69", 45], ["19/03/69", 45.123], ["20/03/69", 67.123]]

    for i in list_of_list:
        A = i[0]
        C = int(i[2])

        if A in result_dict:
            result_dict[A].append(C)
        else:
            result_dict[A] = [C]

    for key, value in result_dict.items():
        averrage = sum(value) / len(value)
        averrage = round(averrage)
        value_list = [key, averrage]
        result.append(value_list)

    if len(result) > 0:
        sheet3.update(result, f"A2:B{len(result)+1}")
