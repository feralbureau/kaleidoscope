"""qrcode module — generate qr codes from text"""
import urllib.request
import urllib.parse
from io import BytesIO
from pyrogram import Client
from pyrogram.types import InputMediaPhoto

commands = ["qrcode", "qr"]

QR_API = "https://api.qrserver.com/v1/create-qr-code/"

async def handle(app: Client, client: Client, message, args):
    if not args:
        await app.send_message(
            message.chat.id,
            "📱 **qrcode** — generate a qr code\n"
            "Usage: `.qrcode text here`\n"
            "Example: `.qrcode Hello World`",
        )
        return

    data = " ".join(args)
    params = urllib.parse.urlencode({"size": "400x400", "data": data})
    url = f"{QR_API}?{params}"

    try:
        req = urllib.request.urlopen(url, timeout=10)
        img_bytes = BytesIO(req.read())
        img_bytes.name = "qrcode.png"
        await app.send_photo(
            message.chat.id,
            img_bytes,
            caption=f"📱 **QR Code** for: `{data[:50]}{'…' if len(data) > 50 else ''}`",
        )
    except Exception as e:
        await app.send_message(
            message.chat.id,
            f"📛 **QR error:** `{e}`",
        )
