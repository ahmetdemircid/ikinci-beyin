---
name: sistemi-guncelle
description: İkinci beyin sisteminin yeni sürümünü GitHub'dan çeker ya da son güncellemeyi geri alır. Sadece sistem skill'lerini (kurulum, gunu-ac, gunu-kapat, saglik-kontrolu, beceri-ogren, paket-kur, sistemi-guncelle) ve AGENTS.md'deki işaretli sistem bölümünü yeniler. Kişisel dosyalara (context/, projects/, decisions/, references/, kullanıcının kendi skill'leri ve kuralları) dokunmaz, eski hâli arşive kopyalar. Kullanıcı "/sistemi-guncelle", "sistemi güncelle", "yeni sürüm var mı", "ikinci beyni güncelle" dediğinde, ayrıca "güncellemeyi geri al" dediğinde kullan.
---

# Sistemi güncelle

Bu klasörde iki tür dosya var:

- **Sistem dosyaları:** herkeste aynı, yeni sürümle değişebilir. Bunlar:
  `.claude/skills/kurulum/`, `.claude/skills/gunu-ac/`,
  `.claude/skills/gunu-kapat/`, `.claude/skills/saglik-kontrolu/`,
  `.claude/skills/beceri-ogren/`, `.claude/skills/paket-kur/`,
  `.claude/skills/sistemi-guncelle/` ve `AGENTS.md` içinde
  `<!-- sistem:basla -->` ile `<!-- sistem:bitir -->` arasındaki bölüm.
- **Kişisel dosyalar:** geri kalan her şey. `context/`, `projects/`,
  `decisions/`, `references/`, `runs/`, `archives/`, `.claude/rules/`,
  kullanıcının kendi skill'leri, `AGENTS.md`'nin işaretler dışındaki kısmı.

Sistem skill'lerinin listesi sürümle büyüyebilir. Güncel liste her zaman
**yeni sürümdeki** bu dosyada yazandır; 3. adımdan itibaren onu esas al.

**Kişisel dosyalara bu akışta dokunma.** Tek istisna aşağıdaki "Geçiş"
adımıdır ve ayrı onay ister. Sistem dosyasının eski hâlini değiştirmeden önce
arşive kopyala.

Kullanıcı "güncellemeyi geri al" derse en alttaki "Geri alma" bölümüne git.

## 1. Yeni sürümü geçici alana indir

Bu klasörün DIŞINDA, işletim sisteminin geçici klasöründe boş bir klasör aç.
Şu dosyayı oraya indir ve aç:

`https://github.com/ahmetdemircid/ikinci-beyin/archive/refs/heads/master.zip`

İçinden `ikinci-beyin-master/` klasörü çıkar. Bundan sonra "yeni sürüm" bu
klasör demek. Git gerekmez. İndirme başarısız olursa dur, nedenini tek
cümleyle söyle, hiçbir dosyayı değiştirme.

## 2. Sürümleri karşılaştır

`.claude/skills/sistemi-guncelle/surum.txt` dosyasının ilk satırı sürümdür.
Bu klasördeki ile yeni sürümdekini karşılaştır.

- **Aynıysa:** "Sistem zaten güncel ({sürüm})" de, geçici klasörü kaldır, dur.
- **Bu klasörde `surum.txt` yoksa:** sistem, sürüm takibi eklenmeden önce
  kurulmuş. Güncellemeye devam et.

## 3. Ne değişecek, kullanıcıya göster ve onay al

Sistem dosyalarının her birini yeni sürümdekiyle karşılaştır. Kullanıcıya
kısa bir liste göster, teknik ayrıntı (diff) dökme:

```
Sürüm: {eski} -> {yeni}
Değişecek:
- gunu-kapat: {bir cümleyle ne değişti}
- AGENTS.md sistem bölümü: {bir cümleyle ne değişti}
Yeni eklenen: {varsa skill adı ve ne işe yaradığı}
Dokunulmayacak: senin bilgilerin, projelerin, kararların, kendi kuralların ve skill'lerin.
```

Sonra sor: "Güncelleyeyim mi?" Onay gelmeden hiçbir dosyayı değiştirme.

Kullanıcı bir sistem skill'ini kendisi değiştirmişse (yeni sürümde de eski
sürümde de olmayan satırlar varsa) bunu ayrıca söyle: "Bu dosyada senin
eklediğin satırlar var, güncelleme bunları değiştirecek; eski hâli arşivde
kalacak." Kişisel bir değişikliği kalıcı tutmak istiyorsa yeri
`.claude/rules/` ya da kendi adını verdiği ayrı bir skill'dir.

## 4. Geri dönüş noktası ve arşiv

1. **Git varsa önce kayıt al.** Kaydedilmemiş değişiklik varsa:
   `git add -A` ve `git commit -m "Guncelleme oncesi"`. Sonra o anki kaydın
   kısa kimliğini not et (`git rev-parse --short HEAD`); geri alma bu
   kayda döner. Kullanıcıya söyle: "Güncellemeden önce geri dönüş noktası
   aldım ({kimlik})."
2. `archives/sistem-{YYYYAAGG-SSDD}/` klasörü aç. Değişecek her sistem
   skill'inin klasörünü ve `AGENTS.md`'nin tamamını oraya kopyala. Git yoksa
   tek geri dönüş yolu bu arşivdir.

## 5. Uygula

