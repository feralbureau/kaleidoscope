from pyrogram import Client
from utils import config

commands = ["setprefix"]

async def handle(app: Client, client: Client, message, args):
    if not args:
        p = config.read('prefix')
        await app.send_message(
            message.chat.id,
            f"🔤 **setprefix** — change command prefix\n"
            f"Current prefix: `{p}`\n"
            f"Usage: `.setprefix !`\n"
            f"Example: `.setprefix /` — now commands are `/ping`",
        )
        return
    me = config.read('mainemoji')
    new_prefix = " ".join(args)
    config.add('prefix', new_prefix)
    await app.send_message(message.chat.id, f"{me} **Prefix changed.** \n💫 New prefix: `({new_prefix})`")
