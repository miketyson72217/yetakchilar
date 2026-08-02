import os
import random
import django
from PIL import Image, ImageDraw, ImageFont
import boto3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Leader

# Ensure directories exist
os.makedirs('/home/lochinbek/Desktop/yetakchilar/media/leaders', exist_ok=True)
os.makedirs('/home/lochinbek/Desktop/yetakchilar/media/leaders/quotes', exist_ok=True)

# S3 Client
s3 = boto3.client(
    's3',
    endpoint_url=os.environ.get('AWS_S3_ENDPOINT_URL', 'https://s3.eu-central-1.idrivee2.com'),
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', '0faMQEqc9bxwxKvimBjk'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', 'xXBvzltnMsAJJvl7o2L9CKPfL40i1jbjFlJgNJtJ'),
    region_name=os.environ.get('AWS_S3_REGION_NAME', 'eu-central-1')
)
bucket_name = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'media')

# Palette colors for posters & portraits
GRADIENTS = [
    ('#0f172a', '#1e293b', '#0284c7', '#38bdf8'),
    ('#111827', '#1f2937', '#059669', '#34d399'),
    ('#1e1b4b', '#312e81', '#7c3aed', '#a78bfa'),
    ('#31121d', '#4c1d24', '#e11d48', '#fb7185'),
    ('#042f2e', '#134e4a', '#0d9488', '#2dd4bf'),
    ('#172554', '#1e3a8a', '#2563eb', '#60a5fa'),
    ('#2e1065', '#3b0764', '#9333ea', '#c084fc'),
]

SPHERES = ['biznes', 'texno', 'sport', 'fan', 'sanat', 'tibbiyot', 'ijtimoiy']
REGIONS = [
    'Toshkent', 'Samarqand', 'Farg‘ona', 'Namangan', 'Andijon',
    'Buxoro', 'Xorazm', 'Qashqadaryo', 'Surxondaryo', 'Sirdaryo',
    'Jizzax', 'Navoiy', 'Qoraqalpog‘iston', 'Toshkent viloyati'
]

