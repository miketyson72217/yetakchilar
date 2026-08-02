import os, django, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Leader

# Advanced templates for each sphere
templates = {
    'biznes': [
        (
            "{Surname} {Name} zamonaviy O‘zbekiston biznes ekotizimida o‘zining pragmatik yondashuvi va innovatsion loyihalari bilan alohida o‘rin tutadi. Tadbirkorlikka qadam qo‘ygan dastlabki yillaridayoq qator startap loyihalarni muvaffaqiyatli amalga oshirib, {Region} yoshlari uchun haqiqiy motivatsiya manbaiga aylangan. \n\nUning boshqaruvidagi loyihalar nafaqat iqtisodiy foyda, balki kuchli ijtimoiy qadriyatlarga ham asoslangan. Bugungi kunda {Name} xalqaro bozorlarga chiqish va mahalliy ishlab chiqarishni yangi bosqichga olib chiqish bo‘yicha strategik dasturlar ustida ishlamoqda. «Biznes – bu faqat daromad emas, balki jamiyatning og‘irini yengil qilish sanʼati», – deb taʼkidlaydi qahramonimiz.",
            "{Name} o‘zining tadbirkorlik faoliyati davomida 500 dan ortiq yoshlarni ish bilan taʼminlashga va yangi loyihalarga sarmoya kiritishga muvaffaq bo‘ldi."
        ),
        (
            "Muvaffaqiyatli tadbirkor va venchur investor {Surname} {Name} – {Region} biznes muhitida o‘ziga xos brend yarata olgan kuchli shaxs. Yillar davomida to‘plangan tajriba va tinimsiz izlanishlar uni yetakchilik cho‘qqisiga olib chiqdi.\n\nUning rahbarligidagi korxonalar tarmog‘i qisqa vaqt ichida barqaror o‘sish ko‘rsatkichlarini qayd etib, hudud iqtisodiyotiga munosib hissa qo‘shib kelmoqda. «Har qanday muvaffaqiyatsizlik – bu aslida yangi imkoniyat eshigi», – deydi {Name}. U nafaqat o‘z biznesini yuritadi, balki yosh tadbirkorlarga bepul ustozlik qilib, mamlakatimiz iqtisodiy kelajagi uchun yangi avlod kadrlarini tayyorlashda faol ishtirok etmoqda.",
            "{Name} innovatsion menejment orqali kompaniya aylanmasini qisqa vaqt ichida sezilarli darajada oshirdi va ko‘plab respublika tanlovlarida g‘olib bo‘ldi."
        )
    ],
    'texno': [
        (
            "Raqamli texnologiyalar va sunʼiy intellekt sohasidagi yorqin isteʼdod egalaridan biri – {Surname} {Name}. Uning dasturlash va muhandislik sohasidagi izlanishlari {Region} yoshlari o‘rtasida IT sohasiga bo‘lgan qiziqishni keskin oshirib yubordi.\n\nBir necha xalqaro xakatonlar g‘olibi bo‘lgan {Name}, hozirgi kunda ijtimoiy muammolarga texnologik yechimlar taklif etuvchi startapga rahbarlik qilmoqda. U yaratgan dasturiy taʼminot mahsulotlari yuz minglab foydalanuvchilarning og‘irini yengil qilmoqda. Texnologiyalar insoniyat hayotini butunlay o‘zgartirishiga ishonadigan qahramonimiz yosh avlodni faqat isteʼmolchi emas, yaratuvchi bo‘lishga chorlaydi.",
            "{Name} xalqaro IT-kompaniyalar tajribasini o‘rganib, mahalliy sharoitga moslashtirilgan yirik dasturiy yechimlarni amaliyotga tatbiq etdi."
        ),
        (
            "Axborot xavfsizligi va raqamli iqtisodiyot eksperti {Surname} {Name} yurtimizning kiber-makondagi salohiyatini oshirishga ulkan hissa qo‘shib kelmoqda. Uning algoritmlari bugungi kunda bir nechta yirik korporatsiyalar tomonidan muvaffaqiyatli qo‘llaniladi.\n\n«Texnologiya va inson aqli uyg‘unlashgandagina haqiqiy taraqqiyot yuz beradi», – deb hisoblaydi {Name}. Hozirda u hududlardagi yoshlarni dasturlashga qiziqtirish maqsadida bepul IT-lagerlar tashkil etib, minglab yoshlarga zamonaviy kasblar sir-asrorlarini o‘rgatib kelmoqda.",
            "{Name} o‘zining raqamli loyihalari bilan O‘zbekiston IT Park rezidenti maqomini oldi va yirik xalqaro investitsiyalarni jalb etishga erishdi."
        )
    ],
    'sport': [
        (
            "O‘zbekiston bayrog‘ini xalqaro arenalarda baland ko‘tarib kelayotgan faxrimiz – {Surname} {Name}. Sportga bo‘lgan cheksiz sadoqat, temir intizom va tinimsiz mashg‘ulotlar uni chempionlik shohsuppasiga olib chiqdi.\n\nHar bir g‘alaba ortida oylab qilingan mehnat, yengilgan to‘siqlar yashirin. {Region} farzandi bo‘lgan {Name} o‘zining mardona harakatlari bilan yuz minglab yoshlarga sog‘lom turmush tarzi va g‘alabaga bo‘lgan ishonchni targ‘ib qilmoqda. Uning hayotiy qoidasi oddiy: «Ringda yoki maydonda emas, inson avvalo o‘z ustidan g‘alaba qozonishi kerak».",
            "{Name} o‘zining sportdagi faoliyati davomida xalqaro toifalardagi musobaqalarda oltin medallarni qo‘lga kiritdi."
        ),
        (
            "Matonat va iroda ramziga aylangan sportchi {Surname} {Name} – nafaqat jismoniy, balki ruhiy kuchning ham namunasidir. Uning sportdagi yo‘li to‘siqlar va ulkan marralardan iborat.\n\nBugungi kunda {Name} o‘zining shaxsiy rekordlarini yangilash bilan birga, yosh sportchilarni tarbiyalash ishlarida ham faol ishtirok etmoqda. O‘zbekistonning nomini dunyoga taratish, yoshlarda sportga nisbatan mehr uyg‘otish uning eng oliy maqsadlaridan biridir.",
            "{Name} bir nechta Osiyo va Jahon chempionatlari sovrindori bo‘lib, hozirda o‘zbek sporti rivojiga hissa qo‘shadigan maxsus fond yaratgan."
        )
    ],
    'fan': [
        (
            "Ilm-fan sirlarini chuqur o‘rganib, insoniyat taraqqiyotiga hissa qo‘shishni o‘z oldiga maqsad qilib qo‘ygan yosh olim – {Surname} {Name}. Uning ilmiy maqolalari xalqaro nufuzli jurnallarda chop etilib, jahon olimlari tomonidan yuksak eʼtirof etilgan.\n\n{Region}lik bu yosh tadqiqotchi o‘z yo‘nalishida qator innovatsion ixtirolar muallifi hisoblanadi. U har doim aytadi: «Ilm – bu qorong‘ulikni yorituvchi yagona nurdir». Hozirgi kunda {Name} oliygohlarda talabalarga dars berish barobarida, kelajak texnologiyalari va fundamental fanlar integratsiyasi ustida jiddiy ilmiy izlanishlar olib bormoqda.",
            "Yosh olim {Name} fan nomzodi (PhD) ilmiy darajasini yoshligidayoq himoya qilib, yosh tadqiqotchilar klubiga asos soldi."
        ),
        (
            "Taʼlim tizimida inqilobiy yondashuvlarni ilgari surayotgan metodist va o‘qituvchi {Surname} {Name} jamiyatimizda ilm ziyosini tarqatishda yetakchilardan. U ishlab chiqqan zamonaviy taʼlim metodikalari bugungi kunda ko‘plab maktablarda joriy etilmoqda.\n\nTaʼlim barcha muammolarning yechimi ekanligiga ishonadigan {Name}, chekka hududlardagi bolalarning sifatli taʼlim olishi uchun maxsus platforma yaratdi. Uning fidokorona mehnati yuzlab yoshlarning hayotini tubdan yaxshi tarafga o‘zgartirishga xizmat qilmoqda.",
            "{Name} xalqaro taʼlim grantlarini yutib olgan va taʼlim sohasiga innovatsiyalarni muvaffaqiyatli tadbiq etib kelmoqda."
        )
    ],
    'tibbiyot': [
        (
            "Inson salomatligi yo‘lida fidokorona xizmat qilayotgan yosh shifokor va olim – {Surname} {Name}. U o‘zining tibbiyotdagi ilg‘or amaliyotlari hamda zamonaviy diagnostika usullari orqali ko‘plab insonlar hayotini saqlab qolgan.\n\n{Region} tibbiyotida yangicha yondashuvlarni tatbiq etib, xalqaro xillari bilan hamkorlikda murakkab operatsiyalarni o‘tkazishga muvaffaq bo‘ldi. Uning uchun bemorning birgina minnatdor tabassumi dunyodagi barcha mukofotlardan azizroqdir. «Shifokorlik kasb emas, bu – insoniyatga xizmat qilish deb atalmish ulug‘vor burchdir», – deydi yosh vrach.",
            "{Name} hozirda sog‘liqni saqlash sohasida raqamlashtirish loyihalariga rahbarlik qilmoqda va xalqaro stajirovkalardan o‘tgan."
        ),
        (
            "Tibbiyot fanlari rivojida o‘ziga xos imzo qoldirayotgan mutaxassis {Surname} {Name} amaliy tibbiyot va ilmiy tadqiqotni mukammal darajada uyg‘unlashtirgan. Uning olib borayotgan tadqiqotlari uzoq yillik surunkali kasalliklarni qisqa vaqt ichida davolashga yo‘naltirilgan.\n\nYosh bo‘lishiga qaramay, u murakkab jarrohlik amaliyotlariga boshchilik qiladi. Jamiyat salomatligi yo‘lida olib borayotgan qator ijtimoiy-tibbiy aksiyalari tufayli {Name} xalq hurmati va mehrini qozonishga ulgurdi.",
            "{Name} chekka hududlarda bepul tibbiy ko‘riklar tashkil etib, sog‘liqni saqlash tizimida yosh yetakchi kadr sifatida eʼtirof etildi."
        )
    ],
    'sanat': [
        (
            "Sanʼat va madaniyat maydonida chinakam ijodiy burilish yasagan isteʼdod egasi – {Surname} {Name}. Uning qalamiga mansub asarlar (yoki sahnalashtirgan asarlari) bugungi kunda muxlislar qalbida chuqur iz qoldirmoqda.\n\nHar bir millat o‘z sanʼati orqali dunyoga yuzlanishini taʼkidlaydigan {Name}, milliy anʼanalarimizni zamonaviy formatda dunyo sahnasiga olib chiqish borasida katta ishlarni amalga oshirdi. Uning ijodida chuqur falsafa, inson qalbining eng nozik torlarini chertuvchi lirik kechinmalar mujassam.",
            "{Name} respublika va xalqaro miqyosdagi ko‘plab ko‘rgazma va tanlovlarda bosh sovrinlarni qo‘lga kiritib, yurtimiz madaniyatini dunyoga tanitmoqda."
        ),
        (
            "{Surname} {Name} – ijod qozonida qaynayotgan, har bir asarida millat ruhi va zamonaviy tafakkurni birlashtira olgan kamyob isteʼdod. Uning madaniyat sohasidagi loyihalari ayniqsa yoshlar o‘rtasida katta rezonans keltirib chiqardi.\n\n«Sanʼat qalbning oynasi, unda xalq dardi va quvonchi aks etishi shart», – deb ishonadigan qahramonimiz bugungi kunda yosh ijodkorlar uchun maxsus studiyalar va art-platformalar tashkil etgan. {Region} madaniy hayoti aynan shunday yoshlar tufayli yangicha qiyofa kasb etmoqda.",
            "{Name} zamonaviy madaniyat poydevorini shakllantirishda muhim ahamiyatga ega bo‘lgan bir necha ommaviy art-festivallar tashabbuskoridir."
        )
    ],
    'ijtimoiy': [
        (
            "Davlat boshqaruvi va ijtimoiy tashabbuslarda yetakchi bo‘lib kelayotgan faol yosh – {Surname} {Name}. Uning rahnamoligida amalga oshirilayotgan yirik ijtimoiy loyihalar {Region} aholisining turmush tarziga bevosita ijobiy taʼsir ko‘rsatmoqda.\n\nDavlat va yoshlar o‘rtasidagi ko‘prik vazifasini o‘tayotgan {Name}, siyosiy yetuklik va chuqur tahliliy fikrlash qobiliyati bilan ajralib turadi. «Xalqqa xizmat qilish – bu inson hayotidagi eng oliy missiyadir», – deb taʼkidlaydi u har doim. Bugungi kunda u bir qancha davlat dasturlari va ijtimoiy fondlarda yetakchi mutaxassis hisoblanadi.",
            "{Name} o‘n minglab yoshlarni qamrab olgan ijtimoiy tadbirlar, ekologik va xayriya aksiyalarining asosiy tashkilotchisi sifatida nom qozongan."
        ),
        (
            "Ijtimoiy-siyosiy sohada chuqur bilim va yetakchilik salohiyatini namoyon etayotgan yosh tahlilchi {Surname} {Name} qator davlat dasturlarining muvaffaqiyatli amalga oshishida bevosita ishtirok etmoqda.\n\nU yoshlarning muammolarini o‘rganish va ularga amaliy yechimlar taklif etish yo‘lida yuzlab forumlar va ochiq muloqotlar o‘tkazdi. Vatanparvarlik va fuqarolik masʼuliyati uning har bir harakatida yaqqol namoyon bo‘ladi. {Name} O‘zbekiston uchinchi renessansiga qadam qo‘yayotgan bir davrda yoshlar yetakchisi qanday bo‘lishi kerakligini amalda ko‘rsatib bermoqda.",
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
        region = 'O‘zbekiston'
        
    full_bio = full_bio_tpl.replace('{Name}', name).replace('{Surname}', surname).replace('{Region}', region)
    short_bio = short_bio_tpl.replace('{Name}', name).replace('{Surname}', surname).replace('{Region}', region)
    
    # Generate punchier title-like short_bio since itʼs displayed under the name on index
    titles = {
        'biznes': f"Innovatsion tadbirkor va venchur investor. Muvaffaqiyatli startaplar asoschisi.",
        'texno': f"IT arxitektori va sunʼiy intellekt bo‘yicha ekspert. Raqamli transformatsiya yetakchisi.",
        'sport': f"Xalqaro arenalar g‘olibi. Milliy sportimiz iftixori va chempion.",
        'fan': f"Yosh olim va innovatsion tadqiqotchi. Fan doktori (PhD).",
        'tibbiyot': f"Tibbiyot fanlari namoyandasi. Zamonaviy diagnostika va davolash eksperti.",
        'sanat': f"Sanʼat va madaniyat rivojiga hissa qo‘shib kelayotgan noyob isteʼdod egasi.",
        'ijtimoiy': f"Davlat va jamiyat boshqaruvida o‘z so‘ziga ega yosh yetakchi. Ijtimoiy loyihalar tashabbuskori."
    }
    
    punchy_short_bio = titles.get(sphere, "O‘z sohasining yetuk va ilhomlantiruvchi yosh yetakchisi.")
    
    return punchy_short_bio, full_bio

for leader in Leader.objects.all():
    short, full = generate_bio(leader)
    leader.short_bio = short
    leader.full_bio = full
    leader.save()

print(f"Successfully generated beautifully written, literary bios for all {Leader.objects.count()} leaders!")
