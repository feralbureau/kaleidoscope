from pyrogram import Client
from utils import config

commands = ["setvalue"]

async def handle(app: Client, client: Client, message, args):
    if len(args) < 2:
        await app.send_message(
            message.chat.id,
            "⚙️ **setvalue** — set config values\n"
            "Usage: `.setvalue key value`\n"
            "Examples:\n"
            "`.setvalue prefix !` — change prefix\n"
            "`.setvalue trlang ru` — set translate target language",
        )
        return
    try:
        key = args[0]
        value = args[1]
        config.add(key, value)
        await app.send_message(message.chat.id, "✅  **Value set successfully**")
    except:
        await app.send_message(message.chat.id, "📛  **Error setting value**")
