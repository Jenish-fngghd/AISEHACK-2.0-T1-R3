# Round 3 research log — append only

Every move, what it returned, what it changes. Evidence grade on every claim:
`OWN` measured on our data/metadata · `MECH` someone else's claim, mechanism verified
independently · `THEIRS` rests on an outside assertion, not established for us.

---

## P0-1 — archive integrity  `OWN`

**Extracted already; 41 files, 8 folders.** Verified every one of the six SLC `.tif`
against **Capella's own `_digest.json` md5**, which is a stronger check than comparing
to Round 2 — it tests the delivery, not just the consistency of two copies.

| date | vendor md5 | verdict |
|:--|:--|:--|
| 20250606 | `eb34553c39caaa9e1fa1d3c254619dc0` | OK |
| 20250619 | `d7f9a6e88d58544dac6a26f9079d5a83` | OK |
| 20250814 | `ce13630465accbaadf3b4ac66865d70d` | OK |
| 20251013 | `3fb596bf77ffd699b7ce2ce86f3bce28` | OK |
| 20251029 | `7f81736ea15346515f9cef3e5a605102` | OK |
| 20251112 | `f216c765a7397aed7412c51eb0220b80` | OK |

All four shared `_extended.json` md5s match Round 2 exactly, and **all ten shapefile
component files match Round 2 byte for byte**. So R2's geometry work and its
measurements on the four shared dates transfer without qualification, and `farm_id`
1–966 means the same polygon in both rounds.

**The duplicate-SLC trap is still in the archive**, and it is byte-identical: the
`20250619` folder contains a second copy of the June 6 SLC with md5
`eb34553c39caaa9e1fa1d3c254619dc0`, matching the June 6 file exactly. Guarded in
`src/common.py::_scan_scenes()` by requiring the date in both folder and basename and
asserting exactly one match; `_selfcheck()` asserts the duplicate still exists, so if
the archive ever changes the test fails loudly rather than passing vacuously.

**Answers A4 (§1.3): the description is wrong.** There is no "expanded village AOI"
and no "expanded set of villages" — the delivered shapefiles are the Round 2 files
unchanged. One village, Sokhda, 966 plots. Worth one question to the host and one
honest sentence in the writeup.

*Also in the archive and not mentioned in §2:* each folder carries a
`CAPELLA_..._GEO_HH_..._preview.tif` of 184–190 MB. "Preview" understates it at that
size — these are geocoded products and need looking at before we assume our own
geocoding is the only route to the ground. **Open item, P0-8.**

## P0-2 — scaffold and self-check  `OWN`

`src/common.py` written before any processing code, self-check passing. It reproduces
the §2.1 table *from the delivered metadata* rather than transcribing it:

```
20250606  12:55 IST   left-look  inc=35.244  SF=0.00212186  NESZ=-26.13 dB
20250619  07:44 IST   left-look  inc=28.768  SF=0.00236205  NESZ=-27.76 dB
20250814  08:41 IST   left-look  inc=28.692  SF=0.00198903  NESZ=-27.97 dB
20251013  07:56 IST   left-look  inc=31.528  SF=0.00136443  NESZ=-27.35 dB
20251029  01:37 IST  right-look  inc=29.840  SF=0.00155765  NESZ=-27.74 dB
20251112  19:22 IST   left-look  inc=29.746  SF=0.00162432  NESZ=-27.72 dB
```

Portability debt paid up front: `DATES` is **scanned** from the delivered folders, and
every scene constant is read from `_extended.json` at call time. No date literal exists
downstream of `common.py`. `beta0()` squares the scale factor and `_selfcheck()`
asserts it, so Round 2's shipped calibration defect cannot silently recur.

## P0-3 — Sentinel-1 / Sentinel-2 scene census  `OWN`

`src/p0_census.py`. **Kill criterion written before the run: fewer than three S2 scenes
under 20% cloud between 1 Oct and 30 Nov kills the late-season optical lead.**

Result: **20**. The lead lives, decisively.

| month 2025 | S2 scenes | min cloud |
|:--|--:|--:|
| May | 16 | 0.369% |
| Jun | 16 | 21.265% |
| Jul | 14 | 92.554% |
| Aug | 16 | 84.890% |
| Sep | 16 | 35.462% |
| **Oct** | 14 | **0.003%** |
| **Nov** | 16 | **0.001%** |
| Dec | 6 | 0.001% |

**Round 2's "there is no optical over Sokhda" was exactly right for the window it
measured and wrong to generalise, precisely as §5.1 anticipated.** June–September is
unusable; October–December is close to perfect. Nine distinct clear dates fall between
13 Oct and 12 Dec.

**The luck repeats.** Round 2 had a same-day 0.003%-cloud S2 scene on its last Capella
date. Round 3 has one again: **12 November 2025, 0.001% cloud, same day as the final
Capella acquisition.** Two of six Capella dates now carry a same-day, essentially
cloud-free optical witness.

**And the gap is informative.** 29 October — the anomalous scene on every other axis —
is the one new date with *no* clean optical partner: nearest S2 is 28 Oct at 63.4%
cloud, with 23 Oct (16.8%) and 7 Nov (0.001%) bracketing it. Every independent check
of that date will have to be indirect.

Sentinel-1: **18 scenes, 7 May – 9 Dec, all descending relative orbit 34, VV+VH** —
one orbit only, so no incidence mixing, and the series extends 27 days past the last
Capella date. This is the same series R2 used, extended through harvest.

**Changes:** the reflexive "no optical exists here" line is retired for this round. A
dense late-season optical witness exists and it covers the entire forecast-critical
window. Whether it stays a witness or is promoted to an input is a §5.1 decision with a
real cost, not a free win — but the option is now real and measured.

## P0-4 — overpass-hour meteorology  `OWN`

`src/p0_weather.py`, Open-Meteo ERA5-Land archive, hourly, 1 May – 15 Dec. One value
for the whole village, so under the resolution-ceiling rule (11 km and beyond explains
**0.000** of within-village variation) it may inform *timing and level* only and must
never be used to rank farms.

| date | IST | look | RH% | dew-pt depression °C | soil moist. | rain 24 h | rain 72 h |
|:--|:--|:--|--:|--:|--:|--:|--:|
| 20250606 | 12:55 | left | 45 | 13.9 | 0.151 | 0.0 | 1.5 |
| 20250619 | 07:44 | left | 95 | **0.9** | 0.434 | 24.4 | 66.6 |
| 20250814 | 08:41 | left | 89 | 2.0 | 0.196 | 3.3 | 6.5 |
| 20251013 | 07:56 | left | 71 | 5.5 | **0.133** | 0.0 | 0.0 |
| **20251029** | **01:37** | **right** | 75 | 4.9 | **0.372** | 0.0 | **55.7** |
| 20251112 | 19:22 | left | 63 | 7.4 | 0.227 | 0.0 | 0.0 |

**The dew hypothesis for the night pass does not survive its own check.** Dew requires
the dew-point depression to approach zero. On 29 Oct at 01:37 it is **4.9 °C**, and on
12 Nov at 19:22 it is 7.4 °C — both drier than 19 June (0.9 °C) and 14 August (2.0 °C),
which are morning passes. **The two new acquisitions are not dew-affected; two of the
four *old* ones are closer to saturation than either.** This kills a confounder §7.1
budgeted for and hands us the reverse finding, which is more useful.

**But a larger confounder replaces it, and it is the significant result of Phase 0.**

### An unseasonal late-October rain event sits between 13 Oct and 29 Oct

| day | rain mm | soil moisture |
|:--|--:|--:|
| 15–25 Oct | ~0.9 total | 0.116–0.139 |
| **26 Oct** | **39.6** | 0.254 |
| **27 Oct** | **26.9** | 0.411 |
| **28 Oct** | **14.7** | 0.417 |
| **29 Oct (overpass)** | 0.1 | **0.382** |
| 30 Oct – 1 Nov | 28.0 | 0.395–0.418 |
| 12 Nov (overpass) | 0.0 | 0.227 |

**81.2 mm over 26–28 October, then 28 mm more over 30 Oct – 1 Nov.** Soil moisture
triples, 0.127 → 0.417, and the 29 October acquisition lands on the descending limb at
**0.382 — the wettest soil of any post-monsoon date, and second-wettest of all six
acquisitions, behind only the 19 June monsoon-onset scene.** October's rain total is
111.5 mm, nearly all of it in that one week; November's is 10.4 mm, all before the 4th.

Four consequences, and they reorder Phase 1:

1. **29 October is not a clean late-season scene.** Soil moisture is a first-order
   X-band term and it bites hardest exactly where the canopy is gone — the harvested
   cereal fields that should read dark. A "harvest / senescence" reading of 29 Oct is
   confounded, and not by dew but by wet ground.
2. **The 29 Oct ↔ 12 Nov pair is confounded on three axes at once** — opposite look
   sides, 0.382 → 0.227 soil moisture, and 14 days of phenology. §7.1 hoped this was a
   geometry-matched pair; the incidence match (0.094°) is real but it is the least of
   what separates the two scenes. **Any difference feature built on this pair must
   carry a soil-moisture control, and the groundnut-lift test of §4 needs its control
   strengthened: canopy-to-bare-soil and wet-to-dry both live in that difference.**
3. **12 November is clean**: zero rain for eight days, soil on a smooth monotonic
   drying limb, no dew, left-looking like the four Round 2 dates, and a same-day
   0.001%-cloud optical witness. It is the best-conditioned acquisition in the stack.
4. **The event is agronomically real and it is a yield story no other team holds.**
   Unseasonal rain at the end of October in central Gujarat lands on open cotton bolls
   (staining, quality loss) and on groundnut at lifting (delayed lift, pod sprouting,
   aflatoxin risk) — and it falls in the exact gap between Round 2's last observation
   and Round 3's new ones. It is a checkable, dated, physical event with a direct yield
   consequence for the two crops that are 74% of the village. **This belongs in the
   forecast, not only in the caveats.** `MECH` on the agronomic consequence pending
   R-A; `OWN` on the event itself.

Monsoon totals for the record: May 24.2, Jun 197.1, Jul 265.8, Aug 267.4, Sep 201.9,
Oct 111.5, Nov 10.4, Dec 0.0 mm.

## P0-5 — witness fetch launched  `OWN`

`src/p0_witness.py` running in background: 18 S1 RTC dates (VV and VH) and every S2
date under 20% cloud, per farm, with a per-farm SCL valid fraction rather than a
scene-level cloud percentage — a village cloud number says nothing about one 0.27 ha
field. Both stacks extend past 12 November.

Sentinel-1 leg finished in 3 minutes: **all 18 dates, both polarisations, 36 columns,
no partial tiles dropped**. Sentinel-2 leg still running.

## P0-6 — inherited per-farm assets  `OWN`

`src/p0_inherit.py`. Twelve assets copied into `data_aux/inherited/`, none read across
from the frozen Round 2 tree at analysis time.

