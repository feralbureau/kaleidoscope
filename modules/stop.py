"""stop module — gracefully stop the userbot"""
from pyrogram import Client
from utils import config

commands = ["stop", "exit"]

async def handle(app: Client, client: Client, message, args):
    me = config.read('mainemoji')
    await app.send_message(message.chat.id, f"{me} `kaleidoscope` is now closed.")
    await app.stop()
