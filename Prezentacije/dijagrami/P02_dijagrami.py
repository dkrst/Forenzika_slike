# Vlastite ilustracije za Predavanje02 (Uvod u digitalnu obradu i analizu slike).
# Uporaba: python3 dijagrami/P02_dijagrami.py  -> zapisuje u slike/ (datoteke p02_*.png)
#
# Testne slike su iz paketa scikit-image (skimage.data) i slobodne su za uporabu:
# astronaut (NASA, javno dobro), coffee (CC0), chelsea (CC0), moon, page.

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import cv2
from skimage import data, exposure

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.size"] = 12
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "slike"))

PL = (58/255, 48/255, 104/255)
SV = (108/255, 96/255, 176/255)
NG = (196/255, 120/255, 20/255)
SI = (110/255, 118/255, 128/255)
RNG = np.random.default_rng(7)


def spremi(fig, ime, dpi=130):
    # fotografske ilustracije kao JPEG (manja datoteka); ilustracije kod kojih su
    # fini detalji piksela sama poanta (demozaik, uint8/float, šum) ostaju PNG
    kw = {"pil_kwargs": {"quality": 92}} if ime.endswith(".jpg") else {}
    fig.savefig(ime, dpi=dpi, bbox_inches="tight", facecolor="white", **kw)
    plt.close(fig)
    print("  ", ime)


def gray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def prikazi(ax, img, naslov=None, cmap="gray", **kw):
    if img.ndim == 2:
        ax.imshow(img, cmap=cmap, vmin=kw.pop("vmin", 0), vmax=kw.pop("vmax", 255), **kw)
    else:
        ax.imshow(img, **kw)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if naslov:
        ax.set_title(naslov, fontsize=13)


def hist(ax, img, boja=PL, naslov=None, ymax=None):
    h = np.bincount(img.ravel(), minlength=256)
    ax.bar(np.arange(256), h, width=1.0, color=boja)
    ax.set_xlim(-2, 257); ax.set_yticks([])
    ax.set_xticks([0, 128, 255])
    if ymax:
        ax.set_ylim(0, ymax)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    if naslov:
        ax.set_title(naslov, fontsize=12)


# ---------------------------------------------------------------- spektar
def valna_u_rgb(wl):
    # aproksimacija boje za valnu duljinu (Bruton), samo za ilustraciju
    if 380 <= wl < 440: r, g, b = -(wl-440)/60, 0, 1
    elif wl < 490: r, g, b = 0, (wl-440)/50, 1
    elif wl < 510: r, g, b = 0, 1, -(wl-510)/20
    elif wl < 580: r, g, b = (wl-510)/70, 1, 0
    elif wl < 645: r, g, b = 1, -(wl-645)/65, 0
    elif wl <= 750: r, g, b = 1, 0, 0
    else: return (0, 0, 0)
    f = 0.3 + 0.7*(wl-380)/40 if wl < 420 else (0.3 + 0.7*(750-wl)/105 if wl > 645 else 1)
    return (r*f, g*f, b*f)


def spektar():
    fig, ax = plt.subplots(figsize=(12, 2.6))
    pojasevi = [("gama", 0, 1), ("X", 1, 2), ("UV", 2, 3), ("", 3, 4.2), ("IR", 4.2, 5.4),
                ("mikrovalovi", 5.4, 6.6), ("radio", 6.6, 8)]
    for ime, a, b in pojasevi:
        if ime:
            ax.add_patch(Rectangle((a, 0.55), b-a, 0.35, fc=(0.9, 0.89, 0.94), ec="white", lw=2))
            ax.text((a+b)/2, 0.725, ime, ha="center", va="center", fontsize=12, color=PL)
    wl = np.linspace(380, 750, 400)
    for i, w in enumerate(wl):
        x = 3 + 1.2*i/len(wl)
        ax.add_patch(Rectangle((x, 0.55), 1.2/len(wl)+0.002, 0.35, fc=valna_u_rgb(w), ec="none"))
    ax.annotate("", xy=(8.0, 0.4), xytext=(0, 0.4), arrowprops=dict(arrowstyle="->", color=SI))
    ax.text(4, 0.3, "valna duljina raste →", ha="center", fontsize=10, color=SI)
    # uvecani vidljivi dio
    y0 = -0.45
    for i, w in enumerate(wl):
        x = 1.0 + 6.0*i/len(wl)
        ax.add_patch(Rectangle((x, y0), 6.0/len(wl)+0.005, 0.45, fc=valna_u_rgb(w), ec="none"))
    for w in [400, 450, 500, 550, 600, 650, 700, 750]:
        x = 1.0 + 6.0*(w-380)/370
        ax.text(x, y0-0.12, f"{w}", ha="center", va="top", fontsize=10, color=SI)
    ax.text(4.0, y0-0.37, "vidljivi dio spektra [nm]", ha="center", fontsize=11, color=PL)
    ax.plot([3, 1.0], [0.55, 0.0], color=SI, lw=0.8, ls="--")
    ax.plot([4.2, 7.0], [0.55, 0.0], color=SI, lw=0.8, ls="--")
    ax.set_xlim(-0.1, 8.1); ax.set_ylim(-0.95, 0.95); ax.axis("off")
    spremi(fig, "p02_spektar.png")


