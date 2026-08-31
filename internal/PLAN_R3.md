# Round 3 plan — for approval

Synthesis of Phase 1 (`RESEARCH_LOG.md`, P1-1…P1-9) and Phase 2 (`RESEARCH_PHASE2.md`,
R-A…R-H + addendum). Nothing here is built yet.

**★ The schedule premise has changed and it changes everything below.** §9 assumes the
submission closes *3 September end of day*. Phase 0 (P0-10) measured the Kaggle deadline as
**2026-09-03 07:00 UTC = 12:30 IST**, verified against R2's, which converts to exactly midnight
IST. **We lose the whole of 3 September**, and 3 September is the second day of the Goa finals.
The plan therefore treats **1 September end of day as the hard finish for everything**, with
2–3 September consumed by travel, presenting and a 12:30 submission we should have made two days
earlier. *User action: confirm the wording with the host.*

---

# 1. Recommended method

## The recommendation: **anchor-plus-modifier, with the modifier doing far more work**

Three layers, and each is answerable to a separate question a judge can ask.

| layer | what it does | what it contributes |
|:--|:--|:--|
| **Level** — district/state anchor per crop, adjusted for 2025-26 | sets t/ha per crop | the absolute level, which no label-free method can get from imagery alone |
| **Modifier** — per-plot index from the six-date X-band stack | distributes the level across plots | the spatial variance — **the thing we are actually being scored on** |
| **Uncertainty** — ensemble spread across modifier variants + a village-level conformal interval | states what we do not know | 25 rubric points |

**Why this and not something more ambitious.** Two working days remain. The measured case
(§8, R2's `OWN` result) is that **our yield column is a good measurement carried on a bad label**:
conditioned on label agreement our yield correlates **+0.678** with Megalodon and **+0.751** with
DeepThinkers, mean **+0.395**, while unconditioned it goes negative. The method is not the defect.
**The defect is that the crop label explains η² = 0.820 of yield variance, so the SAR contributes
only 0.180.** Two other teams reached 0.474 and 0.499. **The single highest-value change available
is to move that number**, and that is a modifier problem, not a model-family problem.

**How the components combine.** Production = Σ(yield × area). Per plot,
`yield_p = anchor(crop_p) × modifier_p`, with the modifier normalised **within crop** so that the
area-weighted mean modifier is 1.0 by construction — which makes the anchor mean the thing it
claims to be, and makes the modifier's contribution auditable as a single number (the variance it
adds). We report that number.

## Alternative 1, and why it lost: **SAFY-family semi-empirical growth model**

`MECH`, and it was the first-pass recommendation. Designed for exactly our problem statement —
*"calibrate a simple crop model without resorting to in situ data"* — with SAR-derived GAI
established practice (SAFY-WB driven by Sentinel-1), and double-logistic interpolation for
missing acquisitions that would cover our 56-day mid-season gap. P1-7 makes its 4-parameter free
set newly identifiable at n=6 (2 residual df, against 0 at n=4).

**Why it lost: two reasons, one of substance and one of schedule.**

- **Substance.** SAFY ingests a **GAI/LAI** time series. B-1 establishes that **X-band correlates
  poorly with LAI and biomass** and saturates at very low biomass — LAI belongs to C-band, biomass
  to L-band. Driving a light-use-efficiency model with a proxy the physics says is weak is
  precisely the "importing a result whose objective was subtly different" failure §8 warns about.
- **Schedule.** Even if the proxy worked, 4 weakly-identified parameters × 5 crops fitted and
  validated in two days, with no ground truth, is not a defensible calibration.

**It is not dead — it is demoted to a gated stretch.** Test **T1** decides. If an X-band feature
does serve as a GAI proxy, a SAFY modifier for cotton alone (the crop with a real forecast
problem) becomes worth the day. If T1 fails, we have a reportable negative that cost four hours.

## Alternative 2, and why it lost: **process-based model with data assimilation**

DSSAT / APSIM / AquaCrop / WOFOST with sequential or variational assimilation. `MECH`, well
established, better than anything above **where it can be parameterised**.

**Why it lost: parameterisation cost, and the rubric's own arithmetic.** It needs cultivar
coefficients, soil hydraulic profiles, and per-plot management — sowing date, density, irrigation,
fertiliser — for **five crops across 966 smallholder plots with no ground truth and no agronomic
survey**. Every one of those would be invented. **Plausibility & Defensibility is 25 points;
Innovation is 15.** A model we cannot parameterise defensibly is worse than a simpler one we can.

