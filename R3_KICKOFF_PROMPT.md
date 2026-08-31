# Round 3 kickoff prompt

Paste everything below the line as the first message in a new chat opened in
`C:\Users\sorat\Downloads\AISEHack_R2_SAR_Crop\AISEHACK-2.0-T1-R3`.

---

I am Team GDHTM in the ANRF AISEHack 2.0 final round (Round 3): **SAR crop yield
forecasting**, Sokhda village, Vadodara district, Gujarat, 966 farm plots. We are one of six
teams shortlisted from Round 2. Round 3 closes **3 September 2026, end of day**, and the work
is presented in person at the Goa finals, **2–3 September 2026**. Today is 30 August 2026.

Working directory for this round: `C:\Users\sorat\Downloads\AISEHack_R2_SAR_Crop\AISEHACK-2.0-T1-R3`
Read-only reference from the last round: `C:\Users\sorat\Downloads\AISEHack_R2_SAR_Crop\AISEHACK-2.0-T1-R2`

**This message asks you for research and a plan, not for an implementation.** Work through
Phases 0–3 below and stop at the gate. Do not build the pipeline, do not write the model, do
not touch a deliverable until I approve the plan. If you finish a phase early, go deeper in
the next one rather than starting the build.

---

# 1. What Round 3 actually asks for

Verbatim from the competition, with the parts that change our work in bold.

> Round 2 asked you to estimate crop health and **yield-to-date**. Round 3 changes the task:
> you now have the full temporal picture — **6 Capella X-band HH-polarization SLC
> acquisitions spanning the entire growing season** — and your job is to produce a **final
> yield forecast, not an estimate-to-date**. This means **predicting the actual yield outcome
> at harvest** for each plot, using the complete time series rather than a partial one.

For each of the 966 plots, produce:

1. a **final yield forecast** for the crop grown on that plot;
2. **supporting plot-level stats/metrics that justify how the forecast was derived**;
3. **aggregated village-level yield summaries by crop type** — Rice, Cotton, Maize, Bajra,
   Groundnut.

No ground truth is provided, deliberately. No prescribed method. Any modelling approach and
any external data are permitted "as long as your writeup clearly explains and justifies your
methodology and any external sources used". Crop classification is **carried forward from
prior rounds** — it is an input this round, not a deliverable.

## 1.1 The rubric, and what changed from Round 2

| criterion | R3 pts | R2 pts | what it rewards |
|:--|--:|--:|:--|
| Technical Soundness | **25** | 25 | a rigorous, well-justified method for a **final forecast** from the full 6-pass series |
| Creativity | **15** | 20 | novel or thoughtful modelling, **including sensible use of external data** |
| Plausibility & Defensibility | **25** | 20 | forecast values physically/agronomically plausible, **with clear reasoning and sanity checks given the absence of ground truth** |
| Aggregation | **15** | 10 | sound logic rolling plot-level forecasts up to **village level, by crop type** |
| Documentation & Presentation | **20** | 25 | writeup, notebook, and **the in-person Goa presentation and written document** |

Four consequences, and they should drive the whole plan:

1. **Plausibility & Defensibility is now the joint-largest criterion at 25**, and its wording
   names our exact situation — "sanity checks given the absence of ground truth". This is the
   criterion Round 2 taught us to win: our whole post-R2 pass was measured negatives,
   controls that could fail, and retracted claims. **Sanity checks are worth as much as the
   model.** Budget for them like a deliverable, not like a QA step.
2. **Aggregation went 10 → 15 and is explicitly per crop type.** In R2 this was nearly free
   (966/966 rows, one clear rule). It is no longer free: it now needs a stated aggregation
   rule, per-crop village totals, and — if we can — uncertainty propagated to the village
   level. Production must be `Σ(yield × area)`, never a mean of per-hectare rates.
3. **Creativity dropped 20 → 15 and Technical Soundness held at 25.** The premium moved from
   novelty toward rigour. A defensible physical forecast beats a clever unvalidated one.
4. **Documentation is 20 and now includes the live Goa presentation.** The PPT is a scored
   artefact, not an afterthought, and it has an earlier effective deadline than the writeup.

## 1.2 Submission requirements

