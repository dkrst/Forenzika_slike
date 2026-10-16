# Vlastite ilustracije za Predavanje03 (Formati zapisa digitalne slike).
# Uporaba: python3 dijagrami/P03_dijagrami.py  -> zapisuje u slike/ (datoteke p03_*)
#
# Testne slike su iz paketa scikit-image (skimage.data) i slobodne su za uporabu.
# Skripta usput generira i stvarne datoteke u svim formatima, iz kojih se
# ocitavaju velicine navedene na slajdovima.

import io
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, FancyBboxPatch
import cv2
from PIL import Image
from skimage import data

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.size"] = 12
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "slike"))

PL = (58/255, 48/255, 104/255)
SV = (108/255, 96/255, 176/255)
NG = (196/255, 120/255, 20/255)
SI = (110/255, 118/255, 128/255)
SLIKA = data.coffee()                      # 600 x 400, RGB


def spremi(fig, ime, dpi=130):
    kw = {"pil_kwargs": {"quality": 92}} if ime.endswith(".jpg") else {}
    fig.savefig(ime, dpi=dpi, bbox_inches="tight", facecolor="white", **kw)
    plt.close(fig)
    print("  ", ime)


def prikazi(ax, img, naslov=None, **kw):
    if img.ndim == 2:
        ax.imshow(img, cmap="gray", vmin=0, vmax=255, **kw)
    else:
        ax.imshow(img, **kw)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if naslov:
        ax.set_title(naslov, fontsize=12)


def jpeg_krug(img, q, subsampling=2):
    """Spremi u JPEG i vrati (dekodirana slika, broj bajtova)."""
    buf = io.BytesIO()
    Image.fromarray(img).save(buf, "JPEG", quality=q, subsampling=subsampling)
    n = buf.tell(); buf.seek(0)
    return np.asarray(Image.open(buf).convert("RGB")), n


# ---------------------------------------------------------------- struktura datoteke
def struktura_datoteke():
    fig, ax = plt.subplots(figsize=(12, 2.9))
    dijelovi = [("potpis\n(magic number)", 1.5, (0.86, 0.84, 0.92)),
                ("zaglavlje\nširina, visina, dubina,\nprostor boja, kompresija", 2.9, (0.93, 0.91, 0.97)),
                ("metapodaci\nEXIF, XMP, ICC profil", 2.6, (1.0, 0.95, 0.86)),
                ("podaci o pikselima\n(sažeti ili ne)", 5.0, (0.90, 0.93, 0.90))]
    x = 0
    for ime, w, boja in dijelovi:
        ax.add_patch(FancyBboxPatch((x, 0), w, 1.25, boxstyle="round,pad=0.02,rounding_size=0.05",
                                    fc=boja, ec=SI, lw=1.2))
        ax.text(x + w/2, 0.62, ime, ha="center", va="center", fontsize=11.5, color="black")
        x += w + 0.12
    ax.annotate("", xy=(x - 0.12, -0.3), xytext=(0, -0.3),
                arrowprops=dict(arrowstyle="->", color=SI, lw=1.2))
    ax.text((x - 0.12)/2, -0.55, "redoslijed bajtova u datoteci", ha="center", fontsize=11, color=SI)
    ax.set_xlim(-0.2, x); ax.set_ylim(-0.95, 1.45); ax.axis("off")
    spremi(fig, "p03_struktura_datoteke.png")