| asset | rows × cols | join |
|:--|--:|:--|
| `embed` (AlphaEarth 64-band) | 966 × 65 | copied |
| `s1_agree` (per-farm `s1_ok`/`emb_ok`) | 956 × 6 | partial — e17's 956-farm analysis set |
| `label_dist` (five-class posterior) | 966 × 10 | exact |
| `uncert` (calibrated sampling SE) | 885 × 5 | partial — e11 excluded the smallest plots |
| `gee` (Dynamic World + WorldCereal) | 966 × 9 | exact |
| `consensus` (six teams' labels) | 966 × 10 | exact |
| `calib_ref` (SF² four-date features) | 966 × 61 | copied — **reproduction target, not input** |
| `anchors` (461 Vadodara season records) | 461 × 7 | copied |
| `orion_feat` (third party) | 966 × 50 | exact |
| `orion_ndvi` (third party) | 966 × 13 | exact |
| `orion_vill` / `orion_zone` (third party) | 6 × 10 / 46 × 8 | copied |

Both partial joins are by design, not corruption, and both are documented in the
experiment that produced them. Nothing was patched.

### The third-party tables verify

The prompt's standard for a competitor file is that the join must reproduce a figure
the team published themselves. Aggregating Orion's `farm_yield.csv` by `crop_type`,
area-weighted, reproduces **every cell** of their published `village_summary.csv`:

```
Bajra      n 167/167  area  57.7306/57.7306  y 1.6922/1.6922  prod   97.6945/97.6945
Cotton     n 101/101  area  61.2614/61.2614  y 1.0766/1.0766  prod   65.9548/65.9548
Groundnut  n 296/296  area 115.8259/115.8259 y 2.4649/2.4649  prod  285.4969/285.4969
Maize      n 293/293  area 130.3978/130.3978 y 2.7900/2.7900  prod  363.8156/363.8156
Rice       n 109/109  area  82.3240/82.3240  y 2.2910/2.2910  prod  188.6006/188.6006
ALL  1001.5624 vs published 1001.5623679638768
```

So `orion_feat.csv`'s `g0_db_T1..T4` is genuinely the feature table behind their
shipped product, and the cross-implementation radiometry check of §7.3 is armed and
can be run the moment our own per-farm γ⁰ exists. Their aggregation rule is also now
readable rather than inferred: **production is `Σ(yield × area)` and the reported
per-crop yield is the area-weighted mean** — the rule §7.3 and R-F say we should use,
confirmed as what a shortlisted team actually did.

### An unplanned finding that bears on the groundnut dispute  `OWN`

§3.1 records Orion's argument — from their code comments — that groundnut in Gujarat is
a Saurashtra crop and that Sokhda's 30.8% groundnut share is an over-allocation, their
external agro-zone reference putting it near 16%.

**Their own shipped map does not implement that argument.** Orion assign groundnut
**296 of 966 plots and 25.9% of area** — far closer to our 30.8% than to the 16% their
comments cite. The team that made the case against a high groundnut share shipped a
high groundnut share.

That does not make 30.8% right. It does mean the strongest external argument against
our second-largest class was not acted on by the people who made it, which lowers what
it can be cited for. Their crop mix by area, against ours:

| crop | ours (R1 reconstruction) | Orion shipped |
|:--|--:|--:|
| Cotton | **43.0%** | **13.7%** |
| Groundnut | 31.0% | 25.9% |
| Rice | 10.6% | 18.4% |
| Bajra | 9.4% | 12.9% |
| Maize | **6.0%** | **29.1%** |

Groundnut is the crop we *agree* about most closely. Cotton and maize are where the
six-team κ of 0.060 actually lives — a 29-point disagreement on cotton and a 23-point
disagreement on maize, in opposite directions. **The label dispute worth resolving in
Round 3 is cotton-versus-maize, not groundnut**, and that reorders which comparison is
worth running against §4's lift test. `OWN`.

## P0-7 — kharif 2025-26 anchors: leads, not yet evidence  `THEIRS`

First pass only; R-A does this properly. Nothing below is usable until sourced to a
primary document.

- **Groundnut, Gujarat, kharif 2025-26: 2,092 kg/ha**, down from 2,210 in 2024-25, on
  22.02 lakh ha (up 2.93 lakh ha). Attributed to the Solvent Extractors' Association —
  a trade body, not the Directorate. `THEIRS` until matched against an official release.
- **Cotton lint, Gujarat: 597 kg/ha** (CEIC, March 2025), against the 647 kg/ha Round 2
  used. A ~8% difference on the anchor that carries the level for 43% of our area, so it
  matters and must be resolved to a primary source.
- National kharif foodgrain 2025-26 First Advance Estimates released 27 Nov 2025;
  Second Advance Estimates for 2025-26 exist. Third/Final should exist by now.
- `desagri.gov.in` refused the connection (ECONNREFUSED 164.100.114.118:443) — retry.
- `data.gov.in` returns **HTTP 403** to a plain fetch. The catalog page confirms the
  season-wise Gujarat series exists and is published per estimate round (a "Third
  Advance Estimates … 2023-24" resource is listed), so resource
  `66e33662-6f0b-4bd9-8771-5a33f8ff6cdd` is the right target and the API key is the
  right route.

**BLOCKER, needs the user.** `~/.config/aisehack/datagovin.key` is present, and so are
`gee_oauth.json` and `usda_ers.key`. All three were pasted into a chat transcript and
the standing instruction is to **rotate before use**. Rotation is a human action. Until
it happens the data.gov.in route stays closed, and with it the single best candidate for
a season-matched, year-matched anchor.

## P0-8 — an unexamined 1.1 GB in the archive  `OWN`

Each scene folder carries a `CAPELLA_..._GEO_HH_..._preview.tif` at 184–190 MB, six of
them, 1.13 GB total — never mentioned in the dataset description and, as far as the
Round 2 record shows, never opened by us or by any competitor. At that size "preview"
is a misnomer; these are plausibly geocoded detected products. If they carry a usable
map projection they are an independent check on our own GCP geocoding, and possibly a
shortcut past it. **Open it before Phase 1 designs the geocoding step.**

## P0-9 — the witness stacks landed, and one of them corroborates the rain event  `OWN`

`witness_s1.csv` 966 × 37 (18 dates, VV and VH, no scene dropped) and `witness_s2.csv`
966 × 31 (15 clear dates). 956 of 966 farms carry values on every date; the missing 10
are the degenerate parcels enclosing ~0 ha, exactly as in Round 2.

Village-median S2 NDVI: 0.303 (13 Oct) → 0.304 (18 Oct) → 0.307 (23 Oct) → **0.363
(7 Nov)** → 0.359 (9 Nov) → 0.339 (12 Nov) → 0.323 (17 Nov) → 0.328 (22 Nov). The
village gets **greener** into early November before turning over. That is not a
senescing kharif landscape and it needs explaining in Phase 1.

### ERA5 soil moisture is not just reanalysis here — C-band sees it

**Kill criterion, written before the run: if C-band VH does not track the ERA5
soil-moisture series across the 18 independent S1 dates, the reanalysis series is not
evidence about ground condition and P0-4 must be restated as a model output.**

| | Spearman ρ vs ERA5 soil moisture | p |
|:--|--:|--:|
| S1 VH village median | **+0.749** | 0.0004 |
| S1 VV village median | +0.692 | 0.0015 |

It survives. An independent satellite, a different band, a different polarisation and a
different geometry track the reanalysis soil-moisture series across the whole season.
**P0-4 is upgraded from a reanalysis claim to a corroborated one.**

And the individual date does the same work:

| S1 date | soil moisture | VH median dB |
|:--|--:|--:|
| 22 Oct | 0.135 | −15.31 |
| **3 Nov** | **0.385** | **−13.55** |
| 15 Nov | 0.181 | −15.35 |

**A +1.8 dB excursion at 3 November, between two dry dates 24 days apart, at a soil
moisture of 0.385 — within 0.013 of the 0.372 at the 29 October Capella overpass.**
Phenology is monotonic over 24 days; this is not phenology. So before a single X-band
pixel is read we have an independent, quantified prior for the size of the wet-soil
confound on 29 October: **order 2 dB at C-band VH.** X-band HH at a shallower incidence
will not be identical, but this bounds the problem and gives the Phase 1 test something
to predict rather than merely discover.

## P0-8 resolved — the "preview" is a full geocoded product  `OWN`

Opened. `CAPELLA_..._GEO_HH_..._preview.tif` is **not a thumbnail**:

- **CRS: EPSG:32643, WGS 84 / UTM zone 43N** — fully geocoded by the vendor
- **26,678 × 26,850 pixels at 0.74 m**, covering ~19.7 × 19.6 km
- one band, **uint8**, nodata 0

So the vendor ships its own geocoding of every scene, and Round 2 never opened it.

**What it is not: a radiometric source.** uint8 with a gappy histogram (values 2, 3, 4
and 6 are empty while 1 holds 27% of pixels) means a nonlinear display stretch over a
quantised source. There is no route back to β⁰ and it must never feed a calibrated
number.

**What it is: an independent geocoding reference at 0.74 m, from the vendor, for all six
scenes.** Round 2's geocoding rests on a GCP fit whose only quality measure was its own
leave-one-out residual — a self-assessment. This is an external one. It also gives the
look-side question (§7.1) a direct handle: the 29 Oct right-looking scene is geocoded by
Capella into the same UTM grid as the five left-looking ones, so the geometric part of
the look-side difference can be separated from the radiometric part by construction.

Assuming the stretch is monotone — testable — farm-level *rank* comparisons are also
available as a sanity check, though not as a feature.

**Changes:** the geocoding step in Phase 1 gains an external acceptance test, and §3.6's
thin-plate-spline decision can be scored against the vendor's own product rather than
against itself.

## P0-10 — A1, A2, A3 answered, and the deadline is not what we thought  `OWN`

The Kaggle web page is a JavaScript app and returns only its title to a fetch. The
**Kaggle API**, authenticated from `~/.kaggle/kaggle.json`, returns the same information
without rendering.

### ★ The deadline is 12:30 IST on 3 September, not end of day

Kaggle API deadlines are UTC. Converting all three rounds:

| round | API deadline (UTC) | IST |
|:--|:--|:--|
| R1 | 2026-07-25 06:25 | 25 Jul, **11:55** |
| R2 | 2026-08-12 18:30 | 13 Aug, **00:00** (midnight, i.e. end of 12 Aug) |
| **R3** | **2026-09-03 07:00** | **3 Sep, 12:30** |

R2's converts to exactly midnight IST, which is what makes the UTC reading certain
rather than assumed — an "end of day IST" deadline is exactly 18:30 UTC.

**R3's is 12:30 IST on 3 September — midday, on the second day of the Goa finals.** The
working assumption of "3 September, end of day" overstates the budget by about eleven
and a half hours, on the morning we will be presenting. §9.6's schedule already said
finish by 1 September; this makes that a hard requirement rather than a safety margin.
**Flagged to the user; worth confirming against the host's own written wording, since
this is the API's field and not a sentence someone wrote.**

Other metadata: R3 is `Community` category, **no `evaluation_metric` set** (R1 had Mean
Squared Error; R2 had none) — consistent with a rubric-judged round. 5 submissions/day,
team size 10, created 20 Aug, opened 22 Aug. Our R1 rank is recorded as **2**.

### A1 — there is no submission template, and there was none in Round 2 either

The full paginated file listing gives **41 files for R3**: six scene folders and the two
shapefile folders, nothing else. Round 2's listing gives **31 files**, and it likewise
contains **no `Sokhda_Dummy_Submission.xlsx`**.

So the host's dummy submission was never distributed through the Kaggle Data tab. Round
2's log records where it came from: *"User supplied the host's sample writeup and
`Sokhda_Dummy_Submission.xlsx`"* — a host channel outside Kaggle.

**Action for the user, and it is worth real points:** check that same channel for a
Round 3 template. In Round 2 that file caught a **1000× unit error that every internal
check had passed**, because no internal check can know a unit convention that exists
only in the host's file. It is the single highest-value document we do not have.

### A2 — the unit, decided and defensible either way

Round 2's shipped schema, from the host's own dummy:
`village_id, farm_id, crop_type, health_index, yield_estimate_to_date`, with
`village_id = 1` (not the shapefile's `ID_1 = 22`), 966 rows, `farm_id` 1–966, and
**yield in tonnes/hectare**, host range 1.24–9.00.

R3 drops health and asks for a forecast, so the natural carry-forward is
`village_id, farm_id, crop_type, yield_forecast_t_ha` plus the supporting per-plot
statistics the round explicitly asks for. **Carry the unit guard**
(`assert max < 25.0` — no kharif crop yields 25 t/ha) and the `village_id = 1`
assertion; both are cheap and both caught something real.

The dummy's per-crop bands were explicitly synthetic and "not the expected or correct
answer", so they are not a calibration target — worth remembering before anyone reads a
Round 3 template as ground truth.

Also confirmed independently this round: the official district table calls the crop
**"Cotton(lint)"** in its own crop vocabulary, which corroborates §3.1's lint convention
from a source we had not used for that purpose.

### A3 — unresolved, and it cannot be resolved from here

The rubric's "quality of the video" against the Description's "No video is required" is
in the host's prose, which the API does not expose. Assume no video, note the
discrepancy in the writeup, and ask on the same channel as A1.

### Round 2 freeze re-verified

`results/submission.csv` md5 `89b0e4e2aef63ace4989fc0a44590ee5` — unchanged.

## P0-11 — the kharif 2025-26 anchor hunt: a clear negative and a clear route  `OWN`/`THEIRS`

The data.gov.in key works (`status: ok`, 246,091 records on the district APY resource).
Nothing below prints or logs it.

**Definitive negative on the never-opened resource.** `66e33662-…` is a **catalogue**,
not a resource — the API answers `"Meta not found"`. Its two actual resources are:

| resource | content |
|:--|:--|
| `3d8218ff-3b1e-4b92-9734-466620b065b0` | Third AE, **food grains**, Gujarat, **2023-24** |
| `0e2f71a5-6f48-4c07-9593-1c2cc55655b1` | Third AE, **oil seeds**, Gujarat, **2023-24** |

Probing every combination of {first, second, third, fourth, final} × {food-grain,
oil-seeds, commercial, other} × {2023, 2024, 2025} returns **only those two**. So:

**data.gov.in's Gujarat advance-estimates series stops at 2023-24, and carries no
commercial-crops table at all — meaning no cotton.** The §6 hope that this resource
would yield a season- and year-matched anchor **does not survive contact.** Recording it
so nobody spends the hour again.

What it does give, at Directorate-of-Agriculture provenance, units **area '000 ha,
production '000 t, yield kg/ha**:

| Gujarat 2023-24, 3rd AE | area | production | **yield kg/ha** |
|:--|--:|--:|--:|
| Groundnut | 1694.42 | 4642.46 | **2739.85** |
| Castor seed | 724.77 | 1551.72 | 2140.99 |
| Sesamum | 163.31 | 130.71 | 800.42 |
| Total oilseeds | 3126.94 | 7368.62 | 2356.50 |

**Also confirmed: the district APY resource has not been extended.** Filtering to
VADODARA returns **461 records**, exactly the count already cached in the inherited
`anchors` asset, and the years still begin at 1997. No new data there.

**National context, primary source.** PIB, 10 March 2026, *Second Advance Estimates
2025-26*: kharif foodgrain 1741.44 LMT, kharif rice 1239.28 LMT, kharif maize a record
302.47 LMT, kharif groundnut 112.94 LMT (up 8.82 on 104.12), cotton 290.91 lakh bales of
170 kg. Yields are stated to be **CCE-based**. Third AE adds the summer season — and
given today's date it may now exist. National, so context and not an anchor.

**Trade/secondary, `THEIRS`, listed for R-A to chase to a primary document:**
Gujarat groundnut kharif 2025-26 at **2,092 kg/ha** on 22.02 lakh ha (SEA); Gujarat
cotton lint **597 kg/ha** (CEIC, Mar 2025) against the **647** Round 2 used — an 8% move
on the anchor carrying the level for 43% of our area.

**Route that remains open for R-A:** the Directorate of Agriculture Gujarat's own
publications (`dag.gujarat.gov.in` — the indexed `index.htm` 404s, so find the current
path), `desagri.gov.in` (refused connection today, retry), the UPAg portal, and the PIB
Third Advance Estimates annexure tables, which are where state-wise numbers live.

---

## Phase 0 gate

| gate condition | status |
|:--|:--|
| six scenes resolve correctly | **pass** — scanned, not hardcoded; duplicate trap guarded and asserted |
| shared four confirmed identical | **pass** — plus all six verified against the vendor's own digest |
| external fetches running or blockers documented | **pass** — S1 18 dates and S2 15 dates landed; weather landed; anchor blockers documented above |
| inherited per-farm assets joined and verified or dropped | **pass** — 12 copied, 2 partial joins explained, third-party table verified to every digit |
| A1–A4 answered or recorded unanswerable | **A1 pass** (no template exists on Kaggle; user to check the host channel) · **A2 pass** · **A3 unanswerable from here** · **A4 pass** (description is wrong) |

Two items carried into Phase 1 rather than blocking it: the host-channel template check
(user action) and the Gujarat kharif 2025-26 anchor (R-A).

---

# Phase 1 — comprehensive EDA

## P1-1. The chain rebuilt on six scenes; incidence from orbit geometry — `OWN`

`src/p1_prep.py`. SLC → β⁰ = SF²·|z|² → per-pixel θ from the 108 orbit state vectors →
σ⁰ = β⁰·sinθ, γ⁰ = β⁰·tanθ → geocode to EPSG:32643 with the scene's own GCPs, `average`
resampling (which *is* the multilook: averaging power over the slant pixels in a ground
cell is what multilooking does, and it happens inside the warp). Two grids, 5 m base and
2 m fine. β⁰ is written out as well as γ⁰ because the noise-floor test below is a
statement about the product's radiometry, not about our incidence correction.

**Incidence validated against the vendor's annotated centre angle, all six dates:**

| date | look | ours (°) | vendor (°) | Δ (°) | AOI span (°) |
|:--|:--|--:|--:|--:|--:|
| 06 Jun | left | 35.2402 | 35.2441 | −0.0039 | 35.05–35.44 |
| 19 Jun | left | 28.7608 | 28.7683 | −0.0075 | 28.54–28.98 |
| 14 Aug | left | 28.6865 | 28.6921 | −0.0057 | 28.47–28.91 |
| 13 Oct | left | 31.5222 | 31.5278 | −0.0056 | 31.31–31.74 |
| **29 Oct** | **right** | 29.8344 | 29.8399 | −0.0055 | 29.61–30.04 |
| **12 Nov** | left | 29.7470 | 29.7459 | **+0.0011** | 29.53–29.97 |

Worst case 0.0075°, against a 6.55° spread *between* dates. **The right-looking scene
needs no special handling** — the state-vector geometry is agnostic to look side and
reproduces the vendor's own number just as tightly there as anywhere else. R2's 0.006°
result on four dates holds on six.

Geocoded validity over the AOI: 86.7–87.7% on the five left-looking dates, **81.9% on
29 Oct**. The mirrored swath clips a different part of the village. Per-farm consequences
are measured in P1-4, not inferred from this.

## P1-2. ★ The calibration convention, and a correction to Round 2's own post-mortem — `OWN`

Kill criterion, written before the run: under SF², each new scene's |darkest 0.1% − `nesz_peak`|
must land inside the four known scenes' range widened by 1.0 dB.

| date | new | look | `nesz_peak` | SF β⁰ | vs | **SF² β⁰** | **vs** | SF² γ⁰ | vs |
|:--|:--|:--|--:|--:|--:|--:|--:|--:|--:|
| 06 Jun | | left | −26.13 | +1.5 | +27.6 | −25.22 | **+0.91** | −26.72 | −0.59 |
| 19 Jun | | left | −27.76 | +1.1 | +28.9 | −25.14 | **+2.62** | −27.74 | +0.03 |
| 14 Aug | | left | −27.97 | +1.2 | +29.2 | −25.80 | **+2.18** | −28.40 | −0.43 |
| 13 Oct | | left | −27.35 | +3.0 | +30.4 | −25.64 | **+1.71** | −27.76 | −0.41 |
| 29 Oct | **NEW** | **right** | −27.74 | +3.2 | +30.9 | −24.90 | **+2.84** | −27.32 | +0.42 |
| 12 Nov | **NEW** | left | −27.72 | +1.1 | +28.8 | −26.84 | **+0.88** | −29.26 | −1.54 |

**Kill criterion: pass.** Both new scenes land inside the known band on every quantity.
Under SF the darkest content sits **+29.3 dB** above the declared floor on all six; under
SF² it sits **+1.86 dB** above. Six scenes, six different scale factors, six different
declared floors. **The R2 defect is closed and the SF² convention is confirmed on the
full stack.**

**★ The unplanned finding, which corrects our own R2 post-mortem.** R2 reported "0.35 dB
mean absolute error under SF²" and we reproduced that number to three digits — 0.363 dB —
*but only on γ⁰, and only on R2's four dates*. Running the same test on all three
quantities exposes what that number was:

| quantity | mean (dB) | MAE | sd | scenes **below** the declared floor |
|:--|--:|--:|--:|:--|
| **β⁰** | **+1.86** | 1.856 | 0.841 | **0/6 — physically admissible** |
| σ⁰ | −1.08 | 1.080 | 0.692 | 6/6 — impossible |
| γ⁰ | −0.42 | 0.569 | 0.663 | 4/6 — impossible |

The darkest content in a scene sits *at or above* the noise floor, never below it: a
negative residual says the product's own quietest pixels are quieter than the noise the
vendor declares. So **the residual's sign is a harder test than its magnitude**, and γ⁰'s
smaller MAE is bought by sitting under the floor on four of six dates. R2 compared the
wrong quantity and the small number it got was a cancellation — tanθ at 28–35° is −2.8 to
−1.5 dB, which happens to offset β⁰'s +1.9 dB bias.

`nesz_peak` is referenced to **β⁰**, the quantity the product is annotated in
(`radiometry: beta_nought`). That is the only one of the three that is admissible on all
six scenes, and it is a statement about the vendor's annotation that only the data could
settle.

**What it changes.** The SF² verdict is *strengthened*, not weakened — the case for it
never depended on the 0.35 dB, and the residual it should have been reporting is +1.86 dB
with a 0.84 dB scatter, which is a sensible margin between the darkest real content in a
27 km strip and the system floor. What it does change is the **NESZ quality gate of §3.6**:
that gate must be built in β⁰ against `nesz_peak` directly, and a gate written in γ⁰ would
have declared a fifth of the scene to be below the noise floor.

## P1-3. ★ The look-side question answered, and a trap caught in our own code — `OWN`

`src/p1_stable.py`. Three stable classes — WATER (isotropic; no orientation, no dew, no
canopy), BUILT (dihedral, orientation-sensitive, *cannot* respond to soil moisture),
CROP (inside the farm polygons) — all scored only on pixels valid on all six dates, so a
coverage difference cannot masquerade as a radiometric one.

### The trap, because it nearly became a finding

The first version defined the classes on the four Round-2 dates and evaluated all six. It
produced a clean **3.4 dB drop in built-up on both new dates, in both look directions** —
exactly the shape a real discovery has. It is a selection artefact. Picking the brightest
0.5% of pixels on dates A–D selects partly on speckle, so those pixels are *guaranteed* to
come out darker on any date not used to pick them. Same statistical manufacture that made
R2's coherence experiment uninformative.

Rebuilt on four two-date folds with every date scored only out-of-sample, and the artefact
measured rather than assumed:

| class | selection bias (in-sample − out-of-sample) |
|:--|--:|
| built | **+2.59 dB** (per fold +2.45, +3.35, +0.70, +3.88) |
| water | −0.52 dB (water is spatially coherent, so far less speckle-selected) |

**+2.59 of the 3.4 dB was the artefact.** Every number below is out-of-sample.

### Q1 — look side. Answer: no detectable anisotropy. 29 Oct is differenceable.

Per-target dB difference across each pair, one target per connected component. A constant
offset moves every target alike and leaves the *spread* at the noise floor; an orientation
effect moves each target differently and only the spread can see it.

| class | pair | n | mean | **sd** | p05..p95 |
|:--|:--|--:|--:|--:|:--|
| built | **TEST look-reversed** (29 Oct ↔ 12 Nov) | 92 | **−0.05** | **1.81** | −3.3..+2.4 |
| built | CTRL same-look A (19 Jun ↔ 14 Aug) | 77 | +0.38 | 1.92 | −2.2..+3.3 |
| built | CTRL same-look B (13 Oct ↔ 12 Nov) | 92 | +2.20 | 1.90 | −0.4..+6.1 |
| water | **TEST look-reversed** | 231 | **+2.87** | **2.39** | −0.8..+6.6 |
| water | CTRL same-look A | 185 | +0.74 | 1.52 | −1.5..+3.5 |
| water | CTRL same-look B | 231 | +0.46 | 1.21 | −1.6..+2.3 |

Prediction P2 said the reversed pair would spread *more*. **It does not: ratio 0.944
against a 1.5 kill threshold, so the anisotropy hypothesis is dead.** Built-up sits at a
flat 1.8–1.9 dB per-target sd on all three pairs including both same-look controls — that
is the same-look repeat noise, and look reversal adds nothing above it. The mean offset on
the reversed pair is **−0.05 dB**.

The stronger form of the same result: **water, which is isotropic and physically incapable
of an orientation effect, spreads *more* (2.39) than built-up (1.81) on that same pair.**
Nothing in the reversed-pair spread can be attributed to target orientation when the
isotropic class carries more of it than the anisotropic one.

**What it changes.** 29 October enters temporal differences like any other date. No
per-target correction, no restriction to isotropic targets, no scalar offset needed. The
§7.1 worry is closed and the date the forecast leans on is usable.

### The failure that was worth more than the test — water is disqualified as a reference

Prediction P1 said water would differ by <1 dB across every pair. On the reversed pair it
differs by **+2.87 dB**, six times either control. Water is isotropic, so this is not look
side. 29 October is the only date of the six with wind above 10 m/s — **14.1 m/s against
6.7–9.6 everywhere else** — and wind roughening of a smooth water surface at X-band is
standard (`MECH`). The anomaly is ours (`OWN`); the mechanism is textbook.

**Round 2 referenced every date to an in-scene water surface** to cancel Capella's
undeclared absolute calibration. Carried forward unexamined, that would have injected
roughly **+2.9 dB of wind roughening into the 29 October scene** — one of the two dates
the entire forecast leans on, and in the direction that reads as canopy change.
**Water-point referencing must not be reused this round without a wind gate.**

### Q2 — wetness, reframed and confirmed

| date | look | local | soil m. | wind | water | built | crop | crop−built |
|:--|:--|:--|--:|--:|--:|--:|--:|--:|
| 06 Jun | left | 12:55 | 0.151 | 7.1 | −19.95 | −14.02 | −17.80 | −3.79 |
| 19 Jun | left | 07:44 | **0.434** | 6.7 | −20.13 | −11.22 | **−15.16** | −3.94 |
| 14 Aug | left | 08:41 | 0.196 | 8.1 | −20.65 | −10.77 | −17.28 | −6.51 |
| 13 Oct | left | 07:56 | 0.133 | 9.6 | −20.57 | −12.38 | −17.12 | −4.74 |
| 29 Oct | **right** | 01:37 | **0.372** | **14.1** | −19.39 | −14.88 | **−15.58** | **−0.71** |
| 12 Nov | left | 19:22 | 0.220 | 7.6 | −21.04 | −14.78 | −19.06 | −4.28 |

Prediction P3 **held**: crop−built rises **+4.03 dB** from 13 Oct to 29 Oct against
**+0.46 dB** to 12 Nov, tracking soil moisture (0.133 → 0.372 → 0.220) and not time of
day. The two wettest dates are the two brightest cropland dates, by 1.5–3.9 dB, while
built-up — which cannot respond to moisture — shows ρ = −0.14 against soil moisture.

**Dew is not the mechanism**, exactly as Phase 0 found: the two night passes are the
*drier* ones by dew-point depression. **Soil moisture is.** This is now confirmed inside
our own X-band data, having already been established in ERA5-Land and independently in
C-band S1 (ρ = +0.749, p = 0.0004). Three instruments, same answer.

**What it changes.** Any late-season "senescence" read off 29 October is confounded with a
+4 dB wetness term of the same sign and larger size. The 29 Oct ↔ 13 Oct difference is not
interpretable as canopy change without a moisture correction, and this is the single
largest threat to the forecast identified so far.

### Open question carried to Phase 2

Built-up is **not flat**: 4.1 dB out-of-sample range across the season, arc-shaped in
time. A brightness-defined class in a village selects tree-crop and orchard double bounce
alongside settlement, and that *is* seasonal. So built-up is a valid *directional* control
(it cannot respond to moisture) but not an absolute radiometric reference. **Inter-date
referencing is now an open decision** — water is wind-contaminated on 29 Oct, built-up is
seasonally contaminated, and R2's choice cannot simply be inherited.

## P1-4. Per-farm extraction on six dates, coverage, and the NESZ gate that is not needed — `OWN`

`src/p1_features.py`. 966 rows × 111 columns. Buffer ladder: **951 farms at −5 m, 5 at
−2 m, 10 at 0 m, 0 failed** — every plot gets a label, as Coverage's 15 points require.
Effective looks estimated from the data, 5.4–6.8 across dates (the `average`-resampling
multilook, not the vendor's annotated ENL of 1.0).

### Coverage per plot per date, and a bias nobody would find by looking at a village total

| date | look | farms with pixels | missing | area lost |
|:--|:--|--:|--:|--:|
| 06 Jun | left | 937 | 29 | 0.99% |
| 19 Jun | left | 913 | 53 | — |
| 14 Aug | left | 918 | 48 | — |
| 13 Oct | left | 925 | 41 | 1.33% |
| **29 Oct** | **right** | **832** | **134** | **5.01%** |
| 12 Nov | left | 937 | 29 | 0.99% |

**832 / 966 farms have all six dates. 29 have none. 81 are missing 29 October alone.**
Median per-farm coverage is 1.0 on every date — missingness is all-or-nothing per plot, so
this is a swath boundary, not scattered dropout.

**★ The missing set is crop-biased on every single date, chi-square p ≤ 1.4e-3.** On the
five left-looking dates the missing farms are **almost entirely cotton** (29/29, 50/53,
48/48, 41/41, 29/29): the north-west swath edge cuts a block of plots that Round 2 labelled
cotton, and it cuts the same block every time. 29 October's mirrored swath drops a
different and much more mixed region — 80 cotton, 17 rice, 17 groundnut, 14 bajra, 6 maize.

In area the picture is milder, and the honest version is the area one: the 29 permanently
missing farms are **4.43 ha of 447.54, under 1%**, because the cotton plots on that edge are
small (median cotton plot 0.26 ha). 29 October loses **5.01% of village area**, spread
1.9–8.8% by crop. So the aggregation deliverable is not in danger, but **any per-plot
statistic quoted as "the cotton mean" is computed on a systematically incomplete cotton
sample on every date**, and 29 of 455 cotton plots have never been observed by this sensor
at all — Round 2 assigned them a crop from something other than X-band.

### The NESZ quality gate: a clean negative, and one less thing to build

§3.6 listed a NESZ quality gate as a capability gap, on the expectation that dark, smooth,
harvested fields late in the season would put plot means into the noise. Measured in beta0
against each scene's own declared floor (P1-2 established beta0 is the right quantity):

| date | `nesz_peak` | farm margin p05 | median | farms below floor | farms with >half pixels within 6 dB |
|:--|--:|--:|--:|--:|--:|
| 06 Jun | −26.13 | +7.37 | +8.46 | 0 | 5 |
| 19 Jun | −27.76 | +10.70 | +12.55 | 0 | 0 |
| 14 Aug | −27.97 | +9.35 | +10.76 | 0 | 1 |
| 13 Oct | −27.35 | +8.88 | +10.46 | 0 | 0 |
| 29 Oct | −27.74 | +10.77 | +12.77 | 0 | 0 |
| 12 Nov | −27.72 | +7.75 | +8.66 | 0 | 1 |

**Not one farm on any date has a mean below the noise floor, and the worst 5th percentile
on the worst date still clears it by 7.4 dB.** Not a single farm on any date has half its
pixels within 3 dB of the floor. The anticipated late-season problem does not occur — 12
November, the darkest date, still sits 8.66 dB clear. **§3.6's gate is closed by
measurement rather than by construction**, and the margin column is kept as a reportable
QC exhibit rather than as a filter. The margin tracks the wetness finding exactly: the two
wettest dates (19 Jun, 29 Oct) have the largest margins, the two driest the smallest.

## P1-5. ★ The groundnut-lift test — discarded, and the reason is worth more than the test — `OWN`

`src/p1_traj.py`. §4 consequence 4, run as specified with the three cereals as the control
that must show no fortnight signature.

| test | n | mean a | mean b | diff | effect | p |
|:--|--:|--:|--:|--:|--:|--:|
| PRIMARY groundnut vs cereals | 204 / 253 | −3.856 | −3.965 | **+0.109** | 0.82 | **0.416** |
| **CONTROL rice vs maize+bajra** | 69 / 184 | −3.039 | −4.313 | **+1.274** | **5.86** | **0.0000** |
| REFERENCE cotton vs cereals | 375 / 253 | −3.793 | −3.965 | +0.173 | 1.34 | 0.179 |

**The control fired at twelve times the size of the primary effect.** Groundnut differs
from the cereals by 0.109 dB (p = 0.42, indistinguishable); rice differs from maize+bajra
by 1.274 dB at p < 1e-4, when all three are bare soil and should be identical. Per §4's own
instruction — *if that control fails, discard the test and say so* — **the test is
discarded.**

### Why it fired, which is the actual finding

Run the same rice-vs-maize+bajra contrast on every window:

| window | diff | p |
|:--|--:|--:|
| 19 Jun → 14 Aug | −6.624 | 0.0000 |
| 14 Aug → 13 Oct | +1.105 | 0.0000 |
| 13 Oct → 29 Oct | −1.492 | 0.0000 |
| 13 Oct → 12 Nov | −0.648 | 0.0000 |
| 29 Oct → 12 Nov | +1.274 | 0.0000 |

**It fires in all five windows, with the sign flipping.** This is not a fortnight event and
not dew, look side or harvest traffic. It is that **Round 2's crop labels were themselves
derived from these gamma0 trajectories.** Rice was assigned in part *because* of the 19
June spike (+2.73 dB above the other cereals on the one date with 24.4 mm of rain in the
preceding hours). Contrasting label-classes on the features that produced the labels is
circular, and the control was guaranteed to fire before the data was read.

**What it changes, and it is a real constraint on the round.** The §4 lift test is not
runnable with R2's labels — *no* label-versus-label contrast on this backscatter stack is,
by the same argument. Making it runnable requires crop labels **not derived from Capella
X-band**: the S1 C-band predictions, the AlphaEarth embeddings, or Dynamic World /
WorldCereal, all of which are inherited and on disk. Every one of them is a **frozen
witness**, and §5.1 requires naming and freezing a replacement before promoting one. So the
test is not dead — it is **priced**, and the price is one witness. That decision belongs to
Phase 3, not to an EDA script that stumbled into it.

## P1-6. The six-date trajectory: predictions written first, two of them failed — `OWN`

Area-weighted mean gamma0 (dB), because the deliverable aggregates as sum(yield × area):

| date | Rice | Cotton | Maize | Bajra | Groundnut |
|:--|--:|--:|--:|--:|--:|
| 06 Jun | −19.20 | −18.04 | −19.16 | −19.27 | −19.50 |
| 19 Jun | **−13.84** | −16.55 | −17.41 | −18.27 | −17.87 |
| 14 Aug | −20.25 | −17.57 | −18.55 | −20.61 | −20.39 |
| 13 Oct | −19.27 | −17.50 | −20.29 | −20.10 | −18.79 |
| 29 Oct | −18.20 | −17.01 | −18.24 | −17.50 | −17.59 |
| 12 Nov | −21.18 | −20.50 | −21.57 | −21.65 | −21.10 |

**PRED-A — cotton separates further from the cereals as they go bare. FAILED.** The
cotton-minus-cereal gap *shrinks*: +2.24 (14 Aug), +2.39 (13 Oct), +0.97 (29 Oct), +0.97
(12 Nov). Cotton is still standing and still picking on 12 November, yet by then it is
within 1 dB of bare cereal ground. Either X-band HH stops discriminating a picked cotton
canopy from bare soil, or the labels are wrong about which plots are cotton. **This
directly threatens the crop the round is about** and it goes to Phase 2 as a research
question, not as a conclusion.

**PRED-C — the three cereals are indistinguishable after 13 Oct. HELD ON LEVEL, FAILED ON
CHANGE.** On 12 November they span 0.47 dB, which is indistinguishable. Their *changes*
differ significantly, for the circularity reason in P1-5.

**PRED-D — every crop rises on 29 October by a similar amount. HELD ON SIGN, FAILED ON
"SIMILAR", and the failure is coherent.** Every crop rises: cotton +0.49, rice +1.07,
groundnut +1.20, maize +2.05, bajra +2.60. The spread is 2.1 dB and it is **ordered by
canopy cover** — cotton, with the most standing canopy, rises least; bajra and maize, bare
by then, rise most. A closed canopy shields the soil from an X-band view of its moisture.

That is the physically right answer and it is bad news for the correction: **the 29 October
wetness term is not a scene-wide scalar and cannot be removed by one.** It is a
canopy-dependent term, which means the same rain that contaminates the late-season signal
also carries information about canopy closure. Whether that is exploitable or only
hazardous is a Phase 2 question. Every crop then falls 3.0–4.2 dB into 12 November as soil
moisture drops 0.372 → 0.220.

## P1-7. What n=6 buys over n=4 — `OWN`

Six-point trajectories over the 832 fully covered farms, PCA on the dB series:

| PC | 1 | 2 | 3 | 4 | 5 | 6 |
|:--|--:|--:|--:|--:|--:|--:|
| variance | 0.526 | 0.200 | 0.106 | 0.080 | 0.048 | 0.039 |

Two components carry 72.7%, three carry 83.3%. **Six dates span roughly three effective
directions, not six.**

| model | params | df at n=4 | df at n=6 | identifiable at n=6 |
|:--|--:|--:|--:|:--|
| linear | 2 | 2 | 4 | yes |
| quadratic | 3 | 1 | 3 | yes |
| asymmetric Gaussian | 4 | **0** | **2** | **newly yes** |
| single logistic | 4 | **0** | **2** | **newly yes** |
| SAFY, minimum free set | 4 | **0** | **2** | **newly yes** |
| double logistic | 6 | −2 | **0** | **no** |

**The concrete answer: n=6 moves the 4-parameter phenology and light-use-efficiency family
from exactly-determined to over-determined**, which is the difference between a curve that
interpolates and a fit that can be tested. It does *not* reach the 6-parameter double
logistic, which still has zero residual degrees of freedom. And the 4-parameter fits are
weakly identified even so — three effective directions against four parameters — so any
such model must report parameter uncertainty rather than point values.

## P1-8. ★ Cross-implementation check: our chain against Project Orion's — `OWN` + `THEIRS`

`src/p1_xcheck.py`. A common-mode error in our own chain is invisible to every internal
consistency check, because an internal check compares our numbers to our other numbers.
That is how our scale-factor error and another team's geoid error both survived a whole
round. Orion processed the same byte-identical scenes over the same byte-identical polygons
with an independent implementation, so this is the only external instrument we have.

| date | n | Pearson r | Spearman | our dB − theirs | resid sd | resid vs log area | best off-diagonal r |
|:--|--:|--:|--:|--:|--:|--:|--:|
| 06 Jun | 927 | **0.956** | 0.919 | +1.19 | 0.40 | −0.27 | 0.545 |
| 19 Jun | 903 | **0.984** | 0.951 | +0.68 | 0.68 | −0.37 | 0.457 |
| 14 Aug | 904 | **0.921** | 0.918 | +0.95 | 0.88 | −0.27 | 0.666 |
| 13 Oct | 908 | **0.892** | 0.940 | +0.93 | 0.82 | −0.28 | 0.599 |

**The control passes.** Any two SAR extractions over these polygons correlate somewhat,
because farms differ from each other for reasons that persist across dates — so every one
of our dates was also correlated against every one of *theirs*. The diagonal beats the best
off-diagonal by **0.255 at worst** (0.892 vs 0.599 on the weakest date, 0.984 vs 0.457 on
the strongest). The agreement is date-specific and not a village-shape artefact.

### The second control was a hypothesis, and it was falsified — usefully

We predicted that if Orion had used the unsquared SF convention, our values would sit
10log₁₀(SF) below theirs: −26.3 to −28.6 dB, a *different* number on each date. **Measured:
+0.68 to +1.19 dB. The hypothesis is wrong by 27 dB on all four dates. Orion used the
squared convention too.**

That is a **third independent line of support for SF²** — after capella-reader and after
the vendor's own `nesz_peak` — from a source that owes us nothing and was written before we
knew we were wrong. It also upgrades this test: with both chains in the same convention the
comparison is of **absolute level**, and two independent implementations of geocoding,
incidence and extraction agree to about **1 dB**, with a residual scatter of 0.40–0.88 dB.

### The residual structure, which is a real difference and not noise

`resid vs log area` is **−0.27 to −0.37 on all four dates**, same sign every time. On small
plots our values run high relative to theirs. That is traceable: they erode adaptively
(their `erode_m` is ~2.6 m on farm 1), we use a fixed −5 m buffer ladder. Different interior
definitions leave different amounts of edge contamination, and the difference bites hardest
where the plot is smallest. Not an error in either chain, but it is a **quantified
sensitivity of the per-plot number to the interior rule**, and it belongs in the writeup
next to any per-plot claim.

## P1-9. The failure-mode regression suite — `OWN`

`src/tests_regression.py`, **11 passed, 1 skipped, 0 failed.** One assertion per defect that
survived internal consistency checking in a working pipeline. Round 2's suite ported, plus
three classes it never covered.

| check | the defect it catches |
|:--|:--|
| `scale_factor_is_squared` | the R2 calibration defect returning; asserts β⁰(1+0j) = SF² *and* ≠ SF |
| `darkest_content_sits_above_the_declared_noise_floor` | calibration **double**-correction; asserted in β⁰, because in γ⁰ it fires on four of six *correct* scenes |
| `incidence_matches_the_vendors_own_annotation` | the geoid class — wrong ellipsoid, height convention, swapped ECEF axis; <0.02° on all six |
| `farm_join_is_not_off_by_one` | 1-based/0-based join, **with a positive control**: the deliberately shifted join must score ≥0.5 worse in r, or the test cannot detect its own bug |
| `every_farm_survives_to_the_table` | silent row loss; 966 rows, buffer ladder never fails, the 29 no-data farms present and flagged |
| **`a_parameter_that_should_change_the_result_does`** | **the silent no-op.** GDAL takes `METHOD='GCP_TPS'` and ignores it — only `SRC_METHOD` works. Our `average` resampling *is* the multilook, so if the argument were ignored we would ship single-look data with no symptom. Asserts average ≠ nearest **and** that average reduces variance |
| `texture_is_computed_on_unfiltered_data` | a speckle filter inserted upstream, detected without reading code: lag-1 spatial autocorrelation on the fine grid must stay under 0.85 |
| `no_degenerate_parcel_defines_a_grid` | see below |
| `apy_units_are_homogeneous` | the bales-of-lint inhomogeneity, which only makes cotton **too small** and so slips past an upper-bound guard |
| `features_are_not_degenerate` | a constant column, a collapsed distribution, an all-NaN feature — all three pass a schema check |
| `forecast_sanity` | skipped until a forecast exists; the thresholds are fixed **now**, while there is no number to defend |
| `r2_submission_is_still_frozen` | md5 `89b0e4e2aef63ace4989fc0a44590ee5` |

**★ Re-testing R2's degenerate-parcel finding split it in two.** R2 recorded "nine parcels
enclose ~0 ha and their centroids land up to 835 km away". The zero-area parcels are real
and still there — **ten of them, the smallest at 0.0000 m²**. The 835 km displacement was
not: it came from R2's own hand-rolled area-weighted shoelace centroid dividing by a
near-zero area. A library centroid puts all ten inside the village, 2.4 km from centre at
worst. So the check is now two assertions guarding two different things — one that the
degenerate parcels have not been silently cleaned out of the data, one that **our own**
centroid code does not reproduce R2's bug.

---

# Phase 1 gate

## Every finding, tagged by what it changes

| # | finding | what it changes |
|:--|:--|:--|
| P1-1 | Incidence from orbit state vectors agrees with the vendor's annotation to ≤0.0075° on all six, including the right-looking scene | **Nothing needs special handling for look side in the geometry.** A cheap Technical Soundness exhibit |
| P1-2 | SF² confirmed on six scenes; `nesz_peak` is referenced to **β⁰**, and R2's "0.35 dB" was a γ⁰ comparison that sat *below* the floor on 4 of 6 dates | The R2 defect is **closed**. Any NESZ gate must be written in β⁰ — in γ⁰ it would declare a fifth of the scene sub-noise |
| P1-3a | No detectable look-side anisotropy: reversed-pair per-target sd 1.81 dB against a 1.90 dB same-look control; mean offset −0.05 dB | **29 October is usable in temporal differences with no correction.** The §7.1 worry closes |
| P1-3b | Water is +2.87 dB brighter on 29 Oct, six times either control; 14.1 m/s wind, double every other date | **R2's water-point referencing must not be reused without a wind gate.** It would inject +2.9 dB into a load-bearing date |
| P1-3c | Cropland tracks soil moisture where built-up cannot; three instruments (ERA5, C-band S1, our X-band) agree | Late-season "senescence" on 29 Oct is confounded with a **+4 dB wetness term of the same sign and larger size**. Largest identified threat to the forecast |
| P1-3d | Built-up moves 4.1 dB across the season, out-of-sample | Built-up is a **directional control**, not an absolute reference. Inter-date referencing is an **open decision** |
| P1-4a | Coverage crop-biased on every date; the NW swath edge cuts the same cotton block every time; 29 of 455 cotton plots never observed | Area impact under 1% (small plots), so aggregation is safe — but **every per-plot "cotton mean" is on a systematically incomplete sample**, and it must be said |
| P1-4b | 29 Oct's mirrored swath loses 134 farms / **5.01% of village area**, spread 1.9–8.8% across crops | Imputation policy for one date, and a coverage table the writeup needs |
| P1-4c | **No farm on any date has a mean below the noise floor**; worst p05 clears it by 7.4 dB | **§3.6's NESZ quality gate is not needed.** Closed by measurement; the margin stays as a QC exhibit, not a filter |
| P1-5 | The groundnut-lift test is **discarded** — its control fired at 12× the primary effect, and fires in all five windows because R2's labels were derived from these same trajectories | The §4 test is **priced, not dead**: it needs labels not derived from Capella, and every candidate is a frozen witness. A Phase 3 decision |
| P1-6a | **PRED-A failed.** The cotton−cereal gap *shrinks* to +0.97 dB by 12 Nov | X-band HH may stop separating picked cotton from bare soil — or the cotton labels are wrong. Threatens the crop the round is about |
| P1-6b | **PRED-D failed informatively.** The 29 Oct rise is ordered by canopy cover: cotton +0.49, bajra +2.60 | The wetness term is **canopy-dependent and cannot be removed by a scalar** — and therefore also carries canopy information |
| P1-7 | Six dates span ~3 effective directions (2 PCs = 72.7%, 3 = 83.3%) | n=6 makes the **4-parameter** phenology/SAFY family over-determined where n=4 left 0 df. It does **not** reach the 6-parameter double logistic |
| P1-8 | Two independent chains agree to **~1 dB absolute**, r = 0.89–0.98, diagonal beats off-diagonal by ≥0.255. The unsquared-SF hypothesis falsified by 27 dB | **Third independent confirmation of SF².** No common-mode error detected in our chain. Residual depends on plot size (ρ ≈ −0.3) — a quantified sensitivity to the interior rule |
| P1-9 | Regression suite 11/11 green, incl. silent-no-op and degenerate-output classes; R2's "835 km parcels" split into a real data defect and R2's own centroid bug | The suite guards the pipeline; the split means one assertion guards the data and one guards our code |

## Predictions recorded before the plots, and which held

| prediction | outcome |
|:--|:--|
| **P1** water differs <1 dB across every pair | **FAILED** (+2.87 dB on the reversed pair) — and the failure found the wind confound |
| **P2** built-up spreads more on the look-reversed pair (anisotropy) | **FAILED** (ratio 0.944 vs a 1.5 kill threshold) — hypothesis dead, 29 Oct freed |
| **P3** crop−built rises more on 29 Oct than on 12 Nov, tracking soil moisture | **HELD** (+4.03 vs +0.46 dB) |
| **PRED-A** cotton separates further from the cereals as they go bare | **FAILED** — the gap shrinks |
| **PRED-B** groundnut steps across the lift fortnight | **UNTESTABLE** — control fired, test discarded |
| **PRED-C** the three cereals are indistinguishable after 13 Oct | **HELD on level** (0.47 dB), **FAILED on change** (circularity) |
| **PRED-D** every crop rises on 29 Oct by a similar amount | **HELD on sign, FAILED on "similar"** — and the failure is physically coherent |

Three of seven held outright. That ratio is the argument for writing them down first.

## Open questions Phase 2 must answer

1. **Cotton at X-band, late season.** Why does picked, still-standing cotton converge to
   within 1 dB of bare soil by 12 November? Saturation, defoliation, row structure, or a
   label problem. **43% of area, and the only crop where "forecast" is not a synonym for
   "estimate".** (R-B, R-A)
2. **Soil-moisture correction, canopy-dependent.** What does the literature offer for
   removing a wetness term that scales with canopy cover — and is the WCM the tool, now
   that the calibration is fixed and its R2 rejection premise has changed? (R-B)
3. **Inter-date referencing.** Water is wind-contaminated on 29 Oct, built-up is seasonally
   contaminated. What does the literature do when no in-scene invariant is available?
4. **Labels not derived from Capella.** The lift test, and any label-vs-label contrast on
   this stack, needs them. Which inherited asset is worth spending a witness on, and what
   replacement witness gets named and frozen? (R-C, and a Phase 3 decision)
5. **Which model family for 6 irregular dates spanning 3 effective directions.** P1-7 makes
   the 4-parameter family newly identifiable but only weakly. (R-C)
6. **The Gujarat kharif 2025-26 anchor**, still open from Phase 0, now sharpened: cotton
   lint 597 vs the 647 R2 used, on the crop carrying 43% of area. (R-A)

## Gate conditions

| condition | status |
|:--|:--|
| the two new scenes characterised against the four known | **pass** — calibration, incidence, look side, wetness, coverage, all six |
| written EDA document, findings tagged by what they change | **pass** — the table above |
| predictions recorded before plots, with which held | **pass** — 3 of 7 held, all recorded |
| sanity infrastructure built early | **pass** — regression suite 11/11, cross-implementation check passing with its control |
| open questions for the research phase listed | **pass** — six, above |

R2 submission re-verified frozen: `89b0e4e2aef63ace4989fc0a44590ee5` (asserted in the suite).


---

**Phase 2 research document:** `internal/RESEARCH_PHASE2.md` — R-A to R-H, every
claim graded OWN/MECH/THEIRS, with the shortlist, the recommendation, the three tests that
must run before anything is built, and what is still missing.

---

# Phase 3 — build

## P3-1. T1, the SAFY gate: the proxy works where we can see it, and we cannot see where it matters — `OWN`

`src/p3_t1_gai.py`. Within-crop Spearman of each X-band feature against **same-day** Sentinel-2
NDVI. Within crop, not pooled: a pooled correlation would be driven by between-crop differences,
and P1-5 established that R2's labels were themselves derived from these trajectories, so pooled
would be correlating the SAR with itself.

| feature | 13 Oct: Bajra / Cotton / Groundnut / Maize / Rice | 12 Nov: same order |
|:--|:--|:--|
| **γ⁰ dB** | **0.52 / 0.52 / 0.33 / 0.23 / 0.69** | **0.07 / 0.52 / 0.41 / 0.21 / 0.56** |
| CV | 0.04 / −0.03 / −0.19 / −0.12 / 0.20 | −0.12 / 0.04 / −0.17 / −0.13 / 0.01 |
| GLCM resid | 0.32 / 0.03 / 0.23 / 0.27 / 0.59 | 0.00 / 0.15 / 0.02 / −0.04 / 0.17 |
| K-texture | ~0 throughout | ~0 throughout |

**γ⁰ brightness clears ρ = 0.5 in 5 of 10 crop-date cells, and on cotton it clears on both
dates (0.52, 0.52).** Texture and uniformity carry nothing against NDVI. An internal consistency
check falls out for free: **bajra collapses 0.52 → 0.07 between the dates**, which is exactly
what a crop that is off the field by then should do — bare soil ranks nothing.

**The pre-registered criterion ("clears ρ = 0.5 within crop on ≥3 dates") is not satisfiable, and
the reason is availability, not performance.** Only **two** of six Capella dates have a same-day
clear S2 partner. The monsoon eliminated usable optical between 11 May and 13 October (Phase 0
census: July minimum cloud 92.6%), and 29 October's nearest clear scene is 23 October — six days
*before* it and, worse, before the rain that changed the scene by +4 dB. Reported and discounted,
not quietly averaged in.

**★ Verdict: SAFY is dead, and for a better reason than the threshold.** SAFY integrates light use
across the **growing season, June to September** — and that is precisely the window where we have
**zero** optical validation and where R-B B-1 says X-band saturates. **You cannot calibrate a
growth model on a proxy you can only validate after the growth is over.** Recorded as a negative
that cost four hours, exactly as the gate was designed to do.

**And the gate validated the baseline while killing the stretch.** A within-crop ranking against
an independent same-day sensor is precisely what the modifier does, and γ⁰ delivers it at
ρ ≈ 0.5 on cotton — the crop that carries 43% of area.

## P3-2. T2, the WCM re-test: both controls failed, and the WCM is discarded — `OWN`

`src/p3_t2_wcm.py`. Bare reference defined by **Sentinel-2 alone** (lowest NDVI decile on 13 Oct,
same-day, n = 83) so that the control could not be true by construction — the P1-5 mistake, not
repeated. Bare ground rose **+1.94 dB** across the 23–28 October rain (soil moisture 0.133 →
0.372). Fitted two-way transmissivity T² = crop rise / bare rise, bootstrapped:

| crop | n | rise dB | **T²** | 95% CI | NDVI 13 Oct | T² ≤ 1 |
|:--|--:|--:|--:|:--|--:|:--|
| Cotton | 369 | +0.89 | **0.46** | [0.32, 0.60] | 0.369 | yes |
| Rice | 69 | +1.25 | 0.65 | [0.46, 0.82] | 0.225 | yes |
| Groundnut | 203 | +1.36 | 0.70 | [0.57, 0.91] | 0.286 | yes |
| Maize | 48 | +2.21 | 1.14 | [0.92, 1.52] | 0.188 | yes |
| **Bajra** | 132 | +2.98 | **1.53** | **[1.27, 1.90]** | 0.251 | **NO** |

**C1 (physicality) FAILS.** Bajra's transmissivity is 1.53 with a bootstrap CI entirely above 1.
**A canopy cannot amplify the soil signal** — the model forbids T² > 1. Bajra ground rose 3.0 dB
where independently-defined bare ground rose 1.9.

**C2 (ordering) is inconclusive, and that is my design error, stated.** ρ = −0.50 is the right
sign but p = 0.39. With **five crops**, Spearman needs |ρ| ≥ 0.9 to reach p < 0.10 — **the control
was underpowered by construction and should not be counted either way.** C1 alone is decisive and
well-powered.

**Verdict: WCM discarded, per the rule written before the run.** The reason is informative and it
is the *same* reason P1-5 found: **there is a soil/field-position term of comparable size to the
canopy term.** Bajra is not bare-equivalent because bajra fields differ from the reference in
drainage or soil, not in canopy — the identical confound that made rice separate from the other
cereals in every window. Two independent experiments now point at the same unmodelled term.

**What it changes:** the 29 October wetness cannot be removed by a canopy model either. It stays
excluded from the level features and kept as a moisture observation and an ensemble member.

## ★ P3-3. The build, and a correction to the brief's own η² baseline — `OWN`

`src/p3_build.py`. `yield_forecast = anchor(crop) × modifier`, modifier normalised so the
**within-crop area-weighted mean is exactly 1.0** — which makes the crop's area-weighted yield
come out equal to its anchor by construction, so the modifier adds spread without moving the
level, and its contribution is auditable as one number.

**This is a FINAL forecast. The completion factor is not applied to it** — R2 shipped a
yield-to-date and multiplied down; §4 asks for the final yield, so the factor's role inverts and
survives only as a separate `yield_to_date` column, which is what makes D1 possible.

**29 October is excluded from the level features** (P1-3c wetness, P1-6b canopy-dependence, P3-2
WCM failure, Phase 2 A-2 documented cause). Kept as an ensemble member; the two variants differ by
a median of **1.43 health points**.

### ★ The 0.820 baseline does not reproduce

§8 states that in Round 2 the crop label explained **η² = 0.820** of yield variance. Re-measured
directly from **Round 2's own shipped `submission.csv`** with a single estimator:

| column | unweighted η² | area-weighted |
|:--|--:|--:|
| **R2 shipped `yield_estimate_to_date`** | **0.9248** | 0.9305 |
| R3 `yield_forecast_t_ha` | **0.9148** | 0.9157 |
| R3 `yield_to_date_t_ha` | 0.9523 | 0.9541 |

**The 0.820 in the brief is not recoverable from the artefact it describes.** Like the "0.35 dB"
of P1-2, it appears to have been computed on a different quantity. The comparison is therefore
made against R2's *measured* value with the identical estimator: **0.9248 → 0.9148, a 1.0 pp
improvement.** Real, but modest, and it should be reported as modest.

**And η² is the wrong thing to chase on its own.** It is dominated by the anchor spread across
crops — 0.73 t/ha lint cotton against 2.51 t/ha groundnut, a 3.4× range that is **real agronomy,
not a modelling defect**. Driving η² down by widening `YIELD_SPREAD` would be turning a knob to
move a metric. The honest measure of the SAR's contribution is whether the **within-crop ranking
is real**, and T1 answers that independently: ρ ≈ 0.5 against same-day S2 NDVI on cotton, on both
testable dates.

### Deliverable

| crop | plots | area ha | share | anchor t/ha | forecast t/ha | production t | **epistemic object** |
|:--|--:|--:|--:|--:|--:|--:|:--|
| Cotton | 455 | 193.4 | 43.2% | 0.730 | 0.730 | 141.2 | **FORECAST** |
| Groundnut | 221 | 137.7 | 30.8% | 2.514 | 2.514 | 346.1 | **NEAR-COMPLETE MEASUREMENT** |
| Rice | 86 | 47.4 | 10.6% | 1.690 | 1.690 | 80.2 | retrospective reconstruction |
| Bajra | 149 | 42.3 | 9.5% | 1.910 | 1.910 | 80.8 | retrospective reconstruction |
| Maize | 55 | 26.7 | 6.0% | 2.312 | 2.312 | 61.8 | retrospective reconstruction |
| **ALL** | 966 | 447.5 | 100% | — | **1.587** | **710.0** | three different objects |

**46 zones** on a 500 m grid carry a **39.7-point** health spread behind the single village row
(Orion found 32). Ours carries an uncertainty column; neither Orion's nor 8bit's does.

Dynamic World census reproduces R2's exactly once `dw_mode` is read correctly — it is the zonal
*mean* of the mode band, a float, not a label. 252 non-crop parcels, **16.58% of area**; 35 also
flagged by our own low-index rule. **Flag, never filter** — they still enter the crop shares and
the village aggregate, which is the actual defect being disclosed.

## ★ P3-4. The defensibility battery: 19/19, and D4 is the one that matters — `OWN`

`src/p3_checks.py`. Every threshold fixed in `PLAN_R3.md` before the run.

| check | result |
|:--|:--|
| **D1** forecast vs R2 yield-to-date | **all 6 pass.** Rice 1.04, Maize 1.00, **Cotton 1.84**, Groundnut 1.30, Bajra 0.71, village **1.19** (710.0 t vs 594.9 t) |
| **D2** cross-team band | **pass**, 710.0 t inside 578–1268 t |
| **D3** published yield ranges | **all 5 pass**, cotton 0.730 t/ha **lint** |
| **D4** non-circular label test | **pass — see below** |
| **D5** cross-crop ordering | **pass**, cotton lowest yield-to-date at 0.20 t/ha, the only crop still picking |
| **D8** degenerate output | **all 5 pass**, 886 distinct yields, health sd 18.9 pts |

**D1 is the check no other team can run**, and it behaves. The three cereals reproduce R2 within
4% — they must, their season closed before R2's last date. Cotton rises **1.84×** because the
forecast is final and R2's was to-date. **Bajra falls to 0.71× and that is the anchor correction
showing up exactly where it should** (2.714 → 1.910 t/ha), on the crop ADD-3 independently
identified as our weakest share.

### ★ D4 — our labels survive the test that dissolved Orion's

P1-5 proved every naive label test on this stack is circular. Orion's residual method is the fix:
regress the independent witness on the SAR ranking axis that produced the labels (PC1 of the
six-date γ⁰ series), then run the group test on the **residual**.

| | explains raw NDVI | explains the residual | **survives** |
|:--|--:|--:|--:|
| **our labels** | **20.2%** (p = 5.7e-36) | **11.2%** (p = 1.1e-21) | **55%** |
| Orion's own Tier-2 labels (their figure) | 19% | 0.2% | **1%** |

**On the one non-circular test that exists — their design — our crop labels carry more than half
their information beyond the dominant SAR axis, where theirs carried one fiftieth.** This is the
strongest answer available to the team that raised the label objection, and it is answered on
their instrument, not ours.

*Caveat, stated: our residual test is run by us on our labels; their 19%/0.2% is their reported
figure on their labels and their implementation. The designs match; the implementations were not
cross-checked.*

## P3-5. Baseline gate reached — one day early

**Regression suite 12/12 (`forecast_sanity` now runs rather than skipping), defensibility 19/19,
submission valid at 966 rows, R2 still `89b0e4e2aef63ace4989fc0a44590ee5`.**

The plan's 31 August end-of-day gate — *a complete, valid, defensible submission exists on disk* —
is met on 30 August. Everything remaining is improvement on something already shippable.

## P3-6. Uncertainty, and the finding that the zero IS the answer — `OWN`

`src/p3_uncertainty.py`. The first run computed an eight-member ensemble and returned a village
production spread of **exactly 0.0 t**. Not a bug. The modifier is normalised to area-weighted
mean 1.0 within crop, so each crop's area-weighted yield equals its anchor by construction and
**the village total is anchor × area. The SAR cannot move it.**

That redirected the whole analysis. The honest decomposition:

| term | scope | value |
|:--|:--|--:|
| sampling (calibrated 3.4%, split-half, no tuning) | per farm | 5.8 health pts |
| ensemble, 8 members, leave-one-date-out | per farm | 0.028 t/ha (2.2%) |
| **ensemble** | **village** | **0.0 t — by construction** |
| crop label, MC over the shipped posterior | village | 41.6 t |
| **anchor**, MC over independent published sources | village | **158.2 t** |
| both | village | 170.0 t → **[628, 798] t** |

**The dominant village-level uncertainty is the anchor, at nearly 4× the label term and
infinitely more than the imagery.** This is the published limitation of anchor-plus-modifier
stated as a measurement rather than a caveat: at village level the SAR contributes nothing, at
plot level it contributes all the spread (validated ρ ≈ 0.5 vs same-day S2), at zone level all
39.7 points of between-zone variation.

**Conformal (arXiv 2509.10321) is reported as arithmetic, not as a number.** The guarantee is
1 − α − β and β is our label error rate, unbounded from anything we hold (κ = 0.060 bounds
disagreement, not error). A nominal 90% is 60% at β = 0.30. Published as a curve.

Moran's I on the yield residual **0.083, z = 7.4** — plots are not independent, so any
sub-village interval under an independence assumption is too narrow.

## P3-7. Spatial hold-out: 7/9, and the two failures are real — `OWN`

`src/p3_validate.py`. The pipeline fits almost nothing to a target — the health weights come
from redundancy alone (`w_k ~ 1/Σ|ρ|`, a function of the feature matrix, blind to every witness),
the anchors are published, the spread is a stated prior. That is a claim, so it was tested.

| test | result |
|:--|:--|
| **V1** weight stability, west vs east | **pass** — largest drift 0.032 |
| **V2** rank transfer across halves | **pass** — ρ 0.9997 and 0.9967 |
| **V3** witness relationship in both halves | **pass** — all four pairs agree in sign and size |
| **V4** GLCM npix regression, out of sample | **FAIL ×2** — residual vs log(npix) ρ −0.27, −0.40 |

**V4 is a genuine failure and is reported as one.** The GLCM entropy residual does not
generalise across the spatial split. **It does not enter the shipped health index** — verified by
inspection of `health_parts`, which uses only `g0_db_20250814`, `g0_db_20250619`, `cv_20250814`,
the season integral and the late-season slope. So the failure does not touch the deliverable, but
it is recorded rather than dropped, and it disqualifies GLCM texture from any future promotion
without a rebuilt correction.

## P3-8. The figures, and what looking at them caught — `OWN`

Four figures rendered, opened and examined. Round 2's lesson (four rounds of rework) is that the
figure is the check on the prose. It caught four defects, one substantive:

1. **★ F3's title read "cereals flat … bajra down" — but bajra IS a cereal.** A self-contradicting
   caption on a correct figure. Exactly the class Round 2 warned no metric can catch, because
   every number passes identically either way. Retitled to name rice and maize explicitly.
2. **F1's left panel read "groundnut dominates Sokhda"** — most of the gap is the lint convention.
   Added: cotton leads on *area*, not tonnage.
3. **F4's threshold line implied ρ killed SAFY.** It did not — availability did. Annotated.
4. **F3 coloured a ×1.00 ratio as a decrease**; null results now render neutral.

Also fixed: an arrow tip obscuring the "0.0" it pointed at, and axis labels reading `1013` /
`1112` as counts rather than dates.

## P3-9. Deliverables complete

`WRITEUP.md`, `PRESENTATION.md` (10 slides + anticipated questions), `results/submission.csv`
(966 rows), village and 46-zone summaries, per-farm uncertainty, four figures.

**Final state: regression suite 12/12, defensibility battery 19/19, spatial hold-out 7/9 with
both failures on a feature outside the shipped path, R2 submission still
`89b0e4e2aef63ace4989fc0a44590ee5`.**

The plan's 31 August baseline gate and its 1 September finish are both met on **30 August**.

---

## P3-10 — the anchor audit, and two things it turned up

**Motivation.** With the ensemble measured at 0.0 t, every remaining lever on the village total
is the anchor or the crop areas. Effort was redirected there rather than at more SAR work, which
the decomposition had already shown cannot move the number.

**a) We had padded our own uncertainty.** `ANCHOR_SOURCES` carried, for Rice and Maize,
`[base, base*0.85, base*1.15]` — an invented +/-15% bracket, sitting directly beneath a comment
stating that every entry was "a real number from a real source; the spread between them is the
uncertainty, rather than a percentage we invented". Two of five crops, 26% of village area.

Replaced with the Gujarat State First Advance Estimates for kharif 2024-25 (Directorate of
Agriculture Gujarat, released 21 Sep 2024): rice 2537.97, maize 2022.15, bajra 1786.66,
groundnut 3026.31, cotton 634.83 kg/ha. STATE not district, so by the rule already applied to
groundnut these are carried as SPREAD and not adopted as anchors. No anchor value changed; the
deliverable is byte-identical.

  anchor term   158.2 -> 187.4 t        label+anchor   170.0 -> 184.8 t
  interval      [628, 798] -> [659, 844] t

The interval got WIDER. Reality exceeded the padding: rice's independent value sits 50% above the
district base. We had been understating uncertainty on a quarter of the village.

  ** side benefit: bajra at 1786.66 is a FOURTH independent estimator near 1.9, corroborating the
     post-R2 correction to 1910 and further isolating the 2714 cell we rejected.

**b) The district series is unreachable, not merely stale.** data.gov.in resource
66e33662-6f0b-4bd9-8771-5a33f8ff6cdd (the id the kickoff brief cites) returns **HTTP 200 carrying
{"status":"error","message":"Meta not found"}** — a 200 that is not a success, the same shape as
the PMFBY SPA shell. `/catalog` returns 404. The retry loop does not fire on either, because one
is a 200 and the other is a hard 404. Recorded in the anchor provenance as SEARCHED AND FAILED,
which is a materially different claim from "not found".

National 2025-26 FAE was rejected as an adjustment source: it publishes PRODUCTION only
(rice 124.504 mt, maize 28.303 mt) and area moved in both crops, so a production ratio cannot be
read as a yield ratio. adj_2025_26 held at 1.00 for both, now with a documented reason.

**c) The label term is a BIAS, and our first diagnosis of it was wrong.** The label-only interval
[721.2, 761.9] does not contain the point estimate 710.0.

  hypothesis  the modifier is normalised within crop; resampling labels while holding the
              shipped modifier fixed breaks that normalisation -> artefact.
  test        renormalise inside the MC: m_b = modifier(hi, sampled_labels, area).
  result      REJECTED. The gap grew (712.1 -> 721.2). Control held: the anchor-only interval
              was unchanged at 187.4 t, confirming the patch touched only the label path.
              The renormalisation is KEPT anyway, being the correct MC regardless.

  actual cause  argmax over a diffuse posterior (69.4% of farms have no class above p=0.5).
                Argmax concentrates area into the classes that win most often; the posterior
                spreads it into higher-anchor crops.

                  Cotton -35.1 ha (0.730 t/ha, lowest)   Maize +36.8 ha (2.312)
                  Groundnut -36.5 ha                     Bajra +22.5 ha   Rice +12.3 ha

                  argmax 710.0 t   posterior-mean 741.5 t   bias +31.5 t (+4.4%), LOW

Reported, not corrected. The deliverable needs one crop label per farm, and a village total
disagreeing with the sum of its own farms would be a worse defect than a stated bias.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze intact at
89b0e4e2aef63ace4989fc0a44590ee5, submission.csv unchanged. Figures regenerated; F2 propagated
the new widths. The bias was deliberately NOT added to F2: that axis is interval width, and a
bias is not a width.

---

## P3-11 — both uncertainty terms were too narrow, each caught by an EXTERNAL control

P3-10 widened the anchor once, using published values. This entry is the follow-up question:
**how would we know if the width were still wrong?** Counting published sources measures our
literature search, not the world, so both terms were tested against something outside our model.
Both failed.

**a) THE LABEL TERM, understated ~6x.** Our MC samples OUR OWN posterior, so a confidently-wrong
classifier buys a confidently-narrow interval -- it measures our confidence, not our accuracy.
Five other teams labelled these same 966 farms in R2 (inherited/consensus.csv). Re-running the
village total under each label set, our anchors and modifier held fixed:

    consensus (majority) 650.3    Megalodon 695.0    CodingBits 700.0    8bit 703.7
    OURS 710.0            DeepThinkers 722.8         Orion 886.8

    external range 236.5 t   vs   40.7 t from our own posterior

  CONTROL: crop_GDHTM is our own R2 labelling and must reproduce the shipped 710.0 t through
  this independent code path. It does, to <0.05 t. control_gdhtm_reproduces_shipped=True.

  Reassuring half: 4 of 5 other teams land within +/-2% of us. We are not the outlier; Orion is.

