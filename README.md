# İkinci Beyin

Claude Code, Codex ve agy için kişisel çalışma klasörü. Seni, işini ve devam
eden projelerini dosyalarda tutar. Her oturum kapanınca o oturumda ne
yapıldığını arka planda günlüğe yazar. Yeni oturumda baştan anlatmak zorunda
kalmazsın, üç araç da aynı hafızayı kullanır.

## Kurulum

1. Bilgisayarında boş bir klasör aç (adında Türkçe karakter ve boşluk olmasın,
   ör. `ikinci-beyin`). VS Code'da bu klasörü aç, Claude Code'u başlat.
2. Claude'a şunu yapıştır:

   ```
   https://github.com/ahmetdemircid/ikinci-beyin adresini oku ve bu klasöre kur.
   ```

Claude dosyaları indirir ve hemen sana tek tek soru sormaya başlar (15-20
dakika). Cevaplarına göre klasörleri kurup dosyaları dolduracak. Bitince oturumu
kapat, yeni oturum aç ve hiçbir şey anlatmadan **"Önümüzdeki iki haftada beni
neler bekliyor?"** diye sor.

**Gerekenler:** Claude Code. Günlüğün kendiliğinden yazılması için ayrıca
Python 3 ve terminalde `claude` komutu; ikisi yoksa kurulum söyler, klasörün
geri kalanı onlarsız da çalışır. Codex kullanıyorsan kurulumdan sonra
Codex'te bir kez `/hooks` yazıp onayla.

Zaten dolu bir çalışma klasörün varsa aynı mesajı orada yapıştır. Var olan
hiçbir dosya silinmez, taşınmaz, üstüne yazılmaz.

## Kurulumdan sonra klasör

```
AGENTS.md                ana kural dosyası (Codex de okur)
CLAUDE.md                AGENTS.md'yi ve bağlam dosyalarını yükler
context/                 sen, işin, öncelikler, hedefler, yazı örneklerin
projects/index.md        projelerin haritası, her projede bir DEVAM.md
decisions/log.md         karar günlüğü, sadece ekleme yapılır
decisions/reddedilenler.md  reddettiğin fikirler, tekrar önerilmez
hafiza/otomatik/         kalıcı tercih ve kuralların (üç araç da okur)
gunluk/                  her oturumun kaydı, kendiliğinden yazılır
.claude/skills/          tekrar eden işler (.agents/skills: Codex ve agy kopyası)
sistem/                  günlüğü yazan arka plan kodu, dokunman gerekmez
references/              referans, şablonlar, iş günlüğü, gelen kutusu
runs/                    otomasyon kayıtları
archives/                hiçbir şey silinmez, buraya taşınır
```

## Kullanırken

Komut ezberlemen gerekmez, normal konuş:

| Ne dersin | Ne olur |
|---|---|
| "Nerede kalmıştık?", "Bugün ne yapıyoruz?" | Yaklaşan tarihleri, projelerin sıradaki adımını ve tek bir "sıradaki iş" önerisini söyler |
| Normal çalışırsın | Proje ilerleyince, karar alınınca Claude o anda ilgili dosyaya yazar. Oturumu kapatınca ne yapıldığı günlüğe kendiliğinden yazılır |
| "En son ne yaptık?", "Dün ne yaptık?" | Günlükten cevap verir |
| "Bundan sonra hep şöyle yap" | Kalıcı kural olarak hafızaya yazılır. Konuşmada geçen kural adaylarını ertesi gün "onaylıyor musun" diye sorar, onaysız uygulamaz |
| Bir işi ikinci kez yaptırırsın | Claude "kalıcı hale getireyim mi?" diye bir kez sorar. Evet dersen işi skill'e çevirir, yeni bir oturumda dener, bundan sonra tek cümleyle yapar. İstersen sen de "bunu kalıcı yap" diyebilirsin |
| Bir fikri reddedersin | Gerekçesiyle kaydedilir, bir daha önerilmez |
| "Not al: ..." | Gelen kutusuna düşer, sonra birlikte ilgili yere dağıtılır |
| "Bugünlük bu kadar" | Projelerin durumunu günceller, bu bilgisayarda bir geri dönüş noktası (Git kaydı) alır |
| "Klasörü kontrol et" (haftada bir) | Dağılan yerleri bulur, onay vermeden düzeltmez |
| "Paketi kur" | AI Builder Kulübü'nden indirdiğin hazır sistem paketini kurar |
| "Sistemi güncelle" | Yeni sürümü çeker. Senin bilgilerine, projelerine, kararlarına dokunmaz |

## Bilgilerin değişince

`/kurulum guncelle` yaz. Sadece değişen bölümü sorar, eski hâli `archives/`
altına kopyalar.

## Asistan için kurulum adımları

Bu bölüm, kullanıcının "bu adresi oku ve bu klasöre kur" dediği yapay zeka
asistanı için yazıldı. Dosyaları indirmeden önce oku, adımları sırayla uygula.

### 1. Dosyaları klasörün köküne getir

Kullanıcının açık olduğu klasör, ikinci beynin kendisi olacak. Dosyalar bu
klasörün **köküne** gelmeli, alt klasöre değil. Önce klasörde ne olduğuna bak.

- **Klasör boşsa:**
  `git clone https://github.com/ahmetdemircid/ikinci-beyin .`
- **Klasörde yalnızca editörün oluşturduğu şeyler varsa** (`.claude/`, `.vscode/`):
  `git clone ... .` boş olmayan klasörde çalışmaz. Şunu kullan:
  `git init`, `git remote add origin https://github.com/ahmetdemircid/ikinci-beyin`,
  `git pull origin master`.
- **Klasörde kullanıcının kendi dosyaları varsa:** hiçbir dosyanın üstüne yazma.
  Repoyu klasör dışında geçici bir yere klonla, yalnızca `.claude/skills/`
  klasörünü buraya kopyala, geçici kopyayı kaldır.
- **Git kurulu değilse:**
  `https://github.com/ahmetdemircid/ikinci-beyin/archive/refs/heads/master.zip`
  dosyasını indir, içindeki `ikinci-beyin-master/` klasörünün içeriğini köke aç.

### 2. Kullanıcıya teknik ayrıntı gösterme

Commit geçmişi, dosya listesi, komut çıktısı özetleme. İndirmenin bittiğini
tek cümleyle söyle.

### 3. Röportajı hemen başlat

Kullanıcıdan `/reload-skills` ya da `/kurulum` yazmasını isteme. Bu oturumda
`.claude/skills/kurulum/SKILL.md` dosyasını oku ve oradaki adımları uygula.
O dosyadaki `${CLAUDE_SKILL_DIR}` yolu `.claude/skills/kurulum` demektir.
