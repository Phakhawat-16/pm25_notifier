import requests
import time
import schedule

api_key = 'f364b635c8871d7401c24280a77afebe'
telegram_bot_token = '7864405183:AAGWYDDbU3E6wjCn7a3_joj4MDdIJXppfGo'
chat_id = '-1002417767289'
lat = 13.7563
lon = 100.5018

def send_pm25_alert():
    print("🔍 กำลังดึงข้อมูล PM 2.5 ...")
    
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    print(f"🌐 สถานะ API: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"📊 ข้อมูลที่ได้รับ: {data}")
        
        pm25 = data['list'][0]['components']['pm2_5']
        print(f'🌫 PM 2.5 ตอนนี้: {pm25} µg/m³')

        if pm25 > 100:
            advice = "อากาศเป็นอันตรายมาก! ควรอยู่ในอาคารและปิดหน้าต่าง"
        elif pm25 > 50:
            advice = "คุณภาพอากาศไม่ดี ควรใส่หน้ากากเมื่อออกข้างนอก"
        else:
            advice = "อากาศดี สามารถออกข้างนอกได้ตามปกติ"

        message = f"🌫 **แจ้งเตือนค่าฝุ่น PM 2.5** 🌫\n\nค่าฝุ่น PM 2.5 ตอนนี้: {pm25} µg/m³\n\nคำแนะนำ: {advice}"
        
        print("✉️ กำลังส่งข้อความไปยัง Telegram ...")
        telegram_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
        params = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        telegram_response = requests.get(telegram_url, params=params)
        print(f"📩 สถานะ Telegram: {telegram_response.status_code}")
        
        if telegram_response.status_code == 200:
            print("✅ ส่งข้อความแจ้งเตือนเรียบร้อยแล้ว!")
        else:
            print(f"❌ เกิดข้อผิดพลาดในการส่งข้อความ: {telegram_response.text}")
    else:
        print(f"⚠️ ไม่สามารถเชื่อมต่อกับ API ได้: {response.status_code}, ข้อความ: {response.text}")

# ทดสอบเรียกใช้ฟังก์ชันโดยตรง
send_pm25_alert()

# ตั้งเวลาให้ฟังก์ชันทำงานทุก 10 นาที
schedule.every(1).minutes.do(send_pm25_alert)

while True:
    print("⌛ รอ schedule ทำงาน...")
    schedule.run_pending()
    time.sleep(60)

