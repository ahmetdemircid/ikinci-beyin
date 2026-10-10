# Kurulum talimatı

Bu dosya, kullanıcının "bunu oku ve bu klasöre kur" dediği yapay zeka asistanı
için yazıldı. Adımları sırayla uygula.

## 1. Dosyaları klasörün köküne getir

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

## 2. Kullanıcıya teknik ayrıntı gösterme

Commit geçmişi, dosya listesi, komut çıktısı özetleme. İndirmenin bittiğini
tek cümleyle söyle.

## 3. Röportajı hemen başlat

Kullanıcıdan `/reload-skills` ya da `/kurulum` yazmasını isteme. Bu oturumda
`.claude/skills/kurulum/SKILL.md` dosyasını oku ve oradaki adımları uygula.
O dosyadaki `${CLAUDE_SKILL_DIR}` yolu `.claude/skills/kurulum` demektir.
