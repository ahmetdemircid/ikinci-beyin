---
name: kurulum
description: İkinci beyni kişiye göre kurar. Sorular tek tek sorulur, her cevap anında references/kurulum-cevaplari.md dosyasına yazılır. Ardından iskelet klasörler oluşturulur ve context/, AGENTS.md, .claude/rules/ ile projects/index.md cevaplara göre doldurulur. Kullanıcı "/kurulum", "kurulumu başlat", "beni tanı", "bilgilerimi güncelle", "kurulumu yeniden yap" dediğinde ya da klasörde henüz AGENTS.md yokken kullan.
argument-hint: "[guncelle | bolum-adi]"
---

# Kurulum

Bu klasörü kullanıcının ikinci beynine çevirirsin: onu tanıyan, her yeni oturumda
nerede kaldığını bilen bir çalışma klasörü. İş iki parçadan oluşur:

1. **İskelet.** Klasör ve dosya adları herkeste aynıdır, `${CLAUDE_SKILL_DIR}/iskelet/`
   içinde durur. Bu adları değiştirme, çünkü diğer skill'ler bu yolları okur.
2. **İçerik.** Röportajdan gelir, kişiye özeldir.

Soruların tamamı `${CLAUDE_SKILL_DIR}/sorular.md` dosyasında. Röportaja başlamadan
önce o dosyayı oku.

## Kesin kurallar

- **Hiçbir dosyayı silme, taşıma, yeniden adlandırma.** Var olan bir dosyanın
  üstüne yazman gerekiyorsa önce `archives/kurulum-oncesi-{YYYY-AA-GG-SSDD}/`
  altına kopyasını al.
- **Uydurma.** Kullanıcı cevap vermediyse o alanı boş bırak ve "(cevap yok)" yaz.
  Hedef, rakam, rakip ya da araç tahmin etme.
- **Soruları tek tek sor.** Kullanıcı cevap vermeden sonraki soruya geçme.
- **Her cevabı anında yaz.** Kullanıcının cevabını hemen
  `references/kurulum-cevaplari.md` dosyasına ekle. Oturum yarıda koparsa
  kaldığın yerden devam edebilmen buna bağlı.
- **Kullanıcının sözlerini koru.** Cevapları özetleyip başka kelimelerle yeniden
  yazma. Context dosyaları kısa ve düzenli olabilir, ama ham cevaplar dosyası
  kullanıcının kendi cümleleridir.

## 1. Durumu tespit et

Önce şunlara bak: `references/kurulum-cevaplari.md`, `AGENTS.md`, `CLAUDE.md`, kök
klasördeki diğer dosya ve klasörler. Sonra hangi moddasın, kullanıcıya tek
cümleyle söyle.

| Mod | Ne zaman | Ne yaparsın |
|---|---|---|
| **İlk kurulum** | Cevaplar dosyası yok. Kökte sadece şablonla gelenler var: `README.md`, `.gitignore`, `.gitattributes`, `.git`, `.claude/`, `LICENSE` (editörün açtığı `.vscode/` da sayılmaz) | Tüm adımlar sırayla |
| **Devam** | Cevaplar dosyası var, başında `Durum: yarım` yazıyor | Cevaplanmamış ilk sorudan devam et, önceki cevapları tekrar sorma |
| **Güncelleme** | Cevaplar dosyası var, `Durum: tamamlandı` | Bölümleri listele, hangisinin değiştiğini sor, sadece onu sor ve sadece etkilenen dosyaları güncelle (aşağıda) |
| **Dolu klasör** | Cevaplar dosyası yok ama kökte başka dosya/klasör var | İlk kurulum gibi, ama 3. adımdaki "dolu klasör" kuralları geçerli |

Kullanıcı `$ARGUMENTS` içinde `guncelle` ya da bir bölüm adı verdiyse güncelleme
moduna doğrudan gir.

## 2. Röportaj

Başlamadan önce kullanıcıya üç şey söyle, kısaca:
- Yaklaşık kaç soru olduğunu ve 15-20 dakika süreceğini.
- Düzgün cümle kurmasına gerek olmadığını, konuşur gibi yazabileceğini.
- Bir soruyu "geç" diyerek atlayabileceğini, sonradan `/kurulum guncelle` ile
  doldurabileceğini.

Sonra `sorular.md`'deki sırayla ilerle. Her soruda şunları uygula:

