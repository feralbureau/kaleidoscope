"""define module — look up word definitions from Free Dictionary API"""

import json
import urllib.error
import urllib.parse
import urllib.request
from pyrogram import Client

commands = ["define", "dict", "definition"]

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"


async def handle(app: Client, client: Client, message, args):
    if not args:
        await app.send_message(
            message.chat.id,
            "📖 **define** — look up word definitions\n"
            "Usage: `.define word`\n"
            "Example: `.define serendipity`",
        )
        return

    word = " ".join(args).strip().lower()
    url = API_URL.format(urllib.parse.quote(word))

    try:
        req = urllib.request.urlopen(url, timeout=10)
        data = json.loads(req.read().decode())[0]

        phonetic = data.get("phonetic", "")
        word_title = data.get("word", word)

        lines = [f"📖 **{word_title.capitalize()}**"]
        if phonetic:
            lines.append(f"🔊 `{phonetic}`")

        for i, meaning in enumerate(data.get("meanings", [])[:3]):
            part_of_speech = meaning.get("partOfSpeech", "")
            defs = meaning.get("definitions", [])
            if defs:
                top_def = defs[0]
                definition = top_def.get("definition", "")
                example = top_def.get("example", "")
                lines.append(f"\n**{part_of_speech}**")
                lines.append(f"   {definition}")
                if example:
                    lines.append(f"   _\"{example}\"_")

        await app.send_message(message.chat.id, "\n".join(lines))

    except urllib.error.HTTPError as e:
        if e.code == 404:
            await app.send_message(
                message.chat.id,
                f"📛 **Not found:** no definition for `{word}`",
            )
        else:
            await app.send_message(
                message.chat.id,
                f"📛 **Error:** API returned {e.code}",
            )
    except (urllib.error.URLError, json.JSONDecodeError):
        await app.send_message(
            message.chat.id,
            "📛 **Error:** could not reach dictionary service",
        )
    except Exception as e:
        await app.send_message(
            message.chat.id,
            f"📛 **Error:** `{e}`",
        )
