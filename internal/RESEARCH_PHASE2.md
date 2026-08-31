# Phase 2 — deep research, organised by question

Grading, applied to every claim: **`OWN`** we measured it this round · **`MECH`** an established
physical mechanism or a literature result · **`THEIRS`** a third party asserts it and we have
not verified it.

For every source: what it claims, what it measured that on, and **whether its objective is the
same as ours**. Round 2 lost time twice to importing a result whose objective was subtly
different, so the objective column is not decoration.

Our configuration, which is what every method must be ranked *for*: X-band, **HH**,
single-pol, **6 irregular dates** 6 Jun – 12 Nov, incidence 28.7–35.2°, 966 plots of
**0.27 ha median**, smallholder kharif, **no labels, no ground truth**.

---

# R-A. The forecast target and the agronomy that defines it

## ★ A-1. Gujarat cotton was 80% through its FIRST picking two days before our last scene

**Source:** USDA FAS GAIN report **IN2025-0071**, *Cotton and Products Update*, New Delhi,
**dated 2 December 2025**, citing the **MOAFW weekly weather report of 10 November 2025**.
`THEIRS` (USDA analysis) resting on `primary` (Indian government). Objective: commodity
supply-and-demand forecasting — *not* remote sensing, so it is independent of everything we do.

> "The central zone (Gujarat, Madhya Pradesh, and Maharashtra) is focused on the initial
> first picking, where completion varies greatly, from **a high of 80 percent in Gujarat**
> to only 15 percent in Maharashtra."

**Why this is the single most useful external number we have found.** Our last acquisition is
**12 November**. This is a state-level harvest-progress figure dated **10 November** — a
two-day offset. Round 2 assigned cotton a completion factor of **0.45** with no dated source
at all. This is a dated, official one.

**What it does and does not say.** It is *first* picking, and Indian cotton takes two to three.
It is state-level, not Vadodara. The conversion from "80% of first picking" to "fraction of
final yield in hand on 12 November" needs the yield split across pickings, and **we could not
find a published split** — searched USDA GAIN, CICR-adjacent literature, and Indian agronomy
sources; the retrievable literature covers picking *intervals* and seed quality, not the yield
share per picking. **Recorded as an explicit gap.** The north zone comparison bounds it: Haryana
and Rajasthan were 90% and 60% into their *third* picking on the same date, so Gujarat at 80%
of first is genuinely mid-season, consistent with §4's "picking runs to January".

## ★ A-2. Our 29 October scene sits inside a documented state-wide crop-damage event

`THEIRS`, and it corroborates `OWN` P1-3c exactly.

> "Heavy rainfall between **October 23rd and 28th** affected **239 talukas across 33
> districts**, with preliminary estimates indicating damage to **over 10 lakh hectares** of
> agricultural land." The Gujarat cabinet ordered an immediate **seven-day crop damage survey**.

Phase 0 found **81.2 mm over 26–28 October** in ERA5-Land at Sokhda and soil moisture rising
0.127 → 0.417, with our 29 October overpass landing on the wet peak at 0.372. We reported that
as a meteorological anomaly we had discovered. **It is a state-scale agricultural disaster with
a government damage survey attached, and one of our two new acquisitions is inside it.**

Three consequences, and they are not all radiometric:

1. **Radiometric.** The +4.03 dB canopy-dependent wetness term measured in P1-3c is not an
   ERA5 artefact. It has an independently documented cause.
2. **Agronomic.** Over 10 lakh ha of standing crop was damaged in that window. **The event is a
   yield-loss mechanism, not only a backscatter confound.** A forecast that treats 29 October
   purely as a contaminated observation misses that the crop itself changed.
3. **On the anchor.** Any yield anchor from a pre-2025 statistic is a level for a year this one
   is not. USDA already carries the correction downward (A-3).

## A-3. The 2025 season, and the direction the anchor must move

`THEIRS` (USDA FAS IN2025-0071):

- India MY2025/26 cotton yield revised **down 3% to 463 kg/ha** lint; production 23.8 M bales.
- Cause: *"highly uneven monsoon rainfall and the widespread use of low-performing, unapproved
  hybrid seeds."*
- Heavy August–September rain caused *"root rot, flower and square shedding, and stunted
  vegetative growth"*, timed onto *"the critical flowering and boll-development stages"*.
- **"Major producing states (Maharashtra, Gujarat, and Telangana) were affected by widespread
  flooding and waterlogging during the late-maturity period. The prolonged moisture stress
  resulted in boll drop, flower shedding, and heightened pest and disease pressure."**

**The direction is unambiguous: 2025-26 Gujarat cotton is a below-normal year, damaged
specifically at boll development and again at late maturity.** R2's anchor was a 2022-23
district statistic. Carrying it forward unadjusted forecasts a normal year.

## ★ A-4. The bale convention, confirmed by a primary source, in one line

`THEIRS`, but explicit and self-consistent — the report states the same quantity three ways:

> "23.8 million **480-lb bales** (30.5 million **170-kg bales** / 5.2 MMT)"

Check: 23.8 × 480 lb = 23.8 × 217.7 kg = 5.18 MMT. ✔ And 30.5 × 170 kg = 5.19 MMT. ✔
**The 170 kg Indian bale is confirmed**, and so is the fact that international reporting uses a
*different* bale. This validates R2's `BALE_KG = 170.0` and the lint convention from a source
we had not used this way, and it names the exact trap: a table quoting "bales" without saying
which kind is a 1.28× error waiting to happen.

## ★ A-5. A new datum on the groundnut dispute — from the season itself

`THEIRS` (USDA FAS IN2025-0071), on 2025 sowing:

> "Most of the reduction in cotton acreage has shifted toward rice, pulses, maize, and
> sugarcane. In Punjab and Haryana, cotton area has largely been diverted to paddy, while
> **in Gujarat it has shifted primarily to groundnut**."