# 45 Unique Leaders Data
RAW_LEADERS = [
    ("Kamalova Maftuna Zoxirovna", "biznes", "Buxoro", "F", "Mehmonxona menejmentida yetakchi mutaxassis", "Vatel Hotel Management bitiruvchisi, Kaizen sertifikati va Karuta Taikai Respublika g‘olibi.", "1-oktabr 1999-yil", "Buxoro shahri", "Oliy (Vatel Hotel Management)", "Muvaffaqiyat — bu tasodif emas, balki har kuni qilinadigan to‘g‘ri tanlovlar natijasidir."),
    ("Yusupova Malika Rustamovna", "biznes", "Toshkent", "F", "Xalqaro Startap Asoschisi & CEO", "100 dan ortiq yoshlarga ustozlik qilgan va yashil texnologiyalar startapini yo‘lga qo‘ygan biznes yetakchisi.", "15-may 1998-yil", "Toshkent shahri", "Oliy (Westminster University)", "Haqiqiy rahbar o‘z jamoasining imkoniyatlariga ishonch bag‘ishlaydi."),
    ("Alimov Javohir Otabekovich", "texno", "Samarqand", "M", "Sunʼiy Intellekt Innovatori & Engineer", "AI platformalari muallifi, xalqaro hackathonlar 1-o‘rin sohibi va IT ekotizim tashabbuskori.", "10-iyun 2000-yil", "Samarqand shahri", "Oliy (INHA University)", "Texnologiya — bu faqat vosita. Asosiy kuch — insonning ijodiy tafakkurida."),
    ("Karimova Zebo Bobur qizi", "sport", "Toshkent", "F", "Olimpiya Chempioni & Sport Ustasi", "Xalqaro musobaqalar oltin medali egasi hamda yosh sportchilarni qo‘llab-quvvatlash jamg‘armasi asoschisi.", "22-avgust 2001-yil", "Toshkent shahri", "Oliy (Jismoniy Tarbiya Instituti)", "Har bir mag‘lubiyat — bu yanada kuchliroq bo‘lib qaytish uchun imkoniyatdir."),
    ("Ismoilov Said Anvarovich", "biznes", "Buxoro", "M", "Venchur Investitsiyalar Mutaxassisi", "Yashil energetika va ekologik startaplarni moliyalashtiruvchi fond boshqaruvchisi.", "5-fevral 1997-yil", "Buxoro shahri", "Oliy (TDIU)", "Kelajakka kiritilgan eng yaxshi investitsiya — bu bilim va yoshlar rivojidir."),
    ("Umarova Dilnoza Sherzodovna", "tibbiyot", "Namangan", "F", "Genom Tadqiqotchisi & Tibbiyot Olima", "Tibbiyot fanlari bo‘yicha izlanuvchi, biokimyoviy innovatsiyalar muallifi.", "12-noyabr 1996-yil", "Namangan shahri", "Oliy (Toshkent Tibbiyot Akademiyasi)", "Inson salomatligi va baxti — biz intiladigan eng oliy maqsaddir."),
    ("Rahimov Jasur Bahodirovich", "texno", "Farg‘ona", "M", "Cybersecurity & Cloud Systems Lead", "Kiberxavfsizlik eksperti, bulutli infratuzilmalarni himoya qilish tizimlari ishlab chiquvchisi.", "18-sentabr 1999-yil", "Farg‘ona shahri", "Oliy (TATU)", "Raqamli dunyoda xavfsizlik — bu har bir tizimning poydevoridir."),
    ("Nazarova Rayhona Shavkatovna", "sanat", "Xorazm", "F", "Xalqaro Dizayner & Art Director", "Zamonaviy etno-dizayn yo‘nalishi vakili, Parij va Milan moda haftaliklari qatnashchisi.", "4-aprel 2002-yil", "Xiva shahri", "Oliy (Milliy Rassomlik va Dizayn Instituti)", "Sanʼat — bu millat ruhining zamonaviy shaklda namoyon bo‘lishidir."),
    ("Rustamov Azizbek Akmalovich", "fan", "Toshkent", "M", "Kvant Fizikasi Bo‘yicha Geniy Olim", "Xalqaro fizika olimpiadalari g‘olibi, kvant hisoblash sohasida maqolalar muallifi.", "29-yanvar 2001-yil", "Toshkent shahri", "Oliy (O‘zMU)", "Ilm-fan chegaralari faqat bizning tasavvurimiz bilan belgilanadi."),
    ("Qosimova Nigora Murod qizi", "ijtimoiy", "Qashqadaryo", "F", "Volontyorlik Harakati Yetakchisi", "10,000 dan ortiq ehtiyojmand oilalarga manzilli yordam bergan xayriya loyihasi rahbari.", "8-mart 2000-yil", "Qarshi shahri", "Oliy (Jahon Tillari Universiteti)", "Kichik bir ezgu amal butun jamiyat hayotini o‘zgartirishi mumkin."),
    ("Tursunov Sardor Ilhomovich", "biznes", "Andijon", "M", "Agrotexkonologiya & FinTech Asoschisi", "Qishloq xo‘jaligida tomchilatib sug‘orish intellektual tizimlarini joriy etgan tadbirkor.", "11-iyul 1997-yil", "Andijon shahri", "Oliy (Toshkent Agrotexnologiyalar Universiteti)", "Zamonaviy dehqonchilik va texnologiya — oziq-ovqat xavfsizligining garovidir."),
    ("Azimova Madinabonu Botirovna", "sanat", "Samarqand", "F", "Simfonik Orkestr Dirijyori & Kompozitor", "Xalqaro kompozitorlar tanlovi sovrindori, milliy va mumtoz kuylar targ‘ibotchisi.", "19-dekabr 1998-yil", "Samarqand shahri", "Oliy (O‘zbekiston Davlat Konservatoriyasi)", "Musiqa — qalbning eng samimiy va sheʼriy tilidir."),
    ("Xolmatov Elbek Sheraliyevich", "texno", "Toshkent", "M", "Robotics & Automation Specialist", "Sanoat robototexnikasi loyihalari muallifi, xalqaro robototexnika kubogi g‘olibi.", "23-oktabr 2001-yil", "Toshkent shahri", "Oliy (Turin Politexnika Universiteti)", "Kelajak kelmaydi, kelajakni biz o‘z qo‘llarimiz bilan yasaymiz."),
    ("Sharipova Shahnoza Erkinovna", "tibbiyot", "Toshkent viloyati", "F", "Neyroxirurg & Tibbiyot Innovatori", "Kam invasiv neyroxirurgiya amaliyotlarini muvaffaqiyatli o‘tkazayotgan yosh jarroh.", "30-avgust 1995-yil", "Chirchiq shahri", "Oliy (Toshkent Pediatriya Tibbiyot Instituti)", "Har bir saqlab qolingan hayot — bu eng buyuk g‘alabadir."),
    ("Abdullayev Jamshid Alisherovich", "sport", "Surxondaryo", "M", "Dzyudo Bo‘yicha Jahon Chempioni", "Xalqaro turnirlar oltin medali sohibi, Surxondaryoda sport maktabi asoschisi.", "14-fevral 1999-yil", "Termiz shahri", "Oliy (Jismoniy Tarbiya Universiteti)", "Haqiqiy chempion gilamda emas, mashg‘ulotlarda yetishib chiqadi."),
    ("Soliheva Yulduz Husniddin qizi", "fan", "Navoiy", "F", "Kimyo-Texnologiya Bo‘yicha Izlanuvchi", "Yashil kimyo va polimer materiallar sohasidagi patentlar muallifi.", "2-may 2000-yil", "Navoiy shahri", "Oliy (Navoiy Davlat Konchilik Instituti)", "Tabiat qonunlarini o‘rganish — kelajak texnologiyalarining kalitidir."),
    ("Murodov Nodirbek Mansurovich", "biznes", "Jizzax", "M", "Logistika va E-Commerce Eksperti", "O‘zbekistondagi yirik ekspress-yetkazib berish platformasi hammuassisi.", "17-aprel 1998-yil", "Jizzax shahri", "Oliy (Toshkent Avtomobil Yo‘llari Instituti)", "Muvaffaqiyatli biznes — mijozga tez va sifatli xizmat ko‘rsatishdan boshlanadi."),
    ("Oripova Sevinch Farhodovna", "ijtimoiy", "Sirdaryo", "F", "Inkluziv Taʼlim & Eco-Activist", "Imkoniyati cheklangan yoshlar uchun raqamli ko‘nikmalar markazi rahbari.", "25-noyabr 2001-yil", "Guliston shahri", "Oliy (Guliston Davlat Universiteti)", "Teng imkoniyatlar yaratish — bu adolatli jamiyat qurishning asosidir."),
    ("Hamroyev Temur Mansurovich", "texno", "Buxoro", "M", "Game Development & 3D Artist", "Xalqaro o‘yin kompaniyalari bilan hamkorlik qilayotgan 3D grafika va o‘yinlar muallifi.", "7-iyul 2002-yil", "Buxoro shahri", "Oliy (TATU Buxoro filiali)", "Tasavvur kuchi va kod birlashganda mo‘jizalar yaratiladi."),
    ("Sodiqova Gulsanam Ulug‘bek qizi", "tibbiyot", "Andijon", "F", "Farmatsevtika & Biotexnologiya", "Tabiiy giyohlardan yangi preparatlar yaratayotgan yosh olima.", "16-sentyabr 1997-yil", "Andijon shahri", "Oliy (Toshkent Farmatsevtika Instituti)", "Tabiatda har bir dardning darmoni yashiringan."),
    ("Mansurov Behruz Rustamovich", "biznes", "Toshkent", "M", "Real Estate & Architecture Developer", "Zamonaviy ekologik bino loyihalari va shaharsozlik innovatsiyalari rahbari.", "9-yanvar 1996-yil", "Toshkent shahri", "Oliy (Toshkent Arxitektura Qurilish Instituti)", "Biz qurayotgan binolar kelajak avlodlarga meros bo‘lib qoladi."),
    ("Jalilova Kamola Ilhomovna", "sanat", "Qoraqalpog‘iston", "F", "Etnografik Liboslar Dizayneri", "Qoraqalpoq milliy bezaklarini zamonaviy uslubga tatbiq etayotgan dizayner.", "13-may 2000-yil", "Nukus shahri", "Oliy (Nukus Davlat Sanʼat Instituti)", "Milliy qadriyatlarimiz — ilhomimizning tuganmas manbaidir."),
    ("Boboyev Bekzod Olimovich", "sport", "Samarqand", "M", "Shaxmat Bo‘yicha Xalqaro Grossmeyster", "Xalqaro shaxmat turnirlari g‘olibi, intellektual shaxmat akademiyasi ustozi.", "21-oktabr 2003-yil", "Samarqand shahri", "Oliy (SamDU)", "Shaxmat taxtasidagi kabi hayotda ham har bir yurish masʼuliyat talab qiladi."),
    ("Eshonqulova Zilola Akramovna", "fan", "Farg‘ona", "F", "Filologiya & Tarjimashunoslik Olimasi", "O‘zbek adabiyoti durdonalarini ingliz va fransuz tillariga o‘girgan tarjimon.", "3-iyun 1999-yil", "Qo‘qon shahri", "Oliy (Farg‘ona Davlat Universiteti)", "Til — bu xalqlar o‘rtasidagi eng mustahkam va ko‘rinmas ko‘prikdir."),
    ("Mirzayev Otabek Shuhratovich", "texno", "Toshkent", "M", "Blockchain & Web3 Architect", "Xavfsiz blokcheyn protokollari va kripto-infratuzilmalar bo‘yicha muhandis.", "28-noyabr 1997-yil", "Toshkent shahri", "Oliy (Westminster University)", "Raqamli ishonch va shaffoflik — bu yangi iqtisodiyot kalitidir."),
    ("Akramova Munisa Farruxovna", "ijtimoiy", "Toshkent", "F", "Yoshlar Siyosati & Ekologiya Harakati", "O‘zbekistonda plastiksiz kelajak ekologik aksiyasi tashabbuskori.", "17-avgust 2002-yil", "Toshkent shahri", "Oliy (Jahon Iqtisodiyoti va Diplomatiya Universiteti)", "Biz Yerni ota-onalarimizdan meros olmadik, uni farzandlarimizdan qarzga oldik."),
    ("Rahmatullayev Dostonbek Komilovich", "biznes", "Namangan", "M", "Tekstil va Tikuvchilik Klasteri CEO", "1500 dan ortiq xotin-qizlarni ish bilan taʼminlagan eksportyor tadbirkor.", "24-dekabr 1995-yil", "Namangan shahri", "Oliy (Namangan Muhandislik Instituti)", "Mehnat va halollik — doimiy va barqaror muvaffaqiyat garovidir."),
    ("Qurbonova Dilnavoz Alisher qizi", "sanat", "Buxoro", "F", "Miniatura va Xattotlik Ustozi", "Buxoro miniatyura maktabini qayta tiklayotgan va xalqaro ko‘rgazmalar g‘olibi.", "6-iyul 2001-yil", "Buxoro shahri", "Oliy (Buxoro Davlat Universiteti)", "Sanʼatda har bir chiziq va rang inson ruhining aksidir."),
    ("Yusupov Shohruhbek Akramovich", "tibbiyot", "Samarqand", "M", "Kardiolog & Sunʼiy Yurak Tizimlari", "Yurak-qon tomir kasalliklarini barvaqt aniqlash bo‘yicha startap asoschisi.", "19-sentyabr 1996-yil", "Samarqand shahri", "Oliy (Samarqand Tibbiyot Universiteti)", "Urayotgan har bir yurak — bizga bildirilgan yuksak ishonchdir."),
    ("Hasanova Shahzoda Baxtiyor qizi", "sport", "Toshkent", "F", "Badiiy Gimnastika Bo‘yicha Chempion", "Jahon kubogi sovrindori, yosh gimnastikachilar murabbiyi.", "12-fevral 2002-yil", "Toshkent shahri", "Oliy (Jismoniy Tarbiya Instituti)", "G‘alaba ortida minglab soatlik sabr va tinimsiz mehnat yotadi."),
    ("Qodirov Sherzod Zokirovich", "texno", "Navoiy", "M", "IoT va Smart City Infratuzilmasi", "Aqlli shahar texnologiyalari va svetoforlar boshqaruvi tizimlari muallifi.", "8-oktabr 1998-yil", "Navoiy shahri", "Oliy (TATU)", "Aqlli shaharlar — insonlar vaqtini va resurslarini tejaydi."),
    ("Tohirova Mohinur Rustamovna", "fan", "Toshkent viloyati", "F", "Astrofizik va Kosmik Tadqiqotchi", "O‘zbekistonda birinchi kosmik nanosum sunʼiy yo‘ldoshi loyihasi ishtirokchisi.", "27-aprel 2000-yil", "Olmaliq shahri", "Oliy (O‘zMU)", "Koinotni o‘rganish — insoniyatning o‘z kelajagini tushunishidir."),
    ("Inoyatov Anvarbek Sobirovich", "biznes", "Xorazm", "M", "Agroturizm va Eko-Hotel Asoschisi", "Qadimgi Xiva uslubidagi yashil eko-mehmonxonalar tarmog‘i tadbirkori.", "5-avgust 1997-yil", "Urganch shahri", "Oliy (Urganch Davlat Universiteti)", "Turizm — bu milliy madaniyatimizni dunyoga ko‘rsatish imkoniyatidir."),
    ("Bo‘riyeva Nargiza Otabek qizi", "ijtimoiy", "Qashqadaryo", "F", "Qishloq Qizlari Taʼlimi Tashabbuskori", "Olis qishloqlardagi 5000 dan ortiq qizlarga IT va ingliz tili darslarini tashkil etgan.", "14-noyabr 2001-yil", "Shahrisabz shahri", "Oliy (Toshkent Davlat Pedagogika Universiteti)", "Bir qizni o‘qitsangiz — butun bir oilani va jamiyatni o‘qitgan bo‘lasiz."),
    ("Xolmurodov Doniyor Sunnatovich", "sanat", "Toshkent", "M", "Kino Rejissyor va Hujjatli Film Ustasi", "Xalqaro kinofestivallar g‘olibi, O‘zbekiston yoshlari haqidagi filmlar rejissyori.", "22-iyun 1999-yil", "Toshkent shahri", "Oliy (O‘zbekiston Davlat Sanʼat va Madaniyat Instituti)", "Kino — bu insonlar qalbiga yetib boruvchi eng kuchli til."),
    ("Salimov Umidjon Dilshodovich", "sport", "Andijon", "M", "Boks Bo‘yicha Osiyo Chempioni", "Xalqaro turnirlarda O‘zbekiston bayrog‘ini baland ko‘targan charm qo‘lqop ustasi.", "31-oktabr 2000-yil", "Andijon shahri", "Oliy (Andijon Davlat Universiteti)", "Ringda ham, hayotda ham eng muhimi — taslim bo‘lmaslikdir."),
    ("Usmonova Asalxon Jasur qizi", "texno", "Samarqand", "F", "UX/UI & Product Design Lead", "Xalqaro ilovalar dizayneri, qulay va chiroyli raqamli mahsulotlar muallifi.", "18-may 2002-yil", "Samarqand shahri", "Oliy (TATU Samarqand filiali)", "Dizayn — bu faqat chiroyli ko‘rinish emas, bu qanday ishlashidir."),
    ("Karimov Murodjon Anvarovich", "tibbiyot", "Toshkent", "M", "Stomatolog-Implantolog Innovator", "3D bosma stomatologik implantlar va raqamli tabassum dizayni mutaxassisi.", "9-mart 1996-yil", "Toshkent shahri", "Oliy (Toshkent Davlat Stomatologiya Instituti)", "Har bir insonning samimiy tabassumi — dunyoni yanada go‘zal qiladi."),
    ("Rahmatova Nigora Sobir qizi", "fan", "Buxoro", "F", "Botanika va Ekologiya Fanlari Doktori", "O‘zbekistondagi noyob o‘simliklar genofondini saqlash bo‘yicha izlanuvchi.", "20-sentabr 1998-yil", "Buxoro shahri", "Oliy (Buxoro Davlat Universiteti)", "O‘simliklar dunyosini asrash — yer yuzida hayotni asrash demakdir."),
    ("Abduqodirov Abrorali Dilshodovich", "biznes", "Farg‘ona", "M", "Eko-Qadoqlash va Qayta Ishlash CEO", "Plastik o‘rnini bosuvchi bioparchalanuvchi qadoqlash korxonasi tadbirkori.", "13-avgust 1997-yil", "Marg‘ilon shahri", "Oliy (Farg‘ona Politexnika Instituti)", "Atrof-muhitni asrash — har bir tadbirkorning ijtimoiy burchidir."),
    ("G‘ofurova Sevara Mansur qizi", "ijtimoiy", "Toshkent", "F", "Psixolog & Yoshlar Mentori", "O‘smirlar ruhiy salomatligi va kasbga yo‘naltirish bo‘yicha markaz rahbari.", "2-oktabr 2000-yil", "Toshkent shahri", "Oliy (O‘zMU)", "O‘zligini anglagan va o‘ziga ishongan inson har qanday cho‘qqini egallaydi."),
    ("Ismatov Umidbek Farhodovich", "sport", "Xorazm", "M", "Yengil Atletika & Maratonchi", "Xalqaro marafonlar g‘olibi, sog‘lom turmush tarzi targ‘ibotchisi.", "15-yanvar 1999-yil", "Urganch shahri", "Oliy (Urganch Davlat Universiteti)", "Har bir bosilgan qadam — marraga eltuvchi masofani qisqartiradi."),
    ("Sulaymonova Diyora Ulug‘bek qizi", "sanat", "Toshkent", "F", "Teatr Aktrisasi & Boshlovchi", "Davlat teatri aktrisasi, bir necha nufuzli sahna asarlari bosh rol ijrochisi.", "26-iyun 2001-yil", "Toshkent shahri", "Oliy (Sanʼat va Madaniyat Instituti)", "Sahna — bu haqiqat va samimiyat sinovdan o‘tadigan muqaddas maskandir."),
    ("Yoqubov Sherali Bahromovich", "texno", "Toshkent viloyati", "M", "Data Science & Big Analytics Lead", "Katta maʼlumotlarni tahlil qilish va prognozlash modellarini yaratuvchi analitik.", "4-noyabr 1997-yil", "Angren shahri", "Oliy (TUIT)", "Maʼlumotlar — bu yangi davrning eng qimmatli xomashyosidir."),
    ("Toshpulatov Boburmirzo Alisherovich", "fan", "Samarqand", "M", "Tarix va Arxeologiya Tadqiqotchisi", "Buyuk Ipak yo‘li yodgorliklarini o‘rganayotgan yosh arxeolog olim.", "10-avgust 1998-yil", "Samarqand shahri", "Oliy (SamDU)", "O‘tmishni chuqur anglash — yorug‘ kelajakni to‘g‘ri qurishga yordam beradi.")
]

