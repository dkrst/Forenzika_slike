---
title: "Predavanje 2 --- Uvod u digitalnu obradu i analizu slike"
subtitle: "Forenzička analiza digitalne slike"
author: Damir Krstinić
institute: "FESB --- Sveučilište u Splitu"
lang: hr
---

# Kako vidimo

## Svjetlost

- Svjetlost je **elektromagnetsko zračenje** koje podražuje fotoreceptore oka
- Ljudsko oko osjetljivo je na vrlo mali dio spektra: približno **380--750 nm**

![](slike/p02_spektar.png){width=100%}

## Boja predmeta

- Izvor svjetla ima svoju **spektralnu raspodjelu energije** $L(\lambda)$
- Površina predmeta dio valnih duljina upija, a dio odbija: **reflektivnost** $\rho(\lambda)$
- U oko (ili kameru) stiže:

$$I(\lambda) = \rho(\lambda) \, L(\lambda)$$

- Boja koju vidimo ovisi i o predmetu **i o izvoru svjetla**
    - isti predmet pod žaruljom i pod dnevnim svjetlom daje drukčiji $I(\lambda)$
    - mozak to kompenzira; kamera mora to učiniti računski --- **balans bijele**

## Ljudski vizualni sustav

:::::: columns
::: {.column width="44%"}
![](slike/p02_oko.png){width=100%}
:::
::: {.column width="54%"}
- **Optički sustav** (rožnica, leća) fokusira sliku na mrežnicu
- **Mrežnica** pretvara svjetlost u električne signale
- **Mozak** te signale tumači

\vspace{1ex}
\includegraphics[width=\linewidth]{slike/p02_hvs_model.jpg}
:::
::::::

## Štapići i čunjići

:::::: columns
::: {.column width="49%"}
**Čunjići** --- fotopski (svijetli) vid

- 6--7 milijuna, uglavnom u žutoj pjegi
- osjetljivi na boju --- tri vrste
- svaki povezan na vlastiti živac → oštra, detaljna slika
:::
::: {.column width="49%"}
**Štapići** --- skotopski (tamni) vid

- 75--150 milijuna, raspršeni po mrežnici
- znatno osjetljiviji, ali **ne razlikuju boje**
- više štapića dijeli jedan živac → manje detalja
:::
::::::

\vspace{1ex}

\begin{deklaracija}
Pri slabom svjetlu vidimo štapićima --- zato u mraku ne raspoznajemo boje.
\end{deklaracija}

## Odziv fotoreceptora

:::::: columns
::: {.column width="55%"}
![](slike/p02_odziv_fotoreceptora.jpg){width=100%}
:::
::: {.column width="43%"}
- Tri vrste čunjića s maksimumom odziva oko **420, 534 i 564 nm**
- Odzivi se jako preklapaju
- Štapići (isprekidano): maksimum oko **498 nm**
- Model odziva triju vrsta čunjića naziva se **LMS** (detaljno u P3)
:::
::::::

## Metamerizam

![](slike/p02_metamerizam.png){width=92%}

\begin{deklaracija}
Oko ne može rekonstruirati spektar: svjetlost svodi na \textbf{tri broja}. Različiti spektri mogu dati istu boju --- i zato su za zapis boje dovoljne tri vrijednosti po pikselu.
\end{deklaracija}

# Osnove boje

## Miješanje boja

- **Trikromatska teorija:** gotovo svaka boja može se dobiti miješanjem tri primarne boje

![](slike/p02_mijesanje.png){height=44%}

- **Aditivno** --- svjetla se zbrajaju (zasloni, projektori): RGB
- **Suptraktivno** --- pigmenti upijaju svjetlost (tisak): CMY + crna (K)

## RGB prostor boja

:::::: columns
::: {.column width="46%"}
![](slike/p02_rgb_kocka.png){width=100%}
:::
::: {.column width="52%"}
- Svaka boja je točka u kocki $(R, G, B)$
- Crna je u ishodištu $(0,0,0)$, bijela u suprotnom vrhu $(1,1,1)$ --- na slici središnji vrh
- Dijagonala $R = G = B$ su **sive razine**
- Uz 8 bita po kanalu: $256^3 \approx 16{,}7$ milijuna boja
:::
::::::

## Iz boje u sive razine

![](slike/p02_u_sivo.jpg){width=80%}