Orion's case against our 30.8% groundnut share (§3.1, and `DELIVERABLE_MINING.md` §3) rests on
*"Gujarat's groundnut area is concentrated in Saurashtra, not the central zone"* and a
`CROP_MIX_REFERENCE` of 16%. That reference is an agro-zone prior. **This is a statement about
the specific season our scenes image, and it says Gujarat groundnut gained area at cotton's
expense in 2025.**

It does not settle 30.8% against 16% — it is state-level, and Saurashtra could absorb all of the
shift. But it is the first evidence anyone has produced that is *dated to this season* rather
than to an agro-zone norm, and it points our way. **Report it as what it is: a directional datum,
not a resolution.** Real ground truth remains the only thing that settles the share.

## A-6. Groundnut — when yield is determined, versus when it is lifted

`MECH`, Indian agronomy literature (middle-Gujarat kharif trials, ICAR/JAU-adjacent sources):

- **Physiological maturity at ~135 days after sowing**; maximum dry matter accumulated by 135 DAS.
- Harvest indicated when **75–80% of pods are fully matured** — yellowing lower foliage, leaf
  spotting and drop, dark tan inside the shell.
- Critical moisture stages are flowering and **peg penetration / pod filling**.
- **"Early harvest (immature pods) reduces yield significantly; late harvest causes pod
  shattering and aflatoxin risk in wet conditions."**

Kharif sowing on the monsoon onset (mid-June, consistent with our 19 June scene being
pre-/early-sowing) puts **135 DAS at late October**. So:

**Yield is determined by ~late October. Lifting follows. 12 November is therefore *after* the
determining event, and §4's characterisation of groundnut as "a near-complete measurement" is
agronomically correct.** ✔

And the sharp edge: **the 23–28 October rain lands on groundnut at physiological maturity,
which is precisely the condition the literature names for pod shattering and aflatoxin loss.**
The same event that contaminates our radiometry is a yield-loss mechanism for 31% of the village.

## A-7. Vadodara's rank within Gujarat — NOT verified, and the search is on the record

Orion's code asserts *"Vadodara ranks 1st in Gujarat for maize yield, 2nd for cotton yield."*
§8 flags it as unverified and worth verifying, because it constrains anchor plausibility.

**We could not verify it and we found nothing supporting it.** The district-level Gujarat
literature that is retrievable reports crop **specialisation** (area share), not yield rank, and
on that measure: *maize specialisation highest in **Panchmahal***, *cotton specialisation
highest in **Bharuch and Surendranagar***. Vadodara is described as growing cotton, pigeon pea,
paddy, maize and wheat, with no rank claim.

Specialisation is not yield, so this **does not refute** Orion. It establishes only that the
claim has no support we can find. **Status: `THEIRS`, unverified, do not build on it.** The
plausibility test §8 wanted — "a Vadodara anchor for maize and cotton should sit near the top of
the state range" — cannot be run until the district-wise yield series is obtained, and Phase 0
(P0-11) established that data.gov.in's Gujarat series stops at 2023-24 with no commercial-crops
table at all.

---

# R-B. What X-band HH can and cannot retrieve

## B-1. Saturation, and the non-monotonicity — the constraint on everything

`MECH`, multi-frequency comparisons and X-band rice studies:

- **X-band saturates at very low biomass**, a direct consequence of the short wavelength.
- LAI correlates best with **C-band**, total biomass with **L-band**; *"shorter wavelengths
  including X-band were poorly correlated with LAI and biomass."*
- The rice result that pins the non-monotonicity: **backscatter peaks at ~60 cm plant height and
  then declines, before the ~100 cm maximum height is reached.**

**This is why R2 built the index on structure, moisture and temporal change rather than on
brightness, and the literature confirms that was the right call.** It also states the WCM
inversion hazard precisely: **below the turning point the inversion is two-to-one.** A brightness
value alone cannot say which side of the peak a canopy is on; only the temporal series can.

## ★ B-2. The physical justification for an X-band yield proxy — and it is a real one

`MECH`, X-band rice studies (COSMO-SkyMed and TerraSAR-X):

> **Panicle biomass was best correlated with X-band σ⁰.** Backscattering coefficients at high
> microwave frequencies (Ka, Ku, X) were highly correlated with **weight of ear**.
> *"X-band SAR would be promising for **direct assessments of rice grain yields** at regional
> scales from space, whereas it would have limited capability to assess the whole-canopy
> variables only during the very early growth stages."*

**This is the claim §8 asked us to chase, and it is well supported.** The apparent weakness of
X-band — it does not penetrate to see whole-canopy biomass — is the same property that makes it
sensitive to the *upper, grain-bearing* layer. An X-band yield proxy is therefore physically
motivated, not merely correlational, and that is a genuinely strong argument to make to a panel.

**Objective and configuration caveats, stated because they matter.** Measured on **rice**, at
**VV**, at shallow incidence, with a panicle layer that sits at the canopy top in a way cotton
bolls and groundnut pods do not. Our configuration is **HH**, 28.7–35.2°, on cotton and
groundnut. **Groundnut is the hard case: pods are underground.** The panicle argument transfers
to a crop whose harvested organ is in the upper canopy — cotton bolls, plausibly — and does
**not** transfer to groundnut, where X-band cannot see the yield-bearing organ at all. That
asymmetry belongs in the writeup: it is exactly §4's "three different epistemic objects".

## ★ B-3. Cotton late-season — P1-6a has a physical explanation, and it is not a bug

The sharpest open question from Phase 1: the cotton-minus-cereal gap *shrinks* to +0.97 dB by
12 November, when cotton is still standing.

**X-band cotton literature is thin, as §8 predicted.** The best available is C-band and its
objective differs, so it is used for mechanism only:

