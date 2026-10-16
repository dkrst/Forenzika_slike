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
    """Okomiti prikaz dijelova datoteke; visine blokova priblizno prate njihov udio."""
    fig, ax = plt.subplots(figsize=(5.4, 7.4))
    dijelovi = [("potpis (magic number)", 0.85, (0.86, 0.84, 0.92)),
                ("zaglavlje\nširina, visina, dubina,\nprostor boja, kompresija", 1.95, (0.93, 0.91, 0.97)),
                ("metapodaci\nEXIF, XMP, ICC profil", 1.55, (1.0, 0.95, 0.86)),
                ("podaci o pikselima\n(sažeti ili ne)", 4.3, (0.90, 0.93, 0.90))]
    y = sum(d[1] for d in dijelovi) + 0.12*(len(dijelovi)-1)
    for ime, h, boja in dijelovi:
        y -= h
        ax.add_patch(FancyBboxPatch((0.55, y), 5.0, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc=boja, ec=SI, lw=1.2))
        ax.text(3.05, y + h/2, ime, ha="center", va="center", fontsize=13, color="black",
                linespacing=1.55)
        y -= 0.12
    uk = sum(d[1] for d in dijelovi) + 0.12*(len(dijelovi)-1)
    ax.annotate("", xy=(0.26, 0.0), xytext=(0.26, uk),
                arrowprops=dict(arrowstyle="->", color=SI, lw=1.3))
    ax.text(-0.02, uk/2, "redoslijed bajtova u datoteci", rotation=90, ha="center", va="center",
            fontsize=12, color=SI)
    ax.set_xlim(-0.35, 5.65); ax.set_ylim(-0.25, uk + 0.25); ax.axis("off")
    spremi(fig, "p03_struktura_datoteke.png")


# ---------------------------------------------------------------- podjela formata
def podjela_formata():
    fig, ax = plt.subplots(figsize=(12, 5.2))

    def kut(x, y, w, h, naslov, tekst, boja, fs=10.5):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                    fc=boja, ec=SI, lw=1.2))
        ax.text(x + w/2, y + h - 0.20, naslov, ha="center", va="top", fontsize=12.5,
                weight="bold", color=PL)
        ax.text(x + w/2, y + h - 0.62, tekst, ha="center", va="top", fontsize=fs, color="black",
                linespacing=1.45)

    GY, GH = 2.80, 2.15                      # gornji red
    DY, DH = 0.10, 1.90                      # donji red, odmaknut nize
    kut(0.0, GY, 3.1, GH, "bez sažimanja", "svaki piksel\nopisan zasebno\n\nBMP, TIFF, PPM", (0.92, 0.95, 0.92))
    kut(3.45, GY, 3.1, GH, "sa sažimanjem", "slika zapisana\nmatematičkim\nalgoritmom", (0.93, 0.91, 0.97))
    kut(6.9, GY, 3.1, GH, "RAW", "izravno očitanje senzora;\nformat ovisi o proizvođaču\n\n"
        "CR2, CR3 (Canon), NEF (Nikon),\nARW (Sony), RAF (Fuji),\nORF (Olympus), …",
        (1.0, 0.95, 0.86), fs=9.2)
    kut(2.2, DY, 3.1, DH, "bez gubitka", "informacija se\nu cijelosti čuva\n\nPNG, GIF, TIFF LZW", (0.93, 0.91, 0.97))
    kut(5.65, DY, 3.1, DH, "s gubitkom", "dio informacije\ntrajno se odbacuje\n\nJPEG, WebP, HEIC", (0.93, 0.91, 0.97))

    # lomljene strelice: od donjeg ruba "sa sazimanjem" do gornjih rubova dvaju blokova
    xs, ys = 5.0, GY
    ym = DY + DH + 0.40
    ax.plot([xs, xs], [ys, ym], color=SI, lw=1.4, solid_capstyle="round")
    for xc in (3.75, 7.20):
        ax.plot([xs, xc], [ym, ym], color=SI, lw=1.4, solid_capstyle="round")
        ax.add_patch(FancyArrowPatch((xc, ym), (xc, DY + DH), arrowstyle="-|>",
                                     mutation_scale=15, color=SI, lw=1.4))
    ax.set_xlim(-0.2, 10.2); ax.set_ylim(-0.05, 5.1); ax.axis("off")
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
    """Samo RLE; Huffmanov primjer je na slajdu kao tablica."""
    niz = [200]*7 + [60]*5 + [200]*4
    fig, a = plt.subplots(figsize=(7.4, 3.0))
    for i, v in enumerate(niz):
        a.add_patch(Rectangle((i, 1.15), 1, 0.85, fc=(v/255, v/255, v/255), ec=(0.5, 0.5, 0.5), lw=0.8))
        a.text(i + 0.5, 1.575, str(v), ha="center", va="center", fontsize=9,
               color="black" if v > 120 else "white")
    a.text(8, 2.35, f"{len(niz)} piksela = {len(niz)} bajtova", ha="center", fontsize=12.5, color=PL)
    parovi = [(7, 200), (5, 60), (4, 200)]
    x = 0
    for n, v in parovi:
        a.add_patch(FancyBboxPatch((x + 0.05, 0.05), n - 0.2, 0.75,
                                   boxstyle="round,pad=0.01,rounding_size=0.08",
                                   fc=(1.0, 0.95, 0.86), ec=NG, lw=1.2))
        a.text(x + n/2 - 0.05, 0.42, f"({n}, {v})", ha="center", va="center", fontsize=12.5)
        x += n
    a.text(8, -0.45, "3 para = 6 bajtova", ha="center", fontsize=12.5, color=NG)
    a.set_xlim(-0.3, 16.3); a.set_ylim(-0.8, 2.65); a.axis("off")
    spremi(fig, "p03_rle.png")


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


