# Vlastiti dijagrami za Predavanje01 (GOP struktura, vremenska crta generativnih modela).
# Uporaba: python3 dijagrami/P01_dijagrami.py  -> zapisuje u slike/
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams["font.family"] = "DejaVu Sans"
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "slike"))
PL = (58/255, 48/255, 104/255); SV = (108/255, 96/255, 176/255)
NG = (196/255, 120/255, 20/255); SI = (110/255, 118/255, 128/255)

# ---------- GOP struktura ----------
seq = list("IBBPBBPBBPBBI")
boje = {"I": PL, "P": SV, "B": (0.82, 0.80, 0.90)}
fig, ax = plt.subplots(figsize=(11, 3.3))
for k, t in enumerate(seq):
    ax.add_patch(FancyBboxPatch((k, 0), 0.8, 1.2, boxstyle="round,pad=0.02,rounding_size=0.08",
                 fc=boje[t], ec="white", lw=1.5))
    ax.text(k + 0.4, 0.6, t, ha="center", va="center", fontsize=18, weight="bold",
            color="white" if t != "B" else PL)
    ax.text(k + 0.4, -0.3, str(k), ha="center", va="center", fontsize=10, color=SI)
# reference P -> prethodni I/P
refs = [(3, 0), (6, 3), (9, 6)]
for dst, src in refs:
    ax.add_patch(FancyArrowPatch((src + 0.55, 1.25), (dst + 0.25, 1.25),
                 connectionstyle="arc3,rad=-0.45", arrowstyle="-|>", mutation_scale=14, color=NG, lw=1.6))
# B -> oba susjeda (jedan primjer)
for s in (0, 3):
    ax.add_patch(FancyArrowPatch((s + 0.4, -0.05), (1.4, -0.05),
                 connectionstyle="arc3,rad=0.5" if s == 0 else "arc3,rad=-0.5",
                 arrowstyle="-|>", mutation_scale=12, color=SI, lw=1.3, ls="--"))
ax.annotate("GOP (Group of Pictures)", xy=(6.2, 2.35), ha="center", fontsize=12, color=PL, weight="bold")
ax.plot([0, 11.8], [2.1, 2.1], color=PL, lw=1.2)
ax.plot([0, 0], [2.0, 2.2], color=PL, lw=1.2); ax.plot([11.8, 11.8], [2.0, 2.2], color=PL, lw=1.2)
ax.set_xlim(-0.3, 13.2); ax.set_ylim(-0.9, 2.7); ax.axis("off")
leg = [("I", "intra — samostalno kodiran okvir (kao slika)"),
       ("P", "predviđen iz prethodnog I/P okvira"),
       ("B", "predviđen iz prethodnog i sljedećeg okvira")]
fig.savefig("gop_struktura.png", dpi=200, bbox_inches="tight", transparent=True)
plt.close(fig)

# ---------- vremenska crta generativnih modela ----------
dog = [(2014, "GAN", 1), (2017, "Deepfake", -1),
       (2019, "StyleGAN\nnepostojeća\nlica", 1), (2021, "C2PA", -1),
       (2022, "Difuzijski\nmodeli", 1),
       (2023, "\u201ePapa\nu jakni\u201c", -1),
       (2024, "Generativni\nvideo", 1), (2025, "Video\nsa zvukom", -1),
       (2026, "EU AI Act\nčl. 50", 1)]
fig, ax = plt.subplots(figsize=(12, 4.6))
ax.plot([2013.4, 2026.6], [0, 0], color=PL, lw=2.5)
for g, t, s in dog:
    c = NG if "C2PA" in t or "AI Act" in t else SV
    ax.plot([g, g], [0, 0.55 * s], color=c, lw=1.2)
    ax.plot(g, 0, "o", ms=9, color=c, mec="white", mew=1.5)
    ax.text(g, 0.62 * s, t, ha="center", va="bottom" if s > 0 else "top", fontsize=14, color="black")
    ax.text(g, -0.13 * s, str(g), ha="center", va="top" if s > 0 else "bottom", fontsize=13, color=SI, weight="bold")
ax.set_xlim(2013.3, 2026.7); ax.set_ylim(-1.75, 1.75); ax.axis("off")
fig.savefig("ai_vremenska_crta.png", dpi=200, bbox_inches="tight", transparent=True)
plt.close(fig)
print("ok")
