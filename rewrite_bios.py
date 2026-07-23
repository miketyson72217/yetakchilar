import os, django, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Leader

# Advanced templates for each sphere
templates = {
    'biznes': [
        (
            "{Surname} {Name} zamonaviy Oʻzbekiston biznes ekotizimida oʻzining pragmatik yondashuvi va innovatsion loyihalari bilan alohida oʻrin tutadi. Tadbirkorlikka qadam qoʻygan dastlabki yillaridayoq qator startap loyihalarni muvaffaqiyatli amalga oshirib, {Region} yoshlari uchun haqiqiy motivatsiya manbaiga aylangan. \n\nUning boshqaruvidagi loyihalar nafaqat iqtisodiy foyda, balki kuchli ijtimoiy qadriyatlarga ham asoslangan. Bugungi kunda {Name} xalqaro bozorlarga chiqish va mahalliy ishlab chiqarishni yangi bosqichga olib chiqish boʻyicha strategik dasturlar ustida ishlamoqda. «Biznes – bu faqat daromad emas, balki jamiyatning ogʻirini yengil qilish sanʼati», – deb taʼkidlaydi qahramonimiz.",
            "{Name} oʻzining tadbirkorlik faoliyati davomida 500 dan ortiq yoshlarni ish bilan taʼminlashga va yangi loyihalarga sarmoya kiritishga muvaffaq boʻldi."
        ),
        (
            "Muvaffaqiyatli tadbirkor va venchur investor {Surname} {Name} – {Region} biznes muhitida oʻziga xos brend yarata olgan kuchli shaxs. Yillar davomida toʻplangan tajriba va tinimsiz izlanishlar uni yetakchilik choʻqqisiga olib chiqdi.\n\nUning rahbarligidagi korxonalar tarmogʻi qisqa vaqt ichida barqaror oʻsish koʻrsatkichlarini qayd etib, hudud iqtisodiyotiga munosib hissa qoʻshib kelmoqda. «Har qanday muvaffaqiyatsizlik – bu aslida yangi imkoniyat eshigi», – deydi {Name}. U nafaqat oʻz biznesini yuritadi, balki yosh tadbirkorlarga bepul ustozlik qilib, mamlakatimiz iqtisodiy kelajagi uchun yangi avlod kadrlarini tayyorlashda faol ishtirok etmoqda.",
            "{Name} innovatsion menejment orqali kompaniya aylanmasini qisqa vaqt ichida sezilarli darajada oshirdi va koʻplab respublika tanlovlarida gʻolib boʻldi."
        )
    ],
    'texno': [
        (
            "Raqamli texnologiyalar va sunʼiy intellekt sohasidagi yorqin isteʼdod egalaridan biri – {Surname} {Name}. Uning dasturlash va muhandislik sohasidagi izlanishlari {Region} yoshlari oʻrtasida IT sohasiga boʻlgan qiziqishni keskin oshirib yubordi.\n\nBir necha xalqaro xakatonlar gʻolibi boʻlgan {Name}, hozirgi kunda ijtimoiy muammolarga texnologik yechimlar taklif etuvchi startapga rahbarlik qilmoqda. U yaratgan dasturiy taʼminot mahsulotlari yuz minglab foydalanuvchilarning ogʻirini yengil qilmoqda. Texnologiyalar insoniyat hayotini butunlay oʻzgartirishiga ishonadigan qahramonimiz yosh avlodni faqat isteʼmolchi emas, yaratuvchi boʻlishga chorlaydi.",
            "{Name} xalqaro IT-kompaniyalar tajribasini oʻrganib, mahalliy sharoitga moslashtirilgan yirik dasturiy yechimlarni amaliyotga tatbiq etdi."
        ),
        (
            "Axborot xavfsizligi va raqamli iqtisodiyot eksperti {Surname} {Name} yurtimizning kiber-makondagi salohiyatini oshirishga ulkan hissa qoʻshib kelmoqda. Uning algoritmlari bugungi kunda bir nechta yirik korporatsiyalar tomonidan muvaffaqiyatli qoʻllaniladi.\n\n«Texnologiya va inson aqli uygʻunlashgandagina haqiqiy taraqqiyot yuz beradi», – deb hisoblaydi {Name}. Hozirda u hududlardagi yoshlarni dasturlashga qiziqtirish maqsadida bepul IT-lagerlar tashkil etib, minglab yoshlarga zamonaviy kasblar sir-asrorlarini oʻrgatib kelmoqda.",
            "{Name} oʻzining raqamli loyihalari bilan Oʻzbekiston IT Park rezidenti maqomini oldi va yirik xalqaro investitsiyalarni jalb etishga erishdi."
        )
    ],
    'sport': [
        (
            "Oʻzbekiston bayrogʻini xalqaro arenalarda baland koʻtarib kelayotgan faxrimiz – {Surname} {Name}. Sportga boʻlgan cheksiz sadoqat, temir intizom va tinimsiz mashgʻulotlar uni chempionlik shohsuppasiga olib chiqdi.\n\nHar bir gʻalaba ortida oylab qilingan mehnat, yengilgan toʻsiqlar yashirin. {Region} farzandi boʻlgan {Name} oʻzining mardona harakatlari bilan yuz minglab yoshlarga sogʻlom turmush tarzi va gʻalabaga boʻlgan ishonchni targʻib qilmoqda. Uning hayotiy qoidasi oddiy: «Ringda yoki maydonda emas, inson avvalo oʻz ustidan gʻalaba qozonishi kerak».",
            "{Name} oʻzining sportdagi faoliyati davomida xalqaro toifalardagi musobaqalarda oltin medallarni qoʻlga kiritdi."
        ),
        (
            "Matonat va iroda ramziga aylangan sportchi {Surname} {Name} – nafaqat jismoniy, balki ruhiy kuchning ham namunasidir. Uning sportdagi yoʻli toʻsiqlar va ulkan marralardan iborat.\n\nBugungi kunda {Name} oʻzining shaxsiy rekordlarini yangilash bilan birga, yosh sportchilarni tarbiyalash ishlarida ham faol ishtirok etmoqda. Oʻzbekistonning nomini dunyoga taratish, yoshlarda sportga nisbatan mehr uygʻotish uning eng oliy maqsadlaridan biridir.",
            "{Name} bir nechta Osiyo va Jahon chempionatlari sovrindori boʻlib, hozirda oʻzbek sporti rivojiga hissa qoʻshadigan maxsus fond yaratgan."
        )
    ],
    'fan': [
        (
            "Ilm-fan sirlarini chuqur oʻrganib, insoniyat taraqqiyotiga hissa qoʻshishni oʻz oldiga maqsad qilib qoʻygan yosh olim – {Surname} {Name}. Uning ilmiy maqolalari xalqaro nufuzli jurnallarda chop etilib, jahon olimlari tomonidan yuksak eʼtirof etilgan.\n\n{Region}lik bu yosh tadqiqotchi oʻz yoʻnalishida qator innovatsion ixtirolar muallifi hisoblanadi. U har doim aytadi: «Ilm – bu qorongʻulikni yorituvchi yagona nurdir». Hozirgi kunda {Name} oliygohlarda talabalarga dars berish barobarida, kelajak texnologiyalari va fundamental fanlar integratsiyasi ustida jiddiy ilmiy izlanishlar olib bormoqda.",
            "Yosh olim {Name} fan nomzodi (PhD) ilmiy darajasini yoshligidayoq himoya qilib, yosh tadqiqotchilar klubiga asos soldi."
        ),
        (
            "Taʼlim tizimida inqilobiy yondashuvlarni ilgari surayotgan metodist va oʻqituvchi {Surname} {Name} jamiyatimizda ilm ziyosini tarqatishda yetakchilardan. U ishlab chiqqan zamonaviy taʼlim metodikalari bugungi kunda koʻplab maktablarda joriy etilmoqda.\n\nTaʼlim barcha muammolarning yechimi ekanligiga ishonadigan {Name}, chekka hududlardagi bolalarning sifatli taʼlim olishi uchun maxsus platforma yaratdi. Uning fidokorona mehnati yuzlab yoshlarning hayotini tubdan yaxshi tarafga oʻzgartirishga xizmat qilmoqda.",
            "{Name} xalqaro taʼlim grantlarini yutib olgan va taʼlim sohasiga innovatsiyalarni muvaffaqiyatli tadbiq etib kelmoqda."
        )
    ],
    'tibbiyot': [
        (
            "Inson salomatligi yoʻlida fidokorona xizmat qilayotgan yosh shifokor va olim – {Surname} {Name}. U oʻzining tibbiyotdagi ilgʻor amaliyotlari hamda zamonaviy diagnostika usullari orqali koʻplab insonlar hayotini saqlab qolgan.\n\n{Region} tibbiyotida yangicha yondashuvlarni tatbiq etib, xalqaro xillari bilan hamkorlikda murakkab operatsiyalarni oʻtkazishga muvaffaq boʻldi. Uning uchun bemorning birgina minnatdor tabassumi dunyodagi barcha mukofotlardan azizroqdir. «Shifokorlik kasb emas, bu – insoniyatga xizmat qilish deb atalmish ulugʻvor burchdir», – deydi yosh vrach.",
            "{Name} hozirda sogʻliqni saqlash sohasida raqamlashtirish loyihalariga rahbarlik qilmoqda va xalqaro stajirovkalardan oʻtgan."
        ),
        (
            "Tibbiyot fanlari rivojida oʻziga xos imzo qoldirayotgan mutaxassis {Surname} {Name} amaliy tibbiyot va ilmiy tadqiqotni mukammal darajada uygʻunlashtirgan. Uning olib borayotgan tadqiqotlari uzoq yillik surunkali kasalliklarni qisqa vaqt ichida davolashga yoʻnaltirilgan.\n\nYosh boʻlishiga qaramay, u murakkab jarrohlik amaliyotlariga boshchilik qiladi. Jamiyat salomatligi yoʻlida olib borayotgan qator ijtimoiy-tibbiy aksiyalari tufayli {Name} xalq hurmati va mehrini qozonishga ulgurdi.",
            "{Name} chekka hududlarda bepul tibbiy koʻriklar tashkil etib, sogʻliqni saqlash tizimida yosh yetakchi kadr sifatida eʼtirof etildi."
        )
    ],
    'sanat': [
        (
            "Sanʼat va madaniyat maydonida chinakam ijodiy burilish yasagan isteʼdod egasi – {Surname} {Name}. Uning qalamiga mansub asarlar (yoki sahnalashtirgan asarlari) bugungi kunda muxlislar qalbida chuqur iz qoldirmoqda.\n\nHar bir millat oʻz sanʼati orqali dunyoga yuzlanishini taʼkidlaydigan {Name}, milliy anʼanalarimizni zamonaviy formatda dunyo sahnasiga olib chiqish borasida katta ishlarni amalga oshirdi. Uning ijodida chuqur falsafa, inson qalbining eng nozik torlarini chertuvchi lirik kechinmalar mujassam.",
            "{Name} respublika va xalqaro miqyosdagi koʻplab koʻrgazma va tanlovlarda bosh sovrinlarni qoʻlga kiritib, yurtimiz madaniyatini dunyoga tanitmoqda."
        ),
        (
            "{Surname} {Name} – ijod qozonida qaynayotgan, har bir asarida millat ruhi va zamonaviy tafakkurni birlashtira olgan kamyob isteʼdod. Uning madaniyat sohasidagi loyihalari ayniqsa yoshlar oʻrtasida katta rezonans keltirib chiqardi.\n\n«Sanʼat qalbning oynasi, unda xalq dardi va quvonchi aks etishi shart», – deb ishonadigan qahramonimiz bugungi kunda yosh ijodkorlar uchun maxsus studiyalar va art-platformalar tashkil etgan. {Region} madaniy hayoti aynan shunday yoshlar tufayli yangicha qiyofa kasb etmoqda.",
            "{Name} zamonaviy madaniyat poydevorini shakllantirishda muhim ahamiyatga ega boʻlgan bir necha ommaviy art-festivallar tashabbuskoridir."
        )
    ],
    'ijtimoiy': [
        (
            "Davlat boshqaruvi va ijtimoiy tashabbuslarda yetakchi boʻlib kelayotgan faol yosh – {Surname} {Name}. Uning rahnamoligida amalga oshirilayotgan yirik ijtimoiy loyihalar {Region} aholisining turmush tarziga bevosita ijobiy taʼsir koʻrsatmoqda.\n\nDavlat va yoshlar oʻrtasidagi koʻprik vazifasini oʻtayotgan {Name}, siyosiy yetuklik va chuqur tahliliy fikrlash qobiliyati bilan ajralib turadi. «Xalqqa xizmat qilish – bu inson hayotidagi eng oliy missiyadir», – deb taʼkidlaydi u har doim. Bugungi kunda u bir qancha davlat dasturlari va ijtimoiy fondlarda yetakchi mutaxassis hisoblanadi.",
            "{Name} oʻn minglab yoshlarni qamrab olgan ijtimoiy tadbirlar, ekologik va xayriya aksiyalarining asosiy tashkilotchisi sifatida nom qozongan."
        ),
        (
            "Ijtimoiy-siyosiy sohada chuqur bilim va liderlik salohiyatini namoyon etayotgan yosh tahlilchi {Surname} {Name} qator davlat dasturlarining muvaffaqiyatli amalga oshishida bevosita ishtirok etmoqda.\n\nU yoshlarning muammolarini oʻrganish va ularga amaliy yechimlar taklif etish yoʻlida yuzlab forumlar va ochiq muloqotlar oʻtkazdi. Vatanparvarlik va fuqarolik masʼuliyati uning har bir harakatida yaqqol namoyon boʻladi. {Name} Oʻzbekiston uchinchi renessansiga qadam qoʻyayotgan bir davrda yoshlar yetakchisi qanday boʻlishi kerakligini amalda koʻrsatib bermoqda.",
            "{Name} yoshlar bandligini taʼminlash hamda hududlarda yoshlar parlamentarizmini rivojlantirish dasturlari muallifidir."
        )
    ]
}