*Demirci & Sunar, ISPRS Archives XLVIII-4/W18-2025 (2026), "Overcoming Optical Gaps: Evaluating
SAR–Optical Consistency for Cotton Phenology"* — 11 adjacent cotton fields, Didim, Türkiye, 2024
season, Sentinel-1 SLC dual-pol + Sentinel-2. **Objective: SAR–optical temporal consistency, not
yield.** `THEIRS` for its numbers, `MECH` for its mechanism:

> Metrics *"start low in early growth, rise sharply during vegetative expansion, peak at maximum
> biomass in late July–early August, and **decline toward harvest**."*
> *"...until senescence, when **declining leaf water content and leaf drop reduce both canopy
> structure and backscatter**."*
> NDVI–VH mean **r = 0.930** across the 11 fields; Stokes g₀–MSAVI 0.863.

**So cotton backscatter genuinely falls late season — leaf drop is a structural loss, and
defoliation before picking is deliberate.** At C-band, which penetrates further and sees more
volume. **At X-band, which saturates earlier and samples the upper canopy, convergence toward
the soil signal should happen sooner and more completely.** P1-6a is consistent with physics,
not evidence of a broken pipeline.

**What this changes for the round.** It reframes the cotton problem correctly. The issue is not
that our cotton signal failed — it is that **X-band brightness stops carrying cotton canopy
information at exactly the point where picking begins**, which is the window the forecast must
extrapolate across. A cotton forecast cannot lean on 12 November *brightness*. It must lean on
the **shape of the trajectory up to the point where the signal was still informative**, plus an
external picking-progress constraint (A-1). That is a design conclusion, and it comes from
Phase 1's failed prediction rather than from any paper.

## B-4. Dew — bounded, and now formally dismissed

`MECH`, canopy-water studies (soybean, corn, wheat; L-band-focused with X-band comparison):

- **Water on canopies can raise X-band backscatter by up to 2–3 dB**; up to **3.8 dB** difference
  between presence and absence of surface canopy water on the soil-reflectivity path.
- Dew present on canopy most days **midnight to 10:00**.
- **"The effect of surface canopy water on backscatter decreases with increase in frequency."**

Our 01:37 pass sits squarely in that dew window, so the hypothesis deserved its test. **Phase 0
killed it on the physics of the specific nights**: dew-point depression was **4.9 °C** on 29 Oct
and **7.4 °C** on 12 Nov, against **0.9 °C** on 19 June and **2.0 °C** on 14 August. The night
passes are the *drier* ones. The literature adds two things: the magnitude we would have been
exposed to is 2–3.8 dB (material — comparable to our whole crop signal), and X-band is the
**least** dew-sensitive of the microwave bands. **Dew is dismissed with a magnitude bound
attached, which is a stronger statement than dismissing it without one.**

## B-5. Azimuthal anisotropy and look side

The literature question is moot: **we measured it (P1-3a) and there is none detectable** —
reversed-pair per-target sd 1.81 dB against a 1.90 dB same-look control, and the isotropic class
(water) spreads *more* than the anisotropic one on the same pair. `OWN` beats `MECH` here, and
our own measurement on our own scenes over our own targets is the better evidence.

## ★ B-6. Re-opening the WCM rejection — the premise has changed, but a new obstacle appeared

§8 calls this "one of the highest-value re-openings available". R2 rejected the WCM inversion as
a health component because the observed August/June ratio sat **below the model's floor at any
monsoon-plausible soil moisture**, and the discrepancy was the same size as our own calibration
uncertainty.

**The calibration is now fixed (P1-2, confirmed three independent ways), so the second half of
that reason is gone.** The premise genuinely has changed and the re-test is warranted.

But Phase 1 raised a new obstacle the R2 rejection never had to face. The WCM separates a soil
term from a vegetation term, and its soil term needs soil moisture. **P1-6b measured that the
soil-moisture response is canopy-dependent** — the 29 October rise runs from +0.49 dB (cotton,
most canopy) to +2.60 dB (bajra, bare) — which is *exactly what the WCM predicts*, since the
vegetation layer attenuates the soil contribution by a two-way factor. **That is not a problem
for the WCM. It is a validation of it, and it is the strongest argument for the WCM this round
has produced.** A 2.1 dB spread ordered by canopy cover is the WCM's central prediction observed
directly in our own data, on six dates, with a bare-soil control (the cereals).

**Test that would kill it:** fit the WCM's attenuation term per crop against the 13 Oct → 29 Oct
rise and the ERA5 soil-moisture step. If the fitted attenuation does not order the crops the same
way an independent canopy proxy does, the agreement is coincidence. **Control:** the three
cereals, all bare by then, must fit with near-zero attenuation. Unlike the groundnut-lift test,
this control is *not* circular — it tests a coefficient, not a class contrast, and its prediction
(attenuation ≈ 0 for bare ground) is fixed by the model before any label is consulted.

---

# R-C. Yield forecasting without labels — the core question

Ranked **for our configuration**, not in the abstract.

## C-1. Semi-empirical growth models — the SAFY family. **Recommended core.**

`MECH` / `THEIRS`. SAFY = *Simple Algorithm for Yield estimation*, a semi-physical light-use-
efficiency model. What the literature establishes:

- SAFY-WB (with water balance) is **"controlled by the Green Area Index (GAI), derived from
  satellite images acquired in the microwave and optical domains"** — SAR provided by
  Sentinel-1. **SAR-derived GAI is established practice, not an improvisation.**
- **"...demonstrates the potential of high resolution remote sensing data to calibrate a simple
  crop model *without resorting to in situ data*."** That is our problem statement verbatim.
- **"the use of a double logistic function to interpolate GAI time series permits to improve the
  estimations of biomass and yield when remote sensing data are missing"** — directly addresses
  our 56-day mid-season gap.
