import os
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views
from django.views.generic.base import RedirectView

admin_url_path = os.environ.get('ADMIN_URL_PATH', 'admin-yt-9k8v7q2x4m/').strip('/')

urlpatterns = [
    path(f'{admin_url_path}/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon-192x192.png', permanent=True)),
    
    # Home routes
    path('', views.index_view, name='index'),
    path('index.html', views.index_view, name='index_html'),
    
    # Biz haqimizda routes
    path('biz-haqimizda/', views.biz_haqimizda_view, name='biz_haqimizda_slash'),
    path('biz-haqimizda', views.biz_haqimizda_view, name='biz_haqimizda_clean'),
    path('biz_haqimizda.html', views.biz_haqimizda_view, name='biz_haqimizda'),

    # Yetakchilar routes
    path('yetakchilar/', views.yetakchilar_view, name='yetakchilar_slash'),
    path('yetakchilar', views.yetakchilar_view, name='yetakchilar_clean'),
    path('yetakchilar.html', views.yetakchilar_view, name='yetakchilar'),

    # Yetakchi detail routes
    path('yetakchi/<slug:slug>/', views.leader_detail_view, name='leader_detail'),
    path('yetakchi/<slug:slug>', views.leader_detail_view),
    path('yetakchi/<slug:slug>/index.html', views.leader_detail_view),
    
    path('kamalova_maftuna.html', views.leader_detail_view, {'slug': 'kamalova-maftuna'}, name='kamalova_maftuna'),
    path('kamalova-maftuna', views.leader_detail_view, {'slug': 'kamalova-maftuna'}),

    # Jurnal routes
    path('jurnal/', views.jurnal_view, name='jurnal_slash'),
    path('jurnal', views.jurnal_view, name='jurnal_clean'),
    path('jurnal.html', views.jurnal_view, name='jurnal'),

    # Iqtiboslar routes
    path('iqtiboslar/', views.iqtiboslar_view, name='iqtiboslar_slash'),
    path('iqtiboslar', views.iqtiboslar_view, name='iqtiboslar_clean'),
    path('iqtiboslar.html', views.iqtiboslar_view, name='iqtiboslar'),


    # Imkoniyatlar routes
    path('imkoniyatlar/', views.imkoniyatlar_view, name='imkoniyatlar_slash'),
    path('imkoniyatlar', views.imkoniyatlar_view, name='imkoniyatlar_clean'),
    path('imkoniyatlar.html', views.imkoniyatlar_view, name='imkoniyatlar'),
    path('imkoniyatlar/<slug:slug>/', views.opportunity_detail_view, name='opportunity_detail'),
    path('imkoniyatlar/<slug:slug>', views.opportunity_detail_view),

    # Ariza routes
    path('ariza/', views.ariza_view, name='ariza_slash'),
    path('ariza', views.ariza_view, name='ariza_clean'),
    path('ariza.html', views.ariza_view, name='ariza'),

    # SEO routes
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('googlea7829e18419689e0.html', views.google_verification, name='google_verification'),

    # Download route
    path('download-image/', views.download_image_view, name='download_image'),

    # Telegram Bot webhook
    path('telegram-webhook/', views.telegram_webhook_view, name='telegram_webhook'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
