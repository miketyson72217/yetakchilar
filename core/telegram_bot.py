import json
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

TOTAL_PRICE = 80_000
INSTALLMENT_STEP = 10_000
INSTALLMENT_DAYS = 12


def _bot_request(method, payload):
    """Internal helper to call Telegram Bot API."""
    bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    if not bot_token:
        logger.warning("TELEGRAM_BOT_TOKEN sozlanmagan")
        return None
    url = f"https://api.telegram.org/bot{bot_token}/{method}"
    try:
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error(f"Telegram API xatosi ({method}): {e}")
        return None


def _get_keyboard_for_status(application):
    """
    Returns the correct inline keyboard based on application's current status and payment_type.
    This is the single source of truth for all bot button states.
    """
    app_id = application.id
    tg_user = application.telegram_username.replace('@', '').strip()
    status = application.status
    payment_type = application.payment_type
    paid = application.paid_amount

    # ------------------------------------------------------------------
    # State 1: NEW — just arrived, need to contact
    # ------------------------------------------------------------------
    if status == 'NEW':
        keyboard = [
            [
                {'text': '✅ Bog‘lanildi', 'callback_data': f'app_contacted_{app_id}'},
                {'text': '⚠️ Bog‘lanishni iloji bo‘lmadi', 'callback_data': f'app_unreachable_{app_id}'},
            ]
        ]
        if tg_user and tg_user != 'kiritilmagan':
            keyboard.append([{'text': '💬 Telegramda yozish', 'url': f'https://t.me/{tg_user}'}])
        return keyboard

    # ------------------------------------------------------------------
    # State 2: CONTACTED — talked, now approve or reject
    # ------------------------------------------------------------------
    if status == 'CONTACTED':
        keyboard = [
            [
                {'text': '✅ Qabul qilindi', 'callback_data': f'app_approved_{app_id}'},
                {'text': '❌ Rad etildi', 'callback_data': f'app_rejected_{app_id}'},
            ]
        ]
        if tg_user and tg_user != 'kiritilmagan':
            keyboard.append([{'text': '💬 Telegramda yozish', 'url': f'https://t.me/{tg_user}'}])
        return keyboard

    # ------------------------------------------------------------------
    # State 3: APPROVED — choose payment type
    # ------------------------------------------------------------------
    if status == 'APPROVED':
        keyboard = [
            [
                {'text': f'💳 Bir martada — {TOTAL_PRICE:,} so‘m', 'callback_data': f'app_pay_full_{app_id}'},
            ],
            [
                {'text': f'📅 Bo‘lib-bo‘lib — {INSTALLMENT_DAYS} kun', 'callback_data': f'app_pay_installment_{app_id}'},
            ],
        ]
        if tg_user and tg_user != 'kiritilmagan':
            keyboard.append([{'text': '💬 Telegramda yozish', 'url': f'https://t.me/{tg_user}'}])
        return keyboard

    # ------------------------------------------------------------------
    # State 4: IN_PROGRESS — payment started
    # ------------------------------------------------------------------
    if status == 'IN_PROGRESS':
        if payment_type == 'full':
            # Waiting for full payment confirmation
            keyboard = [
                [{'text': f'✅ {TOTAL_PRICE:,} so‘m to‘lov tasdiqlandi — PROFIL YARATING', 'callback_data': f'app_fully_paid_{app_id}'}],
            ]
        else:
            # Installment mode
            remaining = TOTAL_PRICE - paid
            next_step = min(INSTALLMENT_STEP, remaining)
            keyboard = []

            if paid == 0:
                keyboard.append([{
                    'text': f'✅ Birinchi {INSTALLMENT_STEP:,} so‘m keldi — Profil yaratishni boshlang',
                    'callback_data': f'app_first_paid_{app_id}'
                }])
            elif paid < TOTAL_PRICE:
                keyboard.append([{
                    'text': f'➕ Keyingi to‘lov keldi (+{next_step:,} so‘m) — Jami: {paid + next_step:,} / {TOTAL_PRICE:,}',
                    'callback_data': f'app_next_paid_{app_id}'
                }])
                keyboard.append([{
                    'text': f'✅ To‘lov yakunlandi ({TOTAL_PRICE:,} so‘m to‘liq)',
                    'callback_data': f'app_fully_paid_{app_id}'
                }])

        if tg_user and tg_user != 'kiritilmagan':
            keyboard.append([{'text': '💬 Telegramda yozish', 'url': f'https://t.me/{tg_user}'}])
        return keyboard

    # ------------------------------------------------------------------
    # Terminal states: COMPLETED, REJECTED, UNREACHABLE
    # ------------------------------------------------------------------
    if tg_user and tg_user != 'kiritilmagan':
        return [[{'text': '💬 Telegramda yozish', 'url': f'https://t.me/{tg_user}'}]]
    return []