# ---------------------------------------------------------------- podjela formata
def podjela_formata():
    fig, ax = plt.subplots(figsize=(12, 4.6))

    def kut(x, y, w, h, naslov, tekst, boja):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                    fc=boja, ec=SI, lw=1.2))
        ax.text(x + w/2, y + h - 0.22, naslov, ha="center", va="top", fontsize=12.5,
                weight="bold", color=PL)
        ax.text(x + w/2, y + h - 0.60, tekst, ha="center", va="top", fontsize=10.5, color="black",
                linespacing=1.45)

    ax.text(5.0, 4.35, "Formati zapisa digitalne slike", ha="center", fontsize=14,
            weight="bold", color=PL)
    kut(0.0, 2.35, 3.1, 1.70, "bez sažimanja", "svaki piksel opisan\nzasebno\n\nBMP, TIFF, PPM", (0.92, 0.95, 0.92))
    kut(3.45, 2.35, 3.1, 1.70, "sa sažimanjem", "slika zapisana\nmatematičkim algoritmom", (0.93, 0.91, 0.97))
    kut(6.9, 2.35, 3.1, 1.70, "RAW", "izravno očitanje\nsenzora\n\nCR3, NEF, ARW, DNG", (1.0, 0.95, 0.86))
    kut(2.2, 0.15, 3.1, 1.70, "bez gubitka", "informacija se\nu cijelosti čuva\n\nPNG, GIF, TIFF LZW", (0.93, 0.91, 0.97))
    kut(5.65, 0.15, 3.1, 1.70, "s gubitkom", "dio informacije\ntrajno se odbacuje\n\nJPEG, WebP, HEIC", (0.93, 0.91, 0.97))
    for x0, x1 in [(5.0, 3.75), (5.0, 7.2)]:
        ax.add_patch(FancyArrowPatch((x0, 2.35), (x1, 1.85), arrowstyle="-", color=SI, lw=1.2,
                                     connectionstyle="angle,angleA=-90,angleB=180,rad=0"))
    ax.set_xlim(-0.2, 10.2); ax.set_ylim(-0.05, 4.7); ax.axis("off")
    spremi(fig, "p03_podjela_formata.png")


# ---------------------------------------------------------------- velicine u formatima
def velicine():
    img = SLIKA
    pil = Image.fromarray(img)
    sirovo = img.size
    mjere = []

    def vel(spremi_fn):
        buf = io.BytesIO(); spremi_fn(buf); return buf.tell()

    mjere.append(("BMP", vel(lambda b: pil.save(b, "BMP")), "bez sažimanja"))
    mjere.append(("TIFF", vel(lambda b: pil.save(b, "TIFF")), "bez sažimanja"))
    mjere.append(("TIFF LZW", vel(lambda b: pil.save(b, "TIFF", compression="tiff_lzw")), "bez gubitka"))
    mjere.append(("PNG", vel(lambda b: pil.save(b, "PNG")), "bez gubitka"))
    mjere.append(("GIF", vel(lambda b: pil.convert("P", palette=Image.ADAPTIVE, colors=256).save(b, "GIF")), "bez gubitka, 256 boja"))
    for q in (95, 75, 50, 10):
        mjere.append((f"JPEG Q={q}", vel(lambda b, q=q: pil.save(b, "JPEG", quality=q, subsampling=2)), "s gubitkom"))

    fig, ax = plt.subplots(figsize=(11, 4.4))
    imena = [m[0] for m in mjere][::-1]
    vrij = [m[1]/1024 for m in mjere][::-1]
    boje = [NG if "JPEG" in m[0] else (SV if m[2] != "bez sažimanja" else PL) for m in mjere][::-1]
    ax.barh(imena, vrij, color=boje, height=0.62)
    for i, (v, m) in enumerate(zip(vrij, [m for m in mjere][::-1])):
        ax.text(v + 8, i, f"{v:,.0f} kB   ({sirovo/m[1]:.1f}:1)", va="center", fontsize=11)
    ax.axvline(sirovo/1024, color=SI, ls="--", lw=1.2)
    ax.text(sirovo/1024, -1.15, "sirovi podaci: 703 kB", ha="center", va="center",
            fontsize=10.5, color=SI)
    ax.set_xlim(0, sirovo/1024*1.42); ax.set_xticks([]); ax.set_ylim(-1.7, len(imena) - 0.3)
    for s in ["top", "right", "bottom"]:
        ax.spines[s].set_visible(False)
    ax.set_title("ista slika (600 × 400) u različitim formatima", fontsize=13)
    spremi(fig, "p03_velicine.png")
    return mjere


