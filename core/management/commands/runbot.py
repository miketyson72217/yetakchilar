import json
import time
import requests
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Application

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Run Telegram bot long polling for @yetakchilar_bot with inline button handlers"

    def handle(self, *args, **options):
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        if not bot_token:
            self.stderr.write(self.style.ERROR("TELEGRAM_BOT_TOKEN topilmadi! .env yoki settings.py ni tekshiring."))
            return

        api_url = f"https://api.telegram.org/bot{bot_token}"
        self.stdout.write(self.style.SUCCESS(f"🤖 Bot ishga tushdi! Token: {bot_token[:10]}..."))

        offset = None

        while True:
            try:
                params = {'timeout': 20, 'offset': offset}
                resp = requests.get(f"{api_url}/getUpdates", params=params, timeout=25)
                if resp.status_code != 200:
                    time.sleep(3)
                    continue

                data = resp.json()
                if not data.get('ok'):
                    time.sleep(3)
                    continue

                for update in data.get('result', []):
                    offset = update['update_id'] + 1

                    # Handle Callback Queries (Inline Button Clicks)
                    if 'callback_query' in update:
                        self.handle_callback(api_url, update['callback_query'])
                        continue

                    # Handle Messages
                    message = update.get('message')
                    if not message:
                        continue

                    chat_id = message['chat']['id']
                    text = message.get('text', '').strip()

                    if text in ['/start', 'Start']:
                        reply = (
                            "👋 <b>Assalomu alaykum!</b>\n\n"
                            "<b>'Yosh Yetakchilar'</b> Telegram botiga xush kelibsiz!\n\n"
                            "Siz bu bot orqali loyihada ishtirok etish uchun ariza topshirishingiz "
                            "va adminlar bilan bog'lanishingiz mumkin.\n\n"
                            "📌 <b>Mavjud buyruqlar:</b>\n"
                            "/ariza - Loyihaga ariza topshirish\n"
                            "/id - Chat ID raqamingizni olish (Adminlar uchun)\n"
                            "/help - Yordam"
                        )
                        self.send_message(api_url, chat_id, reply)

                    elif text in ['/id', '/myid']:
                        reply = f"🆔 <b>Sizning Chat IDingiz:</b> <code>{chat_id}</code>\n\n<i>Admin bildirishnomalari uchun settings.py ga kiriting.</i>"
                        self.send_message(api_url, chat_id, reply)

                    elif text in ['/help', 'Help']:
                        reply = "❓ Yordam uchun vebsaytimizga tashrif buyuring yoki adminlarga murojaat qiling."
                        self.send_message(api_url, chat_id, reply)

                    elif text.startswith('/ariza'):
                        reply = (
                            "📝 <b>Ariza topshirish:</b>\n\n"
                            "Iltimos, ismingiz va telefon raqamingizni yuboring:\n"
                            "Masalan: <i>Ali Valiyev +998901234567</i>\n\n"
                            "yoki vebsayt orqali ariza qoldiring!"
                        )
                        self.send_message(api_url, chat_id, reply)

            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("Bot to'xtatildi."))
                break
            except Exception as e:
                logger.error(f"Bot xatoligi: {e}")
                time.sleep(3)

    def handle_callback(self, api_url, cb):
        cb_id = cb['id']
        data = cb.get('data', '')
        message = cb.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        msg_id = message.get('message_id')
        admin_user = cb.get('from', {})
        admin_name = admin_user.get('first_name', '')
        admin_username = f"@{admin_user.get('username')}" if admin_user.get('username') else admin_name

        if data.startswith('app_contacted_') or data.startswith('app_rejected_'):
            app_id = data.split('_')[-1]
            action = 'CONTACTED' if 'contacted' in data else 'REJECTED'

            app = Application.objects.filter(id=app_id).first()
            if app:
                app.status = action
                app.save()

            status_text = "✅ ISHLAB BOʻLINGAN ARIZA (Bogʻlanildi)" if action == 'CONTACTED' else "❌ RAD ETILGAN ARIZA"
            status_badge = "🟢 Bogʻlanildi (Koʻrib chiqildi)" if action == 'CONTACTED' else "🔴 Rad etildi"

            new_text = (
                f"<b>{status_text} (#id{app_id})</b>\n\n"
                f"👤 <b>Ism va Familiya:</b> {app.full_name if app else 'Nomzod'}\n"
                f"📞 <b>Telefon:</b> {app.phone if app else '-'}\n"
                f"✈️ <b>Telegram:</b> {app.telegram_username if app else '-'}\n"
                f"📊 <b>Holati:</b> {status_badge}\n"
                f"👨‍💼 <b>Ishlovchi Admin:</b> {admin_username}\n"
            )

            new_buttons = []
            if action == 'CONTACTED':
                new_buttons.append([{'text': '🟢 Ishlab boʻlindi (Bogʻlanildi)', 'callback_data': 'done'}])
            else:
                new_buttons.append([{'text': '🔴 Rad etildi', 'callback_data': 'done'}])

            tg_user = app.telegram_username.replace('@', '').strip() if app else ''
            if tg_user and tg_user != 'kiritilmagan':
                new_buttons.append([{'text': '💬 Telegramda yozish', 'url': f'https://t.me/{tg_user}'}])

            # Edit message in Telegram
            try:
                requests.post(f"{api_url}/editMessageText", json={
                    'chat_id': chat_id,
                    'message_id': msg_id,
                    'text': new_text,
                    'parse_mode': 'HTML',
                    'reply_markup': {'inline_keyboard': new_buttons}
                }, timeout=5)

                requests.post(f"{api_url}/answerCallbackQuery", json={
                    'callback_query_id': cb_id,
                    'text': f"Ariza holati oʻzgartirildi: {status_badge}"
                }, timeout=5)
            except Exception as e:
                logger.error(f"Callback handle error: {e}")

    def send_message(self, api_url, chat_id, text):
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        try:
            requests.post(f"{api_url}/sendMessage", json=payload, timeout=5)
        except Exception as e:
            logger.error(f"Message send error: {e}")
