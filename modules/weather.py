import json, urllib.request, urllib.parse
from pyrogram import Client

commands = ["weather", "wttr"]

async def handle(app: Client, client: Client, message, args):
    if not args:
        await app.send_message(
            message.chat.id,
            "🌤 **weather** — check current weather\n"
            "Usage: `.weather city name`\n"
            "Example: `.weather Warsaw`",
        )
        return

    city = " ".join(args)
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
        req = urllib.request.urlopen(url, timeout=10)
        data = json.loads(req.read().decode())
        cc = data["current_condition"][0]
        desc = cc["weatherDesc"][0]["value"]
        temp = cc["temp_C"]
        feels = cc["FeelsLikeC"]
        wind = cc["windspeedKmph"]
        humidity = cc["humidity"]
        area = data["nearest_area"][0]
        cityname = area["areaName"][0]["value"]
        country = area["country"][0]["value"]

        await app.send_message(
            message.chat.id,
            f"🔅 **{cityname}, {country}**\n"
            f"🌡️ **{temp}°C** (feels like {feels}°C)\n"
            f"☁️ {desc}\n"
            f"💨 Wind: {wind} km/h | 💧 Humidity: {humidity}%",
        )
    except Exception as e:
        await app.send_message(
            message.chat.id,
            f"📛 **Weather error:** city not found\n"
            f"Try: `.weather Warsaw`",
        )