# ---------------------------------------------------------------- metamerizam
def metamerizam():
    wl = np.arange(400, 701, 2.0)
    g = lambda m, s: np.exp(-0.5*((wl-m)/s)**2)
    C = np.vstack([g(564, 50), g(534, 42), g(420, 28)])     # pojednostavljeni L, M, S
    A = 0.55 + 0.25*np.sin((wl-400)/300*np.pi)               # glatki spektar
    # B = A + komponenta iz nul-prostora matrice C -> isti odziv L, M, S
    v = np.sin((wl-400)/300*6*np.pi) * 0.35
    P = C.T @ np.linalg.solve(C @ C.T, C)
    B = A + (v - P @ v)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 3.6), gridspec_kw={"width_ratios": [2.3, 1]})
    a1.plot(wl, A, color=PL, lw=2.5, label="spektar A")
    a1.plot(wl, B, color=NG, lw=2.5, label="spektar B")
    a1.set_xlabel("valna duljina [nm]"); a1.set_ylabel("energija")
    a1.set_yticks([]); a1.legend(frameon=False, loc="upper left")
    for s in ["top", "right"]:
        a1.spines[s].set_visible(False)
    ra, rb = C @ A, C @ B
    x = np.arange(3)
    a2.bar(x-0.18, ra, 0.34, color=PL, label="A")
    a2.bar(x+0.18, rb, 0.34, color=NG, label="B")
    a2.set_xticks(x); a2.set_xticklabels(["L", "M", "S"]); a2.set_yticks([])
    a2.set_title("odziv čunjića", fontsize=12)
    for s in ["top", "right", "left"]:
        a2.spines[s].set_visible(False)
    fig.tight_layout()
    spremi(fig, "p02_metamerizam.png")


def metamerizam_zuta():
    # monokromatska žuta (580 nm) i mješavina crvene i zelene linije sa zaslona;
    # intenziteti linija računaju se tako da odzivi L i M budu jednaki (S je u oba slučaja ~0)
    g = lambda wl, m, s: np.exp(-0.5*((wl-m)/s)**2)
    cun = lambda wl: np.array([g(wl, 564, 50), g(wl, 534, 42), g(wl, 420, 28)])   # L, M, S
    zuta = 580.0; crv, zel = 630.0, 532.0
    odz_z = cun(zuta)
    Mtx = np.column_stack([cun(crv)[:2], cun(zel)[:2]])
    a_c, a_z = np.linalg.solve(Mtx, odz_z[:2])
    odz_m = a_c*cun(crv) + a_z*cun(zel)
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6), gridspec_kw={"width_ratios": [1.3, 1.3, 1]})
    for a, linije, nasl in [(ax[0], [(zuta, 1.0)], "monokromatska žuta, 580 nm"),
                            (ax[1], [(crv, a_c), (zel, a_z)], "zaslon: crvena + zelena")]:
        for wl, amp in linije:
            a.plot([wl, wl], [0, amp], color=valna_u_rgb(wl), lw=6, solid_capstyle="butt")
        a.set_xlim(400, 700); a.set_ylim(0, max(1.0, a_c, a_z)*1.12)
        a.set_xlabel("valna duljina [nm]"); a.set_yticks([]); a.set_title(nasl, fontsize=12)
        for sp in ["top", "right", "left"]:
            a.spines[sp].set_visible(False)
    x = np.arange(3)
    ax[2].bar(x-0.18, odz_z, 0.34, color=(0.93, 0.78, 0.0), label="žuta 580 nm")
    ax[2].bar(x+0.18, odz_m, 0.34, color=SV, label="crvena + zelena")
    ax[2].set_xticks(x); ax[2].set_xticklabels(["L", "M", "S"]); ax[2].set_yticks([])
    ax[2].set_title("odziv čunjića", fontsize=12); ax[2].legend(frameon=False, fontsize=9)
    for sp in ["top", "right", "left"]:
        ax[2].spines[sp].set_visible(False)
    fig.tight_layout()
    spremi(fig, "p02_metamerizam_zuta.png")


# ---------------------------------------------------------------- mijesanje boja
def mijesanje():
    N = 500
    yy, xx = np.mgrid[0:N, 0:N] / N
    centri = [(0.5, 0.36), (0.36, 0.62), (0.64, 0.62)]
    r = 0.24
    maske = [((xx-cx)**2 + (yy-cy)**2) < r**2 for cx, cy in centri]
    adit = np.zeros((N, N, 3))
    for k, m in enumerate(maske):
        adit[..., k] += m
    sub = np.ones((N, N, 3))
    for k, m in enumerate(maske):          # C upija R, M upija G, Y upija B
        sub[..., k] -= m
    sub = np.clip(sub, 0, 1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4.4))
    prikazi(a1, np.clip(adit, 0, 1), "aditivno (RGB) — zasloni")
    prikazi(a2, sub, "suptraktivno (CMY) — tisak")
    a1.set_facecolor("black")
    spremi(fig, "p02_mijesanje.png")