# Generate custom avatar image for leader
def generate_leader_portrait(leader_data, index):
    name, sphere, region, gender = leader_data[0], leader_data[1], leader_data[2], leader_data[3]
    bg_colors = GRADIENTS[index % len(GRADIENTS)]
    
    img = Image.new('RGB', (600, 800), color=bg_colors[0])
    draw = ImageDraw.Draw(img)
    
    # Draw decorative gradient circles
    draw.ellipse([-100, -100, 700, 700], outline=bg_colors[2], width=8)
    draw.ellipse([50, 50, 550, 550], outline=bg_colors[3], width=4)
    
    # Draw center avatar badge
    center_x, center_y = 300, 320
    radius = 160
    draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius], fill=bg_colors[1], outline='#00A6EB', width=6)
    
    # Initials
    parts = name.split()
    initials = (parts[0][0] + parts[1][0]).upper() if len(parts) > 1 else parts[0][:2].upper()
    
    # Default PIL Font
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
        font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except:
        font_large = font_name = font_sub = ImageFont.load_default()
        
    # Draw initials text
    draw.text((center_x, center_y), initials, fill='#ffffff', font=font_large, anchor='mm')
    
    # Bottom info box
    draw.rectangle([30, 560, 570, 760], fill='#0b1727', outline='#00A6EB', width=2)
    
    # Draw Name & Info
    display_name = parts[0] + " " + parts[1]
    draw.text((300, 615), display_name, fill='#ffffff', font=font_name, anchor='mm')
    draw.text((300, 675), f"{sphere.upper()} | {region}", fill='#00A6EB', font=font_sub, anchor='mm')
    draw.text((300, 715), "O‘ZBEKISTON YETAKCHI YOSHLARI", fill='#94a3b8', font=font_sub, anchor='mm')
    
    filename = f"leader_photo_{index}.png"
    filepath = f"/home/lochinbek/Desktop/yetakchilar/media/leaders/{filename}"
    img.save(filepath, 'PNG')
    
    # Upload to S3
    s3_key = f"leaders/{filename}"
    s3.upload_file(filepath, bucket_name, s3_key)
    return f"leaders/{filename}"

