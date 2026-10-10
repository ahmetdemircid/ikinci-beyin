# İkinci Beyin

Claude Code (ve Codex) için kişisel çalışma klasörü. Seni, işini ve devam eden
projelerini dosyalarda tutar. Her yeni oturumda baştan anlatmak zorunda
kalmazsın.

## Kurulum

1. Bilgisayarında boş bir klasör aç (adında Türkçe karakter ve boşluk olmasın,
   ör. `ikinci-beyin`). VS Code'da bu klasörü aç, Claude Code'u başlat.
2. Claude'a şunu yaz:

   ```
   Bunu kur: https://github.com/ahmetdemircid/ikinci-beyin
   ```

Claude repoyu indirir ve hemen sana soru sormaya başlar. Başka bir şey yazmana
gerek yok.

**ZIP ile**

1. Repo sayfasında yeşil **Code** düğmesi, **Download ZIP**. Zip'i aç.
2. Açılan klasörü VS Code'da aç, Claude Code'u başlat.
3. `/kurulum` yaz.

Claude sana tek tek soru soracak (15-20 dakika). Cevaplarına göre klasörleri
kurup dosyaları dolduracak. Bitince oturumu kapat, yeni oturum aç ve
hiçbir şey anlatmadan **"Önümüzdeki iki haftada beni neler bekliyor?"** diye sor.

Zaten dolu bir çalışma klasörün varsa: bu repodaki `.claude/skills/` klasörünü
kendi klasörüne kopyala ve orada `/kurulum` yaz. Var olan hiçbir dosya
silinmez, taşınmaz.

## Claude için kurulum talimatı

Bu bölüm, bu repoyu kullanıcı için kuran yapay zeka asistanına yazıldı.

1. Dosyalar, kullanıcının açık olduğu klasörün **köküne** gelmeli, alt klasöre
   değil. Klasör boşsa `git clone https://github.com/ahmetdemircid/ikinci-beyin .`
   kullan. Alt klasöre klonladıysan içindeki her şeyi (`.git`, `.claude`,
   `.gitignore`, `.gitattributes` dahil) köke taşı ve boş kalan alt klasörü
   kaldır. Kökte kullanıcıya ait dosyalar zaten varsa hiçbirinin üstüne yazma,
   yalnızca `.claude/skills/` klasörünü köke kopyala.
2. Kullanıcıya commit geçmişi, dosya listesi ya da teknik ayrıntı gösterme.
   Klonlamanın bittiğini tek cümleyle söyle.
3. Kullanıcıdan `/reload-skills` ya da `/kurulum` yazmasını isteme. Hemen
   `.claude/skills/kurulum/SKILL.md` dosyasını oku ve oradaki adımları bu
   oturumda uygula. O dosyadaki `${CLAUDE_SKILL_DIR}` yolu
   `.claude/skills/kurulum` demektir.

## Kurulumdan sonra klasör

```
AGENTS.md                ana kural dosyası (Codex de okur)
CLAUDE.md                AGENTS.md'yi ve bağlam dosyalarını yükler
context/                 sen, işin, öncelikler, hedefler, yazı örneklerin
projects/index.md        projelerin haritası, her projede bir DEVAM.md
decisions/log.md         karar günlüğü, sadece ekleme yapılır
.claude/rules/           kalıcı kurallar (düzeltmeler buraya)
.claude/skills/          tekrar eden işler
references/              referans malzeme, şablonlar, kurulum cevapları
runs/                    otomasyon kayıtları
archives/                hiçbir şey silinmez, buraya taşınır
```

## Her gün

| Ne zaman | Komut | Ne yapar |
|---|---|---|
| Oturum başı | `/gunu-ac` | Nerede kaldığını, yaklaşan tarihleri, sıradaki işi söyler |
| Oturum sonu | `/gunu-kapat` | Konuşulanı dosyalara yazar, kararları kaydeder, Git kaydı alır |
| Haftada bir | `/saglik-kontrolu` | Dağılan yerleri bulur, onay vermeden düzeltmez |

## Bilgilerin değişince

`/kurulum guncelle` yaz. Sadece değişen bölümü sorar, eski hâli `archives/`
altına kopyalar.
