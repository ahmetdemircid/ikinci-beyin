"""Hook giris noktasi (Claude Code, Codex, agy). Agir is yapmaz: kuyruga bir satir yazar,
gerekirse arka plan iscisini (ozetci.py) baslatir ve hemen doner.

Kullanim:  python kanca.py <olay> [arac]
  olay: baslangic | bitis | stop        arac: claude (varsayilan) | codex | agy

  Claude  SessionStart -> baslangic        SessionEnd -> bitis
  Codex   SessionStart -> baslangic codex  SessionEnd -> bitis codex   Stop -> stop codex
  agy     SessionStart -> baslangic agy    Stop -> stop agy   (agy'de SessionEnd yok)

bitis  : kuyruga "bitti" isaretiyle yaz + isciyi baslat (hemen islenir)
stop   : sadece kuyruga yaz (her cevapta gelir; oturum 10 dk bosta kalinca islenir)
baslangic: kuyruga yazmaz, isciyi baslatir (yetisme: bekleyen ve coken oturumlar)
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

BURASI = Path(__file__).resolve().parent
KUYRUK = BURASI / "kuyruk.jsonl"


def isciyi_baslat():
    pyw = Path(sys.executable).with_name("pythonw.exe")
    exe = str(pyw) if pyw.exists() else sys.executable
    komut = [exe, "-I", str(BURASI / "ozetci.py")]
    ortak = dict(stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                 stderr=subprocess.DEVNULL, close_fds=True)
    if os.name != "nt":
        subprocess.Popen(komut, start_new_session=True, **ortak)
        return
    bayrak = (subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
              | subprocess.CREATE_NO_WINDOW | subprocess.BELOW_NORMAL_PRIORITY_CLASS)
    try:
        subprocess.Popen(komut, creationflags=bayrak | subprocess.CREATE_BREAKAWAY_FROM_JOB, **ortak)
    except OSError:
        subprocess.Popen(komut, creationflags=bayrak, **ortak)  # is nesnesi breakaway'e izin vermiyorsa


def main():
    # Dongu korumasi: ozetcinin kendi model cagrisi hook tetiklerse hicbir sey yapma.
    if os.environ.get("IKINCI_BEYIN_OZETCI") == "1":
        return
    olay = sys.argv[1] if len(sys.argv) > 1 else ""
    arac = sys.argv[2] if len(sys.argv) > 2 else "claude"
    # Otomasyon eleme: Claude'un actigi kabuktan baslayan agy -p / codex exec (CLAUDECODE=1 miras kalir).
    # Claude'un kendi hook'unda bu kontrol yapilmaz; orada otomasyon 'entrypoint' ile elenir.
    if arac in ("codex", "agy") and os.environ.get("CLAUDECODE") == "1":
        return
    try:
        girdi = json.load(sys.stdin)
    except Exception:
        girdi = {}
    if arac == "agy":
        oturum, dosya = girdi.get("conversationId", ""), girdi.get("transcriptPath", "")
    else:
        oturum, dosya = girdi.get("session_id", ""), girdi.get("transcript_path", "")
    if dosya.startswith("\\\\?\\"):
        dosya = dosya[4:]
    if olay in ("bitis", "stop") and oturum and dosya:
        satir = json.dumps({"arac": arac, "oturum": oturum, "dosya": dosya,
                            "bitti": olay == "bitis", "t": round(time.time())}, ensure_ascii=False)
        with open(KUYRUK, "a", encoding="utf-8") as f:
            f.write(satir + "\n")
    if olay in ("bitis", "baslangic"):
        isciyi_baslat()
    if olay == "baslangic":
        skill_farki_bas(arac)


def skill_farki_bas(arac):
    # Ayri dosya, istege bagli: yoksa ya da hata verirse oturum etkilenmez. stdout -> modele baglam.
    # Claude/Codex: duz metin. agy: JSON ister (duz metinde "failed to unmarshal" verip atar);
    # bicim resmi dokumandan: antigravity.google/docs/hooks SessionStart. metadata alani kullanilmaz (bilinen panik).
    try:
        sys.path.insert(0, str(BURASI.parent))
        import skill_fark
        metin = skill_fark.fark(skill_fark.KASA)
        if not metin:
            return
        if arac == "agy":
            print(json.dumps({"injectSteps": [{"systemMessage": {"systemMessage": metin}}]}, ensure_ascii=False))
        else:
            print(metin)
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # hook asla oturumu bozmaz
