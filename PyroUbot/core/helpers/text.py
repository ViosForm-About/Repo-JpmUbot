from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PyroUbot import OWNER_ID, bot, ubot, get_expired_date


class MSG:
    def EXP_MSG_UBOT(X):
        return f"""
<blockquote>
<b>❏ ⚠️ PEMBERITAHUAN KADALUARSA ⚠️</b>
<b>├─ • Nama Akun:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├─ • ID Pengguna:</b> <code>{X.me.id}</code>
<b>├─ • Status:</b> <code>Tidak Aktif</code>
<b>╰─ • Masa aktif telah habis</b>
</blockquote>
"""

    def START(message):
        return f"""
<blockquote>
<b>✨ HALO {message.from_user.first_name}! ✨</b>

<b>🤖 @{bot.me.username}</b>
<i>Bot pembuat Userbot Telegram</i>

<b>📈 STATS:</b>
├ Userbot aktif: <b>{len(ubot._ubot)}</b>
├ Owner: <a href=tg://openmessage?user_id={OWNER_ID}>@Viosf_12</a>
╰ Version: <b>SolidS v2.0</b>

<b>🚀 Pilih menu untuk memulai:</b>
</blockquote>
"""

    def TEXT_PAYMENT(harga, total, bulan):
        return f"""
<blockquote>
<b>╭══════════════════╮</b>
<b>│   💳 PEMBAYARAN   │</b>
<b>╰══════════════════╯</b>

<b>📋 Rincian Pesanan:</b>
<b>├─ • Harga/Bulan: Rp {harga}.000</b>
<b>├─ • Durasi: {bulan} Bulan</b>
<b>├─ • Total: Rp {total}.000</b>
<b>│</b>
<b>├ 💰 Metode Pembayaran:</b>
<b>│   • QRIS All Payment</b>
<b>│   • Transfer Bank</b>
<b>│   • E-Wallet</b>
<b>│</b>
<b>├ 📞 Kontak Admin:</b>
<b>│   <a href=tg://openmessage?user_id={OWNER_ID}>@Viosf_12</a></b>
<b>│</b>
<b>╰ 🛒 <b>Instruksi:</b></b>
<b>   1. Lakukan pembayaran sesuai total</b>
<b>   2. Screenshot bukti bayar</b>
<b>   3. Klik tombol konfirmasi</b>
<b>   4. Tunggu aktivasi (1-5 menit)</b>
</blockquote>
"""

    async def UBOT(count):
        return f"""
<blockquote>
<b>╭══════════════════╮</b>
<b>│   👤 USERBOT INFO  │</b>
<b>╰══════════════════╯</b>

<b>📊 No. Urut: {int(count) + 1}/{len(ubot._ubot)}</b>
<b>├─ • Nama: <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a></b>
<b>├─ • User ID: <code>{ubot._ubot[int(count)].me.id}</code></b>
<b>├─ • Username: @{ubot._ubot[int(count)].me.username or 'Tidak ada'}</b>
<b>╰─ • Status: Aktif ✅</b>
</blockquote>
"""

    def POLICY():
        return """<blockquote>
<b>╭══════════════════╮</b>
<b>│   📜 KEBIJAKAN     │</b>
<b>╰══════════════════╯</b>

<b>🔒 Ketentuan Layanan:</b>
<b>• Setiap userbot maksimal 1 akun</b>
<b>• Dilarang spam/auto status</b>
<b>• Backup data secara berkala</b>
<b>• Masa aktif sesuai pembayaran</b>
<b>• Support 24 jam via admin</b>

<b>📞 Hubungi kami jika ada kendala:</b>
<b><a href=tg://openmessage?user_id={OWNER_ID}>@Viosf_12</a></b>
</blockquote>
"""
