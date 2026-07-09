from pyrogram import Client
from utils import config

commands = ['notes']


def note_key(note_name):
    return f"note_{note_name}"

async def handle(app: Client, client: Client, message, args):
    command = args[0] if args else None

    if command == "save":
        if len(args) < 3:
            await app.send_message(message.chat.id, "📛 **Usage:** `notes save [name] [content]`")
            return
        note_name = args[1]
        note_content = " ".join(args[2:])
        config.add(note_key(note_name), note_content)
        await app.send_message(message.chat.id, f"✅ Note **{note_name}** saved successfully!")

    elif command == "get":
        if len(args) < 2:
            await app.send_message(message.chat.id, "📛 **Usage:** `notes get [name]`")
            return
        note_name = args[1]
        note_content = config.read(note_key(note_name))
        if note_content:
            await app.send_message(message.chat.id, f"💫 Note **{note_name}**:\n\n `{note_content}`")
        else:
            await app.send_message(message.chat.id, f"📛  Note **{note_name}** not found!")

    elif command == "delete":
        if len(args) < 2:
            await app.send_message(message.chat.id, "📛 **Usage:** `notes delete [name]`")
            return
        note_name = args[1]
        all_keys = config.readAll()
        if note_key(note_name) in all_keys:
            config.remove(note_key(note_name))
            await app.send_message(message.chat.id, f"✅ Note **{note_name}** deleted successfully!")
        else:
            await app.send_message(message.chat.id, f"📛 Note **{note_name}** not found!")

    elif command == "list":
        all_keys = config.readAll()
        note_keys = [key for key in all_keys if key.startswith("note_")]
        if note_keys:
            note_names = [key.replace("note_", "") for key in note_keys]
            note_list = "\n".join(f"📝 **{name}**" for name in note_names)
            await app.send_message(message.chat.id, f"📒 **Saved notes:**\n{note_list}")
        else:
            await app.send_message(message.chat.id, "💢 You have no saved notes.")

    else:
        await app.send_message(message.chat.id, "💫 **Usage:**\n\n🔰 `notes save [note_name] [note_content]`  -  **new note**\n🔰 `notes get [note_name]`  -  **read note**\n🔰 `notes delete [note_name]`  -  **delete note**\n🔰 `notes list`  -  **get list of your notes**")