**b) THE ANCHOR TERM, still too narrow after P3-10 widened it.** Tested against what a Vadodara
kharif yield actually does year to year (district APY 1997-2012, inherited/anchors.csv, 15-16
kharif seasons per crop):

    crop        our source CV   district interannual CV
    Cotton         0.180            0.397    TOO NARROW
    Rice           0.284            0.332    comparable
    Maize          0.095            0.243    TOO NARROW
    Bajra          0.243            0.283    comparable
    Groundnut      0.152            0.491    TOO NARROW  <- 49% of village production

Adopted the district's measured 1-sd envelope for the three that failed. This IS a percentage on
a base -- the practice P3-10 criticised -- with the distinction that the percentage is measured
from this district's own history rather than chosen to look reasonable. Rice and Bajra untouched.
The envelope is unconditional and includes catastrophic seasons; kept wide deliberately, since
our 29 October scene sits inside a state-declared disaster.

    anchor 187.4 -> 385.2 t    both 184.8 -> 320.0 t    interval [598, 918] t

**c) WHY "both" IS NARROWER THAN "anchor alone"** (320.0 < 385.2), which looks impossible.
Real interaction, not a bug: each draw takes ONE anchor per crop and applies it to all of that
crop's area, so a concentrated allocation is more exposed to any single draw. Our argmax labels
are a concentrated portfolio -- Herfindahl 0.305 vs 0.235 for the posterior -- so resampling
labels diversifies the anchor exposure and partially cancels it. Concentration in the crop map
amplifies anchor risk.