# ---------------------------------------------------------------- matricni zapis u boji
def matrica_rgb():
    """Slika u boji i uvecani isjecak s RGB vrijednostima piksela."""
    img = SLIKA
    y0, x0, n = 200, 380, 6          # izrez preko ruba, s velikim rasponom vrijednosti
    blok = img[y0:y0+n, x0:x0+n]
    fig = plt.figure(figsize=(11.5, 5.0))
    a1 = fig.add_axes([0.0, 0.08, 0.40, 0.84])
    prikazi(a1, img)
    a1.add_patch(Rectangle((x0, y0), n, n, fill=False, ec=(0.1, 0.2, 0.9), lw=2))
    a2 = fig.add_axes([0.45, 0.02, 0.55, 0.96])
    a2.set_xlim(-0.5, n - 0.5); a2.set_ylim(n - 0.5, -0.5)
    a2.set_xticks([]); a2.set_yticks([]); a2.axis("off")
    for i in range(n):
        for j in range(n):
            r, g, b = blok[i, j]
            a2.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fc=np.array([r, g, b])/255, ec="white", lw=0.6))
            svijetlo = 0.299*r + 0.587*g + 0.114*b > 125
            t = "k" if svijetlo else "w"
            a2.text(j, i - 0.25, f"{r:3d}", ha="center", va="center", fontsize=10.5,
                    color=(0.75, 0.1, 0.1) if svijetlo else (1, 0.55, 0.55), family="DejaVu Sans Mono")
            a2.text(j, i + 0.02, f"{g:3d}", ha="center", va="center", fontsize=10.5,
                    color=(0.05, 0.45, 0.1) if svijetlo else (0.55, 1, 0.6), family="DejaVu Sans Mono")
            a2.text(j, i + 0.27, f"{b:3d}", ha="center", va="center", fontsize=10.5,
                    color=(0.1, 0.2, 0.8) if svijetlo else (0.6, 0.75, 1), family="DejaVu Sans Mono")
    for (xa, ya), (xb, yb) in [((x0 + n, y0), (-0.5, -0.5)), ((x0 + n, y0 + n), (-0.5, n - 0.5))]:
        from matplotlib.patches import ConnectionPatch
        fig.add_artist(ConnectionPatch(xyA=(xa, ya), coordsA=a1.transData,
                                       xyB=(xb, yb), coordsB=a2.transData,
                                       color=(0.1, 0.2, 0.9), lw=1.0))
    spremi(fig, "p03_matrica_rgb.jpg")


