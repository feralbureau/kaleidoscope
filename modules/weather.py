from pyrogram import Client
import python_weather, asyncio, os

commands = ["weather"]

async def handle(app: Client, client: Client, message, args):
    async with python_weather.Client(unit=python_weather.METRIC) as wclient:
        weather = await wclient.get(" ".join(args))
        city = " ".join(args)
        await app.send_message(message.chat.id, f"🔅 Weather in:  `{city.capitalize()}, {weather.country}` 📍\n🔱 **Kind:  **`{weather.kind}`\n🌡️ **Temperature: ** `{weather.temperature} °C`\n💨 **Feels like:  ** `{weather.feels_like} °C`")