**Ship the rejection as an exhibit.** Naming a more sophisticated method, and stating in one line
why it was rejected on defensibility rather than on capability, is itself worth marks.

---

# 2. The forecast's structure, per crop — three epistemic objects in one column

§4's central point, made operational. **This is the differentiator: every other team will ship one
undifferentiated number.**

| crop | area | 12 Nov status | **what the number is** | how it is produced |
|:--|--:|:--|:--|:--|
| **Cotton** | 43.0% | ~**28%** of yield picked (ADD-2); ~72% still on the plant | **A genuine FORECAST** — the only one | trajectory shape to 13 Oct + external picking constraint. **Not** 12 Nov brightness |
| **Groundnut** | 31.0% | yield determined ~late Oct (135 DAS); lifting done or nearly | **A near-complete MEASUREMENT** | full six-date trajectory; the determining event is inside our window |
| **Rice / Maize / Bajra** | 26.0% | long harvested | **A RETROSPECTIVE RECONSTRUCTION** | trajectory to 13 Oct only; the two new dates observe bare soil |

**Three consequences we must act on, not just describe.**

1. **Cotton cannot lean on the last date.** B-3: cotton backscatter genuinely falls at senescence
   (leaf drop is structural, and defoliation before picking is deliberate), and at X-band —
   earlier saturation, upper-canopy sampling — convergence toward the soil signal comes sooner.
   P1-6a measured exactly that: the cotton-minus-cereal gap **shrinks to +0.97 dB** by 12 November
   while cotton is still standing. **X-band brightness stops carrying cotton canopy information
   at the moment picking begins**, which is the window the forecast must cross. Use the trajectory
   *shape* while it was informative, and let A-1/ADD-2 carry the remaining season.
2. **Groundnut's yield organ is invisible to us, and we must say so.** B-2 is the strongest
   physical argument we have — panicle biomass correlates *best* with X-band σ⁰, because the short
   wavelength samples the upper, grain-bearing layer. That argument transfers to cotton bolls and
   **dies on groundnut, whose pods are underground.** For 31% of the village the X-band signal is
   a proxy for canopy state and lifting date, never for the harvested organ. **Stating this
   asymmetry is more valuable than hiding it**, and no other team is positioned to state it.
3. **For the three cereals, claiming the new dates help is a claim that can fail.** Say plainly
   that R3 adds nothing to their forecast, and that they are also the three crops with **zero
   independent label corroboration** (§3.1), so error compounds there. **Say it before a judge
   finds it.**