# ---------------------------------------------------------------- percepcija boje (stari slajdovi 27 i 28)
from matplotlib.patches import Ellipse

# boje očitane iz izvornog slajda (ispunjene elipse)
KOJA_BOJA = [(221, 38, 38), (255, 0, 0), (255, 79, 92),
             (35, 79, 92), (0, 79, 92), (35, 92, 71)]


def koja_boja(s_vrijednostima, ime):
    fig, ax = plt.subplots(figsize=(10, 4.4))
    for k, c in enumerate(KOJA_BOJA):
        x, y = 1.0 + (k % 3)*2.1, 2.2 - (k // 3)*1.9
        ax.add_patch(Ellipse((x, y), 1.9, 1.5, fc=np.array(c)/255, ec=(0.25, 0.25, 0.25), lw=0.8))
        if s_vrijednostima:
            ax.text(x, y, f"R {c[0]:>3}\nG {c[1]:>3}\nB {c[2]:>3}", ha="center", va="center",
                    fontsize=15, color="white", family="DejaVu Sans Mono", linespacing=1.3)
    ax.set_xlim(-0.05, 6.35); ax.set_ylim(-0.6, 3.05); ax.set_aspect("equal"); ax.axis("off")
    spremi(fig, ime)


def hsv_nizovi():
    redovi = [("Ton (Hue) — dominantna valna duljina",
               [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 0)]),
              ("Zasićenje (Saturation) — udio čiste boje, odmak od sive",
               [(255, 0, 0), (255, 51, 51), (255, 102, 102), (255, 153, 153), (255, 204, 204), (204, 204, 204)]),
              ("Vrijednost (Value) — svjetlina, intenzitet",
               [(255, 0, 0), (204, 0, 0), (153, 0, 0), (102, 0, 0), (51, 0, 0), (0, 0, 0)])]
    fig, ax = plt.subplots(figsize=(12, 5.4))
    for r, (naslov, boje) in enumerate(redovi):
        y = 2.4 - r*1.25
        ax.text(0.0, y + 0.42, f"{r+1}. {naslov}", fontsize=14, color=PL, va="bottom")
        for k, c in enumerate(boje):
            ax.add_patch(Ellipse((0.8 + k*1.75, y), 1.6, 0.62, fc=np.array(c)/255,
                                 ec=(0.25, 0.25, 0.25), lw=0.8))
    ax.set_xlim(-0.1, 10.65); ax.set_ylim(-0.5, 3.1); ax.set_aspect("equal"); ax.axis("off")
    spremi(fig, "p02_hsv_nizovi.png")



def hsv_kanali():
    img = data.astronaut()
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)          # OpenCV: H u rasponu 0-179
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.5))
    prikazi(ax[0], img, "RGB")
    ax[1].imshow(hsv[..., 0], cmap="hsv", vmin=0, vmax=179)
    ax[1].set_xticks([]); ax[1].set_yticks([]); ax[1].set_title("H — ton", fontsize=13)
    for sp in ax[1].spines.values():
        sp.set_visible(False)
    prikazi(ax[2], hsv[..., 1], "S — zasićenje")
    prikazi(ax[3], hsv[..., 2], "V — vrijednost")
    fig.tight_layout()
    spremi(fig, "p02_hsv_kanali.jpg")


# ---------------------------------------------------------------- RGB kocka
def rgb_kocka():
    fig = plt.figure(figsize=(5.4, 5.2))
    ax = fig.add_subplot(111, projection="3d")
    n = 32
    t = np.linspace(0, 1, n)
    U, V = np.meshgrid(t, t)
    J = np.ones_like(U)
    for X, Y, Z in [(J, U, V), (U, J, V), (U, V, J)]:          # plohe R=1, G=1, B=1
        ax.plot_surface(X, Y, Z, facecolors=np.dstack([X, Y, Z]), shade=False,
                        rstride=1, cstride=1, lw=0, antialiased=False)
    vrhovi = {"crvena (1,0,0)": (1, 0, 0), "zelena (0,1,0)": (0, 1, 0), "plava (0,0,1)": (0, 0, 1),
              "žuta": (1, 1, 0), "cijan": (0, 1, 1), "magenta": (1, 0, 1)}
    vrhovi["bijela (1,1,1)"] = (1, 1, 1)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
    ax.set_axis_off()
    ax.view_init(elev=28, azim=40)
    ax.set_box_aspect((1, 1, 1))
    fig.canvas.draw()
    from mpl_toolkits.mplot3d import proj3d
    tocke = {k: proj3d.proj_transform(*p, ax.get_proj())[:2] for k, p in vrhovi.items()}
    cx = np.mean([v[0] for v in tocke.values()]); cy = np.mean([v[1] for v in tocke.values()])
    for ime, (x2, y2) in tocke.items():
        if ime.startswith("bijela"):          # središnji vrh; opisan u tekstu slajda
            continue
        dx, dy = x2 - cx, y2 - cy
        nrm = np.hypot(dx, dy) + 1e-9
        ax.text2D(x2 + 0.018*dx/nrm, y2 + 0.018*dy/nrm, ime, fontsize=11,
                  ha="left" if dx > 0.005 else ("right" if dx < -0.005 else "center"),
                  va="bottom" if dy > 0 else "top", transform=ax.transData)
    spremi(fig, "p02_rgb_kocka.png")


