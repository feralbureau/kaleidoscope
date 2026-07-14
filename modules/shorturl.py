"""shorturl module — shorten long urls"""
import urllib.request
import urllib.parse
from pyrogram import Client

commands = ["shorten", "shorturl", "tiny"]

ISGD_API = "https://is.gd/create.php"

async def handle(app: Client, client: Client, message, args):
    if not args:
        await app.send_message(
            message.chat.id,
            "🔗 **shorturl** — shorten a url\n"
            "Usage: `.shorten https://example.com/very/long/url`\n"
            "Example: `.shorten https://github.com/feralbureau/kaleidoscope`",
        )
        return

    long_url = args[0]
    params = urllib.parse.urlencode({"format": "simple", "url": long_url})
    url = f"{ISGD_API}?{params}"

    try:
        req = urllib.request.urlopen(url, timeout=10)
        short = req.read().decode().strip()
        await app.send_message(
            message.chat.id,
            f"🔗 **Short URL**\n"
            f"Original: `{long_url}`\n"
            f"Short: `{short}`",
        )
    except Exception as e:
        await app.send_message(
            message.chat.id,
            f"📛 **Shorten error:** `{e}`\n"
            f"Make sure the url is valid and publicly accessible.",
        )
