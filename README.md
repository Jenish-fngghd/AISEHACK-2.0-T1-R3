# Sokhda kharif 2025 - SAR crop health and yield forecast

Final yield forecast for 966 farm plots in Sokhda village, Vadodara district, Gujarat, built
from six Capella X-band HH SLC acquisitions spanning 6 June to 12 November 2025.

**AISEHack 2.0 · Round 3 · Team GDHTM** · 966 plots · 447.5 ha · **710.0 t (1.587 t/ha)**

* * *

## Table of contents

- [Highlights](#highlights)
- [The result](#the-result)
- [Tech stack](#tech-stack)
- [Method](#method)
- [Pipeline](#pipeline)
- [Repository structure](#repository-structure)
- [Script reference](#script-reference)
- [Outputs](#outputs)
- [Prerequisites](#prerequisites)
- [Environment variables](#environment-variables)
- [Setup](#setup)
- [Running](#running)
- [Verification](#verification)
- [Design guarantees](#design-guarantees)
- [Troubleshooting](#troubleshooting)
- [Further documentation](#further-documentation)
- [Team](#team)

* * *

## Highlights

- **Every output is committed.** The result can be checked without installing anything or
  downloading the 3 GB of imagery. Start at [Outputs](#outputs).
- **Nothing is fitted to an outcome.** There is no harvest record for this village, so a
  supervised regressor would be fitted against labels we invented ourselves. The health index
  has five physically named parts and fixed weights.
- **The village total is mathematically invariant to the imagery**, by construction, and we
  say so. The modifier is normalised to an area-weighted mean of exactly 1.0 within each crop.
- **Every row of the deliverable is typed** as a forecast, a measurement, or a retrospective
  reconstruction, according to where the crop's calendar sits relative to the acquisitions.
- **19 defensibility checks with thresholds fixed before the run**, plus a 12-assertion
  regression suite. Both print a per-item table, so a failure names itself.
- **Ten experiments were built after the forecast was frozen**, each against a kill criterion
  written down in advance. Six died. None of them changed a shipped number.

* * *

## The result

| Crop | Plots | Area (ha) | Anchor t/ha | Forecast t/ha | Production (t) | Epistemic object |
|:--|--:|--:|--:|--:|--:|:--|
| Cotton (lint) | 455 | 193.4 | 0.730 | 0.730 | 141.2 | **forecast** |
| Groundnut | 221 | 137.7 | 2.514 | 2.514 | 346.1 | **near-complete measurement** |
| Rice | 86 | 47.4 | 1.690 | 1.690 | 80.2 | retrospective reconstruction |
| Bajra | 149 | 42.3 | 1.910 | 1.910 | 80.8 | retrospective reconstruction |
| Maize | 55 | 26.7 | 2.312 | 2.312 | 61.8 | retrospective reconstruction |
| **All** | **966** | **447.5** | - | **1.587** | **710.0** | three different objects |

Cotton is reported as **lint**, roughly 34% of the seed cotton a farmer picks, which is why
0.730 t/ha sits below the cereals. It leads on area, not on tonnage.

A fixed 500 m grid also gives **46 sub-village zones** of five or more farms, spanning health
indices 36.6 to 76.3, each with its own uncertainty column.

* * *

## Tech stack

| Layer | Choice |
|:--|:--|
| Language | Python 3.12 |
| Raster I/O | `rasterio` (GDAL) |
| Vector / parcels | `geopandas`, `pyproj` |
| Numerics | `numpy`, `scipy` |
| Tables | `pandas` |
| Morphology | `scikit-image` |
| Figures | `matplotlib`, `pillow` |
| External imagery | Microsoft Planetary Computer STAC (Sentinel-1 RTC, Sentinel-2 L2A) |
| External statistics | data.gov.in OGD API, MOAFW and Gujarat DES publications, ERA5-Land |
| Model | none trained. No fitting, no weights file, no checkpoint |

> ⚠️ **There is no trained model in this repository, and that is deliberate.** No plot-level
> harvest record for Sokhda is public, and PMFBY village CCE yields are gated behind an officer
> login. A regressor trained here would be scored against labels of our own construction.

* * *

## Method

```
yield_forecast[plot] = anchor(crop) x modifier[plot]
production           = SUM(yield x area)          -- never a mean of per-hectare rates
```

- The **anchor** sets the level for each crop, from a published statistic
  (`data_aux/anchors_r3.csv`, with sources).
- The **modifier** distributes plots within a crop. It is built from a z-scored health index
  and then normalised so its **area-weighted mean is exactly 1.0 within each crop**.
- That normalisation makes each crop's area-weighted yield equal its anchor by construction,
  so the village total reduces to `SUM(anchor_c x area_c)` and cannot be moved by the imagery.

**So the SAR decides exactly two things:** the ordering of plots within a crop, and which crop
each plot is. Everything scalar - the level, and the spread parameter `YIELD_SPREAD = 0.30` -
is injected by us and published rather than buried. `src/p3_build.py` is where this happens and
is short enough to read end to end.

* * *

## Pipeline

```
  vendor SLC (complex, slant range)
        |
        |  p1_prep.py        beta0 = SF^2 |z|^2  ->  sigma0  ->  gamma0, geocoded,
        |                    common 2 m and 5 m grids
        v
  calibrated backscatter rasters ................ results/cache/  (regenerated, not committed)
        |
        |  p1_features.py    966 parcels x 6 dates, negative-buffer ladder -5/-2/0 m,
        |                    coverage and NESZ gates -> 111 features per farm
        v
  per-farm feature table ........................ results/tables/p1_farm_features.csv
        |
        |  p3_build.py       five-part health index (level, growth, uniformity,
        |                    persistence, senescence; fixed weights)
        |                    crop map -> anchor x modifier -> aggregation
        v
  deliverable ................................... results/submission.csv        (966 rows)
                                                  results/tables/p3_village_summary.csv
                                                  results/tables/p3_zone_summary.csv (46 zones)
        |
        |  p3_checks.py  (19)   tests_regression.py  (12)   p3_figures.py  (9 figures)
        v
  verification and figures ...................... results/tables/p3_checks.csv
                                                  results/figures/p3_f1..f9.png
```

Ancillary data enters as **gates and corrections, never as predictors**. The 29 October scene
is excluded from the level features on a measured wind and rain confound; cotton completion is
dated to the MOAFW weekly report of 10 November 2025.

* * *

## Repository structure

```
AISEHACK-2.0-T1-R3/
├── src/
│   ├── common.py               every path, date, AOI and scene constant; run as a self-check
│   ├── stac.py                 Planetary Computer STAC access (anonymous)
│   ├── datagovin.py            data.gov.in client; the key lives outside the repo
│   ├── p0_*.py                 scene census, weather, witness stacks, Round 2 inheritance
│   ├── p1_*.py                 SLC preprocessing, calibration, features, stable targets
│   ├── p3_build.py             THE DELIVERABLE
│   ├── p3_checks.py            19-check defensibility battery
│   ├── tests_regression.py     12 failure-mode assertions
│   ├── p3_figures.py           the nine figures
│   ├── p3_composite.py         2x2 panel used in the check-in PDF
│   └── p3_*.py                 the ten post-freeze experiments
├── data_aux/
│   ├── anchors_r3.csv          published yield statistics used as anchors, with sources
│   └── inherited/              per-farm assets carried forward from Round 2
├── results/
│   ├── submission.csv          the deliverable, 966 rows
│   ├── tables/                 every intermediate and analysis table (46 files)
│   ├── figures/                p1_*.png and p3_f1..f9.png
│   ├── cache/                  derived rasters, 351 MB, regenerated (not committed)
│   └── log.jsonl               run ledger: every invocation and what it wrote
├── MIDNIGHT_CHECKIN.pdf        two-page technical brief
├── MIDNIGHT_CHECKIN.docx       the same content, editable
└── README.md
```

* * *

## Script reference

### Phase 0 - inventory and ancillary data

| Script | What it does |
|:--|:--|
| `p0_census.py` | census of every Sentinel-1 and Sentinel-2 scene over the village for the season |
| `p0_weather.py` | hourly meteorology at every Capella overpass, plus the season series (ERA5-Land) |
| `p0_witness.py` | full-season independent witness stacks per farm, through harvest |
| `p0_inherit.py` | copies, joins and verifies the per-farm assets inherited from Round 2 |

### Phase 1 - imagery to per-farm features

| Script | What it does |
|:--|:--|
| `p1_prep.py` | six SLCs to calibrated, geocoded beta0 / sigma0 / gamma0 on a common grid |
| `p1_calib.py` | adjudicates the calibration convention on all six scenes against the vendor's NESZ |
| `p1_features.py` | 966 x 111 per-farm features, buffer ladder, coverage and noise-floor gates |
| `p1_stable.py` | the look-side question and the wetness question, on persistent stable targets |
| `p1_traj.py` | six-date trajectory per crop, the groundnut-lift test, identifiability |
| `p1_xcheck.py` | cross-implementation check on our own radiometry |

### Phase 3 - deliverable and verification

| Script | What it does |
|:--|:--|
| `p3_build.py` | health index, final yield forecast, aggregation, `submission.csv` |
| `p3_uncertainty.py` | the four uncertainty terms, reported separately |
| `p3_validate.py` | spatial hold-out: refit in one half, apply to the other |
| `p3_checks.py` | the 19-check defensibility battery |
| `tests_regression.py` | 12 assertions, one per defect that once got past somebody competent |
| `p3_figures.py` | the nine figures |

### The ten post-freeze experiments

Built **after** the forecast was frozen, each against a kill criterion written down in advance.
None of them changes a shipped number.

| Script | Question | Verdict |
|:--|:--|:--|
| `p3_t2_wcm.py` | Can the Water Cloud Model be fixed and retried? | killed, unidentifiable |
| `p3_t1_gai.py` | Can SAFY's canopy proxy work on this stack? | killed on availability |
| `p3_dawidskene.py` | Does label fusion validate our crop map? | won, then voided by its own provenance control |
| `p3_fusion.py` | Does adding Sentinel-1 C-band improve the forecast? | real information, rejected on the held-out date |
| `p3_climatology.py` | Was 2025 an ordinary year at Sokhda? | survived; the non-farm control reversed the naive reading |
| `p3_harvest.py` | Can we test our own harvest-timing claim? | could not be run, and we say so |
| `p3_representative.py` | Is Sokhda typical of the district whose statistic we borrow? | survived as a flag, not applied |
| `p3_spatial.py` | Is the ranking the farm, or where the farm sits? | survived; 96% field-scale |
| `p3_edge.py` | Is it the farm, or the parcel outline? | survived; no parcel-size bias |
| `p3_voi.py` | What did each of the six acquisitions buy? | survived, and shrank a claim of ours |
| `p3_speckle.py` | Would the same 97 farms be named if we re-flew? | survived; 69% retention against a 10% floor |

Supporting: `p3_s1_season.py` (Sentinel-1 growth window), `p3_salvage.py` (were the killed
methods useful in any way), `p3_repr_control.py` (the control for `p3_representative.py`).

* * *

## Outputs

Everything below is committed, so a reviewer can check the result without running the pipeline.

| File | What it holds |
|:--|:--|
| `results/submission.csv` | **the deliverable.** 966 rows: `village_id, farm_id, crop_type, health_index, yield_forecast_t_ha` |
| `results/tables/p3_village_summary.csv` | village and per-crop totals making up 710.0 t |
| `results/tables/p3_zone_summary.csv` | the 46 sub-village zones |
| `results/tables/p3_farm_uncertainty.csv` | per-farm uncertainty |
| `results/tables/p3_checks.csv` | the 19 checks, one row each, with the pre-registered threshold |
| `results/tables/p1_farm_features.csv` | the 966 x 111 feature table the index is built from |
| `results/figures/p3_f1_deliverable.png` | the forecast, split by epistemic object |
| `results/figures/p3_f3_d1.png` | D1: Round 2 yield-to-date against Round 3 final forecast |
| `results/figures/p3_f2, f4..f9` | uncertainty, witness, climatology, spatial, value of information, speckle, edge |
| `results/log.jsonl` | run ledger: every script invocation and what it wrote |

* * *

## Prerequisites

- **Python 3.12**
- The challenge data: `anrf-aise-hack-2-0-round-3-sar-crop-yield-forecasting/`, including
  `Farm_boundaries_shp/` and `Village_Shp/`
- Network access, but **only** for the post-freeze experiments that fetch Sentinel-1 and
  Sentinel-2. The main pipeline runs offline.
- No account, key or token is required for anything in the main pipeline.

* * *

## Environment variables

All are read in `src/common.py`. All are optional if the data sits in its default location.

| Var | Required | Notes |
|:--|:--:|:--|
| `AISE_DATA` | recommended | path to the challenge data directory. Defaults to `./anrf-aise-hack-2-0-round-3-sar-crop-yield-forecasting/` |
| `AISE_R2` | for check D1 only | path to the Round 2 repository. Without it, D1 is the one check of 19 that cannot run |
| `AISE_VILLAGE` | - | village name, default `Sokhda` |
| `AISE_FARMS` | - | explicit path to the farm-boundary shapefile |
| `AISE_VILLAGE_SHP` | - | explicit path to the village shapefile |

* * *

## Setup

```bash
git clone https://github.com/Jenish-fngghd/AISEHACK-2.0-T1-R3.git
cd AISEHACK-2.0-T1-R3
pip install numpy pandas scipy geopandas rasterio scikit-image pyproj matplotlib pillow
export AISE_DATA=/path/to/anrf-aise-hack-2-0-round-3-sar-crop-yield-forecasting
```

```powershell
# Windows PowerShell
$env:AISE_DATA = "D:\path\to\anrf-aise-hack-2-0-round-3-sar-crop-yield-forecasting"
```

> ⚠️ **`PROJ_LIB` from another GDAL installation silently breaks `pyproj`'s CRS lookups.**
> `src/common.py` clears it before `rasterio` is imported anywhere. That line is deliberate and
> must stay ahead of the first `rasterio` import.

* * *

## Running

On Windows the scripts are invoked as `py -3.12`; on Linux or macOS use `python3.12`.

**1. Self-check.** Confirms the six scenes are found, the duplicate-SLC trap is clear, and the
SF-squared calibration assertion holds. It prints one line per scene:

```
py -3.12 src/common.py
```

**2. Rebuild the deliverable.** In this order:

```
py -3.12 src/p1_prep.py           # SLC -> beta0 / sigma0 / gamma0, geocoded
py -3.12 src/p1_calib.py          # the noise-floor adjudication, all six scenes
py -3.12 src/p1_features.py       # 966 x 111 per-farm features
py -3.12 src/p3_build.py          # anchors x modifier -> submission.csv + aggregation
```

`p1_prep.py` is the long step and writes to `results/cache/`. Everything after it is fast.

**3. Verify.**

```
py -3.12 src/p3_checks.py         # 19 checks, thresholds fixed before the run
py -3.12 src/tests_regression.py  # 12 failure-mode assertions
py -3.12 src/p3_figures.py        # the nine figures
```

**4. The post-freeze experiments** (optional, and each needs network access):

```
py -3.12 -u src/p3_climatology.py
py -3.12 -u src/p3_voi.py
py -3.12 -u src/p3_speckle.py
py -3.12 -u src/p3_spatial.py
py -3.12 -u src/p3_edge.py
py -3.12 -u src/p3_representative.py
py -3.12 -u src/p3_t1_gai.py
py -3.12 -u src/p3_t2_wcm.py
py -3.12 -u src/p3_dawidskene.py
py -3.12 -u src/p3_fusion.py
py -3.12 -u src/p3_harvest.py
```

* * *

## Verification

| Command | Expected |
|:--|:--|
| `src/p3_checks.py` | **19 / 19 pass** (18 / 19 without `AISE_R2`, D1 skipped) |
| `src/tests_regression.py` | **12 / 12 pass** |
| `md5sum results/submission.csv` | `8304407ed23bc67168fb26fca21a03d1` |
| row count of `results/submission.csv` | 966 |

Both suites print a per-item table rather than a single pass/fail, so a failure names the check
that broke and the value that broke it.

* * *

## Design guarantees

- **The submission is frozen and checksum-pinned.** Every post-freeze script re-verifies the
  md5 on the way out, so an experiment cannot quietly move the deliverable.
- **Controls abort, they do not warn.** A script whose own control fails exits with a message
  saying the result is void, rather than printing a number anyway.
- **Nothing is hardcoded that can be read.** Dates are scanned from the delivered data and
  every scene constant is read from the vendor's `_extended.json`. Round 2 measured its own
  portability debt at 20 of 33 files hardcoding acquisition dates; `src/common.py` exists to
  make that impossible.
- **No secret is ever printed.** The only credential the code can use is a data.gov.in key read
  from `~/.config/aisehack/datagovin.key`, outside the repository. It is never logged, echoed,
  or written into an output, and retry messages deliberately omit the request URL because the
  URL carries the key.
- **Privacy.** Some land records carry owner names. Only the crop column was ever extracted,
  only aggregate accuracy is ever reported, and no owner name or individually linked survey
  number appears in any committed file. The source record is excluded by `.gitignore`.
- **Not in the repository, by policy:** the vendor SLCs (3.0 GB, the vendor's to distribute),
  `results/cache/` (351 MB, regenerated by `p1_prep.py`), the owner-name land record, and every
  credential file.

* * *

## Troubleshooting

- **`CRSError` or a projection failure from `pyproj`** - a stale `PROJ_LIB` from another GDAL
  install. Import `src/common.py` first, or unset the variable; see the note under
  [Setup](#setup).
- **`FileNotFoundError` on the shapefile** - `AISE_DATA` is unset or points above the data
  directory. Run `py -3.12 src/common.py`; it prints the paths it resolved.
- **Check D1 fails or errors** - it needs the Round 2 repository beside this one, or `AISE_R2`
  set to it. The other 18 checks are self-contained.
- **A post-freeze script exits with "control failed"** - that is the intended behaviour. The
  experiment's own control did not hold, so its result is void and is not reported.
- **`UnicodeEncodeError` on Windows** - the console is cp1252 and some scripts print symbols
  outside it. Run with `py -3.12 -u`, which the post-freeze commands above already do.
- **`p1_prep.py` looks stuck** - it is the long step, processing six SLCs into `results/cache/`.
  The ledger at `results/log.jsonl` records progress.

* * *

## Further documentation

- **`MIDNIGHT_CHECKIN.pdf`** - the two-page technical brief: strategy, novelty, assumptions,
  results, pivots and the final roadmap. `MIDNIGHT_CHECKIN.docx` is the same content, editable.
- **Module docstrings.** Every script opens with what it decides and what would have falsified
  it. `src/p3_build.py` and `src/p3_checks.py` are the two worth reading first.
- **`results/log.jsonl`** - the run ledger, if you want to see the order things actually ran in.

* * *

## Team

**Team GDHTM** - Jenish, Mahi and Yash. Built for AISEHack 2.0, Remote Sensing track (Satellite
Driven Crop Yield Forecasting), Round 3 and the Goa Grand Finale.