# ---------------------------------------------------------------- u sivo
def u_sivo():
    boje = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
    trake = np.zeros((120, 360, 3), np.uint8)
    for i, b in enumerate(boje):
        trake[:, i*60:(i+1)*60] = b
    prosjek = trake.mean(axis=2).astype(np.uint8)
    tezinski = (0.299*trake[..., 0] + 0.587*trake[..., 1] + 0.114*trake[..., 2]).astype(np.uint8)
    img = data.coffee()
    fig, ax = plt.subplots(2, 3, figsize=(12, 5.6), gridspec_kw={"height_ratios": [1, 1.7]})
    prikazi(ax[0, 0], trake, "izvornik")
    prikazi(ax[0, 1], prosjek, "(R+G+B)/3")
    prikazi(ax[0, 2], tezinski, "0,299R + 0,587G + 0,114B")
    prikazi(ax[1, 0], img)
    prikazi(ax[1, 1], img.mean(axis=2).astype(np.uint8))
    prikazi(ax[1, 2], (0.299*img[..., 0] + 0.587*img[..., 1] + 0.114*img[..., 2]).astype(np.uint8))
    fig.tight_layout()
    spremi(fig, "p02_u_sivo.jpg")


# ---------------------------------------------------------------- Bayer i demozaikiranje
def demozaik():
    img = data.chelsea()                                    # demozaikira se cijela slika,
    maska = np.zeros_like(img)                              # prikazuje se detalj krzna
    maska[0::2, 0::2, 0] = 1                                # R
    maska[0::2, 1::2, 1] = 1; maska[1::2, 0::2, 1] = 1      # G
    maska[1::2, 1::2, 2] = 1                                # B
    mozaik_boja = img * maska
    # sirovi zapis senzora (jedan broj po pikselu) i bilinearno demozaikiranje (OpenCV)
    raw = (img * maska).sum(axis=2).astype(np.uint8)
    dem = cv2.cvtColor(raw, cv2.COLOR_BayerBG2RGB)        # uzorak RGGB u OpenCV nazivlju
    y, x, k = 8, 184, 48
    c = lambda a: a[y:y+k, x:x+k]
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.6))
    prikazi(ax[0], c(img), "scena", interpolation="nearest")
    prikazi(ax[1], c(mozaik_boja), "kroz CFA filtar", interpolation="nearest")
    prikazi(ax[2], c(raw), "sirovi zapis senzora", interpolation="nearest")
    prikazi(ax[3], c(dem), "demozaikirano", interpolation="nearest")
    fig.tight_layout()
    spremi(fig, "p02_demozaik.png")


# ---------------------------------------------------------------- uzorkovanje i kvantizacija
def uzorkovanje():
    x = np.linspace(0, 1, 600)
    f = 0.5 + 0.3*np.sin(2*np.pi*1.3*x) + 0.12*np.sin(2*np.pi*4.1*x)
    xs = np.linspace(0, 1, 16)
    fs = 0.5 + 0.3*np.sin(2*np.pi*1.3*xs) + 0.12*np.sin(2*np.pi*4.1*xs)
    razine = 8
    fq = np.round(fs*(razine-1))/(razine-1)
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.2), sharey=True)
    for a in ax:
        for s in ["top", "right"]:
            a.spines[s].set_visible(False)
        a.set_xticks([]); a.set_ylim(0, 1)
    ax[0].plot(x, f, color=PL, lw=2.5); ax[0].set_title("kontinuirani signal f(x)")
    ax[0].set_yticks([])
    ax[1].plot(x, f, color=SI, lw=1, alpha=0.6)
    mk1, st1, _ = ax[1].stem(xs, fs, linefmt="-", markerfmt="o", basefmt=" ")
    plt.setp(mk1, color=PL); plt.setp(st1, color=PL)
    ax[1].set_title("uzorkovanje (prostor)")
    for q in np.linspace(0, 1, razine):
        ax[2].axhline(q, color=SI, lw=0.6, ls=":")
    ax[2].plot(x, f, color=SI, lw=1, alpha=0.6)
    mk, st, _ = ax[2].stem(xs, fq, linefmt="-", markerfmt="s", basefmt=" ")
    plt.setp(mk, color=NG); plt.setp(st, color=NG)
    ax[2].set_title(f"kvantizacija ({razine} razina)")
    fig.tight_layout()
    spremi(fig, "p02_uzorkovanje.png")


