"""Ikinci beyin: sistem guncellemesi. Dosya isini model degil bu betik yapar; model sadece anlatir ve onay alir.

  python sistem/guncelle.py --kontrol        yeni surumu indir, neyin degisecegini yaz, HICBIR dosyaya dokunma
  python sistem/guncelle.py --uygula         geri donus noktasi + arsiv al, sadece sistem dosyalarini degistir
  python sistem/guncelle.py --geri-al        son guncellemeyi geri al

Secenekler:
  --kaynak YOL   yeni surum: klasor ya da zip (verilmezse GitHub'dan indirilir)
  --hedef YOL    guncellenecek ikinci beyin klasoru (verilmezse bu betigin klasoru)

Kurallar (bozulmamasi gerekenler):
  - Sadece YENI surumun sistem/sistem-dosyalari.txt listesindekiler ve AGENTS.md'nin isaretli bolumu degisir.
  - Kisisel dosyalara dokunulmaz. Iskeletten sadece hedefte HIC olmayan, doldurma alani ({{...}}) icermeyen
    dosyalar eklenir. .gitignore'a eksik satir eklenir, var olan satir silinmez.
  - Degismeden once: Git varsa kayit, her durumda archives/sistem-{tarih}/onceki/ altina kopya.
  - Kisisel dosyada degisiklik gerektiren gecisler betikte yapilmaz; sistem/bekleyen-gecisler.txt'ye yazilir,
    model kullaniciya sorup uygular ve satiri siler.
Cikis kodu: 0 basarili ya da zaten guncel, 1 hata (hicbir sey degismedi ya da yarim kaldiysa yazar), 2 kullanim hatasi.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

ZIP_ADRESI = "https://github.com/ahmetdemircid/ikinci-beyin/archive/refs/heads/master.zip"
LISTE = "sistem/sistem-dosyalari.txt"
SURUM = ".claude/skills/sistemi-guncelle/surum.txt"
GECISLER = ".claude/skills/sistemi-guncelle/gecisler"
ISKELET = ".claude/skills/kurulum/iskelet"
SON = "sistem/son-guncelleme.json"
BEKLEYEN = "sistem/bekleyen-gecisler.txt"   # kisisel: model gecisi yapinca satiri siler
BASLA, BITIR = "<!-- sistem:basla -->", "<!-- sistem:bitir -->"
ISKELETTEN_EKLENMEZ = ("hafiza/",)          # hafiza klasorunu kur.py ve gecis notlari kurar
GITIGNORE = ["CLAUDE.local.md", ".claude/settings.local.json", ".env", ".codex/hooks.json",
             ".agents/hooks.json", "sistem/hafiza/durum.json", "sistem/hafiza/kuyruk*.jsonl",
             "sistem/hafiza/kayit.log", "sistem/hafiza/parca-ozetleri/", "sistem/hafiza/.kilit", "__pycache__/"]
GIZLI = [".claude/settings.local.json", ".env", ".codex/hooks.json", ".agents/hooks.json"]
ATLA = shutil.ignore_patterns("__pycache__", "*.pyc")


class Hata(Exception):
    pass


DEGISTI = False   # hedefte ilk dosya degistiginde True (hata mesaji icin)


# ---------- yardimcilar ----------
def surum_anahtari(s):
    return tuple(int(x) for x in re.findall(r"\d+", s or "0")) or (0,)


def surum_oku(kok):
    yol = kok / SURUM
    if not yol.exists():
        return "0", []
    satirlar = [s.strip() for s in yol.read_text(encoding="utf-8").splitlines() if s.strip()]
    surum = satirlar[0] if satirlar else "0"
    bekleyen = [s.split(":", 1)[1].strip() for s in satirlar[1:]
                if s.startswith(("bekleyen-gecis:", "atlanan-gecis:"))]
    return surum, bekleyen


def bekleyen_oku(kok):
    """Bekleyen gecis surumleri: yeni dosya + eski bicim (surum.txt'deki atlanan-gecis satirlari)."""
    _, eski_bicim = surum_oku(kok)
    yol = kok / BEKLEYEN
    dosyada = []
    if yol.exists():
        dosyada = [x.split()[0] for x in yol.read_text(encoding="utf-8").splitlines()
                   if x.strip() and not x.lstrip().startswith("#")]
    return list(dict.fromkeys(eski_bicim + dosyada))


def liste_oku(kaynak):
    yol = kaynak / LISTE
    if not yol.exists():
        raise Hata(f"Yeni sürümde {LISTE} yok; bu kaynak güncelleme için uygun değil.")
    ogeler = []
    for s in yol.read_text(encoding="utf-8").splitlines():
        s = s.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("/") or ".." in s.split("/") or ":" in s:
            raise Hata(f"Listede güvensiz yol: {s}")
        ogeler.append(s)
    return ogeler


def icinde_mi(kok, yol):
    try:
        yol.resolve().relative_to(kok.resolve())
        return True
    except ValueError:
        return False


def ayni_mi(a, b):
    """Dosya ya da klasor icerigi ayni mi (pycache haric)."""
    if a.is_file() and b.is_file():
        return a.read_bytes() == b.read_bytes()
    if a.is_dir() and b.is_dir():
        return dosya_haritasi(a) == dosya_haritasi(b)
    return False


def dosya_haritasi(klasor):
    harita = {}
    for kok, alt, adlar in os.walk(klasor):
        alt[:] = [x for x in alt if x != "__pycache__"]
        for ad in adlar:
            if ad.endswith(".pyc"):
                continue
            p = Path(kok) / ad
            harita[p.relative_to(klasor).as_posix()] = p.read_bytes()
    return harita


def sistem_bolumu(metin):
    if metin.count(BASLA) != 1 or metin.count(BITIR) != 1:
        return None
    b, s = metin.index(BASLA), metin.index(BITIR)
    if b > s:
        return None
    return b, s + len(BITIR)


def git(hedef, *arg, kontrol=True):
    r = subprocess.run(["git", *arg], cwd=hedef, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if kontrol and r.returncode != 0:
        raise Hata(f"git {' '.join(arg)}: {(r.stderr or r.stdout).strip()[:300]}")
    return r


def git_var(hedef):
    return shutil.which("git") and (hedef / ".git").exists()


# ---------- kaynak ----------
def kaynak_hazirla(kaynak_arg, gecici):
    if kaynak_arg:
        yol = Path(kaynak_arg).resolve()
        if yol.is_dir():
            return yol
        if yol.is_file() and yol.suffix == ".zip":
            return zip_ac(yol, gecici)
        raise Hata(f"Kaynak bulunamadı: {kaynak_arg}")
    zip_yolu = gecici / "yeni.zip"
    try:
        with urllib.request.urlopen(ZIP_ADRESI, timeout=60) as r, open(zip_yolu, "wb") as f:
            shutil.copyfileobj(r, f)
    except Exception as e:
        raise Hata(f"Yeni sürüm indirilemedi ({type(e).__name__}: {e}). İnternet bağlantısını kontrol et.")
    return zip_ac(zip_yolu, gecici)


def zip_ac(zip_yolu, gecici):
    hedef = gecici / "acilan"
    with zipfile.ZipFile(zip_yolu) as z:
        for ad in z.namelist():
            if not icinde_mi(hedef, hedef / ad):
                raise Hata(f"Zip içinde güvensiz yol: {ad}")
        z.extractall(hedef)
    ustler = [p for p in hedef.iterdir() if p.is_dir()]
    if len(ustler) != 1:
        raise Hata("Zip beklenen düzende değil (tek üst klasör yok).")
    return ustler[0]


# ---------- plan ----------
def plan_cikar(hedef, kaynak):
    eski_surum, _ = surum_oku(hedef)
    eski_bekleyen = bekleyen_oku(hedef)
    yeni_surum, _ = surum_oku(kaynak)
    ogeler = liste_oku(kaynak)
    degisiklik = []   # (oge, durum) durum: yeni | degisecek | ayni
    for oge in ogeler:
        k, h = kaynak / oge, hedef / oge
        if not k.exists():
            raise Hata(f"Yeni sürümde listedeki dosya yok: {oge}")
        if not h.exists():
            degisiklik.append((oge, "yeni"))
        elif ayni_mi(k, h):
            degisiklik.append((oge, "ayni"))
        else:
            degisiklik.append((oge, "degisecek"))
    # AGENTS.md
    agents = "yok"
    hedef_agents = hedef / "AGENTS.md"
    if hedef_agents.exists():
        hm = hedef_agents.read_text(encoding="utf-8")
        km = (kaynak / ISKELET / "AGENTS.md").read_text(encoding="utf-8")
        hb, kb = sistem_bolumu(hm), sistem_bolumu(km)
        if kb is None:
            raise Hata("Yeni sürümün AGENTS.md şablonunda sistem işaretleri yok.")
        if hb is None:
            agents = "isaretsiz"
        else:
            agents = "ayni" if hm[hb[0]:hb[1]] == km[kb[0]:kb[1]] else "degisecek"
    # iskeletten yeni bos dosyalar
    iskelet_yeni = []
    isk = kaynak / ISKELET
    for p in sorted(isk.rglob("*")):
        if not p.is_file():
            continue
        goreli = p.relative_to(isk).as_posix()
        if goreli.startswith(ISKELETTEN_EKLENMEZ) or (hedef / goreli).exists():
            continue
        try:
            if "{{" in p.read_text(encoding="utf-8"):
                continue
        except UnicodeDecodeError:
            continue
        iskelet_yeni.append(goreli)
    # gecisler
    gecisler = []
    gk = kaynak / GECISLER
    if gk.is_dir():
        for p in sorted(gk.glob("*.md"), key=lambda x: surum_anahtari(x.stem)):
            if p.name.lower() == "readme.md":
                continue
            if surum_anahtari(p.stem) > surum_anahtari(eski_surum) or p.stem in eski_bekleyen:
                ilk = next((s.lstrip("# ").strip() for s in p.read_text(encoding="utf-8").splitlines()
                            if s.strip()), p.stem)
                gecisler.append((p.stem, ilk))
    return {"eski": eski_surum, "yeni": yeni_surum, "degisiklik": degisiklik, "agents": agents,
            "iskelet_yeni": iskelet_yeni, "gecisler": gecisler}


def plan_yaz(plan, hedef):
    print(f"Klasör: {hedef}")
    print(f"Sürüm: {plan['eski']} -> {plan['yeni']}")
    gruplar = {"yeni": "Eklenecek", "degisecek": "Değişecek"}
    for durum, baslik in gruplar.items():
        ogeler = [o for o, d in plan["degisiklik"] if d == durum]
        if ogeler:
            print(f"{baslik}:")
            for o in ogeler:
                print(f"  - {o}")
    agents = {"degisecek": "sistem bölümü değişecek (işaretler dışına dokunulmaz)", "ayni": "aynı",
              "isaretsiz": "İŞARET YOK: eski kurulum, betik dokunmaz, model elle yapmalı", "yok": "dosya yok"}
    print(f"AGENTS.md: {agents[plan['agents']]}")
    if plan["iskelet_yeni"]:
        print("Yeni boş dosyalar (sadece eksikse eklenir): " + ", ".join(plan["iskelet_yeni"]))
    if plan["gecisler"]:
        print("Kişisel dosyaya dokunan geçişler (ayrı onay ister, betik yapmaz):")
        for s, baslik in plan["gecisler"]:
            print(f"  - {s}: {baslik}  ({GECISLER}/{s}.md)")
    print("Dokunulmayacak: bilgilerin, projelerin, kararların, hafızan, günlüğün, kendi skill'lerin.")


def guncel_mi(plan):
    return (not any(d != "ayni" for _, d in plan["degisiklik"]) and plan["agents"] in ("ayni", "yok")
            and not plan["iskelet_yeni"] and surum_anahtari(plan["yeni"]) <= surum_anahtari(plan["eski"]))


# ---------- uygula ----------
def gitignore_tamamla(hedef):
    yol = hedef / ".gitignore"
    mevcut = yol.read_text(encoding="utf-8") if yol.exists() else ""
    satirlar = {s.strip() for s in mevcut.splitlines()}
    eksik = [s for s in GITIGNORE if s not in satirlar]
    if eksik:
        ek = ("" if not mevcut or mevcut.endswith("\n") else "\n") + "".join(s + "\n" for s in eksik)
        with open(yol, "a", encoding="utf-8", newline="\n") as f:
            f.write(ek)
    return eksik


def git_kayit(hedef, mesaj):
    """Gizli dosyalar daha once Git'e girmisse once takipten cikar (dosya diskte kalir), sonra kayit al."""
    takipte = git(hedef, "ls-files", "--", *GIZLI, kontrol=False).stdout.split()
    if takipte:
        git(hedef, "rm", "--cached", "-q", "--", *takipte)
    git(hedef, "add", "-A")
    kimlik = []
    if not git(hedef, "config", "user.email", kontrol=False).stdout.strip():
        kimlik = ["-c", "user.name=ikinci-beyin", "-c", "user.email=ikinci-beyin@localhost"]
    git(hedef, *kimlik, "commit", "-q", "--allow-empty", "-m", mesaj)
    return git(hedef, "rev-parse", "--short", "HEAD").stdout.strip(), takipte


def uygula(hedef, kaynak, plan):
    zaman = dt.datetime.now()
    arsiv = hedef / "archives" / f"sistem-{zaman:%Y%m%d-%H%M%S}"
    onceki = arsiv / "onceki"
    kayit = {"tarih": zaman.isoformat(timespec="seconds"), "eski": plan["eski"], "yeni": plan["yeni"],
             "arsiv": arsiv.relative_to(hedef).as_posix(), "degisen": [], "eklenen": [], "agents": False,
             "git": None}
    eksik_ignore = gitignore_tamamla(hedef)
    if git_var(hedef):
        kayit["git"], cikarilan = git_kayit(hedef, f"Guncelleme oncesi geri donus noktasi ({plan['eski']} -> {plan['yeni']})")
        print(f"Geri dönüş noktası (Git): {kayit['git']}")
        if cikarilan:
            print("Git takibinden çıkarıldı (dosyalar yerinde, kişisel ayar): " + ", ".join(cikarilan))
    else:
        print("Git yok: geri dönüş yalnızca arşivden.")
    onceki.mkdir(parents=True, exist_ok=True)
    # Once hepsini arsive al ve kaydi yaz, sonra degistir: arada hata olursa --geri-al calisir.
    for oge, durum in plan["degisiklik"]:
        if durum != "degisecek":
            continue
        h, a = hedef / oge, onceki / oge
        if h.is_dir():
            shutil.copytree(h, a, ignore=ATLA)
        else:
            a.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(h, a)
    if (hedef / "AGENTS.md").exists():
        shutil.copy2(hedef / "AGENTS.md", onceki / "AGENTS.md")
    kayit["degisen"] = [o for o, d in plan["degisiklik"] if d == "degisecek"]
    kayit["eklenen"] = [o for o, d in plan["degisiklik"] if d == "yeni"] + list(plan["iskelet_yeni"])
    kayit["agents"] = plan["agents"] == "degisecek"
    (hedef / SON).parent.mkdir(parents=True, exist_ok=True)
    (hedef / SON).write_text(json.dumps(kayit, ensure_ascii=False, indent=1), encoding="utf-8")
    global DEGISTI
    DEGISTI = True
    if eksik_ignore:
        print("Eklenen .gitignore satırları: " + ", ".join(eksik_ignore))
    for oge, durum in plan["degisiklik"]:
        if durum == "ayni":
            continue
        k, h = kaynak / oge, hedef / oge
        if not icinde_mi(hedef, h):
            raise Hata(f"Hedef klasör dışında yol: {oge}")
        if h.is_dir():
            shutil.rmtree(h)
        elif h.exists():
            h.unlink()
        h.parent.mkdir(parents=True, exist_ok=True)
        if k.is_dir():
            shutil.copytree(k, h, ignore=ATLA)
        else:
            shutil.copy2(k, h)
    if plan["agents"] == "degisecek":
        hm = (hedef / "AGENTS.md").read_text(encoding="utf-8")
        km = (kaynak / ISKELET / "AGENTS.md").read_text(encoding="utf-8")
        hb, kb = sistem_bolumu(hm), sistem_bolumu(km)
        (hedef / "AGENTS.md").write_text(hm[:hb[0]] + km[kb[0]:kb[1]] + hm[hb[1]:], encoding="utf-8", newline="")
    for goreli in plan["iskelet_yeni"]:
        h = hedef / goreli
        h.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(kaynak / ISKELET / goreli, h)
    if plan["gecisler"]:
        ilk = ("# Bekleyen gecisler: kullaniciya sorulup yapilinca satir silinir. Reddedilirse satir kalir,"
               " sonraki guncellemede yeniden sorulur.")
        govde = [ilk] + [f"{v}  {b}" for v, b in plan["gecisler"]]
        (hedef / BEKLEYEN).write_text(chr(10).join(govde) + chr(10), encoding="utf-8")
    print(f"Arşiv: {kayit['arsiv']}")
    print(f"Güncellendi: {plan['eski']} -> {plan['yeni']} ({len(kayit['degisen'])} değişti, "
          f"{len(kayit['eklenen'])} eklendi{', AGENTS.md sistem bölümü' if kayit['agents'] else ''})")
    kur_calistir(hedef)
    if plan["gecisler"]:
        print(f"SIRADAKİ: bekleyen geçişleri kullanıcıya tek tek sor ({BEKLEYEN}).")
    if plan["agents"] == "isaretsiz":
        print("SIRADAKİ: AGENTS.md'de sistem işaretleri yok; sistemi-guncelle skill'indeki 'işaretler yoksa' adımı.")


def kur_calistir(hedef):
    kur = hedef / "sistem" / "kur.py"
    if not kur.exists():
        return
    r = subprocess.run([sys.executable, "-I", str(kur), "--sistem-skilleri"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=180)
    print("--- kur.py ---")
    print((r.stdout or "").strip() or (r.stderr or "").strip())


# ---------- geri al ----------
def geri_al(hedef):
    yol = hedef / SON
    if not yol.exists():
        raise Hata("Geri alınacak güncelleme kaydı yok (sistem/son-guncelleme.json).")
    kayit = json.loads(yol.read_text(encoding="utf-8"))
    if kayit.get("geri_alindi"):
        raise Hata("Son güncelleme zaten geri alınmış.")
    arsiv = hedef / kayit["arsiv"]
    onceki = arsiv / "onceki"
    if not onceki.is_dir():
        raise Hata(f"Arşiv bulunamadı: {kayit['arsiv']}")
    kenar = arsiv / f"geri-alinan-{dt.datetime.now():%Y%m%d-%H%M%S}"
    tasinan, korunan = [], []
    for oge in kayit["degisen"] + kayit["eklenen"]:
        h = hedef / oge
        if oge in kayit["eklenen"] and oge.startswith("sistem/"):
            korunan.append(oge)      # kancalar bu dosyalara bagli; tasinirsa her oturumda hata verir
            continue
        if h.exists():
            (kenar / oge).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(h), str(kenar / oge))
            tasinan.append(oge)
        if oge in kayit["degisen"]:
            k = onceki / oge
            h.parent.mkdir(parents=True, exist_ok=True)
            if k.is_dir():
                shutil.copytree(k, h)
            elif k.exists():
                shutil.copy2(k, h)
    if kayit.get("agents"):
        eski = (onceki / "AGENTS.md").read_text(encoding="utf-8")
        simdi = (hedef / "AGENTS.md").read_text(encoding="utf-8")
        eb, sb = sistem_bolumu(eski), sistem_bolumu(simdi)
        if eb and sb:
            (hedef / "AGENTS.md").write_text(simdi[:sb[0]] + eski[eb[0]:eb[1]] + simdi[sb[1]:],
                                             encoding="utf-8", newline="")
    kayit["geri_alindi"] = dt.datetime.now().isoformat(timespec="seconds")
    yol.write_text(json.dumps(kayit, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Geri alındı: {kayit['yeni']} -> {kayit['eski']}")
    print(f"Yeni sürümün dosyaları kenara alındı: {kenar.relative_to(hedef).as_posix()}")
    if korunan:
        print("Yerinde bırakıldı (günlük kancaları bunlara bağlı): " + ", ".join(korunan))
    print("Kişisel dosyalara ve geçişlerle yapılan değişikliklere dokunulmadı.")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    kip = p.add_mutually_exclusive_group(required=True)
    kip.add_argument("--kontrol", action="store_true")
    kip.add_argument("--uygula", action="store_true")
    kip.add_argument("--geri-al", action="store_true")
    p.add_argument("--kaynak")
    p.add_argument("--hedef")
    a = p.parse_args()
    hedef = Path(a.hedef).resolve() if a.hedef else Path(__file__).resolve().parent.parent
    if not (hedef / ".claude").is_dir():
        print(f"HATA: {hedef} bir ikinci beyin klasörüne benzemiyor (.claude yok).")
        return 2
    if not a.geri_al and not (hedef / "AGENTS.md").exists():
        print("HATA: bu klasörde kurulum yapılmamış (AGENTS.md yok). Önce kurulum: /kurulum")
        return 2
    try:
        if a.geri_al:
            geri_al(hedef)
            return 0
        with tempfile.TemporaryDirectory(prefix="ikinci-beyin-") as g:
            kaynak = kaynak_hazirla(a.kaynak, Path(g))
            if kaynak.resolve() == hedef.resolve():
                raise Hata("Kaynak ile hedef aynı klasör.")
            plan = plan_cikar(hedef, kaynak)
            if guncel_mi(plan):
                print(f"Sistem zaten güncel ({plan['eski']}).")
                return 0
            plan_yaz(plan, hedef)
            if a.uygula:
                print("---")
                uygula(hedef, kaynak, plan)
        return 0
    except Exception as e:
        print(f"HATA: {e}" if isinstance(e, Hata) else f"HATA (beklenmeyen): {type(e).__name__}: {e}")
        print("Güncelleme yarıda kaldı: arşiv ve kayıt duruyor, '--geri-al' ile geri alınabilir." if DEGISTI
              else "Hiçbir sistem dosyası değişmedi.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
