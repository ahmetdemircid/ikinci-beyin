---
name: saglik-kontrolu
description: İkinci beyin klasörünün haftalık bakımı. Haritada olmayan ya da diskte olmayan proje klasörlerini, giriş dosyası eksik klasörleri, eskimiş DEVAM.md dosyalarını, var olmayan dosyaya verilen atıfları, geçmişte kalmış tarihleri, boş kalan kurulum alanlarını, büyüyen kural dosyalarını ve karar günlüğünden silinmiş satırları bulur. Önce rapor verir, kullanıcı onaylamadan hiçbir şeyi düzeltmez. Kullanıcı "/saglik-kontrolu", "sağlık kontrolü", "klasörü kontrol et", "bakım yap" dediğinde kullan.
---

# Sağlık kontrolü

Klasör büyüdükçe dağılır: harita eskir, DEVAM.md'ler güncellenmez, dosyalar
taşınır ama atıflar eski yeri gösterir. Bu skill bunları bulur.

**Önce sadece oku ve raporla.** Rapordan önce hiçbir dosyayı değiştirme. Rapor
bittikten sonra kullanıcı hangi maddeleri düzeltmeni isterse sadece onları
düzelt. Hiçbir durumda dosya silme.

Araçlarını kullan: klasör listesi için Glob, metin aramak için Grep, okumak
için Read. Tahminle "var" ya da "yok" deme, her bulguyu bir araç sonucuna
dayandır.

## Kontroller

Her kontrolde bulguyu kanıtıyla not et (dosya yolu, satır, tarih).

### K1. Haritada olmayan klasör (yetim)
`projects/` altındaki her klasörü listele. `projects/index.md`'de (Aktif ya da
Bitenler tablosunda) adı geçmeyen klasör yetimdir.

### K2. Diskte olmayan klasör
`projects/index.md`'de adı geçen ama `projects/` altında bulunmayan klasör.
`archives/` altına taşınmış olabilir, varsa nerede olduğunu yaz.

### K3. Giriş dosyası olmayan klasör
`projects/` altındaki her klasörde `DEVAM.md`, `README.md` ya da `index.md`
dosyalarından en az biri olmalı.

### K4. Eskimiş proje
`projects/index.md`'de durumu "aktif" olan ama `DEVAM.md`'sindeki "Son
güncelleme" tarihi bugünden 14 günden eski olan proje.

### K5. Kırık atıf
Şu dosyalarda geçen dosya yollarını tara: `AGENTS.md`, `CLAUDE.md` (`@`
satırları dahil), `context/*.md`, `projects/index.md`, her `DEVAM.md`. Ters
tırnak içindeki göreli yollar ve `@` ile başlayan yollar atıftır. Gösterdiği
dosya ya da klasör yoksa kırık atıftır. `{ad}` gibi süslü parantezli kalıplar
ve `references/sablonlar/` içindeki örnek yollar atıf değildir, bunları sayma.

### K6. Geçmişte kalmış tarih
`context/current-priorities.md` "Yaklaşan tarihler" bölümünde bugünden önce
kalmış tarih.

### K7. Bağlam tazeliği
- `context/current-priorities.md` "Son güncelleme" tarihi 30 günden eski mi?
- `context/goals.md`'deki çeyrek bugünün çeyreği mi?

### K8. Boş alan
`(cevap yok` ile başlayan satırlar: kurulumda atlanan sorular. Hangi dosyada,
hangi başlık altında olduğunu yaz.

### K9. Boyut
- `AGENTS.md` 150 satırı geçiyor mu?
- `context/` altındaki her dosya 60 satırı geçiyor mu? Bu dosyalar her
  oturumda yükleniyor, büyüdükçe her mesaj daha çok token harcar.

### K10. Karar günlüğü bütünlüğü
Git varsa `git log -p --format="%h %cd" --date=short -- decisions/log.md`
çıktısında `-` ile başlayan (silinmiş) satır var mı? Varsa günlük "sadece
ekleme" kuralını çiğnemiş demektir. Hangi commit'te, hangi satır silinmiş, yaz.
Commit edilmemiş değişiklikler için `git diff -- decisions/log.md` de bak.
Git yoksa bu kontrolü "Git yok, yapılamadı" diye geç.

### K11. Kaydedilmemiş iş
Git varsa `git status --short` ve son commit tarihi. 3 günden uzun süredir
kaydedilmemiş değişiklik varsa not et.

## Rapor

Önce tek satır özet ver: "{N} sorun buldum: {X} önemli, {Y} küçük." Sorun
yoksa "Klasör sağlıklı" de ve hangi kontrollerin yapıldığını tek satırda say.

Sonra tablo:

| # | Kontrol | Bulgu | Kanıt | Önerilen düzeltme |
|---|---|---|---|---|

Önemli sayılanlar: K1, K2, K5, K10 (bunlar yeni oturumun yanlış yere
bakmasına ya da kaydın kaybolmasına yol açar). Diğerleri küçüktür. Tabloyu
önce önemliler gelecek şekilde sırala.

Önerilen düzeltme her zaman silmeyen bir işlem olmalı: haritaya satır ekle,
DEVAM.md oluştur, atıfı yeni yola çevir, tarihi "Geçmiş"e indir, dosyayı
`archives/`'e taşı.

Raporun sonunda sor: "Hangilerini düzelteyim? (numara yaz, 'hepsi' ya da
'hiçbiri')"

Bu skill kural dosyalarının birbiriyle çelişip çelişmediğine bakmaz. Bunu
Claude Code'un kendi komutu yapar. Raporun en altına tek satır ekle: "Kural
çelişkisi için ayda bir `/doctor prompt-audit` çalıştır."

## Kayıt

Rapordan sonra (kullanıcının cevabını beklemeden) `runs/{YYYY-AA-GG}-saglik-kontrolu.md`
dosyasına kısa bir kayıt yaz: tarih, kaç sorun, hangi kontroller bulgu verdi.
Kullanıcı düzeltme isterse düzelttiklerini aynı dosyanın altına ekle.
Bu kayıt sonraki kontrollerde "aynı sorun tekrar mı ediyor?" sorusunun cevabı.