# Generate Quote Poster Image for leader
def generate_quote_poster(leader_data, index):
    name, sphere, region, _, _, _, _, _, _, quote_text = leader_data
    bg_colors = GRADIENTS[(index + 3) % len(GRADIENTS)]
    
    img = Image.new('RGB', (1080, 1350), color=bg_colors[0])
    draw = ImageDraw.Draw(img)
    
    # Background frame & border
    draw.rectangle([40, 40, 1040, 1310], outline='#00A6EB', width=6)
    draw.rectangle([60, 60, 1020, 1290], fill=bg_colors[1], outline=bg_colors[3], width=3)
    
    try:
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_quote = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
        font_author = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        font_meta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        font_header = font_quote = font_author = font_meta = ImageFont.load_default()
        
    # Top Branding Header
    draw.text((540, 120), "O‘ZBEKISTON YETAKCHI YOSHLARI ENSIKLOPEDIYASI", fill='#00A6EB', font=font_header, anchor='mm')
    draw.text((540, 170), "YETAKCHILAR IQTIBOSI", fill='#94a3b8', font=font_meta, anchor='mm')
    draw.line([200, 210, 880, 210], fill='#00A6EB', width=3)
    
    # Quote Icon
    draw.text((540, 300), "“", fill='#00A6EB', font=font_quote, anchor='mm')
    
    # Word wrap quote text
    words = quote_text.split()
    lines = []
    curr_line = ""
    for w in words:
        if len(curr_line + " " + w) < 32:
            curr_line += " " + w if curr_line else w
        else:
            lines.append(curr_line)
            curr_line = w
    if curr_line:
        lines.append(curr_line)
        
    start_y = 480 - (len(lines) * 30)
    for i, line in enumerate(lines):
        draw.text((540, start_y + (i * 65)), line, fill='#ffffff', font=font_quote, anchor='mm')
        
    # Bottom Author Bar
    draw.rectangle([100, 1000, 980, 1220], fill='#0b1727', outline='#00A6EB', width=3)
    draw.text((540, 1060), name.upper(), fill='#ffffff', font=font_author, anchor='mm')
    draw.text((540, 1130), f"{sphere.upper()} SOHASI — {region.upper()}", fill='#00A6EB', font=font_meta, anchor='mm')
    draw.text((540, 1175), "O‘zYYE Rasmiy Iqtibos Posteri", fill='#94a3b8', font=font_meta, anchor='mm')
    
    filename = f"quote_poster_{index}.png"
    filepath = f"/home/lochinbek/Desktop/yetakchilar/media/leaders/quotes/{filename}"
    img.save(filepath, 'PNG')
    
    # Upload to S3
    s3_key = f"leaders/quotes/{filename}"
    s3.upload_file(filepath, bucket_name, s3_key)
    return f"leaders/quotes/{filename}"