- **Belirsiz cevabı bir kez somutlaştır.** "Büyümek", "yakında", "daha çok
  müşteri" gibi ölçülemeyen bir cevapta bir kez rakam, tarih ya da örnek iste
  ("Ne kadar büyümek, hangi tarihe kadar?"). İkinci kez sorma. Kullanıcı
  "bilmiyorum" derse cevabı olduğu gibi kabul et ve dosyaya `(belirsiz)`
  işaretiyle yaz.
- **Uzun cevabı bölme.** Bir cevap sonraki soruyu da karşılıyorsa o soruyu sorma,
  "bunu az önce söyledin, şöyle not aldım" de ve aldığın notu göster.
- **Yazı örneği sorusunda** kullanıcıdan son yazdığı iki metni düzenlemeden
  yapıştırmasını iste. Bu metinleri düzeltme, kısaltma, yorumlama. Olduğu gibi
  `context/writing-samples.md` dosyasına koy.

Her cevaptan sonra `references/kurulum-cevaplari.md` dosyasına şu biçimde ekle:

```
### {soru kodu} {soru}
{kullanıcının cevabı, kendi kelimeleriyle}
```

Dosya yoksa `iskelet/references/kurulum-cevaplari.md` kalıbıyla oluştur ve başına
`Durum: yarım` yaz. Bütün sorular bitince bu satırı `Durum: tamamlandı`
yap ve tarihi ekle.

## 3. İskeleti kur ve doldur

Röportaj bitince `iskelet/` altındaki her dosyayı klasördeki aynı yola kopyala.
Klasörde zaten bulunan dosyayı kopyalama: `references/kurulum-cevaplari.md`
röportajda oluştu, dolu klasörde başka dosyalar da olabilir. Var olan
`CLAUDE.md` ve `AGENTS.md` için aşağıdaki "dolu klasör kuralları" geçerli.
Dosyalardaki `{{...}}` alanlarını cevaplarla doldur. Doldururken:

- **Cevap yoksa alanı silme.** Yerine `(cevap yok, /kurulum guncelle ile doldur)`
  yaz. Sağlık kontrolü bu satırları bulur.
- **Tarih kullan.** `{{BUGUN}}` alanlarına bugünün tarihini yaz (YYYY-AA-GG).
  `{{CEYREK}}` için içinde bulunulan çeyreği yaz (ör. "2026 Ç4, Ekim-Aralık").
- **context/ dosyalarını kısa tut.** Her dosya bir ekranı geçmesin. Bu
  dosyalar her oturumda yükleniyor, uzun dosya her mesajda token harcatır.
- **Projeler.** `projects/index.md`'ye kullanıcının saydığı her proje için
  bir satır ekle. Her proje için `projects/{klasor-adi}/DEVAM.md` oluştur.
  Klasör adı küçük harf, tireli ve Türkçe karaktersiz olsun (ör.
  `web-sitesi-yenileme`). Şablon olarak `iskelet/references/sablonlar/DEVAM.md`
  kullan. Bildiğin kadarını doldur, bilmediğin alana "(henüz yok)" yaz.
- **İletişim kuralları.** Kullanıcının yasakları (emoji, belli kelimeler,
  uzunluk) `.claude/rules/iletisim.md` dosyasına gider. AGENTS.md'de bunun
  sadece tek cümlelik özeti durur.
- **`.claude/` izni.** Claude Code `.claude/` klasörüne yazmayı korur ve
  sohbetteki "izin veriyorum" sözü yetmez, ayrı bir onay penceresi açılır. Bu
  dosyayı yazmadan hemen önce kullanıcıya şunu söyle: "Şimdi kural dosyasını
  yazacağım. Claude Code bu klasör için ayrıca izin soracak, onayla." Yazma
  yine reddedilirse dosyanın içeriğini kullanıcıya göster ve kapanışta
  eksik olarak belirt.

**Dolu klasör kuralları:**
- Var olan dosya ve klasörlere dokunma. Hepsini listele, sonra
  `projects/index.md`'nin altına "Kurulumdan önce vardı" başlıklı bir tabloyla
  yazdıkları yerde kaydet. Taşıma önerin varsa sadece öner, kendin taşıma.
- Kökte zaten `CLAUDE.md` ya da `AGENTS.md` varsa önce arşive kopyala. Sonra
  eski dosyadaki kişisel kuralları yeni dosyanın "Kullanıcının eklediği kurallar"
  bölümüne olduğu gibi taşı ve neyi taşıdığını kullanıcıya göster.

**Güncelleme modunda** sadece değişen bölümün dosyalarını yeniden yaz:

