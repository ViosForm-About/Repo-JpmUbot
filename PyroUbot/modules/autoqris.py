import os
import asyncio
import aiohttp
import json
import logging
import math
from datetime import datetime, timedelta
from urllib.parse import urlencode
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageFont
import qrcode

# PyroUbot
from PyroUbot import *

__MODULE__ = "ǫʀɪs ᴘᴀʏᴍᴇɴᴛ"
__HELP__ = """
<b>⦿ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ǫʀɪs ᴘᴀʏᴍᴇɴᴛ ⦿</b>

<blockquote>⎆ ᴘᴇʀɪɴᴛᴀʜ:

ᚗ <code>{0}setapi</code> [ᴀᴘɪ_ᴋᴇʏ]
⊶ ᴍᴇɴɢᴀᴛᴜʀ ᴀᴘɪ ᴋᴇʏ ʀᴜᴍᴀʜᴏᴛᴘ

ᚗ <code>{0}qris</code> [ɴᴏᴍɪɴᴀʟ]
⊶ ᴍᴇᴍʙᴜᴀᴛ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ǫʀɪs

ᚗ <code>{0}cektransaksi</code> [ɪᴅ_ᴛʀᴀɴsᴀᴋsɪ]
⊶ ᴍᴇᴍᴇʀɪᴋsᴀ sᴛᴀᴛᴜs ᴛʀᴀɴsᴀᴋsɪ

ᚗ <code>{0}batalkan</code> [ɪᴅ_ᴛʀᴀɴsᴀᴋsɪ]
⊶ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴛʀᴀɴsᴀᴋsɪ

ᚗ <code>{0}saldo</code>
⊶ ᴍᴇɴɢᴇᴄᴇᴋ sᴀʟᴅᴏ ᴘʀᴏᴠɪᴅᴇʀ</blockquote>

<b>⦿ ᴄᴏɴᴛᴏʜ ᴘᴇɴɢɢᴜɴᴀᴀɴ:</b>
<blockquote>⎆ <code>{0}setapi api_key_anda</code>
⎆ <code>{0}qris 20000</code>
⎆ <code>{0}cektransaksi QRIS_123456</code></blockquote>
"""

