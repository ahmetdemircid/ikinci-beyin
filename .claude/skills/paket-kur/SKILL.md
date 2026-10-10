---
name: paket-kur
description: AI Builder Kulübü'nden indirilen hazır sistem paketini (zip) bu klasöre kurar. Paketin içindekileri önce gösterir, onay alır, kişisel dosyalara dokunmaz, eski sürümü arşive kopyalar. Kullanıcı "paketi kur", "kulüpten indirdiğim dosyayı kur", "şu zip'i kur", "hazır sistemi yükle" dediğinde ya da klasöre bir paket zip'i bırakıp kurulmasını istediğinde kullan.
---

# Paket kur

Kulüp paketleri, Ahmet'in kendi kullandığı hazır skill ve sistemlerdir. Her
biri AI Builder Kulübü'ndeki ilgili dersin içinde zip olarak durur. Hangi
paketlerin olduğu `${CLAUDE_SKILL_DIR}/katalog.md` dosyasında yazıyor.

## Kesin kurallar

- **Sadece kullanıcının elindeki zip'i kurarsın.** Paketleri internetten
  indirmeye, başka yerde aramaya ya da katalogdaki bir sistemi kendin yazmaya
  çalışma. Zip yoksa kurulacak bir şey yoktur.
- **Kurarken paketin içindeki hiçbir betiği çalıştırma.** Sadece dosyaları
  yerine kopyalarsın. Bir betiğin çalışması gerekiyorsa bunu kurulumdan sonra
  kullanıcıya söylersin, o karar verir. `paket.md`'deki zararsız kontrolleri
  (bir programın kurulu olup olmadığını soran `ffmpeg -version` gibi sürüm
  sorguları) kullanıcının onayıyla çalıştırabilirsin.
- **Kişisel dosyalara dokunma:** `context/`, `projects/`, `decisions/`,
  `references/` (sadece `references/paketler.md`'ye satır eklenir),
  `.claude/rules/`.
- **Hiçbir şeyi silme.** Eski sürümün üstüne yazmadan önce arşive kopyala.

## 1. Zip'i bul

Kullanıcı yolu verdiyse onu kullan. Vermediyse bu klasörün kökünde ve
kullanıcının İndirilenler klasöründe adı `.zip` ile biten ve içinde
`paket.md` olan dosyaya bak. Birden fazla varsa listele, hangisi diye sor.
Bulamazsan kullanıcıya şunu söyle: "Paketi kulüpteki ilgili dersin altından
indir, bu klasöre bırak, sonra tekrar söyle."

## 2. Geçici alana aç ve oku

Zip'i bu klasörün **dışında**, işletim sisteminin geçici klasöründe boş bir
klasöre aç. İçinde `paket.md` yoksa dur: "Bu bir kulüp paketi değil" de.

`paket.md` şunları içerir: paket adı, sürüm, ne işe yaradığı, içindeki
skill'ler, gerekenler (ör. "ffmpeg kurulu olmalı"), kurulumdan sonra
yapılacaklar.

## 3. Göster ve onay al

```
Paket: {ad} ({sürüm})
Ne yapar: {bir cümle}
Kurulacak: {skill adları, birer satır}
Gerekenler: {varsa}
Bu klasörde aynı adda olan: {varsa, "eski hâli arşive kopyalanacak"}
```

Sonra sor: "Kurayım mı?" Onay gelmeden hiçbir dosyayı değiştirme.

## 4. Kur

1. Bu klasörde aynı adda bir skill varsa önce
   `archives/paket-{ad}-{YYYYAAGG}/` altına kopyala.
2. Paketteki `skills/` altındaki her klasörü `.claude/skills/` altına kopyala.
   Claude Code `.claude/` klasörüne yazarken izin sorabilir; önceden söyle.
3. `references/paketler.md` dosyasına bir satır ekle (dosya yoksa başlığıyla
   oluştur): `| {ad} | {sürüm} | {bugünün tarihi} | {skill adları} |`
4. `AGENTS.md`'de `<!-- sistem:basla -->` işaretinin üstündeki "Senin
   skill'lerin" tablosuna her skill için bir satır ekle, yanına `(kulüp
   paketi)` yaz.
5. Geçici klasörü kaldır (sadece 2. adımda açtığın klasörü).
6. Zip bu klasörün içindeyse `archives/paketler/` altına taşı; ileride
   yeniden kurmak gerekirse orada durur. İndirilenler gibi klasör dışındaki
   bir yerdeyse dokunma.
7. Git varsa: `git add -A` ve `git commit -m "Paket kuruldu: {ad} {sürüm}"`.

## 5. Kullanıcıya söyle

- Neyin kurulduğunu ve nasıl çağrılacağını, birer satır.
- `paket.md`'deki "kurulumdan sonra yapılacaklar" varsa onları sırayla.
- "Yeni skill'lerin kesin görünmesi için yeni bir oturum aç."

Paketin yeni sürümü kulüpte yayınlandığında aynı adımlar tekrar çalışır,
eski sürüm arşive iner.
