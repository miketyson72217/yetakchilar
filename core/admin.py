from django.contrib import admin
from django.utils.html import format_html
from .models import Leader, Journal, Quote, Application

admin.site.site_header = "Oʻzbekiston Yetakchi Yoshlari Ensiklopediyasi"
admin.site.site_title = "OʻzYYE Boshqaruv Paneli"
admin.site.index_title = "Ensiklopediyani Boshqarish"


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'name', 'sphere', 'region', 'top100_rank', 'is_featured', 'created_at')
    list_filter = ('sphere', 'region', 'is_featured')
    search_fields = ('name', 'short_bio', 'full_bio')
    prepopulated_fields = {'slug': ('name', 'sphere')}
    list_editable = ('top100_rank', 'is_featured')


    fieldsets = (
        ("Asosiy Maʻlumotlar", {
            'fields': ('name', 'slug', 'sphere', 'region', 'photo', 'short_bio', 'is_featured', 'top100_rank')
        }),
        ("Iqtibos Poster Rasmi", {
            'fields': ('quote_poster',)
        }),
        ("Shaxsiy & Kasbiy Tafsilotlar", {
            'fields': ('birth_date', 'birth_place', 'education', 'full_bio')
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />', obj.photo.url)
        return "Rasm yoʻq"
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
        return "Muqova yoʻq"
    cover_preview.short_description = "Muqova"


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_title', 'quote_preview', 'is_featured')
    list_filter = ('is_featured',)
    search_fields = ('author_name', 'quote_text')
    list_editable = ('is_featured',)

    def quote_preview(self, obj):
        return obj.quote_text[:60] + "..." if len(obj.quote_text) > 60 else obj.quote_text
    quote_preview.short_description = "Iqtibos Matni"


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'telegram_username', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'phone', 'telegram_username')
    list_editable = ('status',)
    readonly_fields = ('full_name', 'phone', 'telegram_username', 'created_at')

    fieldsets = (
        ("Nomzod Maʻlumotlari", {
            'fields': ('full_name', 'phone', 'telegram_username', 'created_at')
        }),
        ("Qaror / Holat", {
            'fields': ('status',)
        }),
    )