# Konfigurasi
QRIS_FEE_PERCENTAGE = 0.7  # 0.7%
QRIS_FEE_FLAT = 150  # Rp 150
PAYMENT_TIMEOUT = 300  # 5 menit
STATUS_CHECK_INTERVAL = 10  # 10 detik

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("qris_payment.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("QRIS_Payment")

# Database sederhana
QRIS_DB = {}
USER_API_KEYS = {}
ACTIVE_DEPOSITS = {}
DEPOSIT_LOCKS = {}

class QRISProvider:
    def __init__(self):
        self.rumahotp_base_url = "https://api.rumahotp.com/api"
        self.atlantich2h_base_url = "https://api.atlantich2h.com/api"  # Ganti dengan URL sebenarnya
        
    async def enhanced_safe_api_call(self, api_call_func, operation_name, max_retries=3, priority='normal'):
        """Enhanced safe API call dengan retry mechanism"""
        for attempt in range(max_retries):
            try:
                result = await api_call_func()
                return result
            except asyncio.TimeoutError:
                logger.warning(f"Timeout pada {operation_name}, attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    return {"success": False, "message": "Timeout: Server tidak merespons"}
            except aiohttp.ClientError as e:
                logger.warning(f"Network error pada {operation_name}, attempt {attempt + 1}: {str(e)}")
                if attempt == max_retries - 1:
                    return {"success": False, "message": f"Network error: {str(e)}"}
            except Exception as e:
                logger.error(f"Unexpected error pada {operation_name}, attempt {attempt + 1}: {str(e)}")
                if attempt == max_retries - 1:
                    return {"success": False, "message": f"System error: {str(e)}"}
            
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return {"success": False, "message": "Max retries exceeded"}

    async def rumahotp_create_deposit(self, api_key: str, nominal: int, reff_id: str):
        """Membuat deposit menggunakan RumahOTP"""
        async def api_call():
            # Hitung biaya admin
            admin_fee = math.ceil(nominal * QRIS_FEE_PERCENTAGE / 100) + QRIS_FEE_FLAT
            total_amount = nominal + admin_fee

            headers = {
                'x-apikey': api_key,
                'Accept': 'application/json'
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.rumahotp_base_url}/v2/deposit/create?amount={total_amount}&payment_id=qris",
                    headers=headers,
                    timeout=30
                ) as response:
                    result = await response.json()
                    
                    if result and result.get('success'):
                        return {
                            "success": True,
                            "data": result.get('data', {}),
                            "adminFee": admin_fee,
                            "totalAmount": total_amount
                        }
                    else:
                        return {
                            "success": False,
                            "message": result.get('error', {}).get('message') or result.get('message') or "Gagal membuat deposit RumahOTP"
                        }

        return await self.enhanced_safe_api_call(api_call, 'CREATE_DEPOSIT_RUMAHOTP', 3, 'high')

    async def rumahotp_check_status(self, api_key: str, deposit_id: str):
        """Cek status deposit RumahOTP"""
        async def api_call():
            headers = {
                'x-apikey': api_key,
                'Accept': 'application/json'
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.rumahotp_base_url}/v2/deposit/get_status?deposit_id={deposit_id}",
                    headers=headers,
                    timeout=25
                ) as response:
                    result = await response.json()
                    
                    if result and result.get('success'):
                        return {
                            "success": True,
                            "data": result.get('data', {})
                        }
                    else:
                        return {
                            "success": False,
                            "message": result.get('error', {}).get('message') or result.get('message') or 'Unknown error'
                        }

        return await self.enhanced_safe_api_call(api_call, 'CHECK_DEPOSIT_STATUS_RUMAHOTP', 2, 'normal')

    async def rumahotp_cancel_deposit(self, api_key: str, deposit_id: str):
        """Batalkan deposit RumahOTP"""
        async def api_call():
            logger.info(f"🔄 Membatalkan deposit RumahOTP: {deposit_id}")
            headers = {
                'x-apikey': api_key,
                'Accept': 'application/json'
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.rumahotp_base_url}/v1/deposit/cancel?deposit_id={deposit_id}",
                    headers=headers,
                    timeout=25
                ) as response:
                    result = await response.json()
                    logger.info(f'📦 Response Cancel Deposit RumahOTP: {json.dumps(result, indent=2)}')

                    if result and result.get('success'):
                        return {
                            "success": True,
                            "data": result.get('data', {})
                        }
                    else:
                        return {
                            "success": False,
                            "message": result.get('error', {}).get('message') or result.get('message') or 'Gagal membatalkan deposit'
                        }

        return await self.enhanced_safe_api_call(api_call, 'CANCEL_DEPOSIT_RUMAHOTP', 2, 'high')

    async def rumahotp_get_balance(self, api_key: str):
        """Get balance RumahOTP"""
        async def api_call():
            headers = {
                'x-apikey': api_key,
                'Accept': 'application/json'
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.rumahotp_base_url}/v2/profile",
                    headers=headers,
                    timeout=30
                ) as response:
                    return await response.json()

        return await self.enhanced_safe_api_call(api_call, 'GET_BALANCE_RUMAHOTP', 3, 'normal')

    async def atlantich2h_create_deposit(self, api_key: str, nominal: int, reff_id: str):
        """Membuat deposit menggunakan Atlantic H2H"""
        async def api_call():
            # Hitung biaya admin
            admin_fee = math.ceil(nominal * QRIS_FEE_PERCENTAGE / 100) + QRIS_FEE_FLAT
            total_amount = nominal + admin_fee

            payload = {
                'api_key': api_key,
                'reff_id': reff_id,
                'nominal': int(total_amount),
                'type': 'ewallet',
                'metode': 'qrisfast'
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.atlantich2h_base_url}/deposit/create",
                    data=payload,
                    headers=headers,
                    timeout=30
                ) as response:
                    result = await response.json()

                    if not result.get('status'):
                        return {
                            "success": False,
                            "message": result.get('message') or "Gagal membuat pembayaran"
                        }

                    info = result.get('data', {})
                    
                    if not info.get('qr_string'):
                        return {
                            "success": False,
                            "message": "QR code tidak tersedia dari payment gateway"
                        }

                    return {
                        "success": True,
                        "data": info,
                        "adminFee": admin_fee,
                        "totalAmount": total_amount
                    }

        return await self.enhanced_safe_api_call(api_call, 'CREATE_DEPOSIT_ATLANTIC', 3, 'high')

    async def atlantich2h_check_status(self, api_key: str, trx_id: str):
        """Cek status deposit Atlantic H2H"""
        async def api_call():
            payload = {
                'api_key': api_key,
                'id': trx_id
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.atlantich2h_base_url}/deposit/status",
                    data=payload,
                    headers=headers,
                    timeout=25
                ) as response:
                    result = await response.json()
                    
                    if result and result.get('status') == True:
                        return {
                            "success": True,
                            "data": result.get('data', {})
                        }
                    else:
                        return {
                            "success": False,
                            "message": result.get('message') or 'Unknown error'
                        }

        return await self.enhanced_safe_api_call(api_call, 'CHECK_DEPOSIT_STATUS_ATLANTIC', 2, 'normal')

    async def atlantich2h_cancel_deposit(self, api_key: str, trx_id: str):
        """Batalkan deposit Atlantic H2H"""
        async def api_call():
            logger.info(f"🔄 Membatalkan deposit Atlantic: {trx_id}")
            payload = {
                'api_key': api_key,
                'id': trx_id
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.atlantich2h_base_url}/deposit/cancel",
                    data=payload,
                    headers=headers,
                    timeout=25
                ) as response:
                    result = await response.json()
                    logger.info(f'📦 Response Cancel Deposit Atlantic: {json.dumps(result, indent=2)}')

                    if result and result.get('status') == True:
                        return {
                            "success": True,
                            "data": result.get('data', {})
                        }
                    else:
                        return {
                            "success": False,
                            "message": result.get('message') or 'Gagal membatalkan deposit'
                        }

        return await self.enhanced_safe_api_call(api_call, 'CANCEL_DEPOSIT_ATLANTIC', 2, 'high')

    async def generate_qr_image(self, qr_content: str, amount: int, custom_id: str, provider: str):
        """Generate gambar QR code dengan informasi lengkap"""
        try:
            logger.info(f"Generating QR image untuk transaksi: {custom_id}")
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_content)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to PIL Image untuk menambahkan text
            img = img.convert('RGB')
            draw = ImageDraw.Draw(img)
            
            # Tambahkan informasi
            try:
                font_paths = [
                    "arial.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                    "/System/Library/Fonts/Arial.ttf"
                ]
                
                font_small = None
                for font_path in font_paths:
                    try:
                        font_small = ImageFont.truetype(font_path, 14)
                        break
                    except:
                        continue
                
                if font_small is None:
                    font_small = ImageFont.load_default()
                    
            except Exception as font_error:
                logger.warning(f"Font loading failed: {font_error}, using default font")
                font_small = ImageFont.load_default()
            
            # Tambahkan text informasi
            admin_fee = math.ceil(amount * QRIS_FEE_PERCENTAGE / 100) + QRIS_FEE_FLAT
            total_amount = amount + admin_fee
            
            info_text = [
                "QRIS PAYMENT",
                f"Provider: {provider}",
                f"Amount: Rp {amount:,}",
                f"Admin Fee: Rp {admin_fee:,}",
                f"Total: Rp {total_amount:,}",
                f"ID: {custom_id}",
                f"Time: {datetime.now().strftime('%H:%M:%S')}",
                "Status: PENDING"
            ]
            
            # Calculate image dimensions for text
            img_width, img_height = img.size
            y_position = img_height + 10
            
            for text in info_text:
                try:
                    bbox = draw.textbbox((0, 0), text, font=font_small)
                    text_width = bbox[2] - bbox[0]
                    x = (img_width - text_width) / 2
                    draw.text((x, y_position), text, font=font_small, fill='black')
                    y_position += 20
                except Exception as text_error:
                    logger.warning(f"Error drawing text '{text}': {text_error}")
                    continue
            
            logger.info("QR image generated successfully")
            return img
            
        except Exception as e:
            logger.error(f"Error generating QR image: {str(e)}")
            raise e


