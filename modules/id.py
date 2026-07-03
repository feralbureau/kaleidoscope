from pyrogram import Client
from utils import config

commands = ["id"]

async def handle(app: Client, client: Client, message, args):
    me = config.read('mainemoji')
    chat = message.chat
    reply = message.reply_to_message

    if reply and reply.from_user:
        user = reply.from_user
        text = f"{me} **User Info**\n👤 Name: **{user.first_name}**\n🆔 ID: `{user.id}`\n💬 Chat ID: `{chat.id}`"
        if user.username:
            text += f"\n🔗 @{user.username}"
    else:
        text = f"{me} **Chat Info**\n💬 Title: **{chat.title or 'Private Chat'}**\n🆔 Chat ID: `{chat.id}`"
        if chat.type == "private" and hasattr(chat, 'first_name'):
            text += f"\n👤 User: **{chat.first_name}**"

    if args:
        try:
            users = await client.get_users(args[0])
            if hasattr(users, '__iter__'):
                user = users[0]
            else:
                user = users
            text += f"\n\n🔍 **Lookup:** {user.first_name} → `{user.id}`"
        except Exception:
            pass

    await app.send_message(chat.id, text)
