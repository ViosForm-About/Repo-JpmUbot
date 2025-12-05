import asyncio
import importlib
from datetime import datetime

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.raw import functions

from PyroUbot import *


@PY.BOT("start")
@PY.START
@PY.PRIVATE
async def _(client, message):
    user_id = message.from_user.id
    buttons = BTN.START(message)
    msg = MSG.START(message)
    pantek = "https://files.catbox.moe/17utal.jpg"

    await bot.send_photo(
        user_id, 
        pantek, 
        caption=msg, 
        reply_markup=buttons if buttons else None
    )


@PY.BOT("bahan")
async def _(client, message):
    user_id = message.from_user.id
    if user_id in ubot._get_my_id:
        buttons = BTN.ALREADY_UBOT()
        text = """
<blockquote><b>⌭ ᴀɴᴅᴀ ꜱᴜᴅᴀʜ ᴍᴇᴍʙᴜᴀᴛ ᴜꜱᴇʀʙᴏᴛ

⌭ ᴊɪᴋᴀ ᴜꜱᴇʀʙᴏᴛ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʙɪꜱᴀ ᴅɪɢᴜɴᴀᴋᴀɴ ꜱɪʟᴀʜᴋᴀɴ ᴋᴇᴛɪᴋ /restart</b></blockquote>
"""
        await message.reply(text, reply_markup=buttons)
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = BTN.BACK_HOME()
        text = f"""
<blockquote><b><b>☫ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ!</b>

<b>☫ ᴋᴀʀᴇɴᴀ ᴍᴀᴋsɪᴍᴀʟ ᴜsᴇʀʙᴏᴛ ᴀᴅᴀʟᴀʜ {Fonts.smallcap(str(len(ubot._ubot)))} ᴛᴇʟᴀʜ ᴛᴇʀᴄᴀᴘᴀɪ</b>

<blockquote><b>☫ sɪʟᴀʜᴋᴀɴ ʜᴜʙᴜɴɢɪ owner</b></blockquote>
"""
        await message.reply(text, reply_markup=buttons)
    else:
        premium_users, ultra_premium_users = await get_list_from_vars(client.me.id, "PREM_USERS"), await get_list_from_vars(client.me.id, "ULTRA_PREM")
        if user_id not in premium_users and user_id not in ultra_premium_users:
            buttons = BTN.PAYMENT_OPTIONS()
            await message.reply(MSG.POLICY(), reply_markup=buttons)
        else:
            buttons = BTN.CONTINUE_CREATE()
            await message.reply(
                "<blockquote><b>⌭ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇᴍʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ꜱɪʟᴀʜᴋᴀɴ ᴋᴇᴛɪᴋ /buat_ubot ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜꜱᴇʀʙᴏᴛ</b></blockquote>",
                reply_markup=buttons
            )


@PY.BOT("status")
async def _(client, message):
    user_id = message.from_user.id
    if user_id in ubot._get_my_id:
        buttons = BTN.BACK_HOME()
        exp = await get_expired_date(user_id)
        prefix = await get_pref(user_id)
        waktu = exp.strftime("%d-%m-%Y") if exp else "None"
        text = f"""
<blockquote> ᴜꜱᴇʀʙᴏᴛ ᴘʀᴇᴍɪᴜᴍ ʙʏ @yaetiem
   ꜱᴛᴀᴛᴜꜱ : ᴘʀᴇᴍɪᴜᴍ
   ᴘʀᴇꜰɪxᴇꜱ : {prefix[0]}
   ᴇxᴘɪʀᴇᴅ_ᴏɴ : {waktu}</b></blockquote>
"""
        await message.reply(text, reply_markup=buttons)
    else:
        buttons = BTN.BUY_UBOT_OPTIONS()
        await message.reply(
            "<blockquote><b>✮ ᴍᴀᴀꜰ ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴍᴇᴍʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ, ꜱɪʟᴀᴋᴀɴ ᴍᴇᴍʙᴇʟɪ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ.</b></blockquote>",
            reply_markup=buttons
        )


