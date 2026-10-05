# İkinci Beyin

Claude Code (ve Codex) için kişisel çalışma klasörü. Seni, işini ve devam eden
projelerini dosyalarda tutar. Her yeni oturumda baştan anlatmak zorunda
kalmazsın.

## Kurulum

**Yol 1: Claude'a kurdur (en kolayı)**

1. Bilgisayarında boş bir klasör aç (adında Türkçe karakter ve boşluk olmasın,
   ör. `ikinci-beyin`). VS Code'da bu klasörü aç, Claude Code'u başlat.
2. Claude'a şunu yaz: `Bu repoyu bu klasörün içine klonla: https://github.com/ahmetdemircid/ikinci-beyin`
3. Klonlama bitince **`/reload-skills`** yaz. Bu adımı atlama: Claude Code,
   oturum açıldıktan sonra gelen skill'leri kendiliğinden görmez. İstersen
   bunun yerine Claude Code'u kapatıp yeniden açabilirsin.
4. `/kurulum` yaz.

**Yol 2: ZIP indir**

1. Repo sayfasında yeşil **Code** düğmesi, **Download ZIP**. Zip'i aç.
2. Açılan klasörü VS Code'da aç, Claude Code'u başlat.
3. `/kurulum` yaz.

Claude sana tek tek soru soracak (15-20 dakika). Cevaplarına göre klasörleri
kurup dosyaları dolduracak. Bitince oturumu kapat, yeni oturum aç ve
hiçbir şey anlatmadan **"Önümüzdeki iki haftada beni neler bekliyor?"** diye sor.

Zaten dolu bir çalışma klasörün varsa: bu repodaki `.claude/skills/` klasörünü
kendi klasörüne kopyala ve orada `/kurulum` yaz. Var olan hiçbir dosya
silinmez, taşınmaz.

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
