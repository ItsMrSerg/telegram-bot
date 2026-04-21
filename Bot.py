import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8370672715:AAHMhxeaJhH-uDdHKSyRPYoqAKnlk0tVX6k"
ADMIN_ID = 1396547701

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот работает 👍")

# ВСЕ сообщения
@dp.message()
async def handler(message: types.Message):

    text = message.text or ""

    # 1. ЕСЛИ ЭТО АДМИН → команда отправки
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

        return

    # 2. ЕСЛИ ЭТО ПОЛЬЗОВАТЕЛЬ → пересылка админу
    await bot.send_message(
        ADMIN_ID,
        f"📩 {message.from_user.id}:\n{text}"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())