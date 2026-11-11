---
name: gunu-kapat
description: Çalışma oturumunu kapatır. Bu oturumda çalışılan projelerin DEVAM.md dosyasındaki "Şu an" bölümünü ve durum tablosunu günceller, sonra Git kaydı alır. Günlüğü yazmaz, onu oturum kapanınca arka plandaki özetçi yazar. Kullanıcı "/gunu-kapat", "günü kapat", "oturumu kapat", "bugünlük bu kadar", "kapatıyorum", "yarın devam ederiz" dediğinde kullan.
---

# Günü kapat

Amacın, yarın açılacak yeni oturumun kaldığı yerden devam edebilmesi. Yeni
oturum bu konuşmayı göremez; DEVAM.md'yi ve günlüğü görür.

İş bölümü:
- **Ne yapıldı** kaydını oturum kapanınca arka plandaki özetçi `gunluk/`'e
  yazar. Sen günlüğe yazma, DEVAM'a da "ne yapıldı" yazma.
- **Şu anki durum ve sıradaki adım** senin işin: DEVAM.md.
- Karar, ret ve not zaten çalışırken anında yazılıyor (AGENTS.md "Kayıt").
  Burada sadece eksik kalan varsa tamamla, zaten yazılmışı tekrar yazma.

Her şey zaten günceliyse bunu söyle ve sadece Git kaydını al.

## Kesin kurallar

- **Hiçbir şey silme.** DEVAM.md'de eskiyen bilgi aynı klasördeki `GECMIS.md`'nin
  en üstüne taşınır.
- **Uydurma.** Sadece bu oturumda gerçekten konuşulan ya da yapılan şeyi yaz.
- **Öneri karar değildir.** Kullanıcının onaylamadığı öneri "Kararlar"a girmez,
  durum tablosunda "(öneri)" diye durur.

## 1. Hangi projeler?

Bu konuşmada hangi projelerde çalışıldığına bak. Git varsa `git status --short`
ile değişen dosyaları da gör. Hiç iş yapılmadıysa ve değişen dosya yoksa
"kapatılacak bir şey yok" de ve dur.

## 2. DEVAM.md'yi güncelle

Çalışılan her proje için `projects/{ad}/DEVAM.md`. Biçim
`references/sablonlar/DEVAM.md`:

- **Şu an:** "İş" ve "Sıradaki adım" satırlarını yeni duruma göre yeniden yaz.
  Sıradaki adım tek ve somut olsun ("devam et" değil, hangi dosyanın hangi
  bölümü) ve kimin yapacağı yazsın. "Bu oturumda oku"ya yarınki oturumun
  okuması gereken en fazla 3 dosyayı yaz. "Güncellendi"ye bugünün tarih ve saati.
- **Durum tablosu:** değişen satırın durumunu, son dosyasını, kullanıcının
  sözünü ve açık işini güncelle. Değişmeyen satıra dokunma.
- **Kararlar:** bu oturumda kullanıcının açıkça verdiği proje kararı eksikse ekle.

Dosya eski biçimdeyse (Şu an bölümü yok) kendiliğinden çevirme. Eski
biçimdeki "Şu anki durum" ve "Sıradaki adım" bölümlerini güncelle, kullanıcıya
bir kez "DEVAM'ı yeni biçime çevireyim mi?" diye sor.

Proje bittiyse durumunu "bitti" yap, klasörü `archives/{ad}-{YYYYAAGG}/` altına
taşı ve `projects/index.md`'de satırı "Bitenler" tablosuna indir. Yeni açılan
proje klasörünün `DEVAM.md`'si ya da `projects/index.md` satırı yoksa ikisini
de oluştur. `projects/index.md`'de dokunulan projelerin "Son dokunuş" tarihini
güncelle.

## 3. Kaydet

Git yoksa bu adımı atla ve raporda söyle.

Git varsa:
1. `git add -A`
2. `git commit -m "Gun kapanisi {YYYY-AA-GG}: {en fazla 6 kelimelik ozet}"`
3. Commit Git'te ad/e-posta olmadığı için reddedilirse sormadan `/kurulum`
   skill'indeki gibi sadece bu klasör için tanımla ve tekrar dene.

`git push` yapma. Kayıt bu bilgisayarda kalır.

## 4. Rapor

Kısa tut:

```
**Kapatıldı: {tarih}**

- Güncellenen: {DEVAM dosyaları, birer satır}
- Yarın ilk iş: {en önemli projenin "Sıradaki adım"ı}
- Git: {commit kısa kimliği ya da "Git yok"}
```

Son satır: "Günlük, oturumu kapatınca arka planda yazılacak."