# ---------------------------------------------------------------- RLE i Huffman
def rle_huffman():
    fig, ax = plt.subplots(1, 2, figsize=(13, 3.4))
    # RLE
    niz = [200]*7 + [60]*5 + [200]*4
    a = ax[0]
    for i, v in enumerate(niz):
        a.add_patch(Rectangle((i, 1.1), 1, 0.8, fc=(v/255, v/255, v/255), ec="white", lw=1))
    a.text(8, 2.25, f"{len(niz)} piksela = {len(niz)} bajtova", ha="center", fontsize=12, color=PL)
    parovi = [(7, 200), (5, 60), (4, 200)]
    x = 0
    for n, v in parovi:
        a.add_patch(FancyBboxPatch((x, 0.0), n - 0.1, 0.72, boxstyle="round,pad=0.01,rounding_size=0.08",
                                   fc=(1.0, 0.95, 0.86), ec=NG, lw=1.2))
        a.text(x + (n - 0.1)/2, 0.36, f"({n}, {v})", ha="center", va="center", fontsize=12)
        x += n
    a.text(8, -0.5, "3 para = 6 bajtova", ha="center", fontsize=12, color=NG)
    a.set_xlim(-0.3, 16.3); a.set_ylim(-0.85, 2.6); a.axis("off")
    a.set_title("RLE — ponavljanje istih vrijednosti", fontsize=13)

    # Huffman
    a = ax[1]
    sim = [("A", 0.45, "0"), ("B", 0.25, "10"), ("C", 0.20, "110"), ("D", 0.10, "111")]
    a.text(0.02, 0.88, "simbol      vjerojatnost      kôd", fontsize=12, color=PL, family="DejaVu Sans Mono")
    for i, (s, p, k) in enumerate(sim):
        y = 0.70 - i*0.145
        a.text(0.05, y, f"{s}", fontsize=13, family="DejaVu Sans Mono")
        a.add_patch(Rectangle((0.26, y - 0.012), p*0.42, 0.055, fc=SV, ec="none"))
        a.text(0.26 + p*0.42 + 0.015, y, f"{p:.2f}", fontsize=11.5, va="baseline")
        a.text(0.72, y, k, fontsize=13, family="DejaVu Sans Mono", color=NG)
    a.text(0.02, 0.07, "česti simboli dobivaju kraće kodove\nprosječno 1,85 bita umjesto 2 bita",
           fontsize=11.5, color=SI)
    a.set_xlim(0, 1); a.set_ylim(0, 1); a.axis("off")
    a.set_title("Huffmanovo kodiranje — učestalost simbola", fontsize=13)
    fig.tight_layout()
    spremi(fig, "p03_rle_huffman.png")


# ---------------------------------------------------------------- PNG filtri
def png_filtri():
    g = cv2.cvtColor(SLIKA, cv2.COLOR_RGB2GRAY).astype(int)
    sub = g[120:320, 150:450]
    razlika = np.zeros_like(sub)
    razlika[:, 1:] = sub[:, 1:] - sub[:, :-1]          # filtar "Sub"
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.2),
                           gridspec_kw={"width_ratios": [1, 1, 1.15]})
    prikazi(ax[0], sub.astype(np.uint8), "izvorne vrijednosti")
    ax[1].imshow(np.clip(razlika + 128, 0, 255), cmap="gray", vmin=0, vmax=255)
    ax[1].set_xticks([]); ax[1].set_yticks([])
    for s in ax[1].spines.values():
        s.set_visible(False)
    ax[1].set_title("razlika od lijevog susjeda", fontsize=12)
    ax[2].hist(sub.ravel(), bins=64, range=(-128, 255), color=PL, alpha=0.75, label="izvorne")
    ax[2].hist(razlika.ravel(), bins=64, range=(-128, 255), color=NG, alpha=0.8, label="razlike")
    ax[2].set_yticks([]); ax[2].legend(frameon=False, fontsize=10.5)
    ax[2].set_title("raspodjela vrijednosti", fontsize=12)
    for s in ["top", "right", "left"]:
        ax[2].spines[s].set_visible(False)
    fig.tight_layout()
    spremi(fig, "p03_png_filtri.png")


