from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import uuid

import os

def get_profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('leaders/', filename)

class Leader(models.Model):
    SPHERE_CHOICES = [
        ('biznes', 'Tadbirkorlik va Biznes'),
        ('texno', 'Texnologiya va IT'),
        ('sport', 'Sport'),
        ('fan', 'Fan va Ta’lim'),
        ('sanat', 'San’at va Madaniyat'),
        ('tibbiyot', 'Tibbiyot'),
        ('ijtimoiy', 'Ijtimoiy faoliyat'),
        ('media', 'Media va Jurnalistika'),
    ]

    REGION_CHOICES = [
        ('Toshkent', 'Toshkent shahri'),
        ('Samarqand', 'Samarqand'),
        ('Farg‘ona', 'Farg‘ona'),
        ('Namangan', 'Namangan'),
        ('Andijon', 'Andijon'),
        ('Buxoro', 'Buxoro'),
        ('Xorazm', 'Xorazm'),
        ('Qashqadaryo', 'Qashqadaryo'),
        ('Surxondaryo', 'Surxondaryo'),
        ('Sirdaryo', 'Sirdaryo'),
        ('Jizzax', 'Jizzax'),
        ('Navoiy', 'Navoiy'),
        ('Qoraqalpog‘iston', 'Qoraqalpog‘iston'),
        ('Toshkent viloyati', 'Toshkent viloyati'),
    ]

    name = models.CharField(max_length=255, verbose_name="F.I.SH. (Familiya, ism, sharif)")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL slagi")
    sphere = models.CharField(max_length=50, choices=SPHERE_CHOICES, verbose_name="Soha")
    region = models.CharField(max_length=100, choices=REGION_CHOICES, verbose_name="Hudud")
    photo = models.ImageField(upload_to=get_profile_image_path, verbose_name="Portret rasm")
    short_bio = models.CharField(max_length=255, blank=True, null=True, verbose_name="Qisqa status (masalan: Ijodkor | Jamoatchilik faoli)")
    full_bio = RichTextField(blank=True, verbose_name="To‘liq biografiya va yutuqlar")
    bio_file = models.FileField(upload_to='bios/', blank=True, null=True, verbose_name="Biografiya fayli (PDF/DOCX, ixtiyoriy)")
    birth_date = models.CharField(max_length=100, blank=True, verbose_name="Tug‘ilgan sana")
    birth_place = models.CharField(max_length=100, blank=True, verbose_name="Tug‘ilgan joy")
    education = models.CharField(max_length=255, blank=True, verbose_name="Ta’lim")
    quote_poster = models.ImageField(upload_to='leaders/quotes/', blank=True, null=True, verbose_name="Iqtibos poster rasmi (16:9 keng)")
    quote_poster_1x1 = models.ImageField(upload_to='leaders/quotes/1x1/', blank=True, null=True, verbose_name="Iqtibos poster rasmi (1:1 kvadrat)")
    is_featured = models.BooleanField(default=False, verbose_name="Bosh sahifada yetakchini ko‘rsatish")
    show_in_leaders = models.BooleanField(default=False, verbose_name="Yetakchilar sahifasida ko‘rsatish (Top)")
    show_quote = models.BooleanField(default=False, verbose_name="Iqtiboslar sahifasida ko‘rsatish (Top)")
    is_quote_featured = models.BooleanField(default=False, verbose_name="Bosh sahifada iqtibosini ko‘rsatish")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo‘shilgan sana")

    class Meta:
        verbose_name = "Yetakchi"
        verbose_name_plural = "Yetakchilar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_sphere_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = str(uuid.uuid4())
            while Leader.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = str(uuid.uuid4())
            self.slug = slug
        super().save(*args, **kwargs)



class Journal(models.Model):
    issue_number = models.PositiveIntegerField(default=1, verbose_name="Son raqami")
    title = models.CharField(max_length=255, verbose_name="Jurnal sarlavhasi")
    author = models.CharField(max_length=255, default='O‘zbekiston Yetakchi Yoshlari', verbose_name="Muallif")
    description = models.TextField(verbose_name="Tavsif")
    front_cover = models.ImageField(upload_to='journals/covers/', verbose_name="Old muqova rasmi")
    back_cover = models.ImageField(upload_to='journals/covers/', blank=True, null=True, verbose_name="Orqa muqova rasmi")
    pdf_file = models.FileField(upload_to='journals/pdfs/', blank=True, null=True, verbose_name="PDF fayl (Yuklab olish uchun)")
    pages_count = models.PositiveIntegerField(default=48, verbose_name="Sahifalar soni")
    file_size = models.CharField(max_length=50, default='24 MB', verbose_name="Fayl hajmi")
    issn = models.CharField(max_length=50, default='ISSN 2023-1234', verbose_name="ISSN raqami")
    release_date = models.CharField(max_length=100, default='Iyun 2024', verbose_name="Chop etilgan sana")
    is_active = models.BooleanField(default=True, verbose_name="Faol / E’lon qilingan")

    class Meta:
        verbose_name = "Online Jurnal"
        verbose_name_plural = "Online Jurnallar"
        ordering = ['-issue_number']

    def __str__(self):
        return f"{self.issue_number}-son: {self.title}"




