# ░█░█░█░█░█▀█░█▄█░█▀█░█▀▄░▀█▀
# ░█▀█░█▀▄░█▀█░█░█░█░█░█▀▄░░█░
# ░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀             
# Name: modules/help.py
# Description: Help module
# Author: hkamori | 0xhkamori.github.io
# ----------------------------------------------
# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ------------------------------------------------

import importlib
from pathlib import Path
from pyrogram import Client
from utils import config

commands = ["help", "commands"]

async def handle(app: Client, client: Client, message, args):
    e = config.read('help_emoji')
    me = config.read('mainemoji')
    
    # build command list lazily
    modules_dir = Path("modules")
    commands_dict = {}
    for f in modules_dir.glob("*.py"):
        if f.stem == "__init__":
            continue
        module = importlib.import_module(f"modules.{f.stem}")
        if hasattr(module, 'commands'):
            commands_dict[f.stem] = module.commands

    commands_count = sum(len(cmds) for cmds in commands_dict.values())
    modules_count = len(commands_dict)
    msgtosend = f"{me} **{commands_count}** Commands available. **{modules_count}** modules.\n\n"

    for module_name, module_commands in commands_dict.items():
            commands_str = " | ".join(module_commands)
            msgtosend += f"{e} **{module_name.capitalize()}**:  ({commands_str})\n"
    await app.send_message(message.chat.id, msgtosend)