print("Starting generation of 45 leaders & quote posters...")

for idx, item in enumerate(RAW_LEADERS, 1):
    name, sphere, region, gender, short_bio, full_bio, birth_date, birth_place, education, quote_text = item
    
    # Generate images & upload to S3
    photo_s3_path = generate_leader_portrait(item, idx)
    poster_s3_path = generate_quote_poster(item, idx)
    
    # Save to PostgreSQL DB
    leader, created = Leader.objects.get_or_create(
        name=name,
        defaults={
            'sphere': sphere,
            'region': region,
            'photo': photo_s3_path,
            'short_bio': short_bio,
            'full_bio': full_bio,
            'birth_date': birth_date,
            'birth_place': birth_place,
            'education': education,
            'quote_poster': poster_s3_path,
            'is_featured': True
        }
    )
    if not created:
        leader.sphere = sphere
        leader.region = region
        leader.photo = photo_s3_path
        leader.short_bio = short_bio
        leader.full_bio = full_bio
        leader.birth_date = birth_date
        leader.birth_place = birth_place
        leader.education = education
        leader.quote_poster = poster_s3_path
        leader.is_featured = True
        leader.save()
        

    print(f"[{idx}/45] Created/Updated: {name} ({sphere}, {region})")

print("All 45 leaders & quotes successfully generated, uploaded to S3, and seeded to DB!")
