"""ping module — check telegram ping and bot uptime"""
import time
import socket
from pyrogram import Client

commands = ["ping", "pong", "alive", "check"]
_start_time = time.monotonic()


def _get_ping() -> str:
    """Measure latency to Telegram servers."""
    try:
        start = time.time()
        socket.create_connection(("149.154.167.51", 80), timeout=5)
        elapsed = (time.time() - start) * 1000
        return f"{elapsed:.2f} ms"
    except OSError:
        return "⚠️ Error connecting to Telegram."


def _format_uptime(seconds: float) -> str:
    """Format uptime seconds into a human-readable string."""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    parts.append(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    return " ".join(parts)


async def handle(app: Client, client: Client, message, args):
    ping_time = _get_ping()
    uptime = _format_uptime(time.monotonic() - _start_time)
    await app.send_message(
        message.chat.id,
        f"⚡ **Telegram ping:** `{ping_time}`\n🚀 **Uptime:** `{uptime}`",
    )
