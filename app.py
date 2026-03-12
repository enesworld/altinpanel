from flask import Flask, render_template
import feedparser
from datetime import datetime, timedelta
import calendar

app = Flask(__name__)

def haberleri_getir(rss_listesi, aranan_kelime):
    bulunan_haberler = []
    toplam_taranan = 0

    for rss_url in rss_listesi:
        feed = feedparser.parse(rss_url)
        toplam_taranan += len(feed.entries)
        
        for entry in feed.entries:
            baslik = entry.title.lower() if hasattr(entry, 'title') else ""
            ozet = entry.summary.lower() if hasattr(entry, 'summary') else ""

            if aranan_kelime in baslik or aranan_kelime in ozet:
                parsed_date = entry.get('published_parsed') or entry.get('updated_parsed')
                
                if parsed_date:
                    dt = datetime.utcfromtimestamp(calendar.timegm(parsed_date)) + timedelta(hours=3)
                    aylar = {1:"Ocak", 2:"Şubat", 3:"Mart", 4:"Nisan", 5:"Mayıs", 6:"Haziran", 
                             7:"Temmuz", 8:"Ağustos", 9:"Eylül", 10:"Ekim", 11:"Kasım", 12:"Aralık"}
                    tarih_metni = f"{dt.day} {aylar[dt.month]} {dt.year}, {dt.strftime('%H:%M')}"
                    zaman_damgasi = dt.timestamp()
                else:
                    tarih_metni = "Tarih belirtilmemiş"
                    zaman_damgasi = 0

                bulunan_haberler.append({
                    'baslik': entry.title,
                    'link': entry.link,
                    'tarih': tarih_metni,
                    'zaman_damgasi': zaman_damgasi
                })

    bulunan_haberler.sort(key=lambda x: x['zaman_damgasi'], reverse=True)
    return bulunan_haberler, toplam_taranan

@app.route('/haber-ozel-tara')
def ana_sayfa():
    return render_template('index.html', haberler=None)

@app.route('/haber-ozel-tara/tara')
def tara():
    rss_kaynaklari = [
        "https://www.hurriyet.com.tr/rss/anasayfa",
        "https://www.sozcu.com.tr/rss/tum-haberler.xml",
        "https://www.ntv.com.tr/son-dakika.rss",
        "https://news.google.com/rss/search?q=bakırköy&hl=tr&gl=TR&ceid=TR:tr"
    ]
    aranan = "bakırköy"
    haberler, taranan_sayisi = haberleri_getir(rss_kaynaklari, aranan)
    return render_template('index.html', haberler=haberler, aranan=aranan, taranan_sayisi=taranan_sayisi)

if __name__ == '__main__':
    app.run(debug=True)