**d) FIGURE DEFECT, found by looking (twice).** F2's "crop label" bar showed only the 41 t
internal number, making the figure contradict the slide it illustrates -- a reader would take
away the understated term. Added the external bar. The explanatory annotation then rendered
BEHIND the bars, unreadable; fixed with zorder + a background box. The figure remains the check
on the prose.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze 89b0e4e2aef63ace4989fc0a44590ee5,
submission.csv unchanged at 8304407ed23bc67168fb26fca21a03d1, 966 rows. No anchor value and no
shipped number moved: this entry changed only what we claim to know about them.

---

## P3-12 — consistency sweep, and closing the last self-declared open question

**a) Stale-number sweep.** The headline anchor term moved three times in one session
(158.2 -> 187.4 -> 385.2) across two long documents. Swept every numeric claim in WRITEUP.md and
PRESENTATION.md against results/tables/. Found and fixed:

  - WRITEUP line 373 still presented 187.4 t as the final anchor width. Rewritten to state the
    two-stage widening explicitly, since both stages are part of the argument.
  - p3_uncertainty.csv's note for the anchor row still read "MC over independent published
    anchors per crop", which no longer describes it: three crops now carry the district's
    interannual envelope. Note corrected.
  - ** an overstatement of our own: both documents claimed 4 of 5 other teams land within
    "+/-2%" of our 710 t. Megalodon is 695.0 t = -2.1%, marginally outside. Corrected to 2.2%
    (695.0-722.8 t) in both places. Small, but it is the exact class of error that costs
    credibility when a judge checks it.

