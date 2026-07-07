"""echo module — repeat text back in chat"""
from pyrogram import Client

commands = ["echo", "say"]

async def handle(app: Client, client: Client, message, args):
    if not args:
        await app.send_message(
            message.chat.id,
            "🗣 **echo** — repeat text back\n"
            "Usage: `.echo Hello world`\n"
            "Example: `.echo I am a bot`",
        )
        return
    text = " ".join(args)
    await app.send_message(message.chat.id, text)