- Jednostavni prosjek daje istu sivu za crvenu, zelenu i plavu
- Težine prate osjetljivost oka --- najveću na zeleno (ITU-R BT.601)

## Nijansa, zasićenje, intenzitet

- RGB je praktičan za uređaje, ali ne opisuje boju onako kako je doživljavamo
- Čovjek boju opisuje drukčije:
    - **nijansa** (*hue*) --- „koja je to boja": crvena, žuta, plava…
    - **zasićenje** (*saturation*) --- koliko je boja čista, a koliko „razrijeđena" bijelom
    - **intenzitet** (*intensity*) --- koliko je svijetla
- Prostori boja HSI, HSV, Lab --- detaljno u P3

# Od svjetla do piksela

## Senzor i CFA filtar

:::::: columns
::: {.column width="42%"}
![](slike/p02_bayer.jpg){width=100%}
:::
::: {.column width="56%"}
- Fotosenzor mjeri samo **količinu svjetla**, ne i boju
- Ispred senzora je mozaik filtara boja --- **CFA** (*Color Filter Array*)
    - svaki piksel „vidi" samo jednu komponentu
- **Bayerov uzorak** (Kodak, patent 1976.):
    - 50 % zelenih, 25 % crvenih, 25 % plavih
    - zelenih je dvostruko jer oko najviše detalja vidi upravo preko zelene komponente
:::
::::::

## Demozaikiranje

![](slike/p02_demozaik.png){width=100%}

- U svakom pikselu **dvije od tri** vrijednosti boje interpoliraju se iz susjeda
- Na finim detaljima nastaju artefakti --- lažne boje
- Interpolacija ostavlja **pravilnu korelaciju među susjednim pikselima**, specifičnu za algoritam proizvođača --- važan forenzički trag

## Obrada u kameri

![](slike/cjevovod_kamere.jpg){width=62%}

- Tipični koraci: demozaikiranje → balans bijele → korekcija boja → **gama korekcija** → uklanjanje šuma, izoštravanje → kompresija
- Svaki proizvođač ove korake provodi na svoj način --- rezultat nosi **potpis uređaja**

## Gama korekcija

:::::: columns
::: {.column width="32%"}
![](slike/p02_gama_krivulja.jpg){width=100%}
:::
::: {.column width="66%"}
- Kodiranje u kameri: $V_c = V_{in}^{1/\gamma}$, prikaz: $V_{out} = V_c^{\gamma}$, tipično $\gamma \approx 2{,}2$
- Izvorno kompenzira nelinearnost CRT zaslona
- Danas važnije: oko je osjetljivije na razlike u **tamnim** tonovima
    - gama kodiranje tamnim tonovima daje više od 256 raspoloživih razina
:::
::::::

\begin{center}
\includegraphics[height=0.24\textheight]{slike/p02_gama_izvornik.jpg}\hspace{0.6em}\includegraphics[height=0.24\textheight]{slike/p02_gama_primjeri.jpg}
\end{center}

## RAW i obrađena slika

:::::: columns
::: {.column width="49%"}
**RAW**

- Izravno očitanje senzora nakon A/D pretvorbe
- Jedna vrijednost po pikselu (mozaik)
- 12--14 bita, linearni odziv, bez obrade
- Format proizvođača (CR3, NEF, ARW…) ili otvoreni DNG
:::
::: {.column width="49%"}
**Obrađena slika**

- Tri kanala po pikselu (RGB)
- 8 bita po kanalu
- Demozaikirana, balansirana, gama kodirana
- Najčešće sažeta (JPEG, HEIF)
:::
::::::

\vspace{1ex}

\begin{deklaracija}
RAW je najbliži onome što je senzor zabilježio, ali ni RAW datoteka sama po sebi ne jamči autentičnost.
\end{deklaracija}

# Zapis digitalne slike

## Uzorkovanje i kvantizacija

![](slike/p02_uzorkovanje.png){width=100%}

- **Uzorkovanje** --- kontinuirana scena mjeri se u konačnom broju točaka (piksela)
- **Kvantizacija** --- izmjerena vrijednost zaokružuje se na jednu od konačnog broja razina

## Slika kao matrica

![](slike/p02_matrica.jpg){width=82%}

- Slika sivih razina je matrica $f(m, n)$: $m$ je redak, $n$ stupac, ishodište gore lijevo

## Slika u boji

![](slike/p02_kanali.jpg){width=100%}