Verified against p3_village_summary.csv: 710.028 t / 447.540 ha / 1.5865 t/ha; area shares
43.22 / 30.76 / 26.02; cotton 0.2044 of 0.7301 in hand = 72% still on the plant; groundnut
346.119 t = 48.7% of production, supporting the "49% of village production" claim.

**b) The bajra share, costed at last.** Slide 10 has asserted since Round 2 that our bajra share
is our most likely map error (we assign 9.45%, Gujarat's 2025 sowing profile gives 2.9%) without
ever saying what it costs. Reallocated the least bajra-confident plots to their next-best
posterior class until the share reaches the profile:

    bajra share 9.45% -> 2.81%     village 710.0 -> 723.7 t    (+13.7 t, +1.9%)
    absorbed by: Groundnut 60 plots, Rice 10, Maize 6, Cotton 3

**Our worst-suspected share error is worth under 2% of the total.** The reason is structural:
bajra's anchor (1.910 t/ha) sits close to the area-weighted village mean (1.587), so moving its
area barely moves production. Worth knowing before being asked, and it is a smaller term than
either the label (236.5 t external) or the anchor (385.2 t).

**Verification.** regression 12/12, defensibility 19/19, R2 freeze
89b0e4e2aef63ace4989fc0a44590ee5, submission 8304407ed23bc67168fb26fca21a03d1, 966 rows.

---

## P3-13 — ★ our headline claim was wrong, and it was wrong AGAINST us

For two rounds the deck and the writeup have led with: **"at village level the SAR contributes
nothing to the total."** Auditing the sentence rather than the arithmetic shows it is false.

The arithmetic is fine. The modifier is normalised to area-weighted mean 1.0 within crop, so the
MODIFIER cannot move the village total, and the eight-member ensemble measuring 0.0 t is correct.
The error is the inference from "the modifier cannot move it" to "the SAR cannot move it".

    village total = SUM_c  anchor_c  x  area_c
                           --------     --------
                           published    a SAR PRODUCT
                           statistic

The anchors are government yield statistics we did not produce. The AREAS are set entirely by the
crop map -- and the crop map is built from these same Capella trajectories. That is not a
convenient rereading: it is the documented fact behind P1-5 (the groundnut-lift control fired at
12x because R2's labels came from these trajectories) and behind the whole circularity argument
in WRITEUP 3.1. Verified again here: WRITEUP 6.3 describes "the SAR ranking axis that produced
the labels", with S2 NDVI held as an independent witness that was never fitted.

**So the SAR supplies one of the two factors in the product**, and P3-11 already measured what
that factor is worth: 236.5 t of village-total spread, externally, from five other teams'
labellings of the same farms. We had been publishing 0.0 t.

Corrected framing -- three channels, one zero:

    crop map    236.5 t of the village total      (SAR)
    plot        all within-crop spread, rho ~ 0.5 vs an independent same-day sensor   (SAR)
    zone        39.7 health points                (SAR)
    modifier    0.0 t  -- zero BY CONSTRUCTION, because we normalised it, not by failure

The true limitation is narrower than we were stating: **the SAR does not set the LEVEL.** A
published statistic does, and it is the largest thing we are unsure about at 385.2 t.

Reported prominently because the correction runs in our favour. A team that only ever finds
errors flattering to itself is not auditing, it is marketing -- and this one had been costing us
the strongest honest claim we have.

Reconciled everywhere so nothing in the repo contradicts: PRESENTATION slide 8 (headline, table
row, three-channel paragraph, and the closing Say line, which had said "it isn't the radar"),
WRITEUP 7 "the zero is the finding" (which also still carried a stale 158 t), p3_figures F2 title
and bar label, p3_uncertainty module docstring and the ensemble log note.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze
89b0e4e2aef63ace4989fc0a44590ee5, submission 8304407ed23bc67168fb26fca21a03d1, 966 rows.
Figure re-rendered and inspected.

---

## P3-14 — the two dead methods, autopsied; and a new one that killed our own slide 9

### a) WCM: it was never capable of contributing (src/p3_salvage.py)

The published kill was physical (bajra T^2 = 1.53, a canopy cannot amplify). That leaves open
"fix it and retry". The stronger result closes that door:

    rho(rise_db, T^2) = +1.000, EXACTLY, across all five crops.

T^2 is a perfectly monotone relabelling of the raw two-date difference. With one difference per
crop and several free parameters the WCM is UNIDENTIFIABLE -- one degree of freedom of data, so
T^2 is pinned by rise_db alone. Even had the physics passed it would have added nothing.
rho(NDVI, T^2) and rho(NDVI, rise_db) are both -0.500, identical to machine precision.

  General lesson, now in the writeup: a model with more free parameters than observations per
  unit returns a monotone relabelling of its input and looks physical while adding nothing. The
  tell is a rank correlation of 1.000 against the raw quantity. Cheap to compute, worth doing
  before believing any retrieval.

### b) SAFY: the proxy is real; the kill was availability, now with a rate

gamma0 vs same-day S2 NDVI within crop REPLICATES: cotton 0.518 (13 Oct) and 0.522 (12 Nov),
two dates 30 days apart in very different crop states, agreeing to 0.004. Rice 0.690 / 0.561.

Temporal decay measured on 29 Oct, whose nearest optical partner is 6 days away:

    Bajra -33%   Cotton -36%   Groundnut -41%   Rice -37%    (Maize +1%, but never had signal)
    same-day median rho 0.464  ->  6-day-gap median rho 0.218

**The canopy signal loses about a third of its strength in six days**, and there is no same-day
optical anywhere in the Jun-Sep window SAFY integrates over. Correctly killed, now measured.
SALVAGED: the decay rate is a keeper -- it sets the revisit cadence any future X-band GAI
assimilation here would need, and justifies weighting dates rather than interpolating.

### c) ★ Dawid-Skene label fusion, and the control that voided it (src/p3_dawidskene.py)

Since 4.1 established the SAR decides only ORDERING and CLASSIFICATION, and the ordering cannot
move the village total, the crop map is the only place a better method changes the answer. Six
teams labelled these same 966 farms. Dawid & Skene (1979) EM recovers latent labels plus a
per-annotator confusion matrix with no ground truth -- strictly more than majority vote, which
assumes equal reliability and independent errors, both false here.

It ran clean and beat everything on D4's referee:

    ours 11.22% residual / 55.4% survives     majority vote 8.25% / 59.2%
    Dawid-Skene 26.27% / 91.0%                (DS differs from ours on 509 of 966 farms)

Three controls all passed: not degenerate (all 5 classes, more balanced than ours); OUT-OF-SAMPLE
on the 12 Nov witness the margin WIDENS (ours 5.08%, DS 54.90%); shuffled DS labels with
identical class proportions score 0.46% against DS's 26.27%.

**Then the provenance control voided the comparison.** The D4 referee removes the SAR axis. It
does not remove an OPTICAL axis. Its non-circularity is a property of OUR pipeline (our labels
are SAR-derived), not of the test. Per-team residual eta2:

    DeepThinkers 21.9%   8bit 26.0%   CodingBits 20.6%    <- optical-informed
    Megalodon 16.1%      Orion 11.6%  OURS 11.2%          <- the two SAR-like sets

Dawid-Skene fuses all six and inherits optical information our labels never saw. Its win is not
evidence of being more correct; the referee cannot separate "better" from "saw another sensor".
NOT ADOPTED -- and it should not be, on four grounds: unverifiable with any tool we hold, it
would change 509 of 966 farms three days out, it makes our map depend on competitors' work, and
it destroys the SAR-only provenance that is our actual differentiator.

### d) ★★ The same control killed our own slide 9, which was a claim in our favour

Slide 9 read: "our labels survive the test that dissolved a competitor's -- ours 55%, their
Tier-2 1%." Applied consistently to all six teams' SHIPPED labels:

    DeepThinkers 98.3%   8bit 96.8%   CodingBits 91.6%   Megalodon 90.1%   Orion 72.4%
    OURS 55.4%   <- LAST OF SIX

The old comparison set our number, computed by us, against Orion's self-reported figure for a
DIFFERENT label set (their Tier-2, not the crop_Orion they shipped, which scores 72.4%). Not
like-for-like.

But the metric does not measure label quality -- it measures information beyond the dominant SAR
axis, which optical labels acquire for free. So the ranking is a PROVENANCE DETECTOR, and read
correctly it says our crop map is the least contaminated by anything that is not radar. Slide 9
and WRITEUP 6.3 rewritten to the corrected reading. This is the second headline claim corrected
in two days and the first one that was purely self-flattering.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze unchanged, submission
unchanged -- nothing here touched the deliverable.

---

## P3-15 — Sentinel-1 fusion: built, tested, REJECTED by its control; and what it exposed

### a) The GEE path died; Planetary Computer replaced it with no credentials

ee.Initialize() failed on a stale project ('SSIP' not found). The cached refresh token then
failed a manual refresh (401) even with a matching client_id/secret supplied by the user, so the
token was minted by a different client and is dead -- interactive browser consent would be
needed. Abandoned after three attempts per the no-rabbit-hole rule.

Microsoft Planetary Computer serves sentinel-1-rtc (gamma0, terrain corrected, 10 m) through a
STAC API with an ANONYMOUS SAS token endpoint. Full chain verified: search -> sign -> windowed
COG read over Sokhda. No account, no key. GEE is not needed.

### b) The asset (src/p3_s1_season.py)

    Capella X-band    6 dates,  3 in Jun-Sep
    Sentinel-1 C-band 16 dates, 9 in Jun-Sep, 12-day cadence, cloud-free

★ ALL 16 SCENES ARE ONE TRACK (descending, relative orbit 34). No look-side or incidence mixing;
the confound Phase 1 spent effort excluding from the Capella stack does not arise. Asserted in
code -- the run aborts if a second track ever appears. 966 farms x 16 dates x {VV,VH}, zonal
means computed in POWER then converted (averaging dB biases the mean low), 98.8% coverage.

Provenance: Sentinel-1 is SAR, so X+C fusion preserves the P3-14d claim that our products are
the least optically-contaminated of the six teams. An optical index would score better on an
optical witness and would mean nothing.

### c) S1 carries real incremental information -- partial rho after removing Capella gamma0

    cotton    (43% area)  +0.346  p=1.1e-12   ADDS
    groundnut (31%)       +0.362  p=3.2e-08   ADDS
    rice      (11%)       +0.304  p=4.5e-03   marginal under Bonferroni

85% of village area. The growth window genuinely holds canopy information our own sensor did
not observe.

### d) ★ AND THE FUSED INDEX STILL FAILED ITS CONTROL. NOT ADOPTED.

Fused health index, weights derived by the SAME blind redundancy rule, referee = within-crop rho
vs same-day S2, area-weighted:

    13 Oct witness            shipped -0.0217   fused +0.1400   delta +0.1617
    12 Nov witness (CONTROL)  shipped +0.0900   fused +0.0682   delta -0.0218

Improves on one date, degrades on the other. "Carries extra information about a witness" is not
"improves the forecast", and a change that only helps on the date you looked at is the oldest
mistake there is. NOT ADOPTED.

  Confirmed en route: the village total is INVARIANT under fusion (710.0 t both ways, difference
  0.000 t) because the modifier is normalised within crop. Fusion could only ever have moved the
  distribution -- 877 of 966 plot yields would have changed, the total none.

### e) A sign error I thought I had found, refuted by the control

senesce correlates NEGATIVELY with 13 Oct NDVI on all five crops (-0.129 to -0.575), the largest
witness correlation of any family, and enters the index with a POSITIVE weight of 0.211 while
every other family is explicitly oriented. That reads exactly like a sign bug.

    flip senesce:  13 Oct -0.0217 -> +0.2926      12 Nov CONTROL +0.0900 -> +0.0166

The control says no. The explanation is structural: senesce is the slope BETWEEN 13 Oct and
12 Nov, so it shares a term with the 13 Oct witness -- a high 13 Oct gamma0 mechanically makes
the slope more negative. The negative correlation is an artefact of the witness date being the
slope's own start point, not a sign error. Shipped orientation is correct and stays.

### f) ★ What did survive: a misattributed validation claim, now corrected

WRITEUP 7 and slide 8 both said the plot level is "validated at rho ~ 0.5 against an independent
same-day sensor". That rho ~ 0.5 is the same-day gamma0 FEATURE (cotton 0.518, rice 0.690). It is
NOT the composite health index that actually drives the deliverable, which sits at rho ~ 0.09
area-weighted against the 12 Nov witness. We validated an input and reported it as validation of
the product. Both documents corrected; no test in the repo had ever put the shipped index against
the witness, which is why this survived two rounds.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze unchanged, submission
unchanged -- nothing in P3-15 touched the deliverable.

---

## P3-16 — ★ a nine-year radar climatology: the first time the SAR says anything about the LEVEL

### The idea, and why it is not blocked by the thing that blocks everything else

4.1 concluded the SAR decides only ORDERING and CLASSIFICATION, because absolute yield
calibration needs a label. That holds WITHIN a season. Across seasons it does not:

    absolute level  needs a LABEL   -- we have none
    RELATIVE level  needs a HISTORY -- Sentinel-1 has nine years over this village

The gap it lands in is specific and self-declared: four of five crops carry adj_2025_26 = 1.00
with the reason "no kharif 2025-26 anchor found ... held at base and flagged". That 1.00 is an
ASSUMPTION that 2025 was an ordinary year at Sokhda. Nothing published at district or state
level can test it for this village. Nine years of radar can.

### Why it is newly possible, and the geometry check

Every Sentinel-1 scene over Sokhda in Jun-Sep, in every year 2016-2025, is on ONE track
(descending, relative orbit 34). Nine years, no look-side or incidence mixing -- the confound
that normally dominates multi-year SAR comparison is simply absent. Checked, not assumed: the
Oct-Nov window is NOT single-track (2019 carries ascending 71) and those scenes are dropped.

### ★ The control fired, and it reversed the naive reading

Every year measured twice over the same scenes: FARM pixels (signal) and NON-FARM pixels in the
same AOI (control). Growing season, 2025 vs the 2017-2024 climatology:

    VH farm     (raw signal)   z = +1.20    <- naive read: "bright year, crops did well"
    VH nonfarm  (CONTROL)      z = +1.39    <- the LANDSCAPE moved MORE
    VH farm - nonfarm          z = -0.16    <- the only quantity that can be about the crop
    VV farm - nonfarm          z = -0.84

The raw +1.20 is void: the whole scene brightened, farms included, and none of it is
crop-specific. Had we reported the raw farm anomaly we would have claimed a good season from
what is landscape-wide soil moisture.

### The result, which is a POSITIVE finding and not a null

    z(farm - nonfarm) = -0.16 over Jun-Sep.

**The 2025 growing season at Sokhda was statistically ordinary.** So adj_2025_26 = 1.00, which
we had held for four crops as an admitted assumption, is now supported by a village-specific
measurement. An assumption became a measurement; that is the whole value.

### ★★ And the late-season window separates cleanly from it

Rerun over 01 Oct - 15 Nov, track 34 only:

    VH farm     z = +0.48        VH nonfarm (CONTROL) z = +1.01
    VH farm - nonfarm  z = -1.62      (2025 -0.42 dB vs climatology -0.23 +/- 0.12)

The landscape brightened on wet soil (+1.01) and the farms did NOT keep up (+0.48), so relative
to their own normal relationship with the surroundings the parcels went DARKER. Growing season
ordinary, late season anomalous -- independent nine-year support for the October damage
narrative we had until now sourced from ERA5 and a news report, and it corroborates the
epistemic-object split: the crop grew normally and was hit after groundnut matured but while
cotton still stood.

  HONEST LIMITS, stated because -1.62 is not decisive: n = 8 climatology years, only 2-4 scenes
  per year in that window against 7-10 in the growing season, VH backscatter is a weak proxy
  for yield, and 2019 sits at -0.41 against 2025's -0.42 -- so 2025 is the most negative of nine
  years but only marginally beyond 2019. SUGGESTIVE, not established. Not used to adjust any
  anchor; reported as corroboration.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze unchanged, submission
unchanged. Nothing here touched the deliverable.

---

## P3-17 — docs synced to P3-14/15/16, and a fifth approach that failed its controls

### a) Documentation sync

Nothing from P3-14/15/16 had reached the deliverable documents. Added:

  WRITEUP  new section 9 "Four approaches we built after the forecast was frozen" covering the
           WCM autopsy (9.1), the SAFY decay rate (9.2), Dawid-Skene and the provenance control
           (9.3), X+C fusion and its failed control (9.4), and the nine-year climatology (9.5).
           Old section 9 renumbered to 10; section 8 kept its number deliberately so the three
           existing cross-references to it stayed valid. 3.2's heading now points to 9.1.
  DECK     slide 5 gains the climatology as independent corroboration of the October event and
           of adj_2025_26 = 1.00; slide 6's kill table gains Dawid-Skene and X+C fusion plus the
           WCM rho=1.000 result; slide 10 goes from "eleven items, six ours" to "fourteen,
           eight" adding the slide-9 correction and the misattributed rho~0.5; a new
           anticipated question covers everything tried beyond the six scenes.
  FIGURES  F5 climatology added. The LEFT panel is the argument: farm and non-farm move together
           so the raw 2025 rise is landscape moisture, and only the difference can be about the
           crop. Rendered and inspected.

### b) ★ T20 harvest detection — designed to test OUR OWN headline claim, and it failed

Slide 1 and the opening paragraph rest on the three epistemic objects, and every part of that
split comes from literature -- published calendars, plus Sharma & Goyal (1999) for cotton's
picking fractions. Three rounds and no test against data. Prediction written BEFORE the run,
purely ordinal: rice/maize/bajra earliest, groundnut later, cotton latest.

Confound handled by design: 81.2 mm fell 26-28 Oct, so a naive detector would report a
village-wide harvest on 3 Nov. Detection therefore ran on each plot MINUS the per-date village
median, removing any common mode.

    CONTROL 1  crops separate?      Kruskal-Wallis H=1.3, p=0.86    THEY DO NOT
    CONTROL 2  agronomic order?     Maize<Bajra<Groundnut<Rice<Cotton   CONTRADICTS
    CONTROL 3  one date dominant?   3 Nov on 20.7% of plots         passed

Diagnosed rather than abandoned. It is NOT plot size alone: restricting to larger parcels does
not recover separation (top 50% p=0.93, top 25% p=0.32, top 10% p=0.49) and the detected crop
ORDER RESHUFFLES RANDOMLY between subsets -- the signature of noise, not of a weak real signal.
Median parcel is 28 Sentinel-1 pixels; a steepest-single-drop estimator on 16 noisy points at
that size carries no timing information.

★ WHAT IT DOES NOT SHOW. A failed test is not evidence against the hypothesis. This does not
refute the epistemic-object split -- it means we could not test it this way. Recorded at the top
of WRITEUP section 8: our headline claim is the least independently verified thing we ship, and
the reader is told so.

Running score on approaches attempted after the forecast froze: five built, one survived
(the climatology), four killed by their own controls.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze unchanged, submission
unchanged at 966 rows.

---

## P3-18 — is Sokhda TYPICAL of the district whose statistic we borrow? (T21, src/p3_representative.py)

### The unexamined assumption under our dominant uncertainty

The anchor is a Vadodara DISTRICT statistic applied to ONE VILLAGE, and it carries 385.2 t of
the village interval -- more than every other term combined. P3-16's climatology tested the YEAR
adjustment (was 2025 ordinary at Sokhda? yes, z = -0.16). It never touched the assumption
underneath it:

    village yield  ==  district average yield

This has never been asked in three rounds, and it is a DIRECTIONAL error if wrong. A district
average applied to a village systematically poorer than its district overstates production, and
widening an interval hides a bias rather than fixing it.

Radar can test it because the comparison is RELATIVE, and relative is exactly what section 4.1
established a label-free method CAN do.

### Design, and why block-matched

Comparing Sokhda's 447 ha mean against individual pixels would compare incomparable spreads. So
the surrounding ~22 km box is cut into blocks of SOKHDA'S OWN SIZE (2.1 km ~ 441 ha), each
averaged over CROPLAND pixels only (ESA WorldCover 2021 class 40, via Planetary Computer, free).
Blocks touching Sokhda are excluded from the reference. Sokhda is then one draw from a
distribution of like-sized, like-land-use neighbours and its PERCENTILE means something.

All scenes restricted to track 34 descending, as in P3-16, so no geometry mixing.

### The control, fixed before the run

One year's percentile could be weather, noise or one bad scene. The whole comparison is repeated
for every year 2017-2025. STABLE rank across nine independent seasons = a structural property of
the village, which bears on the anchor. WANDERING rank = noise, report and stop. The criterion
was set in code before results existed: sd(offset) < 0.5 dB AND the same sign in all nine years.

### Honest limit, stated before seeing the answer

VH is a canopy-density proxy, not yield. A stable offset is evidence of a systematic canopy
difference, which is suggestive about yield and not equivalent to it. To be reported as a
DIRECTIONAL FLAG on the anchor, never applied as a correction.

Result recorded in the following entry once the nine-year run completes.

## P3-19 — T21 result: Sokhda is NOT typical of its landscape, and it is not an artefact

### The numbers

Block-matched comparison, 271 usable cropland neighbour blocks of Sokhda's own size (2.1 km,
~441 ha), ESA WorldCover 2021 class 40, S1 track 34 descending only, Jun-Sep:

    2017  offset +1.41 dB   percentile 91.9      (5 scenes)
    2018  offset +1.85 dB   percentile 91.9      (5 scenes)
    2019  offset +1.50 dB   percentile 85.2      (5 scenes)
    2025  offset +1.05 dB                        (1 scene, from the control run)

Same sign every year, 1.0-1.9 dB, Sokhda in roughly the top 10-15% of its cropland landscape.

### ★ The control that could have killed it, and did not

T21 measures Sokhda over SURVEYED PARCEL POLYGONS but its neighbours over WORLDCOVER-CLASSIFIED
CROPLAND. Those are different objects -- a classifier's cropland sweeps in margins, tracks, bunds
and fallow, all darker than a cultivated field -- so the asymmetry alone could manufacture the
whole offset. And the masks really do disagree:

    Sokhda parcels 11153 px | WorldCover cropland in hull 13757 px | overlap only 7191 px

64% of parcel pixels are called cropland by WorldCover; 52% of hull cropland lies in a parcel.
More than a third of the area is defined differently by the two conventions. So the concern was
real and large, not hypothetical.

Re-measuring Sokhda THE NEIGHBOURS' WAY (WorldCover cropland inside Sokhda's hull, parcels
ignored), so one definition governs both sides:

    offset_parcels     +1.051 dB
    offset_like4like   +1.007 dB
    definition_effect  +0.044 dB     <- 4% of the offset

