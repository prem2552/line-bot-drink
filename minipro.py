def pn():
    exit = "Y"
    while exit != "N":
        phone = str(input("ใส่เบอร์ของคุณ: "))
        length = len(phone)
        if phone == "+66963861033":
            print("สวัสดีครับคุณปิติภัทร")

        elif phone.startswith("+66") and length == 12:
            print("รหัสเบอร์โทรศัพท์ประเทศไทย")

        elif phone.lstrip("+").isnumeric() == False:
            print("กรุณากรอกเบอร์โทรศัพท์ใหม่ครับ")
        elif phone.startswith("+") and length <= 15:
            while True:
                country = str(input("What country are your from: "))
                country = country.upper()
                if ("THAI" in country) == True:
                    print("Please fill in the information correctly.")
                else:
                    print("Thank you for using the service.")
                    break
        else:
            print("กรุณาใส่เบอร์โทรศัพท์ครับ/Please enter your phone number.")
        exit = str(input("คุณต้องการทำรายการนี้ต่อมั้ย (Y/N): "))
        exit = exit.upper()


pn()
