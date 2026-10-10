---
name: beceri-ogren
description: Kullanıcıyla birlikte yapılmış ve beğenilmiş bir işi kalıcı bir skill'e çevirir, sonra yeni bir oturumda kullanıcının kendi cümlesiyle deneyip çalıştığını kanıtlar. Kullanıcı "bunu kalıcı yap", "bunu skill yap", "bunu öğren", "bir dahakine tek cümleyle yap", "bunu her seferinde böyle yap" dediğinde ya da Claude'un "kalıcı hale getireyim mi?" sorusuna evet dediğinde kullan.
---

# Beceri öğren

Amacın şu: kullanıcının bir kere birlikte yaptığı işi, bir dahakine tek
cümleyle aynı kalitede yapabilmek. Skill, işin nasıl yapıldığını anlatan
kalıcı bir tariftir: `.claude/skills/{ad}/SKILL.md`.

Kullanıcı yeni başlamış olabilir. "Skill" kelimesini ilk kez duyuyorsa bir
cümleyle açıkla: "Skill, bu işi nasıl yaptığımızı yazdığım kalıcı bir tarif.
Bir dahakine sadece söylemen yeterli, aynı şekilde yaparım."

## Kesin kurallar

- **Önce gerçek iş, sonra skill.** Skill'in kaynağı bu oturumda gerçekten
  yapılmış ve kullanıcının beğendiği bir iştir. Kullanıcı süreci sadece
  anlattıysa önce o işi bir kez birlikte yap, çıktıyı göster, beğenmeden
  skill yazma.
- **Uydurma adım ekleme.** Skill'e sadece yapılan işte gerçekten olan adımları
  ve kullanıcının söylediği kuralları yaz.
- **Sistem skill'lerinin adını kullanma:** `kurulum`, `gunu-ac`, `gunu-kapat`,
  `saglik-kontrolu`, `sistemi-guncelle`, `beceri-ogren`, `paket-kur`.
- **Var olan skill'in üstüne yazma.** Aynı adda skill varsa önce
  `archives/{ad}-{YYYYAAGG}/` altına kopyala ve kullanıcıya söyle.
- **Test geçmeden "hazır" deme.**

## 1. İşi topla

Bu konuşmadan şunları çıkar ve kullanıcıya kısa bir liste olarak göster:

- **Ne iş:** tek cümle.
- **Girdi:** her seferinde değişen şey (bir not, bir link, bir dosya, bir konu).
- **Adımlar:** gerçekten yapılan adımlar, sırayla.
- **Kurallar:** kullanıcının bu işte söylediği tercihler ve düzeltmeler
  ("daha kısa", "emoji yok", "şu başlıkla başla").
- **İyi çıktı:** kullanıcının beğendiği son çıktı.

Eksik olan varsa en fazla üç soru sor, tek tek. Genelde şunlar eksik kalır:
- "Bu işi bana hangi cümleyle söylersin?" (en az iki örnek cümle al)
- "Çıktı nereye gitsin: sohbete mi, bir dosyaya mı?"
- "İyi çıktıyı kötüsünden ne ayırır?"

## 2. Skill'i yaz

**Ad:** kısa, küçük harf, tireli, Türkçe karaktersiz (ör. `linkedin-postu`,
`haftalik-rapor`). Kullanıcıya öner, beğenmezse onun dediğini kullan.

**Yazma yolu:**
- Oturumda Anthropic'in `skill-creator` skill'i varsa onu kullan; skill
  yazmanın güncel kurallarını o bilir. Bu dosyadaki kuralları ona ek olarak
  uygula.
- Yoksa kendin yaz. `.claude/skills/{ad}/SKILL.md` şu yapıda olsun:

```
---
name: {ad}
description: {Ne yapar, tek cümle}. Kullanıcı "{örnek cümle 1}", "{örnek cümle 2}" dediğinde ya da {hangi durumda} kullan.
---

# {İşin adı}

{Amaç, iki cümle.}

## Girdi
{Her seferinde ne verilir. Verilmezse ne sorulur.}

## Adımlar
1. ...

## Kurallar
- {kullanıcının tercihleri ve düzeltmeleri}

## Çıktı
{Biçim ve yer. Örnek için ornek-cikti.md dosyasına bak.}
```

`description` alanı en önemli satır: yeni oturumda Claude skill'i bu satıra
bakarak seçer. Kullanıcının kendi cümlelerini içine koy.