qris_provider = QRISProvider()


def format_number(number):
    """Format number dengan separator"""
    return f"{number:,}".replace(",", ".")


def get_indonesian_time():
    """Dapatkan waktu Indonesia"""
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


def log_user_activity(user_id: int, action: str, details: str = ""):
    """Log aktivitas user"""
    logger.info(f"USER_ACTIVITY | User: {user_id} | Action: {action} | Details: {details}")


async def monitor_deposit_status(client: Client, deposit_data: dict):
    """Background task untuk memonitor status deposit"""
    trx_id = deposit_data['trx_id']
    user_id = deposit_data['user_id']
    chat_id = deposit_data['chat_id']
    provider = deposit_data['provider']
    api_key = deposit_data['api_key']
    nominal = deposit_data['nominal']
    admin_fee = deposit_data['admin_fee']
    total_amount = deposit_data['total_amount']
    reff_id = deposit_data['reff_id']
    
    logger.info(f"Starting background monitoring untuk deposit: {trx_id}")
    
    attempts = 0
    max_attempts = 30  # 30 x 10 detik = 5 menit
    
    while attempts < max_attempts:
        attempts += 1
        
        # Cek timeout
        if datetime.now().timestamp() - deposit_data['start_time'] > PAYMENT_TIMEOUT:
            logger.info(f"Deposit {trx_id} expired")
            await handle_expired_deposit(client, deposit_data)
            break
        
        # Cek status deposit
        try:
            if provider == 'rumahotp':
                status_result = await qris_provider.rumahotp_check_status(api_key, deposit_data['deposit_id'])
            else:
                status_result = await qris_provider.atlantich2h_check_status(api_key, trx_id)
            
            if status_result and status_result['success']:
                status_data = status_result['data']
                status = status_data.get('status', '').lower()
                
                if status in ['success', 'paid', 'completed']:
                    logger.info(f"Deposit {trx_id} completed successfully")
                    await handle_successful_deposit(client, deposit_data, status_data)
                    break
                elif status in ['cancel', 'expired', 'failed']:
                    logger.info(f"Deposit {trx_id} failed with status: {status}")
                    await handle_failed_deposit(client, deposit_data, status)
                    break
            
        except Exception as e:
            logger.error(f"Error checking deposit status {trx_id}: {str(e)}")
        
        await asyncio.sleep(STATUS_CHECK_INTERVAL)
    
    # Cleanup
    if trx_id in ACTIVE_DEPOSITS:
        del ACTIVE_DEPOSITS[trx_id]
    if trx_id in DEPOSIT_LOCKS:
        del DEPOSIT_LOCKS[trx_id]


