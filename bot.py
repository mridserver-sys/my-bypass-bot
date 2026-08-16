import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# BotFather থেকে পাওয়া আপনার টোকেনটি এখানে কোটেশনের ভেতর বসান
BOT_TOKEN = "8800197472:AAFtHyhNhVKuYR08pNG4wi1XGu2MMYDMc3I"

# কেউ বটের ভেতর /start দিলে এই মেসেজটি যাবে
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("স্বাগতম! যেকোনো অ্যাড-শর্টনার লিংক পাঠালে আমি আসল লিংক বের করে দেব।")

# লিংক রিসিভ ও বাইপাস করার লজিক
async def bypass_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    # ইনপুটটি কোনো ওয়েব লিংক কি না যাচাই করা
    if not (url.startswith("http://") or url.startswith("https://")):
        await update.message.reply_text("দয়া করে একটি সঠিক লিংক দিন (যেমন: https://...)।")
        return

    await update.message.reply_text("লিংক বাইপাস করা হচ্ছে, কিছুক্ষণ অপেক্ষা করুন...")

    try:
        # বাইপাস API-তে রিকোয়েস্ট পাঠানো
        api_url = f"https://api.bypass.vip/bypass?url={url}"
        response = requests.get(api_url, timeout=20)
        data = response.json()

        # সফল হলে আসল লিংক রিটার্ন করা
        if data.get("status") == "success" and data.get("destination"):
            destination = data.get("destination")
            await update.message.reply_text(f"✅ মূল ডাউনলোড লিংক:\n{destination}")
        else:
            await update.message.reply_text("❌ এই লিংকটি বাইপাস করা সম্ভব হয়নি বা সাইটটি সাপোর্টেড নয়।")
            
    except Exception:
        await update.message.reply_text("সার্ভারে সমস্যা হয়েছে। দয়া করে কিছুক্ষণ পর আবার চেষ্টা করুন।")

if __name__ == '__main__':
    # বট ইনিশিয়ালাইজ ও হ্যান্ডলার যুক্ত করা
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bypass_link))
    
    # বট চালু করা
    print("বট চালু হয়েছে...")
    app.run_polling()
  