The two masks disagree on a third of the AREA but agree on the RADIOMETRY. The offset survives.

### ★★ THE CONFOUND WE CANNOT RESOLVE, AND WHY THIS IS A FLAG NOT A CORRECTION

VH backscatter differs BY CROP. Sokhda is 43% cotton and 31% groundnut; the surrounding
landscape's crop mix is unknown to us, because we have crop labels for 966 parcels and for
nothing outside them. So "Sokhda is brighter than its neighbours" has at least two readings:

    (a) Sokhda's crops are doing better than the district      -> anchor understates us
    (b) Sokhda simply grows MORE OF A BRIGHTER CROP than its neighbours   -> anchor is fine
                                                                            and the offset is
                                                                            a crop-mix effect

Nothing we hold separates them. Classifying the surrounding landscape would require a crop map
we cannot validate, and the whole reason the anchor exists is that we have no yields.

So: REPORTED AS A DIRECTIONAL FLAG ON THE ANCHOR, NOT APPLIED. It joins the argmax bias
(+31.5 t, P3-10c) as a second independent reason to think 710 t is conservative rather than
optimistic, and both are stated rather than corrected.

### Engineering, recorded because three separate traps cost real time

  1. reproject(source=rasterio.band(ds,1), ...) pulls the WHOLE source raster over the network
     -- a 3-degree WorldCover tile and a 21701x28512 S1 scene. Gigabytes per read; the first
     attempt printed nothing for ten minutes. Fixed: window-read first, then reproject.
  2. Python buffers stdout when piped, so a `timeout`-killed run showed NO output at all even
     though it had been working. Fixed: run with -u.
  3. ★ Planetary Computer SAS tokens EXPIRE. sign() cached one per container for the life of
     the process -- fine for the 90-second S1 extraction, fatal for a nine-year loop, which died
     at year 4 with 'IReadBlock failed ... Cannot read offset/size for strile' on a URL whose
     se= had already passed. Fixed: refresh on age (20 min) plus a re-signed retry on any read
     failure.

