import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# Replace with your bot token
BOT_TOKEN = "7923532245:AAEU6PMcm_ImVuELVoWV4H5iA2Qn0Fxxtyg"
API_URL = "https://nametoapk.ytansh038.workers.dev/?name="  # Your API URL
START_IMAGE = "https://envs.sh/Q0_.jpg"  # Replace with your image URL

async def start(update: Update, context: CallbackContext) -> None:
    caption = (
        "🔍 Welcome to APK Finder Bot!\n\n"
        "Use this bot to find APK files for your favorite apps.\n\n"
        "📌 *How to use?*\n"
        "1️⃣ Type `/apk <app_name>` to search for an app.\n"
        "2️⃣ Get the download link and image instantly.\n\n"
        "🔽 Try searching for an app now!"
    )

    buttons = [
        [
            InlineKeyboardButton("💬 Support", url="https://t.me/+7AUuVrP8F69kYWY1"),
            InlineKeyboardButton("📢 Channel", url="https://t.me/+7AUuVrP8F69kYWY1"),
        ],
        [InlineKeyboardButton("🔗 Website", url="anshapiweb.vercel.app")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.reply_photo(photo=START_IMAGE, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")

async def fetch_apk(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /apk <app_name>")
        return

    app_name = " ".join(context.args)
    response = requests.get(API_URL + app_name)

    if response.status_code != 200:
        await update.message.reply_text("⚠️ Error fetching data from API.")
        return

    data = response.json()

    if not data:
        await update.message.reply_text("❌ No apps found.")
        return

    for app in data:
        name = app.get("name", "Unknown App")
        package = app.get("package", "Unknown Package")
        apk_url = app.get("path", "No APK Found")
        image_url = app.get("image", "")

        message = f"📱 *{name}*\n📦 Package: `{package}`\n🔗 [Download APK]({apk_url})"
        keyboard = [[InlineKeyboardButton("⬇️ Download APK", url=apk_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_photo(photo=image_url, caption=message, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("apk", fetch_apk))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