- Variants exist for sugarcane (SAFY-Sugar) and corn; the family is crop-adaptable.

**What it needs:** a GAI/LAI proxy time series, daily meteorology (we have ERA5-Land hourly for
the whole season), sowing date, and ~4 free parameters.
**What we have:** all of it except a validated GAI proxy and per-plot sowing dates.
**What would kill it:** if no X-band feature can serve as a GAI proxy — which B-1 makes a live
risk, since X-band correlates *poorly* with LAI. **This is the decisive test and it must be run
before committing.**
**Identifiability:** P1-7 puts a 4-parameter free set at **2 residual df at n=6, where n=4 gave
0.** Newly feasible this round, and weakly so — three effective trajectory directions against
four parameters, so parameter uncertainty must be reported, never point values.

## C-2. Process-based models with data assimilation — **rejected, on cost**

DSSAT / APSIM / AquaCrop / WOFOST with forcing, recalibration, sequential filters or variational
assimilation. `MECH`, well established, and demonstrably better where it can be parameterised —
joint LAI + soil-moisture assimilation from S1+S2 into WOFOST is a published wheat result.

**The honest cost:** cultivar coefficients, soil profile hydraulic properties, management
(sowing date, density, irrigation, fertiliser) per plot — for **five crops** across 966
smallholder plots with **no ground truth and no agronomic survey**. Every one of those is a
number we would be inventing.

**Rejected**, and the reason is the rubric's own arithmetic: **Plausibility & Defensibility is 25
points, Innovation is 15.** §8 states the rule and it applies exactly here — *a model we cannot
parameterise defensibly is worse than a simpler one we can*. Worth **naming in the writeup as
considered and rejected with the reason**, which is itself a defensibility exhibit.

## C-3. Growth-curve extrapolation and phenology metrics — **partly viable, bounded by P1-7**

Standard forms: double logistic, asymmetric Gaussian, piecewise logistic, Fourier, splines.
Predictors: integral, peak, rate, duration.

**P1-7 is the binding constraint, and it is ours:** double logistic has **6 parameters and 0
residual df at n=6** — not identifiable. Asymmetric Gaussian and single logistic (4 params) have
2 df. Six dates span ~3 effective directions (2 PCs = 72.7%, 3 = 83.3%).

**The cotton problem this family cannot solve:** our series ends mid-picking, so curve
extrapolation past 12 November is extrapolation past the last observation *and* past the point
where B-3 says the signal stopped carrying canopy information. **Extrapolating a curve fitted to
a signal that has gone flat produces a confident wrong answer.** Use the fitted shape as
*features*, not as an extrapolator.

## C-4. Dasymetric / anchor-plus-modifier — the incumbent, and the criticism is published

`MECH`. The literature name is **spatial disaggregation / downscaling of regional yields**; the
closest published analogue to our exact task is *"Subfield-level crop yield mapping without
ground truth data: a scale transfer framework"*.

**The published limitation is precisely our own criticism, which is worth knowing:**

> *"The variation of remote sensing observations differs by scale, resulting in a **distribution
> shift at the disaggregate scale** and degrading model performance due to scale effects."*

So the incumbent's weakness has a name and a citation, and we can state it as a known property
rather than as an admission.