The full nine-year run was interrupted three times by the above and by task kills; the four
years measured are consistent enough to report, and the decisive control is the like-for-like
one, which is complete. Not re-attempted.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze unchanged, submission
unchanged. Nothing here touched the deliverable.

---

## P3-20 (T22) — Is the ranking about the farm, or about where the farm is?

`src/p3_spatial.py` -> `p3_spatial.csv`, `p3_spatial_stats.csv`, `p3_spatial_variogram.csv`,
figure `p3_f6_spatial.png`. Writeup §9.8, deck slide 9b.

**What was NOT new.** §7 already reported Moran's I = 0.083 (z = 7.4) on the yield residual,
computed in `p3_uncertainty.py` with an analytic normal z. That established only that plots
are not independent, and it was used for exactly one purpose: an independence-based
sub-village interval would be too narrow. The statistic existed; the question did not.

**What was new.** Spatial correlation *of what, caused by what, and how big*. Every approach
in three rounds treats a parcel as an independent unit and ranks it. If the within-crop
ranking is a smooth landscape gradient, the per-farm advice reduces to "your location is
poor" and the sub-village deliverable is a soil map with a radar badge on it. That premise
had never been tested.

**Method.** Within-crop standardised health residual over 966 parcel centroids (UTM 32643,
mean field 68 m). Row-normalised inverse-distance weights to 400 m: mean 48.9 neighbours,
0 isolated. Empirical variogram in fixed bins to 1.6 km. Moran's I against a within-crop
permutation null, 999 shuffles -- shuffling INSIDE crop is what makes the null test location
and not crop identity.

