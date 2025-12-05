from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from PyroUbot.config import OWNER_ID
from PyroUbot import *



@PY.UBOT("prem")
async def _(client, message):
    user = message.from_user
    seller_id = await get_list_from_vars(bot.me.id, "SELER_USERS")
    if user.id not in seller_id:
        return
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("memproses...")
    if not user_id:
        return await msg.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ - ʙᴜʟᴀɴ</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    if not get_bulan:
        get_bulan = 1

    prem_users = await get_list_from_vars(bot.me.id, "PREM_USERS")

    if user.id in prem_users:
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ꜱᴜᴅᴀʜ ᴘʀᴇᴍɪᴜᴍ</ci></b>
<b>ᴇxᴘɪʀᴇᴅ: {get_bulan} ʙᴜʟᴀɴ</b></blockquote>
"""
        )

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await set_expired_date(user_id, expired)
        await add_to_vars(bot.me.id, "PREM_USERS", user.id)
        await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴇxᴘɪʀᴇᴅ: {get_bulan} ʙᴜʟᴀɴ</b>
<b>ꜱɪʟᴀʜᴋᴀɴ ʙᴜᴋᴀ @{bot.me.username} ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜꜱᴇʀʙᴏᴛ</b></blockquote>
"""
        )
        return await bot.send_message(
            OWNER_ID,
            f"• ɪᴅ-ꜱᴇʟʟᴇʀ: `{message.from_user.id}`\n\n• ɪᴅ-ᴄᴜꜱᴛᴏᴍᴇʀ: `{user_id}`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⁉️ ꜱᴇʟʟᴇʀ",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "ᴄᴜꜱᴛᴏᴍᴇʀ ⁉️", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("unprem")
async def _(client, message):
    msg = await message.reply("ꜱᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏꜱᴇꜱ...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    prem_users = await get_list_from_vars(bot.me.id, "PREM_USERS")

    if user.id not in prem_users:
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴛɪᴅᴀᴋ ᴛᴇʀᴅᴀꜰᴛᴀʀ</ci></b></blockquote>
"""
        )
    try:
        await remove_from_vars(bot.me.id, "PREM_USERS", user.id)
        await rem_expired_date(user_id)
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴛᴇʟᴀʜ ᴅɪ ʜᴀᴘᴜꜱ ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀꜱᴇ</ci></b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)
        

@PY.UBOT("getprem")
async def _(client, message):
    text = ""
    count = 0
    user = message.from_user
    seller_id = await get_list_from_vars(bot.me.id, "SELER_USERS")
    if user.id not in seller_id:
        return
    prem = await get_list_from_vars(bot.me.id, "PREM_USERS")
    prem_users = []

    for user_id in prem:
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"<blockquote><b>{userlist}\n</blockquote></b>"
    if not text:
        await message.reply_text("ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴅɪᴛᴇᴍᴜᴋᴀɴ")
    else:
        await message.reply_text(text)


@PY.UBOT("seles")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    msg = await message.reply("ꜱᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏꜱᴇꜱ...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await get_list_from_vars(bot.me.id, "SELER_USERS")

    if user.id in sudo_users:
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ꜱᴜᴅᴀʜ ʀᴇꜱᴇʟʟᴇʀ</ci></b></blockquote>
"""
        )

    try:
        await add_to_vars(bot.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ʀᴇꜱᴇʟʟᴇʀ</ci></b>
<b>ꜱɪʟᴀʜᴋᴀɴ ʙᴜᴋᴀ @{bot.me.username}</b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("unseles")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    msg = await message.reply("ꜱᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏꜱᴇꜱ...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seles_users = await get_list_from_vars(bot.me.id, "SELER_USERS")

    if user.id not in seles_users:
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴛɪᴅᴀᴋ ᴛᴇʀᴅᴀꜰᴛᴀʀ</ci></b></blockquote>
"""
        )

    try:
        await remove_from_vars(bot.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴛᴇʟᴀʜ ᴅɪ ʜᴀᴘᴜꜱ ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀꜱᴇ</ci></b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("getseles")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    Sh = await message.reply("ꜱᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏꜱᴇꜱ...")
    seles_users = await get_list_from_vars(bot.me.id, "SELER_USERS")

    if not seles_users:
        return await Sh.edit("ᴅᴀꜰᴛᴀʀ ꜱᴇʟʟᴇʀ ᴋᴏꜱᴏɴɢ")

    seles_list = []
    for user_id in seles_users:
        try:
            user = await client.get_users(int(user_id))
            seles_list.append(
                f"<blockquote>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | `{user.id}`</blockquote>"
            )
        except:
            continue

    if seles_list:
        response = (
            "📋 ᴅᴀꜰᴛᴀʀ ʀᴇꜱᴇʟʟᴇʀ:\n\n"
            + "\n".join(seles_list)
            + f"\n\n• ᴛᴏᴛᴀʟ ʀᴇꜱᴇʟʟᴇʀ: {len(seles_list)}"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴɢᴀᴍʙɪʟ ᴅᴀꜰᴛᴀʀ ꜱᴇʟʟᴇʀ")


@PY.UBOT("time")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    Tm = await message.reply("processing . . .")
    bajingan = message.command
    if len(bajingan) != 3:
        return await Tm.edit(f"gunakan /set_time user_id hari")
    user_id = int(bajingan[1])
    get_day = int(bajingan[2])
    print(user_id , get_day)
    try:
        get_id = (await client.get_users(user_id)).id
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    await Tm.edit(f"""
💬 INFORMATION
 name: {user.mention}
 id: {get_id}
 aktifkan_selama: {get_day} hari
"""
    )


@PY.UBOT("cek")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    Sh = await message.reply("ᴘʀᴏᴄᴇꜱꜱɪɴɢ . . .")
    user_id = await extract_user(message)
    if not user_id:
        return await Sh.edit("ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴛᴇᴍᴜᴋᴀɴ")
    try:
        get_exp = await get_expired_date(user_id)
        sh = await client.get_users(user_id)
    except Exception as error:
        return await Sh.ediit(error)
    if get_exp is None:
        await Sh.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: {sh.mention}</b>
<b>ɪᴅ: `{user_id}`</b>
<b>ᴘʟᴀɴ : ɴᴏɴᴇ</b>
<b>ᴘʀᴇꜰɪx : .</b>
<b>ᴇxᴘɪʀᴇᴅ : ɴᴏɴᴀᴋᴛɪꜰ</b></blockquote>
""")
    else:
        SH = await ubot.get_prefix(user_id)
        exp = get_exp.strftime("%d-%m-%Y")
        if user_id in await get_list_from_vars(bot.me.id, "ULTRA_PREM"):
            status = "SuperUltra"
        else:
            status = "Premium"
        await Sh.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: {sh.mention}</b>
<b>ɪᴅ: `{user_id}`</b>
<b>ᴘʟᴀɴ : {status}</b>
<b>ᴘʀᴇꜰɪx : {' '.join(SH)}</b>
<b>ᴇxᴘɪʀᴇᴅ : {exp}</b></blockquote>
"""
        )


@PY.UBOT("addadmin")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await get_list_from_vars(bot.me.id, "ADMIN_USERS")

    if user.id in admin_users:
        return await msg.edit(f"""
💬 INFORMATION
name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
id: {user.id}
keterangan: sudah dalam daftar
"""
        )

    try:
        await add_to_vars(bot.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
💬 INFORMATION
name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
id: {user.id}
keterangan: admin
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("unadmin")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await get_list_from_vars(bot.me.id, "ADMIN_USERS")

    if user.id not in admin_users:
        return await msg.edit(f"""
💬 INFORMATION
name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
id: {user.id}
keterangan: tidak daam daftar
"""
        )

    try:
        await remove_from_vars(bot.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
💬 INFORMATION
name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
id: {user.id}
keterangan: unadmin
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("getadmin")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return
    Sh = await message.reply("sedang memproses...")
    admin_users = await get_list_from_vars(bot.me.id, "ADMIN_USERS")

    if not admin_users:
        return await Sh.edit("<s>daftar admin kosong</s>")

    admin_list = []
    for user_id in admin_users:
        try:
            user = await client.get_users(int(user_id))
            admin_list.append(
                f"👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | {user.id}"
            )
        except:
            continue

    if admin_list:
        response = (
            "📋 daftar admin:\n\n"
            + "\n".join(admin_list)
            + f"\n\n⚜️ total admin: {len(admin_list)}"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("tidak dapat mengambil daftar admin")

@PY.UBOT("addowner")
async def addowner_handler(client, message):
    user = message.from_user
    # Hanya developer yang bisa menambah owner
    if user.id != OWNER_ID:
        return await message.reply_text(f"❌ ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴅᴇᴠᴇʟᴏᴘᴇʀ!")
    
    msg = await message.reply("⏳ ꜱᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏꜱᴇꜱ...")
    user_id = await extract_user(message)
    
    if not user_id:
        return await msg.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>")
    
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(str(error))
    
    # Cek apakah user sudah menjadi owner
    owner_users = await get_list_from_vars(bot.me.id, "OWNER_USERS") or []
    
    if user.id in owner_users:
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ꜱᴜᴅᴀʜ ᴍᴇɴᴊᴀᴅɪ ᴏᴡɴᴇʀ</b></blockquote>
""")
    
    try:
        # Tambahkan ke daftar owner
        await add_to_vars(bot.me.id, "OWNER_USERS", user.id)
        
        # Berikan semua hak akses (prem, seles, admin, ultra)
        await add_to_vars(bot.me.id, "PREM_USERS", user.id)
        await add_to_vars(bot.me.id, "SELER_USERS", user.id)
        await add_to_vars(bot.me.id, "ADMIN_USERS", user.id)
        await add_to_vars(bot.me.id, "ULTRA_PREM", user.id)
        
        # Set expired date (misalnya 1 tahun)
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(years=1)
        await set_expired_date(user.id, expired)
        
        return await msg.edit(f"""
<blockquote><b>✅ ʙᴇʀʜᴀsɪʟ ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴏᴡɴᴇʀ</b>
<b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴏᴡɴᴇʀ</b>
<b>ʜᴀᴋ ᴀᴋsᴇs:</b>
├ ᴘʀᴇᴍɪᴜᴍ ✅
├ ʀᴇsᴇʟʟᴇʀ ✅
├ ᴀᴅᴍɪɴ ✅
╰ sᴜᴘᴇʀᴜʟᴛʀᴀ ✅
<b>ᴇxᴘɪʀᴇᴅ: 1 ᴛᴀʜᴜɴ</b></blockquote>
""")
    except Exception as error:
        return await msg.edit(str(error))


@PY.UBOT("unowner")
async def unowner_handler(client, message):
    user = message.from_user
    # Hanya developer yang bisa menghapus owner
    if user.id != OWNER_ID:
        return await message.reply_text(f"❌ ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴅᴇᴠᴇʟᴏᴘᴇʀ!")
    
    msg = await message.reply("⏳ ꜱᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏꜱᴇꜱ...")
    user_id = await extract_user(message)
    
    if not user_id:
        return await msg.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>")
    
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(str(error))
    
    # Cek apakah user adalah owner
    owner_users = await get_list_from_vars(bot.me.id, "OWNER_USERS") or []
    
    if user.id not in owner_users:
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ʙᴜᴋᴀɴ ᴏᴡɴᴇʀ</b></blockquote>
""")
    
    try:
        # Hapus dari daftar owner
        await remove_from_vars(bot.me.id, "OWNER_USERS", user.id)
        
        # Tapi TIDAK menghapus hak akses lainnya (prem, seles, admin, ultra)
        # Biarkan tetap ada sebagai bentuk penghargaan
        
        return await msg.edit(f"""
<blockquote><b>✅ ʙᴇʀʜᴀsɪʟ ᴍᴇɴɢʜᴀᴘᴜs ᴏᴡɴᴇʀ</b>
<b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: `{user.id}`</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ʙᴜᴋᴀɴ ᴏᴡɴᴇʀ</b>
<b>ʜᴀᴋ ᴀᴋsᴇs:</b>
├ ᴘʀᴇᴍɪᴜᴍ ✅ (ᴛᴇᴛᴀᴘ ᴀᴋᴛɪғ)
├ ʀᴇsᴇʟʟᴇʀ ✅ (ᴛᴇᴛᴀᴘ ᴀᴋᴛɪғ)
├ ᴀᴅᴍɪɴ ✅ (ᴛᴇᴛᴀᴘ ᴀᴋᴛɪғ)
╰ sᴜᴘᴇʀᴜʟᴛʀᴀ ✅ (ᴛᴇᴛᴀᴘ ᴀᴋᴛɪғ)</blockquote>
""")
    except Exception as error:
        return await msg.edit(str(error))


@PY.UBOT("getowner")
async def getowner_handler(client, message):
    user = message.from_user
    
    # Cek apakah user adalah developer atau owner
    owner_users = await get_list_from_vars(bot.me.id, "OWNER_USERS") or []
    
    if user.id != OWNER_ID and user.id not in owner_users:
        return await message.reply_text(f"❌ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ᴀᴋsᴇs!")
    
    Sh = await message.reply("⏳ ꜱᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏꜱᴇꜱ...")
    owner_users = await get_list_from_vars(bot.me.id, "OWNER_USERS") or []
    
    if not owner_users:
        return await Sh.edit("<blockquote><b>📭 ᴅᴀꜰᴛᴀʀ ᴏᴡɴᴇʀ ᴋᴏꜱᴏɴɢ</b></blockquote>")
    
    text = "<blockquote><b>📋 ᴅᴀꜰᴛᴀʀ ᴏᴡɴᴇʀ:</b></blockquote>\n"
    count = 0
    
    for owner_id in owner_users:
        try:
            owner = await client.get_users(owner_id)
            count += 1
            
            # Cek apakah user adalah developer
            if owner_id == OWNER_ID:
                status = "👑 ᴅᴇᴠᴇʟᴏᴘᴇʀ"
            else:
                status = "👑 ᴏᴡɴᴇʀ"
            
            text += f"""
<blockquote><b>{count}. {owner.mention}</b>
├ <b>ɪᴅ:</b> <code>{owner_id}</code>
├ <b>ᴜsᴇʀɴᴀᴍᴇ:</b> @{owner.username if owner.username else 'ᴛɪᴅᴀᴋ ᴀᴅᴀ'}
╰ <b>ꜱᴛᴀᴛᴜs:</b> {status}</blockquote>
"""
        except Exception:
            continue
    
    text += f"\n<blockquote><b>📊 ᴛᴏᴛᴀʟ ᴏᴡɴᴇʀ: {count}</b></blockquote>"
    await Sh.edit(text)


@PY.UBOT("myowner")
async def myowner_handler(client, message):
    user = message.from_user
    
    # Cek apakah user adalah developer
    if user.id == OWNER_ID:
        return await message.reply("""
<blockquote><b>👑 ꜱᴛᴀᴛᴜꜱ: ᴅᴇᴠᴇʟᴏᴘᴇʀ</b>
<b>├ ᴘᴇʀɪɴᴛᴀʜ ᴋʜᴜꜱᴜꜱ:</b>
├ <code>/addowner</code> - ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴏᴡɴᴇʀ
├ <code>/unowner</code> - ᴍᴇɴɢʜᴀᴘᴜꜱ ᴏᴡɴᴇʀ
├ <code>/getowner</code> - ᴍᴇʟɪʜᴀᴛ ᴅᴀꜰᴛᴀʀ ᴏᴡɴᴇʀ
╰ <code>/myowner</code> - ᴍᴇʟɪʜᴀᴛ ꜱᴛᴀᴛᴜꜱ</blockquote>
""")
    
    # Cek apakah user adalah owner
    owner_users = await get_list_from_vars(bot.me.id, "OWNER_USERS") or []
    
    if user.id in owner_users:
        return await message.reply("""
<blockquote><b>👑 ꜱᴛᴀᴛᴜꜱ: ᴏᴡɴᴇʀ</b>
<b>├ ᴘᴇʀɪɴᴛᴀʜ ᴋʜᴜꜱᴜꜱ:</b>
├ <code>/addadmin</code> - ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴀᴅᴍɪɴ
├ <code>/addseles</code> - ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ʀᴇsᴇʟʟᴇʀ
├ <code>/addprem</code> - ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴘʀᴇᴍɪᴜᴍ
├ <code>/addultra</code> - ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ sᴜᴘᴇʀᴜʟᴛʀᴀ
╰ <code>/myowner</code> - ᴍᴇʟɪʜᴀᴛ ꜱᴛᴀᴛᴜꜱ</blockquote>
""")
    
    # Jika bukan developer atau owner
    await message.reply("<blockquote><b>❌ ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴀᴛᴀᴜ ᴏᴡɴᴇʀ!</b></blockquote>")


@PY.UBOT("checkowner")
async def checkowner_handler(client, message):
    user = message.from_user
    msg = await message.reply("⏳ ꜱᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏꜱᴇꜱ...")
    
    # Cek status user
    owner_users = await get_list_from_vars(bot.me.id, "OWNER_USERS") or []
    seller_users = await get_list_from_vars(bot.me.id, "SELER_USERS") or []
    admin_users = await get_list_from_vars(bot.me.id, "ADMIN_USERS") or []
    prem_users = await get_list_from_vars(bot.me.id, "PREM_USERS") or []
    ultra_users = await get_list_from_vars(bot.me.id, "ULTRA_PREM") or []
    
    status_text = f"""
<blockquote><b>📊 ꜱᴛᴀᴛᴜꜱ ᴀᴋsᴇs</b>
<b>├ ɴᴀᴍᴇ:</b> {user.mention}
<b>├ ɪᴅ:</b> <code>{user.id}</code>
<b>├ ᴅᴇᴠᴇʟᴏᴘᴇʀ:</b> {'✅' if user.id == OWNER_ID else '❌'}
<b>├ ᴏᴡɴᴇʀ:</b> {'✅' if user.id in owner_users else '❌'}
<b>├ ʀᴇsᴇʟʟᴇʀ:</b> {'✅' if user.id in seller_users else '❌'}
<b>├ ᴀᴅᴍɪɴ:</b> {'✅' if user.id in admin_users else '❌'}
<b>├ ᴘʀᴇᴍɪᴜᴍ:</b> {'✅' if user.id in prem_users else '❌'}
<b>╰ sᴜᴘᴇʀᴜʟᴛʀᴀ:</b> {'✅' if user.id in ultra_users else '❌'}</blockquote>
"""
    
    await msg.edit(status_text)

@PY.UBOT("addultra")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply_text(f"{ggl}mau ngapain kamu ?")
    msg = await message.reply(f"{prs}sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{ggl}{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    ultra_users = await get_list_from_vars(bot.me.id, "ULTRA_PREM")

    if user.id in ultra_users:
        return await msg.edit(f"{ggl}sudah menjadi superultra!")

    try:
        await add_to_vars(bot.me.id, "ULTRA_PREM", user.id)
        return await msg.edit(f"{brhsl}berhasil menjadi superultra")
    except Exception as error:
        return await msg.edit(error)

@PY.UBOT("rmultra")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply_text(f"{ggl}mau ngapain kamu ?")
    msg = await message.reply(f"{prs}sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{ggl}{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    ultra_users = await get_list_from_vars(bot.me.id, "ULTRA_PREM")

    if user.id not in ultra_users:
        return await msg.edit(f"{ggl}tidak ada di dalam database superultra")

    try:
        await remove_from_vars(bot.me.id, "ULTRA_PREM", user.id)
        return await msg.edit(f"{brhsl}berhasil di hapus dari daftar superultra")
    except Exception as error:
        return await msg.edit(error)
