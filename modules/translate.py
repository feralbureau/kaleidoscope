from googletrans import Translator
from pyrogram import Client
from utils import config

commands = ["tr"]
translator = Translator()

async def handle(app: Client, client: Client, message, args):
    if not args:
        trlang = config.read('trlang')
        await app.send_message(
            message.chat.id,
            f"🌐 **tr** — translate text\n"
            f"Target language: `{trlang}`\n"
            f"Usage: `.tr text`\n"
            f"Example: `.tr Hello world`\n"
            f"Change target: `.setvalue trlang ru`",
        )
        return

    phrase = " ".join(args)
    try:
        translation = translator.translate(phrase, dest=config.read('trlang'))
        await app.send_message(message.chat.id,
                                f"🧾 **Translated:** `{translation.text} ({translation.dest})`")
    except Exception:
        await app.send_message(message.chat.id, f"📛  **Error.** Try changing your destination language: `.setvalue trlang (language code. example: en)`")
