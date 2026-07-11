"""afk module — set away-from-keyboard auto-reply

When afk is set, the bot auto-replies to direct messages
and @mentions with the afk reason.
"""
from pyrogram import Client
from utils import config

commands = ["afk"]
_me_cache = None


async def _get_me(client: Client):
    """Cached get_me — avoids repeated API calls."""
    global _me_cache
    if _me_cache is None:
        _me_cache = await client.get_me()
    return _me_cache


async def handle(app: Client, client: Client, message, args):
    """Set or disable afk mode."""
    if args and args[0].lower() in ("off", "stop", "back", "disable"):
        config.add("afk_enabled", False)
        config.remove("afk_reason")
        me = config.read("mainemoji")
        await app.send_message(
            message.chat.id, f"{me} **AFK disabled.** Welcome back!"
        )
        return

    reason = " ".join(args) if args else "No reason given"
    config.add("afk_enabled", True)
    config.add("afk_reason", reason)
    me = config.read("mainemoji")
    await app.send_message(
        message.chat.id,
        f"{me} **AFK enabled.**\n📝 Reason: `{reason}`",
    )


async def on_all_messages(app: Client, client: Client, message):
    """Respond to messages when afk is set, and auto-disable on user activity."""
    if not config.read("afk_enabled"):
        return

    if not message.from_user:
        return

    me = await _get_me(client)

    # User's own non-command messages disable afk
    if message.from_user.id == me.id:
        if (
            message.text
            and not message.text.startswith(config.read("prefix"))
        ):
            config.add("afk_enabled", False)
            config.remove("afk_reason")
            await app.send_message(
                message.chat.id,
                "👋 **AFK disabled.** Welcome back!",
            )
        return

    # Other people's messages — reply with afk notice
    reason = config.read("afk_reason") or "No reason given"

    if message.chat.type == "private":
        await message.reply(
            f"🤖 **I'm currently AFK.**\n📝 {reason}"
        )
    elif (
        message.text
        and me.username
        and f"@{me.username}" in message.text
    ):
        await message.reply(
            f"🤖 **@{me.username}** is currently AFK.\n📝 {reason}"
        )
