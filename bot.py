from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from PIL import Image
import io

BOT_TOKEN = '7609953248:AAFbKD9vX7islPDwapF0qorkhWd-fqaJY-0'

# Load logos once at startup
logo_kiri = Image.open("logo_kiri.png").convert("RGBA")
logo_kanan = Image.open("logo_kanan.png").convert("RGBA")

def paste_logo(base_img, logo_img, position, margin_x=0, margin_y=-5, scale=0.25):
    logo_width = int(base_img.width * scale)
    logo_height = int(logo_img.height * (logo_width / logo_img.width))
    logo = logo_img.resize((logo_width, logo_height), Image.LANCZOS)

    if position == "top_left":
        pos = (margin_x, margin_y)
    elif position == "top_right":
        pos = (base_img.width - logo.width - margin_x, margin_y)
    else:
        pos = (0, 0)

    base_img.paste(logo, pos, logo)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await update.message.photo[-1].get_file()
    photo_bytes = await photo.download_as_bytearray()

    image = Image.open(io.BytesIO(photo_bytes)).convert("RGBA")

    paste_logo(image, logo_kiri, "top_left", margin_x=0, margin_y=-5, scale=0.25)
    paste_logo(image, logo_kanan, "top_right", margin_x=0, margin_y=-5, scale=0.25)

    # Convert to RGB and save as high quality JPEG
    rgb_image = image.convert("RGB")
    output = io.BytesIO()
    output.name = "hasil_logo.jpg"
    rgb_image.save(output, format='JPEG', quality=100)
    output.seek(0)

    await update.message.reply_document(document=output, caption="KIRIMLAH KEGRUP (Kualitas Tinggi)")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == '__main__':
    print("Bot berjalan...")
    app.run_polling()
