from pykeyboard import InlineKeyboard
from pyrogram.errors import MessageNotModified
from pyrogram.types import *
from pyromod.helpers import ikb
from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InputTextMessageContent)
import re

from PyroUbot import *


def detect_url_links(text):
    """Detect URLs in text"""
    link_pattern = (
        r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?"
    )
    return re.findall(link_pattern, text)


def detect_button_and_text(text):
    """Detect button pattern and text"""
    button_matches = re.findall(r"\| ([^|]+) - ([^|]+) \|", text)
    text_matches = re.search(r"(.*?) \|", text, re.DOTALL).group(1) if "|" in text else text
    return button_matches, text_matches


def create_inline_keyboard(text, user_id=False, is_back=False):
    """Create inline keyboard from text pattern"""
    keyboard = []
    button_matches, text_matches = detect_button_and_text(text)

    prev_button_data = None
    for button_text, button_data in button_matches:
        data = (
            button_data.split("#")[0]
            if detect_url_links(button_data.split("#")[0])
            else f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]} {button_data.split('#')[0]}"
        )
        cb_data = data if user_id else button_data.split("#")[0]
        
        if "#" in button_data:
            if prev_button_data:
                if detect_url_links(cb_data):
                    keyboard[-1].append(InlineKeyboardButton(button_text, url=cb_data))
                else:
                    keyboard[-1].append(InlineKeyboardButton(button_text, callback_data=cb_data))
            else:
                if detect_url_links(cb_data):
                    button_row = [InlineKeyboardButton(button_text, url=cb_data)]
                else:
                    button_row = [InlineKeyboardButton(button_text, callback_data=cb_data)]
                keyboard.append(button_row)
        else:
            if button_data.startswith("http"):
                button_row = [InlineKeyboardButton(button_text, url=cb_data)]
            else:
                button_row = [InlineKeyboardButton(button_text, callback_data=cb_data)]
            keyboard.append(button_row)

        prev_button_data = button_data

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    if user_id and is_back:
        markup.inline_keyboard.append([
            InlineKeyboardButton(
                "ᴋᴇᴍʙᴀʟɪ",
                f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]}",
            )
        ])

    return markup, text_matches


