from pyrogram import Client
from utils import config

commands = ["settings", "config"]

async def handle(app: Client, client: Client, message, args):
    msg = "⚠  **Configuration**\n\n"
    p = config.read('prefix')
    config_list = [[key, value] for key, value in config.readAll().items()]

    for item in config_list:
        msg += f'❗ `{item[0]}` = "`{item[1]}`"\n'
    msg += f'\nℹ  To change or add new values, use `{p}setvalue (name) (value)`'
    await app.send_message(message.chat.id, msg)
