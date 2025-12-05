import asyncio

from pyrogram.enums import ChatType
from pyrogram import filters

from .. import *
from PyroUbot import *

__MODULE__ = "ᴀᴜᴛᴏʀᴇsᴘᴏɴᴇ"
__HELP__ = """
<blockquote><b>『 bantuan autoresponse 』</b>

<b>perintah:</b> <code>{0}autoresponse</code> [reply pesan]
   <code>menyimpan pesan untuk autoresponse</code>

<b>perintah:</b> <code>{0}response</code> [on/off]
   <code>mengaktifkan/menonaktifkan autoresponse</code>

<b>catatan:</b>
• jika akun premium dan pesan yang di-reply mengandung emoji premium,
  maka emoji premium akan ditambahkan di respons
• autoresponse hanya bekerja di chat pribadi</blockquote>
"""

# Database keys
AUTORESPONSE_STATUS = "AUTORESPONSE_STATUS"
AUTORESPONSE_MESSAGE = "AUTORESPONSE_MESSAGE"
AUTORESPONSE_PREMIUM_EMOJI = "AUTORESPONSE_PREMIUM_EMOJI"

# Daftar emoji premium (contoh)
PREMIUM_EMOJIS = ["✨", "⭐", "🌟", "💫", "🎁", "🎉", "💰", "💎", "🔥", "🪐", "🤖", "👑", "💠", "🎯"]

def extract_premium_emoji(text):
    """Mengekstrak emoji premium dari teks"""
    for emoji in PREMIUM_EMOJIS:
        if emoji in text:
            return emoji
    return None

@PY.UBOT("autoresponse")
@PY.TOP_CMD
async def _(client, message):
    if not message.reply_to_message:
        return await message.reply("<b>Harap reply ke pesan yang ingin dijadikan autoresponse!</b>")
    
    if not message.reply_to_message.text and not message.reply_to_message.caption:
        return await message.reply("<b>Hanya pesan teks yang didukung!</b>")
    
    r = await message.reply("<b>Memproses...</b>")
    
    # Ambil teks dari pesan yang di-reply
    if message.reply_to_message.text:
        response_text = message.reply_to_message.text
    else:
        response_text = message.reply_to_message.caption or ""
    
    # Cek apakah ada emoji premium
    premium_emoji = extract_premium_emoji(response_text)
    
    # Jika akun premium dan ada emoji premium, tambahkan emoji
    if client.me.is_premium and premium_emoji:
        response_text = f"{premium_emoji} {response_text}"
        await set_vars(client.me.id, AUTORESPONSE_PREMIUM_EMOJI, premium_emoji)
    else:
        await set_vars(client.me.id, AUTORESPONSE_PREMIUM_EMOJI, "")
    
    # Simpan pesan response
    await set_vars(client.me.id, AUTORESPONSE_MESSAGE, response_text)
    
    await r.edit("<b>Autoresponse berhasil disimpan! Gunakan <code>.response on</code> untuk mengaktifkan.</b>")

@PY.UBOT("response")
@PY.TOP_CMD
async def _(client, message):
    args = message.text.split()
    
    if len(args) < 2:
        return await message.reply(f"<b>Gunakan: <code>{args[0]}</code> [on/off]</b>")
    
    status = args[1].lower()
    r = await message.reply("<b>Memproses...</b>")
    
    if status == "on":
        # Cek apakah sudah ada pesan response yang disimpan
        response_msg = await get_vars(client.me.id, AUTORESPONSE_MESSAGE)
        if not response_msg:
            await r.edit("<b>Silahkan set autoresponse terlebih dahulu dengan <code>.autoresponse</code></b>")
            return
        
        await set_vars(client.me.id, AUTORESPONSE_STATUS, "ON")
        await r.edit("<b>✅ Autoresponse telah diaktifkan!</b>")
        
    elif status == "off":
        await set_vars(client.me.id, AUTORESPONSE_STATUS, "OFF")
        await r.edit("<b>❌ Autoresponse telah dimatikan!</b>")
    else:
        await r.edit(f"<b>Gunakan: <code>{args[0]}</code> [on/off]</b>")

# Handler untuk auto response
@PY.ON_MESSAGE(filters.private & filters.incoming)
async def auto_response_handler(client, message):
    # Skip jika pesan dari diri sendiri
    if message.from_user and message.from_user.id == client.me.id:
        return
    
    # Skip jika pesan adalah command
    if message.text and message.text.startswith("."):
        return
    
    # Cek status autoresponse
    status = await get_vars(client.me.id, AUTORESPONSE_STATUS)
    if status != "ON":
        return
    
    # Ambil pesan response
    response_msg = await get_vars(client.me.id, AUTORESPONSE_MESSAGE)
    if not response_msg:
        return
    
    # Tambahkan delay kecil untuk menghindari flood
    await asyncio.sleep(1)
    
    try:
        # Kirim response
        await client.send_message(
            chat_id=message.chat.id,
            text=response_msg,
            reply_to_message_id=message.id
        )
    except Exception as e:
        print(f"Error sending auto response: {e}")

# Handler untuk menangani ketika ada perubahan status premium
@PY.ON_MESSAGE(filters.me & filters.command("autoresponse", prefixes="."))
async def update_premium_response(client, message):
    """Update response jika status premium berubah"""
    if not message.reply_to_message:
        return
    
    # Ambil pesan response yang lama
    old_response = await get_vars(client.me.id, AUTORESPONSE_MESSAGE)
    if not old_response:
        return
    
    # Cek apakah ada emoji premium di response lama
    premium_emoji_stored = await get_vars(client.me.id, AUTORESPONSE_PREMIUM_EMOJI)
    
    # Update berdasarkan status premium saat ini
    if client.me.is_premium and premium_emoji_stored:
        # Jika premium dan ada emoji premium yang disimpan, tambahkan
        if not old_response.startswith(premium_emoji_stored + " "):
            new_response = f"{premium_emoji_stored} {old_response}"
            await set_vars(client.me.id, AUTORESPONSE_MESSAGE, new_response)
    else:
        # Jika bukan premium, hapus emoji premium di awal
        if premium_emoji_stored and old_response.startswith(premium_emoji_stored + " "):
            new_response = old_response[len(premium_emoji_stored) + 1:]
            await set_vars(client.me.id, AUTORESPONSE_MESSAGE, new_response)

# Command untuk menampilkan status autoresponse
@PY.UBOT("response_status")
@PY.TOP_CMD
async def _(client, message):
    status = await get_vars(client.me.id, AUTORESPONSE_STATUS) or "OFF"
    response_msg = await get_vars(client.me.id, AUTORESPONSE_MESSAGE)
    
    if response_msg:
        preview = response_msg[:50] + "..." if len(response_msg) > 50 else response_msg
    else:
        preview = "Belum diset"
    
    text = f"""
<b>Status Autoresponse:</b>
├ <b>Status:</b> <code>{status}</code>
├ <b>Akun Premium:</b> <code>{'Ya' if client.me.is_premium else 'Tidak'}</code>
└ <b>Preview Response:</b>
   <code>{preview}</code>
"""
    await message.reply(text)