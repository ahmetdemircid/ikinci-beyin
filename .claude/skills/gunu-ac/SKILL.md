---
name: gunu-ac
description: Güne ya da yeni bir çalışma oturumuna başlarken nerede kalındığını özetler. Yaklaşan tarihleri, devam eden projelerin sıradaki adımını, açık kararları ve kaydedilmemiş değişiklikleri gösterir, tek bir "sıradaki iş" önerir. Hiçbir dosyayı değiştirmez. Kullanıcı "/gunu-ac", "günü aç", "günaydın", "nerede kalmıştık", "bugün ne yapıyoruz", "nereden başlayalım" dediğinde kullan.
---

# Günü aç

Amacın kullanıcıya iki dakikada "buradasın" demek. Yeni oturum hiçbir şey
hatırlamaz; bu skill dosyalardan hatırlatır.

**Bu skill hiçbir dosyayı değiştirmez.** Sadece okur ve rapor verir. Bir şeyin
düzeltilmesi gerekiyorsa raporda söyle, kendin düzeltme.

## 1. Oku

Sırayla ve sadece bunları oku. Proje klasörlerini baştan sona tarama.

1. Bugünün tarihi ve haftanın günü.
2. `context/current-priorities.md` ve `context/goals.md` (Claude Code'da zaten
   yüklü, tekrar okuma).
3. `projects/index.md`: "Aktif" tablosundaki projeler.
4. Aktif her projenin `DEVAM.md` dosyasından sadece şu bölümler: "Son
   güncelleme" tarihi, "Şu anki durum", "Sıradaki adım", "Açık kararlar".
5. `decisions/log.md`: son 5 kayıt.
6. Git varsa: `git status --short` (kaydedilmemiş değişiklik var mı) ve
   `git log -1 --format=%cd --date=short` (son kayıt ne zaman).
7. `runs/` altında son 7 güne ait kayıt varsa onların sonuç satırları.

## 2. Hesapla

- **Yaklaşan tarihler:** bugünden itibaren 14 gün içindeki her tarih. Kaynak:
  current-priorities ve DEVAM dosyaları. Her birine "kaç gün kaldı" yaz.
- **Geçmiş tarih:** listede duran ama bugünden önce kalmış bir tarih varsa
  ayrıca not et. Kullanıcıya "oldu mu?" diye sor, olduğunu varsayma.
- **Eskimiş proje:** durumu "aktif" olduğu halde DEVAM.md'si 14 günden uzun
  süredir güncellenmemiş proje.
- **Sıradaki iş:** tek bir iş seç. Seçerken sırayla şunlara bak:
  1. En yakın tarihi olan iş.
  2. Çeyrek hedefine doğrudan bağlı iş.
  3. Başkasının beklediği iş.
  
  Seçtiğin işin gerekçesini bir cümleyle yaz. İş, bir DEVAM.md'deki "Sıradaki
  adım" satırından gelmeli. Dosyalarda olmayan bir iş uydurma.

## 3. Raporla

Aşağıdaki biçimi kullan. Kısa tut, tamamı bir ekranı geçmesin. Boş kalan
bölümü yazma.

```
**{Gün}, {tarih}**

**Sıradaki iş:** {iş}. {Bir cümle gerekçe.}

**Yaklaşan**
- {tarih} ({N} gün): {ne}

**Projeler**
- {proje}: {durum}. Sıradaki: {adım}

**Açık kararlar**
- {karar}: {kimi bekliyor}

**Dikkat**
- {kaydedilmemiş değişiklik / eskimiş proje / geçmiş tarih}
```

Raporun sonunda tek bir soru sor: "{Sıradaki iş} ile mi başlayalım?"

## Kurallar

- `context/` dosyalarındaki kişisel iletişim kuralları burada da geçerli
  (emoji, uzunluk vb.).
- Bir dosya yoksa ya da beklenen bölüm boşsa uydurma. "Dikkat" altına "X
  dosyası yok" yaz ve geç.
- Haftada bir kez sağlık kontrolü yapılmamışsa (`runs/` altında son 7 günde
  `saglik-kontrolu` kaydı yoksa) "Dikkat" altında `/saglik-kontrolu` öner.