async def handle_successful_deposit(client: Client, deposit_data: dict, status_data: dict):
    """Handle deposit yang berhasil"""
    try:
        trx_id = deposit_data['trx_id']
        user_id = deposit_data['user_id']
        chat_id = deposit_data['chat_id']
        
        # Kirim notifikasi sukses
        success_message = (
            f"✅ **DEPOSIT BERHASIL!**\n\n"
            f"💵 **Nominal:** Rp {format_number(deposit_data['nominal'])}\n"
            f"📦 **Biaya Admin:** Rp {format_number(deposit_data['admin_fee'])}\n"
            f"💠 **Total Bayar:** Rp {format_number(deposit_data['total_amount'])}\n"
            f"🆔 **Ref ID:** {deposit_data['reff_id']}\n"
            f"🕒 **Waktu:** {get_indonesian_time()}\n\n"
            f"🎉 **Terima kasih! Pembayaran telah berhasil.**"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💰 Cek Saldo", callback_data="check_balance")],
            [InlineKeyboardButton("🔙 Menu Utama", callback_data="main_menu")]
        ])
        
        await client.send_message(
            chat_id,
            success_message,
            reply_markup=keyboard
        )
        
        logger.info(f"Success notification sent for deposit: {trx_id}")
        
    except Exception as e:
        logger.error(f"Error handling successful deposit: {str(e)}")


async def handle_failed_deposit(client: Client, deposit_data: dict, status: str):
    """Handle deposit yang gagal"""
    try:
        trx_id = deposit_data['trx_id']
        chat_id = deposit_data['chat_id']
        
        failed_message = (
            f"❌ **DEPOSIT GAGAL**\n\n"
            f"💵 **Nominal:** Rp {format_number(deposit_data['nominal'])}\n"
            f"📦 **Biaya Admin:** Rp {format_number(deposit_data['admin_fee'])}\n"
            f"💠 **Total Bayar:** Rp {format_number(deposit_data['total_amount'])}\n"
            f"📊 **Status:** {status.upper()}\n"
            f"🆔 **Ref ID:** {deposit_data['reff_id']}\n\n"
            f"Deposit telah dibatalkan atau gagal.\n"
            f"Silakan buat deposit baru jika masih ingin melanjutkan."
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Deposit Lagi", callback_data="deposit_menu")],
            [InlineKeyboardButton("🔙 Menu Utama", callback_data="main_menu")]
        ])
        
        await client.send_message(
            chat_id,
            failed_message,
            reply_markup=keyboard
        )
        
        logger.info(f"Failed notification sent for deposit: {trx_id}")
        
    except Exception as e:
        logger.error(f"Error handling failed deposit: {str(e)}")


async def handle_expired_deposit(client: Client, deposit_data: dict):
    """Handle deposit yang expired"""
    try:
        trx_id = deposit_data['trx_id']
        chat_id = deposit_data['chat_id']
        
        expired_message = (
            f"⏰ **WAKTU PEMBAYARAN HABIS**\n\n"
            f"💵 **Nominal:** Rp {format_number(deposit_data['nominal'])}\n"
            f"📦 **Biaya Admin:** Rp {format_number(deposit_data['admin_fee'])}\n"
            f"💠 **Total Bayar:** Rp {format_number(deposit_data['total_amount'])}\n"
            f"🆔 **Ref ID:** {deposit_data['reff_id']}\n\n"
            f"Deposit telah kadaluarsa.\n"
            f"QR Code tidak lagi valid.\n\n"
            f"Silakan buat deposit baru jika masih ingin melanjutkan."
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Deposit Lagi", callback_data="deposit_menu")],
            [InlineKeyboardButton("🔙 Menu Utama", callback_data="main_menu")]
        ])
        
        await client.send_message(
            chat_id,
            expired_message,
            reply_markup=keyboard
        )
        
        logger.info(f"Expired notification sent for deposit: {trx_id}")
        
    except Exception as e:
        logger.error(f"Error handling expired deposit: {str(e)}")