class BTN:
    """Class untuk semua button keyboard"""
    
    @staticmethod
    def ALIVE(get_id):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="ᴛᴜᴛᴜᴘ",
                    callback_data=f"alv_cls {int(get_id[1])} {int(get_id[2])}",
                )
            ],
            [
                InlineKeyboardButton(text="ʜᴇʟᴘ", callback_data="help_back")
            ]
        ])

    @staticmethod
    def BOT_HELP():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("ʀᴇsᴛᴀʀᴛ", callback_data="reboot")],
            [InlineKeyboardButton("ꜱʏꜱᴛᴇᴍ", callback_data="system")],
            [InlineKeyboardButton("ᴜʙᴏᴛ", callback_data="ubot")],
            [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", callback_data="update")],
        ])
        
    @staticmethod
    def ADD_EXP(user_id):
        keyboard = InlineKeyboard(row_width=3)
        btns = []
        for X in range(1, 13):
            btns.append(
                InlineKeyboardButton(
                    f"{X} ʙᴜʟᴀɴ",
                    callback_data=f"success {user_id} {X}",
                )
            )
        keyboard.add(*btns)
        keyboard.row(
            InlineKeyboardButton("⦪ ᴅᴀᴘᴀᴛᴋᴀɴ ᴘʀᴏfɪʟ ⦫", callback_data=f"profil {user_id}")
        )
        keyboard.row(
            InlineKeyboardButton("⦪ ᴛᴏʟᴀᴋ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ⦫", callback_data=f"failed {user_id}")
        )
        return keyboard

    @staticmethod
    def EXP_UBOT():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("ʙᴇʟɪ ᴜsᴇʀʙᴏᴛ", callback_data="bahan")]
        ])

    @staticmethod
    def START(message):
        if message.from_user.id == OWNER_ID:
            return InlineKeyboardMarkup([
                [InlineKeyboardButton("⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⦫", callback_data="bahan")],
                [
                    InlineKeyboardButton("⦪ ɢɪᴛᴘᴜʟʟ ⦫", callback_data="cb_gitpull"),
                    InlineKeyboardButton("⦪ ʀᴇsᴛᴀʀᴛ ⦫", callback_data="cb_restart")
                ],
                [InlineKeyboardButton("⦪ ʟɪsᴛ ᴜsᴇʀʙᴏᴛ ⦫", callback_data="cek_ubot")]
            ])
        else:
            return InlineKeyboardMarkup([
                [InlineKeyboardButton("⦪ ʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ⦫", callback_data="bahan")],
                [
                    InlineKeyboardButton("⦪ ɢʀᴏᴜᴘ ᴘᴜʙʟɪᴄ ⳼", url="t.me/publicvios"), 
                    InlineKeyboardButton("⦪ ᴄʜᴀɴɴᴇʟ ⦫", url="t.me/informasiubot")
                ],
                [
                    InlineKeyboardButton("⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⳼", callback_data="buat_ubot"),
                    InlineKeyboardButton("⦪ ʜᴇʟᴘ ᴍᴇɴᴜ ⦫", callback_data="help_back")
                ],
                [InlineKeyboardButton("⦪ sᴜᴘᴘᴏʀᴛ ⦫", callback_data="support")]
            ])

    @staticmethod
    def PLUS_MINUS(query, user_id):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("-1", callback_data=f"kurang {query}"),
                InlineKeyboardButton("+1", callback_data=f"tambah {query}"),
            ],
            [InlineKeyboardButton("⦪ ᴋᴏɴꜰɪʀᴍᴀsɪ ⦫", callback_data="confirm")],
            [InlineKeyboardButton("⦪ ʙᴀᴛᴀʟᴋᴀɴ ⦫", callback_data=f"home {user_id}")],
        ])

    @staticmethod
    def UBOT(user_id, count):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "⦪ ʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ ⦫",
                    callback_data=f"del_ubot {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "⦪ ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ ⦫",
                    callback_data=f"cek_masa_aktif {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton("⟢", callback_data=f"p_ub {int(count)}"),
                InlineKeyboardButton("⟣", callback_data=f"n_ub {int(count)}"),
            ],
        ])

    @staticmethod
    def DEAK(count):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"p_ub {int(count)}"),
                InlineKeyboardButton("⦪ sᴇᴛᴜᴊᴜɪ ⦫", callback_data=f"deak_akun {int(count)}"),
            ],
        ])

    @staticmethod
    def PAYMENT():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ ᴋᴏɴꜰɪʀᴍᴀsɪ", callback_data="konfirmasi_bayar")]
        ])

    @staticmethod
    def BATAL():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ ʙᴀᴛᴀʟ", callback_data="batal")]
        ])

    @staticmethod
    def NAV_USERBOT(count, total_ubot):
        keyboard = []
        nav_buttons = []
        
        if count > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"prev_{count-1}"))
        
        nav_buttons.append(InlineKeyboardButton(f"{count + 1}/{total_ubot}", callback_data="count"))
        
        if count < total_ubot - 1:
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"next_{count+1}"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        keyboard.append([InlineKeyboardButton("🗑️ ʜᴀᴘᴜs", callback_data=f"hapus_{count}")])
        
        return InlineKeyboardMarkup(keyboard)


async def create_button(m):
    """Create button from text pattern"""
    buttons = InlineKeyboard(row_width=1)
    keyboard = []
    msg = []
    
    if "-/" not in m.text.split(None, 1)[1]:
        for X in m.text.split(None, 1)[1].split():
            X_parts = X.split(":", 1)
            keyboard.append(
                InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1])
            )
            msg.append(X_parts[0])
        buttons.add(*keyboard)
        text = m.reply_to_message.text if m.reply_to_message else " ".join(msg)
    else:
        for X in m.text.split("-/", 1)[1].split():
            X_parts = X.split(":", 1)
            keyboard.append(
                InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1])
            )
        buttons.add(*keyboard)
        text = m.text.split("-/", 1)[0].split(None, 1)[1]

    return buttons, text


async def notes_create_button(text):
    """Create button for notes"""
    buttons = InlineKeyboard(row_width=2)
    keyboard = []
    split_text = text.split("-/", 1)
    
    for X in split_text[1].split():
        split_X = X.split(":", 1)
        button_text = split_X[0].replace("_", " ")
        button_url = split_X[1]
        keyboard.append(InlineKeyboardButton(button_text, url=button_url))
    
    buttons.add(*keyboard)
    return buttons, split_text[0]
