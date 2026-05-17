import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from groq import Groq

# Kalitlar (Ular joyida, teginmang)
BOT_TOKEN = "8837303824:AAE9hHUnZWcsO7ihCGRQ3stp9TIJzJn5N4Y"
GROQ_API_KEY = "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"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
import httpx
proxy_client = httpx.Client(proxies={})
ai_client = Groq(api_key=GROQ_API_KEY, http_client=proxy_client)


# Menyuni yaratish
def get_menu():
    buttons = [
        [KeyboardButton(text="💪 Shaxsiy trenirovka rejasi")],
        [KeyboardButton(text="🍏 Sog'lom ovqatlanish menyusi")],
        [KeyboardButton(text="❓ Sport bo'yicha savol berish")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        f"Salom, {message.from_user.first_name}! 👋\n"
        "Men sizning shaxsiy AI Sport va Parhez murabbiymandirman. 🏋️‍♂️🍏\n\n"
        "Xohlagan tilingizda (O'zbekcha, Ruscha, Inglizcha) savol bering yoki tugmalardan birini tanlang:",
        reply_markup=get_menu()
    )

@dp.message(F.text == "💪 Shaxsiy trenirovka rejasi")
async def training_plan(message: Message):
    await message.answer(
        "Sizga mos reja tuzishim uchun yoshingiz, bo'yingiz, vazningiz, "
        "maqsadingiz va qayerda shug'ullanishizni (uyda/zalda) yozib yuboring.\n"
        "*(Xohlagan tilingizda yozishingiz mumkin)*"
    )

@dp.message(F.text == "🍏 Sog'lom ovqatlanish menyusi")
async def diet_plan(message: Message):
    await message.answer(
        "Sizga parhez menyusi tuzishim uchun vazningiz, bo'yingiz, "
        "kuniga necha marta ovqatlanishingiz va allergiyangiz bormi — yozing.\n"
        "*(Xohlagan tilingizda yozishingiz mumkin)*"
    )

@dp.message(F.text == "❓ Sport bo'yicha savol berish")
async def ask_question(message: Message):
    await message.answer("Sport yoki to'g'ri ovqatlanish bo'yicha xohlagan savolingizni xohlagan tilingizda yozib yuboring. 🧠")

@dp.message()
async def handle_ai_request(message: Message):
    status_msg = await message.answer("AI o'ylamoqda... 🤖⏳")
    
    try:
        # Eng oxirgi va 100% ishlayotgan ko'p tilli model: llama-3.3-70b-versatile
        chat_completion = ai_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional sports coach and experienced nutritionist. "
                        "CRITICAL RULE: Detect the language used by the user (Uzbek, Russian, or English) "
                        "and reply ONLY in that exact language. Your grammar must be absolutely flawless, "
                        "natural, and professional. Do not use direct robotic translations. "
                        "Use clear bullet points and emojis to structure your response beautifully."
                    )
                },
                {"role": "user", "content": message.text}
            ],
            model="llama-3.3-70b-versatile", # AKTUAL VA ISHLAYDIGAN MODEL
        )
        
        ai_response = chat_completion.choices[0].message.content
        await status_msg.edit_text(ai_response)
            
    except Exception as e:
        print(f"DIQQAT XATOLIK: {e}")
        await status_msg.edit_text(f"Xatolik yuz berdi: {str(e)[:100]}")

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())


   