@PY.BOT("setapi")
@PY.UBOT("setapi")
async def set_api_key(client: Client, message: Message):
    """Set API key untuk provider"""
    user_id = message.from_user.id
    log_user_activity(user_id, "SET_API", "Mengatur API key")
    
    if len(message.command) < 2:
        return await message.reply(
            "❌ **Format salah!**\n\n"
            "**Gunakan:** `.setapi [api_key_anda]`\n\n"
            "**Contoh:** `.setapi your_api_key_here`\n\n"
            "**Catatan:** Saat ini hanya mendukung RumahOTP provider."
        )
    
    api_key = message.command[1]
    
    # Validasi API key format
    if len(api_key) < 10:
        return await message.reply("❌ **Format API key tidak valid!**")
    
    # Simpan API key user
    USER_API_KEYS[user_id] = api_key
    logger.info(f"User {user_id} berhasil menyimpan API key")
    
    await message.reply(
        "✅ **API Key berhasil disimpan!**\n\n"
        "Sekarang Anda bisa menggunakan:\n"
        "• `.qris [nominal]` - Buat QRIS payment\n"
        "• `.cektransaksi [id]` - Cek status transaksi\n"
        "• `.batalkan [id]` - Batalkan transaksi\n"
        "• `.saldo` - Cek saldo provider\n\n"
        "**Contoh:** `.qris 20000`"
    )


@PY.BOT("qris")
@PY.UBOT("qris")
async def create_qris_payment(client: Client, message: Message):
    """Buat QRIS payment"""
    user_id = message.from_user.id
    
    # Cek API key
    if user_id not in USER_API_KEYS:
        return await message.reply(
            "❌ **API Key belum diset!**\n"
            "Gunakan `.setapi [api_key]` terlebih dahulu.\n\n"
            "Dapatkan API key dari provider yang didukung."
        )
    
    # Cek parameter
    if len(message.command) < 2:
        return await message.reply(
            "❌ **Format salah!**\n\n"
            "**Gunakan:** `.qris [nominal]`\n"
            "**Contoh:** `.qris 20000`\n\n"
            "**Ketentuan:**\n"
            "• Minimum: Rp 10,000\n"
            "• Maksimum: Rp 1,000,000"
        )
    
    try:
        amount = int(message.command[1])
        if amount < 10000:
            return await message.reply("❌ **Minimum nominal Rp 10.000**")
        if amount > 1000000:
            return await message.reply("❌ **Maximum nominal Rp 1.000.000**")
            
    except ValueError:
        return await message.reply("❌ **Nominal harus angka!**")
    
    api_key = USER_API_KEYS[user_id]
    log_user_activity(user_id, "CREATE_QRIS", f"Amount: {amount}")
    
    msg = await message.reply("🔄 **Membuat QRIS payment...**")
    
    try:
        # Buat custom ID
        custom_id = f"QRIS_{user_id}_{int(datetime.now().timestamp())}"
        
        # Pilih provider (saat ini hanya RumahOTP)
        provider = 'rumahotp'
        
        # Create deposit
        if provider == 'rumahotp':
            result = await qris_provider.rumahotp_create_deposit(api_key, amount, custom_id)
        else:
            result = await qris_provider.atlantich2h_create_deposit(api_key, amount, custom_id)
        
        if not result.get('success'):
            error_msg = result.get('message', 'Unknown error')
            logger.error(f"QRIS creation failed for user {user_id}: {error_msg}")
            return await msg.edit(f"❌ **Error:** {error_msg}")
        
        # Simpan data transaksi
        deposit_data = result.get('data', {})
        admin_fee = result.get('adminFee', 0)
        total_amount = result.get('totalAmount', amount)
        
        trx_data = {
            'user_id': user_id,
            'chat_id': message.chat.id,
            'amount': amount,
            'admin_fee': admin_fee,
            'total_amount': total_amount,
            'reff_id': custom_id,
            'provider': provider,
            'api_key': api_key,
            'deposit_id': deposit_data.get('deposit_id', custom_id),
            'trx_id': custom_id,
            'qr_content': deposit_data.get('qr_string', deposit_data.get('qr_content', '')),
            'start_time': datetime.now().timestamp(),
            'status': 'PENDING'
        }
        
        QRIS_DB[custom_id] = trx_data
        ACTIVE_DEPOSITS[custom_id] = trx_data
        
        logger.info(f"QRIS created successfully for user {user_id}, ID: {custom_id}")
        
        # Generate QR image
        qr_image = await qris_provider.generate_qr_image(
            trx_data['qr_content'],
            amount,
            custom_id,
            provider.upper()
        )
        
        # Save image
        filename = f"qris_{custom_id}.jpg"
        qr_image.save(filename)
        
        # Kirim gambar QR
        caption = (
            f"💳 **QRIS PAYMENT - {provider.upper()}**\n\n"
            f"💰 **Nominal:** Rp {format_number(amount)}\n"
            f"📦 **Biaya Admin:** Rp {format_number(admin_fee)}\n"
            f"💠 **Total Bayar:** Rp {format_number(total_amount)}\n"
            f"🆔 **ID Transaksi:** `{custom_id}`\n"
            f"⏰ **Batas Waktu:** 5 Menit\n"
            f"📊 **Status:** 🟡 PENDING\n\n"
            f"**Cara Bayar:**\n"
            f"1. Buka aplikasi mobile banking/e-wallet\n"
            f"2. Scan QR code di atas\n"
            f"3. Bayar sesuai total amount\n"
            f"4. Transaksi akan otomatis terverifikasi\n\n"
            f"**Periksa status:** `.cektransaksi {custom_id}`"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Cek Status", callback_data=f"cek_{custom_id}")],
            [InlineKeyboardButton("❌ Batalkan", callback_data=f"cancel_{custom_id}")]
        ])
        
        await message.reply_photo(
            photo=filename,
            caption=caption,
            reply_markup=keyboard
        )
        await msg.delete()
        
        # Start background monitoring
        asyncio.create_task(monitor_deposit_status(client, trx_data))
        
        # Cleanup
        os.remove(filename)
        
    except Exception as e:
        logger.error(f"Unexpected error in create_qris_payment for user {user_id}: {str(e)}")
        await msg.edit(f"❌ **Error:** {str(e)}")