# ---------------------------------------------------------------- BMP hex dump s bojama
def bmp_hex():
    """Hex zapis male BMP datoteke; bajtovi svakog piksela oznaceni njegovom bojom."""
    a = np.array([[[255, 0, 0], [255, 255, 255], [0, 0, 255]],
                  [[0, 255, 0], [0, 0, 0], [255, 255, 0]]], np.uint8)      # 3 x 2
    buf = io.BytesIO(); Image.fromarray(a).save(buf, "BMP")
    b = buf.getvalue()
    ZAG, SIR, RED = 54, 3, 12                      # zaglavlje, piksela po retku, bajtova po retku
    po_retku = 12
    n_red = (len(b) + po_retku - 1) // po_retku

    fig, ax = plt.subplots(figsize=(11.5, 3.6))
    dx, dy = 1.0, 1.0
    for i, bajt in enumerate(b):
        r, c = divmod(i, po_retku)
        x, y = 2.1 + c*dx, -r*dy
        ax.text(x, y, f"{bajt:02X}", ha="center", va="center", fontsize=12.5,
                family="DejaVu Sans Mono", zorder=3)
    # pozadine: zaglavlje
    for i in range(0, ZAG):
        r, c = divmod(i, po_retku)
        ax.add_patch(Rectangle((2.1 + c*dx - 0.46, -r*dy - 0.42), 0.92, 0.84,
                               fc=(0.92, 0.92, 0.94), ec="none", zorder=1))
    # pozadine: pikseli u vlastitoj boji, dopuna sivo
    for red in range(2):
        baza = ZAG + red*RED
        for p_i in range(SIR):
            off = baza + p_i*3
            bb, gg, rr = b[off], b[off+1], b[off+2]
            boja = np.array([rr, gg, bb]) / 255
            svijetlo = 0.299*rr + 0.587*gg + 0.114*bb > 128
            for k in range(3):
                r, c = divmod(off + k, po_retku)
                ax.add_patch(Rectangle((2.1 + c*dx - 0.48, -r*dy - 0.44), 0.96, 0.88,
                                       fc=boja, ec=(0.35, 0.35, 0.35), lw=0.6, zorder=2))
                ax.texts[off + k].set_color("black" if svijetlo else "white")
                ax.texts[off + k].set_zorder(4)
        for k in range(baza + 9, baza + 12):       # dopuna do 12 B
            r, c = divmod(k, po_retku)
            ax.add_patch(Rectangle((2.1 + c*dx - 0.48, -r*dy - 0.44), 0.96, 0.88,
                                   fc=(0.97, 0.97, 0.97), ec=(0.6, 0.6, 0.6), lw=0.6,
                                   ls=":", zorder=2))
            ax.texts[k].set_color(SI); ax.texts[k].set_zorder(4)
    # oznake redaka i opisi
    for r in range(n_red):
        ax.text(0.95, -r*dy, f"{r*po_retku:04X}", ha="right", va="center", fontsize=12,
                family="DejaVu Sans Mono", color=SI)
    ax.text(2.1 + 11*dx + 1.0, -2.2*dy, "zaglavlje\n54 B", ha="left", va="center",
            fontsize=12, color=SI)
    ax.text(2.1 + 11*dx + 1.0, -5.25*dy, "pikseli\n24 B", ha="left", va="center",
            fontsize=12, color=SI)
    ax.plot([2.1 + 11*dx + 0.75]*2, [-0.45, -3.55], color=SI, lw=1.2)
    ax.plot([2.1 + 11*dx + 0.75]*2, [-4.45, -6.4], color=SI, lw=1.2)
    ax.set_xlim(0.2, 2.1 + 11*dx + 3.4); ax.set_ylim(-(n_red - 0.5)*dy, 0.6)
    ax.set_aspect("equal"); ax.axis("off")
    spremi(fig, "p03_bmp_hex.png")


def bmp_slicica():
    """Uvecana slika 3 x 2 piksela koja odgovara hex zapisu na istom slajdu."""
    a = np.array([[[255, 0, 0], [255, 255, 255], [0, 0, 255]],
                  [[0, 255, 0], [0, 0, 0], [255, 255, 0]]], np.uint8)
    fig, ax = plt.subplots(figsize=(2.4, 1.75))
    ax.imshow(a, interpolation="nearest", extent=(0, 3, 2, 0))
    for x in range(4):
        ax.plot([x, x], [0, 2], color=(0.45, 0.45, 0.45), lw=1.1)
    for y in range(3):
        ax.plot([0, 3], [y, y], color=(0.45, 0.45, 0.45), lw=1.1)
    ax.add_patch(Rectangle((0, 0), 3, 2, fill=False, ec=(0.3, 0.3, 0.3), lw=1.6, zorder=5))
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(-0.05, 3.05); ax.set_ylim(2.05, -0.05)
    ax.axis("off")
    spremi(fig, "p03_bmp_slicica.png", dpi=200)


