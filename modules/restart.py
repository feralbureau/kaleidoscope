import os
import sys
from pyrogram import Client
from utils import config

commands = ["restart", "reboot"]

async def handle(app: Client, client: Client, message, args):
    me = config.read('mainemoji')
    await app.send_message(message.chat.id, f"{me} `Kaleidoscope` **is restarting...**")
    os.execv(sys.executable, ['python'] + sys.argv)
