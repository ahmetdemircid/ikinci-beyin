# İkinci Beyin

Claude Code (ve Codex) için kişisel çalışma klasörü. Seni, işini ve devam eden
projelerini dosyalarda tutar. Her yeni oturumda baştan anlatmak zorunda
kalmazsın.

## Kurulum

1. Bilgisayarında boş bir klasör aç (adında Türkçe karakter ve boşluk olmasın,
   ör. `ikinci-beyin`). VS Code'da bu klasörü aç, Claude Code'u başlat.
2. Claude'a şunu yapıştır:

   ```
   https://raw.githubusercontent.com/ahmetdemircid/ikinci-beyin/master/KURULUM.md dosyasını oku ve bu klasöre kur.
   ```

Claude dosyaları indirir ve hemen sana tek tek soru sormaya başlar (15-20
dakika). Cevaplarına göre klasörleri kurup dosyaları dolduracak. Bitince oturumu
kapat, yeni oturum aç ve hiçbir şey anlatmadan **"Önümüzdeki iki haftada beni
neler bekliyor?"** diye sor.

Zaten dolu bir çalışma klasörün varsa aynı mesajı orada yapıştır. Var olan
hiçbir dosya silinmez, taşınmaz, üstüne yazılmaz.

Bu repoyu kuran asistan: adımlar `KURULUM.md` dosyasında.

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