| Bölüm | Etkilediği dosyalar |
|---|---|
| A Sen | `context/me.md`, AGENTS.md'nin ilk satırları |
| B İşin | `context/work.md` |
| C Şimdi | `context/current-priorities.md`, `context/goals.md`, `projects/index.md` |
| D Konuşma | `.claude/rules/iletisim.md`, AGENTS.md'deki özet cümle, `context/writing-samples.md` |
| E Devret | `context/work.md` "Tekrar eden işler" bölümü |

Değişen her dosyanın eski hâlini önce `archives/kurulum-oncesi-{tarih}/` altına
kopyala. Eski cevapları da `references/kurulum-cevaplari.md` içinde silme;
yeni cevabı altına `(güncellendi {tarih})` notuyla ekle.

## 4. Git

`git --version` çalıştır.
- Git yoksa bu adımı atla ve kullanıcıya bir cümleyle söyle: "Git kurulu değil,
  geri alma özelliği olmadan devam ediyoruz; kurmak istersen git-scm.com."
- Git varsa ve klasörde `.git` yoksa `git init` çalıştır. Git'i sen
  başlattıysan ve `.gitattributes` yoksa şu iki satırla oluştur (Windows'ta
  her kayıtta çıkan satır sonu uyarılarını önler):
  `# Satir sonlarini her yerde ayni tutar.` ve `* text=auto eol=lf`.
  Klasörde zaten `.git` varsa `.gitattributes`'a dokunma.
- `git remote -v` çalıştır. `origin` bu şablonun indirildiği repoyu
  gösteriyorsa (klasör `git clone` ile geldiyse böyledir) kullanıcıya söyle:
  "Bu klasör hâlâ şablonun GitHub reposuna bağlı. Artık içinde senin kişisel
  bilgilerin var, yanlışlıkla oraya gönderilmesin diye bağlantıyı
  kaldırayım mı?" Evet derse `git remote remove origin` çalıştır. Kendi
  yedek reposunu bağlamak isterse bunu ayrıca yapar.
- `.gitignore` içinde şu üç satır yoksa ekle (dosya yoksa oluştur):
  `CLAUDE.local.md`, `.claude/settings.local.json`, `.env`. Bunlar kişisel
  ayar ve şifre dosyaları, paylaşılan kayda girmemeli.
- Commit'i kendin atma. Kullanıcıya sor: "İlk kaydı alayım mı? Bundan sonra
  bir şey bozulursa bu noktaya dönebilirsin." Evet derse
  `git add -A && git commit -m "Ikinci beyin kuruldu"` çalıştır.
- Commit "Please tell me who you are" hatasıyla reddedilirse Git'te ad ve
  e-posta tanımlı değildir. Kullanıcıdan bir ad ve e-posta iste, sadece bu
  klasör için tanımla (`git config user.name "..."` ve
  `git config user.email "..."`, `--global` KULLANMA) ve commit'i tekrar dene.

## 5. Kendini denetle

Kullanıcıya göstermeden önce kendin kontrol et:

1. Cevaplarda geçen her rakam, tarih ve proje adı ilgili context dosyasında var
   mı? Eksik olanı ekle.
2. Context dosyalarında cevaplarda olmayan bir iddia var mı? Varsa sil, çünkü o
   iddiayı sen uydurmuşsun.
3. `CLAUDE.md` içindeki her `@` yolu gerçekten var olan bir dosyayı gösteriyor
   mu?
4. AGENTS.md 150 satırın altında mı?

## 6. Kapanış

Kullanıcıya sırayla şunları göster:

1. Oluşan klasör ağacı ve her dosyanın ne içerdiği, birer satırla.
2. E bölümünün cevaplarından çıkan "ileride skill'e dönüşebilecek işler"
   listesi. Bu liste `context/work.md` içinde de duruyor olmalı.
3. Kurulumun gerçekten çalıştığını görmek için şu adım (bunu aynen yaz):

   > Bu oturumu kapat, yeni bir oturum aç ve hiçbir şey anlatmadan şunu sor:
   > **"Önümüzdeki iki haftada beni neler bekliyor?"** Seni tanımayan bir
   > asistan bunu bilemez. Cevap burada söylediğin tarihleri ve projeleri
   > sayıyorsa kurulum çalışıyor demektir. Genel bir tavsiye listesi veriyorsa
   > bir yer eksik, `/kurulum guncelle` ile düzeltiriz.

4. Bundan sonraki alışkanlık, üç satırla:
   - Oturuma `/gunu-ac` ile başla.
   - Oturumu `/gunu-kapat` ile bitir. Kapatılmayan oturumda konuşulan kaybolur.
   - Haftada bir `/saglik-kontrolu` çalıştır.