@PY.BOT("cektransaksi")
@PY.UBOT("cektransaksi")
async def check_transaction(client: Client, message: Message):
    """Cek status transaksi"""
    user_id = message.from_user.id
    
    if len(message.command) < 2:
        return await message.reply(
            "❌ **Format salah!**\n\n"
            "**Gunakan:** `.cektransaksi [id_transaksi]`\n"
            "**Contoh:** `.cektransaksi QRIS_123456789`"
        )
    
    custom_id = message.command[1]
    log_user_activity(user_id, "CHECK_TRANSACTION", f"ID: {custom_id}")
    
    msg = await message.reply("🔄 **Memeriksa status transaksi...**")
    
    try:
        # Cek di database lokal
        if custom_id not in QRIS_DB:
            return await msg.edit("❌ **ID transaksi tidak ditemukan!**")
        
        transaction = QRIS_DB[custom_id]
        
        # Cek authorization
        if transaction['user_id'] != user_id:
            return await msg.edit("❌ **Anda tidak memiliki akses ke transaksi ini!**")
        
        # Check status dari API
        api_key = USER_API_KEYS[user_id]
        
        if transaction['provider'] == 'rumahotp':
            status_result = await qris_provider.rumahotp_check_status(api_key, transaction['deposit_id'])
        else:
            status_result = await qris_provider.atlantich2h_check_status(api_key, custom_id)
        
        if status_result and status_result['success']:
            status_data = status_result['data']
            status = status_data.get('status', 'PENDING').upper()
            
            status_emoji = {
                'PENDING': '🟡',
                'SUCCESS': '🟢', 
                'PAID': '🟢',
                'COMPLETED': '🟢',
                'FAILED': '🔴',
                'CANCEL': '🔴',
                'EXPIRED': '⚫'
            }
            
            emoji = status_emoji.get(status, '🟡')
            
            response = (
                f"📊 **STATUS TRANSAKSI**\n\n"
                f"🆔 **ID:** `{custom_id}`\n"
                f"💰 **Nominal:** Rp {format_number(transaction['amount'])}\n"
                f"📦 **Biaya Admin:** Rp {format_number(transaction['admin_fee'])}\n"
                f"💠 **Total:** Rp {format_number(transaction['total_amount'])}\n"
                f"📅 **Dibuat:** {get_indonesian_time()}\n"
                f"📊 **Status:** {emoji} {status}\n\n"
            )
            
            if status in ['SUCCESS', 'PAID', 'COMPLETED']:
                response += "✅ **Pembayaran berhasil!**"
            elif status == 'PENDING':
                response += "⏳ **Menunggu pembayaran...**"
            elif status in ['FAILED', 'CANCEL']:
                response += "❌ **Pembayaran gagal!**"
            elif status == 'EXPIRED':
                response += "⏰ **Waktu pembayaran habis!**"
                
            logger.info(f"Transaction {custom_id} status: {status}")
            await msg.edit(response)
        else:
            error_msg = status_result.get('message', 'Unknown error') if status_result else 'Tidak dapat menghubungi provider'
            logger.error(f"Failed to check transaction {custom_id}: {error_msg}")
            await msg.edit(f"❌ **Error:** {error_msg}")
            
    except Exception as e:
        logger.error(f"Unexpected error in check_transaction for user {user_id}: {str(e)}")
        await msg.edit(f"❌ **Error:** {str(e)}")


