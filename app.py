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

# นำ Channel Access Token และ Channel Secret ของคุณมาใส่ตรงนี้
configuration = Configuration(
    access_token="vnsBJP9AvLUXsfOPoHS/mPjbHiwgk3IgzGGH/fWJik4e+L7ACs7Jq14UK7f+tFV1BaIaVpNbaarZdywmEtM6XhlIDFvDfMXkK5FDPT9SaHQTIefA+wcgAAWrTldI0TzX2BaDyN8xQDHpS0W3Ma46yQdB04t89/1O/w1cDnyilFU="
)
handler = WebhookHandler("b97673e4e7f87358de56cca3099995d6")

# ฐานข้อมูลสูตรเครื่องดื่ม
drink_recipes = {
    "A-1": (
        "A-1 : ( เอสเพรสโซ่ )\n- กาแฟสด100 \n-ครีมข้น 40 \n-นมคาร์ 40 ราคา 35 \n ** ถ้าปั่น ครีมข้น เพิ่มเป็น 60 ราคา 40 ** "
    ),
    "เอสเปรสโซ่": ("สูตรเอสเปรสโซ่:\n- ผงกาแฟ 18 กรัม\n- น้ำร้อน 30 ml"),
    "นมชมพู": (
        "สูตรนมชมพู:\n- น้ำแดงเฮบลูบอยด์ 30 ml\n- นมข้นหวาน 30 ml\n- นมสด 90"
        " ml\n- น้ำร้อน 60 ml"
    ),
    "ชาไทย": (
        "สูตรชาไทย:\n- ผงชาไทย 15 กรัม\n- น้ำร้อน 120 ml\n- นมข้นหวาน 30 ml\n- นมข้นจืด"
        " 20 ml"
    ),
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

    # เช็กเมนูน้ำในฐานข้อมูล
    if user_message in drink_recipes:
        reply_text = drink_recipes[user_message]
    else:
        reply_text = "ไม่มีในข้อมูล"

    # ส่งข้อความกลับหาผู้ใช้
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
