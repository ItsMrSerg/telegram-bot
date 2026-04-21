import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from flask import Flask
import threading

TOKEN = "ВСТАВЬ_ТОКЕН"
ADMIN_ID = 123456789

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ----------------- FLASK SERVER (Render PORT FIX) -----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask, daemon=True).start()

# ----------------- BOT LOGIC -----------------

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот работает 👍")

@dp.message()
async def handler(message: types.Message):

    text = message.text or ""

    # пользователь → админу
    if message.from_user.id != ADMIN_ID:
        await bot.send_message(
            ADMIN_ID,
            f"📩 {message.from_user.id}:\n{text}"
        )
        return

    # админ отправляет: ID текст
    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer("Формат: ID текст")
        return

    try:
        user_id = int(parts[0])
        msg = parts[1]

        await bot.send_message(user_id, msg)
        await message.answer("Отправлено ✔")

    except Exception as e:
        await message.answer(f"Ошибка:\n{e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