# ---------------------------------------------------------------- GIF paleta
def gif_paleta():
    pil = Image.fromarray(SLIKA)
    p256 = pil.convert("P", palette=Image.ADAPTIVE, colors=256).convert("RGB")
    p16d = pil.convert("P", palette=Image.ADAPTIVE, colors=16, dither=Image.FLOYDSTEINBERG).convert("RGB")
    p16 = pil.convert("P", palette=Image.ADAPTIVE, colors=16, dither=Image.NONE).convert("RGB")
    y, x, h, w = 60, 280, 150, 220
    c = lambda im: np.asarray(im)[y:y+h, x:x+w]
    fig, ax = plt.subplots(1, 4, figsize=(13, 2.9))
    prikazi(ax[0], c(pil), "izvornik (16,7 mil. boja)")
    prikazi(ax[1], c(p256), "256 boja")
    prikazi(ax[2], c(p16), "16 boja, bez ditheringa")
    prikazi(ax[3], c(p16d), "16 boja, dithering")
    fig.tight_layout()
    spremi(fig, "p03_gif_paleta.jpg")


# ---------------------------------------------------------------- JPEG kvalitete
def jpeg_kvalitete():
    y, x, h, w = 95, 300, 130, 175
    fig, ax = plt.subplots(2, 4, figsize=(13, 5.0))
    prikazi(ax[0, 0], SLIKA, "izvornik")
    prikazi(ax[1, 0], SLIKA[y:y+h, x:x+w], None, interpolation="nearest")
    for k, q in enumerate([75, 25, 10]):
        dek, n = jpeg_krug(SLIKA, q)
        prikazi(ax[0, k+1], dek, f"Q = {q}   ({n/1024:.0f} kB)")
        prikazi(ax[1, k+1], dek[y:y+h, x:x+w], None, interpolation="nearest")
    fig.tight_layout()
    spremi(fig, "p03_jpeg_kvalitete.jpg")


