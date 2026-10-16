# ใช้ Python เวอร์ชันทางการ
FROM python:3.14-slim

# กำหนดโฟลเดอร์ทำงานข้างใน Container
WORKDIR /app

# คัดลอกไฟล์ requirements หรือติดตั้งไลบรารีที่จำเป็น
RUN pip install --no-cache-dir flask line-bot-sdk gunicorn

# คัดลอกไฟล์โค้ดทั้งหมดเข้าไป
COPY . /app

# เปิดพอร์ต 5000
EXPOSE 5000

# คำสั่งสำหรับรันเซิร์ฟเวอร์ด้วย Gunicorn (เสถียรว่ารันผ่าน Flask ธรรมดา)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]