**The measured case for keeping it** (§8, R2's own result — `OWN`): our yield column correlated
*negatively* with three of five teams, and correcting the bajra anchor moved those correlations
by **−0.001**. The cause is that **yield is 82% explained by the crop label** (η² = 0.820) and
the crop maps agree at chance. Conditioned on label agreement, our yield agrees at **+0.678**
(Megalodon) and **+0.751** (DeepThinkers) — the two teams whose method most resembles ours —
**mean +0.395**. **Our yield column is a good measurement carried on a bad label.**

**Quantifying what the SAR actually contributes** — §8 demands this and it is answerable
directly: the anchor sets the level, the SAR sets the spread, so the SAR's contribution is
**1 − η²_label = 0.180** of yield variance under R2's design. Two other teams reached η² of
0.474 and 0.499, i.e. SAR contributions of 0.526 and 0.501. **That is the number to move, it is
a single reportable figure, and "we raised the SAR's share of yield variance from 0.180 to X" is
exactly the kind of claim the panel rewards.**

## C-5. Unsupervised / self-supervised at n=966 — **re-checked, still no**

R2 priced this out. The extra dates change the arithmetic only marginally: 966 samples × 6 dates
against a designed physical feature set. Representation learning needs far more. **Negative
re-confirmed and reportable**, which was the cheap-and-worth-it part.

## C-6. Hybrid and ensemble — **recommended for the uncertainty estimate**

`MECH`. Multi-model ensembles: *"the mean or median of an MME is a better predictor that
provides model uncertainty information compared to individual models"*, and the **spread across
genuinely different method families is an uncertainty estimate that needs no ground truth.**

With no labels and no truth, this is one of very few honest routes to a calibrated-looking
interval — and it converts C-1's weak identifiability from a liability into an input.

---

# R-D. Sparse irregular time series

Six acquisitions, irregular, 6 Jun – 12 Nov, a **56-day mid-season gap**, two clustered at the end.

- **Standard practice** is curve fitting (double logistic, asymmetric Gaussian, Savitzky-Golay,
  splines, Fourier) — all developed for *dense* series and all assuming enough points to
  constrain the form. `MECH`.
- **The SAFY practice is the transferable one:** fit a double logistic to the GAI series
  specifically to **interpolate across missing acquisitions**, then drive the crop model with the
  interpolated series. The interpolation is a scaffold, not a measurement.
- **Our binding limit is P1-7, not the literature**: at n=6 spanning 3 effective directions, the
  6-parameter forms are unidentifiable and the 4-parameter forms are weakly identified.

**The C-band scaffold question, and the answer.** We hold **18 dates** of Sentinel-1 RTC on one
relative orbit, cloud-immune, spanning the season — a genuinely dense series. The ISPRS cotton
result (B-3) gives **NDVI–VH r = 0.930** on cotton, so C-band VH tracks cotton canopy status
well. Using it as a **temporal scaffold** — to constrain the *shape* between our X-band dates
without contributing *level* — is principled and is what the SAFY interpolation does.

**But it costs a witness.** S1 is currently frozen, and it is the witness that independently
corroborated the soil-moisture finding at ρ = +0.749, p = 0.0004. §5.1 requires naming and
freezing a replacement before promoting it. **The replacement is available: 20 Sentinel-2 scenes
under 20% cloud in Oct–Nov, including a 0.001%-cloud scene on 12 November, same-day with our
final Capella acquisition.** That is a *better* late-season witness than S1 for the dates that
matter. **Recommendation: this trade is worth making, and Phase 3 should make it explicitly —
promote S1 to scaffold, freeze S2 as the witness, and record the swap.**

---

# R-E. Uncertainty and validation without ground truth — where 25 points live

## E-1. Where R2 got to, and why the interesting part is elsewhere

`OWN`: R2's split-half sampling-noise model predicted its own noise to **within 3.4% with no
tuning** — genuinely calibrated. But that noise is only **15.9% of between-farm signal** and does
**not** predict disagreement with a withheld sensor. **The sampling term is calibrated and not
limiting. The uncertainty that matters is structural**, and P1-5 named its largest component:
the crop label.

## E-2. Conformal prediction — usable, with one specific variant to read

`MECH`. Inductive conformal prediction is **model-agnostic, needs no retraining, distribution-
free**, and gives a coverage guarantee that *"remains absent from other pixel-wise uncertainty
quantification methodologies"*. It adapts honestly: *"with high-quality inputs, conformal
prediction yields smaller, more accurate sets; with noisy data or a poorly fitted model, it
expands the prediction sets to maintain the desired coverage."*

**The blocker is the obvious one: standard ICP needs a labelled calibration set and we have
none.** The variant to read is **arXiv 2509.10321, *"Conformal prediction without knowledge of
labeled calibration data"*** — retrieved and named here, not yet assessed. **Flagged as the
single highest-value unread paper of this phase.**

**Fallback if it does not deliver:** calibrate against the one quasi-label we do have — the
**district anchor at village scale** — giving an interval on the *aggregate*, which is where the
15-point Aggregation criterion lives anyway.

## E-3. Cross-scale validation — three rungs, one of which nobody else has

1. Village total against the district statistic.
2. Forecast against independent-sensor phenology (S2, the witness).
3. **★ Forecast against Round 2's yield-to-date.** The forecast must *exceed* the to-date figure
   for crops still standing, and roughly *equal* it for crops already harvested. **Only we can run
   this, because only we have a Round 2.** It costs nothing and it is a genuine falsifier.

## E-4. Sensitivity, ablation and spatial hold-out

`MECH` + `THEIRS`. Spatial hold-out is the standard for anything fitted, and R2 adopted it after
a competitor demonstrated it — whereupon **it promptly overturned one of our own published
claims**. That history is the argument for using it by default. Ensemble spread (C-6) doubles as
sensitivity evidence.

---

# R-F. Aggregation — now 15 points

## F-1. The rule

**Production = Σ(yield × area).** Never a mean of per-hectare rates. Area-weighted means for any
reported per-hectare figure. Missing and imputed plots must be **counted and stated**, not
silently dropped — P1-4 gives the exact numbers: 29 farms never observed (4.43 ha, <1%), 134
farms missing on 29 October (**5.01% of village area**, 1.9–8.8% by crop).

## F-2. Uncertainty propagation, and the trap

`MECH`. **Spatial autocorrelation dominates.** *"Uncertainty attributed to residual variance,
largely resulting from **spatial correlation of residuals**, dominated all other sources for most
parcels."* Moran's I on our layers is positive and significant, so **treating plots as
independent will understate the village interval** — and understating an interval is the failure
mode a panel is most likely to probe.

**The directly applicable method:** arXiv **2412.16403**, *"From pixels to parcels: flexible,
practical small-area uncertainty estimation for spatial averages obtained from aboveground
biomass maps."* Same structural problem as ours — a small-area aggregate of a wall-to-wall map
with spatially correlated errors — in a different domain. **Named for Phase 3 to implement.**

## F-3. ★ The denominator, which is a defensibility question not an arithmetic one

Three numbers, all real: **966 digitised plots = 447.5 ha**; village **cropped area ≈ 690.9 ha**;
village **polygon = 1174.1 ha**. A total over plots is **not** a total over the village — it
covers **65% of cropped area**.

**Recommendation: report the plot-based total as the primary figure (it is what we measured),
report the village-scale extrapolation beside it, and state the 65% coverage explicitly.** Every
other team will report one number. Reporting both with the gap explained is cheap and is exactly
what a panel notices.

## F-4. Sub-village reporting

With one village the required table is one row and carries no spatial information. **A fixed zone
grid costs almost nothing and shows within-village variation the single row hides** — Orion's
46-zone `zone_summary.csv` is on disk as a worked example, and another team found 32 points of
health spread behind their single number. **Neither Orion's nor 8bit's village summary carries an
uncertainty column. That is where ours is better rather than merely different.**

---

# R-G. The competitive field — forward-looking only

Per §8, the writeups are exhausted; the useful question is what each team does with two extra
dates. Working from `DELIVERABLE_MINING.md` and `COMPETITOR_ANALYSIS_R2.md` rather than re-mining.

## ★ G-1. Orion's NESZ gate — their capability gap, closed by our measurement

Orion gates farms on clearing the declared noise floor by **`NESZ_MARGIN_DB = 3.0`**. R2 recorded
this as a capability gap of ours, noting *"we have 12–23% of AOI pixels near the noise floor by
our own reckoning, and no gate on it."*

**Measured this round under the corrected calibration** (`OWN`, P1-4c and the scene-level check):

| | within 0 dB | within 3 dB | within 6 dB |
|:--|--:|--:|--:|
| AOI pixels (worst date, 6 Jun) | 0.03% | **1.03%** | 14.57% |
| AOI pixels (best date, 29 Oct) | 0.00% | **0.12%** | 2.15% |
| farms with >25% of pixels affected, any date | **0** | **0** | 134 |
| farm means below the floor, any date | **0** | — | — |

**Orion's gate passes every one of our 966 farms on all six dates.** R2's "12–23%" figure was
computed under the unsquared calibration and does not survive P1-2. **The capability gap is
closed by measurement, and the gate is not worth building** — but the margin table is worth
shipping as a QC exhibit, because it answers a question a competent judge may ask.

## G-2. Who can say anything about cotton after 13 October — the round's real question

**Nobody but us has the two new dates**, so on the face of it everyone can. The forward question
is what each team's committed method *does* with them:

- **Orion** — reserved-scene validation discipline, hard quality gates, 46-zone aggregation. Best
  placed to use the new dates *as validation*. Their code note — *"no reserved scene cleared the
  gate, so this audit runs against the..."* — suggests the published reserved-scene story is
  weaker than presented. **Read before citing them as a model.**
- **Coding Bits** — physics priors annotated against sweep argmax; the most likely team to reason
  about the wetness confound rather than absorb it. Highest chance of independently finding the
  29 October problem.
- **Megalodon** — district anchor discounted by crop progress, same family as ours; agreed with us
  within 3% on village production. **Most likely convergent validation, and A-1's dated picking
  figure is the thing that could separate us from them.**

**Where we can be alone, defensibly:** the look-side result (P1-3a), the wetness quantification
with three instruments (P1-3c + A-2), the calibration-quantity correction (P1-2), the
forecast-vs-R2-yield-to-date check (E-3), and the dated 10 November picking anchor (A-1).
**Convergent validity is evidence and lone dissent is a defect** — in R2 one lone position was
corroborated to 0.25 pp and the other was our bug. **Every item above has an internal control or
an external corroborator attached, which is the difference.**

## G-3. Method notes worth adopting

`ERODE_MAX_M = 4.0`, `ERODE_FRACTION = 0.25` — Orion's **proportional** erosion against our fixed
ladder. **P1-8 measured the consequence**: our residual against their γ⁰ correlates with plot size
at ρ = −0.27 to −0.37 on all four shared dates, same sign every time. The interior rule is a real
and quantified sensitivity. **Worth testing proportional erosion and reporting the difference**,
not adopting silently.

---

# R-H. Presentation

Ten minutes to a panel is a different artefact from a report. R2's own evidence is the best guide
we have and it is `OWN`: the most persuasive devices were a **decile-trend plot** and a
**validation table where each row states what it *establishes*, not what it measures**.

The lesson worth repeating because it took four rounds to learn: **render every figure, open it,
and look at it.** That practice found three real defects and **one substantive error — a wrong
physical explanation attached to a correct feature**, which no validation number would ever have
caught because every metric passed identically either way. **The figure was the check on the
prose.** Budget time for the looking.

Register to match, from the strongest teams' own code: an optimum at the edge of a sweep grid
**flagged rather than adopted**; a weight annotated *"PHYSICS PRIOR — deliberately not the
sweep's argmax"*; a bare *"did not replicate, reported anyway."* **That is the register the panel
rewarded.** This round gives us the material for it honestly: two of three look-side predictions
failed, PRED-A failed, and the groundnut-lift test was discarded by its own control.

---

# Shortlist and recommendation

## The recommendation

**A hybrid: an anchor-plus-modifier level, with a SAFY-family growth model carrying substantially
more of the per-plot variance than R2's index did, and an ensemble spread across families as the
uncertainty estimate.** Three crops, three epistemic objects, handled differently and *named* as
different.

| component | choice | why | what kills it |
|:--|:--|:--|:--|
| level | district/state anchor, **adjusted downward for 2025** per A-3, cotton progress from **A-1** | it is the only defensible source of level with no ground truth, and the 2025 adjustment is now sourced and dated | the anchor stays unverified for kharif 2025-26 (P0-11 blocker, still open) |
| per-plot modifier | SAFY-family, 4 free params, GAI proxy from X-band + C-band scaffold | 2 residual df at n=6 (P1-7); designed for calibration without in-situ data | **no X-band feature works as a GAI proxy** (B-1 makes this a live risk) — test first |
| cotton | trajectory shape to ~13 Oct + external picking constraint; **not** 12 Nov brightness | B-3: X-band stops carrying cotton canopy information right at picking | if A-1's first-picking figure cannot be converted to a yield fraction |
| groundnut | near-complete measurement, yield determined ~late Oct (A-6) | 12 Nov is after physiological maturity | — |
| cereals | retrospective reconstruction, **stated as such** | season closed before R2's last date | claiming the new dates improve them |
| uncertainty | ensemble spread across families + conformal if arXiv 2509.10321 delivers | only honest route with no labels | ICP variant needs labels after all → fall back to aggregate-level interval |
| aggregation | Σ(yield×area), spatial-correlation-aware interval (arXiv 2412.16403), **both denominators reported** | 15 points, and nobody else ships an uncertainty column | — |
| witness swap | **promote S1 to temporal scaffold, freeze S2 (20 scenes, incl. same-day 12 Nov) as witness** | S2 is the better late-season witness for the dates that matter | — |

## The three tests that must run before anything is built

1. **Can any X-band feature serve as a GAI proxy?** B-1 says X-band correlates poorly with LAI.
   The whole SAFY recommendation rests on this. **Run it first.**
2. **The WCM re-test (B-6).** The rejection premise has changed and P1-6b's canopy-ordered
   moisture response is the WCM's own central prediction, observed in our data with a bare-soil
   control that is *not* circular.
3. **Does the label carry less of the yield variance than R2's η² = 0.820?** That single number is
   the honest measure of what the SAR contributed, and moving it is the structural fix.

## What is still missing, stated plainly

- **The Gujarat kharif 2025-26 yield anchor**, still open from Phase 0. A-3 gives the direction
  (down) and the national number (463 kg/ha lint), not the state or district figure.
- **The cotton yield split across pickings.** A-1 gives 80% of *first* picking on 10 November; the
  conversion to a fraction of final yield is unsourced.
- **Vadodara's rank within Gujarat** (A-7) — unverified, no supporting evidence found.
- **arXiv 2509.10321** — named, not yet read; it decides whether E-2 is available at all.

---

# Phase 2 addendum — the four gaps, closed

Everything below was listed as missing at the end of the first pass. Three are now answered,
one is answered negatively and stays on the record as unverified.

## ★ ADD-1. The conformal paper, read — and it does not do what we needed

*Flechsig & Pilz, "Conformal prediction without knowledge of labeled calibration data",
arXiv **2509.10321**, 12 September 2025.* `MECH`.

> "We extend the method of conformal prediction beyond the case relying on labeled calibration
> data. Replacing the calibration scores by suitable estimates, we identify conformity sets C
> for classification and regression models that rely on **unlabeled** calibration data. Given a
> classification model with accuracy 1−β, we prove that the conformity sets guarantee a coverage
> of **P(Y ∈ C) ≥ 1 − α − β**… The same coverage guarantee also holds for regression models, if
> we replace the accuracy by a similar exactness measure."

**Read the guarantee carefully, because it is the whole answer.** The method removes the need for
labelled calibration data and replaces it with the need to **know the model's accuracy β**. For a
problem with *no ground truth at all*, β is not a smaller unknown than the labels were — **it is
the same unknown wearing a different hat.** The theorem is sound; it is not a way to get
something for nothing, and it does not claim to be.

**So E-2's optimistic reading is withdrawn.** But the paper is still usable, in a specific and
honest way, because β does not have to come from labels — only from a defensible bound:

- The guarantee is **conservative and monotone in β**. If we can defend an *upper* bound on our
  error rate, we get a *valid* (if wide) interval.
- The arithmetic is unforgiving and must be stated: **a nominal 90% (α = 0.10) with β = 0.30
  delivers a real guarantee of only 60%.** Given P1-5 and §3.1 — six-team κ = 0.060 on the crop
  label, and yield 82% explained by that label — a defensible β for a *per-plot* forecast is
  large. **Per-plot conformal intervals would be too wide to be worth shipping.**
- **Where it does work is the aggregate.** At village scale the label errors partially cancel,
  the district anchor supplies an external check, and β can be bounded from the cross-scale
  reconciliation rather than invented.

**Revised recommendation: use it for the village-level interval, not per plot; state β
explicitly and show the 1 − α − β arithmetic rather than quoting a nominal level.** Showing that
arithmetic honestly is worth more to a Plausibility & Defensibility score than a tighter interval
with a hidden assumption. Ensemble spread (C-6) remains the primary per-plot uncertainty.

## ★ ADD-2. The cotton picking split — found, at source, with its provenance

`THEIRS`, traced to a primary citation. *Technical Report, "Design and Development of a Cotton
Picking Head", SERB/DST-funded; Punjab Agricultural University Ludhiana + ICAR-CICR Nagpur +
CSIR-CMERI Centre of Excellence for Farm Machinery; project completed 31.12.2017.* Quoting:

> "**Sharma and Goyal (1999)** reported that there were **three manual pickings** in a crop season
> at an approximate **interval of 15 days**. The first, second and the third picking constituted
> **35, 50 and 15 %** of the cotton yield respectively."

**Combined with A-1** (Gujarat 80% through *first* picking on 10 November 2025, MOAFW via USDA),
this closes the conversion that was missing:

**Fraction of final cotton yield picked by 10 November 2025 ≈ 0.80 × 35% = 28%.**
**≈72% of the cotton crop was still on the plant two days before our last acquisition.**

**Caveats, and they are real.** Sharma & Goyal is **1999 and Punjab-context** — pre-Bt, and the
north zone plants end-April/May under irrigation while the central zone plants mid-June/July
largely rain-fed (USDA IN2026-0020, Table 1). The 15-day × 3-picking model finishes by mid-
December, whereas §4 has central-zone picking running to January. **Use the 35/50/15 split as the
yield weighting; do not use its calendar.** It is the only quantitative split we could find in
three separate searches, and its provenance chain is credible.

### ★ What this does to Round 2's cotton number — and to what Round 3 must ship

R2 assigned cotton a completion factor of **0.45**, undated and unsourced. On 13 October, four
weeks before Gujarat reached 80% of *first* picking, the picked fraction was necessarily far
below 0.35 — plausibly under 0.10.

**But the two quantities are not the same thing, and that ambiguity is itself the finding.**
"Completion" can mean *fraction of final yield already picked* or *fraction of final yield already
determined* (bolls set but unpicked). For mid-October, 0.45 is indefensible as the first and
arguable as the second. **R2 shipped a column called `yield_estimate_to_date` without fixing which
one it meant.**

**Round 3 must fix it, and the round's own framing forces the answer.** §4: the deliverable is a
**final** yield forecast, not a yield-to-date. So the completion factor's role *inverts* — R2
multiplied down by it; R3 must not multiply down at all. And this hands E-3 a **sourced, numeric
prediction** for the one consistency test only we can run:

> For cotton, **final forecast ÷ R2 yield-to-date should be ≈ 1/0.45 ≈ 2.2** if R2's factor is
> read as a determined-yield fraction, and larger if read as picked. For the three cereals,
> harvested before R2's last date, the ratio should be **≈ 1.0**.

A predicted ratio per crop, fixed in advance from external sources, that our own two rounds can
be checked against. **No other team can run it.**

## ★ ADD-3. The Gujarat kharif 2025 anchor — and Orion's own source, turned around

Phase 0 (P0-11) established that data.gov.in's Gujarat series stops at 2023-24 with no
commercial-crops table. The **area** side is nonetheless now sourced, and it settles more than it
was asked to.

**Gujarat kharif 2025 sowing, as of 4 August 2025** (state government figures, lakh ha):
groundnut **20.41** (116.62% of normal), cotton **20.35**, paddy **7.17** (81.89%), maize **2.64**
(92.82%), bajra **1.53** (83.84%). Total 70.47 lakh ha = 82.35% of the normal 85.57.

**These are the exact numbers in Orion's code comment.** Their `CROP_MIX_REFERENCE` — the
external reference behind the strongest published objection to our crop map — is derived from
this snapshot. **The source is now identified and verified, which means it can be checked against
what they built from it.**

Normalising the five crops to shares of their own total:

| crop | **Gujarat kharif 2025 sowing** | **ours (R1)** | Orion's reference | Orion's shipped map |
|:--|--:|--:|--:|--:|
| Cotton | 39.1% | 43.2% | 32.0% | 13.7% |
| Groundnut | **39.2%** | 30.8% | **16.0%** | 25.9% |
| Rice | 13.8% | 10.6% | 26.0% | — |
| Maize | 5.1% | 6.0% | **18.0%** | **29.1%** |
| Bajra | 2.9% | **9.5%** | 8.0% | — |

**Total absolute deviation from the actual 2025 state sowing profile: ours 23.2 pp, Orion's
reference 60.5 pp.** Sum of (x−s)²/s: **ours 17.8, theirs 67.6.** **Our crop mix is 2.6× closer
to the season's own sowing profile than the reference used to argue against it** — and Orion
derived that reference *from these very figures*, then adjusted it away from them on agro-zone
reasoning. The adjustment moved them further from their own data.

The groundnut:cotton ratio makes the same point in one number: **state 1.00, ours 0.71, Orion's
reference 0.50.** Their objection was that we have too much groundnut. The season the scenes image
had groundnut **surpassing cotton state-wide for the first time**, at 116.62% of normal area,
with USDA independently reporting that Gujarat's lost cotton area "shifted primarily to
groundnut" (A-5). **We sit between the raw state proportion and their prior; they sit further from
the state than we do, in the direction their own source contradicts.**

**Where this cuts against us, stated because it must be.** **Bajra is our weak class: 9.5% against
a state share of 2.9%**, our largest single deviation, and Round 1 independently found real bajra
area in Vadodara close to zero. **If any share in our map should be revised down, the evidence
points at bajra, not groundnut.** That is a concrete, sourced self-correction and it should be
shipped as one.

**And the honest limits.** State ≠ village; a single village may legitimately differ from its
state, which is the premise of dasymetric mapping. Sown area ≠ our plot-share. The 4 August
snapshot is mid-sowing at 82% complete. **None of this settles 30.8% against 16%.** It does
establish that the argument from state sowing, run on the actual state sowing, favours us — and
Orion's objection was itself an argument from state sowing.

## ADD-4. Vadodara's rank — searched twice more, still unverified, mild counter-evidence

Orion's code asserts *"Vadodara ranks 1st in Gujarat for maize yield, 2nd for cotton yield."*

Three independent searches found **no support**. What they did find, all of it about **area or
specialisation rather than yield**: maize specialisation highest in **Panchmahal**; cotton
specialisation highest in **Bharuch and Surendranagar**; Gujarat's major maize belts described as
**Surendranagar, Kutch, Banaskantha and north Gujarat**, with Vadodara absent from the list.

Specialisation is not yield, so this **does not refute** the claim — a district can have modest
area and top yield. **Status unchanged: `THEIRS`, unverified, not to be built on.** The
plausibility test §8 wanted cannot be run until a district-wise Gujarat yield series is obtained,
and P0-11 established that route is closed on data.gov.in.

## ADD-5. Correction to A-3 — the 2025-26 cotton year, stated precisely

The first pass said "2025-26 Gujarat cotton is a below-normal year". The full USDA series
(IN2026-0020, **3 April 2026**) requires a more careful statement. India cotton yield, kg/ha:

| MY | 2023/24 | 2024/25 | **2025/26** | 2026/27 (forecast) |
|:--|--:|--:|--:|--:|
| yield kg/ha | 440 | 464 | **463** | 477 |

**2025/26 finished at 463 kg/ha — essentially flat on 2024/25's 464, not down on it.** The "three
percent decline" in the December report was against USDA's own *earlier projection* for 2025/26
(467), not against the previous year. The rain damage is real and USDA attributes it explicitly —
the 2026/27 forecast rises *"due to recovery from **last year's untimely heavy rains**"* — but it
suppressed the year relative to **potential**, not relative to **history**.

**What it changes for the anchor:** do **not** apply a large downward adjustment to a
historically-anchored cotton level for 2025-26. The correct adjustment is small and negative
against trend. Also confirmed from Table 1: **central zone (Gujarat, Maharashtra, MP) plants
mid-June–July after monsoon onset, largely rain-fed, and is 55% of national production** —
consistent with our 19 June scene sitting at or just before sowing, and it makes Sokhda
rain-fed rather than irrigated, which matters for any water-balance model in C-1.
