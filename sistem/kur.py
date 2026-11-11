"""Ikinci beyin: hafiza ve kanca kurulumu. Kurulum skill'i ve sistemi-guncelle calistirir; elle de calisir.

  python sistem/kur.py              kur (tekrar calistirmak guvenli: var olani bozmaz, eksigi tamamlar)
  python sistem/kur.py --kontrol    sadece durumu raporla, hicbir dosyaya yazma
  python sistem/kur.py --sistem-skilleri   sistem skill'lerini .agents/skills'e yeniden kopyala (guncelleme sonrasi)

Ne yapar:
  1. hafiza/otomatik/ (MEMORY.md), gunluk/, references/kural-adaylari.md yoksa olusturur.
  2. .claude/settings.local.json: autoMemoryDirectory (bu klasorun tam yolu) + SessionStart/SessionEnd kancasi.
     Dosyadaki diger ayarlara dokunmaz, sadece eksik olani ekler.
  3. .codex/hooks.json ve .agents/hooks.json (Codex ve agy kancalari), ayni sekilde birlestirerek.
  4. .claude/skills altindaki skill'leri .agents/skills'e kopyalar (sadece orada olmayanlar).
  5. Python ve 'claude' komutunu kontrol eder. 'claude' yoksa gunluk yazilmaz, bunu soyler.
Bu klasorun yolu ayar dosyalarina yazilir; o dosyalar kisisel oldugu icin .gitignore'dadir.
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
KANCA = KOK / "sistem" / "hafiza" / "kanca.py"
DURUM = KOK / "sistem" / "hafiza" / "durum.json"
def _sistem_skilleri():
    """Sistem skill'leri tek yerden: sistem/sistem-dosyalari.txt (guncelle.py ile ayni liste)."""
    try:
        satirlar = (KOK / "sistem" / "sistem-dosyalari.txt").read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    return [s.strip().rstrip("/").split("/")[-1] for s in satirlar if s.strip().startswith(".claude/skills/")]


SISTEM_SKILLERI = _sistem_skilleri()
ATLA = shutil.ignore_patterns("__pycache__", "node_modules", ".venv", "venv", ".git")
WIN = os.name == "nt"

rapor = []   # (durum, metin)  durum: "tamam" | "eklendi" | "uyari"


def yaz_rapor(durum, metin):
    rapor.append((durum, metin))


def python_adi():
    """Kanca komutunda kullanilacak Python adi. Bosluklu tam yol yerine PATH'teki ad (agy tirnak sevmiyor)."""
    adaylar = ["python", "py", "python3"] if WIN else ["python3", "python"]
    for ad in adaylar:
        yol = shutil.which(ad)
        if not yol:
            continue
        try:
            cikti = subprocess.run([yol, "-c", "import sys;print(sys.version_info[0])"],
                                   capture_output=True, text=True, timeout=20).stdout.strip()
        except Exception:
            continue
        if cikti == "3":
            return ad
    return None


def json_oku(yol):
    if not yol.exists():
        return {}
    try:
        return json.loads(yol.read_text(encoding="utf-8-sig") or "{}")
    except json.JSONDecodeError:
        return None


