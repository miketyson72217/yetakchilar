from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Leader, Journal, Application
from .telegram_bot import send_telegram_application_notification

import random
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
import bleach

ALLOWED_TAGS = [
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'hr',
    'strong', 'em', 'u', 's', 'a', 'img', 'ul', 'ol', 'li',
    'blockquote', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'span', 'div', 'sub', 'sup',
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'target', 'rel'],
    'img': ['src', 'alt', 'width', 'height'],
    'td': ['colspan', 'rowspan'],
    'th': ['colspan', 'rowspan'],
    'span': ['style'],
    'div': ['style'],
    'p': ['style'],
}

def sanitize_html(html_content):
    """Sanitize HTML content to prevent XSS attacks."""
    if not html_content:
        return ''
    return bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )

def index_view(request):
    featured_leaders = Leader.objects.filter(is_featured=True).order_by('-created_at')[:12]
    journal = Journal.objects.filter(is_active=True).first()
    
    # Random quote size for homepage
    quotes_qs = Leader.objects.filter(show_quote=True, quote_poster__isnull=False).order_by('-created_at')[:3]
    quotes = list(quotes_qs)
    for q in quotes:
        opts = []
        if q.quote_poster: opts.append(q.quote_poster.url)
        if q.quote_poster_1x1: opts.append(q.quote_poster_1x1.url)
        q.random_poster_url = random.choice(opts) if opts else None

    total_leaders_count = Leader.objects.count()
    
    context = {
        'featured_leaders': featured_leaders,
        'journal': journal,
        'quotes': quotes,
        'total_leaders_count': total_leaders_count or 500,
    }
    return render(request, 'index.html', context)


def biz_haqimizda_view(request):
    return render(request, 'biz_haqimizda.html')


def yetakchilar_view(request):
    sphere = request.GET.get('sphere')
    leaders = Leader.objects.all().order_by('-created_at')
    if sphere and sphere != 'all':
        leaders = leaders.filter(sphere=sphere)

    context = {
        'leaders': leaders,
        'active_sphere': sphere or 'all',
    }
    return render(request, 'yetakchilar.html', context)


from django.http import JsonResponse, Http404

def leader_detail_view(request, slug):
    leader = Leader.objects.filter(slug=slug).first()

    # Smart fallback: if old slug or partial match, find leader and redirect to new slug
    if not leader:
        slug_parts = [p for p in slug.split('-') if len(p) > 2 and p not in ['dr', 'mr', 'mrs', 'ms']]
        for part in slug_parts:
            candidate = Leader.objects.filter(name__icontains=part).first() or Leader.objects.filter(slug__icontains=part).first()
            if candidate:
                return redirect(f"/yetakchi/{candidate.slug}/", permanent=True)
        raise Http404("Bunday yetakchi topilmadi.")

    related_leaders = Leader.objects.exclude(id=leader.id).filter(sphere=leader.sphere)[:3]
    
    # Sanitize rich text content to prevent XSS
    if leader.full_bio:
        leader.full_bio = sanitize_html(leader.full_bio)

    context = {
        'leader': leader,
        'related_leaders': related_leaders,
    }
    return render(request, 'leader_detail.html', context)



def jurnal_view(request):
    journal = Journal.objects.filter(is_active=True).first()
    context = {
        'journal': journal,
    }
    return render(request, 'jurnal.html', context)




def iqtiboslar_view(request):
    quotes_qs = Leader.objects.filter(show_quote=True).order_by('-created_at')[:7]
    quotes = list(quotes_qs)
    for q in quotes:
        opts = []
        if q.quote_poster: opts.append(q.quote_poster.url)
        if q.quote_poster_1x1: opts.append(q.quote_poster_1x1.url)
        q.random_poster_url = random.choice(opts) if opts else None

    context = {
        'quotes': quotes,
    }
    return render(request, 'iqtiboslar.html', context)



import logging

logger = logging.getLogger(__name__)

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def ariza_view(request):
    if request.method == 'POST':
        full_name = (request.POST.get('full_name') or request.POST.get('name', '')).strip()
        phone = (request.POST.get('phone', '')).strip()
        telegram_username = (request.POST.get('telegram_username') or request.POST.get('telegram', '')).strip()

        if telegram_username and not telegram_username.startswith('@'):
            telegram_username = f"@{telegram_username}"

        if full_name and phone:
            app = Application.objects.create(
                full_name=full_name,
                phone=phone,
                telegram_username=telegram_username or '@kiritilmagan'
            )
            
            # Send Telegram Bot notification to Admin Group
            try:
                send_telegram_application_notification(app)
            except Exception as e:
                logger.error(f"Telegram notification error: {e}")

            success_msg = 'Arizangiz muvaffaqiyatli yuborildi! Tez orada jamoamiz arizangizni ko‘rib chiqib, siz bilan bog‘lanishadi.'


            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', '').lower()
            if is_ajax:
                return JsonResponse({'status': 'ok', 'message': success_msg})

            messages.success(request, success_msg)
            return redirect('/ariza/')
        else:
            err_msg = 'Iltimos, barcha majburiy maydonlarni to‘liq kiriting.'
            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', '').lower()
            if is_ajax:
                return JsonResponse({'status': 'error', 'message': err_msg}, status=400)
            messages.error(request, err_msg)
            return redirect('/ariza/')

    return render(request, 'ariza.html')


from django.http import HttpResponse

def robots_txt(request):
    content = """User-agent: *
Allow: /

Sitemap: https://yetakchilar.uz/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')


def sitemap_xml(request):
    leaders = Leader.objects.all()
    return render(request, 'sitemap.xml', {'leaders': leaders}, content_type='application/xml')

def google_verification(request):
    return HttpResponse("google-site-verification: googlea7829e18419689e0.html", content_type="text/html")
