import asyncio
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from aiohttp import web

TOKEN = "8370672715:AAHMhxeaJhH-uDdHKSyRPYoqAKnlk0tVX6k"
ADMIN_ID = 1396547701  # свой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# -----------------------------
# WEB СЕРВЕР ДЛЯ RENDER (PORT FIX)
# -----------------------------
async def handle(request):
    return web.Response(text="Bot is running")

def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    web.run_app(app, port=10000)

threading.Thread(target=run_web, daemon=True).start()

# -----------------------------
# /start
# -----------------------------
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот работает 👍")

    if message.from_user.id != ADMIN_ID:
        await bot.send_message(
            ADMIN_ID,
            f"🆕 Новый пользователь:\nID: {message.from_user.id}\nИмя: {message.from_user.full_name}"
        )

# -----------------------------
# сообщения пользователей → админу
# -----------------------------
@dp.message()
async def handle_messages(message: types.Message):

    if message.from_user.id == ADMIN_ID:
        return

    text = message.text or "[не текст]"

    await bot.send_message(
        ADMIN_ID,
        f"📩 {message.from_user.id}:\n{text}"
    )

    # -----------------------------
    # админ отправляет: ID текст
    # -----------------------------
    if message.from_user.id == ADMIN_ID:

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

# -----------------------------
# запуск бота
# -----------------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
