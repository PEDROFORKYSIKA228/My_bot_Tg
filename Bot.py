from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes,CallbackQueryHandler
import asyncio
import aiohttp

API = "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"
TOKEN = "8429288786:AAGPz4aymZMkRhDV4R-TwtqVBLWvNLTP6Ec"
Chat_his = {}

async def ask_ai(session, messages):
    async with session.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/devstral-2512:free",
            "messages": messages
        }
    ) as resp:
        result = await resp.json()
        if "choices" not in result or len(result["choices"]) == 0:
            print("Етить колотить! Проблема!:", result)
            return "Возникла ошибка при обращении к ИИ😢."
        return result["choices"][0]["message"]["content"].strip()
  
async def send_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    Chat_his.setdefault(chat_id, [])
    Chat_his[chat_id].append({"role": "user", "content": update.message.text})
    
    async with aiohttp.ClientSession() as session:
        ai_answ = await ask_ai(session, Chat_his[chat_id])
        Chat_his[chat_id].append({"role": "assistant", "content": ai_answ})
        await update.message.reply_text(ai_answ)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Это бот с ИИ(Искуственным интелектом🤖). ❓Он может ответить на ваши вопросы, и если вы хотите, чтобы бот говорил с вами на другом языке, то просто напишите ему!😁 Для ознакомления с остальными функциями, используйте команду /help❗")

async def help_com(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅Команды: /help /int_menu. Связаться с владельцем можно через команду /int_menu👽 ")

async def inl_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🤟 Лайк", callback_data="like"), InlineKeyboardButton("👊 Дизлайк", callback_data="dislike")],
        [InlineKeyboardButton("👽 Связь с владельцем:", url="https://t.me/racoon_13752")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Оцените бота:", reply_markup=reply_markup)

async def click_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "like":
        await query.edit_message_text("Питер вас уважает😎")
    elif query.data == "dislike":
        await query.edit_message_text("Не ну питер это не одобряет")

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_com))
    app.add_handler(CommandHandler("int_menu", inl_menu))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), send_request))
    app.add_handler(CallbackQueryHandler(click_button))


    app.run_polling()

if __name__ == "__main__":
    main()

