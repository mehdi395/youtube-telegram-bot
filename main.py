# main.py

import os
import yt_dlp
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# تابع دانلود ویدیو
def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best[filesize<50M]/best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not ("youtube.com" in url or "youtu.be" in url):
        await update.message.reply_text("لطفاً لینک معتبر یوتیوب ارسال کنید.")
        return
    
    await update.message.reply_text("در حال دانلود... لطفاً کمی صبر کنید")
    try:
        file_path = download_video(url)
        await update.message.reply_video(video=open(file_path, 'rb'))
        os.remove(file_path)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("خطا در دانلود و ارسال ویدیو")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک ویدیوی یوتیوب را ارسال کنید.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    logger.info("Bot started...")
    app.run_polling()