class Application(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Yangi'),
        ('CONTACTED', 'Bog‘lanildi'),
        ('UNREACHABLE', 'Bog‘lanib bo‘lmadi'),
        ('APPROVED', 'Qabul qilindi — To‘lov kutilmoqda'),
        ('REJECTED', 'Rad etildi'),
        ('IN_PROGRESS', 'Jarayonda (To‘lov boshlandi)'),
        ('COMPLETED', 'Yakunlandi (To‘liq to‘landi)'),
    ]

    PAYMENT_TYPE_CHOICES = [
        ('full', 'Bir martada — 80,000 so‘m'),
        ('installment', 'Bo‘lib-bo‘lib — 12 kun'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="Ism va Familiya")
    phone = models.CharField(max_length=50, verbose_name="Telefon raqami")
    telegram_username = models.CharField(max_length=100, verbose_name="Telegram Username")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Holat")
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_TYPE_CHOICES,
        null=True, blank=True, verbose_name="To‘lov turi"
    )
    paid_amount = models.PositiveIntegerField(default=0, verbose_name="To‘langan summa (so‘mda)")
    telegram_message_id = models.BigIntegerField(null=True, blank=True, verbose_name="Bot xabar IDsi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")

    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Ariza: {self.full_name} ({self.phone}) — {self.get_status_display()}"

class JournalArticle(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='articles', verbose_name="Jurnal")
    category = models.CharField(max_length=100, verbose_name="Kategoriya (masalan: LIDERLIK va INTIZOM)")
    title = models.CharField(max_length=255, verbose_name="Maqola sarlavhasi")
    short_description = models.TextField(verbose_name="Qisqa tavsif (Ushbu sonda nimalar bor uchun)")
    author_name = models.CharField(max_length=255, verbose_name="Muallif ismi")
    page_number = models.PositiveIntegerField(verbose_name="Sahifa raqami (Jurnal ichida)")
    content = models.TextField(verbose_name="Maqola matni (paragraflar uchun)")
    pull_quote = models.CharField(max_length=500, blank=True, null=True, verbose_name="Iqtibos (Pull quote)")
    
    class Meta:
        verbose_name = "Jurnal Maqolasi"
        verbose_name_plural = "Jurnal Maqolalari"
        ordering = ['page_number']

    def __str__(self):
        return f"{self.title} ({self.page_number}-sahifa)"

from .countries import COUNTRY_CHOICES
from django.utils.text import slugify
import uuid

class Opportunity(models.Model):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="URL Slug")
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, blank=True, null=True, verbose_name="Davlat")
    format = models.CharField(max_length=100, blank=True, null=True, verbose_name="Dastur shakli (masalan: Oflayn)")
    badge = models.CharField(max_length=50, blank=True, null=True, verbose_name="Maxsus belgi (Masalan: Maxsus grant)")
    age_category = models.CharField(max_length=50, blank=True, null=True, verbose_name="Yosh toifasi (masalan: 18-30)")
    description = RichTextField(verbose_name="Batafsil ma’lumot (Matn va imtiyozlar)")
    registration_link = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ro‘yxatdan o‘tish havolasi")
    deadline = models.CharField(max_length=100, blank=True, null=True, verbose_name="So‘nggi muddat (masalan: 30-Avgust)")
    deadline_date = models.DateField(blank=True, null=True, verbose_name="Haqiqiy sana (Avtomatlashtirish uchun)")
    image = models.ImageField(upload_to='opportunities/', blank=True, null=True, verbose_name="Rasm / Poster")
    is_active = models.BooleanField(default=True, verbose_name="Faol / E’lon qilingan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo‘shilgan sana")

    class Meta:
        verbose_name = "Imkoniyat (Grant/Dastur)"
        verbose_name_plural = "Imkoniyatlar (Grantlar/Dasturlar)"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        super().save(*args, **kwargs)