```python
img = cv2.imread("slika.jpg")     # POZOR: OpenCV čita kanale redom B, G, R
print(img.shape, img.dtype)       # (400, 600, 3) uint8
B, G, R = cv2.split(img)
```

- **Binarna slika** --- samo vrijednosti 0 i 1 (maske, segmentacija)

## Prostorna rezolucija i dubina boje

![](slike/p02_rezolucija_dubina.jpg){height=86%}

## Cjelobrojni zapis --- uint8

- Najčešći zapis: 8 bita po kanalu, vrijednosti **0--255**
- Što kada rezultat operacije izađe iz tog raspona?

```python
a = np.full((2, 2), 200, np.uint8)
b = np.full((2, 2), 100, np.uint8)
a + b              # 44   -> preljev (modulo 256)
cv2.add(a, b)      # 255  -> zasićenje (odsijecanje)
b - a              # 156
cv2.subtract(b, a) # 0
```

\begin{deklaracija}
Ista operacija daje različit rezultat ovisno o biblioteci --- bez ikakve poruke o pogrešci.
\end{deklaracija}

## Zašto pomični zarez?

![](slike/p02_float_vs_int.png){height=58%}

- Međurezultati se računaju u pomičnom zarezu, najčešće u rasponu $[0, 1]$
- U `uint8` se zaokružuje **samo jednom, na kraju** --- svako zaokruživanje trajno gubi informaciju

## Područje interesa (ROI)

- Često analiziramo samo dio slike --- **ROI** (*Region of Interest*)

```python
roi = img[120:150, 100:180]         # retci 120-149, stupci 100-179
print(roi.shape)                    # (30, 80, 3)

roi[:] = 0                          # POZOR: mijenja i izvornu sliku!
roi = img[120:150, 100:180].copy()  # neovisna kopija
```

\begin{deklaracija}
U forenzičkoj analizi izvorna slika se nikada ne mijenja --- radi se isključivo na kopiji.
\end{deklaracija}

# Osnovne operacije

## Vrste operacija na slici

- **Točkaste** --- izlaz ovisi samo o pikselu na istoj koordinati

$$g(m, n) = T\big(f(m, n)\big)$$

- **Lokalne** --- izlaz ovisi o pikselu i njegovom **susjedstvu** (filtri, konvolucija)
- **Globalne** --- izlaz ovisi o **svim** pikselima slike (histogram, Fourierova transformacija)

## Točkaste operacije

![](slike/p02_tockaste.jpg){width=100%}

- **LUT** (*lookup table*) --- tablica izlaznih vrijednosti za svih 256 mogućih ulaza
    - preslikavanje je obično indeksiranje: `g = lut[f]`
    - bilo koja točkasta operacija na `uint8` slici može se zapisati kao LUT

## Razlika dviju slika

![](slike/p02_razlika.jpg){width=100%}

- Izmjenu koju oko ne primjećuje razlika odmah otkriva
- Uvjet: slike moraju biti **poravnate** i jednako zapisane --- inače razlika pokazuje sve, a ne samo izmjenu

## Geometrijske operacije

- Izrezivanje, skaliranje, rotacija, perspektivne transformacije
- Novi pikseli ne padaju na mrežu izvornih → vrijednosti se **interpoliraju**
    - najbliži susjed, bilinearna, bikubična interpolacija

```python
mala = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
```

\begin{deklaracija}
Interpolacija uvodi periodične korelacije među pikselima --- trag koji otkriva da je dio slike skaliran ili rotiran.
\end{deklaracija}

# Histogram

## Histogram i kumulativni histogram

![](slike/p02_histogram.jpg){width=100%}

$$h(k) = \big|\{(m,n) : f(m,n) = k\}\big|, \qquad H(k) = \sum_{i=0}^{k} h(i)$$

```python
h = np.bincount(g.ravel(), minlength=256)    # ili cv2.calcHist
```

## Histogram slike u boji

![](slike/p02_histogram_rgb.jpg){width=100%}

- Za sliku u boji računaju se tri nezavisna histograma, za svaki kanal posebno
- Višedimenzionalni histogram opisuje zajedničku raspodjelu kanala (P3)

## Histogram ne vidi prostor

![](slike/p02_permutacija.png){height=60%}

\begin{deklaracija}
Histogram opisuje samo \textbf{koliko} je kojih vrijednosti, a ne \textbf{gdje} su u slici.
\end{deklaracija}

## Čitanje histograma

![](slike/p02_tipovi_histograma.jpg){width=90%}

