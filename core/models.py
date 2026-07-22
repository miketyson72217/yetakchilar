from django.db import models
from django.utils.text import slugify

class Leader(models.Model):
    SPHERE_CHOICES = [
        ('biznes', 'Tadbirkorlik & Biznes'),
        ('texno', 'Texnologiya & IT'),
        ('sport', 'Sport'),
        ('fan', 'Fan & Taʻlim'),
        ('sanat', 'Sanʻat & Madaniyat'),
        ('tibbiyot', 'Tibbiyot'),
        ('ijtimoiy', 'Ijtimoiy faoliyat'),
    ]

    REGION_CHOICES = [
        ('Toshkent', 'Toshkent shahri'),
        ('Samarqand', 'Samarqand'),
        ('Fargʻona', 'Fargʻona'),
        ('Namangan', 'Namangan'),
        ('Andijon', 'Andijon'),
        ('Buxoro', 'Buxoro'),
        ('Xorazm', 'Xorazm'),
        ('Qashqadaryo', 'Qashqadaryo'),
        ('Surxondaryo', 'Surxondaryo'),
        ('Sirdaryo', 'Sirdaryo'),
        ('Jizzax', 'Jizzax'),
        ('Navoiy', 'Navoiy'),
        ('Qoraqalpogʻiston', 'Qoraqalpogʻiston'),
        ('Toshkent viloyati', 'Toshkent viloyati'),
    ]

    name = models.CharField(max_length=255, verbose_name="Ism va Familiya")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL slagi")
    sphere = models.CharField(max_length=50, choices=SPHERE_CHOICES, verbose_name="Soha")
    region = models.CharField(max_length=100, choices=REGION_CHOICES, verbose_name="Viloyat")
    photo = models.ImageField(upload_to='leaders/', verbose_name="Portret rasm")
    short_bio = models.CharField(max_length=255, verbose_name="Qisqa tavsif / Unvon")
    full_bio = models.TextField(blank=True, verbose_name="Toʻliq biografiya va yutuqlar")
    birth_date = models.CharField(max_length=100, blank=True, verbose_name="Tugʻilgan sana")
    birth_place = models.CharField(max_length=100, blank=True, verbose_name="Tugʻilgan joy")
    education = models.CharField(max_length=255, blank=True, verbose_name="Taʻlim")
    top100_rank = models.PositiveIntegerField(null=True, blank=True, verbose_name="TOP 100 oʻrni")
    quote_poster = models.ImageField(upload_to='leaders/quotes/', blank=True, null=True, verbose_name="Iqtibos poster rasmi (Rasm sifatida)")
    is_featured = models.BooleanField(default=False, verbose_name="Bosh sahifada koʻrsatish")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qoʻshilgan vaqt")

    class Meta:
        verbose_name = "Yetakchi"
        verbose_name_plural = "Yetakchilar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_sphere_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            components = [self.name]
            if self.sphere:
                components.append(self.sphere)
            if self.region:
                components.append(self.region)

            base_slug = slugify(" ".join(components))
            if not base_slug:
                base_slug = 'yetakchi'

            slug = base_slug
            counter = 1
            while Leader.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)



class Journal(models.Model):
    issue_number = models.PositiveIntegerField(default=1, verbose_name="Son raqami")
    title = models.CharField(max_length=255, verbose_name="Jurnal sarlavhasi")
    author = models.CharField(max_length=255, default='Oʻzbekiston Yetakchi Yoshlari', verbose_name="Muallif")
    description = models.TextField(verbose_name="Tavsif")
    front_cover = models.ImageField(upload_to='journals/covers/', verbose_name="Old muqova rasmi")
    back_cover = models.ImageField(upload_to='journals/covers/', blank=True, null=True, verbose_name="Orqa muqova rasmi")
    pdf_file = models.FileField(upload_to='journals/pdfs/', blank=True, null=True, verbose_name="PDF fayl (Yuklab olish uchun)")
    pages_count = models.PositiveIntegerField(default=48, verbose_name="Sahifalar soni")
    file_size = models.CharField(max_length=50, default='24 MB', verbose_name="Fayl hajmi")
    issn = models.CharField(max_length=50, default='ISSN 2023-1234', verbose_name="ISSN raqami")
    release_date = models.CharField(max_length=100, default='Iyun 2024', verbose_name="Chop etilgan sana")
    is_active = models.BooleanField(default=True, verbose_name="Faol / Eʻlon qilingan")

    class Meta:
        verbose_name = "Online Jurnal"
        verbose_name_plural = "Online Jurnallar"
        ordering = ['-issue_number']

    def __str__(self):
        return f"{self.issue_number}-son: {self.title}"


class Quote(models.Model):
    quote_text = models.TextField(verbose_name="Iqtibos matni")
    author_name = models.CharField(max_length=255, verbose_name="Muallif ismi")
    author_title = models.CharField(max_length=255, verbose_name="Muallif kasbi / unvoni")
    author_photo = models.ImageField(upload_to='quotes/', blank=True, null=True, verbose_name="Muallif rasmi")
    poster_image = models.ImageField(upload_to='quotes/posters/', blank=True, null=True, verbose_name="Iqtibos poster rasmi (Rasm sifatida)")
    is_featured = models.BooleanField(default=True, verbose_name="Bosh sahifada koʻrsatish")

    class Meta:
        verbose_name = "Iqtibos"
        verbose_name_plural = "Iqtiboslar"

    def __str__(self):
        return f'"{self.quote_text[:40]}..." — {self.author_name}'


class Application(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Yangi'),
        ('CONTACTED', 'Bogʻlanildi'),
        ('APPROVED', 'Qabul qilindi'),
        ('REJECTED', 'Rad etildi'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="Ism va Familiya")
    phone = models.CharField(max_length=50, verbose_name="Telefon raqami")
    telegram_username = models.CharField(max_length=100, verbose_name="Telegram Username")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Holat")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")

    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Ariza: {self.full_name} ({self.phone}) — {self.get_status_display()}"