# ---------------------------------------------------------------- poduzorkovanje kroma
def krom_poduzorkovanje():
    # fini uzorak: tanke pruge koje se razlikuju samo po boji, uz priblizno jednaku svjetlinu
    n = 96
    img = np.zeros((n, n, 3), np.uint8)
    img[:, :] = (150, 150, 150)
    for k in range(0, n, 4):
        img[:, k:k+2] = (205, 95, 95)
        img[:, k+2:k+4] = (70, 145, 150)
    img[:n//2] = img[:n//2][:, ::-1]
    for k in range(0, n, 6):
        img[k:k+3, :n//2] = (90, 170, 90)
    vel = lambda a: cv2.resize(a, (300, 300), interpolation=cv2.INTER_NEAREST)
    fig, ax = plt.subplots(1, 3, figsize=(12, 4.0))
    prikazi(ax[0], vel(img), "izvornik")
    for k, (sub, ime) in enumerate([(0, "4:4:4 — puna kroma"), (2, "4:2:0 — kroma na ¼")]):
        dek, n_b = jpeg_krug(img, 95, subsampling=sub)
        prikazi(ax[k+1], vel(dek), f"{ime}   ({n_b} B)")
    fig.tight_layout()
    spremi(fig, "p03_krom_poduzorkovanje.png")


# ---------------------------------------------------------------- JPEG blokovi 8x8
def jpeg_blokovi():
    y, x, h, w = 120, 150, 64, 64
    izr = SLIKA[y:y+h, x:x+w]
    dek, _ = jpeg_krug(SLIKA, 8)
    izr_q = dek[y:y+h, x:x+w]
    fig, ax = plt.subplots(1, 2, figsize=(9.5, 4.8))
    for a, im, naslov in [(ax[0], izr, "izvornik"), (ax[1], izr_q, "JPEG Q = 8")]:
        prikazi(a, im, naslov, interpolation="nearest")
        for k in range(0, w+1, 8):
            a.axvline(k - 0.5, color=(1, 1, 1, 0.45), lw=0.8)
            a.axhline(k - 0.5, color=(1, 1, 1, 0.45), lw=0.8)
    fig.tight_layout()
    spremi(fig, "p03_jpeg_blokovi.jpg")


# ---------------------------------------------------------------- kvantizacijske tablice
def kvant_tablice():
    pil = Image.fromarray(SLIKA)
    fig, ax = plt.subplots(1, 3, figsize=(13, 4.2))
    for k, q in enumerate([90, 50, 10]):
        buf = io.BytesIO(); pil.save(buf, "JPEG", quality=q); buf.seek(0)
        t = np.array(Image.open(buf).quantization[0]).reshape(8, 8)
        ax[k].imshow(np.log1p(t), cmap="YlOrBr", vmin=0, vmax=np.log1p(255))
        for i in range(8):
            for j in range(8):
                ax[k].text(j, i, str(t[i, j]), ha="center", va="center", fontsize=8.5,
                           color="white" if t[i, j] > 90 else "black")
        ax[k].set_xticks([]); ax[k].set_yticks([])
        ax[k].set_title(f"Q = {q}", fontsize=13)
    fig.suptitle("kvantizacijske tablice za kanal svjetline (lijevo gore: niske frekvencije)",
                 fontsize=12, y=0.03)
    fig.tight_layout()
    spremi(fig, "p03_kvant_tablice.png")


# ---------------------------------------------------------------- RAW: mozaik i razvijena slika
def raw_razvijanje():
    img = SLIKA
    maska = np.zeros_like(img)
    maska[0::2, 0::2, 0] = 1
    maska[0::2, 1::2, 1] = 1; maska[1::2, 0::2, 1] = 1
    maska[1::2, 1::2, 2] = 1
    sirovo = (img * maska).sum(axis=2).astype(np.uint8)
    dem = cv2.cvtColor(sirovo, cv2.COLOR_BayerBG2RGB)
    topla = np.clip(dem.astype(float) * np.array([1.18, 1.0, 0.82]), 0, 255).astype(np.uint8)
    hladna = np.clip(dem.astype(float) * np.array([0.85, 1.0, 1.25]), 0, 255).astype(np.uint8)
    y, x, h, w = 60, 180, 220, 300
    c = lambda a: a[y:y+h, x:x+w]
    fig, ax = plt.subplots(1, 4, figsize=(13, 2.9))
    prikazi(ax[0], c(sirovo), "sirovo očitanje senzora")
    prikazi(ax[1], c(dem), "razvijeno, neutralno")
    prikazi(ax[2], c(topla), "topliji balans bijele")
    prikazi(ax[3], c(hladna), "hladniji balans bijele")
    fig.tight_layout()
    spremi(fig, "p03_raw_razvijanje.jpg")


# ---------------------------------------------------------------- ugradena slicica
def thumbnail_trag():
    img = SLIKA.copy()
    th = cv2.resize(img, (160, 107), interpolation=cv2.INTER_AREA)   # sličica snimljena prije izmjene
    izm = img.copy()
    izm[150:330, 60:260] = cv2.GaussianBlur(izm[150:330, 60:260], (0, 0), 9)
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.2),
                           gridspec_kw={"width_ratios": [1.4, 1.4, 0.75]})
    prikazi(ax[0], img, "izvorna fotografija")
    prikazi(ax[1], izm, "izmijenjena fotografija")
    prikazi(ax[2], th, "ugrađena sličica u EXIF-u")
    fig.tight_layout()
    spremi(fig, "p03_thumbnail.jpg")


if __name__ == "__main__":
    for fn in [struktura_datoteke, podjela_formata, velicine, rle_huffman, png_filtri,
               gif_paleta, jpeg_kvalitete, krom_poduzorkovanje, jpeg_blokovi,
               kvant_tablice, raw_razvijanje, thumbnail_trag]:
        fn()