@PY.BOT("batalkan")
@PY.UBOT("batalkan")
async def cancel_transaction(client: Client, message: Message):
    """Batalkan transaksi"""
    user_id = message.from_user.id
    
    if len(message.command) < 2:
        return await message.reply(
            "❌ **Format salah!**\n\n"
            "**Gunakan:** `.batalkan [id_transaksi]`\n"
            "**Contoh:** `.batalkan QRIS_123456789`"
        )
    
    custom_id = message.command[1]
    log_user_activity(user_id, "CANCEL_TRANSACTION", f"ID: {custom_id}")
    
    msg = await message.reply("🔄 **Membatalkan transaksi...**")
    
    try:
        # Cek di database lokal
        if custom_id not in QRIS_DB:
            return await msg.edit("❌ **ID transaksi tidak ditemukan!**")
        
        transaction = QRIS_DB[custom_id]
        
        # Cek authorization
        if transaction['user_id'] != user_id:
            return await msg.edit("❌ **Anda tidak memiliki akses ke transaksi ini!**")
        
        # Batalkan transaksi
        api_key = USER_API_KEYS[user_id]
        
        if transaction['provider'] == 'rumahotp':
            cancel_result = await qris_provider.rumahotp_cancel_deposit(api_key, transaction['deposit_id'])
        else:
            cancel_result = await qris_provider.atlantich2h_cancel_deposit(api_key, custom_id)
        
        if cancel_result and cancel_result['success']:
            # Hapus dari active deposits
            if custom_id in ACTIVE_DEPOSITS:
                del ACTIVE_DEPOSITS[custom_id]
            
            await msg.edit("✅ **Transaksi berhasil dibatalkan!**")
            logger.info(f"Transaction {custom_id} cancelled successfully")
        else:
            error_msg = cancel_result.get('message', 'Unknown error') if cancel_result else 'Tidak dapat menghubungi provider'
            await msg.edit(f"❌ **Error:** {error_msg}")
            
    except Exception as e:
        logger.error(f"Unexpected error in cancel_transaction for user {user_id}: {str(e)}")
        await msg.edit(f"❌ **Error:** {str(e)}")


@PY.BOT("saldo")
@PY.UBOT("saldo")
async def check_balance(client: Client, message: Message):
    """Cek saldo provider"""
    user_id = message.from_user.id
    
    # Cek API key
    if user_id not in USER_API_KEYS:
        return await message.reply(
            "❌ **API Key belum diset!**\n"
            "Gunakan `.setapi [api_key]` terlebih dahulu."
        )
    
    api_key = USER_API_KEYS[user_id]
    log_user_activity(user_id, "CHECK_BALANCE")
    
    msg = await message.reply("🔄 **Mengecek saldo...**")
    
    try:
        # Saat ini hanya cek saldo RumahOTP
        balance_result = await qris_provider.rumahotp_get_balance(api_key)
        
        if balance_result and balance_result.get('success'):
            data = balance_result.get('data', {})
            balance = data.get('balance', 0)
            username = data.get('username', 'Unknown')
            
            response = (
                f"💰 **SALDO PROVIDER**\n\n"
                f"👤 **Username:** {username}\n"
                f"💳 **Saldo:** Rp {format_number(balance)}\n"
                f"🏢 **Provider:** RumahOTP\n"
                f"🕒 **Update:** {get_indonesian_time()}"
            )
            
            await msg.edit(response)
        else:
            error_msg = balance_result.get('message', 'Unknown error') if balance_result else 'Tidak dapat menghubungi provider'
            await msg.edit(f"❌ **Error:** {error_msg}")
            
    except Exception as e:
        logger.error(f"Unexpected error in check_balance for user {user_id}: {str(e)}")
        await msg.edit(f"❌ **Error:** {str(e)}")


