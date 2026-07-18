"""joke module — fetch random jokes from jokeapi"""
import json
import urllib.request
import urllib.parse
from pyrogram import Client

commands = ["joke", "jokes", "dadjoke"]


async def handle(app: Client, client: Client, message, args):
    category = "Any"
    if args:
        cat = args[0].lower()
        valid_cats = {"any", "programming", "misc", "dark", "pun", "spooky", "christmas"}
        if cat in valid_cats:
            category = cat.capitalize()

    try:
        url = f"https://v2.jokeapi.dev/joke/{category}?blacklistFlags=nsfw,religious,racist,sexist,explicit&type=single,twopart"
        req = urllib.request.urlopen(url, timeout=10)
        data = json.loads(req.read().decode())

        if data.get("error"):
            await app.send_message(message.chat.id, "📛 **Joke error:** couldn't fetch a joke right now")
            return

        if data["type"] == "single":
            text = data["joke"]
        else:
            text = f"**{data['setup']}**\n\n_{data['delivery']}_"

        category_emoji = {
            "Programming": "💻",
            "Misc": "🎭",
            "Dark": "🌑",
            "Pun": "😏",
            "Spooky": "👻",
            "Christmas": "🎄",
        }
        emoji = category_emoji.get(data.get("category", ""), "😂")
        await app.send_message(message.chat.id, f"{emoji} **{data.get('category', 'Joke')}**\n\n{text}")
    except Exception as e:
        await app.send_message(message.chat.id, f"📛 **Joke error:** `{e}`")