# ---------------------------------------------------------------- TIFF: tagovi i IFD
def tiff_struktura():
    """Zaglavlje -> IFD s tagovima -> podaci; desno anatomija jednog taga.
    Popis tagova je stvarni sadrzaj IFD-a datoteke generirane nize."""
    b = io.BytesIO()
    Image.fromarray(SLIKA).save(b, "TIFF", compression="tiff_lzw")
    d = b.getvalue()
    import struct
    bo = "<" if d[:2] == b"II" else ">"
    off = struct.unpack(bo + "I", d[4:8])[0]
    n = struct.unpack(bo + "H", d[off:off + 2])[0]
    IME = {256: "ImageWidth", 257: "ImageLength", 258: "BitsPerSample", 259: "Compression",
           262: "PhotometricInterpretation", 273: "StripOffsets", 277: "SamplesPerPixel",
           278: "RowsPerStrip", 279: "StripByteCounts", 284: "PlanarConfiguration"}
    tagovi = []
    for i in range(n):
        p = off + 2 + i * 12
        tag, tip, brv = struct.unpack(bo + "HHI", d[p:p + 8])
        tagovi.append((tag, IME.get(tag, "?")))

    fig, ax = plt.subplots(figsize=(12.6, 5.6))

    def blok(x, y, w, h, naslov, tekst, boja, fs=10.5, mono=False, lijevo=None):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                    fc=boja, ec=SI, lw=1.2))
        ax.text(x + w / 2, y + h - 0.16, naslov, ha="center", va="top", fontsize=12,
                weight="bold", color=PL)
        ax.text(x + lijevo if lijevo is not None else x + w / 2, y + h - 0.62, tekst,
                ha="left" if lijevo is not None else "center", va="top", fontsize=fs,
                color="black", linespacing=1.45,
                family="DejaVu Sans Mono" if mono else "DejaVu Sans")

    # lijevi stupac: redoslijed u datoteci
    blok(0.0, 4.25, 4.5, 1.15, "zaglavlje  (8 bajtova)",
         "II / MM  +  42  +  odmak do IFD-a", (0.86, 0.84, 0.92), fs=10)
    blok(0.0, 1.05, 4.5, 2.95, "IFD  (Image File Directory)",
         "broj tagova (2 B)\n" + "\n".join(f"{t:>3d}   {ime}" for t, ime in tagovi[:6])
         + f"\n…   ({len(tagovi)} tagova)\nodmak do sljedećeg IFD-a (4 B)",
         (0.93, 0.91, 0.97), fs=9.2, mono=True, lijevo=0.42)
    blok(0.0, 0.0, 4.5, 0.82, "podaci o pikselima",
         "trake (strips) ili pločice (tiles)", (0.90, 0.93, 0.90), fs=10)

    ax.annotate("", xy=(-0.30, 0.0), xytext=(-0.30, 5.40),
                arrowprops=dict(arrowstyle="->", color=SI, lw=1.3))
    ax.text(-0.62, 2.70, "redoslijed bajtova", rotation=90, ha="center", va="center",
            fontsize=10.5, color=SI)

    # IFD -> podaci: tag StripOffsets pokazuje gdje su podaci
    ax.add_patch(FancyArrowPatch((2.25, 1.05), (2.25, 0.82), arrowstyle="-|>",
                                 mutation_scale=14, color=NG, lw=1.4))
    ax.text(2.45, 0.93, "StripOffsets", ha="left", va="center", fontsize=9, color=NG)

    # desni dio: anatomija jednog taga
    ax.text(7.9, 5.35, "svaki tag zauzima 12 bajtova", ha="center", va="top",
            fontsize=12, weight="bold", color=PL)
    polja = [("oznaka", "2 B", "259"), ("tip", "2 B", "SHORT"),
             ("broj vrij.", "4 B", "1"), ("vrijednost\nili odmak", "4 B", "5")]
    x0, w, h = 5.3, 1.3, 1.0
    for i, (ime, bajt, vr) in enumerate(polja):
        x = x0 + i * (w + 0.12)
        ax.add_patch(FancyBboxPatch((x, 3.85), w, h, boxstyle="round,pad=0.02,rounding_size=0.05",
                                    fc=(0.93, 0.91, 0.97), ec=SI, lw=1.2))
        ax.text(x + w / 2, 4.52, ime, ha="center", va="center", fontsize=9.5,
                color="black", linespacing=1.3)
        ax.text(x + w / 2, 4.02, bajt, ha="center", va="center", fontsize=9, color=SI)
        ax.add_patch(FancyBboxPatch((x, 2.80), w, 0.70, boxstyle="round,pad=0.02,rounding_size=0.05",
                                    fc=(1.0, 0.95, 0.86), ec=NG, lw=1.2))
        ax.text(x + w / 2, 3.15, vr, ha="center", va="center", fontsize=10.5,
                family="DejaVu Sans Mono", color="black")
    ax.text(x0, 2.42, "primjer:   oznaka 259 = Compression,  vrijednost 5 = LZW",
            ha="left", va="center", fontsize=10.5, color=PL)
    ax.text(x0, 1.80,
            "Čitač koji ne poznaje neki tag jednostavno ga preskoči —\n"
            "zato se TIFF mogao proširivati desetljećima bez loma\n"
            "kompatibilnosti. Ista struktura nosi i EXIF metapodatke.",
            ha="left", va="top", fontsize=10.5, color="black", linespacing=1.6)

    ax.set_xlim(-0.95, 11.3); ax.set_ylim(-0.1, 5.6); ax.axis("off")
    spremi(fig, "p03_tiff_struktura.png")