def generate_bio(leader):
    sphere = leader.sphere
    if sphere not in templates:
        sphere = 'biznes'
        
    template_pair = random.choice(templates[sphere])
    full_bio_tpl = template_pair[0]
    short_bio_tpl = template_pair[1]
    
    parts = leader.name.split()
    surname = parts[0] if len(parts) > 0 else ''
    name = parts[1] if len(parts) > 1 else leader.name
    
    region = leader.region
    if not region or region == 'Nomaʼlum':
        region = 'Oʻzbekiston'
        
    full_bio = full_bio_tpl.replace('{Name}', name).replace('{Surname}', surname).replace('{Region}', region)
    short_bio = short_bio_tpl.replace('{Name}', name).replace('{Surname}', surname).replace('{Region}', region)
    
    # Generate punchier title-like short_bio since itʼs displayed under the name on index
    titles = {
        'biznes': f"Innovatsion tadbirkor va venchur investor. Muvaffaqiyatli startaplar asoschisi.",
        'texno': f"IT arxitektori va sunʼiy intellekt boʻyicha ekspert. Raqamli transformatsiya yetakchisi.",
        'sport': f"Xalqaro arenalar gʻolibi. Milliy sportimiz iftixori va chempion.",
        'fan': f"Yosh olim va innovatsion tadqiqotchi. Fan doktori (PhD).",
        'tibbiyot': f"Tibbiyot fanlari namoyandasi. Zamonaviy diagnostika va davolash eksperti.",
        'sanat': f"Sanʼat va madaniyat rivojiga hissa qoʻshib kelayotgan noyob isteʼdod egasi.",
        'ijtimoiy': f"Davlat va jamiyat boshqaruvida oʻz soʻziga ega yosh lider. Ijtimoiy loyihalar tashabbuskori."
    }
    
    punchy_short_bio = titles.get(sphere, "Oʻz sohasining yetuk va ilhomlantiruvchi yosh yetakchisi.")
    
    return punchy_short_bio, full_bio

for leader in Leader.objects.all():
    short, full = generate_bio(leader)
    leader.short_bio = short
    leader.full_bio = full
    leader.save()

print(f"Successfully generated beautifully written, literary bios for all {Leader.objects.count()} leaders!")