# ---------------------------------------------------------------- matrica piksela
def matrica():
    g = gray(data.astronaut())
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.2), gridspec_kw={"width_ratios": [1, 1.25]})
    prikazi(a1, g)
    y0, x0, n = 170, 230, 10
    a1.add_patch(Rectangle((x0, y0), n, n, fill=False, ec=NG, lw=2.5))
    blok = g[y0:y0+n, x0:x0+n]
    prikazi(a2, blok, interpolation="nearest")
    for i in range(n):
        for j in range(n):
            v = blok[i, j]
            a2.text(j, i, str(v), ha="center", va="center", fontsize=9,
                    color="white" if v < 110 else "black")
    a2.set_title("f(m, n) — vrijednosti piksela", fontsize=13)
    fig.tight_layout()
    spremi(fig, "p02_matrica.jpg")


# ---------------------------------------------------------------- RGB kanali
def kanali():
    img = data.coffee()
    fig, ax = plt.subplots(1, 4, figsize=(13, 2.6))
    prikazi(ax[0], img, "RGB")
    for k, ime in enumerate(["R", "G", "B"]):
        prikazi(ax[k+1], img[..., k], ime)
    fig.tight_layout()
    spremi(fig, "p02_kanali.jpg")


# ---------------------------------------------------------------- rezolucija i dubina
def rezolucija_dubina():
    g = gray(data.astronaut())[0:320, 60:380]
    fig, ax = plt.subplots(2, 4, figsize=(12, 6.4))
    for k, n in enumerate([320, 80, 40, 20]):
        m = cv2.resize(cv2.resize(g, (n, n), interpolation=cv2.INTER_AREA), (320, 320),
                       interpolation=cv2.INTER_NEAREST)
        prikazi(ax[0, k], m, f"{n} × {n}")
    for k, b in enumerate([8, 4, 2, 1]):
        L = 2**b
        q = (np.floor(g/256*L) * (255/(L-1))).astype(np.uint8)
        prikazi(ax[1, k], q, f"{b} bit ({L} razin{'a' if L > 4 else 'e'})")
    fig.tight_layout()
    spremi(fig, "p02_rezolucija_dubina.jpg")


# ---------------------------------------------------------------- float vs int
def float_vs_int():
    g = gray(data.astronaut())[40:300, 120:380]
    u = (g // 24).astype(np.uint8)                                  # uint8: potamni pa posvijetli
    u = np.clip(u.astype(np.uint16) * 24, 0, 255).astype(np.uint8)
    f = g.astype(np.float64) / 255.0
    f = f / 24.0
    f = np.clip(f * 24.0, 0, 1)
    fu = np.round(f * 255).astype(np.uint8)
    fig, ax = plt.subplots(2, 3, figsize=(12, 6.2), gridspec_kw={"height_ratios": [2, 1]})
    prikazi(ax[0, 0], g, "izvornik")
    prikazi(ax[0, 1], u, "uint8: /24 pa ×24")
    prikazi(ax[0, 2], fu, "float: /24 pa ×24")
    hist(ax[1, 0], g); hist(ax[1, 1], u, boja=NG); hist(ax[1, 2], fu)
    fig.tight_layout()
    spremi(fig, "p02_float_vs_int.png")


# ---------------------------------------------------------------- tockaste operacije
def tockaste():
    g = gray(data.coffee())
    lut = RNG.integers(0, 256, 256).astype(np.uint8)
    fig, ax = plt.subplots(1, 4, figsize=(13, 2.7))
    prikazi(ax[0], g, "izvornik")
    prikazi(ax[1], 255 - g, "negativ: 255 − f")
    prikazi(ax[2], ((g > 120) * 255).astype(np.uint8), "prag: f > 120")
    prikazi(ax[3], lut[g], "slučajna LUT")
    fig.tight_layout()
    spremi(fig, "p02_tockaste.jpg")


# ---------------------------------------------------------------- razlika slika
def razlika():
    img = data.coffee().copy()
    izm = img.copy()
    # dio drvene podloge kopiran preko drugog dijela podloge (copy-move) -- okom se teško uočava
    izm[262:302, 515:575] = img[218:258, 515:575]
    d = np.abs(img.astype(int) - izm.astype(int)).sum(axis=2)
    d = np.clip(d * 4.0, 0, 255).astype(np.uint8)            # pojačano radi vidljivosti
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.2))
    prikazi(ax[0], img, "slika A")
    prikazi(ax[1], izm, "slika B")
    prikazi(ax[2], 255 - d, "|A − B| (pojačano)")
    fig.tight_layout()
    spremi(fig, "p02_razlika.jpg")


# ---------------------------------------------------------------- histogram
def histogram():
    g = gray(data.coffee())
    h = np.bincount(g.ravel(), minlength=256)
    H = np.cumsum(h)
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.3), gridspec_kw={"width_ratios": [1.2, 1.4, 1.4]})
    prikazi(ax[0], g)
    ax[1].bar(np.arange(256), h, width=1.0, color=PL); ax[1].set_title("histogram h(k)")
    ax[2].plot(np.arange(256), H, color=NG, lw=2.5); ax[2].set_title("kumulativni histogram H(k)")
    for a in ax[1:]:
        a.set_xlim(0, 255); a.set_yticks([]); a.set_xticks([0, 128, 255])
        for s in ["top", "right", "left"]:
            a.spines[s].set_visible(False)
    fig.tight_layout()
    spremi(fig, "p02_histogram.jpg")