- **Odsijecanje:** svi pikseli izvan raspona svedeni su na 0 ili 255 --- ta informacija je nepovratno izgubljena

# Poboljšanje slike

## Rastezanje histograma

- Raspon vrijednosti $[f_{min}, f_{max}]$ preslikava se na cijeli raspon $[0, 255]$:

$$g = \frac{f - f_{min}}{f_{max} - f_{min}} \cdot 255$$

- Nekoliko krajnjih piksela može onemogućiti rastezanje
    - zato se često odbacuje mali postotak najtamnijih i najsvjetlijih (npr. 0,5 %)
- Često je ugrađeno u automatiku uređaja za prikaz

## Ujednačavanje histograma

- Cilj: histogram u kojem su sve razine približno jednako zastupljene
- Funkcija preslikavanja je **normalizirani kumulativni histogram**:

$$g(m, n) = 255 \cdot \frac{H\big(f(m, n)\big)}{M \cdot N}$$

- Postupak:
    1. izračunati kumulativni histogram $H(k)$
    2. normalizirati ga na najveću vrijednost (255)
    3. koristiti ga kao LUT

```python
eq = cv2.equalizeHist(g)
```

## Rastezanje i ujednačavanje

![](slike/p02_rastezanje_ujednacavanje.jpg){height=86%}

## Logaritamsko i eksponencijalno preslikavanje

![](slike/p02_log_exp.jpg){width=100%}

- **Logaritamsko** preslikavanje razvlači tamne tonove --- ističe detalje u sjenama
- **Eksponencijalno** preslikavanje razvlači svijetle tonove

## Poboljšanje ostavlja trag

![](slike/p02_cesalj.png){width=100%}

- 8-bitna slika ima samo 256 mogućih vrijednosti
- Rastezanjem se one razmiču --- između njih ostaju **prazni stupci**
- Pravilan uzorak rupa i šiljaka („češalj") otkriva da je kontrast mijenjan, čak i kada slika okom izgleda prirodno

# Konvolucija i korelacija

## Klizni prozor

![](slike/p02_konvolucija_shema.png){width=90%}

- Prozor (jezgra) klizi preko slike; izlaz je **težinska suma** piksela ispod prozora

$$g(m, n) = \sum_{j}\sum_{k} h(j, k)\, f(m - j,\, n - k)$$

## Konvolucija i korelacija

- **Konvolucija** --- jezgra se prije množenja rotira za 180°
- **Korelacija** --- ista operacija bez rotacije:

$$g(m, n) = \sum_{j}\sum_{k} h(j, k)\, f(m + j,\, n + k)$$

- Za simetrične jezgre rezultat je isti
- Na rubovima nedostaju pikseli → **dopunjavanje** (nule, rub, zrcaljenje)

```python
k = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], np.float32) / 16
g = cv2.filter2D(img, -1, k, borderType=cv2.BORDER_REFLECT)
```

\begin{deklaracija}
\texttt{cv2.filter2D} računa korelaciju --- nesimetričnu jezgru treba prethodno rotirati.
\end{deklaracija}

## Korelacija kao mjera sličnosti

![](slike/p02_korelacija.jpg){width=100%}

- **Normalizirana korelacija** mjeri koliko je dio slike sličan zadanom uzorku
- Najveća vrijednost pokazuje gdje se uzorak nalazi
- Isti princip koristi se za otkrivanje **kloniranih** dijelova slike (copy-move)

## Primjeri filtara

![](slike/p02_filtri.jpg){height=88%}

## Konvolucija u forenzici

![](slike/p02_rezidual.png){width=88%}

- Zaglađivanjem se procjenjuje „čisti" sadržaj slike
- Oduzimanjem ostaje **rezidual**: šum i fini detalji
- U šumu se krije **otisak senzora** --- jedinstven za svaki fotoaparat

# Zaključak

## Ključno za forenziku

- Svaki korak nastanka i obrade slike ostavlja trag:
    - **demozaikiranje** --- korelacija susjednih piksela
    - **obrada u kameri** --- potpis proizvođača
    - **promjena kontrasta** --- „češalj" u histogramu
    - **skaliranje i rotacija** --- tragovi interpolacije
    - **šum senzora** --- otisak uređaja
- **Sljedeće predavanje (P3):** matematički model slike i digitalni formati --- prostori boja, zapis slike, JPEG, JFIF i EXIF