**Örnek çıktı:** kullanıcının beğendiği çıktıyı olduğu gibi
`.claude/skills/{ad}/ornek-cikti.md` dosyasına koy. Skill'de "çıktı bu
örnekteki dil ve biçimde olsun" diye ona atıf yap.

`.claude/` klasörüne yazarken Claude Code ayrıca izin sorabilir. Yazmadan
önce kullanıcıya söyle: "Şimdi skill dosyasını yazacağım, Claude Code izin
sorarsa onayla."

## 3. Yeni oturumda dene

Skill'i yazan sen olduğun için ne yapacağını zaten biliyorsun; bu yüzden
burada denemek bir şey kanıtlamaz. Deneme, bu konuşmayı hiç görmemiş yeni bir
oturumda yapılır: kullanıcının yarın açacağı oturumla birebir aynı koşul.

1. Test cümlesi hazırla: kullanıcının 1. adımda verdiği örnek cümlelerden
   biri + yeni bir test girdisi (ilk işteki girdinin aynısı olmasın). Skill'in
   adını cümleye **yazma**; skill'in kendi kendine seçilip seçilmediğini de
   ölçüyoruz. Skill dosyaya kaydediyorsa cümlenin sonuna şunu ekle: "Bu bir
   deneme, kaydedeceğin dosyanın adının başına deneme- yaz."
2. Kullanıcıya söyle: "Şimdi bu konuşmayı görmeyen yeni bir oturumda
   deneyeceğim. Bir iki dakika sürer, limitinden bir miktar kullanır."
3. Bu klasörde terminalde çalıştır:

   ```
   claude -p "{test cümlesi}" --output-format stream-json --verbose --permission-mode acceptEdits --permission-prompts none
   ```

   Komutu tek başına çalıştır: başına `cd` ekleme (zaten bu klasördesin),
   sonuna `>` ile dosyaya yönlendirme ya da `|` ekleme. Birleşik komut izin
   kuralına uymaz, kullanıcıya gereksiz izin sorulur ya da reddedilir.
   Claude Code izin sorarsa kullanıcı onaylar. `--permission-prompts none`
   hata verirse (eski sürüm) o parçayı çıkarıp tekrar dene.
4. Çıktıyı oku ve iki şeye bak:
   - **Seçildi mi?** Akışta adı `Skill` olan ve `{ad}` skill'ini çağıran bir
     araç kullanımı var mı?
   - **İyi mi?** Sonuç `ornek-cikti.md` ile aynı biçimde, aynı kurallarla mı?
5. Kullanıcıya göster: test cümlesi, sonucun kendisi (kısaysa tamamı, uzunsa
   ilk kısmı), iki sorunun cevabı.

**Geçmezse:** seçilmediyse `description`'ı kullanıcının cümlelerine yaklaştır;
kötü çıktıysa eksik kuralı ya da adımı ekle. Sonra bir kez daha dene. İkinci
denemede de geçmezse dur, neyin tutmadığını kullanıcıya açıkça söyle,
"hazır" deme.

**`claude` komutu çalışmıyorsa** (Codex'tesin ya da komut bulunamadı): bir alt
ajana sadece test cümlesini ver, skill'in adını ve bu konuşmayı anlatma.
Kullanıcıya bu denemenin yeni oturum kadar güvenilir olmadığını söyle ve ilk
gerçek kullanımda sonucu birlikte kontrol etmeyi öner.

## 4. Kaydet

1. `AGENTS.md`'de `<!-- sistem:basla -->` işaretinin **üstündeki** "Senin
   skill'lerin" tablosuna bir satır ekle: ad, ne yapar, nasıl söylenir. Bölüm
   yoksa işaretin hemen üstüne oluştur. İşaretlerin arasına yazma, sistem
   güncellemesi orayı yeniden yazar.
2. `references/is-gunlugu.md`'de bu işin satırlarına `skill: {ad}` ekle.
3. `context/work.md` "Tekrar eden işler" listesinde bu iş varsa yanına
   `(skill oldu: {ad})` yaz.
4. Git varsa kayıt al: `git add -A` ve
   `git commit -m "Yeni skill: {ad}"`.

## 5. Kullanıcıya söyle

Kısa tut:

```
Hazır: {ad}

Bundan sonra şöyle demen yeterli: "{örnek cümle}"
Yeni oturumda denedim: {seçildi / çıktı örnekle uyumlu}.
Bir şeyi beğenmezsen söyle, tarifi güncellerim.
```