def histogram_rgb():
    img = data.coffee()
    fig, ax = plt.subplots(1, 2, figsize=(12, 3.3), gridspec_kw={"width_ratios": [1, 1.6]})
    prikazi(ax[0], img)
    for k, c in enumerate([(0.85, 0.15, 0.15), (0.15, 0.6, 0.2), (0.2, 0.3, 0.85)]):
        h = np.bincount(img[..., k].ravel(), minlength=256)
        ax[1].plot(np.arange(256), h, color=c, lw=1.8, label="RGB"[k])
        ax[1].fill_between(np.arange(256), h, color=c, alpha=0.12)
    ax[1].set_xlim(0, 255); ax[1].set_yticks([]); ax[1].set_xticks([0, 128, 255])
    ax[1].legend(frameon=False)
    for s in ["top", "right", "left"]:
        ax[1].spines[s].set_visible(False)
    fig.tight_layout()
    spremi(fig, "p02_histogram_rgb.jpg")


def permutacija():
    g = gray(data.coffee())[::2, ::2]
    p = RNG.permutation(g.ravel()).reshape(g.shape)
    fig, ax = plt.subplots(2, 2, figsize=(8.6, 6.4), gridspec_kw={"height_ratios": [2, 1]})
    prikazi(ax[0, 0], g, "izvornik")
    prikazi(ax[0, 1], p, "isti pikseli, izmiješani")
    hist(ax[1, 0], g); hist(ax[1, 1], p)
    fig.tight_layout()
    spremi(fig, "p02_permutacija.png")


def tipovi_histograma():
    g = gray(data.astronaut())[20:330, 80:390].astype(float)
    varijante = [("tamna", np.clip(g*0.45, 0, 255)),
                 ("svijetla", np.clip(g*0.45 + 140, 0, 255)),
                 ("nizak kontrast", np.clip(g*0.3 + 90, 0, 255)),
                 ("odsijecanje", np.clip(g*1.9 - 40, 0, 255))]
    fig, ax = plt.subplots(2, 4, figsize=(13, 5.2), gridspec_kw={"height_ratios": [2, 1]})
    for k, (ime, v) in enumerate(varijante):
        v = v.astype(np.uint8)
        h = np.bincount(v.ravel(), minlength=256)
        prikazi(ax[0, k], v, ime); hist(ax[1, k], v, ymax=h[1:255].max()*1.25)
    fig.tight_layout()
    spremi(fig, "p02_tipovi_histograma.jpg")


# ---------------------------------------------------------------- poboljsanje
def rastezanje_ujednacavanje():
    m = data.moon()
    lo, hi = np.percentile(m, [0.5, 99.5])                  # odbacuje se 1 % krajnjih vrijednosti
    st = np.clip((m.astype(float) - lo) / (hi - lo) * 255, 0, 255).round().astype(np.uint8)
    eq = cv2.equalizeHist(m)
    fig, ax = plt.subplots(2, 3, figsize=(12, 6.0), gridspec_kw={"height_ratios": [2, 1]})
    for k, (ime, v) in enumerate([("izvornik", m), ("rastezanje", st), ("ujednačavanje", eq)]):
        prikazi(ax[0, k], v, ime); hist(ax[1, k], v, boja=NG if k else PL)
    fig.tight_layout()
    spremi(fig, "p02_rastezanje_ujednacavanje.jpg")


def log_exp():
    x = np.linspace(0, 1, 256)
    lg = np.log1p(9*x)/np.log(10)
    ex = x**2.5
    g = gray(data.astronaut())[20:330, 80:390] / 255.0
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.3), gridspec_kw={"width_ratios": [1.15, 1, 1, 1]})
    ax[0].plot(x, x, color=SI, lw=1.5, ls="--", label="identitet")
    ax[0].plot(x, lg, color=PL, lw=2.5, label="logaritamska")
    ax[0].plot(x, ex, color=NG, lw=2.5, label="eksponencijalna")
    ax[0].set_xlabel("ulaz"); ax[0].set_ylabel("izlaz"); ax[0].legend(frameon=False, fontsize=10)
    ax[0].set_aspect("equal"); ax[0].set_xticks([0, 1]); ax[0].set_yticks([0, 1])
    for s in ["top", "right"]:
        ax[0].spines[s].set_visible(False)
    prikazi(ax[1], (g*255).astype(np.uint8), "izvornik")
    prikazi(ax[2], (np.log1p(9*g)/np.log(10)*255).astype(np.uint8), "log: tamni detalji")
    prikazi(ax[3], (g**2.5*255).astype(np.uint8), "exp: svijetli detalji")
    fig.tight_layout()
    spremi(fig, "p02_log_exp.jpg")


