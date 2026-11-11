"""Skill esitleme kontrolu (modelsiz). .claude/skills ile .agents/skills arasindaki farki bulur.

Tasarim: junction yok; hangi arac skill'i guncellerse obur klasoru de ayni icerikle gunceller.
Bu betik sadece farki bulur ve uyari metni dondurur, hicbir dosyayi degistirmez.

Kullanim:  python -I skill_fark.py [kok]      (kok verilmezse klasor koku)
Istisna:   sistem/skill-istisna.txt  -> bilerek tek tarafta duran skill adlari, satir basina bir tane.
"""
import os
import sys
from pathlib import Path

KASA = Path(__file__).resolve().parent.parent
ATLA = {"node_modules", "__pycache__", ".venv", "venv", ".git"}  # excalidraw node_modules: 3174 dosya, 55 sn
ISTISNA = Path(__file__).resolve().parent / "skill-istisna.txt"
EN_FAZLA = 12  # uyari satirinda gosterilecek en fazla ad


def tara(klasor):
    dosyalar = {}
    for kok, alt, adlar in os.walk(klasor):
        alt[:] = [a for a in alt if a not in ATLA]
        for ad in adlar:
            p = Path(kok) / ad
            dosyalar[p.relative_to(klasor).as_posix()] = p
    return dosyalar


def ayni(a, b):
    try:
        sa, sb = a.stat(), b.stat()
        if sa.st_size != sb.st_size:
            return False
        return a.read_bytes() == b.read_bytes()
    except OSError:
        return False


def istisnalar():
    try:
        return {s.strip() for s in ISTISNA.read_text(encoding="utf-8").splitlines()
                if s.strip() and not s.strip().startswith("#")}
    except OSError:
        return set()


def kisa(adlar):
    adlar = sorted(adlar)
    ek = f" (+{len(adlar) - EN_FAZLA})" if len(adlar) > EN_FAZLA else ""
    return ", ".join(adlar[:EN_FAZLA]) + ek


def fark(kok):
    c, g = Path(kok) / ".claude" / "skills", Path(kok) / ".agents" / "skills"
    if not c.is_dir() and not g.is_dir():
        return None
    a = tara(c) if c.is_dir() else {}
    b = tara(g) if g.is_dir() else {}
    skill = lambda r: r.split("/")[0] if "/" in r else None  # kokteki tek dosyalar (.gitkeep) skill degil
    sa = {skill(r) for r in a} - {None}
    sb = {skill(r) for r in b} - {None}
    haric = istisnalar()
    sadece_c, sadece_g = sa - sb - haric, sb - sa - haric

    farkli = {}  # skill -> "claude" | "agents" (hangi tarafin farkli dosyasi daha yeni)
    for r in (set(a) | set(b)):
        s = skill(r)
        if s is None or s not in sa & sb:
            continue
        if r in a and r in b:
            if ayni(a[r], b[r]):
                continue
            yeni = "claude" if a[r].stat().st_mtime >= b[r].stat().st_mtime else "agents"
        else:
            yeni = "claude" if r in a else "agents"  # dosya tek tarafta: o taraf eklemis
        if farkli.get(s) not in (None, yeni):
            yeni = "iki taraf"
        farkli[s] = yeni

    if not (sadece_c or sadece_g or farkli):
        return None
    satirlar = ["SKILL FARKI (.claude/skills <-> .agents/skills, modelsiz kontrol):"]
    if sadece_c:
        satirlar.append(f"- sadece .claude'da: {kisa(sadece_c)}")
    if sadece_g:
        satirlar.append(f"- sadece .agents'ta: {kisa(sadece_g)}")
    if farkli:
        satirlar.append("- icerik farkli: " + kisa(f"{s} ({y} dosya tarihi yeni; icerik eski olabilir, once farka bak)" if y != "iki taraf"
                                                   else f"{s} (iki tarafta da degisiklik)"
                                                   for s, y in farkli.items()))
    satirlar.append("Ilk cevabinda kullaniciya tek satirla soyle. Kendiliginden esitleme; kullanici onaylarsa "
                    "yeni tarafi obur klasore kopyala. Bilerek tek tarafta duran skill sistem/skill-istisna.txt'ye yazilir.")
    return "\n".join(satirlar)


if __name__ == "__main__":
    metin = fark(sys.argv[1] if len(sys.argv) > 1 else KASA)
    if metin:
        print(metin)
