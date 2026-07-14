# ░█░█░█░█░█▀█░█▄█░█▀█░█▀▄░▀█▀
# ░█▀█░█▀▄░█▀█░█░█░█░█░█▀▄░░█░
# ░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀             
# Name: modules/ily.py
# Description: ILY module
# Author: hkamori | 0xhkamori.github.io
# ----------------------------------------------
# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ------------------------------------------------

import asyncio
import json
import urllib.request
from pyrogram import Client

commands = ["ily"]

ILY_DATA_URL = (
    "https://gist.githubusercontent.com/hikariatama"
    "/89d0246c72e5882e12af43be63f5bca5/raw"
    "/08a5df7255d5e925ab2ede1efc892d9dc93af8e1/ily_classic.json"
)

async def fetch_hearts_animation():
    def _fetch():
        req = urllib.request.urlopen(ILY_DATA_URL, timeout=10)
        return json.loads(req.read().decode())
    return await asyncio.get_event_loop().run_in_executor(None, _fetch)

async def handle(app: Client, client: Client, message, args):
    hearts_animation = await fetch_hearts_animation()
    msg = await app.send_message(message.chat.id, '❤')
    await asyncio.sleep(0.5)
    for frame in hearts_animation:
        await app.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=frame)
        await asyncio.sleep(0.5)