**Schema.** Carry R2's forward — `village_id, farm_id, crop_type, health_index,
yield_forecast_t_ha` — with `village_id = 1` (not the shapefile's 22) and yield in **t/ha**, plus
the per-crop and village aggregation tables. Both R2 guards stay: `assert max < 25.0` and the
`village_id` assertion. **Open: the host template.** A1 established no template exists on Kaggle
and none existed in R2 either; in R2 the host supplied one through another channel and it caught a
1000× unit error. *User action: check that channel.*

---

# 3. The defensibility battery — 25 points, specified as a deliverable

Every row states **what a failure would mean**, which is the point. Thresholds are fixed **now**,
before there is a number to defend.

## 3a. Already built and passing (Phase 1)

| check | status | a failure would mean |
|:--|:--|:--|
| `nesz_peak` adjudication in β⁰, six scenes | ✔ +0.88 to +2.84 dB, all positive | calibration wrong, or a double-correction |
| incidence vs vendor annotation, six scenes | ✔ ≤0.0075° | geoid/ellipsoid/ECEF error |
| **cross-implementation vs Orion**, four dates | ✔ r 0.89–0.98, ~1 dB absolute, diagonal beats off-diagonal by ≥0.255 | **a common-mode error invisible to every internal check** |
| regression suite, 11 assertions | ✔ 11/11, incl. silent-no-op and degenerate-output | a defect class that survived a competent pipeline |
| out-of-sample stable-target design | ✔ selection bias measured at +2.59 dB | a manufactured finding (it nearly was one) |

## 3b. To build, in priority order

| # | check | threshold, fixed now | a failure would mean |
|:--|:--|:--|:--|
| **D1** | **Forecast vs R2 yield-to-date**, per crop | cotton ratio **≈2.2** (1/0.45, ADD-2); three cereals **≈1.0**; every crop **≥1.0** | our two rounds are mutually inconsistent — **only we can run this** |
| **D2** | Village production vs district anchor | within the R2 cross-team band (578–1268 t over 447.5 ha), and we say where we sit and why | the level is wrong, or the crop mix is |
| **D3** | Per-crop yield inside published ranges | each crop within its statistical range, cotton in **lint** | a unit or convention error — the class that made cotton 2.9× too small in R2 |
| **D4** | **Non-circular label test** (Orion's method) | regress the witness on the ranking axis that produced the labels; test the group difference on the **residual** | the labels carry no information beyond the axis that made them — **P1-5 proved every naive label test is circular** |
| **D5** | Cross-crop ordering vs agronomy | cotton > groundnut > cereals in yield-to-date terms | the crop map or the completion model is wrong |
| **D6** | Ensemble spread across modifier variants | spread reported, not suppressed | a single variant is being presented as certainty |
| **D7** | Spatial hold-out for anything fitted | held-out performance reported beside in-sample | overfitting — in R2 this overturned one of our own published claims |
| **D8** | Degenerate-output assertions | forecast not constant, >20 distinct values, ≥3 crops | a collapsed model that passes a schema check |

## 3c. The contamination ledger — reserved-scene discipline, done honestly

§3.6 asks for a reserved scene. **We cannot produce a clean one and should say so rather than
claim one.** Scenes that set design decisions this round: **29 Oct** (look side P1-3a, wetness
P1-3c), **12 Nov** (same pair), **13 Oct** (R2 used it as headline witness *and* corrected the
completion-term sign against it — never accounted for). **What we will do instead:** publish the
ledger of which scene set which decision, and reserve the **S2 12 November scene (0.001% cloud,
same-day with our final Capella acquisition)** as a witness that has entered no design decision.
Before citing Orion's reserved-scene discipline as a model, note their own notebook says *"no
reserved scene cleared the gate"*.

---

# 4. The aggregation rule — 15 points, stated precisely

## The rule

```
production_crop = Σ_p ( yield_p [t/ha] × area_p [ha] )        over plots of that crop
yield_crop      = production_crop / Σ_p area_p                 area-weighted, never a mean of rates
production_village = Σ_crop production_crop
```

**Never a mean of per-hectare rates.** A village statistic that weights a 0.05 ha plot equally
with a 2 ha one is not the statistic the submission is built from.

## Edge cases, with our measured numbers

| case | count | area | treatment |
|:--|--:|--:|:--|
| never observed by Capella (any date) | **29** (all cotton) | 4.43 ha, **0.99%** | keep as rows; impute from the crop's area-weighted mean; **flag** `no_sar_data` |
| missing 29 Oct only | 81 | — | impute that date from the plot's own trajectory; flag |
| missing on 29 Oct in total | **134** | 22.41 ha, **5.01%** | as above; per-crop loss 1.9–8.8%, reported |
| degenerate parcels < 1 m² | **10** | ~0 | keep as rows; **never** allowed to define a spatial grid or extent |
| ten-farm non-crop flag | 10 | 0.60% | **flag, never filter** — they still enter crop shares and the village aggregate, which is the actual defect |

**No farm is ever dropped.** The buffer ladder already guarantees a label for all 966
(951 at −5 m, 5 at −2 m, 10 at 0 m, 0 failures).

## Uncertainty propagation

Plots are **not** independent — Moran's I on our layers is positive and significant, and the
literature is explicit that *"residual variance, largely resulting from spatial correlation of
residuals, dominated all other sources."* Treating plots as independent **understates** the
village interval, which is the failure mode a panel probes. **Method: arXiv 2412.16403,
"From pixels to parcels"** — small-area uncertainty for spatial averages from wall-to-wall maps,
structurally our problem. Village-level conformal interval per ADD-1, with **β stated and the
1 − α − β arithmetic shown**, not a nominal level quoted.

## ★ The denominator — a defensibility question, not an arithmetic one

Three real numbers: **966 plots = 447.5 ha**; village **cropped area ≈ 690.9 ha**; village
**polygon = 1174.1 ha**. Our plots cover **65% of cropped area**.

**Decision: report the plot-based total as primary (it is what we measured), report the
village-scale extrapolation beside it, and state the 65% coverage explicitly.** Everyone else
will report one number.

## Sub-village product

A fixed **500 m zone grid**, per-zone aggregates, ≥5 farms per zone. Cheap, and it shows
within-village variation a single row hides — another team found 32 points of health spread behind
their one number. **Ours carries an uncertainty column. Neither Orion's nor 8bit's does.** That is
where we are better rather than merely different.

---

# 5. Explicit decision on every freeze-dividend item and capability gap

## 5a. Freeze dividend (§3.5) — **all five ship. These are the cheapest points in the round.**

| item | decision | note |
|:--|:--|:--|
| SF² calibration | **SHIP — done** | confirmed three independent ways (P1-2, P1-8); the R2 defect is closed |
| Bajra anchor 2.714 → 1.91 t/ha | **SHIP** | and see the separate, *new* bajra finding in 5c |
| Ten-farm non-crop flag | **SHIP as a flag, never a filter** | they still enter the aggregate — that is the defect being disclosed |
| Calibrated sampling uncertainty | **SHIP, honestly labelled** | calibrated to 3.4% with no tuning, but only 15.9% of between-farm signal; presenting it as general confidence would overclaim. **All six shortlisted teams shipped point estimates and none demonstrated calibration** |
| Crop-label posterior | **SHIP** | median max probability 0.409; 69.4% of farms with no class above 0.5. No other team ships a per-farm label distribution at all |

## 5b. Capability gaps (§3.6) — three ship, one drops, two are gated

| gap | decision | reason |
|:--|:--|:--|
| **NESZ per-farm quality gate** | **★ DROP — closed by measurement** | P1-4c: **zero farms on any date have a mean below the floor**; worst p05 clears by **7.4 dB**; zero farms have half their pixels within 3 dB. Orion's `NESZ_MARGIN_DB = 3.0` **passes all 966 farms on all six dates**. R2's "12–23% of pixels near the floor" was computed under the *unsquared* calibration and does not survive P1-2. **Ship the margin table as a QC exhibit instead of building a gate that fires on nobody** |
| **Orion's quality constants** | **★ MIN_CORE_PX REJECTED with a measurement; the rest ship as FLAGS** | `MIN_CORE_PX = 60` flags **431/966 (45%) of our farms** and **11/966 (1%) of theirs** — their median core is **2115 px against our 69**, a ~30× finer grid. **The constant is grid-dependent and not transferable**; the defensible version is an *area* (~78 m²), which on our 5 m grid is ~3 px and flags almost nobody. `MIN_VALID_DATES = 3` flags 41 farms (5.97 ha) — adopt as a flag, never a filter. `MIN_DATE_COVERAGE = 0.50` is moot: our per-farm coverage is all-or-nothing (median 1.0) |
| **Proportional erosion** | **TEST, then report the difference** | P1-8 measured the consequence: our residual against Orion's γ⁰ correlates with plot size at **ρ = −0.27 to −0.37 on all four shared dates**, same sign every time. The interior rule is a real, quantified sensitivity. Report it; adopt only if it improves a witness |
| **Thin-plate-spline geocoding** | **STRETCH, gated** | measured 3.62 → **1.78 m** median, 18.5 → 15.2 m at p95; the tail matters at a 52 m median plot side. **Mind the silent-no-op trap** (`SRC_METHOD`, not `METHOD`) — the regression suite already asserts that class. Score by **leave-one-out**, never at the control points where a TPS is zero by construction. Ship only if it passes by the 31 Aug gate |
| **Sub-village spatial product** | **SHIP** | §4 above; cheap, 15-point criterion |
| **Non-circular label test** | **★ SHIP — promoted to high priority** | P1-5 made this urgent rather than optional: it established that **every naive label-vs-label test on this stack is circular**, because R2's labels were derived from these trajectories. Orion's residual method is the only non-circular design we have. This is check **D4** |
| **Reserved-scene discipline** | **SHIP as a contamination ledger** | §3c above — we cannot produce a clean reserve and will say so |

## 5c. ★ New this round: the bajra share, and a self-correction we should ship

ADD-3 compared our crop mix against the **actual Gujarat kharif 2025 sowing profile** — the same
source Orion's `CROP_MIX_REFERENCE` was derived from, now identified and verified.

| crop | GJ 2025 sowing | ours | Orion's reference |
|:--|--:|--:|--:|
| Cotton | 39.1% | 43.2% | 32.0% |
| Groundnut | **39.2%** | 30.8% | **16.0%** |
| Rice | 13.8% | 10.6% | 26.0% |
| Maize | 5.1% | 6.0% | 18.0% |
| **Bajra** | **2.9%** | **9.5%** | 8.0% |

**Total absolute deviation from the season's own sowing profile: ours 23.2 pp, Orion's reference
60.5 pp.** We are **2.6× closer**, and they built their reference *from these figures* and then
adjusted away from them. The groundnut objection does not survive its own source: state
groundnut:cotton was **1.00** in 2025 (groundnut surpassed cotton for the first time, at 116.62%
of normal area), ours is 0.71, theirs 0.50.

**But bajra at 9.5% against a state share of 2.9% is our largest single deviation**, and Round 1
independently found real bajra area in Vadodara close to zero. **Decision: ship this as a stated
self-correction — if any share in our map is wrong, the evidence points at bajra, not groundnut.**
Owning that is worth more than defending everything.

*Limits, stated: state ≠ village, sown area ≠ plot share, and the 4 Aug snapshot is 82% through
sowing. This does not settle 30.8% against 16%. It establishes that the argument from state
sowing, run on the actual state sowing, favours us.*

---

# 6. Schedule against the real deadline

**Working days: 31 August and 1 September.** 30 August (today) is spent on Phases 0–3.

| when | gate | contents |
|:--|:--|:--|
| **31 Aug, midday** | — | modifier rebuilt on six dates; anchors set; T1/T2/T3 run |
| **★ 31 Aug, end of day** | **SUBMITTABLE BASELINE EXISTS** | a complete, valid, defensible submission on disk: modifier + anchors + all five freeze-dividend items + aggregation + D1–D5, D8. **Everything after this is improvement on something already shippable** |
| **1 Sep, midday** | — | stretch items that passed their gates; zone product; conformal village interval; D6, D7 |
| **★ 1 Sep, end of day** | **EVERYTHING FINISHED** | writeup, PPT, figures rendered *and looked at*, final regression suite, submission uploaded |
| 2 Sep | finals day 1 | travel, present |
| **3 Sep, 12:30 IST** | **deadline** | already submitted two days earlier |

**Why the baseline gate is non-negotiable.** Round 1's lesson was an unreconstructable champion.
Round 2's was that a submittable gate early beats a better model late. With two working days and
a deadline 11.5 hours earlier than assumed, that lesson is the plan.

---

# 7. Task list, dependency order

| # | task | phase | cost | kill criterion | blocks |
|:--|:--|:--|:--|:--|:--|
| **T1** | **Can any X-band feature serve as a GAI proxy?** Correlate our features against the S2 NDVI witness within crop | build | 3 h | if no feature clears ρ = 0.5 within crop on ≥3 dates, **SAFY is dead** and we say so | SAFY stretch |
| **T2** | **WCM re-test.** Fit attenuation per crop against the 13 Oct → 29 Oct rise and the ERA5 moisture step | build | 4 h | **the three cereals must fit near-zero attenuation** — bare ground has none. If they do not, discard | WCM component |
| **T3** | **Measure η² of the crop label on our new yield column** | build | 1 h | if η² ≥ 0.820, the modifier has not improved and we report that | the headline claim |
| T4 | Anchors per crop for 2025-26, with the bale convention asserted | build | 2 h | if no kharif 2025-26 anchor exists, fall back to trend-adjusted 2022-23 and say so | everything |
| T5 | Modifier v1 on six dates, normalised within crop | build | 4 h | — | T3, T6, submission |
| T6 | Aggregation + both denominators + zone grid | build | 3 h | — | submission |
| T7 | Freeze-dividend items (all five) | build | 2 h | — | submission |
| T8 | D1–D5, D8 defensibility checks | validate | 3 h | **D1 failing means our two rounds disagree — stop and find out why** | submission |
| **T9** | **★ BASELINE SUBMISSION — 31 Aug EOD** | ship | 1 h | — | **everything after** |
| T10 | Non-circular label test (D4, Orion residual method) | validate | 2 h | — | writeup |
| T11 | Ensemble spread + village conformal interval (D6) | build | 3 h | if β cannot be defended, ship ensemble spread alone | writeup |
| T12 | TPS geocoding, scored by leave-one-out | build | 3 h | if LOO does not beat 3.62 m, or the no-op assertion fires, **drop it** | — |
| T13 | Spatial hold-out (D7) for anything fitted | validate | 2 h | — | writeup |
| T14 | Writeup + PPT + figures **rendered and looked at** | ship | 6 h | — | — |

---

# 8. What we will deliberately not do

**The §3.2 closed list stands** — dense S1 as a label source, Dynamic World filter, WorldCereal,
Quegan–Yu, any covariate coarser than ~1 km, ERA5/POWER/OWM for *ranking*, USDA ERS, AlphaEarth as
a label source, CoV excess over an L=1 baseline, plot-size detrending, GDAL polynomial order 2,
uncertainty-first ground-truth sampling. **None of the six dates changes any of those premises.**

**Priced out or closed in Phases 1–2:**

- **Process-based crop models with assimilation** — parameterisation cost (§1, Alternative 2).
- **Unsupervised / self-supervised representation learning** — re-checked at n=966 × 6 dates;
  the extra dates do not change the arithmetic. **Negative re-confirmed and reportable.**
- **A NESZ quality gate** — closed by measurement; it would fire on nobody (5b).
- **`MIN_CORE_PX = 60`** — rejected with a measurement; not transferable across grids (5b).
- **The §4 groundnut-lift test** — discarded by its own control (P1-5). It is **priced, not dead**:
  it needs labels not derived from Capella, and every candidate is a frozen witness.
- **Per-plot conformal intervals** — ADD-1: the guarantee is 1 − α − β and our per-plot β is large
  enough that the intervals would be too wide to be worth shipping. Village level only.
- **Water-point referencing** — P1-3b: 29 October carries **+2.87 dB** of wind roughening at
  14.1 m/s, double every other date. **Do not inherit R2's referencing without a wind gate.**

---

# 9. Risk register

| risk | early warning | fallback |
|:--|:--|:--|
| **Cotton is the round and X-band goes blind at picking** (B-3, P1-6a) | T1 fails; cotton modifier variance collapses | shift cotton's weight onto the trajectory to 13 Oct + the A-1/ADD-2 picking constraint; **state the limitation rather than hide it** |
| **The 29 Oct wetness term is canopy-dependent and no scalar removes it** (P1-6b) | crop-ordered residuals after correction | drop 29 Oct from the level features, keep it as a *moisture* observation; the WCM re-test (T2) is the principled route |
| **No kharif 2025-26 anchor exists** (P0-11 blocker) | T4 finds nothing | trend-adjusted 2022-23 with the 2025 direction from A-3/ADD-5 (**flat, not sharply down** — 463 vs 464 kg/ha) and the adjustment stated |
| **The crop label still dominates yield variance** | T3 returns η² ≥ 0.820 | report it honestly as the measured bottleneck; the label, not the yield model, is the ceiling — that *is* the finding |
| **Groundnut share dispute reopens at the panel** | a judge cites Orion's 16% | ADD-3: we are 2.6× closer to the season's own sowing profile than their reference, which was built from it. **And volunteer the bajra correction first** |
| **Schedule slips past 31 Aug** | T5/T6 not done by midday 31 Aug | cut T11–T13, ship the baseline; the gate exists precisely for this |
| **No host submission template** | none found on either channel | R2's decoded schema + both unit guards; **flag the residual risk explicitly** |
| **Deadline is 12:30 IST, not end of day** | — | submit by **1 Sep EOD**; treat 2–3 Sep as having no working hours |

---

# Open questions I could not settle

1. **The Gujarat kharif 2025-26 *yield* anchor.** Area is now sourced (ADD-3); yield is not.
   data.gov.in stops at 2023-24 with no commercial-crops table (P0-11). The national number is
   463 kg/ha lint, essentially flat on last year.
2. **Whether R2's cotton completion factor of 0.45 meant *picked* or *determined*.** ADD-2 shows
   0.45 is indefensible as the first and arguable as the second, and R2 never fixed which. It
   changes D1's expected ratio.
3. **Vadodara's rank within Gujarat** — Orion's "1st in maize yield, 2nd in cotton yield" is
   unverified after three searches, with mild counter-evidence on *area*. Do not build on it.
4. **Whether the S1 → scaffold, S2 → witness swap should be made.** Recommended in R-D and it is
   defensible — S2 has 20 clear scenes including a same-day 12 November — but it spends the
   witness that corroborated the soil-moisture finding at ρ = +0.749. **This is your call, not
   mine**, and it is the one decision in the plan I would not make unilaterally.

**Stopping here for approval. Nothing is built.**
