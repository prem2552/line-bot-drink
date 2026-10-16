import random

items = ["ค้อน", "กระดาษ", "กรรไกร"]


def rps(user):
    computer = random.choice(items)
    print(f"คอมพิวเตอร์ออก: {computer}")

    if (
        (user == "ค้อน" and computer == "กรรไกร")
        or (user == "กระดาษ" and computer == "ค้อน")
        or (user == "กรรไกร" and computer == "กระดาษ")
    ):
        print("🤩ชนะ🥳")
    elif user == computer:
        print("🤝เสมอ🤝")
    else:
        print("🤬แพ้😡")


rps(str(input("ออก ค้อน หรือ กระดาษ หรือ กรรไกร: ")))
