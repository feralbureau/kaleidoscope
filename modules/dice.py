"""dice module — roll dice and flip coins"""
import random
from pyrogram import Client

commands = ["dice", "coin", "flip"]

async def handle(app: Client, client: Client, message, args):
    if not args:
        # default: roll a 6-sided die
        result = random.randint(1, 6)
        await app.send_message(message.chat.id, f"🎲 **{result}** (d6)")
        return

    sub = args[0].lower()

    if sub in ("coin", "flip"):
        result = random.choice(["Heads", "Tails"])
        await app.send_message(message.chat.id, f"🪙 **{result}**")
        return

    try:
        sides = int(sub)
    except ValueError:
        await app.send_message(
            message.chat.id,
            "🎲 **dice** — roll dice and flip coins\n"
            "Usage:\n"
            "`.dice` — roll a 6-sided die\n"
            "`.dice 20` — roll a 20-sided die\n"
            "`.dice coin` — flip a coin",
        )
        return

    if sides < 2:
        await app.send_message(message.chat.id, "📛 **Error:** dice must have at least 2 sides")
        return

    result = random.randint(1, sides)
    await app.send_message(message.chat.id, f"🎲 **{result}** (d{sides})")