@PY.BOT("buat_ubot")
async def _(client, message):
    user_id = message.from_user.id
    if user_id in ubot._get_my_id:
        buttons = BTN.ALREADY_UBOT()
        await message.reply(
            "<blockquote><b>✮ ᴀɴᴅᴀ ꜱᴜᴅᴀʜ ᴍᴇᴍʙᴜᴀᴛ ᴜꜱᴇʀʙᴏᴛ\n\n✮ ᴊɪᴋᴀ ᴜꜱᴇʀʙᴏᴛ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ʙɪꜱᴀ ᴅɪɢᴜɴᴀᴋᴀɴ ꜱɪʟᴀʜᴋᴀɴ ᴋᴇᴛɪᴋ /restart</b></blockquote>",
            reply_markup=buttons
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        buttons = BTN.BACK_HOME()
        text = f"""
<blockquote><b><b>✮ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ!</b>

<b>✮ ᴋᴀʀᴇɴᴀ ᴍᴀᴋsɪᴍᴀʟ ᴜsᴇʀʙᴏᴛ ᴀᴅᴀʟᴀʜ {Fonts.smallcap(str(len(ubot._ubot)))} ᴛᴇʟᴀʜ ᴛᴇʀᴄᴀᴘᴀɪ</b>

<blockquote><b>✮ sɪʟᴀʜᴋᴀɴ ʜᴜʙᴜɴɢɪ: ᴀᴅᴍɪɴ ᴊɪᴋᴀ ᴍᴀᴜ ᴅɪʙᴜᴀᴛᴋᴀɴ ʙᴏᴛ sᴇᴘᴇʀᴛɪ sᴀʏᴀ </b></blockquote>
"""
        await message.reply(text, reply_markup=buttons)
    else:
        premium_users, ultra_premium_users = await get_list_from_vars(client.me.id, "PREM_USERS"), await get_list_from_vars(client.me.id, "ULTRA_PREM")
        if user_id not in premium_users and user_id not in ultra_premium_users:
            buttons = BTN.BUY_UBOT_OPTIONS()
            await message.reply(
                "<blockquote><b>✮ ᴍᴀᴀꜰ ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴍᴇᴍʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ, ꜱɪʟᴀᴋᴀɴ ᴍᴇᴍʙᴇʟɪ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b></blockquote>",
                reply_markup=buttons
            )
        else:
            buttons = BTN.CONTINUE_CREATE()
            await message.reply(
                """
<blockquote><b>✮ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ sɪᴀᴘᴋᴀɴ ʙᴀʜᴀɴ ʙᴇʀɪᴋᴜᴛ

    ✮ <code>ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ</code>: ɴᴏᴍᴇʀ ʜᴘ ᴀᴋᴜɴ ᴛᴇʟᴇɢʀᴀᴍ

✮ ᴊɪᴋᴀ sᴜᴅᴀʜ ᴛᴇʀsᴇᴅɪᴀ sɪʟᴀʜᴋᴀɴ ᴋᴇᴛɪᴋ /add_ubot</b></blockquote>
""",
                reply_markup=buttons
            )


@PY.BOT("bayar_dulu")
async def _(client, message):
    user_id = message.from_user.id
    buttons = BTN.PAYMENT_CONFIRMATION()
    await message.reply(
        MSG.TEXT_PAYMENT(30, 30, 1),
        reply_markup=buttons
    )


@PY.BOT("add_ubot")
async def _(client, message):
    user_id = message.from_user.id
    
    # Cek apakah user sudah memiliki userbot
    if user_id in ubot._get_my_id:
        await message.reply(
            "<blockquote><b>✮ ᴀɴᴅᴀ ꜱᴜᴅᴀʜ ᴍᴇᴍʙᴜᴀᴛ ᴜꜱᴇʀʙᴏᴛ\n\n✮ ɢᴜɴᴀᴋᴀɴ /restart ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</b></blockquote>",
            reply_markup=BTN.BACK_HOME()
        )
        return

    await message.reply(
        "<b>✮ sɪʟᴀʜᴋᴀɴ ᴍᴀsᴜᴋᴋᴀɴ ɴᴏᴍᴏʀ ᴛᴇʟᴇᴘᴏɴ ᴛᴇʟᴇɢʀᴀᴍ ᴀɴᴅᴀ ᴅᴇɴɢᴀɴ ꜰᴏʀᴍᴀᴛ ᴋᴏᴅᴇ ɴᴇɢᴀʀᴀ.\nᴄᴏɴᴛᴏʜ: +628xxxxxxx</b>\n\n<b>✮ ɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ</b>"
    )
    
    try:
        phone = await bot.listen(user_id, timeout=300)
    except asyncio.TimeoutError:
        await message.reply("<blockquote>✮ ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪꜱ!\n✮ ɢᴜɴᴀᴋᴀɴ /start ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
        return
    
    if phone.text == '/cancel':
        await message.reply("<blockquote>✮ ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴅɪʟᴀᴋᴜᴋᴀɴ!\n✮ ɢᴜɴᴀᴋᴀɴ /start ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
        return
    
    phone_number = phone.text
    new_client = Ubot(
        name=str(message.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )
    
    get_otp = await message.reply("<blockquote><b>✮ ᴍᴇɴɢɪʀɪᴍ ᴋᴏᴅᴇ ᴏᴛᴘ...</b></blockquote>")
    await new_client.connect()
    
    try:
        code = await new_client.send_code(phone_number.strip())
    except ApiIdInvalid as AID:
        await get_otp.delete()
        await message.reply(str(AID))
        return
    except PhoneNumberInvalid as PNI:
        await get_otp.delete()
        await message.reply(str(PNI))
        return
    except PhoneNumberFlood as PNF:
        await get_otp.delete()
        await message.reply(str(PNF))
        return
    except PhoneNumberBanned as PNB:
        await get_otp.delete()
        await message.reply(str(PNB))
        return
    except PhoneNumberUnoccupied as PNU:
        await get_otp.delete()
        await message.reply(str(PNU))
        return
    except Exception as error:
        await get_otp.delete()
        await message.reply(f"ERROR: {error}")
        return
    
    await get_otp.delete()
    await message.reply(
        "<b>✮ sɪʟᴀᴋᴀɴ ᴘᴇʀɪᴋsᴀ ᴋᴏᴅᴇ ᴏᴛᴘ ᴅᴀʀɪ ᴀᴋᴜɴ ʀᴇꜱᴍɪ ᴛᴇʟᴇɢʀᴀᴍ. ᴋɪʀɪᴍ ᴋᴏᴅᴇ ᴏᴛᴘ ᴋᴇ sɪɴɪ sᴇᴛᴇʟᴀʜ ᴍᴇᴍʙᴀᴄᴀ ꜰᴏʀᴍᴀᴛ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ.</b>\n"
        "\n✮ ᴊɪᴋᴀ ᴋᴏᴅᴇ ᴏᴛᴘ ᴀᴅᴀʟᴀʜ <code>12345</code> ᴛᴏʟᴏɴɢ <b>[ ᴛᴀᴍʙᴀʜᴋᴀɴ sᴘᴀsɪ ]</b> ᴋɪʀɪᴍᴋᴀɴ sᴇᴘᴇʀᴛɪ ɪɴɪ <code>1 2 3 4 5</code>\n"
        "\n<b>✮ ɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ</b>"
    )
    
    try:
        otp = await bot.listen(user_id, timeout=300)
    except asyncio.TimeoutError:
        await message.reply("<blockquote>✮ ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪꜱ!\n✮ ɢᴜɴᴀᴋᴀɴ /start ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
        return
    
    if otp.text == '/cancel':
        await message.reply("<blockquote>✮ ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴅɪʟᴀᴋᴜᴋᴀɴ!\n✮ ɢᴜɴᴀᴋᴀɴ /start ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
        return
    
    otp_code = otp.text
    
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid as PCI:
        await message.reply(str(PCI))
        return
    except PhoneCodeExpired as PCE:
        await message.reply(str(PCE))
        return
    except BadRequest as error:
        await message.reply(f"ERROR: {error}")
        return
    except SessionPasswordNeeded:
        await message.reply(
            "✮ ᴀᴋᴜɴ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇɴɢᴀᴋᴛɪꜰᴋᴀɴ ᴠᴇʀɪꜰɪᴋᴀsɪ ᴅᴜᴀ ʟᴀɴɢᴋᴀʜ. sɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍᴋᴀɴ ᴘᴀssᴡᴏʀᴅɴʏᴀ.\n\n✮ ɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ</b>"
        )
        
        try:
            two_step_code = await bot.listen(user_id, timeout=300)
        except asyncio.TimeoutError:
            await message.reply("<blockquote>✮ ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪꜱ!\n✮ ɢᴜɴᴀᴋᴀɴ /start ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
            return
        
        if two_step_code.text == '/cancel':
            await message.reply("<blockquote>✮ ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴅɪʟᴀᴋᴜᴋᴀɴ!\n✮ ɢᴜɴᴀᴋᴀɴ /start ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
            return
        
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
        except Exception as error:
            await message.reply(f"ERROR: {error}")
            return
    
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    
    bot_msg = await message.reply(
        "sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs....\n\n✮ sɪʟᴀʜᴋᴀɴ ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ"
    )
    
    await new_client.start()
    
    if not user_id == new_client.me.id:
        ubot._ubot.remove(new_client)
        await bot_msg.edit(
            "<b>✮ ʜᴀʀᴀᴘ ɢᴜɴᴀᴋᴀɴ ɴᴏᴍᴇʀ ᴛᴇʟᴇɢʀᴀᴍ ᴀɴᴅᴀ ᴅɪ ᴀᴋᴜɴ ᴀɴᴅᴀ sᴀᴀᴛ ɪɴɪ ᴅᴀɴ ʙᴜᴋᴀɴ ɴᴏᴍᴇʀ ᴛᴇʟᴇɢʀᴀᴍ ᴅᴀʀɪ ᴀᴋᴜɴ ʟᴀɪɴ</b>"
        )
        return
    
    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"PyroUbot.modules.{mod}"))
    
    SH = await ubot.get_prefix(new_client.me.id)
    buttons = BTN.BACK_HOME()
    
    text_done = f"""
<blockquote><b>✮ ʙᴇʀʜᴀꜱɪʟ ᴅɪᴀᴋᴛɪꜰᴋᴀɴ
ᚗ ɴᴀᴍᴇ : <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a>
ᚗ ɪᴅ : {new_client.me.id}
ᚗ ᴘʀᴇꜰɪxᴇꜱ : {' '.join(SH)}
⌭ ʜᴀʀᴀᴘ hubungi admin ᴜɴᴛᴜᴋ ɪɴꜰᴏ" ᴛᴇʀʙᴀʀᴜ
ᴊɪᴋᴀ ʙᴏᴛ ᴛɪᴅᴀᴋ ʀᴇꜱᴘᴏɴ, ᴋᴇᴛɪᴋ /restart</b></blockquote>
"""
    await bot_msg.edit(text_done, reply_markup=buttons)
    await bash("rm -rf *session*")
    await install_my_peer(new_client)
    
    try:
        await new_client.join_chat("q1ngzs")
        await new_client.join_chat("q1ngzs")
        await new_client.join_chat("q1ngzs")
    except UserAlreadyParticipant:
        pass

    await bot.send_message(
        LOGS_MAKER_UBOT,
        f"""
<b>⌬ ᴜsᴇʀʙᴏᴛ ᴅɪᴀᴋᴛɪғᴋᴀɴ</b>
<b> ├ ᴀᴋᴜɴ:</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> 
<b> ╰ ɪᴅ:</b> <code>{new_client.me.id}</code>
"""
    )


@PY.BOT("control")
async def _(client, message):
    buttons = BTN.RESTART_BUTTON()
    await message.reply(
        "<blockquote><b>✮ ᴀɴᴅᴀ ᴀᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ʀᴇꜱᴛᴀʀᴛ?!\n✮ ᴊɪᴋᴀ ɪʏᴀ ᴋᴇᴛɪᴋ /restart</b></blockquote>",
        reply_markup=buttons
    )


@PY.BOT("restart")
async def _(client, message):
    msg = await message.reply("<b>✮ ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>")
    if message.from_user.id not in ubot._get_my_id:
        await msg.edit("❌ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ᴀᴋsᴇs")
        return
    
    for X in ubot._ubot:
        if message.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        ubot._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"PyroUbot.modules.{mod}")
                            )
                        await msg.edit(
                            f"✮ ʀᴇꜱᴛᴀʀᴛ ʙᴇʀʜᴀꜱɪʟ ᴅɪʟᴀᴋᴜᴋᴀɴ !\n\n ✮ ɴᴀᴍᴇ: {UB.me.first_name} {UB.me.last_name or ''} | {UB.me.id}"
                        )
                        return
                    except Exception as error:
                        await msg.edit(f"ERROR: {error}")
                        return


@PY.BOT("getubot")
@PY.ADMIN
async def _(client, message):
    await message.reply(
        await MSG.UBOT(0),
        reply_markup=BTN.UBOT_MENU()
    )


@PY.BOT("cek_masa_aktif")
async def _(client, message):
    user_id = message.from_user.id
    expired = await get_expired_date(user_id)
    try:
        xxxx = (expired - datetime.now()).days
        await message.reply(f"✮ ᴛɪɴɢɢᴀʟ {xxxx} ʜᴀʀɪ ʟᴀɢɪ")
    except:
        await message.reply("✮ sᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴀᴋᴛɪғ")


# Kelas BTN yang sudah diubah menggunakan ReplyKeyboardMarkup
class BTN:
    def ALREADY_UBOT():
        button = [
            [KeyboardButton("⦪ ʀᴇꜱᴛᴀʀᴛ ⦫")],
            [KeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫")]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

    def BACK_HOME():
        button = [
            [KeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫")]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

    def PAYMENT_OPTIONS():
        button = [
            [KeyboardButton("⦪ ʟᴀɴᴊᴜᴛᴋᴀɴ ⦫")],
            [KeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫")]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

    def CONTINUE_CREATE():
        button = [
            [KeyboardButton("⦪ ʟᴀɴᴊᴜᴛᴋᴀɴ ⦫")]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

    def BUY_UBOT_OPTIONS():
        button = [
            [KeyboardButton("✮ ʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ✮")],
            [KeyboardButton("卍 ᴋᴇᴍʙᴀʟɪ 卐")]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

    def PAYMENT_CONFIRMATION():
        button = [
            [KeyboardButton("-1"), KeyboardButton("+1")],
            [KeyboardButton("⦪ ᴋᴏɴꜰɪʀᴍᴀsɪ ⦫")],
            [KeyboardButton("⦪ ʙᴀᴛᴀʟᴋᴀɴ ⦫")]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

    def RESTART_BUTTON():
        button = [
            [KeyboardButton("ʀᴇꜱᴛᴀʀᴛ")]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

    def UBOT_MENU():
        button = [
            [KeyboardButton("⦪ ʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ ⦫")],
            [KeyboardButton("⦪ ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ ⦫")],
            [KeyboardButton("⟢"), KeyboardButton("⟣")]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

    def START(message):
        if not message.from_user.id == OWNER_ID:
            button = [
                [KeyboardButton("⦪ ʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ⦫")],
                [
                    KeyboardButton("⦪ ɢʀᴏᴜᴘ ᴘᴜʙʟɪᴄ ⳼"), 
                    KeyboardButton("⦪ ᴄʜᴀɴɴᴇʟ ⦫")
                ],
                [
                    KeyboardButton("⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⳼"),
                    KeyboardButton("⦪ ʜᴇʟᴘ ᴍᴇɴᴜ ⦫")
                ],
                [KeyboardButton("⦪ sᴜᴘᴘᴏʀᴛ ⦫")]
            ]
        else:
            button = [
                [KeyboardButton("⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⦫")],
                [
                    KeyboardButton("⦪ ɢɪᴛᴘᴜʟʟ ⦫"),
                    KeyboardButton("⦪ ʀᴇsᴛᴀʀᴛ ⦫")
                ],
                [KeyboardButton("⦪ ʟɪsᴛ ᴜsᴇʀʙᴏᴛ ⦫")]
            ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)