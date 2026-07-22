import json
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def send_telegram_application_notification(application):
    """
    Sends a formatted real-time notification to the Admins Telegram Group
    whenever a new application is submitted with inline buttons to mark status.
    """
    bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(settings, 'TELEGRAM_ADMIN_CHAT_ID', '')

    if not bot_token or not chat_id:
        logger.warning("Telegram Bot token or Admin Chat ID not configured in settings.py")
        return False

    message_text = (
        f"📥 <b>YANGI ARIZA KELDI! (#id{application.id})</b>\n\n"
        f"👤 <b>Ism va Familiya:</b> {application.full_name}\n"
        f"📞 <b>Telefon:</b> {application.phone}\n"
        f"✈️ <b>Telegram:</b> {application.telegram_username}\n"
        f"📅 <b>Vaqti:</b> {application.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        f"🟡 <b>Holati:</b> Yangi ariza\n\n"
        f"<i>Arizani koʻrib chiqish va holatini oʻzgartirish uchun quyidagi tugmalardan foydalaning:</i>"
    )

    # Inline action buttons for admins
    inline_keyboard = [
        [
            {'text': '✅ Bogʻlanildi', 'callback_data': f'app_contacted_{application.id}'},
            {'text': '❌ Rad etildi', 'callback_data': f'app_rejected_{application.id}'}
        ]
    ]

    # Add direct Telegram user chat link if available
    tg_user = application.telegram_username.replace('@', '').strip()
    if tg_user and tg_user != 'kiritilmagan':
        inline_keyboard.append([
            {'text': '💬 Telegramda yozish', 'url': f'https://t.me/{tg_user}'}
        ])

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'HTML',
        'reply_markup': json.dumps({'inline_keyboard': inline_keyboard})
    }

    try:
        response = requests.post(url, data=payload, timeout=5)
        if response.status_code == 200:
            logger.info(f"Telegram notification sent for application ID {application.id}")
            return True
        else:
            logger.error(f"Failed to send Telegram notification: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {e}")
        return False

