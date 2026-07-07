from pyrogram import Client
from utils import config
from modules import ping as ping_module

commands = ["stop", "exit"]

async def handle(app: Client, client: Client, message, args):
    me = config.read('mainemoji')
    ping_module.stop_toggle = True
    await app.send_message(message.chat.id, f"{me} `kaleidoscope` is now closed.")
    exit()