- **Skill'ler:** değişen her sistem skill'inin klasörünü yeni sürümdekiyle
  değiştir. Yeni sürümde yeni bir sistem skill'i varsa ekle. Listede olmayan
  skill'lere (kullanıcının kendi skill'leri) dokunma.
- **AGENTS.md, işaretler varsa:** sadece `<!-- sistem:basla -->` ile
  `<!-- sistem:bitir -->` arasını (işaretler dahil), yeni sürümdeki
  `.claude/skills/kurulum/iskelet/AGENTS.md` dosyasının aynı bölümüyle değiştir.
  İşaretlerin dışındaki tek bir karaktere dokunma.
- **AGENTS.md, işaretler yoksa** (eski kurulum): kişisel kısımları ayır. Bunlar
  başlık, "Sen ... iş ortağısın" cümlesi, en üstteki hedef, kullanıcının
  itiraz ve iletişim tercihleri ve "Kullanıcının eklediği kurallar" bölümü.
  Yeni dosyayı şöyle kur: yeni şablonun işaretlerden önceki kısmını bu
  kişisel bilgilerle doldur, ardından yeni sistem bölümünü işaretleriyle
  ekle. Eski dosyadaki bir kural iki tarafa da uymuyorsa silme, "Kullanıcının
  eklediği kurallar" bölümüne olduğu gibi taşı. Sonuçta neyi nereye
  koyduğunu kullanıcıya göster.
- **Yeni sürümle gelen boş dosyalar:** yeni sürümün
  `.claude/skills/kurulum/iskelet/` klasöründe olup bu klasörde hiç olmayan
  dosyaları (ör. `references/is-gunlugu.md`) aynı yola kopyala. Var olan
  dosyaya dokunma. `AGENTS.md`'de işaretlerin üstünde "Senin skill'lerin"
  bölümü yoksa işaretin hemen üstüne şablondaki gibi ekle; bu, işaret
  dışına yapılan tek ekleme.
- **CLAUDE.md:** yeni sürümün `iskelet/CLAUDE.md`'si bu klasördekinden farklıysa
  değiştirme. Farkı göster ve sor.

## 5b. Geçiş (sadece yeni sürüm isterse)

Sistemin kuralı dosya düzenini sabit tutmaktır; neredeyse her güncelleme
kişisel dosyalara dokunmadan biter. Yeni sürümde
`.claude/skills/sistemi-guncelle/gecisler/` altında, bu klasördeki sürümden
yeni ve `{sürüm}.md` adlı bir dosya varsa o sürüm kişisel bir dosyada
değişiklik gerektiriyor demektir (ör. proje haritasına yeni sütun). O
dosyada neyin neden değiştiği yazar. Bu durumda:

1. Hangi kişisel dosyada neyin değişeceğini kullanıcıya önce/sonra örneğiyle
   göster. Teknik ayrıntı dökme, bir iki satırlık örnek yeter.
2. Ayrı onay iste: "Bu değişiklik senin dosyana dokunuyor. Yapayım mı?
   Hayır dersen sistem eski düzenle çalışmaya devam eder."
3. Onay gelirse önce dosyanın kopyasını `archives/sistem-{...}/kisisel/`
   altına al, sonra sadece tarif edilen değişikliği yap. İçerikteki hiçbir
   satırı silme, yeniden yazma ya da özetleme.
4. Hayır derse dokunma ve bunu `surum.txt`'nin ikinci satırına yaz:
   `atlanan-gecis: {sürüm}`. Sonraki güncellemede tekrar sorulur.

## 6. Kontrol et ve kaydet

1. `AGENTS.md`'de işaretler birer kez ve sırayla var mı, `{{` kalmış mı?
2. Sistem skill'lerinin her birinde `SKILL.md` var mı?
3. Geçici klasörü kaldır (sadece 1. adımda açtığın klasörü).
4. Git varsa: `git add -A` ve
   `git commit -m "Sistem guncellendi: {eski} -> {yeni}"`. Git'te ad ve e-posta
   yoksa sadece bu klasör için tanımla (`--global` kullanma). `git push` yapma.

## 7. Rapor

İki üç cümle yeter: hangi sürüme geçildi, ne değişti, eski hâl nerede
(`archives/sistem-.../`). Yeni bir sistem skill'i eklendiyse: "Yeni skill'in
görünmesi için yeni bir oturum aç."

## Geri alma

Kullanıcı "güncellemeyi geri al" derse:

1. `git log --oneline` içinde en son "Guncelleme oncesi" ya da ondan hemen
   önceki kaydı bul. Hangi kayda döneceğini ve o günden bu yana yapılan
   diğer kayıtları kullanıcıya göster.
2. Güncellemeden sonra kullanıcı başka iş de yaptıysa tüm klasörü geri
   sarma; o işler kaybolur. Bunun yerine sadece sistem dosyalarını (sistem
   skill'leri ve `AGENTS.md`'nin işaretli bölümü) ve geçiş adımında
   değişen kişisel dosyaları o kayıttaki hâline getir:
   `git checkout {kimlik} -- {dosya yolları}`. Sonra
   `git commit -m "Guncelleme geri alindi"`.
3. Git yoksa aynı dosyaları `archives/sistem-{...}/` altındaki kopyalardan
   geri koy.
4. "Eski sürüme döndüm. Yeni sürümdeki sorun düzelince tekrar güncelleyebilirsin."
   de. Yeni oturum açmasını söyle.
