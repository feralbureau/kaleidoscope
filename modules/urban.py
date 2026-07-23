"""urban module — look up slang definitions from Urban Dictionary"""

import json
import urllib.error
import urllib.parse
import urllib.request
from pyrogram import Client

commands = ["urban", "ud", "slang"]

API_URL = "https://api.urbandictionary.com/v0/define?term={}"


async def handle(app: Client, client: Client, message, args):
    if not args:
        await app.send_message(
            message.chat.id,
            "📖 **urban** — look up slang definitions\n"
            "Usage: `.urban word`\n"
            "Example: `.urban yeet`",
        )
        return

    word = " ".join(args).strip()
    url = API_URL.format(urllib.parse.quote(word))

    try:
        req = urllib.request.urlopen(url, timeout=10)
        data = json.loads(req.read().decode())

        if not data.get("list"):
            await app.send_message(
                message.chat.id,
                f"📛 **Not found:** no urban definition for `{word}`",
            )
            return

        entry = data["list"][0]
        definition = entry.get("definition", "")
        example = entry.get("example", "")
        author = entry.get("author", "unknown")
        thumbs_up = entry.get("thumbs_up", 0)
        thumbs_down = entry.get("thumbs_down", 0)

        # truncate long defs to stay under telegram's 4096 limit
        msg = f"📖 **{entry.get('word', word)}**\n\n"
        msg += definition[:1500]
        if example:
            msg += f"\n\n💬 **Example:**\n_{example[:500]}_"
        msg += f"\n\n👍 {thumbs_up}  👎 {thumbs_down}  ✍️ {author}"

        await app.send_message(message.chat.id, msg)

    except urllib.error.HTTPError as e:
        await app.send_message(
            message.chat.id,
            f"📛 **Error:** API returned {e.code}",
        )
    except (urllib.error.URLError, json.JSONDecodeError):
        await app.send_message(
            message.chat.id,
            "📛 **Error:** could not reach Urban Dictionary",
        )
    except Exception as e:
        await app.send_message(
            message.chat.id,
            f"📛 **Error:** `{e}`",
        )