# ---------------------------------------------------------------- TIFF LZW: kada pomaze
def tiff_lzw():
    """Velicina TIFF LZW u odnosu na TIFF bez sazimanja, za razlicite vrste slika.
    Sve se slike stvarno zapisu i velicine se izmjere."""
    h, w = 400, 600
    foto = cv2.resize(SLIKA, (w, h), interpolation=cv2.INTER_AREA)
    sivo = cv2.cvtColor(foto, cv2.COLOR_RGB2GRAY)

    grafika = np.full((h, w, 3), 255, np.uint8)
    cv2.rectangle(grafika, (60, 60), (300, 260), (58, 48, 104), -1)
    cv2.circle(grafika, (430, 200), 110, (196, 120, 20), -1)
    cv2.putText(grafika, "TIFF", (90, 350), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (0, 0, 0), 6)

    xx = np.linspace(0, 255, w, dtype=np.float32)
    grad = np.repeat(np.tile(xx, (h, 1))[:, :, None].astype(np.uint8), 3, axis=2)

    rng = np.random.default_rng(0)
    sum_ = rng.integers(0, 256, (h, w, 3), dtype=np.uint8)

    def vel(a, komp):
        b = io.BytesIO()
        Image.fromarray(a).save(b, "TIFF", compression=komp)
        return len(b.getvalue())

    primjeri = [("crtež / tekst", grafika), ("gradijent", grad),
                ("fotografija,\nsive razine", sivo), ("fotografija,\nRGB", foto),
                ("čisti šum", sum_)]
    odnosi, oznake = [], []
    for ime, a in primjeri:
        r = vel(a, "tiff_lzw") / vel(a, None)
        odnosi.append(r)
        oznake.append(ime)
        print(f"     {ime.replace(chr(10), ' '):<26} LZW / bez sažimanja = {r:.2f}")

    fig, ax = plt.subplots(figsize=(11.2, 4.3))
    boje = [(0.35, 0.58, 0.40) if r < 1 else (0.72, 0.30, 0.30) for r in odnosi]
    bars = ax.bar(range(len(odnosi)), odnosi, color=boje, width=0.58,
                  edgecolor="white", linewidth=0.8)
    ax.axhline(1.0, color=PL, lw=1.6, ls="--")
    ax.text(-0.42, 1.04, "veličina bez sažimanja", ha="left", va="bottom",
            fontsize=11, color=PL)
    for i, (b_, r) in enumerate(zip(bars, odnosi)):
        ax.text(i, r + 0.03, f"{r:.2f}×", ha="center", va="bottom", fontsize=12,
                weight="bold", color="black")
    ax.set_xticks(range(len(odnosi)))
    ax.set_xticklabels(oznake, fontsize=11.5, linespacing=1.4)
    ax.set_ylabel("veličina  LZW / bez sažimanja", fontsize=11.5)
    ax.set_ylim(0, max(odnosi) * 1.22)
    ax.set_yticks([0, 0.5, 1.0, 1.5])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(SI); ax.spines["bottom"].set_color(SI)
    ax.tick_params(colors=SI)
    for lbl in ax.get_xticklabels():
        lbl.set_color("black")
    ax.grid(axis="y", color=SI, alpha=0.18, lw=0.7)
    ax.set_axisbelow(True)
    spremi(fig, "p03_tiff_lzw.png")


if __name__ == "__main__":
    for fn in [struktura_datoteke, podjela_formata, velicine, rle_huffman, png_filtri,
               gif_paleta, jpeg_kvalitete, krom_poduzorkovanje, jpeg_blokovi,
               kvant_tablice, raw_razvijanje, thumbnail_trag, matrica_rgb, bmp_hex, bmp_slicica,
               tiff_struktura, tiff_lzw]:
        fn()
