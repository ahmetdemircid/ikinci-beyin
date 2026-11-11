---
name: sistemi-guncelle
description: İkinci beyin sisteminin yeni sürümünü GitHub'dan çeker ya da son güncellemeyi geri alır. Dosya işini sistem/guncelle.py betiği yapar; sadece sistem dosyalarını (sistem/sistem-dosyalari.txt listesi) ve AGENTS.md'deki işaretli sistem bölümünü yeniler. Kişisel dosyalara (context/, projects/, decisions/, references/, hafiza/, gunluk/, kullanıcının kendi skill'leri ve kuralları) dokunmaz, önce Git kaydı ve arşiv alır. Kullanıcı "/sistemi-guncelle", "sistemi güncelle", "yeni sürüm var mı", "ikinci beyni güncelle" dediğinde, ayrıca "güncellemeyi geri al" dediğinde kullan.
---

# Sistemi güncelle

Dosyaları sen değiştirmezsin, `sistem/guncelle.py` değiştirir. Senin işin:
betiği çalıştırmak, çıktısını kullanıcıya sade dille anlatmak, onay almak ve
kişisel dosyaya dokunan geçişleri tek tek sormak.

- **Sistem dosyaları:** yeni sürümün `sistem/sistem-dosyalari.txt` listesindekiler
  (sistem skill'leri ve `sistem/` kodu) ve `AGENTS.md`'de `<!-- sistem:basla -->`
  ile `<!-- sistem:bitir -->` arasındaki bölüm. Herkeste aynıdır.
- **Kişisel dosyalar:** geri kalan her şey. Betik bunlara dokunmaz. Tek
  istisna: `.gitignore`'a eksik satır ekler (silmez) ve iskelette olup
  klasörde hiç olmayan boş dosyaları ekler.

**Kendi elinle sistem dosyasını değiştirme, kopyalama, silme.** Betik
çalışmıyorsa dur ve kullanıcıya söyle; işi elle yapmaya kalkma.

Kullanıcı "güncellemeyi geri al" derse en alttaki "Geri alma" bölümüne git.

## 1. Python

Sırayla `python --version`, `py --version`, `python3 --version` dene; Python 3
veren adı aşağıda `{py}` diye kullan. Hiçbiri yoksa dur: "Güncelleme için
Python gerekiyor. python.org'dan kur, kurarken 'Add python.exe to PATH'
kutusunu işaretle, sonra tekrar 'sistemi güncelle' de." Hiçbir dosyayı değiştirme.

## 2. Kontrol (hiçbir şey değişmez)

`{py} sistem/guncelle.py --kontrol`

Betik yeni sürümü GitHub'dan geçici bir klasöre indirir, karşılaştırır, neyin
değişeceğini yazar. Hiçbir dosyaya dokunmaz.

- "Sistem zaten güncel" yazarsa bunu söyle. `sistem/bekleyen-gecisler.txt`
  varsa 5. adıma geç, yoksa dur.
- "HATA" yazarsa hatayı tek cümleyle söyle ve dur.

## 3. Ne değişecek, kullanıcıya göster ve onay al

**Eski bir sürümün skill'inden buraya geldiysen** (yeni sürüm zaten geçici bir
klasöre indirildi ve bu klasörde `sistem/guncelle.py` yok), kontrolü yeni
sürümdeki betikle yap:
`{py} "{geçici klasör}/sistem/guncelle.py" --kontrol --kaynak "{geçici klasör}" --hedef "{bu klasör}"`.
Sonraki adımlarda da aynı `--kaynak` ve `--hedef` ile çalıştır.

Kontrol çıktısını kısa bir listeye çevir, teknik ayrıntı dökme:

```
Sürüm: {eski} -> {yeni}
Değişecek: {her biri için bir cümle: ne işe yarıyor, ne değişti}
Yeni eklenecek: {varsa}
Senin dosyana dokunacak geçiş: {varsa başlığı; ayrıca sorulacak}
Dokunulmayacak: bilgilerin, projelerin, kararların, hafızan, günlüğün, kendi skill'lerin.
```

Bir sistem skill'inin içine kullanıcı kendi dosyasını ya da satırını eklediyse
güncelleme o skill'in klasörünü yeni sürümle değiştirir; eski hâli arşivde
kalır. Kişisel bir değişikliğin kalıcı yeri `hafiza/otomatik/` ya da
kullanıcının kendi adını verdiği ayrı bir skill'dir.

Sonra sor: "Güncelleyeyim mi?" Onay gelmeden 4. adıma geçme.

## 4. Uygula

`{py} sistem/guncelle.py --uygula` (eski sürümden geldiysen 3. adımdaki
`--kaynak` ve `--hedef` ile)

Betik sırayla: eksik `.gitignore` satırlarını ekler, Git varsa geri dönüş
kaydı alır, değişecek dosyaları `archives/sistem-{tarih}/onceki/` altına
kopyalar, sistem dosyalarını yeni sürümle değiştirir, `AGENTS.md`'nin sadece
işaretli bölümünü yeniler, `sistem/kur.py` ile kancaları ve skill kopyalarını
tamamlar.

Çıktıyı oku:
- "Güncellendi" satırı yoksa ya da "HATA" varsa: hatayı söyle, "yarıda
  kaldı" yazıyorsa geri almayı öner (aşağıda). Kendin onarmaya kalkma.
- "AGENTS.md'de sistem işaretleri yok" yazarsa: aşağıdaki "İşaretsiz AGENTS.md"
  bölümünü uygula.
- `kur.py` çıktısındaki `[UYARI]` satırlarını kullanıcıya söyle.

## 5. Geçişler (kişisel dosyaya dokunur, ayrı onay)

`sistem/bekleyen-gecisler.txt` dosyasındaki her satır bir geçiştir. Her biri
için `.claude/skills/sistemi-guncelle/gecisler/{sürüm}.md` dosyasını oku ve:

1. Hangi kişisel dosyada neyin değişeceğini kullanıcıya önce/sonra örneğiyle
   göster. Bir iki satırlık örnek yeter.
2. Ayrı onay iste: "Bu değişiklik senin dosyana dokunuyor. Yapayım mı?
   Hayır dersen sistem eski düzenle çalışmaya devam eder."
3. Onay gelirse önce dosyanın kopyasını son `archives/sistem-{...}/` altında
   `kisisel/` klasörüne al, sonra sadece tarif edilen değişikliği yap.
   İçerikteki hiçbir satırı silme, yeniden yazma ya da özetleme. Bitince o
   satırı `sistem/bekleyen-gecisler.txt`'den sil.
4. Hayır derse dokunma, satır dosyada kalır; sonraki güncellemede yeniden
   sorulur.

## 6. Kaydet

Git varsa: `git add -A` ve
`git commit -m "Sistem guncellendi: {eski} -> {yeni}"`. Git'te ad ve e-posta
yoksa sadece bu klasör için tanımla (`--global` kullanma). `git push` yapma.

## 7. Rapor

İki üç cümle: hangi sürüme geçildi, ne değişti, eski hâl nerede
(`archives/sistem-.../`), geçişlerden hangisi yapıldı hangisi bekliyor. Son
cümle: "Yeni hâlin devreye girmesi için bu oturumu kapatıp yenisini aç."

## İşaretsiz AGENTS.md (çok eski kurulum)

Betik işaretsiz `AGENTS.md`'ye dokunmaz. Elle yap: önce dosyayı son
`archives/sistem-{...}/onceki/` altına kopyala (betik zaten kopyaladıysa
geç). Kişisel kısımları ayır: başlık, "Sen ... iş ortağısın" cümlesi, en
üstteki hedef, iletişim ve itiraz tercihleri, "Kullanıcının eklediği kurallar"
bölümü. Yeni dosyayı şöyle kur: `.claude/skills/kurulum/iskelet/AGENTS.md`
şablonunun işaretlerden önceki kısmını bu kişisel bilgilerle doldur, ardından
şablonun sistem bölümünü işaretleriyle ekle. İki tarafa da uymayan kuralı
silme, "Kullanıcının eklediği kurallar"a olduğu gibi taşı. Neyi nereye
koyduğunu kullanıcıya göster.

## Geri alma

Kullanıcı "güncellemeyi geri al" derse:

1. `{py} sistem/guncelle.py --geri-al`
2. Betik son güncellemede değişen sistem dosyalarını ve `AGENTS.md`'nin
   işaretli bölümünü arşivdeki eski hâline döndürür, yeni sürümün dosyalarını
   arşivin içine kenara alır. Kişisel dosyalara ve güncellemeden sonra
   yapılan işlere dokunmaz. `sistem/` altına yeni eklenen kodu yerinde
   bırakır, çünkü günlük kancaları ona bağlı.
3. Geçiş adımında değişmiş kişisel dosya varsa betik onları geri almaz.
   Kullanıcı isterse `archives/sistem-{...}/kisisel/` altındaki kopyaları
   geri koy.
4. Git varsa: `git add -A` ve `git commit -m "Guncelleme geri alindi"`.
5. "Eski sürüme döndüm. Yeni sürümdeki sorun düzelince tekrar
   güncelleyebilirsin. Yeni oturum aç." de.