- **Kaggle Writeup, ≤ 2,000 words** (R2's cap was 4 pages; this is tighter — cut hard).
- **Media Gallery**, cover image required. Plot-level forecast maps, village aggregation
  charts, temporal backscatter trends, and anything else that justifies the method.
- **Public notebook** with the full pipeline, no login or paywall.
- **Written documentation** covering methodology in detail — modelling approach, external
  data, **assumptions made in the absence of ground truth**, and **how plot-level forecasts
  were aggregated to village level**. (This is separate from the writeup and replaces R2's
  video.)
- **Goa Finals PPT**, 10 minutes.

## 1.3 Open items to settle before anything is built

Resolve these first; each has bitten a team before.

- **A1. Is there a submission schema or sample file?** The description names no CSV columns.
  In Round 2 the host's `Sokhda_Dummy_Submission.xlsx` caught a **1000× unit error** that
  every one of our internal checks had passed — no internal validation can catch a unit
  convention that exists only in the host's file. Check the Kaggle Data tab, the rules page,
  and any host communication for a template. If none exists, we define the schema ourselves
  and state it, and we carry R2's column names forward so the two rounds are comparable.
- **A2. What unit is the forecast in?** R2's column was t/ha (host dummy 1.24–9.00). Confirm
  R3 expects the same. Also decide and *state* whether cotton is lint or seed cotton — see
  §3.4.
- **A3. The rubric mentions "quality of the video" while the Description says "No video is
  required for this round."** The host's own text contradicts itself. Assume no video, note
  the discrepancy, and if there is a channel to ask, ask.
- **A4. The dataset description claims an "expanded village AOI" and an "expanded set of
  villages".** The delivered shapefiles are byte-identical to Round 2's — one village,
  Sokhda, the same 966 plots (verified, §2.2). Either the description is wrong or a file is
  missing. Worth one question to the host, and worth one honest sentence in the writeup
  either way.

---

# 2. The data, as measured — not as described

I have already inspected the delivered archive. Use these facts; do not re-derive them, but
do verify anything you are about to lean on.

The dataset is still a single zip in the round folder:
`anrf-aise-hack-2-0-round-3-sar-crop-yield-forecasting.zip`, 3,189,776,176 bytes, 41 files.
Extracting it is task one of Phase 0.

## 2.1 The six scenes

| date | IST overpass | look side | centre incidence | scale_factor | nesz_peak dB | ENL | SLC bytes |
|:--|:--|:--|--:|--:|--:|--:|--:|
| 2025-06-06 | 12:55 | left | 35.244 | 0.00212186 | −26.13 | 1.0 | 321,207,995 |
| 2025-06-19 | 07:44 | left | 28.768 | 0.00236205 | −27.76 | 1.0 | 271,736,501 |
| 2025-08-14 | 08:41 | left | 28.692 | 0.00198903 | −27.97 | 1.0 | 274,250,470 |
| 2025-10-13 | 07:56 | left | 31.528 | 0.00136443 | −27.35 | 1.0 | 308,999,247 |
| **2025-10-29** | **01:37** | **right** | 29.840 | 0.00155765 | −27.74 | 1.0 | 290,366,117 |
| **2025-11-12** | **19:22** | left | 29.746 | 0.00162432 | −27.72 | 1.0 | 280,946,011 |

All six are stripmap, HH, ascending, ~9.65 GHz, azimuth bandwidth 5086–5120 Hz,
`radiometry = "beta_nought"`, `calibration = "full"`, annotated ENL 1.0.

**The first four are byte-identical to the Round 2 dataset** — `_extended.json` md5 and SLC
file sizes both match. Every measurement Round 2 made on those dates transfers directly. Only
two scenes are new, and characterising them is the first real technical task of this round.

### Three properties of the new scenes that the description does not mention

1. **29 October is right-looking. The other five are left-looking.** Same ascending pass
   direction, opposite antenna pointing, so the AOI is imaged from the other side and the
   ground-range direction is mirrored relative to field features. For rows, bunds and any
   azimuthally anisotropic canopy this is a genuine radiometric difference, not a nuisance
   constant, and it does not cancel in a between-date difference the way a calibration offset
   does. **Any feature that differences 29 Oct against a left-looking date must be tested for
   this, not assumed clean.**
2. **The two new passes are at night and in the evening**: 01:37 IST (pre-dawn, the peak of
   dew formation) and 19:22 IST (post-sunset). The other four are 07:44–12:55 IST. Canopy and
   soil wetness at X-band is a first-order effect on backscatter, and dew is a documented
   several-dB term. A "senescence" signal read off 29 Oct could be a dew signal. This needs an
   explicit test and, ideally, an independent meteorological check at the overpass hour
   (Open-Meteo hourly, free, no key — Round 2 used it exactly this way).
3. **29 Oct and 12 Nov are only 0.094° apart in incidence** — the closest pair in the stack
   after Jun19↔Aug14 (0.076°) — which would make them a geometry-matched pair for change
   detection and the one candidate for repeat-pass coherence. **But the opposite look sides
   probably spoil it.** Measure it; do not assume either way. If it holds, a 14-day
   late-season pair is a strong asset; if it fails, that is a clean reportable negative.

## 2.2 Plots and village

`Farm_boundaries_shp/Farm_boundaries_shp/Sokhda_Farms.{shp,dbf,prj,shx,cpg}` and
`Village_Shp/Village_Shp/Sokhda_Village.*`. Verified **byte-identical to Round 2**
(`Sokhda_Farms.shp` md5 `c9d7ede5f36de1b7524972f91404af2f`, `.dbf`
`12745a87e8eea707f7c69b65f03fecb5`, `Sokhda_Village.shp` `8ebc7be9cc3f94c925040509088712b3`).

So all of Round 2's geometry work stands: 966 polygons, `FID` 1–966 the only usable
identifier, total 447.5 ha, median plot 0.274 ha, village polygon 1174.1 ha, 9–10 degenerate
parcels enclosing ~0 ha whose centroids land hundreds of km away, 9 invalid geometries needing
`make_valid`.

## 2.3 The trap that is still in the archive

The `20250619` folder again contains a **byte-identical duplicate of the 20250606 SLC**
alongside its own. Matching a scene by folder alone can return the June 6 data as "June 19";
matching by basename alone finds the June 6 name in two folders. **Resolution must require the
date in both the folder name and the file basename, and assert exactly one match.** Round 2's
`src/common.py::slc_path()` is the reference implementation. The failure mode if missed is
silent and plausible-looking: June 19 shows zero change from June 6.

---

# 3. What carries forward from Round 2 — do not re-derive this

The full Round 2 evidence store is at `..\AISEHACK-2.0-T1-R2`. Read these before proposing
anything, in this order. Read them yourself; do not spawn subagents and do not ask me to
summarise them.

1. `post-r2/SPRINT_BRIEF.md` — the compressed state of everything: adversarial Q&A, eleven
   closed ideas, four shipped defects, measured portability debt.
2. `post-r2/README.md` — index of all 18 post-R2 experiments and their verdicts.
3. `docs/REPORT.md` — the R2 method end to end.
4. `post-r2/COMPETITOR_ANALYSIS_R2.md` — teardown of all five other shortlisted writeups,
   plus the cross-team comparison of all six submissions.
5. `post-r2/ROUND3_DIRECTIONS.md`, `KHARIF_ANCHORS.md`, `UNCERTAINTY.md`, `DATA_SOURCES.md`,
   `LABEL_CORROBORATION.md`, `LABEL_DISTRIBUTION.md`, `GROUND_TRUTH_SELECTION.md`, and
   `DELIVERABLE_MINING.md` — the last of these mines the competitors' *notebooks and PDFs*
   rather than their writeups, and it is the source of several items in §3.5, §3.6 and §8 R-G.
   (`post-r2/ROUND3_PLAN.md` is superseded by `SPRINT_BRIEF.md` and `ROUND3_DIRECTIONS.md` —
   skim its progress log at most.)
6. `internal/RESEARCH_LOG.md` — every stage-by-stage decision with its evidence tag.
7. `data_aux/SOURCES.md` — every external input, with caveats and one retraction.

**We are rebuilding fresh for Round 3.** Round 2's `src/` is a reference and an evidence
store, not a base to copy. Reuse the *findings* freely; re-earn the *code*. Round 2 stays
frozen and untouched — `results/submission.csv` must keep md5
`89b0e4e2aef63ace4989fc0a44590ee5`, and nothing in this round writes into that folder.

## 3.1 Facts you will otherwise get wrong

- **Round 1's official score was MSE 11.071, not 0.000.** The 0.000 run was after the
  deadline. Sokhda's crop shares from R1 are our best estimate of the village mix, never
  "exact truth" — but they were right to the decimal against an independent team's read
  (0.25 pp), and they are the crop-mix prior. `data_aux/sokhda_r1_truth.csv`: Cotton 43.0%,
  Groundnut 31.0%, Rice 10.6%, Bajra 9.4%, Maize 6.0%, of 690.88 ha cropped area.
- **Capella SLC calibration is `β⁰ = scale_factor² · |z|²`.** ESA EDAP's `sc` is not the JSON's
  `scale_factor` — it is that field *squared*, as Capella's own `capella-reader` reference
  implementation (`beta0_complex = SF * DN`) settles. Confirmed independently on the vendor's
  own `nesz_peak`: under SF² the darkest 0.1% of pixels land on the declared noise floor to
  **0.35 dB mean absolute error across four scenes**; under SF they sit **+26 to +28 dB
  above** it, which is physically impossible. **Round 2 shipped SF and this is our chance to
  fix it.** Nothing in Round 3 is frozen. Fix it, and verify the same NESZ test on the two new
  scenes.
- **Cotton yield in Indian statistics is lint, not seed cotton** (×2.94 for kapas at 34%
  ginning outturn). Every official source — APY, USDA FAS, CEIC, Gujarat state — reports it
  this way; Gujarat's own figure is 647 kg/ha. R2 tested converting and rejected it on
  evidence that did not decide.
- **The bajra anchor we shipped (2.714 t/ha) is an annual figure on a kharif deliverable.**
  Summer bajra yields 1.6× kharif bajra and is 39% of the area. Corrected value **1.91 t/ha**,
  validated out of sample at 3× the accuracy of doing nothing. Measured, never applied because
  R2 was frozen. **Apply it this round.** The same test *rejected* the equivalent groundnut
  correction — its ratio makes the estimate worse than doing nothing. Rice and maize need no
  correction.
- **Ground truth is blocked and is not coming.** Krishi-DSS needs an API token we do not have;
  AnyROR VF-12 needs a person and a CAPTCHA. Plan on its absence. No team in this competition
  has ground truth either — which is exactly why the rubric scores defensibility instead.
- **Our groundnut share is disputed and the dispute is unsettled.** Three positions exist on
  how much of Sokhda is groundnut: the Vadodara APY 2022–23 table says **0.35%** (off a
  1,004 ha district base), Project Orion's external agro-zone reference says **16%**, and our
  Round 1 whole-village reconstruction says **30.8%**. It is our second-largest class. Orion's
  case — found in their *code comments*, not their writeup, and much stronger there — is that
  groundnut in Gujarat is concentrated in Saurashtra rather than the central zone, that
  Vadodara's field-crop profile is paddy/cotton/maize, and that Round 1 found Vadodara bajra
  near zero against the 9.5% we ship. We tested our groundnut class on both withheld witnesses
  and it separates from bajra in exactly the direction the crop calendar demands (NDVI 0.295 vs
  0.255, Mann–Whitney p = 6.4×10⁻⁵) — **but that validates the class's behaviour, not its
  share.** A class can behave correctly and still be over-allocated. Nothing we held in Round 2
  could settle 30.8% against 16%. See §4 for why Round 3's data might.
- **Our headline R2 claim:** two independent sensor stacks back our cotton labels on **78.8%**
  of farms, and **42.5% of the village is corroborated by neither** — almost entirely rice,
  maize and bajra. We are the only team that measured where its own map is unsupported.

## 3.2 Closed — do not re-propose without new evidence

Each was tested and priced in the post-R2 pass. Re-opening one costs sprint hours and the
answer will not change unless the six-date stack changes the premise — and if you think it
does, say *which* premise and *why* before spending anything.

| idea | why it is closed |
|:--|:--|
| Dense Sentinel-1 as a label source | κ +0.135, below the annual embedding's +0.155; the series is already in the repo |
| Dynamic World non-crop filter | half a farm-size detector; effect flips sign across area deciles |
| WorldCereal crop type | 2021 product, κ = −0.010 |
| Quegan–Yu speckle filter | buys 5.6–6.4% of between-farm signal, on a noise term shown not to drive witness disagreement |
| Any covariate coarser than ~1 km | ceiling 0.041 at 1 km, **0.000** past 11 km, measured on our own farms |
| ERA5 / NASA POWER / OpenWeatherMap for ranking | one value for all 966 farms |
| USDA ERS | US farm finances, 16 US states |
| AlphaEarth embeddings as a label source | 0.0% recall on maize, 4.7% on rice |
| CoV excess over an L=1 speckle baseline | our grid is 4–5 looks, not 1; adopting it reproduces a bug another team publicly retracted |
| Plot-size de-biasing by linear detrend on log(area) | artefact is real, the correction makes the index worse on both witnesses |
| Forcing GDAL polynomial order 2 | 0.07 m; recommendation withdrawn |
| Uncertainty-first ground-truth sample selection | biased −12.4 to −23.6 pp; it measures the hard farms, not the village |

## 3.3 The measured bottleneck

Three independent measurements agree, and they were not designed to:

| measurement | result |
|:--|--:|
| sampling noise as a share of between-farm signal | 15.9% |
| share of yield variance explained by the crop label alone | η² = **0.820** |
| agreement of six independent pipelines' crop labels | κ = **0.060** |

**Our limiting error is the crop label, and it is an information limit, not a processing one.**
Better filtering does not help. In Round 3 the crop label is a carried-forward *input* and is
not itself scored — but yield inherits it wholesale, so how the forecast depends on the label
is a first-class design question, not a detail.

## 3.4 One thing Round 2 could not do that Round 3 can

R2's experiment e18 rejected propagating the crop posterior into yield, and the blocker was a
unit boundary: **cotton's yield is lint while the other four are grain or pod**, so an
expectation across the five classes adds numbers in different units and moved the village
total by +12.8%. That was unfixable in R2 because the submission was frozen.

**It is fixable now.** Put every crop on one commensurable basis before any expectation is
taken — either convert cotton to kapas (×2.94) and say so, or carry both columns explicitly.
Once units are homogeneous, the label posterior becomes propagable, which is the structural fix
for η² = 0.820. Treat this as a *hypothesis to test*, not a decision already made: it needs the
same evidence bar as anything else, and the +25% it moves on the village headline is exactly
the size of move that demands evidence that decides.

## 3.5 The freeze dividend — finished, validated, never shipped

Five pieces of work were completed and tested after Round 2 closed and could not be shipped
because the submission was frozen. **Round 3 freezes nothing.** Each is a ready win that costs
implementation time only, not research time. Re-verify each against the six-date stack rather
than pasting the R2 number, but do not re-litigate the decision.

| item | state | what it needs in R3 |
|:--|:--|:--|
| **SF² calibration** | measured end to end; 99.2% of crop labels unchanged, health ρ 0.9908, production +0.5% | apply from the start; re-run the NESZ check on the two new scenes |
| **Bajra kharif anchor 2.714 → 1.91 t/ha** | three estimators agree to 10%; validated out of sample at 3× the accuracy of doing nothing | apply; re-check against a kharif-2025 anchor if Phase 0 finds one |
| **Ten-farm non-crop flag** | flagged by *both* our own SAR rule and Dynamic World — 10 farms against 6 expected by chance; 0.60% of area, median 0.190 ha; our index already ranked them at median **1.1** against a village median of 50.7 without being told | ship as a **flag, never a filter**; they still enter the crop-share accounting and the village aggregate as though they were fields, and that is the actual defect |
| **Calibrated per-farm sampling uncertainty** | split-half test predicts our own noise to **3.4%** with no tuning (ratio 0.966, ρ +0.9663) across farms spanning two orders of magnitude in pixel count | ship it, presented honestly as *sampling* uncertainty — it is calibrated but it is only 15.9% of between-farm signal and does not predict witness disagreement, so presenting it as general confidence would overclaim |
| **The crop-label posterior as transparency** | already computed per farm; openly unsure (median max probability 0.409, 69.4% of farms with no class above 0.5) | publish it alongside the label with its measured limitations — it is under-confident at the low end and ranks weakly within crop. No other team ships a per-farm label distribution at all |

The uncertainty item deserves emphasis for this round specifically: **all six shortlisted teams
shipped point estimates, four shipped a confidence number, and none demonstrated that its
confidence was calibrated.** With Plausibility & Defensibility now at 25 points and its wording
naming "sanity checks given the absence of ground truth", a *demonstrated* calibration — a test
that needs no labels and could have failed — is the single most on-rubric asset we already own.

## 3.6 Known capability gaps, with the fix already identified

Found in Round 2, never closed. Each is a hypothesis with a named test, not an adoption.

- **A NESZ-based per-farm quality gate.** We discovered `nesz_peak` while adjudicating the
  calibration and then used it nowhere. Orion gates farms on clearing the declared noise floor
  by a stated margin (`NESZ_MARGIN_DB = 3.0`). By our own reckoning 12–23% of AOI pixels sit
  near the floor. **This matters more in Round 3 than it did in Round 2**: the two new dates
  are late-season, when harvested fields are smooth, dry and dark, so a larger fraction of
  plots will approach the noise floor on exactly the acquisitions the forecast leans on. A farm
  whose late-season return is noise-dominated should be flagged, not silently averaged.
- **Orion's other quality constants**, worth testing against ours rather than adopting:
  `MIN_CORE_PX = 60` (below which "the farm-mean is too noisy to trust on its own"),
  `MIN_VALID_DATES = 3`, `MIN_DATE_COVERAGE = 0.50` (a date counts for a farm only above that
  valid-pixel fraction), and proportional erosion (`ERODE_MAX_M = 4.0`, `ERODE_FRACTION = 0.25`)
  rather than our fixed buffer ladder. `MIN_VALID_DATES` becomes more meaningful with six dates
  than with four.
- **Thin-plate-spline geocoding, measured and never built.** Round 2 measured its own GCP fit by
  leave-one-out — fit on 224 control points, predict the held-out one — and got a **3.6 m median
  residual**, about twice as good as the ~8 m another team reported and rejected. So their
  premise does not transfer and we cannot inherit "polynomial geocoding is a defect". **But the
  spline still halves it**: 3.62 → 1.78 m median, and 18.5 → 15.2 m at the 95th percentile. The
  tail is what matters — a 19 m error is **35% of our 52 m median plot side**, i.e. real boundary
  mixing on the worst-placed farms, currently guarded only by eroding before sampling. Verdict
  was "adopt, but not for their reason"; it was never implemented. If it is built, mind the
  silent-no-op trap in §7.3, and score any spline by leave-one-out rather than by its residual
  at the control points, where a TPS is zero by construction and tells you nothing.
- **A sub-village spatial product.** With one village the required aggregation table is a single
  row carrying no spatial information. Orion also reported on a fixed 500 m grid — 46 zones,
  ≥5 farms each, covering 946/966 farms — and found **32 points of health spread** hidden
  behind their one number. Cheap, and Aggregation is now 15 points.
- **A non-circular test of the crop labels.** Ours have none that is not partly circular. The
  method is Orion's: regress the witness on the ranking axis that produced the labels, then run
  the group test on the *residual*. Their own Tier-2 labels explained 19% of raw NDVI variance
  and **0.2% of the residual**.
- **Reserved-scene discipline** — retire any scene that set a design decision from the
  validation set. Round 2 used 13 Oct Sentinel-2 as a headline witness *and* corrected our
  completion-term sign against it; that contamination was never accounted for. With six dates
  there is more room to reserve one properly. **Caveat before citing Orion as the model:** their
  own notebook carries the note *"no reserved scene cleared the gate, so this audit runs
  against the…"*, which suggests the published discipline was cleaner than the executed one.
  Read it before holding it up as a standard.

## 3.7 Per-farm data assets that transfer for free

**The Round 3 shapefile is byte-identical to Round 2's, so `farm_id` 1–966 means the same
polygon in both rounds and every per-farm table below joins exactly.** "Fresh rebuild" applies
to the *pipeline*, not to data that has already been fetched, paid for in API latency, or in
two cases obtained through a route that is now blocked. Do not re-fetch these; do verify the
join on `farm_id` and spot-check a few rows before leaning on any of them.

All paths relative to `..\AISEHACK-2.0-T1-R2\post-r2\`.

| asset | what it is | why it matters in R3 |
|:--|:--|:--|
| `results/e14_embeddings/farm_embed.csv` | 64-band AlphaEarth annual embedding per farm, 961/966 | an independent sensor stack that never saw Capella. **Re-obtaining it needs interactive Google auth** |
| `results/e17_dense_s1/two_sensor_agreement.csv` | per-farm flags `s1_ok`, `emb_ok` — which farms each independent sensor backs | the 42.5%-uncorroborated finding as a *per-farm column*. Lets the forecast carry a corroboration flag rather than a village-level caveat |
| `results/e18_label_distribution/label_distribution.csv` | per-farm five-class posterior, entropy, `p_assigned` | the label distribution §3.5 says to ship |
| `results/e11_uncertainty/health_uncertainty.csv`, `split_half.csv` | calibrated per-farm sampling SE and the raw split-half draws | the calibrated-uncertainty exhibit, already validated |
| `results/e13_gee/farm_gee.csv` | Dynamic World and WorldCereal per farm, incl. the non-crop and irrigation layers | the ten-farm flag; **GEE also needs interactive auth to re-fetch** |
| `results/e4_consensus_all/consensus_crop.csv` | all six teams' crop label per farm, plus consensus and agreement count | cross-team analysis without re-parsing five submissions |
| `results/e1_calibration/farm_features_calibrated.csv` | the **SF²-corrected** per-farm feature table for the four shared dates | not to be used as input — but it is a **reproduction target**: our new four-date features must land on these, and a mismatch is a bug in the new pipeline |
| `results/e10_kharif_anchors/vadodara_season_crops.csv` | 461 Vadodara season-split district records, already fetched | the source API is paged and flaky; this is cached |
| `results/e9_mine/code_*.txt`, `prose_*.txt` | all four competitor notebooks and three PDFs as greppable plain text | 555k chars already extracted — grep, don't re-convert |

### The competitor assets are worth more than the list suggests

`writeups_submissions/project_orion_team_apes/` contains not just their submission but their
**full per-farm feature tables** — `farm_features.csv`, `farm_crops.csv`, `farm_health.csv`,
`farm_yield.csv`, `farm_ndvi.csv`, `village_summary.csv`, `zone_summary.csv`, all 966 rows.
Three of these are unusually valuable:

1. **`farm_features.csv` carries their own per-farm γ⁰ in dB for all four shared dates**
   (`g0_db_T1..T4`), plus per-farm CoV, ENL, pixel counts and coverage fractions, computed by a
   completely independent implementation of the same four scenes we are about to reprocess.
   **This is the only external check available on our own radiometry and geocoding chain**, and
   it is precisely the class of error that has burned this field: our own calibration bug and
   another team's geoid bug were both *common-mode* errors that every internal consistency check
   passed, because every date was wrong the same way. Correlating our new per-farm dB against
   theirs, per date, costs minutes and can catch what no self-consistency test can. Expect a
   constant offset (different calibration conventions) — it is the *farm-to-farm agreement*
   that is the test, not the level.
2. **`farm_ndvi.csv` carries per-farm NDVI for an 18 October scene** (`ndvi_T4R`) as well as
   13 October and a June date. Eighteen October is a date we never fetched, and it is the
   reserved scene their validation was reported against. A second late-season optical reference
   we already hold.
3. **`village_summary.csv` and `zone_summary.csv`** — their village table is per crop with
   area-weighted health, yield, production and a confidence share; their zone table is the 46-zone
   500 m grid. 8bit's `village_summary.csv` is a different per-crop schema again. **Round 3
   scores aggregation at 15 points and asks specifically for village-level summaries by crop
   type — two worked examples of that exact deliverable are sitting in the folder.** Read both
   before designing ours.

## 3.8 Reusable analysis harnesses

Same principle: rebuild the pipeline, not the instruments. These are validation and analysis
tools, not pipeline stages, and re-deriving them would spend a meaningful fraction of a
three-day budget. All in `..\AISEHACK-2.0-T1-R2\post-r2\experiments\`.

| harness | where | what it does |
|:--|:--|:--|
| **spatially blocked k-fold CV** | `e14_embeddings.py::blocks()`, `cv_kappa()` | KMeans on centroids so no farm is predicted by its own neighbours. The standard evaluation harness for anything per-farm; leakage through spatial autocorrelation is the default failure mode here |
| **permutation null** | same file | label shuffles to establish that an observed score is not chance. e14's result sat 8.3 permutation SDs above null |
| **farm-size control** | same file | `rho(area, correct)` — the control that killed the Dynamic World screen. Run it on anything before believing it |
| **split-half sampling test** | `e11_uncertainty.py::farm_pixels()`, `t1_split_half()` | measures a farm's own sampling noise with no model, no witness and no ground truth |
| **resolution ceiling** | `e12_data_ceiling.py::ceiling_curve()` | prices any candidate covariate by cell size before fetching it |
| **overpass-hour weather** | `e12_data_ceiling.py::weather_timing()` | Open-Meteo hourly at the acquisition timestamps. **Point it at all six dates**, including the night and evening passes — §7.1 needs exactly this |
| **NESZ adjudication** | `e6_verify_claims.py::test1_nesz()` | the darkest-percentile-versus-declared-noise-floor test. Re-run on the two new scenes |
| **SF² correction of a feature frame** | `e1_calibration.py::correct()` | the per-date rescale, if a like-for-like comparison against R2 features is wanted |
| **partial Spearman** | `e2_uniformity.py::partial_spearman()` | correlate with brightness partialled out — the check that distinguishes a real effect from an SNR proxy |
| **Cohen's κ + pairwise matrix** | `e4_consensus_all.py::kappa()`, `matrix()` | cross-team and cross-sensor agreement |
| **sampling-design simulator** | `e16_gt_selection.py::synth_truth()` and the estimators | if any sampling or subset-selection question arises, this answers it with a control that passes at zero dependence |

## 3.9 Open leads carried forward — recorded so they are not lost, not recommended

Four ideas were left untested at the end of Round 2, each with the test that would settle it.
They are listed so the plan can consciously decline them rather than rediscover them at 2 a.m.

- **Spatial modelling of the residual.** Moran's I is positive and significant on every layer we
  computed (health 0.105, and 0.42 on the 19 June level), so neighbouring farms genuinely share
  condition — shared soil, water, sowing date, management. We *report* that statistic and never
  *use* the structure. Kriging or a spatial random effect could sharpen per-farm forecasts, and
  `src/pb_mrf.py` in the Round 2 tree is a working MRF over a farm adjacency graph. **Test the
  premise first:** is the *forecast residual* spatially autocorrelated beyond chance? If not,
  there is nothing to smooth. Note also the ceiling argument — if our layer carries *more*
  spatial structure than the optical reference over the same farms, the excess is coming from
  something other than field condition, and that is a warning rather than a win.
- **Texture on the full-resolution complex SLC** rather than on the detected, multilooked
  product, where ours is currently computed. We hold the complex data and most teams discard
  phase on line one.
- **Sentinel-2 harmonic / gap-filled NDVI** — see §5.1; the cloud objection that killed this in
  Round 2 probably does not apply to the October–November window.
- **The irrigation lead.** WorldCereal's irrigation layer correlates **−0.167** (p = 2.4×10⁻⁶)
  with withheld 13 October NDVI — significant and *wrong-signed*, i.e. irrigation-flagged
  parcels are less green in October. Coherent with the summer-occupancy story (a parcel
  irrigated for a summer crop may sit fallow or late in kharif), and therefore weakly connected
  to the groundnut-share question in §3.1. An open lead, never a result.

---

# 4. The intellectual core of this round

Think about this before you read a single paper, because it determines which literature is
relevant.

**"Forecast" means something different for each crop, and the six dates land asymmetrically.**

Gujarat kharif calendar against our stack: rice, maize and bajra are sown on the monsoon onset
and harvested September–October. Groundnut is lifted October–November. Cotton picking runs
October–January.

| crop | ~% of village | season state at 13 Oct (R2's last date) | at 12 Nov (R3's last date) | what R3 adds |
|:--|--:|:--|:--|:--|
| Rice | 10.6% | harvested | long harvested | little or nothing |
| Maize | 6.0% | harvested | long harvested | little or nothing |
| Bajra | 9.4% | harvested | long harvested | little or nothing |
| Groundnut | 31.0% | mid-lift | essentially complete | **the end of its season** |
| Cotton | 43.0% | ~45% through picking | still picking, ends January | **two more points, and still no endpoint** |

Read that table carefully, because three things fall out of it and they should shape the plan:

1. **The two new dates land precisely where Round 2 was weakest.** Cotton and groundnut are
   74% of the village and carried R2's most incomplete completion factors (0.45 and 0.75).
   The new observations are almost pure signal for exactly those two.
2. **For rice, maize and bajra the "forecast" is retrospective** — their season closed before
   even R2's last acquisition. Nothing in the two new scenes observes their grain fill. Any
   claim that the 6-pass series improves their forecast needs to survive a test that could
   fail. These are also the three crops with zero independent corroboration of their labels
   (§3.1), so error compounds here. **Say this before a judge finds it.**
3. **Cotton's season still is not observed to its end.** Picking runs to January; 12 November
   is perhaps a third of the way through. So cotton is the only crop requiring genuine
   *extrapolation beyond the observation window* — which is the literal definition of the task
   the round set. **Cotton is the round.** It is 43% of area, 47% of plots, the crop with the
   only independently corroborated labels, and the only one where "forecast" is not a
   synonym for "estimate". Budget accordingly.
4. **The two new dates bracket the groundnut lift — which may settle a dispute Round 2 could
   not.** Groundnut is lifted October–November, so 29 October and 12 November sit either side
   of the event for most plots. A field that is genuinely groundnut should show a lifting
   signature in that fortnight: standing canopy replaced by disturbed bare soil, which at
   X-band is a large and directional change. A field mislabelled as groundnut — Orion argues
   14.8 points of our village is exactly that (§3.1) — should not. **This is a test we could
   not run in Round 2 because the season ended before our data did, and no other team has
   framed it.** It is cheap, it is falsifiable, it bears on 31% of the village, and it feeds
   the forecast directly rather than only the label: whatever the outcome, knowing *when* each
   plot's season actually ended is a yield-relevant fact. Design it as a proper test with a
   control — the three cereals, already off-field before 13 October, must show **no** such
   fortnight signature, and if they do, the signature is measuring dew, look-side or harvest
   traffic rather than lifting. If that control fails, discard the test and say so.

A corollary worth stating in the writeup: a "final yield forecast" from a series that ends
mid-picking is a forecast for cotton, a near-complete measurement for groundnut, and a
retrospective reconstruction for the three cereals. **Three different epistemic objects in one
column.** Naming that distinction, and handling each correctly, is the kind of thing the
Plausibility & Defensibility criterion is for. Every other team will ship one undifferentiated
number.

---

# 5. Standing rules — these override default behaviour

1. **Test in depth before adopting anything.** This is the rule the entire post-R2 pass was
   built on and it has paid repeatedly: of six ideas borrowed from other shortlisted teams,
   two would have made the product worse; of my own four Round-3 directions, three were
   rejected by their own tests. Other teams' published claims can be wrong, published papers
   can be about a different objective, and my proposals have been wrong more often than not.
   **Every claim needs a control that could fail. If a test fails its own control, discard the
   test and say so.**
2. **Grade every recommendation.** `OWN` = measured on our data or our metadata, no external
   claim load-bearing. `MECH` = someone else's claim, but the mechanism was independently
   verified. `THEIRS` = rests on an outside assertion, not established for us, not actionable.
   Nothing graded THEIRS may enter a deliverable as established.
3. **Name the kill criterion before running the test.** Write down what result would make you
   abandon the idea, in the file, before the run. Round 2 did this for the Water Cloud Model
   and for repeat-pass coherence, and it is what made those failures informative instead of
   embarrassing.
4. **Report the negatives as prominently as the positives.** Every one of the six shortlisted
   Round 2 writeups shipped failures; one team retracted a published finding. That is the
   scoring function. A documented negative outscores a silent omission.
5. **Round 2 is frozen.** Verify `..\AISEHACK-2.0-T1-R2\results\submission.csv` stays md5
   `89b0e4e2aef63ace4989fc0a44590ee5`. Nothing this round writes into that tree.
6. **Never commit until I explicitly say so.** Stage and report; I review first.
7. **Never add a `Co-Authored-By: Claude` trailer** to any commit, in any project.
8. **Privacy.** If any land-record data is touched, extract the crop column only, report
   aggregate accuracy only, never publish owner names or individual-linked survey numbers.
   Keep `ground_truth_vf12.csv` and any token file gitignored.
9. **Reproducibility from the first line.** Round 1's lesson was an unreconstructable champion.
   Version every intermediate, log every run, never overwrite, avoid near-singular solves in
   anything final.

## 5.1 External data policy for this round

Round 3 explicitly permits any external data. That is *permission*, not a *plan*.

- **Default position: Capella X-band stays the primary source**, and Sentinel-1/Sentinel-2
  stay independent witnesses that never enter a shipped number. This was a real strength in
  Round 2 and it is what keeps our validation non-circular. In Round 2 the guidelines
  *required* Capella primacy; in Round 3 they do not, so the discipline is now a choice we
  make and must defend rather than a rule we obey.
- **Relaxing it is allowed if, and only if, it is argued and tested.** If letting optical or
  C-band into the model measurably improves the forecast, that is legitimate under this
  round's rules — but the cost is real: every witness spent is a validation we can no longer
  perform, and we have no ground truth to fall back on. **Any proposal to promote a witness to
  an input must first name its replacement witness and freeze it.** One team's crop map in
  Round 2 was driven by Sentinel-2 in a SAR challenge, and they had to flag it as an exposure.
- **Fetch full-season Sentinel-1 and Sentinel-2 through harvest (November).** R2's witnesses
  stopped at 13 October and cannot speak to the two new dates at all. A forecast that extends
  past 13 October needs a witness that also extends past it. This is the single most valuable
  data-fetch available and it should be Phase 0 work, not Phase 3.
- **Round 2's "there is no optical" argument does not hold for Round 3's window, and this is
  worth thinking about carefully.** We measured **zero** Sentinel-2 scenes under 20% cloud over
  Sokhda in June, July, August or September 2025 — the best July scene was 92.6% cloud — which
  is why the season witness had to be built from Sentinel-1. But that is a statement about the
  *monsoon*. Post-monsoon Gujarat is the dry season, and the evidence says it is clear: our own
  13 October scene came in at **0.003% cloud**, and another team validated against an
  **18 October** scene. **Round 3's two new acquisitions sit in the one window of the year where
  optical is abundant — and that window is exactly the forecast-critical one**, covering
  groundnut's lift and cotton's early picking. A gap-filled or harmonic NDVI series was listed
  in Round 2 as a cheap untested idea whose first test is a cloud-free scene count; run that
  count for mid-October through November before assuming anything either way. This does not
  make optical an input — see the paragraphs above on what promoting a witness costs — but the
  reflexive "no optical exists here" line from Round 2 must not be carried into Round 3
  unexamined, because for these dates it is probably false.
- **An external-data census of all five competitors' Round 2 code found that not one of them
  used Sentinel-1.** Their pipelines touch Sentinel-2, Copernicus DEM, NASA POWER, Open-Meteo
  and the APY/advance-estimate tables — that is the entire field. We are the only team of six
  with a C-band witness and the only one with a season-integrated one. Two consequences:
  **no data edge is available by imitating this field**, so a new-source advantage has to come
  from something none of the six touched; and the asset we already hold is larger than anything
  visible to copy. Extending it through November compounds it.
- **Any other auxiliary source is in scope**, subject to the resolution-ceiling rule below.
- **The resolution ceiling, measured on our own farms.** The most any covariate constant within
  a cell of side L can explain of within-crop variation: 100 m → 0.685; 250 m → 0.226;
  500 m → 0.125; 1 km → 0.041; 5 km → 0.015; 11 km and beyond → **0.000**. (Our 250 m figure
  reproduces another team's exactly, from a different pipeline.) **Anything on a cell larger
  than the 4.1 × 3.6 km village is arithmetically incapable of ranking farms inside it.** Price
  every proposed source against this table *before* fetching it. Coarse data keeps exactly two
  legitimate uses, both about level or timing rather than ranking: **temporal context** (a rain
  event at the overpass hour) and **aggregate anchors** (district yield, never asked to rank).

---

# 6. Phase 0 — set up and verify (do this first)

1. Extract the archive into the round folder. Verify the 41 files, then confirm the four
   shared scenes against Round 2 by md5 and record it. Confirm the two new scenes are
   readable.
2. Initialise the round folder: a git repo, a results tree, a run ledger, and a
   `common.py`-equivalent that centralises paths, dates and guards. Carry forward the two
   environment guards that cost real time in Round 2: `os.environ.pop("PROJ_LIB", None)`
   before any rasterio/pyproj import, and the both-folder-and-basename SLC resolution guard
   with an assertion that exactly one file matches per date. Python is `py -3.12`.
   **Parameterise the dates and the AOI from the first line.** Round 2 measured its own
   portability debt at the end and found 20 of 33 files hardcoding the acquisition dates and 12
   of 33 hardcoding the village name — which turned "run this on six dates instead of four" into
   a refactor rather than a config change. We are writing a six-date pipeline from scratch
   today; the date list belongs in one place, read from the data where possible, and nothing
   downstream should name a date literal.
3. Write the self-check *before* the processing code. In Round 2 the self-check caught the
   duplicate-SLC trap on the first run, before any pixel was read.
4. Start the two external fetches immediately, because they have latency and everything else
   is compute-bound: full-season Sentinel-1 RTC and Sentinel-2 L2A through at least 30
   November 2025 (Microsoft Planetary Computer, anonymous SAS, open licence), and hourly
   precipitation at all six overpass timestamps (Open-Meteo archive, free, no key).
5. Resolve open items A1–A4 from §1.3.
6. Search for **Gujarat kharif 2025-26 yield statistics**. Round 2 anchored on the 2022–23
   district APY table because nothing closer existed. It is now late 2026: Gujarat's First,
   Second and Third Advance Estimates for kharif 2025 — the exact season we observe — should
   be published. **A season-matched, year-matched anchor for the year in question would be a
   material upgrade over anything any team used in Round 2**, and it lands squarely on both
   Plausibility (25) and Creativity's "sensible use of external data". Check the Directorate
   of Agriculture Gujarat, data.gov.in, the Ministry of Agriculture advance estimates series,
   and the district-wise season-wise APY resource Round 2 used
   (`35be999b-0208-4354-b557-f6ca9a5355de`, 246,091 records, 1997–2012, with Kharif / Rabi /
   Summer / Whole Year as separate rows; the API is paged and a 1000-row request times out
   where 250 works).

   Two further sources were identified in Round 2 and **never opened**, both directly on this
   question. `data.gov.in` resource `66e33662-6f0b-4bd9-8771-5a33f8ff6cdd` — *Area, Production
   and Yield of Major crops of Gujarat State*, described as **"season wise and year wise"**,
   which is precisely the annual-versus-kharif axis our bajra defect lies on. It was blocked
   only because the shared public demo key returns HTTP 429 and a free personal key was needed
   — **and we now have one**, in `~/.config/aisehack/` outside the repo. (That key is among
   three that were pasted into a chat transcript and are due for rotation; rotate before use,
   and never print it.) The second is the **ICRISAT District Level Database**, 560 districts
   with a kharif/rabi split, which is the multi-year companion that would fix the thin-base
   instability that made our bajra and groundnut estimates noisy in the first place.

7. **Inventory and verify the inherited per-farm assets (§3.7).** Copy the ones we will use
   into the Round 3 tree — reading across from the frozen Round 2 folder at analysis time is how
   a frozen tree stops being frozen — join each on `farm_id`, confirm 966 rows and an exact key
   match, and spot-check a few values against their source document. Anything that fails the
   join gets dropped and noted, not patched. Do the same for the competitor tables, which are
   third-party files and deserve the same scepticism Round 2 applied before trusting a
   competitor submission: verify the join reproduces a figure the team published themselves.

**Phase 0 gate:** the six scenes resolve correctly, the shared four are confirmed identical,
the external fetches are running or their blockers are documented, the inherited per-farm
assets are joined and verified or explicitly dropped, and A1–A4 are answered or recorded as
unanswerable.

---

# 7. Phase 1 — comprehensive EDA

Not a tour of the data. Every item below exists to answer a question that changes what we
build. Write findings as you go, each with what it changes.

## 7.1 Characterise the two new scenes against the four known ones

- Reproduce the calibration check on all six: form β⁰ under both SF and SF² and compare the
  darkest percentiles against each scene's declared `nesz_peak`. Round 2 got 0.35 dB mean
  absolute error across four scenes under SF². **Confirm the new two behave the same** — if
  they do not, that is a finding about the products, not about our formula.
- Per-pixel incidence from the orbit state vectors for the new scenes, validated against the
  vendor's annotated centre incidence. R2 achieved 0.006° agreement on four dates; the same
  method should hold. This is a cheap, checkable Technical Soundness exhibit.
- **The look-side question.** 29 October is right-looking. Quantify what that does: compare
  persistent stable targets (built-up, water, bare) across look sides against the same targets
  across same-side date pairs. Is the difference a constant offset, a per-target-orientation
  effect, or negligible? **This determines whether 29 Oct can enter a temporal difference at
  all**, and it is a question no other team is likely to have asked.
- **The diurnal question.** 01:37 IST and 19:22 IST against four morning/midday passes. Test
  whether the new dates carry a scene-wide wetness signature: compare stable dry targets
  (built-up, roads) — which should not respond to dew — against vegetated and bare-soil
  targets, which should. Cross-check with the Open-Meteo hourly humidity and precipitation at
  each overpass. If dew is present it must be handled or bounded, because otherwise it
  masquerades as late-season canopy change on exactly the two dates the forecast leans on.
- **The 29 Oct ↔ 12 Nov pair.** 0.094° apart in incidence, 14 days apart, opposite look sides.
  Test whether it is usable as a matched pair for change detection and whether repeat-pass
  coherence is recoverable. R2's coherence attempt on the 56-day Jun19↔Aug14 pair was
  uninformative because the stable-scatterer control never cleared its own bias floor — reuse
  that harness and its three controls (SELF, NULL, STABLE against a like-for-like floor), and
  respect the lesson that scoring bright pixels against an all-pixel floor manufactures an
  excess out of pure statistics.

## 7.2 The six-date trajectory, per plot and per crop

- Per-farm feature extraction on the full stack, with the negative-buffer ladder so no plot is
  ever dropped and every fallback is counted. Coverage matters more than in R2: Aggregation is
  now 15 points.
- **Re-measure coverage on the new dates.** R2 found missingness clustered along a north-west
  swath edge — 29 fully missing after our own geocoding — not random. The new scenes have
  different swath geometry, and 29 Oct's is mirrored. Coverage per plot per date is a table
  the writeup needs.
- Plot the six-point trajectory per crop, area-weighted and with dispersion. **Look at it.**
  R2's single most valuable prose correction came from plotting a trajectory and discovering
  the written physical story was wrong while the feature was right. Do not skip the looking.
- Where do the two new dates sit relative to the R2 four? Does cotton separate further from
  everything else as the cereals go to bare soil? Does groundnut's lift show as a step? The
  crop calendar in §4 makes specific predictions — **write them down before you plot**, then
  report which held.
- **Run the groundnut-lift test set out in §4, consequence 4**, with the three cereals as the
  control that must show no fortnight signature. It is the one experiment available this round
  that could speak to a share dispute covering 31% of the village, and its control can kill it.
- **Measure each farm's margin above the declared noise floor, per date.** `nesz_peak` is
  annotated per scene; compute the fraction of each plot's pixels within a stated margin of it,
  on all six dates. This is the input a NESZ quality gate (§3.6) needs, and the late-season
  dates are where it will bite — dark, smooth, harvested fields are exactly the condition that
  puts a plot mean into the noise. Report the per-date distribution before deciding any
  threshold.
- Season integrals, growth rates, and senescence slopes now have six points instead of four.
  Quantify what that buys: is a curve fit identifiable at n=6 that was not at n=4? What are the
  degrees of freedom against the parameters any candidate model wants?

## 7.3 Sanity infrastructure, built early because it is worth 25 points

- Port forward, or rebuild, the failure-mode regression suite. Each check is one assertion
  corresponding to a defect that survived internal consistency checking in a competent
  pipeline: a geoid error, a 1-based/0-based join, a calibration double-correction, an
  SNR-proxy artefact, a speckle-filter-induced correlation, a unit inhomogeneity, a degenerate
  parcel defining a spatial grid. Round 2's suite is at `..\AISEHACK-2.0-T1-R2\post-r2\tests_regression.py`.
- **Cross-implementation check on our own radiometry — do this early, it is cheap and it is the
  only external check that exists.** Project Orion published per-farm γ⁰ in dB for all four
  shared dates (§3.7). Our rebuilt pipeline processes the same byte-identical scenes over the
  same byte-identical polygons, so per-date farm-to-farm agreement against their column is a
  genuine test of our geocoding, calibration and extraction chain by an independent
  implementation. Expect a constant dB offset from the calibration convention and ignore it;
  the test is the correlation and the residual structure. **A common-mode error in our own chain
  is invisible to every internal consistency check** — that is how our SF error and another
  team's geoid error both survived competent pipelines — and this is the only instrument we have
  that can see one. If agreement is poor on a date, find out why before building anything on
  top of it.
- **Add the silent-no-op class**, which none of those checks covers. The known instance: GDAL
  accepts `METHOD='GCP_TPS'` and **silently ignores it** — the key that works is
  `SRC_METHOD='GCP_TPS'`. A parameter that is accepted and does nothing produces output that
  passes every consistency check while the intended operation never ran. If any option is set
  that is supposed to change a result, assert that the result actually changed.
- A degenerate-output assertion: a collapsed forecast, a single-crop map, or a constant column
  must fail a check rather than pass a schema.
- Decide the sanity-check battery for the forecast itself now, while there is no result to be
  attached to. At minimum: per-crop plausible yield ranges from published statistics; village
  production reconciled against a district anchor; forecast-vs-R2-yield-to-date consistency
  (the forecast must exceed the to-date estimate for crops still standing, and should roughly
  equal it for crops already harvested — **this is a strong internal consistency test that
  costs nothing and that no other team can run, because only we have a Round 2 to compare
  against**); and cross-crop ordering against agronomic expectation.
- **Use the Round 2 cross-team production spread as an external plausibility band.** Five
  teams' village totals over the same 447.5 ha were Megalodon **578 t**, ours **595 t**, Orion
  **1,002 t**, Coding Bits **1,268 t** — a 2.1× spread, most of it driven by crop mix rather
  than by the yield model. (A sixth team's column sums to 21,566 t, ~48 t/ha, which is a unit
  problem rather than a method difference and must be excluded from any cross-team statistic.)
  We and Megalodon agreed within 3% on independent pipelines, both anchoring on district
  statistics discounted by crop progress. That band is a genuine external reference point for
  a *final* forecast — which should land **above** the to-date figures, by roughly the
  un-harvested fraction — and being able to say where we sit in it, and why, is worth more
  than a bare number. Ours is the only team that can compare its own two rounds.

**Phase 1 gate:** a written EDA document with every finding tagged by what it changes, the
predictions-before-plots recorded with which held, and a list of the specific open questions
the research phase must answer.

---

# 8. Phase 2 — deep research

This is the phase I most want done properly. Go wide and go deep: web search, recent papers,
review articles, the references inside those papers, government and agency documentation,
and the technical documentation of any product we might use. Prefer primary sources. Prefer
recent work but chase the foundational citations that recent work rests on. **For every source,
record what it claims, what it measured that on, and whether its objective is the same as
ours** — Round 2 lost time twice to importing a result whose objective was subtly different,
and one of those was an active-learning citation that turned out to be about selecting
training labels when our problem was measuring a frozen map.

Organise the output by research question, not by paper. For each question: what the literature
establishes, how confidently, on what data, what it predicts *for our specific configuration*
(X-band, HH, single-pol, 6 irregular dates, 0.27 ha median plots, smallholder kharif, no
labels), and what test on our data would confirm or kill it.

## R-A. The forecast target, and the agronomy that defines it

- Gujarat / Vadodara kharif 2025 crop calendar per crop: sowing windows, phenological stage
  dates, harvest windows, and how variable those are between plots in one village. We need this
  to say what "final yield" *means* per crop at each of our six acquisition dates.
- Cotton picking dynamics: how yield accumulates across pickings, what fraction is in by
  mid-November, and what determines the remainder. This is the crux of the round.
- Groundnut pod fill and lifting: when is yield determined versus when is it harvested?
- The 2025 monsoon in Gujarat specifically: onset, the July deficit and its recovery, August
  and September surpluses, any late-season events. R2 established the broad picture; refine it
  to the district and to the dates.
- **Kharif 2025-26 official yield statistics** — the advance-estimates series, district level
  if it exists, state level otherwise. Note the units convention for every crop, and check
  every crop for a second cropping season before using any annual mean (this is exactly the
  test that caught our bajra anchor).
- **Where Vadodara sits within Gujarat, per crop.** A competitor's code comments assert that
  Vadodara ranks **1st in Gujarat for maize yield and 2nd for cotton yield** — unverified, and
  worth verifying, because it is a direct constraint on anchor plausibility. If true, a
  Vadodara anchor for those two crops should sit near the *top* of the state range, not at its
  mean, and an anchor that lands mid-range is evidence of a sourcing problem. This is a cheap,
  checkable sanity test on the single number that carries the level of the whole forecast.

## R-B. What X-band HH can and cannot retrieve

- X-band saturation with biomass and LAI, and at what levels. The known result is that X-band
  correlates poorly with total biomass and saturates early — which is *why* R2 built the index
  on structure, moisture and temporal change rather than on brightness.
- The Water Cloud Model at X-band HH: published coefficient sets, the crops they were fitted
  on, the reported inversion error, and the conditions under which the inversion is
  ill-posed. **We have a working WCM inversion from Round 2 that was rejected as a health
  component for a specific measured reason** — the observed August/June ratio sat below the
  model's floor at any monsoon-plausible soil moisture, and the discrepancy was the same size
  as our own calibration uncertainty. With the calibration fixed to SF², **that rejection
  should be re-tested**: the premise may have changed. This is one of the highest-value
  re-openings available and it should be prioritised accordingly. Note also the model's
  non-monotonicity — backscatter dips before it climbs, so the inversion is two-to-one below a
  turning point.
- X-band and panicle/reproductive-organ biomass: the published claim is that X-band correlates
  best with the grain-bearing structure, which is a physical justification for an X-band yield
  proxy rather than a merely correlational one. Chase how well established this is, on which
  crops, at which polarisation and incidence.
- Cotton specifically at X-band: boll development, defoliation, and what the picking sequence
  does to backscatter. Much thinner literature than rice — find what exists.
- Azimuthal/row-direction anisotropy in SAR backscatter over row crops, and what look-side
  reversal does. Needed for §7.1.
- Dew and diurnal moisture effects on X-band backscatter — magnitude, timing, and how the
  literature handles night acquisitions.

## R-C. Yield forecasting methodology without labels — the core question

This determines the shape of the entire submission. Survey the families honestly, then rank
them **for our configuration**, not in the abstract.

- **Semi-empirical crop growth models driven by remote sensing** — the SAFY family and its
  water-balance variants, and comparable light-use-efficiency approaches. These are designed
  precisely for "estimate yield from a satellite-observed growth curve plus meteorology, with
  few or no field measurements", which is our problem statement almost verbatim. Establish what
  they need as input, whether a SAR-derived proxy can substitute for the optical GAI/LAI they
  normally ingest, how many observations they need, and what accuracy is reported.
- **Full process-based crop models with data assimilation** — the DSSAT / APSIM / AquaCrop /
  WOFOST family, and the assimilation strategies (forcing, recalibration, sequential filters,
  variational). Establish the honest cost: parameterisation burden, the number of inputs we do
  not have, and whether a defensible calibration is even possible in the time available.
  **A model we cannot parameterise defensibly is worse than a simpler one we can** — and the
  rubric rewards defensibility over sophistication at 25 points to 15.
- **Growth-curve extrapolation and phenology-metric regression** — fitting a curve to the
  observed series and using its parameters (integral, peak, rate, duration) as yield
  predictors. What functional forms are used, what they need in terms of observation count and
  timing, and what they predict when the series ends before the season does (our cotton case).
- **The dasymetric / anchor-plus-modifier approach we used in Round 2** — an aggregate yield
  level from statistics, disaggregated by a remotely sensed modifier. Establish where this sits
  in the literature, what it is called, its known limitations, and what the published
  alternatives to it are. Be genuinely critical of our own incumbent method here: its weakness
  is that the anchor carries the level and the SAR carries only the spread, so most of the
  answer comes from a statistic rather than from the imagery — and a judge can ask what the
  SAR actually contributed. **Quantify that.**

  One measured result belongs in this decision, because it is the strongest evidence we have
  that the incumbent's problem is not the yield model. Across teams our Round 2 yield column
  correlated *negatively* with three of five others — the only team in that position. The
  obvious explanation (our bajra anchor) was tested and **rejected**: correcting it moved the
  cross-team correlations by a mean of −0.001. The real cause is that yield is 82% explained by
  the crop label and the crop maps agree at chance, so the yield columns inherit the label
  disagreement. Restricting to farms where we and they assign the *same* crop separates the
  two cleanly:

  | vs team | all farms | labels agree | n |
  |:--|--:|--:|--:|
  | Megalodon | +0.000 | **+0.678** | 321 |
  | DeepThinkers | −0.069 | **+0.751** | 166 |
  | Coding Bits | −0.266 | +0.019 | 351 |
  | Orion | −0.313 | −0.173 | 180 |
  | 8bit | −0.315 | −0.262 | 292 |
  | | | **mean +0.395** | |

  Conditioned on agreeing about the crop, our yield agrees strongly with the two teams whose
  method most resembles ours — both of which anchor on district statistics discounted by crop
  progress, exactly as we do. **Our yield column is a good measurement carried on a bad
  label.** Two things follow for Round 3: reporting yield agreement *conditioned on label
  agreement* is a legitimate and strong defensibility exhibit; and the structural fix is to let
  the SAR carry more of the variance so η² falls from 0.820 — two other teams reached 0.474 and
  0.499, so it is achievable.
- **Unsupervised and self-supervised approaches** at n=966 with 6 dates. Round 2 priced this
  out as too small for representation learning to beat a designed physical feature set, and
  documented the reasoning. Re-check whether the extra dates change the arithmetic; expect not,
  but the check is cheap and the negative is reportable.
- **Hybrid designs** — a physical model producing the level with a learned or statistical
  residual, or an ensemble across method families with the spread reported as uncertainty.
  Ensembling across genuinely different method families is one of the few honest routes to an
  uncertainty estimate when there is no ground truth.

## R-D. Sparse irregular time series

Six acquisitions, irregularly spaced, spanning 6 June to 12 November, with a 56-day gap in
the middle and two clustered at the end. What does the literature say about phenology
extraction and curve fitting at this sampling density? What is identifiable and what is not?
What are the standard interpolation or gap-filling approaches and what do they assume? Is
there a principled way to combine a dense C-band series (which we can fetch, and which is
cloud-immune) with a sparse X-band one *as a witness or as a temporal scaffold* without making
C-band the primary source?

## R-E. Uncertainty and validation without ground truth

This is where 25 rubric points live and where the round is most winnable.

- Standard approaches to calibrated uncertainty with no labels. Round 2 built a split-half
  sampling-noise model that predicted its own noise to within 3.4% with no tuning — and then
  showed that noise is only 15.9% of between-farm signal and does not predict disagreement
  with a withheld sensor. So the sampling term is calibrated but not limiting; the interesting
  uncertainty is structural.
- Conformal prediction and distribution-free intervals — what do they need, and is any variant
  usable without labelled calibration data?
- Cross-scale validation: forecast aggregated to village against a district statistic; forecast
  against independent sensor phenology; forecast against the previous round's yield-to-date.
- Sensitivity and ablation as evidence: what is the standard for showing a result is not an
  artefact of a hyperparameter, and what did the six shortlisted teams actually do?
- Spatial hold-out protocols. Round 2 adopted this as a method after a competitor demonstrated
  it, and it promptly overturned one of our own published claims. Use it for anything fitted.

## R-F. Aggregation, which is now 15 points

- Correct practice for aggregating plot-level yield to an area total: production as
  `Σ(yield × area)`, area-weighted means, and the handling of plots with missing or imputed
  values. State the rule and its edge cases.
- Uncertainty propagation from plot to village, including the spatial correlation between
  neighbouring plots — Moran's I on our layers is positive and significant, so treating plots
  as independent will understate the village-level interval. Find the standard treatment.
- What is the right denominator? Our 966 digitised plots total 447.5 ha, while the village's
  cropped area is ~690.9 ha and the village polygon is 1174.1 ha. A village-level total over
  plots is not a village total over the village. **Say which one we are reporting and why**,
  and consider reporting both with the gap explained. This is a defensibility question, not an
  arithmetic one, and it is exactly the sort of thing a panel notices.
- Sub-village reporting: with one village, the required table is one row and carries no spatial
  information. A fixed grid of zones with per-zone aggregates is cheap and shows within-village
  variation that a single row hides. One team did this in Round 2 and found 32 points of health
  spread behind their single number.
- **Two worked examples of this exact deliverable already exist** (§3.7): Orion's
  `village_summary.csv` — per crop, with area-weighted health and yield, production, and a
  confidence share — and 8bit's, on a different per-crop schema, plus Orion's 46-zone
  `zone_summary.csv`. Read both before designing ours. They are not a standard to copy, but a
  15-point criterion is not the place to invent a table format from scratch when two shortlisted
  teams' formats are on disk. Note what each *omits*: neither carries an uncertainty column,
  which is where ours can be better rather than merely different.

## R-G. The competitive field

We have all five other teams' Round 2 writeups, notebooks and submissions at
`..\AISEHACK-2.0-T1-R2\post-r2\writeups_submissions\`. Their Round 2 methods predict their
Round 3 methods. Work out what each is likely to do with two extra dates, where the field will
converge, and where we can be the only team with a given result. **Convergent validity is
evidence and lone dissent is a defect** — in Round 2 one of our lone positions was corroborated
by an independent team's own figures to 0.25 pp, and the other turned out to be our bug. Know
which is which before Goa.

Their **notebooks and methodology PDFs** — 555,246 characters, separate from the writeups —
were mined in Round 2; the results are in `post-r2/DELIVERABLE_MINING.md`. Read it rather than
re-mining, and carry its operating principle forward: **a writeup is an argument, a notebook is
the evidence, and code preserves the failures that prose omits.** That pass produced one
withdrawn recommendation of ours, one silent-no-op trap, one live threat to our largest design
choice, one capability gap, two untested datasets, and the finding that nobody used Sentinel-1.
It also turned up how the strongest teams annotate their own doubt — an optimum sitting at the
edge of a sweep grid, flagged rather than adopted; a weight annotated *"PHYSICS PRIOR —
deliberately not the sweep's argmax"*; a bare *"did not replicate, reported anyway."* That is
the register the panel rewarded, and it is worth matching in our own documentation.

Do not re-read the five writeups from scratch. They were exhausted across twelve sections of
the competitor analysis; a further pass produces restatement, not information. The useful
question now is forward-looking: **what does each team do with two extra dates**, given the
method they already committed to — and specifically, which of them can say anything about
cotton beyond 13 October, which is where this round is decided.

## R-H. Presentation

Ten minutes in front of a panel is a different artefact from a written report. Find what makes
a technical presentation land in that format: how many claims fit, how failures are best
presented, what a single slide can carry. Round 2's evidence says the most persuasive devices
in the field were a decile-trend plot and a validation table where each row states what it
*establishes* rather than what it measures.

Two concrete references are already on disk: `writeups_submissions/8_bits/figures.zip` and the
`deep_thinkers/*.png` set are competitors' actual delivered gallery figures, and our own Round 2
gallery is at `..\AISEHACK-2.0-T1-R2\results\figures\`. One Round 2 lesson about figures is
worth repeating because it took four rounds of rework to learn: **render every figure, open it,
and look at it**, then re-cut until it reads in two seconds. Doing that found three real defects
and one substantive error — a wrong physical explanation attached to a correct feature, which no
validation number would ever have caught, because every metric passed identically either way.
**The figure was the check on the prose.** Budget time for the looking, not just the plotting.

**Phase 2 gate:** a research document organised by question, every claim graded OWN/MECH/
THEIRS, every candidate method carrying what it needs and what would kill it, and an explicit
shortlist with a recommendation.

---

# 9. Phase 3 — the plan, and the task list

Synthesise Phases 1 and 2 into a plan I can approve. It must contain:

1. **A recommended method, with the two strongest alternatives and why they lost.** Name the
   evidence for each. If the recommendation is a hybrid, say what each component contributes
   and how they are combined.
2. **The forecast's structure, per crop**, honouring §4: what is genuinely forecast, what is
   measured, what is reconstructed, and how the deliverable represents three different
   epistemic objects in one column.
3. **The defensibility battery** — the specific sanity checks, with what each one would show if
   it failed. This is 25 points; specify it like a deliverable.
4. **The aggregation rule**, stated precisely, with its edge cases and its uncertainty
   treatment. 15 points.
5. **An explicit decision on each freeze-dividend item (§3.5) and each capability gap (§3.6)** —
   ship, test first, or drop, with a reason. These are the cheapest points available in the
   round because the research behind them is already done, and the failure mode is that they
   get forgotten under the pressure of building something new. Say which are in the submittable
   baseline and which are stretch.
6. **A schedule against the real deadline.** Today is 30 August. The submission closes 3
   September end of day and the finals run 2–3 September in person, so the working days are
   **30, 31 August and 1 September**, with 2–3 September consumed by travel and presenting.
   The PPT and the writeup must therefore be finished by the end of **1 September**, not the
   3rd. Plan for a complete, valid, submittable deliverable existing by the end of **31
   August** — Round 1's lesson was an unreconstructable champion, and Round 2's was that a
   submittable gate early beats a better model late. Everything after that gate is improvement
   on something already shippable.
7. **A task list** in dependency order, each task with its owner phase, its cost estimate, its
   kill criterion, and what it blocks.
8. **What we will deliberately not do**, and why. The closed list in §3.2 plus anything Phase 2
   prices out.
9. **The risk register**: what could still go wrong, what the early warning is, and what the
   fallback is.

**Then stop and report.** Give me the plan, the ranked reasoning, and the open questions you
could not settle. Do not start building until I say so.

---

# 10. How I want you to work

- Read the Round 2 material yourself. Do not spawn subagents for it and do not ask me to
  summarise it.
- Prefer measuring to arguing. Where a question can be settled by running code on our own
  data, run the code — that is what "OWN" evidence means and it is worth more than any
  citation.
- When you find something that contradicts what I have told you here, say so directly and show
  the measurement. Round 2's most valuable moments were the ones where a test overturned our
  own published claim.
- Keep a running research log in the round folder: every move, what it returned, and what it
  changes. Append-only.
- If a phase turns up something that reorders the plan, reorder the plan and say why rather
  than following a stale sequence.
- Flag anything with real latency the moment you find it, so it can run in the background.