def _get_status_header(application):
    """Returns a formatted status header line for the message."""
    icons = {
        'NEW': '🟡 Yangi ariza',
        'CONTACTED': '🔵 Bog‘lanildi — Suhbat jarayonida',
        'UNREACHABLE': '🔴 Bog‘lanishni iloji bo‘lmadi',
        'APPROVED': '🟢 Qabul qilindi — To‘lov turi tanlansin',
        'REJECTED': '❌ Rad etildi',
        'IN_PROGRESS': '💳 Jarayonda — To‘lov kuzatilmoqda',
        'COMPLETED': '✅ Yakunlandi — To‘lov to‘liq',
    }
    label = icons.get(application.status, application.status)

    if application.status == 'IN_PROGRESS' and application.payment_type == 'installment':
        label += f'\n💰 To‘langan: {application.paid_amount:,} / {TOTAL_PRICE:,} so‘m'
    elif application.status == 'IN_PROGRESS' and application.payment_type == 'full':
        label += f'\n💰 To‘lov kutilmoqda: {TOTAL_PRICE:,} so‘m (bir martada)'
    elif application.status == 'COMPLETED':
        label += f'\n💰 To\'liq to‘langan: {application.paid_amount:,} so‘m'

    return label


def _build_message_text(application):
    """Builds the full message text."""
    status_header = _get_status_header(application)
    return (
        f"📥 <b>ARIZA #{application.id} — {application.full_name}</b>\n\n"
        f"📞 <b>Telefon:</b> {application.phone}\n"
        f"✈️ <b>Telegram:</b> {application.telegram_username}\n"
        f"📅 <b>Vaqti:</b> {application.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
        f"<b>Holat:</b> {status_header}"
    )


def send_telegram_application_notification(application):
    """
    Sends the initial notification to the admin group when a new application is submitted.
    Saves the returned message_id to application.telegram_message_id for later editing.
    """
    chat_id = getattr(settings, 'TELEGRAM_ADMIN_CHAT_ID', '')
    if not chat_id:
        logger.warning("TELEGRAM_ADMIN_CHAT_ID sozlanmagan")
        return False

    keyboard = _get_keyboard_for_status(application)
    message_text = _build_message_text(application)

    result = _bot_request('sendMessage', {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'HTML',
        'reply_markup': {'inline_keyboard': keyboard},
    })

    if result and result.get('ok'):
        msg_id = result['result']['message_id']
        # Save message_id to DB for future edits
        application.telegram_message_id = msg_id
        application.save(update_fields=['telegram_message_id'])
        logger.info(f"Telegram xabari yuborildi, message_id={msg_id}, ariza #{application.id}")
        return True
    return False


def edit_telegram_message(application):
    """
    Edits the existing bot message in the admin group to reflect the new status and keyboard.
    Called after each callback action.
    """
    chat_id = getattr(settings, 'TELEGRAM_ADMIN_CHAT_ID', '')
    message_id = application.telegram_message_id

    if not chat_id or not message_id:
        logger.warning(f"edit_telegram_message: chat_id yoki message_id yo'q (ariza #{application.id})")
        return False

    keyboard = _get_keyboard_for_status(application)
    message_text = _build_message_text(application)

    result = _bot_request('editMessageText', {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': message_text,
        'parse_mode': 'HTML',
        'reply_markup': {'inline_keyboard': keyboard},
    })

    if result and result.get('ok'):
        logger.info(f"Telegram xabari yangilandi, ariza #{application.id}")
        return True
    logger.error(f"Telegram xabarini yangilashda xato: {result}")
    return False


def answer_callback_query(callback_query_id, text='', show_alert=False):
    """Answers a Telegram callback query to dismiss the loading indicator."""
    _bot_request('answerCallbackQuery', {
        'callback_query_id': callback_query_id,
        'text': text,
        'show_alert': show_alert,
    })