def cesalj():
    g = gray(data.coffee())
    niski = np.clip(g.astype(float)*0.5 + 60, 0, 255).astype(np.uint8)   # slika niskog kontrasta
    lo, hi = niski.min(), niski.max()
    st = ((niski.astype(float) - lo) / (hi - lo) * 255).round().astype(np.uint8)
    fig, ax = plt.subplots(1, 2, figsize=(12, 2.8))
    hist(ax[0], niski, naslov="prije rastezanja")
    hist(ax[1], st, boja=NG, naslov="nakon rastezanja — „češalj\"")
    fig.tight_layout()
    spremi(fig, "p02_cesalj.png")


# ---------------------------------------------------------------- konvolucija
def konvolucija_shema():
    rng = np.random.default_rng(3)
    A = rng.integers(0, 10, (6, 7))
    K = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    fig, ax = plt.subplots(1, 3, figsize=(13, 4.0), gridspec_kw={"width_ratios": [7, 3.2, 5]})
    def mreza(a, M, naslov, oznaci=None, fc=None):
        r, c = M.shape
        for i in range(r):
            for j in range(c):
                u = oznaci is not None and oznaci[0] <= i < oznaci[0]+3 and oznaci[1] <= j < oznaci[1]+3
                a.add_patch(Rectangle((j, r-1-i), 1, 1, fc=(fc or ((0.93, 0.91, 0.98) if u else "white")),
                                      ec=SI, lw=1))
                a.text(j+0.5, r-0.5-i, str(M[i, j]), ha="center", va="center", fontsize=13)
        if oznaci is not None:
            a.add_patch(Rectangle((oznaci[1], r-3-oznaci[0]), 3, 3, fill=False, ec=NG, lw=3))
        a.set_xlim(-0.2, c+0.2); a.set_ylim(-0.2, r+0.2); a.set_aspect("equal"); a.axis("off")
        a.set_title(naslov, fontsize=13)
    mreza(ax[0], A, "ulazna slika f", oznaci=(1, 2))
    mreza(ax[1], K, "jezgra h (× 1/16)", fc=(1.0, 0.95, 0.88))
    out = np.full((6, 7), "", dtype=object)
    s = int((A[1:4, 2:5]*K).sum())
    out[2, 3] = f"{s/16:.1f}"
    r, c = out.shape
    for i in range(r):
        for j in range(c):
            ax[2].add_patch(Rectangle((j, r-1-i), 1, 1, fc=(1.0, 0.95, 0.88) if out[i, j] else "white", ec=SI, lw=1))
            ax[2].text(j+0.5, r-0.5-i, out[i, j], ha="center", va="center", fontsize=11, weight="bold")
    ax[2].set_xlim(-0.2, c+0.2); ax[2].set_ylim(-0.2, r+0.2); ax[2].set_aspect("equal"); ax[2].axis("off")
    ax[2].set_title("izlaz g", fontsize=13)
    fig.tight_layout()
    spremi(fig, "p02_konvolucija_shema.png")


def filtri():
    g = gray(data.astronaut())[30:330, 110:410]
    s = np.clip(g + RNG.normal(0, 18, g.shape), 0, 255).astype(np.uint8)
    prosjek = cv2.blur(s, (5, 5))
    gauss = cv2.GaussianBlur(s, (7, 7), 1.6)
    lap = cv2.Laplacian(g.astype(np.float32), cv2.CV_32F, ksize=1)
    ostro = np.clip(g.astype(np.float32) - 0.9*lap, 0, 255).astype(np.uint8)
    gx = cv2.Sobel(g.astype(np.float32), cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(g.astype(np.float32), cv2.CV_32F, 0, 1)
    mag = np.clip(np.hypot(gx, gy) / 3, 0, 255).astype(np.uint8)
    fig, ax = plt.subplots(2, 3, figsize=(12, 8.2))
    prikazi(ax[0, 0], s, "slika sa šumom")
    prikazi(ax[0, 1], prosjek, "prosjek 5 × 5")
    prikazi(ax[0, 2], gauss, "Gaussov filtar")
    prikazi(ax[1, 0], g, "izvornik")
    prikazi(ax[1, 1], ostro, "izoštravanje (Laplace)")
    prikazi(ax[1, 2], 255 - mag, "rubovi (Sobel)")
    fig.tight_layout()
    spremi(fig, "p02_filtri.jpg")


def korelacija():
    img = data.coffee()
    g = gray(img)
    y, x, h, w = 228, 330, 60, 62
    T = g[y:y+h, x:x+w]
    R = cv2.matchTemplate(g, T, cv2.TM_CCOEFF_NORMED)
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.4), gridspec_kw={"width_ratios": [1.5, 0.55, 1.5]})
    prikazi(ax[0], img, "slika")
    ax[0].add_patch(Rectangle((x, y), w, h, fill=False, ec=NG, lw=2.5))
    prikazi(ax[1], T, "uzorak")
    ax[2].imshow(R, cmap="magma"); ax[2].set_xticks([]); ax[2].set_yticks([])
    ax[2].set_title("normalizirana korelacija", fontsize=13)
    yy, xx = np.unravel_index(np.argmax(R), R.shape)
    ax[2].add_patch(Circle((xx, yy), 14, fill=False, ec="white", lw=2))
    fig.tight_layout()
    spremi(fig, "p02_korelacija.jpg")


