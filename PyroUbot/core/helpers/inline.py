from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from PyroUbot import *

def detect_url_links(text):
    link_pattern = (
        r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?"
    )
    link_found = re.findall(link_pattern, text)
    return link_found

def detect_button_and_text(text):
    button_matches = re.findall(r"\| ([^|]+) - ([^|]+) \|", text)
    text_matches = (
        re.search(r"(.*?) \|", text, re.DOTALL).group(1) if "|" in text else text
    )
    return button_matches, text_matches

def create_reply_keyboard(text, user_id=False, is_back=False):
    keyboard = []
    button_matches, text_matches = detect_button_and_text(text)

    for button_text, button_data in button_matches:
        # Untuk keyboard biasa, kita hanya bisa menampilkan text
        keyboard.append([KeyboardButton(button_text)])

    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return markup, text_matches

class BTN:
    def ALIVE(get_id):
        button = [
            [KeyboardButton("ᴛᴜᴛᴜᴘ")],
            [KeyboardButton("ʜᴇʟᴘ")]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

    def BOT_HELP(message):
        button = [
            [KeyboardButton("ʀᴇsᴛᴀʀᴛ")],
            [KeyboardButton("ꜱʏꜱᴛᴇᴍ")],
            [KeyboardButton("ᴜʙᴏᴛ")],
            [KeyboardButton("ᴜᴘᴅᴀᴛᴇ")]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)
        
    def ADD_EXP(user_id):
        buttons = []
        # Membuat keyboard dengan 4 baris, masing-masing 3 tombol
        for i in range(0, 12, 3):
            row = []
            for j in range(3):
                if i + j < 12:
                    row.append(KeyboardButton(f"{i+j+1} ʙᴜʟᴀɴ"))
            buttons.append(row)
        
        buttons.append([KeyboardButton("⦪ ᴅᴀᴘᴀᴛᴋᴀɴ ᴘʀᴏfɪʟ ⦫")])
        buttons.append([KeyboardButton("⦪ ᴛᴏʟᴀᴋ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ⦫")])
        
        return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

    def EXP_UBOT():
        button = [
            [KeyboardButton("beli userbot")]
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

    def PLUS_MINUS(query, user_id):
        button = [
            [
                KeyboardButton("-1"),
                KeyboardButton("+1")
            ],
            [KeyboardButton("⦪ ᴋᴏɴꜰɪʀᴍᴀsɪ ⦫")],
            [KeyboardButton("⦪ ʙᴀᴛᴀʟᴋᴀɴ ⦫")]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

    def UBOT(user_id, count):
        button = [
            [KeyboardButton("⦪ ʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ ⦫")],
            [KeyboardButton("⦪ ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ ⦫")],
            [
                KeyboardButton("⟢"),
                KeyboardButton("⟣")
            ]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

    def DEAK(user_id, count):
        button = [
            [
                KeyboardButton("⦪ ᴋᴇᴍʙᴀʟɪ ⦫"),
                KeyboardButton("⦪ sᴇᴛᴜᴊᴜɪ ⦫")
            ]
        ]
        return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

async def create_button(m):
    buttons = []
    msg = []
    
    if "-/" not in m.text.split(None, 1)[1]:
        for X in m.text.split(None, 1)[1].split():
            X_parts = X.split(":", 1)
            buttons.append([KeyboardButton(X_parts[0].replace("_", " "))])
            msg.append(X_parts[0])
        
        if m.reply_to_message:
            text = m.reply_to_message.text
        else:
            text = " ".join(msg)
    else:
        for X in m.text.split("-/", 1)[1].split():
            X_parts = X.split(":", 1)
            buttons.append([KeyboardButton(X_parts[0].replace("_", " "))])
        text = m.text.split("-/", 1)[0].split(None, 1)[1]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True), text

async def notes_create_button(text):
    buttons = []
    split_text = text.split("-/", 1)
    
    for X in split_text[1].split():
        split_X = X.split(":", 1)
        button_text = split_X[0].replace("_", " ")
        buttons.append([KeyboardButton(button_text)])
    
    text_button = split_text[0]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True), text_button