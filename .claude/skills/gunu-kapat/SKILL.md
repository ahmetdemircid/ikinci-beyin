---
name: gunu-kapat
description: Çalışma oturumunu kapatır. Oturum içinde anında yazılmamış bir şey kaldıysa projelerin DEVAM.md dosyalarına yazar, kararları onayla decisions/log.md'ye ekler, değişen öncelikleri günceller, tekrar eden işi ve tekrar eden düzeltmeyi yakalar, sonunda Git kaydı alır. Kullanıcı "/gunu-kapat", "günü kapat", "oturumu kapat", "bugünlük bu kadar", "kapatıyorum", "yarın devam ederiz" dediğinde kullan.
---

# Günü kapat

Amacın, yarın açılacak yeni oturumun bugün konuşulanı bilmeden kaldığı yerden
devam edebilmesi. Yeni oturum bu konuşmayı göremez, sadece dosyaları görür.
Dosyaya yazılmayan şey kaybolur.

Kurallar gereği kayıt oturum boyunca anında tutulur, bu skill bir güvenlik
ağıdır. Her adımda önce dosyaya bak: zaten yazılmış olanı tekrar yazma, sadece
eksik kalanı tamamla. Her şey zaten yazılmışsa bunu söyle ve sadece Git
kaydını al.

## Kesin kurallar

- **Hiçbir şey silme.** DEVAM.md'de eskiyen bilgi "Geçmiş" bölümüne iner,
  silinmez. `decisions/log.md`'de eski kayıt değiştirilmez.
- **Uydurma.** Sadece bu oturumda gerçekten konuşulan ya da yapılan şeyi yaz.
  Emin olmadığın bir şeyi "yapıldı" diye yazma, kullanıcıya sor.
- **Kararı kendin uydurma.** Kullanıcının söylemediği bir kararı ya da
  gerekçeyi onay almadan günlüğe yazma (ayrıntı 3. adımda).

## 1. Bu oturumda ne oldu?

İki kaynağa bak:
1. **Bu konuşma:** hangi projelerde çalışıldı, ne bitti, ne yarım kaldı,
   hangi karar alındı, kullanıcı seni neyde düzeltti.
2. **Git varsa:** `git status --short` ve `git diff --stat`. Hangi dosyalar
   değişti?

Konuşmada hiç iş yapılmadıysa ve değişen dosya da yoksa kullanıcıya
"kapatılacak bir şey yok" de ve dur.

## 2. DEVAM.md dosyalarını güncelle

Bu oturumda dokunulan her proje için `projects/{ad}/DEVAM.md`:
- "Son güncelleme" tarihini bugünün tarihi yap.
- "Şu anki durum" bölümünü yeni duruma göre yeniden yaz.
- "Sıradaki adım" bölümüne tek, somut bir adım yaz. "Devam et" yazma. Neyin,
  hangi dosyanın, hangi bölümünün yapılacağını yaz.
- "Açık kararlar" bölümünde kapanan kararı sil ve "Geçmiş"e taşı, yeni açılan
  kararı ekle.
- "Geçmiş" bölümünün en üstüne tarihli tek satır ekle: bugün ne oldu.

Proje bittiyse durumunu "bitti" yap, klasörü `archives/{ad}-{YYYYAAGG}/` altına
taşı ve `projects/index.md`'de satırı "Bitenler" tablosuna indir, "Nerede"
sütununa yeni yolu yaz. Bu oturumda zaten yapıldıysa tekrar yapma.

Bu oturumda yeni bir proje klasörü açıldıysa ve `DEVAM.md`'si ya da
`projects/index.md` satırı yoksa ikisini de oluştur. Şablon:
`references/sablonlar/DEVAM.md`.

`projects/index.md`'de dokunulan projelerin "Son dokunuş" tarihini güncelle.

## 3. Kararlar

Bu oturumda alınan önemli kararları listele. Önemli karar: fiyat, tarih,
hedef, bir işi bırakma ya da başlatma, bir yöntemi seçme. Günlük küçük
tercihler karar değildir.

Her kararı şu biçimde kullanıcıya göster:
`[YYYY-AA-GG] KARAR: ... | GEREKÇE: ... | BAĞLAM: ...`

- Bu oturumda zaten günlüğe yazılmış kararı tekrar yazma.
- Kullanıcı kararı ve gerekçesini açıkça söylediyse onay beklemeden ekle.
  Gerekçeyi onun sözleriyle yaz, kendi yorumunu ekleme.
- Kararı ya da gerekçeyi sen çıkarıyorsan önce göster ve sor, onaylananları
  ekle.

Kayıtlar `decisions/log.md` dosyasının en altına eklenir.

## 4. Bağlam

- Öncelik değiştiyse `context/current-priorities.md`'yi güncelle. Eski listeyi
  kelimesi kelimesine `archives/oncelikler-gecmisi.md` dosyasının en üstüne
  "## {tarih}" başlığıyla ekle (dosya yoksa oluştur), sonra
  current-priorities'te sadece yeni liste kalsın.
- Çeyrek hedefi değiştiyse `context/goals.md`'yi güncelle. Eski hâli aynı
  şekilde `archives/hedefler-gecmisi.md`'ye taşı.
- Geçmişte kalmış ve gerçekleştiği konuşmada doğrulanan tarihleri "Yaklaşan
  tarihler"den çıkar, ilgili DEVAM.md'nin "Geçmiş"ine yaz.

## 5. Tekrarları yakala

Sadece öner, kendin skill ya da kural yazma.

- **Tekrar eden düzeltme:** kullanıcı seni bu oturumda bir konuda düzelttiyse
  ve aynı düzeltme daha önce de olduysa (`.claude/rules/` ya da konuşma),
  `.claude/rules/` altına kalıcı kural yazmayı öner. Kuralın taslağını göster.
- **Tekrar eden iş:** bu oturumda yapılan bir iş daha önce de aynı adımlarla
  yapıldıysa (DEVAM.md "Geçmiş" satırları, `runs/`, `context/work.md`
  "Tekrar eden işler"), bunun bir skill'e dönüşmesini öner. Kaçıncı kez
  yapıldığını kaynağıyla söyle.

## 6. Kaydet

Git yoksa bu adımı atla ve raporda söyle.

Git varsa:
1. `git add -A`
2. `git commit -m "Gun kapanisi {YYYY-AA-GG}: {en fazla 6 kelimelik ozet}"`
3. Commit Git'te ad/e-posta olmadığı için reddedilirse sormadan `/kurulum` skill'indeki
   gibi sadece bu klasör için tanımla ve tekrar dene.

`git push` yapma. Kayıt bu bilgisayarda kalır.

## 7. Rapor

Kısa tut:

```
**Kapatıldı: {tarih}**

- Güncellenen: {dosyalar, birer satır}
- Günlüğe eklenen karar: {sayı}
- Yarın ilk iş: {en önemli projenin "Sıradaki adım"ı}
- Öneri: {varsa kural/skill önerisi}
- Git: {commit kısa kimliği ya da "Git yok"}
```
