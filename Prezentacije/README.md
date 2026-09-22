# Prezentacije za predavanja

Prezentacije kolegija *Forenzička analiza digitalne slike* (FESB).

## Popis predavanja

| # | Predavanje | Izvor | Slajdovi |
|---|---|---|---|
| 1 | Uvod u forenziku digitalne slike | [md](Predavanje01-Uvod.md) | [pdf](Predavanje01-Uvod.pdf) |
| 2 | Uvod u digitalnu obradu i analizu slike | — | — |
| 3 | Matematički model slike | — | — |

## Struktura

```
Prezentacije/
├── README.md                 <- ovaj popis
├── build_slides.py           <- generiranje PDF-a
├── fesb_slides.tex           <- zajednicka Beamer tema (boje, podnozje, naslovnica)
├── slides_filter.lua         <- slajd sa samo slikom -> bez podnozja; deklaracije; medjuslajdovi
├── PredavanjeNN-Naziv.md     <- izvor (pandoc markdown, H2 = novi slajd)
├── PredavanjeNN-Naziv.pdf    <- generirani slajdovi
├── dijagrami/                <- skripte koje generiraju vlastite dijagrame u slike/
├── slike/                    <- slike svih predavanja
└── OLD/                      <- stare prezentacije kolegija
```

## Generiranje PDF-a

Preduvjeti: `pandoc`, `xelatex`, `lmodern`, DejaVu fontovi; za dijagrame `python3` i `matplotlib`.

```
./build_slides.py            # sve prezentacije
./build_slides.py 01         # samo Predavanje01
```

Za svaku datoteku `Predavanje*.md` generira se `.pdf` istog imena.

## Konvencije

- H1 (`#`) je naslov cjeline, H2 (`##`) je novi slajd.
- Jedan slajd = jedna ideja.
- Slike svih predavanja idu u zajednički `slike/`, s opisnim imenima; izvor se navodi u opisu slike.
- Imenovanje: `PredavanjeNN-Naziv.md`, dvoznamenkasti broj termina.
- Izgled se mijenja isključivo u `fesb_slides.tex` --- nikada u pojedinoj prezentaciji.
