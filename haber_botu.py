import feedparser

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
                haber_bilgisi = {
                    'baslik': entry.title,
                    'link': entry.link
                }
                bulunan_haberler.append(haber_bilgisi)

    return bulunan_haberler, toplam_taranan

rss_kaynaklari = [
    "https://www.hurriyet.com.tr/rss/anasayfa",
    "https://www.sozcu.com.tr/rss/tum-haberler.xml",
    "https://www.ntv.com.tr/son-dakika.rss",
    "https://news.google.com/rss/search?q=bakırköy&hl=tr&gl=TR&ceid=TR:tr"
]

aranan = "bakırköy"
haberler, taranan_sayisi = haberleri_getir(rss_kaynaklari, aranan)

print(f"\nToplam {taranan_sayisi} haber tarandı.")

if haberler:
    print(f"{aranan.upper()} kelimesi geçen {len(haberler)} haber bulundu:\n")
    for haber in haberler:
        print(f"- {haber['baslik']}")
        print(f"  {haber['link']}")
        print("-" * 50)
else:
    print(f"Taranan {taranan_sayisi} haber içinde '{aranan}' kelimesi bulunamadı.")