def json_yaz(yol, veri, kontrol):
    if kontrol:
        return
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps(veri, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def bizim_mi(girdi):
    return "kanca.py" in json.dumps(girdi, ensure_ascii=False)


def olay_ekle(kancalar, olay, komut_girdisi):
    """Claude ve Codex bicimi: {"Olay": [{"hooks": [{type, command}]}]}. Bizimki varsa dokunma."""
    liste = kancalar.setdefault(olay, [])
    if any(bizim_mi(g) for g in liste):
        return False
    liste.append({"hooks": [komut_girdisi]})
    return True


def klasorler(kontrol):
    otomatik = KOK / "hafiza" / "otomatik"
    gerekli = {
        otomatik / "MEMORY.md": "# Hafıza dizini\n\nHer satır bir hafıza dosyasını gösterir. Kalıcı tercih ve kurallar burada.\n",
        KOK / "references" / "kural-adaylari.md": "# Kural adayları (onay bekler, onaysız uygulanmaz)\n",
    }
    for yol, icerik in gerekli.items():
        if yol.exists():
            continue
        if not kontrol:
            yol.parent.mkdir(parents=True, exist_ok=True)
            yol.write_text(icerik, encoding="utf-8")
        yaz_rapor("eklendi", f"{yol.relative_to(KOK).as_posix()} oluşturuldu")
    if not (KOK / "gunluk").is_dir():
        if not kontrol:
            (KOK / "gunluk").mkdir()
        yaz_rapor("eklendi", "gunluk/ oluşturuldu")
    # Ozetci "kurulum" anindan once degisen eski oturumlari ozetlemez. Ani simdi sabitle.
    if not DURUM.exists():
        if not kontrol:
            DURUM.write_text(json.dumps({"kurulum": dt.datetime.now().isoformat(timespec="seconds"),
                                         "oturumlar": {}, "bekleyen": {}}, indent=1), encoding="utf-8")
        yaz_rapor("eklendi", "özetçi başlangıç anı kaydedildi (eski oturumlar özetlenmez)")


def claude_ayari(py, kontrol):
    yol = KOK / ".claude" / "settings.local.json"
    veri = json_oku(yol)
    if veri is None:
        yaz_rapor("uyari", ".claude/settings.local.json okunamadı (bozuk JSON). Dokunmadım, elle düzeltilmeli.")
        return
    degisti = False
    hafiza = (KOK / "hafiza" / "otomatik").as_posix()
    mevcut = veri.get("autoMemoryDirectory")
    if not mevcut:
        veri["autoMemoryDirectory"] = hafiza
        degisti = True
        yaz_rapor("eklendi", "Claude'un hafızası bu klasöre bağlandı (hafiza/otomatik)")
    elif Path(mevcut.replace("~", str(Path.home()), 1)).resolve() != Path(hafiza).resolve():
        yaz_rapor("uyari", f"Claude'un hafızası başka bir yere ayarlı ({mevcut}). Dokunmadım.")
    kancalar = veri.setdefault("hooks", {})
    for olay, arg in (("SessionStart", "baslangic"), ("SessionEnd", "bitis")):
        komut = {"type": "command", "command": f'{py} "$CLAUDE_PROJECT_DIR/sistem/hafiza/kanca.py" {arg}',
                 "timeout": 10}
        if olay_ekle(kancalar, olay, komut):
            degisti = True
            yaz_rapor("eklendi", f"Claude kancası: {olay}")
    if degisti:
        json_yaz(yol, veri, kontrol)
    else:
        yaz_rapor("tamam", "Claude ayarı zaten kurulu")


def codex_ayari(py, kontrol):
    yol = KOK / ".codex" / "hooks.json"
    veri = json_oku(yol)
    if veri is None:
        yaz_rapor("uyari", ".codex/hooks.json okunamadı (bozuk JSON). Dokunmadım.")
        return
    kancalar = veri.setdefault("hooks", {})
    yeni = []
    for olay, arg in (("SessionStart", "baslangic"), ("Stop", "stop"), ("SessionEnd", "bitis")):
        komut = f'{py} "{KANCA.as_posix()}" {arg} codex'
        if olay_ekle(kancalar, olay, {"type": "command", "command": komut, "commandWindows": komut}):
            yeni.append(olay)
    if yeni:
        json_yaz(yol, veri, kontrol)
        yaz_rapor("eklendi", "Codex kancaları yazıldı. Codex'te bir kez /hooks yazıp onaylaman gerekiyor")
    else:
        yaz_rapor("tamam", "Codex kancaları zaten kurulu")


def agy_ayari(py, kontrol):
    yol = KOK / ".agents" / "hooks.json"
    veri = json_oku(yol)
    if veri is None:
        yaz_rapor("uyari", ".agents/hooks.json okunamadı (bozuk JSON). Dokunmadım.")
        return
    kanca = KANCA.as_posix()
    if " " in kanca:
        kanca = f'"{kanca}"'
        yaz_rapor("uyari", "Klasör yolunda boşluk var; agy kancası tırnaklı yazıldı, agy'de çalışmazsa "
                           "klasörü boşluksuz bir yola taşıyıp bu betiği yeniden çalıştır")
    eklendi = False
    for ad, olay, arg in (("hafiza-baslangic", "SessionStart", "baslangic"), ("hafiza-stop", "Stop", "stop")):
        if ad in veri or any(bizim_mi(v) and olay in v for v in veri.values() if isinstance(v, dict)):
            continue
        veri[ad] = {olay: [{"type": "command", "command": f"{py} {kanca} {arg} agy", "timeout": 15}]}
        eklendi = True
    if eklendi:
        json_yaz(yol, veri, kontrol)
        yaz_rapor("eklendi", "agy kancaları yazıldı")
    else:
        yaz_rapor("tamam", "agy kancaları zaten kurulu")


def skill_kopyala(kontrol, sistemi_yenile):
    kaynak, hedef = KOK / ".claude" / "skills", KOK / ".agents" / "skills"
    if not kaynak.is_dir():
        return
    kopyalanan = []
    for d in sorted(p for p in kaynak.iterdir() if p.is_dir()):
        h = hedef / d.name
        yenile = sistemi_yenile and d.name in SISTEM_SKILLERI
        if h.exists() and not yenile:
            continue
        if not kontrol:
            if h.exists():
                shutil.rmtree(h)
            shutil.copytree(d, h, ignore=ATLA)
        kopyalanan.append(d.name)
    if kopyalanan:
        yaz_rapor("eklendi", f"Codex/agy için skill kopyası (.agents/skills): {', '.join(kopyalanan)}")
    else:
        yaz_rapor("tamam", "Skill kopyaları zaten eşit")


def denetim(py):
    if sys.version_info < (3, 8):
        yaz_rapor("uyari", f"Python {sys.version.split()[0]} eski. 3.8 ve üstü gerekiyor.")
    if not py:
        yaz_rapor("uyari", "Kanca için Python komutu bulunamadı (python / py / python3). "
                           "Python'u kurarken 'Add python.exe to PATH' kutusunu işaretle, sonra bu betiği yeniden çalıştır.")
    if shutil.which("claude"):
        yaz_rapor("tamam", "'claude' komutu var: oturum kapanınca günlük kendiliğinden yazılır")
    else:
        komut = ("irm https://claude.ai/install.ps1 | iex   (PowerShell)" if WIN
                 else "curl -fsSL https://claude.ai/install.sh | bash")
        yaz_rapor("uyari", "'claude' komutu bulunamadı. Klasör, hafıza ve skill'ler çalışır ama günlük yazılmaz. "
                           f"Çözüm: terminalde Claude Code'un komutunu kur: {komut}")


def main():
    kontrol = "--kontrol" in sys.argv
    sistemi_yenile = "--sistem-skilleri" in sys.argv
    py = python_adi()
    klasorler(kontrol)
    if py:
        claude_ayari(py, kontrol)
        codex_ayari(py, kontrol)
        agy_ayari(py, kontrol)
    skill_kopyala(kontrol, sistemi_yenile)
    denetim(py)
    baslik = "KONTROL (hiçbir dosya değişmedi)" if kontrol else "KURULUM"
    print(f"{baslik}: {KOK}")
    isaret = {"tamam": "[tamam]", "eklendi": "[eklendi]", "uyari": "[UYARI]"}
    for durum, metin in rapor:
        print(f"{isaret[durum]} {metin}")
    if any(d == "eklendi" for d, _ in rapor) and not kontrol:
        print("Kancalar yeni oturumda devreye girer. Bu oturumu kapatıp yenisini aç.")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