@PY.CALLBACK("cek_")
async def callback_check_status(client, callback_query):
    """Callback untuk cek status"""
    custom_id = callback_query.data.split("_", 1)[1]
    user_id = callback_query.from_user.id
    
    if custom_id not in QRIS_DB:
        await callback_query.answer("❌ Transaksi tidak ditemukan!", show_alert=True)
        return
    
    transaction = QRIS_DB[custom_id]
    
    if transaction['user_id'] != user_id:
        await callback_query.answer("❌ Anda tidak memiliki akses!", show_alert=True)
        return
    
    # Check status
    api_key = USER_API_KEYS.get(user_id)
    if api_key:
        try:
            if transaction['provider'] == 'rumahotp':
                status_result = await qris_provider.rumahotp_check_status(api_key, transaction['deposit_id'])
            else:
                status_result = await qris_provider.atlantich2h_check_status(api_key, custom_id)
            
            if status_result and status_result['success']:
                status_data = status_result['data']
                status = status_data.get('status', 'PENDING').upper()
                
                status_text = {
                    'PENDING': '🟡 PENDING',
                    'SUCCESS': '🟢 SUCCESS', 
                    'PAID': '🟢 PAID',
                    'COMPLETED': '🟢 COMPLETED',
                    'FAILED': '🔴 FAILED',
                    'CANCEL': '🔴 CANCELLED',
                    'EXPIRED': '⚫ EXPIRED'
                }
                
                await callback_query.answer(f"Status: {status_text.get(status, 'PENDING')}", show_alert=True)
            else:
                await callback_query.answer("❌ Gagal memeriksa status", show_alert=True)
        except Exception as e:
            await callback_query.answer("❌ Error memeriksa status", show_alert=True)
    else:
        await callback_query.answer("❌ API Key tidak ditemukan", show_alert=True)


@PY.CALLBACK("cancel_")
async def callback_cancel_transaction(client, callback_query):
    """Callback untuk batalkan transaksi"""
    custom_id = callback_query.data.split("_", 1)[1]
    user_id = callback_query.from_user.id
    
    if custom_id not in QRIS_DB:
        await callback_query.answer("❌ Transaksi tidak ditemukan!", show_alert=True)
        return
    
    transaction = QRIS_DB[custom_id]
    
    if transaction['user_id'] != user_id:
        await callback_query.answer("❌ Anda tidak memiliki akses!", show_alert=True)
        return
    
    # Batalkan transaksi
    api_key = USER_API_KEYS.get(user_id)
    if api_key:
        try:
            if transaction['provider'] == 'rumahotp':
                cancel_result = await qris_provider.rumahotp_cancel_deposit(api_key, transaction['deposit_id'])
            else:
                cancel_result = await qris_provider.atlantich2h_cancel_deposit(api_key, custom_id)
            
            if cancel_result and cancel_result['success']:
                # Hapus dari active deposits
                if custom_id in ACTIVE_DEPOSITS:
                    del ACTIVE_DEPOSITS[custom_id]
                
                await callback_query.answer("✅ Transaksi berhasil dibatalkan!", show_alert=True)
                await callback_query.message.delete()
            else:
                await callback_query.answer("❌ Gagal membatalkan transaksi", show_alert=True)
        except Exception as e:
            await callback_query.answer("❌ Error membatalkan transaksi", show_alert=True)
    else:
        await callback_query.answer("❌ API Key tidak ditemukan", show_alert=True)


# Command untuk testing
@PY.BOT("test_qris")
async def test_qris_system(client, message):
    """Test sistem QRIS"""
    test_results = []
    
    # Test 1: Cek module loaded
    try:
        test_results.append("✅ Module QRIS terload")
    except:
        test_results.append("❌ Module QRIS tidak terload")
    
    # Test 2: Cek dependencies
    try:
        import qrcode
        from PIL import Image
        test_results.append("✅ Dependencies terinstall")
    except ImportError as e:
        test_results.append(f"❌ Dependencies error: {str(e)}")
    
    # Test 3: Cek API key storage
    user_id = message.from_user.id
    if user_id in USER_API_KEYS:
        test_results.append(f"✅ API Key tersimpan: {USER_API_KEYS[user_id][:10]}...")
    else:
        test_results.append("❌ API Key belum diset")
    
    # Test 4: Cek active deposits
    active_count = len(ACTIVE_DEPOSITS)
    test_results.append(f"📊 Active deposits: {active_count}")
    
    response = "🧪 **TEST SISTEM QRIS**\n\n" + "\n".join(test_results)
    await message.reply(response)


# Install dependencies yang diperlukan
def install_dependencies():
    """Install required dependencies"""
    try:
        import qrcode
        from PIL import Image
        logger.info("✅ Semua dependencies sudah terinstall")
    except ImportError:
        logger.warning("⚠️ Beberapa dependencies belum terinstall")
        logger.info("Jalankan: pip install qrcode[pil] pillow aiohttp")

# Jalakan install check saat module di-load
install_dependencies()