**Controls.**
  C1 permutation null -- the licence to exist. Failed = no structure = nothing to decompose.
  C2 incidence angle, regressed out. Incidence varies smoothly across a single Capella scene
     by construction, so anything carrying a residual incidence term inherits a
     landscape-scale gradient for free.
  C3 June bare-soil baseline, regressed out. Separates "this ground is permanently bright"
     from "this season's canopy is doing well here".
  C4 invariance -- village total recomputed from the untouched forecast.

C2 doubles as the POSITIVE CONTROL, which is what makes a null result mean anything. Same
centroids, same bins:

    hi_resid      nugget 0.92  sill 0.99  range ~250 m   structured frac 0.07
    incidence     nugget 0.03  sill 0.43  range >1400 m  structured frac 0.94  [still rising]
    jun_baseline  nugget 0.64  sill 0.83  range ~75 m    structured frac 0.24

The positive control never reaches its sill inside the village -- its structure runs off the
edge of the AOI. The method sees landscape gradients loudly. The subject is flat from the
first bin, 93% nugget.

    Moran raw                 I=+0.0727  null -0.0013+-0.0091  z=+8.1  p=0.0010
    Moran minus_incidence     I=+0.0615  null -0.0009+-0.0093  z=+6.7  p=0.0010
    Moran minus_inc_and_soil  I=+0.0624  null -0.0014+-0.0089  z=+7.2  p=0.0010

Removing both confounds costs ~14% of the statistic and none of its significance. What
survives is structure in this season's canopy, not in the geometry and not in the dirt.

    variance split: landscape 0.085  farm-specific 0.960  (cross -0.046)
    bottom-decile advice list: 75/97 shared between raw and actionable ranking
    C4 village total: 710.0 t

**Verdict: SURVIVED. The premise of the sub-village product holds.** 91% of the within-crop
ranking is field-scale. This is the first result in the document that validates the premise
of the deliverable rather than one of its numbers, and the only late approach whose answer is
good news. It could have gone the other way: had the subject curve looked like the incidence
curve, the per-farm advice list would have been indefensible.

**Stated, not applied.** `actionable_rank` (ranking on the farm-specific component) reorders
the bottom-decile attention list by 22 of 97 farms. Not substituted into the deliverable: the
list was frozen, and a 9% correction to a ranking we cannot validate against yield does not
justify breaking a freeze. Village total invariant by construction.

**The distinction worth carrying into Q&A:** z = +8.1 says the correlation is certainly real;
I = +0.073 says it is small. Significant is not the same as large, and only the second reading
matters for the product. §7's use of the statistic is unaffected and stands.

### Engineering / honesty note

The FIGURE caught an error the table hid. `range_m` was computed as the first lag reaching
95% of a sill estimated from lags > 900 m. For incidence -- still climbing at the last bin --
that "sill" is not a sill and "~1400 m" read as a measurement. Plotting it made the rising
curve obvious. `p3_spatial.py` now flags `range_is_lower_bound` when the last lag exceeds the
mean of the preceding three, and prints `>1400 m [still rising]`. Understating the positive
control weakens the contrast, so the corrected version is the conservative one.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze 89b0e4e2 unchanged,
R3 submission 8304407e unchanged. Nothing here touched the deliverable.

---

## P3-21 (T23) — What did each of the six acquisitions actually buy?

`src/p3_voi.py` -> `p3_voi_lodo.csv`, `p3_voi_greedy.csv`, `p3_voi_stats.csv`,
figure `p3_f7_voi.png`. Writeup §9.9, deck slide 9b.

**The gap.** Six Capella scenes were delivered and all six were used. In three rounds nobody
asked what any single one contributed. It decides which sentences we own: if the ranking is
recoverable from one date, the trajectory machinery is decoration and "we tracked the crop
through the season" is not ours to say.

**C1, the control with an answer known before the run.** 29 October is already excluded from
the primary index -- LEVEL_DATES drops it and with use_29oct=False it enters no part, not even
the integral. So LODO on 29 Oct must give Spearman EXACTLY 1.0000, 0 farms moved. It did.
Harness reproduces the shipped ranking at rho = 1.0000. The run raises SystemExit on failure
rather than reporting numbers from a broken harness.

**Q1 leave-one-date-out** (rho vs shipped, farms leaving the 97-farm attention list):

    6 Jun   0.9993    1
    19 Jun  0.9481   17
    14 Aug  0.2108   77      <- 14 August IS the index
    13 Oct  0.8935   24
    12 Nov  0.8589   26

6 June moves ONE farm. Design fact never previously stated: level, uniform and growth all key
on 14 Aug and 19 Jun, so 6 June enters through the trapezoid integral alone.

**Q2 greedy forward selection:** 1 date 0.857, 2 0.874, 3 0.895, **4 0.9993**, 5 1.0000.
The jump at four is MECHANICAL, not fitted -- senesce is a slope through the late dates and
does not exist until a second late date arrives, so it switches on exactly when 13 Oct joins
12 Nov. Cleanest justification we have for R3's two extra scenes: they did not add another
look, they made a derivative measurable.

**Q3 calendar permutation, 200 draws.** C2 confirms the permutation disturbed growth/persist/
senesce in 200/200. rho(shuffled, shipped) = 0.312, 5-95% [-0.045, 0.885]. Destroying the time
axis costs more than deleting four of five scenes -- the trajectory machinery does real work.
Honest note kept in both figure and writeup: the band's top edge 0.885 exceeds the best
single-date 0.857, because some shuffles leave the peak date in place.

**C3 invariance:** worst within-crop area-weighted modifier mean deviation from 1.0 across all
variants = 3.33e-16. Village total cannot move.

**Verdict: SURVIVED, and it shrinks a claim.** We are entitled to "a peak-canopy index with
temporal corrections", not "a season-long trajectory model". One scene gets the broad
ordering; the rest fix about a third of the attention list and make senescence exist.

### ★ A latent silent failure in the SHIPPED code, found sideways

`derive_weights` takes a Spearman correlation matrix. A zero-variance part makes its column
NaN; `C.sum(axis=1)` then propagates that NaN into EVERY weight, so the composite is all-NaN,
z() returns zeros, norm.cdf(0) = 0.5, and the index becomes a CONSTANT 50 with no error
raised. Thin date subsets produce exactly that (growth with no pair, senesce with one late
date), which is how it surfaced -- several variants scored rho = nan and the greedy argmax was
silently picking arbitrary dates, because max() over NaN keys returns whatever it sees first.

Checked the shipped path: with the delivered six dates the minimum part sd is 1.0848 and all
weights are finite, for BOTH the primary and the with-29-Oct alternate. Nothing shipped is
affected. p3_build.py is frozen and untouched; the guard lives in p3_voi.build(), which drops
zero-variance parts before deriving weights. Recorded because the failure is SILENT -- it
produces a plausible constant, not a crash.

Second bug from the same run: a NaN score could win the greedy argmax. Fixed with an explicit
-inf substitution rather than by hoping NaNs no longer occur.

### Figure caught what the numbers passed, again

First cut of F7 drew the permutation 5-95% band as a filled span. Its top edge (0.885) sits
ABOVE the first three greedy points, so the figure read as "shuffling beats real dates". The
overlap is a real fact with a real cause (shuffles that leave the peak date in place), so it
is now stated in the annotation instead of being cropped away. Third round running that
plotting something changed what we said about it.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze 89b0e4e2 unchanged,
R3 submission 8304407e unchanged. Nothing here touched the deliverable.

---

## P3-22 (T24) — Would the same 97 farms be named if we re-flew the mission?

`src/p3_speckle.py` -> `p3_speckle_farm.csv`, `p3_speckle_sweep.csv`,
figure `p3_f8_speckle.png`. Writeup §9.10, deck slide 9b.

**The gap.** §7's ensemble resamples our MODELLING choices (features, weights, dates). Nothing
ever resampled the MEASUREMENT: same crop, same sensor, same day, a different realisation of
speckle. It is the only error source in this project computable from first principles rather
than argued about, and it had never been propagated into the per-farm ranking -- which is the
part of the deliverable that names individual people's fields.

Parcels are tiny: median 69 px, 159 farms under 20 px on the peak date. Relative SE of a
speckle mean over N looks is 1/sqrt(N) => median farm's brightness known to ~12%.

**Method.** Mean of N independent single-look intensity samples is Gamma(shape N), so perturb
each farm-date by u ~ Gamma(k, 1/k), k = npix * F, applied to g0_lin and g0_db together.
Rebuild with the SHIPPED p3_build.health_parts (not a reimplementation). 500 replicates per
noise level. F swept, not assumed: 2.0 / 1.0 / 0.5 independent looks per pixel.

    F=2.0  retention 0.754 [0.701, 0.804]  rank rho 0.908
    F=1.0  retention 0.686 [0.629, 0.732]  rank rho 0.855   <- nominal
    F=0.5  retention 0.616 [0.557, 0.670]  rank rho 0.786
    chance floor 10.0%

    Of the 97 named farms: 39 return in >=80% of re-flights, 30 in under half.

**Verdict: SURVIVED.** The attention list is far better than chance and about a third of the
individual names are not stable. That is a statement about the product's RESOLUTION, and it
needs the sensor's own noise model, which no ranking method supplies.

### ★ The positive control FAILED, and the failure is in the shipped writeup

C2 as first written: retention among listed farms must rise with pixel count. Result
rho = -0.008. The standing rule is that a test failing its own control is discarded, so the
"mis-specified" claim could not be asserted -- it had to be demonstrated.

Demonstrated: retention among ALREADY-LISTED farms is governed by MARGIN, how far below the
decile boundary the farm sits. Deep farms return whatever their size; boundary farms flip
whatever their size. rho(retention, margin) = +0.921 against rho(retention, npix) = -0.008.
Size and margin are near-independent, so the size effect cannot appear in that statistic.

C2b, the correctly specified version, tests the actual claim -- does speckle reach the index
in a size-dependent way -- and passes decisively:

    npix    0-20   n=159   mean index SD 12.19 points
    npix   20-50   n=224   mean index SD 11.26
    npix  50-150   n=287   mean index SD  7.24
    npix 150-inf   n=296   mean index SD  4.10
    rho(index SD, npix) = -0.622

Both controls are reported. The run raises SystemExit if the corrected control fails OR if the
margin explanation fails, so the mis-specification story cannot be retrofitted.

**C1 caught a real bug on its first run.** Zero noise must be an exact no-op. It reported
retention 0.093 (chance level) because numpy's rng.gamma returns NaN at shape=inf rather than
collapsing onto 1.0. The zero-noise case is now written explicitly rather than taken as a
limit. This is the second time this round a control with a KNOWN ANSWER caught a harness bug
before it could produce a plausible wrong number (cf. P3-21's C1 on 29 October).

**C4** village-total invariance asserted on every one of the 1500 replicates, not once.

### The honest bound, and it is not small

Only the LEVEL is perturbed, not the within-farm CV feeding `uniform` -- and uniform carries
the LARGEST weight in the shipped index, 0.249. A quarter of the index is noise-free by
construction of this test, so every retention above is an UPPER bound and true stability is
worse. Not modelled: a speckle model for a texture statistic needs the within-parcel spatial
correlation length, which we do not have.

Also unmodelled and stated: retention among listed small farms (0.73) slightly EXCEEDS that of
larger ones (0.67), which is the margin effect again and not evidence that small parcels are
safer. No enrichment claim is made in either direction.

**Not applied.** The frozen list is not re-cut. p3_speckle_farm.csv carries per-farm retention
at all three noise levels; the recommendation is that the attention list be read with a
stability column, because a 0.27 ha parcel and a 3.5 ha parcel do not deserve equal confidence
at the same index value.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze 89b0e4e2 unchanged,
R3 submission 8304407e unchanged. Nothing here touched the deliverable.

---

## P3-23 (T25) — Is the attention list measuring the crop, or the parcel boundary?

`src/p3_edge.py` -> `p3_edge_farm.csv`, `p3_edge_stats.csv`, figure `p3_f9_edge.png`.
Writeup §9.8 (merged with P3-20 in the consolidation pass), deck slide 9b.

**The gap, and it was one we named ourselves.** P3-22 closed on an admission: it perturbed the
LEVEL but not the within-farm CV feeding `uniform`, the LARGEST-weight part of the shipped
index (0.249), because a speckle model for a texture statistic needs a correlation length we do
not have. That left the biggest single component of the deliverable untested. This reaches it
by geometry rather than by noise model. Nine prior approaches interrogated which dates, which
neighbourhood, which noise realisation; none asked what a farm's PIXELS are.

Median parcel 69 px ~ 8x8, so a one-pixel border is half of it, and every border pixel mixes
farm with bund, track and neighbour. `level` is pulled toward the neighbourhood mean; `uniform`
is INFLATED by a mixed border, which reads as a patchy stand, which reads as a sick field.
p1_features already rasterises through a [-5,-2,0] m ladder whose bottom rung uses
all_touched=True (10 farms); nobody had asked what that rung costs.

**Method.** The SHIPPED rasterisation split into two disjoint per-farm pixel sets: core (four
neighbours in the same farm) and ring (the rest). Index rebuilt from core alone by the shipped
health_parts. No farm dropped; no-interior farms keep shipped values and are counted.

    boundary fraction   0-20px n=125 1.000 | 20-50 n=250 0.614 | 50-150 n=294 0.420
                        150+   n=297 0.233     median parcel 0.448, 75 farms have NO interior

**C3, the matched-N random null -- the only control that could kill it.** Core has fewer pixels
than the parcel and fewer pixels alone moves a mean and biases a CV, so the boundary split is
measured against discarding the same 37,861 pixels AT RANDOM.

                          drop boundary    random null
    rank rho vs shipped      0.853           0.857
    attention retained       0.639           0.680      (chance 0.100)
    med |level change|       0.484 dB        0.314 dB

The pairs coincide. The boundary carries a real level offset (1.5x the null) that does NOT
reach the ranking. On `uniform` specifically: core-only lowers CV by 4.9% vs 1.0% for the null,
so the edge does inflate our uniformity measure, but not enough to restructure the order.

    rho(index, ring frac) = +0.020    listed 0.412 vs unlisted 0.453 boundary fraction
    rho(ring frac, npix)  = -0.981  => ring fraction IS 1/size, so checked the consequence:
    rho(index, npix)      = -0.017  => NO parcel-size bias, across a 40x spread in area

**Verdict: SURVIVED as a negative result, and the negative is the product.** P3-20 showed the
ranking is about the farm and not its neighbourhood; this shows it is about the farm and not
its outline. Together they license publishing a per-farm list at all. Residual stated: uniform
is measurably edge-inflated, and 75 farms are pure boundary with no interior measurement in
anything we ship.

### C2 failed as first written, and was diagnosed rather than loosened

Injecting a known +3.000 dB into ring pixels missed by 1.94e-07 dB against a 1e-9 threshold.
Two candidate causes, and they separate cleanly: a mask addressing the wrong pixels misses by a
FRACTION OF 3 dB in any dtype, whereas storage precision vanishes in float64. Re-ran the
identical check in float64 -> 7.11e-15. Both are reported and both thresholds enforced, so the
precision story cannot be retrofitted. C1 passed at 3.55e-15 for the same reason it should
have: both sides come from the same float32 array with no arithmetic on the values.

### The figure caught a table error, fourth round running

F9's left panel drew the 0-20 px bin median boundary fraction at 1.00; the printed table said
0.80. The table filtered ring fraction by `both` (farms with a core AND a ring) while the
figure did not -- and all 75 no-interior farms sit in that bin. They ARE parcels, so excluding
them understated exactly the population the test is about. Table fixed to report ring fraction
over every farm and the level difference only where it is defined, with both counts printed.

**Verification.** regression 12/12, defensibility 19/19, R2 freeze 89b0e4e2 unchanged,
R3 submission 8304407e unchanged. Nothing here touched the deliverable.
