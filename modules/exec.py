import subprocess
from pyrogram import Client

commands = ["exec"]

async def handle(app: Client, client: Client, message, args):
    if not args:
        await app.send_message(
            message.chat.id,
            "💻 **exec** — run shell commands\n"
            "Usage: `.exec command`\n"
            "Example: `.exec ls -la`\n"
            "⚠️ Works on the server where bot is hosted",
        )
        return

    command = " ".join(args)
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout if result.stdout else result.stderr
        if not output:
            output = "✅ Command executed (no output)"
        await app.send_message(message.chat.id,
                                f"🔰 **Command:** `{command}`\n\n🔅 **Output:** ```{output}```")
    except subprocess.TimeoutExpired:
        await app.send_message(message.chat.id, f"⏱ **Timeout:** command `{command}` took too long")
    except Exception as e:
        await app.send_message(message.chat.id, f"📛 **Error:** {e}")