def rezidual():
    img = gray(data.astronaut())[30:330, 110:410].astype(np.float32)
    s = img + RNG.normal(0, 4, img.shape)                        # simulirani sum senzora
    glatko = cv2.GaussianBlur(s, (0, 0), 1.2)
    r = s - glatko
    fig, ax = plt.subplots(1, 3, figsize=(12, 4.0))
    prikazi(ax[0], np.clip(s, 0, 255).astype(np.uint8), "slika f")
    prikazi(ax[1], np.clip(glatko, 0, 255).astype(np.uint8), "zaglađeno h ∗ f")
    ax[2].imshow(r, cmap="gray", vmin=-12, vmax=12); ax[2].set_xticks([]); ax[2].set_yticks([])
    ax[2].set_title("rezidual f − h ∗ f", fontsize=13)
    fig.tight_layout()
    spremi(fig, "p02_rezidual.png")



def nyquist_sinus():
    # primjer sa starog slajda "Aliasing": crvena sinusoida (0,9 ciklusa po uzorku) uzorkovana
    # u cijelim brojevima daje iste uzorke kao plava (0,1 ciklusa po uzorku)
    x = np.linspace(-0.5, 10.5, 2000)
    n = np.arange(0, 11)
    visoka = lambda t: np.cos(2*np.pi*0.9*(t - 3))
    niska = lambda t: np.cos(2*np.pi*0.1*(t - 3))
    fig, ax = plt.subplots(figsize=(11, 3.2))
    ax.plot(x, visoka(x), color=(0.85, 0.2, 0.2), lw=1.6, label="signal: 0,9 ciklusa po uzorku")
    ax.plot(x, niska(x), color=PL, lw=2.2, label="alias: 0,1 ciklusa po uzorku")
    ax.vlines(n, 0, niska(n), color=SI, lw=1)
    ax.plot(n, niska(n), "o", color="black", ms=7, zorder=5, label="uzorci")
    ax.axhline(0, color=SI, lw=0.8)
    ax.set_xticks(n); ax.set_yticks([]); ax.set_xlim(-0.5, 10.5)
    ax.set_xlabel("indeks uzorka")
    for sp in ["top", "right", "left"]:
        ax.spines[sp].set_visible(False)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.22), ncol=3, fontsize=11)
    spremi(fig, "p02_nyquist_sinus.png")



def interpolacija():
    # isti izrez (oko), uvećan 8 puta različitim metodama; sva četiri kompozita iste su
    # veličine i rasporeda, pa se na uzastopnim slajdovima uvećanje nalazi na istom mjestu
    from matplotlib.patches import ConnectionPatch
    img = data.astronaut()
    x0, y0, n, k = 226, 84, 32, 8
    metode = [("najblizi", cv2.INTER_NEAREST), ("bilinearna", cv2.INTER_LINEAR),
              ("bikubicna", cv2.INTER_CUBIC), ("lanczos", cv2.INTER_LANCZOS4)]
    for ime, m in metode:
        # interpolira se šire područje, pa se izrezuje -- izbjegavaju se rubni efekti
        pad = 8
        izrez = img[y0-pad:y0+n+pad, x0-pad:x0+n+pad]
        vel = cv2.resize(izrez, None, fx=k, fy=k, interpolation=m)
        vel = vel[pad*k:(pad+n)*k, pad*k:(pad+n)*k]
        fig = plt.figure(figsize=(8, 5.6))
        az = fig.add_axes([0.36, 0.0, 0.64, 1.0])
        az.imshow(vel, interpolation="nearest"); az.set_xticks([]); az.set_yticks([])
        ao = fig.add_axes([0.0, 0.0, 0.3, 0.43])
        ao.imshow(img, interpolation="antialiased"); ao.set_xticks([]); ao.set_yticks([])
        ao.add_patch(Rectangle((x0, y0), n, n, fill=False, ec=(0.1, 0.2, 0.9), lw=1.6))
        for (xa, ya), (xb, yb) in [((x0 + n, y0), (0, 0)), ((x0 + n, y0 + n), (0, n*k - 1))]:
            fig.add_artist(ConnectionPatch(xyA=(xa, ya), coordsA=ao.transData,
                                           xyB=(xb, yb), coordsB=az.transData,
                                           color=(0.1, 0.2, 0.9), lw=1.0))
        spremi(fig, f"p02_interp_{ime}.png")


if __name__ == "__main__":
    for fn in [spektar, metamerizam, metamerizam_zuta, mijesanje, rgb_kocka, u_sivo,
               lambda: koja_boja(False, "p02_koja_boja.png"),
               lambda: koja_boja(True, "p02_koja_boja_rgb.png"), hsv_nizovi, hsv_kanali, demozaik, uzorkovanje, matrica,
               kanali, rezolucija_dubina, float_vs_int, tockaste, razlika, histogram, histogram_rgb,
               permutacija, tipovi_histograma, rastezanje_ujednacavanje, log_exp, cesalj,
               konvolucija_shema, filtri, korelacija, rezidual, nyquist_sinus, interpolacija]:
        fn()
