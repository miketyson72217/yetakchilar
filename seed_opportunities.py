import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Opportunity

data = [
    {
        "title": "Doha Debates Ambassador Program",
        "country": "Qatar 🇶🇦",
        "format": "Onlayn",
        "age_category": "18-26 yosh",
        "deadline": "24-avgust",
        "registration_link": "https://dohadebates.com",
        "description": "<p>Qatar Foundation'ning \"Doha Debates\" loyihasi. Ishtirokchilar dunyoning eng murakkab muammolarini muhokama qilish, tinglash va konstruktiv muloqot ko'nikmalarini rivojlantiradi, xalqaro tengdoshlar bilan uzoq muddatli aloqalar o'rnatadi.</p><br><b>Imtiyozlari:</b><ul><li>75+ davlatdan yoshlar bilan networking</li><li>Rasmiy Doha Debates sertifikati</li><li>Kelajakda mentor sifatida qatnashish imkoniyati</li><li>Muloqot, tanqidiy fikrlash va liderlik ko'nikmalarini rivojlantirish</li></ul>"
    },
    {
        "title": "Global FinTech Hackcelerator 2026",
        "country": "Singapur 🇸🇬",
        "format": "Gibrid",
        "age_category": "Barcha uchun",
        "deadline": "14-avgust",
        "registration_link": "https://www.fintechfestival.sg/",
        "description": "<p>Dastur moliya sohasidagi dolzarb muammolarga innovatsion yechim taklif etuvchi startaplar hamda dasturchilarni qo'llab-quvvatlash va xalqaro bozorga olib chiqishga qaratilgan.</p><br><b>Imtiyozlari:</b><ul><li>Finalchilar uchun $20,000 Singapur dollari miqdorida grant</li><li>Top-3 g'olib uchun qo'shimcha $150,000 Singapur dollari mukofot jamg'armasi</li><li>Global investorlar va venchur fondlari oldida pitch qilish imkoniyati</li><li>Yetakchi FinTech ekspertlaridan 1-ga-1 mentorlik hamda texnik qo'llab-quvvatlov</li></ul>"
    },
    {
        "title": "United World Colleges",
        "country": "Global (Onlayn) 🌍",
        "format": "To'liq, qisman qoplamali",
        "age_category": "15-17",
        "deadline": "30-sentabr",
        "registration_link": "https://uz.uwc.org/",
        "description": "<p>United World Colleges – dunyoning 4 ta qitʼasida joylashgan 18 ta maktab va kollejlar tizimidir. Oʻzlari tanlagan davlatdagi kollej/maktabga qabul qilingan oʻquvchilar u yerda 2 yil o'qishadi.</p><br><b>Imtiyozlari:</b><ul><li>Bepul yotoqxona va oziq-ovqat</li><li>O'qish to'lovlaridan ozod qilinish, darsliklar</li><li>2 yil IB diplomada o'qish</li></ul>"
    },
    {
        "title": "IT Park International IT Training Program 2026",
        "country": "O‘zbekiston 🇺🇿",
        "format": "Oflayn",
        "age_category": "18–30",
        "deadline": "20-avgust",
        "registration_link": "https://it-park.uz/",
        "description": "<p>IT Park Uzbekistan, Raqamli texnologiyalar vazirligi, American International University–Bangladesh va World Bank hamkorligida tashkil etilgan bepul IT-trening dasturiga arizalar qabul qilinmoqda. Darslar ingliz tilida olib boriladi va bitiruvchilarga IT/ITES kompaniyalarida ishga joylashishda ko‘mak beriladi.</p><br><b>Imtiyozlari:</b><ul><li>To‘liq bepul IT-trening</li><li>Dastur yakunida sertifikat</li><li>50% o‘rinlar qizlar uchun ajratilgan</li><li>IT/ITES kompaniyalarida ishga joylashish bo‘yicha ko‘mak</li></ul>"
    },
    {
        "title": "International Medicine & Health Olympiad",
        "country": "AQSh 🇺🇸",
        "format": "Onlayn",
        "age_category": "14-21",
        "deadline": "21-avgust",
        "registration_link": "https://usmdo.org",
        "description": "<p>Tibbiyot, biologiya va sog‘liqni saqlash sohalariga qiziqadigan o‘quvchilar uchun xalqaro olimpiada. Ishtirokchilar dastlab onlayn saralash bosqichida qatnashadilar. Eng yaxshi natija ko‘rsatganlar xalqaro oflayn final bosqichiga taklif etiladi.</p><br><b>Imtiyozlari:</b><ul><li>Oltin, Kumush, Bronza va Honorable Mention mukofotlari;</li><li>Kuchli ishtirokchilar uchun oflayn final bosqichiga yo‘llanma;</li><li>Rasmiy sertifikat va xalqaro e'tirofga ega bo‘lish imkoniyati.</li></ul>"
    },
    {
        "title": "Youth International Math Olympiad (YIMO) 2026",
        "country": "Global (Onlayn) 🌍",
        "format": "Onlayn",
        "age_category": "Barcha yoshdagi maktab o'quvchilari",
        "deadline": "27-avgust",
        "registration_link": "https://yimo-official.org",
        "description": "<p>Bu matematikaga qiziqadigan o‘quvchilar uchun mo‘ljallangan xalqaro onlayn olimpiada. Ishtirokchilar o‘z darajasiga mos divizionda qatnashib, 20 ta matematik masalani yechadilar. Har bir divizionning eng yaxshi 8 nafar ishtirokchisi hisoblash va isbotlash masalalaridan iborat final bosqichiga yo‘l oladi.</p><br><b>Imtiyozlari:</b><ul><li>Bepul xalqaro onlayn olimpiadada ishtirok etish.</li><li>Oltin, Kumush va Bronza mukofotlari hamda ishtirok sertifikati.</li><li>Kuchli ishtirokchilar uchun final bosqichida qatnashish imkoniyati.</li><li>Xalqaro miqyosda matematik bilim va tajribani sinab ko‘rish imkoniyati.</li></ul>"
    },
    {
        "title": "International Neuroscience Olympiad (INO) 2026",
        "country": "AQSh 🇺🇸",
        "format": "Onlayn",
        "age_category": "13-18 yosh",
        "deadline": "12-oktyabr",
        "registration_link": "https://www.ino-global.net",
        "description": "<p>Dunyoning eng yirik yoshlar neyrofan olimpiadalaridan biri. Bu tanlovda ishtirokchilar neyrofan bo'yicha bilimlarini sinovdan o'tkazadi va real ilmiy muammolarga yechim taklif qiladi.</p><br><b>Imtiyozlari:</b><ul><li>G'oliblarga top-20 universitet bilan tadqiqot imkoniyati (yoki pul mukofoti)</li><li>Xalqaro neyrofan ekspertlari bilan networking</li><li>Kollej arizalari uchun kuchli ilmiy tajriba</li></ul>"
    },

    {
        "title": "Harvard Crimson Global Case Competition",
        "country": "AQSh 🇺🇸",
        "format": "Onlayn",
        "age_category": "13-18",
        "deadline": "16-oktyabr",
        "registration_link": "https://casecomp.org",
        "description": "<p>Bu yuqori maktab o'quvchilari o'rtasida business case musobaqasi bo'lib, ishtirokchilar 2-4 kishilik jamoalar sifatida workshoplarda qatnashib, biznes muammolarini hal qilishadi.</p><br><b>Imtiyozlar:</b><ul><li>$2000 gacha bo'lgan pul mukofotlari</li><li>Fortune500 loyihasi workshoplariga qatnashish imkoniyati</li><li>Xalqaro networking imkoniyati</li></ul>"
    },
    {
        "title": "KADEM International Entrepreneurship Bootcamp",
        "country": "Turkiya 🇹🇷",
        "format": "Oflayn",
        "age_category": "18-30",
        "deadline": "30-Avgust",
        "registration_link": "https://www.inovasyondakadin.org",
        "description": "<p>Ushbu lager dunyoning turli mamlakatlaridan kelgan ayol tadbirkorlarni bir joyga jamlaydi hamda ishtirokchilarga madaniyatlararo o‘quv muhiti, treninglar, soha mutaxassislari bilan yakka tartibdagi mentorlik sessiyalari va tajriba almashish uchrashuvlarini taqdim etadi.</p><br><b>Imtiyozlar:</b><ul><li>10 000 AQSH dollarigacha pul mukofoti</li><li>Soha ekspertlari bilan sessiyalar</li><li>Loyiha uchun investitsiya olish imkoniyati</li></ul>"
    }
]

# Clear existing just in case we are re-running
Opportunity.objects.all().delete()

for item in data:
    Opportunity.objects.create(**item)

print(f"Successfully seeded {len(data)} opportunities.")
