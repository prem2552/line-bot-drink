import ssl

ssl._create_default_https_context = ssl._create_unverified_context
from flask import Flask, abort, request
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)


configuration = Configuration(
    access_token="vnsBJP9AvLUXsfOPoHS/mPjbHiwgk3IgzGGH/fWJik4e+L7ACs7Jq14UK7f+tFV1BaIaVpNbaarZdywmEtM6XhlIDFvDfMXkK5FDPT9SaHQTIefA+wcgAAWrTldI0TzX2BaDyN8xQDHpS0W3Ma46yQdB04t89/1O/w1cDnyilFU="
)
handler = WebhookHandler("b97673e4e7f87358de56cca3099995d6")


drink_recipes = {
    "A-1": """A-1 : ( เอสเพรสโซ่ )\n+กาแฟสด100\n+ครีมข้น 40\n+นมคาร์ 40\n ราคา 35\n ** ถ้าปั่น +ครีมข้น เพิ่มเป็น 60\n ราคา 40 ** """,
    "A-2": """A-2 : ( คาปูชิโน่ )\n +กาแฟสด 100\n +ครีมข้น 40\n +นมคาร์ฯ 40\n+ราดฟองนม\n ราคา 40\n ** ถ้าปั่น +ครีมข้น เพิ่มเป็น 60\n ราคา 45 **""",
    "A-3": """A-3 : (ลาเต้)\n +น้ำกาแฟสด 90\n +ครีมข้น 40\n +นมเมจิ 100\m ราคา40 \n ** ถ้าปั่น +ครีมข้น เพิ่มเป็น 60\n ราคา 45 **""",
    "A-4": """A-4 : (มอคค่า)\n +กาแฟสด 100\n +โกโก้ 1 ช้อนชาพูน\n +ครีมข้น 40\n +นมคาร์ 40\n +ราดฟองนม\n ราคา40\n ** ถ้าปั่น +ครีมข้น เพิ่มเป็น 60\n ราคา 45 **""",
    "A-5": """A-5 : (อเมริกาโน่)\n +กาแฟสด 100\n +น้ำเปล่า 100\n +น้ำเชื่อม 20\n ราคา35""",
    "A-6": """A-6 : (อเมริกาโน่+น้ำผึ้ง)\n +กาแฟสด 100\n +น้ำเปล่า 100\n +น้ำเผึ้ง 30\n ราคา40""",
    "A-7": """A-7 : (อเมริกาโน่+น้ำผึ้ง+มะนาว)\n +กาแฟสด 100\n +น้ำเปล่า 100\n +น้ำผึ้ง 40\n +มะนาว 20\n ราคา45""",
    "A-8": """A-8 : (อเมริกาโน่+น้ำส้ม)\n +กาแฟสด 100\n +น้ำส้ม 150\n ราคา40""",
    "A-9": "A-9 (ยกเลิกเมนู)",
    "A-10": """A-10 : (เนสกาแฟ)\n +เนสกาแฟ 1 ช้อน\n +น้ำตาล 1 ช้อน\n +ครีมผง 1ช้อน\n +ครีมข้น 40\n +นมคาร์ 40\n ราคา 30\n **ถ้าปั่น +เนสกาแฟเป็น 2\n +น้ำตาลเป็น 2\n +ครีมข้นเป็น 60\n ราคา 35""",
    "A-11": """A-11 : (กาแฟโบราณ)\n +น้ำแช่กาแฟ100\n +น้ำตาล 1 ช้อน\n +ครีมผง 1ช้อน\n +ครีมข้น 40\n +นมคาร์ 40\n ราคา 30\n ถ้าปั่น +น้ำแช่กาแฟเป็น 150\n +น้ำตาลเป็น 2\n +ครีมข้นเป็น 60\n  ราคา 35""",
    "A-12": """A-12 : (โอเลี้ยง)\n +น้ำแช่กาแฟ 150\n +น้ำตาล 3ช้อน\n ราคา 30\n ถ้าปั่น +น้ำแช่กาแฟเป็น 200\n +น้ำตาลเป็น 8\n ราคา 35""",
    "A-13": """A-13 : (โอเลี้ยงยหล้อ)\n +น้ำแช่กาแฟ 150\n +น้ำตาล 3ช้อน\n +ราดนมคาร์ 40\nราคา 30\n ถ้าปั่น +น้ำแช่กาแฟเป็น 200\n +น้ำตาลเป็น 8\n ราคา 35""",
    "B-1": """B-1 : (น้ำบ๊วยเย็น)\n +เม็ดบ๊วย 3\n +น้ำบ๊วย 3ช้อน\n +น้ำตาล 3\n +น้ำร้อน 150\n *ถ้า บ๊วยโซดา +โซดาแทน น้ำร้อน 150\n +น้ำเชื่อมแทน น้ำตาล 45\n ราคา 30\n **ถ้าปั่น +บ๊วยเป็น 8\n +น้ำบ๊วยเป็น 6\n +น้ำร้อน 100\n ราคา 35""",
    "B-2": """B-2 : (น้ำบ๊วยโซดา+มะนาวเย็น)\n +เม็ดบ๊วย 3\n +น้ำบ๊วย 3ช้อน\n +น้ำเชื่อม 45\n +โซดา 150\n +มะนาว 20\n  ราคา 35\n *ถ้าปั่น +บ๊วยเป็น 8\n +น้ำบ๊วยเป็น 6\n ราคา 40""",
    "B-3": """B-3 : (แดง+โซดาเย็น)\n +น้ำแดง 60\n +โซดา 150\n ราคา 30\n """,
    "B-4": """B-4 : (แดง+โซดา+มะนาวเย็น)\n +น้ำแดง 60\n +โซดา 150\n +มะนาว 20 ราคา 30\n """,
    "B-5": """B-5 : (น้ำผึ้ง+โซดาเย็น)\n +น้ำผึ้ง 60\n +โซดา 150\n ราคา 40\n """,
    "B-6": """B-6 : (ยกเลิกแดง)\n""",
    "B-7": """B-7 : (ชาเขียว+แอปเปิ้ล+โซดาเย็น)\n +ชาเขียว 70\n +น้ำแอปเปิ้ล 60\n +โซดา 100\n ราคา 35\n """,
    "B-8": """B-8 : (สตรอเบอร์รี่+โซดาเย็น)\n +น้ำสตรอเบอร์รี่ 60\n +โซดา 150\n ราคา 30\n """,
    "B-9": """B-9 : (น้ำส้ม+โซดาเย็น)\n +น้ำส้ม 60\n +โซดา 150\n ราคา 30\n """,
    "B-10": """B-10 : (น้ำสัปปะรด+โซดาเย็น)\n +น้ำสัปปะรด 60\n +โซดา 150\n ราคา 30\n """,
    "B-11": """B-11 : (น้ำล่ิ้นจี่+โซดาเย็น)\n +น้ำลิ้นจี่ 60\n +โซดา 150\n ราคา 30\n """,
    "B-12": """B-12 : (น้ำบลูฮาวาย+โซดาเย็น)\n +น้ำบลูฮาวาย 60\n +โซดา 150\n ราคา 30\n """,
    "B-13": """B-13 : (น้ำกีวี่+โซดาเย็น)\n +น้ำกีวี่ 60\n +โซดา 150\n ราคา 30\n """,
    "B-14": """B-14 : (น้ำแอปเปิ้ลเขียว+โซดาเย็น)\n +น้ำแอปเปิ้ล 60\n +โซดา 150\n ราคา 30\n """,
    "B-15": """B-15 : (ยกเลิกแดง)\n""",
    "B-16": """B-16 : (ยกเลิกแดง)\n""",
}


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text.strip()

    if user_message in drink_recipes:
        reply_text = drink_recipes[user_message]
    else:
        reply_text = "ไม่มีในข้อมูล"

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)],
            )
        )


if __name__ == "__main__":
    app.run(port=5000)
