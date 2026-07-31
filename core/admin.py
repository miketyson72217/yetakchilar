from django.contrib import admin
from django.utils.html import format_html
from .models import Leader, Journal, Application, JournalArticle

admin.site.site_header = "O‘zbekiston Yetakchi Yoshlari Ensiklopediyasi"
admin.site.site_title = "O‘zYYE Boshqaruv Paneli"
admin.site.index_title = "Ensiklopediyani Boshqarish"


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'name', 'sphere', 'region', 'is_featured', 'show_in_leaders', 'show_quote', 'is_quote_featured', 'created_at')
    list_filter = ('sphere', 'region', 'is_featured', 'show_in_leaders', 'show_quote', 'is_quote_featured')
    search_fields = ('name', 'short_bio', 'full_bio')
    prepopulated_fields = {'slug': ('name', 'sphere')}
    list_editable = ('is_featured', 'show_in_leaders', 'show_quote', 'is_quote_featured')


    fieldsets = (
        ("Asosiy Maʼlumotlar", {
            'fields': ('name', 'slug', 'sphere', 'region', 'photo', 'short_bio', 'is_featured', 'show_in_leaders', 'show_quote', 'is_quote_featured')
        }),
        ("Iqtibos Poster Rasmlari", {
            'fields': ('quote_poster', 'quote_poster_1x1')
        }),
        ("Shaxsiy & Kasbiy Tafsilotlar", {
            'fields': ('birth_date', 'birth_place', 'full_bio', 'bio_file')
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover; object-position: top center;" />', obj.photo.url)
        return "Rasm yo‘q"
    photo_preview.short_description = "Rasm"


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('issue_number', 'title', 'release_date', 'pages_count', 'is_active', 'cover_preview')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('is_active',)

    def cover_preview(self, obj):
        if obj.front_cover:
            return format_html('<img src="{}" style="width: 40px; height: 55px; border-radius: 4px; object-fit: cover;" />', obj.front_cover.url)
        return "Muqova yo‘q"
    cover_preview.short_description = "Muqova"





@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'telegram_username', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'phone', 'telegram_username')
    list_editable = ('status',)
    readonly_fields = ('full_name', 'phone', 'telegram_username', 'created_at')

    fieldsets = (
        ("Nomzod Maʼlumotlari", {
            'fields': ('full_name', 'phone', 'telegram_username', 'created_at')
        }),
        ("Qaror / Holat", {
            'fields': ('status',)
        }),
    )


