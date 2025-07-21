
# === Binance Price Alert Telegram Bot ===
# Tác giả: ChatGPT - Hướng dẫn cho người mới

import requests
import time
from telegram import Bot

# === Cấu hình ===
TOKEN = '8069404664:AAEeX3JwNyvxKsrXIQQWIG0s6SFLR2NlIrs'
CHAT_ID = '270326108'
COINS = ['BTCUSDT', 'ETHUSDT', 'TRBUSDT', 'ENAUSDT', 'ETHFIUSDT', 'PEPEUSDT', 'WIFUSDT', 'BOMEUSDT', 'LDOUSDT', 'ADAUSDT', 'XRPUSDT']  # Danh sách coin theo dõi
THRESHOLD_PERCENT = 1  # % thay đổi để cảnh báo
INTERVAL = 60  # Thời gian kiểm tra (giây)

bot = Bot(token=TOKEN)
last_prices = {}

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url).json()
    return float(response['price'])

def check_price():
    for coin in COINS:
        try:
            current_price = get_price(coin)
            last_price = last_prices.get(coin)
            if last_price:
                percent_change = ((current_price - last_price) / last_price) * 100
                if abs(percent_change) >= THRESHOLD_PERCENT:
                    direction = "🔺 Tăng" if percent_change > 0 else "🔻 Giảm"
                    message = f"{direction} {coin}: {percent_change:.2f}%\nGiá hiện tại: {current_price:.2f} USDT"
                    bot.send_message(chat_id=CHAT_ID, text=message)
            last_prices[coin] = current_price
        except Exception as e:
            print(f"Lỗi khi kiểm tra giá {coin}: {e}")

# === Vòng lặp chính ===
print("Bot bắt đầu chạy...")
while True:
    check_price()
    time.sleep(INTERVAL)
