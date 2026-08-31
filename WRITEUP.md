# Sokhda kharif 2025 — final yield forecast from six Capella X-band acquisitions

**Round 3 · Team T1 · 966 farm plots, 447.5 ha, Vadodara district, Gujarat**

---

## The one-paragraph version

We forecast **710 t of production over 447.5 ha** for Sokhda's 2025 kharif season, from six
Capella X-band HH SLC acquisitions spanning 6 June to 12 November. The number itself is not
the contribution. **The contribution is that the column contains three different kinds of
object and we say which is which**: cotton (43% of area) is a genuine *forecast* — picking runs
to January and ~72% of the crop was still on the plant at our last acquisition; groundnut (31%)
is a near-complete *measurement*, because its yield was determined at physiological maturity in
late October, inside our observation window; and rice, maize and bajra (26%) are *retrospective
reconstructions*, because their season closed before Round 2's last date and the two new scenes
observe bare soil. Every other team will ship one undifferentiated number.

---

## 1. What changed since Round 2, and what we got wrong

Round 3 gave us two new acquisitions — **29 October** and **12 November** — landing exactly where
Round 2 was weakest. It also gave us the chance to re-audit our own Round 2 work, and that audit
found more than the new data did.

### ★ 1.1 Our Round 2 calibration was wrong, and so was our post-mortem's fix

Round 2 shipped **β⁰ = SF · |z|²**. The correct form is **β⁰ = SF² · |z|²** — the scale factor
applies to the complex amplitude, so power carries its square. Under the unsquared convention
the darkest content in every scene sits **+29.3 dB above the vendor's own declared noise floor**
(`nesz_peak`), which would mean the sensor never reaches its own noise anywhere in a 27 km strip.

Our post-Round-2 note recorded this as settled at "0.35 dB mean absolute error". **We reproduced
that number to three digits — 0.363 dB — and then found it was computed on the wrong quantity.**

| quantity | mean residual vs `nesz_peak` | MAE | scenes **below** the declared floor |
|:--|--:|--:|:--|
| **β⁰** | **+1.86 dB** | 1.856 | **0 / 6 — physically admissible** |
| σ⁰ | −1.08 dB | 1.080 | 6 / 6 — impossible |
| γ⁰ | −0.42 dB | **0.569** | 4 / 6 — impossible |

A scene's darkest pixels cannot be quieter than the noise the sensor declares. **The residual's
sign is a harder test than its magnitude**, and γ⁰'s smaller error was bought by sitting *under*
the floor on four of six dates — tanθ at 28–35° happens to cancel β⁰'s bias. `nesz_peak` is
referenced to **β⁰**, the quantity the product is annotated in. The SF² verdict is unchanged and
strengthened; what changes is that any noise-floor quality gate must be written in β⁰, since in
γ⁰ it would declare a fifth of the scene sub-noise.

**Independent confirmation, three ways:** the vendor's `nesz_peak` on six scenes with six
different scale factors; Capella's own `capella-reader` reference; and Project Orion's published
per-farm γ⁰, which we predicted would sit ~27 dB from ours if they had used the unsquared form.
**They agree with us to 0.7–1.2 dB** — they used the squared convention too.

### 1.2 A number in our own brief does not reproduce

Our Round 2 post-mortem states that the crop label explained **η² = 0.820** of yield variance.
Measured directly from Round 2's shipped `submission.csv` with a single estimator: **0.9248**
unweighted, 0.9305 area-weighted. We report against the value we can reproduce, not the one we
inherited. Round 3 reaches **0.9148** — a 1.0 pp improvement, and we call it modest because it is.

---

## 2. The two new scenes: what they gave and what they cost

### 2.1 Look side — 29 October is right-looking, and it turns out not to matter

29 October is the only right-looking acquisition. A dihedral corner that throws a bright double
bounce to a sensor on one side need not do it from the other, so this could have disqualified the
date from any temporal difference. Measured on persistent stable targets, per target:

| class | pair | n | mean Δ | **sd** |
|:--|:--|--:|--:|--:|
| built-up | **look-reversed** (29 Oct ↔ 12 Nov) | 92 | −0.05 dB | **1.81** |
| built-up | same-look control (19 Jun ↔ 14 Aug) | 77 | +0.38 dB | 1.92 |
| built-up | same-look control (13 Oct ↔ 12 Nov) | 92 | +2.20 dB | 1.90 |
| **water** | **look-reversed** | 231 | +2.87 dB | **2.39** |

Pre-registered kill criterion: the reversed pair must spread ≥1.5× the worst same-look control.
**Ratio 0.944 — the anisotropy hypothesis is dead.** Built-up sits at a flat 1.8–1.9 dB
per-target sd on all three pairs. The stronger form: **water, which is isotropic and physically
incapable of an orientation effect, spreads *more* than built-up on that same pair.** 29 October
enters temporal differences with no correction.

**A caught artefact, reported because it nearly became a finding.** Our first version of this
test defined the stable targets on the four Round 2 dates and evaluated all six — producing a
clean 3.4 dB "drop" on both new dates, in both look directions, exactly the shape a discovery
has. It is selection bias: picking the brightest 0.5% of pixels on dates A–D partly selects
speckle, guaranteeing those pixels come out darker on any date not used to pick them. Rebuilt
out-of-sample on four folds, **the artefact measures +2.59 dB** of the 3.4.

### ★ 2.2 The 29 October scene sits inside a documented agricultural disaster

Water differing by +2.87 dB across the reversed pair was a failed prediction, and chasing it
found the round's largest confound. 29 October is the only date with wind above 10 m/s —
**14.1 m/s against 6.7–9.6 everywhere else** — and wind roughening of smooth water at X-band is
textbook. **Round 2 referenced every date to an in-scene water surface. Carried forward
unexamined, that would have injected ~2.9 dB of wind roughening into a date the forecast leans
on, in the direction that reads as canopy change.**

Behind it is something larger. ERA5-Land at Sokhda shows **81.2 mm of rain over 26–28 October**,
soil moisture rising 0.133 → 0.372, with our overpass on the wet peak. Independently:

> Gujarat, 23–28 October 2025: heavy rainfall **affected 239 talukas across 33 districts**, with
> preliminary estimates of damage to **over 10 lakh hectares** of agricultural land. The state
> cabinet ordered a seven-day crop damage survey.

**So the confound is not a radiometric curiosity — it is a yield-loss mechanism.** Over a million
hectares of standing crop was damaged in that window. A forecast treating 29 October as merely
contaminated misses that the crop itself changed. USDA carries the correction: MY2025/26 Indian
cotton yield revised down 3% to 463 kg/ha, with Gujarat named for *"flooding and waterlogging
during the late-maturity period… boll drop, flower shedding."*

### 2.3 The wetness term is canopy-dependent, so no scalar removes it

We predicted every crop would brighten on 29 October by a similar amount. Every crop brightened —
but by amounts **ordered by canopy cover**:

| crop | 13 Oct → 29 Oct | canopy state |
|:--|--:|:--|
| Cotton | **+0.49 dB** | most standing canopy |
| Rice | +1.07 dB | harvested |
| Groundnut | +1.20 dB | lifting |
| Maize | +2.05 dB | bare |
| Bajra | **+2.60 dB** | bare |

A closed canopy shields the soil from an X-band view of its moisture. This is physically right
and operationally bad: **the 29 October wetness term cannot be removed by a single scene-wide
number.** We excluded the date from the level features and kept it as a moisture observation and
an ensemble member.

---

## 3. Two experiments we ran, and discarded, by their own controls

Both were pre-registered with kill criteria. Both failed. We report them because a control that
can fire is worth more than a result that cannot.

### 3.1 The groundnut-lift test — discarded, and the reason is a constraint on the whole round

29 October and 12 November bracket the groundnut lift. A genuine groundnut field should show a
lifting signature in that fortnight; a mislabelled one should not. Control: the three cereals,
already off-field, must show **no** such signature.

| test | diff | effect size | p |
|:--|--:|--:|--:|
| groundnut vs cereals | +0.109 dB | 0.82 | 0.416 |
| **CONTROL: rice vs maize+bajra** | **+1.274 dB** | **5.86** | **<10⁻⁴** |

**The control fired at twelve times the primary effect**, and it fires in all five inter-date
windows with the sign flipping. The cause: **Round 2's crop labels were themselves derived from
these γ⁰ trajectories**, so contrasting label-classes on the features that produced the labels is
circular. The test is not runnable with our own labels — and neither is any other naive
label-versus-label test on this stack. It is priced, not dead: it needs labels not derived from
Capella, and every candidate on disk is a frozen witness we would have to spend.

### 3.2 The Water Cloud Model — discarded on physicality, then shown to be incapable (§9.1)

The WCM predicts that a soil-moisture change reaches the sensor attenuated by the canopy above
it, by a two-way transmissivity T². §2.3 is exactly that prediction, observed. So we fitted T²
per crop against a bare reference **defined by Sentinel-2 alone** (lowest NDVI decile, same-day,
n = 83) so the control could not be true by construction:

| crop | T² | 95% CI | physical (T² ≤ 1)? |
|:--|--:|:--|:--|
| Cotton | 0.46 | [0.32, 0.60] | yes |
| Rice | 0.65 | [0.46, 0.82] | yes |
| Groundnut | 0.70 | [0.57, 0.91] | yes |
| Maize | 1.14 | [0.92, 1.52] | yes |
| **Bajra** | **1.53** | **[1.27, 1.90]** | **NO** |

**A canopy cannot amplify the soil signal.** Bajra ground rose 3.0 dB where independently-defined
bare ground rose 1.9. Discarded. The diagnosis is the same one §3.1 found: there is a
**soil/field-position term of comparable size to the canopy term** that neither model captures.
Two independent experiments now point at it.

*A caveat on our own design: our second control (ordering across five crops) needed |ρ| ≥ 0.9 to
reach significance and was underpowered by construction. It should not count either way. The
physicality control carried the verdict alone.*

---

## 4. The method

```
yield_forecast[plot] = anchor(crop) × modifier[plot]
production           = Σ (yield × area)          — never a mean of per-hectare rates
```

The **anchor** sets the level per crop, from published statistics adjusted for 2025-26. The
**modifier** distributes it across plots and is normalised so its **area-weighted mean is exactly
1.0 within each crop** — which makes each crop's area-weighted yield equal its anchor by
construction, so the SAR adds spread without moving the level, and its contribution is auditable
as a single number.

**This is a final forecast, not a yield-to-date.** Round 2 shipped a to-date column and multiplied
down by a completion factor; Round 3's deliverable is the final yield, so that factor's role
inverts and survives only as a separate column — which is what makes the consistency check in §6
possible.

### ★ 4.1 Exactly what the SAR decides, and what we inject

The formula above is simple enough to hide something, so we state it explicitly. Inside the
modifier:

```python
v = 1.0 + YIELD_SPREAD * z(hi[m]) / 2.0      # z() has mean 0, sd 1 BY CONSTRUCTION
v = np.clip(v, 0.35, 1.9)
out[m] = v / np.average(v, weights=area[m])  # mean forced to exactly 1.0
```

- `z(hi)` is a **z-score within crop**. Mean 0, sd 1 by construction — so every absolute scale in
  the health index is deleted here. The imagery survives only as an **ordering**.
- `YIELD_SPREAD = 0.30` is **a number we chose**, a stated prior from the literature on
  within-village yield CV. It sets how much spread exists; it is not measured from our data.
- The normalisation then forces the mean to exactly 1.0, deleting any level the ordering implied.
- The **anchor** supplies the level, from a published statistic.

**So every scalar quantity in the deliverable is injected by us. The SAR decides exactly two
things: the ordering of plots within a crop, and which crop each plot is.** That is the complete
and honest inventory of the imagery's role.

**And it cannot be otherwise without labels.** X-band backscatter has no absolute yield
calibration; it can say *plot A looks better than plot B*, never *plot A yields 2.4 t/ha*. That
mapping has to come from somewhere, and with no ground truth it comes from a government
statistic. **A ranking method can rank; it cannot calibrate.** The two exits from this — an
absolute biophysical retrieval (WCM) and a process-based growth model (SAFY) — were both
attempted and both closed on measured evidence, below and in §3.

The consequence is worth stating rather than burying: **the village total is the least
informative thing we ship**, being mostly a published statistic multiplied by our crop map. The
information we added lives in the plot and zone distribution, which is why §7 reports it there.
The compensating strength is that a total this simple has exactly two failure modes — wrong
anchor, wrong crop map — and §7 bounds both externally. A more elaborate total would have more
places to be quietly wrong, with no ground truth to catch it.

### Why not something more ambitious

**SAFY** (semi-empirical light-use-efficiency growth model) was the leading alternative and is
designed almost verbatim for our problem — *"calibrate a simple crop model without resorting to
in situ data"*. We gated it on a test: can any X-band feature serve as the Green Area Index proxy
it ingests? γ⁰ does rank canopy within crop against same-day Sentinel-2 NDVI (**ρ = 0.52 on
cotton on both testable dates**, 0.69 rice). **But only two of six dates have a same-day optical
partner** — the monsoon eliminated usable optical between 11 May and 13 October — and neither
falls in the June–September window SAFY integrates over. **You cannot calibrate a growth model on
a proxy you can only validate after the growth is over.** Killed on availability, not performance.

**Process-based models with data assimilation** (DSSAT/APSIM/WOFOST) were rejected on
parameterisation cost: cultivar coefficients, soil hydraulic profiles and per-plot management for
five crops across 966 smallholder plots with no ground truth. Every input would be invented. A
model we cannot parameterise defensibly is worse than a simpler one we can.

---

## 5. The forecast

| crop | plots | area (ha) | share | anchor t/ha | **forecast t/ha** | production (t) | **epistemic object** |
|:--|--:|--:|--:|--:|--:|--:|:--|
| Cotton | 455 | 193.4 | 43.2% | 0.730 | 0.730 | 141.2 | **FORECAST** |
| Groundnut | 221 | 137.7 | 30.8% | 2.514 | 2.514 | 346.1 | **NEAR-COMPLETE MEASUREMENT** |
| Rice | 86 | 47.4 | 10.6% | 1.690 | 1.690 | 80.2 | retrospective reconstruction |
| Bajra | 149 | 42.3 | 9.5% | 1.910 | 1.910 | 80.8 | retrospective reconstruction |
| Maize | 55 | 26.7 | 6.0% | 2.312 | 2.312 | 61.8 | retrospective reconstruction |
| **ALL** | **966** | **447.5** | 100% | — | **1.587** | **710.0** | three different objects |

**Cotton is reported as lint**, ~34% of the seed cotton a farmer picks, which is why 0.73 t/ha
sits below the cereals. It leads on *area*, not on tonnage.

**Cotton's completion is externally sourced and dated.** The MOAFW weekly report of **10 November
2025** — two days before our final acquisition — put Gujarat at **80% of its *first* picking**.
Indian cotton takes three pickings contributing **35 / 50 / 15%** of yield (Sharma & Goyal 1999,
via CSIR-CMERI). So **≈28% of the cotton crop was in hand and ~72% was still on the plant.**
Round 2 used 0.45 with no dated source at all.

**Groundnut's yield was determined before our last scene.** Physiological maturity is ~135 days
after sowing; kharif sowing on the mid-June monsoon onset puts that in late October. 12 November
is after the determining event — which is what makes it a measurement rather than a forecast.

### Sub-village product

A fixed 500 m grid gives **46 zones** of ≥5 farms. Their health indices span **36.6 to 76.3 —
39.7 points of variation hidden behind the single village row.** Each zone carries an uncertainty
column; the two competitor village summaries we hold carry none.

---

## 6. Defensibility — 19 checks, thresholds fixed before the run

### ★ 6.1 The check no other team can run

Only we have a Round 2 to compare against. Every expected ratio was written down before the
forecast existed.

| crop | R2 yield-to-date | R3 final forecast | ratio | expected | why |
|:--|--:|--:|--:|:--|:--|
| Rice | 1.631 | 1.690 | **1.04** | 0.8–1.3 | harvested before R2's last date — must reproduce |
| Maize | 2.321 | 2.312 | **1.00** | 0.8–1.3 | same |
| **Cotton** | 0.396 | 0.730 | **1.84** | 1.5–4.0 | final vs to-date, still picking |
| Groundnut | 1.931 | 2.514 | **1.30** | 1.0–1.6 | lift essentially complete |
| **Bajra** | 2.675 | 1.910 | **0.71** | 0.5–1.3 | **we corrected its anchor** |
| village | 594.9 t | 710.0 t | 1.19 | ≥1.0 | a final forecast must exceed a to-date |

**All six pass.** The two crops that must not move, don't; the crop that must rise, does; and
bajra falls because we corrected an anchor we had got wrong.

### 6.2 The other checks

| check | result |
|:--|:--|
| village production vs the R2 cross-team spread (578–1268 t over the same area) | **pass**, 710.0 t |
| per-crop yields inside published ranges, cotton in lint | **pass**, all five |
| cross-crop ordering vs agronomy (cotton lowest yield-to-date) | **pass**, 0.20 t/ha |
| degenerate-output assertions (886 distinct yields, 5 crops, health sd 18.9) | **pass**, all five |
| failure-mode regression suite | **12 / 12** |
| cross-implementation radiometry vs Project Orion | r 0.89–0.98, ~1 dB absolute |
| spatial hold-out (weights, rank transfer, witness transfer) | **7 / 9**, see §8 |

### ★ 6.3 The non-circular label test — our labels survive one that dissolved a competitor's

§3.1 proved every naive label test on this stack is circular. Project Orion's residual method is
the fix: regress an independent witness on the SAR ranking axis that produced the labels, then
run the group test on the **residual**.

| | explains raw NDVI | explains the residual | **survives** |
|:--|--:|--:|--:|
| **our labels** | 20.2% (p = 5.7×10⁻³⁶) | **11.2%** (p = 1.1×10⁻²¹) | **55%** |
| Orion's Tier-2 labels *(their reported figure)* | 19% | 0.2% | **1%** |

★ **CORRECTED after Round 3 (see §8).** We ran this metric across all six teams' shipped
Round 2 labels, and the comparison above does not survive: it put our number, computed by us,
against Orion's self-reported figure for a *different* label set. Like-for-like, on their shipped
labels, **we rank last of six** — DeepThinkers 98%, 8bit 97%, CodingBits 92%, Megalodon 90%,
Orion 72%, ours 55%.

The metric does not measure label quality. It measures information **beyond the dominant SAR
axis**, which a labelling built with optical data acquires for free — and three of the six read
as optical-informed (residual η² 0.21–0.26, against 0.11 for the two SAR-like sets). So the
ranking is a **provenance detector**: it says our crop map is the least contaminated by anything
that is not radar. We report the corrected reading because the original was a claim in our own
favour that did not hold.

*Caveat: their figure is their implementation on their labels. The designs match; the
implementations were not cross-checked.*

---

## 7. Uncertainty — and an honest answer about what the SAR contributed

We report four terms separately, because conflating them is how a confidence number stops being
one.

| term | scope | value |
|:--|:--|--:|
| sampling noise (calibrated to 3.4% by split-half, no tuning) | per farm | 5.8 health pts |
| structural — 8-member ensemble, leave-one-date-out | per farm | 0.028 t/ha (2.2%) |
| **structural — same ensemble** | **village** | **0.0 t** |
| crop label, Monte Carlo over **our own** posterior | village | 40.7 t (90% width) |
| **★ crop label, measured EXTERNALLY** — 5 other teams, same 966 farms | village | **236.5 t** |
| **anchor**, calibrated against the district's own interannual spread | village | **385.2 t** |
| label + anchor together | village | 320.0 t → **[598, 918] t** |
| **★ argmax label bias** — directional, not a width | village | **+31.5 t (+4.4%), biased LOW** |

### ★ Both of our uncertainty terms were too narrow, and each was caught by an external control

**The label term was understated ~6×.** Our Monte Carlo samples *our own posterior* — so a
confidently-wrong classifier buys a confidently-narrow interval. It measures our confidence, not
our accuracy. Five other teams labelled these same 966 farms in Round 2, so we re-ran the village
total under each of their label sets, holding our anchors and modifier fixed:

| labels | village total |
|:--|--:|
| consensus (majority vote) | 650.3 t |
| Megalodon · CodingBits · 8bit | 695.0 · 700.0 · 703.7 t |
| **ours** | **710.0 t** |
| DeepThinkers | 722.8 t |
| Orion | 886.8 t |

**Our own posterior says the label is worth 40.7 t. Five independent labellings of the same farms
say 236.5 t.** The check carries its own control: `crop_GDHTM` is our Round 2 labelling and
reproduces the shipped 710.0 t exactly through this independent code path. And the result is
reassuring as well as humbling — four of five other teams land within 2.2% of us (695.0–722.8 t),
so our number is not an outlier; Orion is.

**The anchor term was too narrow too, and still was after we widened it once.** A spread built
from however many published values we happened to find measures our literature search, not the
world. Tested against what a Vadodara kharif yield actually does year to year (district APY
1997–2012, 15–16 seasons per crop):

| crop | our source spread (CV) | district interannual CV | |
|:--|--:|--:|:--|
| Groundnut | 0.152 | **0.491** | too narrow — and it is 49% of village production |
| Cotton | 0.180 | 0.397 | too narrow |
| Maize | 0.095 | 0.243 | too narrow |
| Rice | 0.284 | 0.332 | comparable |
| Bajra | 0.243 | 0.283 | comparable |

For the three that failed we adopt the district's measured 1-sd envelope. That is a percentage
applied to a base — the exact practice criticised above — with the difference that is the whole
point: **the percentage is measured from this district's own history, not chosen to look
reasonable.** The envelope is unconditional and includes catastrophic seasons; we keep it wide
because our own 29 October scene sits inside a state-declared disaster, so this is not a year to
assume the benign tail away.

### Why "both" is narrower than "anchor alone"

The combined interval (320.0 t) is *narrower* than the anchor interval (385.2 t), which looks
impossible. It is a real interaction. Each Monte Carlo draw takes **one anchor per crop** and
applies it to all of that crop's area, so a concentrated allocation is more exposed to any single
draw. Our argmax labels are a concentrated portfolio — Herfindahl **0.305**, against **0.235**
for the posterior — so resampling labels diversifies the anchor exposure and partially cancels
it. Concentration in the crop map amplifies anchor risk.

### Two corrections we made to this table after first publishing it

**1. The anchor term was too narrow, because we had padded it — and it took two passes to fix.**
Rice and Maize each carried a single source plus an invented ±15% bracket, sitting directly
beneath a comment claiming every entry was "a real number from a real source". Replacing that
padding with the Gujarat State First Advance Estimates for kharif 2024-25 (rice 2537.97, maize
2022.15 kg/ha) took the anchor term 158.2 → 187.4 t. **That was still not enough**: the
calibration control against the district's own interannual spread, below, then took it
187.4 → **385.2 t**. Reality was wider than the padding at both attempts — rice's independent
value alone sits 50% above the district base. We were understating our uncertainty on 26% of the
village, and then still understating it on 49% more.

The same source also **corroborates a correction we already shipped**: it puts bajra at 1786.66
kg/ha — a fourth independent estimator near 1.9, and nowhere near the 2714 cell we rejected.

These are STATE figures, so by the rule already applied to groundnut they are carried as spread
and **not adopted as anchors**. They move rice and maize in *opposite* directions, so there is no
single state-vs-district offset to correct for.

**2. The label term is a bias, not only a spread — and we nearly mis-diagnosed it.** The
label-only interval [721.2, 761.9] does not contain the point estimate of 710.0; it sits entirely
above it. Our first hypothesis was an artefact: the modifier is normalised within crop, so
resampling labels while holding the shipped modifier fixed breaks that normalisation.
**Renormalising inside the Monte Carlo made the gap slightly larger, not smaller — the hypothesis
was wrong.** (The renormalisation is kept regardless, because it is the correct MC.)

The real cause is argmax. With 69.4% of farms carrying no class above p = 0.5, argmax
concentrates area into whichever classes win most often — Cotton −35.1 ha, Groundnut −36.5 ha —
while the posterior spreads it into Maize (+36.8 ha) and Bajra (+22.5 ha), which carry higher
anchors:

| | argmax (shipped) | posterior-mean |
|:--|--:|--:|
| village production | **710.0 t** | 741.5 t |

**So the shipped number is biased low by 31.5 t, and we can state the sign and the size.** We
report rather than correct it: the deliverable needs one crop label per farm, and a village total
that disagreed with the sum of its own farms would be a worse defect than a stated bias.

### ★ The zero is the finding — and then we found our statement of it was wrong

**The ensemble moves the village total by exactly 0.0 t across eight genuinely different modifier
constructions.** That is not a bug. The modifier has area-weighted mean 1.0 within crop, so it
cannot move the village total. For two rounds we drew the obvious conclusion and wrote *"at
village level the SAR contributes nothing to the total."*

**That sentence is wrong, and it understates our own work.** Write the total out:

```
village total  =  SUM over crops of    anchor_c    x    area_c
                                      ----------       --------
                                      published        a SAR
                                      statistic        PRODUCT
```

The anchors are government yield statistics we did not produce. **The areas are determined
entirely by the crop map — and the crop map is made from these same Capella trajectories.** That
is not a convenient reinterpretation; it is the documented fact that makes every naive label test
on this stack circular (§3.1), and it is why our own groundnut-lift control fired at 12× the
effect. **The SAR supplies one of the two factors in the product.**

So the SAR reaches this forecast through three channels, and only one is zero:

- **the crop map** — worth **236.5 t** of village-total spread, measured externally;
- **plot level** — all of the within-crop spread. ★ **The ρ ≈ 0.5 validation is of the same-day
  γ⁰ *feature*, not of the composite health index we ship** (see §8): the index itself sits at
  ρ ≈ 0.09 area-weighted against an independent
  same-day sensor;
- **zone level** — all 39.7 points of between-zone variation;
- **the modifier** — **0.0 t**, zero *by construction* because we normalised it that way, not
  because the imagery failed.

The real limitation of anchor-plus-modifier is narrower than we had been stating it: **the SAR
does not set the LEVEL.** A published statistic does, and that anchor is the single largest thing
we are unsure about, at **385.2 t**. We report the correction because it ran against us: a team
that only ever finds errors flattering to itself is not auditing, it is marketing.

### On conformal prediction

Recent work extends conformal prediction to unlabeled calibration data, proving coverage
**P(Y ∈ C) ≥ 1 − α − β** where β is the model's error rate. It removes the need for labelled
calibration data and replaces it with the need to *know β* — and with no ground truth, β is the
same unknown wearing a different hat. Our dominant error is the crop label, and six-team κ = 0.060
bounds *disagreement*, not error.

**So we do not quote a confidence level. We publish the arithmetic:** a nominal 90% interval
guarantees 90% − β, which at a label error rate of 0.30 is **60%**. Showing that honestly is worth
more than a tighter interval resting on a hidden assumption.

### Spatial correlation

Moran's I on the yield residual is **0.083 (z = 7.4)** — plots are not independent, so any
sub-village interval computed under an independence assumption would be too narrow.

That is a statement about variance estimation only. **§9.8** asks the question it does not:
spatial correlation *caused by what*, and does it mean the per-farm ranking is really a soil
map. It is not — 91% of the ranking is field-scale, and the correlation survives removing both
incidence angle and the bare-soil baseline.

---

## 8. What we got wrong, and what we still do not know

★ **Our headline claim is the least independently verified thing we ship.** The three
epistemic objects — cotton a forecast, groundnut a measurement, the cereals a reconstruction —
rest entirely on published crop calendars and, for cotton's completion fraction, on a 1999
paper. We tried to verify it against data with per-plot harvest detection from 16 Sentinel-1
dates, and **the test failed its own controls** (§9.6): the crops do not separate (p = 0.86) and
the detected order reshuffles randomly between subsets, because the median parcel is 28
Sentinel-1 pixels. That is not evidence against the split — it means we could not test it, and
the reader should know that the claim we lead with is the one carrying literature rather than
measurement behind it.

**Reported because a panel will find them anyway, and because two of them are our own errors.**

1. **Our Round 2 calibration was wrong** (§1.1), and our post-mortem's confirmation of the fix
   was computed on the wrong quantity.
2. **A headline number in our own brief does not reproduce** — η² 0.820 vs a measured 0.9248 (§1.2).
3. **We nearly shipped a selection artefact** as a look-side finding; +2.59 dB of a 3.4 dB effect
   was the artefact (§2.1).
4. **Our bajra share is probably too high.** Gujarat's actual kharif 2025 sowing profile gives
   bajra **2.9%** of the five-crop area; we assign **9.5%**, our largest single deviation, and
   Round 1 independently found Vadodara bajra near zero. **If any share in our map is wrong, the
   evidence points at bajra.** We volunteer this rather than defend it.
5. **The spatial hold-out fails 2 of 9 checks**, both on the GLCM texture residual, whose
   out-of-sample dependence on plot size runs to ρ = −0.40. **That feature does not enter the
   shipped index** — verified, not asserted — but the failure is real and reported.
6. **Coverage is crop-biased on every date.** The north-west swath edge cuts the same block of
   cotton plots every time; **29 of 455 cotton plots have never been observed by this sensor**.
   Under 1% of area, but every per-plot "cotton mean" is on a systematically incomplete sample.
   29 October's mirrored swath loses **5.01% of village area**.
7. **We cannot produce a clean reserved scene**, and say so rather than claim one: 29 Oct and
   12 Nov set design decisions, and Round 2 used 13 Oct S2 both as a headline witness and to
   correct a term's sign. We publish the contamination ledger instead.
8. **No Gujarat kharif 2025-26 *yield* anchor exists** that we could find — data.gov.in's state
   series stops at 2023-24 with no commercial-crops table. Area is sourced; yield is not.
9. **The competitor claim that Vadodara ranks 1st in Gujarat for maize yield** is unverified
   after three searches. We did not build on it.

### On the groundnut dispute

A competitor argued our 30.8% groundnut share should be ~16%, from a `CROP_MIX_REFERENCE` derived
from Gujarat's 2025 state sowing figures. We obtained those same figures. Normalised across the
five crops:

| | GJ kharif 2025 sowing | **ours** | their reference |
|:--|--:|--:|--:|
| Cotton | 39.1% | 43.2% | 32.0% |
| **Groundnut** | **39.2%** | **30.8%** | **16.0%** |
| Rice | 13.8% | 10.6% | 26.0% |
| Maize | 5.1% | 6.0% | 18.0% |
| Bajra | 2.9% | 9.5% | 8.0% |
| **total absolute deviation** | — | **23.2 pp** | **60.5 pp** |

**Groundnut surpassed cotton in Gujarat for the first time in 2025, at 116.62% of its normal
area**, and USDA independently reports that Gujarat's lost cotton area *"shifted primarily to
groundnut"*. Their reference was built from these figures and then adjusted away from them.
**This does not settle 30.8% against 16%** — a village may legitimately differ from its state,
and sown area is not plot share — but the argument from state sowing, run on the actual state
sowing, does not favour the objection.

---

## 9. Ten approaches we built after the forecast was frozen

Everything here was built **after** the deliverable was final, against controls fixed in
advance, and **none of it changed a shipped number.** That is the point: with the forecast
frozen, every one of these could only tell us something true, never make our number look
better. Four were rejected by their own controls; a fifth won its comparison and was then
voided by a provenance test we built to catch exactly that; one could not be run at all.

| § | the question | verdict | what it left behind |
|:--|:--|:--|:--|
| 9.1 | Can the Water Cloud Model be fixed and retried? | **killed — unidentifiable** | a one-line test for any model with more parameters than observations |
| 9.2 | Can SAFY's canopy proxy work on this stack? | **killed on availability** | the signal decays ~35% in 6 days — the revisit cadence assimilation would need |
| 9.3 | Should we fuse six teams' crop labels? | **won, then voided** | our referee cannot separate *more correct* from *saw another instrument* |
| 9.4 | Does adding Sentinel-1 C-band improve the forecast? | **real information, rejected** | better on the date we looked at, worse on the held-out one |
| ★ 9.5 | Was 2025 an ordinary year at Sokhda? | **survived** | the only result in three rounds where radar constrains the **level**, not the ordering |
| 9.6 | Can we test our own harvest-timing claim? | **could not be run** | our epistemic split still rests on published calendars, and §8 now says so |
| ★ 9.7 | Is Sokhda typical of the district whose statistic we borrow? | **survived as a flag, not applied** | a second independent reason to think 710 t is conservative |
| ★ 9.8 | Is the ranking the farm, its **location**, or its **outline**? | **survived — good news** | 96% field-scale, no parcel-size bias: what licenses per-farm advice at all |
| ★ 9.9 | What did each of the six acquisitions actually buy? | **survived, and shrank a claim** | "a peak-canopy index with temporal corrections", not "a season-long trajectory model" |
| ★ 9.10 | Would the same 97 farms be named if we re-flew? | **survived** | a stability column on the attention list — 30 of the 97 names are not stable |

**9.5, 9.9 and 9.10 are set out in full below; the rest are summarised.** Every one of them,
including the discarded ones, is written up at full length with its controls and its dead ends
in `internal/RESEARCH_LOG.md` (entries P3-14 to P3-23).

**An access note that made three of them possible.** Our Earth Engine credential was dead — a
stale project, and a refresh token minted by a different OAuth client. Microsoft's Planetary
Computer serves Sentinel-1 RTC (terrain-corrected γ⁰ at 10 m) through a STAC API with an
**anonymous** SAS endpoint. No account, no key. It replaced the blocked path entirely.

### 9.1 The Water Cloud Model was never capable of contributing

§3.2 killed it on physicality (bajra T² = 1.53; a canopy cannot amplify a soil signal), which
left "fix the model and retry" open. This closes it: **ρ(rise_db, T²) = +1.000, exactly, across
all five crops.** With one difference per crop and several free parameters the model is
**unidentifiable** — one degree of freedom of data, so T² is pinned by `rise_db` alone, a
perfectly monotone relabelling of the input we already had. ρ(NDVI, T²) and ρ(NDVI, rise_db) are
both −0.500, identical to machine precision. **Even if the physics had passed it would have
added nothing.**

The general form is worth more than the instance: *a model carrying more free parameters than
observations per unit returns a monotone relabelling of its input, and will look physical while
adding zero information.* The tell is a rank correlation of 1.000 against the raw quantity. One
line to check, and we now check it.

### 9.2 SAFY's proxy is real; the kill was availability, and it has a rate

γ⁰ against same-day Sentinel-2 NDVI within crop **replicates**: cotton **0.518** on 13 October
and **0.522** on 12 November — 30 days apart, in very different crop states, agreeing to 0.004
(rice 0.690 and 0.561). So the proxy works. What fails is the calendar. Measured against 29
October, whose nearest optical partner is 6 days away, **the canopy signal loses a third of its
strength in six days** (bajra −33%, cotton −36%, groundnut −41%, rice −37%) — and there is no
same-day optical anywhere in the June–September window SAFY integrates over. Correctly killed,
now for a measured reason. The decay rate is the keeper: it sets the revisit cadence any future
X-band assimilation over this village would need, and it justifies weighting dates rather than
interpolating between them.

### 9.3 Dawid-Skene label fusion — it won, and the provenance control voided the win

Six teams labelled these same 966 farms. Dawid and Skene (1979) EM recovers latent labels **and**
a per-team confusion matrix with no ground truth — the right tool, since majority vote assumes
equal reliability and independent errors, both false here. It ran clean, beat everything on
§6.3's referee (residual η² **26.3%** against our 11.2%) and survived three controls, including
an out-of-sample one on the 12 November witness where the margin *widened*.

**Then the fourth control killed the comparison.** §6.3's referee removes the *SAR* axis; it does
not remove an *optical* one, and that non-circularity is a property of **our** pipeline, not of
the test. Per-team residual η²: 21.9%, 26.0% and 20.6% read as optical-informed against 11.6%
and 11.2% for the two SAR-like sets. Dawid-Skene fuses all six and **inherits a sensor our labels
never saw**, so the referee cannot separate *more correct* from *saw another instrument*.

Not adopted, on four grounds: unverifiable with any tool we hold; it would change **509 of 966**
farms three days from the deadline; it makes our crop map depend on competitors' work; and it
destroys the SAR-only provenance that §6.3 shows is our actual differentiator.

### 9.4 X-band + C-band fusion — real extra information, rejected by its control

Sentinel-1 gives **16 dates on a single track** (descending, relative orbit 34), nine of them in
June–September, cloud-free, against Capella's three. It is still SAR, so fusing it preserves the
provenance claim — we would not add an optical product for exactly that reason. The extra
information is real: partial ρ against the witness after removing Capella γ⁰ is **cotton +0.346**
(p = 1×10⁻¹²) and **groundnut +0.362** (p = 3×10⁻⁸), 85% of village area.

But information about a witness is not improvement of a forecast:

| | 13 Oct witness | 12 Nov witness (**control**) |
|:--|--:|--:|
| shipped | −0.022 | **+0.090** |
| fused | **+0.140** | +0.068 |

Better on one date, worse on the other. **A change that only helps on the date you looked at is
the oldest mistake there is.** Not adopted. Confirmed on the way through: the village total is
*invariant* under fusion — 710.0 t both ways, difference 0.000 t — so fusion could only ever have
moved the distribution, never the total.

### ★ 9.5 A nine-year radar climatology — the one that survived

**This attacks the thing §4.1 says is impossible.** Absolute yield calibration needs a label,
which is true *within* a season. Across seasons it is not:

> Absolute level needs a **label** — we have none.
> **Relative** level needs a **history** — Sentinel-1 has nine years over this village.

And it lands in a gap we declared ourselves: four of five crops carry `adj_2025_26 = 1.00` with
the stated reason that no kharif 2025-26 statistic exists. **That 1.00 is an assumption that 2025
was an ordinary year at Sokhda**, and nothing published at district or state level can test it
for one village.

It is possible because **every Sentinel-1 scene over Sokhda in June–September, in every year from
2016 to 2025, is on one track.** Nine years with no look-side or incidence mixing — the confound
that normally dominates multi-year SAR comparison is absent here. Checked, not assumed: the
October–November window is *not* single-track (2019 carries ascending 71), and those scenes are
dropped rather than trusted.

**Every year is measured twice** over the same scenes — farm pixels as signal, non-farm pixels in
the same AOI as control — because a multi-year radiometric comparison can drift from calibration,
from the S1B failure in December 2021, or simply from a wetter year:

| growing season, 2025 vs 2017–2024 | z |
|:--|--:|
| VH farm, raw | **+1.20** — reads as "bright year, good season" |
| VH non-farm (**control**) | **+1.39** — the landscape moved *more* |
| **VH farm − non-farm** | **−0.16** |

**The control reversed the naive reading.** Reporting the raw farm anomaly would have announced a
good season from what is landscape-wide soil moisture.

The differenced result is a *positive* finding, not a null: **the 2025 growing season at Sokhda
was statistically ordinary**, so `adj_2025_26 = 1.00` stops being an admitted assumption and
becomes a village-specific measurement.

**And the late season separates cleanly from it.** Rerun over 1 October – 15 November:
**z(farm − non-farm) = −1.62.** The landscape brightened on wet soil (+1.01) and the farms did
not keep up (+0.48) — so relative to their own normal relationship with the surroundings, the
parcels went *darker*. Growing season ordinary, late season anomalous: **independent nine-year
support for the October damage account** we had until now sourced from ERA5 and a news report,
and corroboration of the epistemic-object split — the crop grew normally, then was hit after
groundnut matured but while cotton still stood.

*Honest limits, because −1.62 is not decisive:* n = 8 climatology years; only 2–4 scenes per year
in that window against 7–10 in the growing season; VH is a weak yield proxy; and 2019 sits at
−0.41 against 2025's −0.42, so 2025 is the most negative of nine years but only marginally beyond
2019. **Suggestive, not established — and used to adjust no anchor.**

---

### 9.6 Harvest detection — a test of our OWN headline claim, and it could not be run

Slide 1 and our opening paragraph rest on the three epistemic objects, and every part of that
split comes from **literature**: published crop calendars, and for cotton a picking split from
Sharma and Goyal (1999). Three rounds without one test against data. The 16-date Sentinel-1
series should be able to test it, since harvest removes canopy and moves VH sharply. The
prediction was written down before the run and is purely ordinal — **rice, maize and bajra
earliest; groundnut later; cotton latest** — and detection ran on each plot *minus* the per-date
village median, because 81.2 mm of rain fell on 26–28 October and a naive detector would
otherwise report a spectacular village-wide harvest on 3 November.

**It failed its controls, and we report it as failed.** Do the crops separate at all?
Kruskal–Wallis **p = 0.86** — they do not. Is the order agronomic? `Maize < Bajra < Groundnut <
Rice < Cotton` **contradicts** it. Does one date dominate, the rain leaking through? No, 20.7% —
that control passed. It is not plot size alone either: restricting to larger parcels does not
recover separation (top 50% p = 0.93, top 25% p = 0.32, top 10% p = 0.49) and **the detected
order reshuffles randomly between subsets**, the signature of noise rather than a weak real
signal. The median parcel here is **28 Sentinel-1 pixels**, and a steepest-single-drop estimator
on 16 noisy points at that size carries no timing information.

★ **What this does not show.** A failed test is not evidence against the hypothesis. This does
not refute the epistemic-object split — it means we could not test it this way. The split still
rests on published calendars, which is a weaker footing than we would like, and §8 now says so.

### ★ 9.7 Is Sokhda even typical of the district whose statistic we borrow?

§9.5 tested whether *2025* was an ordinary **year** at Sokhda. It never touched the assumption
underneath the anchor itself: **village yield = district average yield.** That is a Vadodara
*district* statistic applied to *one village*, and it carries 385.2 t of the interval — more than
every other term combined. If it is wrong it is a **bias, not a spread**, and widening an
interval hides a bias rather than fixing it.

Radar can test it, because the comparison is *relative* — the one thing §4.1 establishes a
label-free method can do. The surrounding 22 km is cut into blocks of **Sokhda's own size**
(2.1 km ≈ 441 ha), each averaged over cropland pixels only (ESA WorldCover 2021), giving **271
like-sized, like-land-use neighbours**. Sokhda is one draw from that distribution — and it sits
above it **every year**: +1.41 dB in 2017 (91.9th percentile), +1.85 in 2018 (91.9th), +1.50 in
2019 (85.2nd), +1.05 in 2025. **Roughly the top 10–15% of its own cropland landscape.**

**The control that could have killed it.** Sokhda was measured over *surveyed parcels*, its
neighbours over *classifier-labelled cropland* — different objects, since a classifier sweeps in
margins, tracks, bunds and fallow, all darker than a cultivated field. The masks genuinely
disagree: 11 153 parcel pixels against 13 757 WorldCover-cropland pixels in the same hull,
**overlapping on only 7 191**. So we re-measured Sokhda *the neighbours' way*: offset +1.051 dB
by parcels, +1.007 like-for-like, a **definition effect of +0.044 dB**. The two conventions
disagree on a third of the **area** and agree on the **radiometry**. The offset is not a masking
artefact.

**★★ And the confound we cannot resolve — which is why this is a flag, not a correction.** VH
backscatter differs **by crop**. Sokhda is 43% cotton and 31% groundnut; the surrounding
landscape's crop mix is unknown to us, because we hold labels for 966 parcels and for nothing
outside them. So "brighter than its neighbours" has at least two readings: **(a)** Sokhda's crops
are genuinely doing better than the district, so the anchor **understates** us; or **(b)** Sokhda
simply grows more of a *brighter crop*, so the anchor is fine and this is crop mix. **Nothing we
hold separates them** — classifying the surrounding landscape would need a crop map we could not
validate, and the entire reason the anchor exists is that we have no yields.

So this is **reported as a directional flag on the anchor and not applied.** It joins the argmax
label bias (§7, +31.5 t) as a second, independent reason to think **710 t is conservative rather
than optimistic** — both stated rather than corrected, because a correction we cannot verify is
worth less than a bias we can name.

---

### ★ 9.8 Is the ranking about the farm — or about where it sits, or how it is drawn?

**Figures:** `p3_f6_spatial.png`, `p3_f9_edge.png`

Every approach in this document ranks a parcel as an independent unit. Two ways that ranking
could be an artefact, and neither had ever been tested:

> **location** — if it is a smooth landscape gradient (soil, water table, canal command), the
> advice a farmer reads off it is *"your location is poor"*, which no in-season action changes.
> **outline** — the median parcel here is **69 pixels, about 8×8**, so a one-pixel border is
> *half of it*, and every border pixel mixes the farm with the bund, the track and the
> neighbour. That corrupts `level`, and it *inflates* `uniform` — our **largest weight, 0.249** —
> because a mixed border reads as a patchy stand, which reads as a sick field.

Both were attacked separately, and both came back the same way.

**Location.** Within-crop standardised health residual over the 966 centroids; row-normalised
inverse-distance weights to 400 m (mean 48.9 neighbours, no parcel isolated); empirical variogram
to 1.6 km plus Moran's I against a **within-crop permutation null** (999 shuffles) — shuffling
*inside* crop is what makes the null test location rather than crop identity.

A null result is worthless unless the method demonstrably detects the thing when present, so the
same variogram runs on **incidence angle**, which varies smoothly across a single Capella scene
*by construction*:

| series | nugget | structured fraction | range |
|:--|--:|--:|--:|
| health-index ranking (subject) | 0.92 | **0.07** | ~250 m |
| incidence angle (**positive control**) | 0.03 | **0.94** | **>1400 m, still rising** |
| June bare soil (control) | 0.64 | 0.24 | ~75 m |

**The positive control never reaches its sill inside the village** — its structure runs off the
edge of the AOI. The method sees landscape gradients loudly. The ranking is flat from the first
bin: **93% nugget, essentially all field-scale.** (Incidence's range is reported as a lower bound,
not a number; the curve is still climbing at the last lag. The figure caught that — the tabulated
"~1400 m" looked like a measurement until it was plotted.)

And the correlation is neither the sensor nor the dirt. Moran's I is **+0.0727** raw (null
−0.0013 ± 0.0091, z = +8.1, p = 0.001), **+0.0615** after regressing out incidence, **+0.0624**
after removing incidence *and* soil — both confounds cost 14% of the statistic and none of its
significance. Decomposing the confound-free residual into a neighbourhood mean (self excluded)
and the contrast against it: **9% is where the farm is, 96% is the farm itself.** (They exceed
100% because the components are slightly anticorrelated, cross term −0.046.)

**Outline.** The **shipped** rasterisation split into two disjoint per-farm pixel sets — `core`,
pixels whose four neighbours belong to the same farm, and `ring`, everything else — and the index
rebuilt from cores alone by the shipped index function. The first number is the alarming one:
**the median parcel is 45% boundary pixel, and 75 farms have no interior pixel at all** (under
20 px: 100% boundary; over 150 px: 23%).

Core has fewer pixels than the parcel, and fewer pixels alone moves a mean and biases a CV. So
the split is measured against a null that discards **the same 37 861 pixels at random**:

| | drop the boundary | **control: same count, at random** |
|:--|--:|--:|
| rank ρ with shipped index | 0.853 | **0.857** |
| attention list retained | 0.639 | **0.680** |
| median \|level change\| at peak | 0.484 dB | 0.314 dB |

**The pairs coincide.** The boundary carries a real level offset — 1.5× the null — that does not
reach the ranking. On `uniform` specifically, the part §9.10 could not test, core-only lowers the
CV by **4.9%** against **1.0%** for the null: the edge does inflate our uniformity measure, by
about four points of CV beyond sampling, but not enough to reorder anything.

Two controls with known answers guard it. Core and ring partition the shipped pixel set by
construction, so their union must reproduce `p1_farm_features.csv` — max error **3.6e-15 dB**,
ρ = 1.0000. And a known **+3.000 dB** injected into ring pixels must be recovered exactly.
**That second control failed as first written**, at 1.94e-07 against a 1e-9 threshold. The two
candidate causes were not assumed apart: a mask addressing the wrong pixels would miss by a
*fraction of 3 dB in any precision*, so the identical check was re-run in float64, where it
returns **7.1e-15**. Both numbers are reported and both thresholds are enforced.

### What this licenses us to say

**Significant is not the same as large.** z = +8.1 is overwhelming evidence the spatial
correlation is real; I = +0.073 says it is small, and the second is what matters for the product.
§7's use of the statistic stands unchanged — a sub-village interval still must not assume
independence. But the two worries it did not address, that we might be selling farmers a soil map
with a radar badge on it or a map of our own parcel outlines, **do not survive the test**: 91% of
what we rank is the field rather than its neighbourhood, and ρ(index, boundary fraction) is
**+0.020**.

That last one has a consequence worth stating on its own. Boundary fraction is very nearly a
deterministic function of size (ρ = **−0.981** against pixel count), so we checked it directly:
**ρ(index, parcel size) = −0.017.** Across a 40× spread in farm area, **our health index carries
essentially no parcel-size bias** — which in a smallholder village is the fairness property the
product needs, and the one it would have been easiest to fail silently.

This is the only approach here whose answer is good news, and it is what validates the
**premise** of the sub-village deliverable rather than one of its numbers. It could have gone the
other way: had the subject variogram looked like the incidence one, or had the pairs in that
table come apart, the per-farm advice list would have been indefensible and we would have had to
say so.

**One concrete thing it changes, and one honest residual.** Ranking on the actionable component
instead of the raw index reorders the bottom decile — **75 of 97 farms are shared, 22 change** —
and those 22 are farms flagged as poor mainly because their *neighbourhood* is dark. We report it
as `actionable_rank` in `p3_spatial.csv` and **do not substitute it**: the shipped list was
frozen, and a 9% correction to a ranking we cannot validate against yield is not worth breaking a
freeze for. The residual: `uniform` is measurably edge-inflated, and 75 farms are pure boundary
with no interior measurement in anything we ship. The village total is untouched by construction
and re-verified at **710.0 t**.

---

### ★ 9.9 What did each of the six acquisitions actually buy?

We were **given** six Capella scenes and we used all six. In three rounds nobody asked what
any single one of them contributed. That gap matters because the answer decides which
sentences we are entitled to say. If the shipped ranking is recoverable from one date, then
growth, persistence and senescence are decoration and *"we tracked the crop through the
season"* is not a claim we own.

**★ The control has a known answer, and it runs first.** 29 October is already excluded from
the primary index — `LEVEL_DATES` drops it and with `use_29oct=False` it enters no part, not
even the integral. So leave-one-date-out on 29 October **must** return Spearman exactly
1.0000 with zero farms moved. It does. Anything else would have meant the harness was wrong
and every number below was void; the run aborts on failure rather than reporting.

**Q1 — drop one date and rebuild.** Ranking agreement with the shipped index, and farms
leaving the 97-farm bottom-decile attention list:

| withheld | ρ | farms leaving the attention list |
|:--|--:|--:|
| 6 Jun | 0.9993 | **1** |
| 19 Jun | 0.9481 | 17 |
| **14 Aug** | **0.2108** | **77** |
| 13 Oct | 0.8935 | 24 |
| 12 Nov | 0.8589 | 26 |

**14 August *is* the index.** Remove it and four-fifths of the attention list changes. And
**6 June bought one farm** — a design fact we had never stated: level, uniformity and growth
all key on 14 August and 19 June, so 6 June enters through the trapezoid integral alone.

**Q2 — how many scenes do we need?** Greedy forward selection: **one scene reaches ρ = 0.857**,
two 0.874, three 0.895, and then **four reaches 0.9993**. That jump is mechanical, not fitted:
senescence is a slope through the late dates and **does not exist until a second late date
arrives**, so it switches on exactly when 13 October joins 12 November. This is the cleanest
justification we have for Round 3's two extra scenes — they did not add another look, they
made a *derivative* measurable.

**Q3 — does the index use the time axis at all?** Permute which physical scene sits in which
calendar slot, 200 times, and rebuild. Growth, persistence and senescence are all defined by
ordering, so a correctly built index must move — and the control confirms the permutation
disturbed the temporal parts in **200 of 200** draws.

> **ρ(shuffled calendar, shipped) = 0.312, 5–95% range [−0.045, 0.885].**

**Destroying the time axis costs more than deleting four of the five scenes.** The trajectory
machinery is doing real work. Honesty about the band: its top edge, 0.885, is above the
best single-date score of 0.857, because some shuffles happen to leave the peak date in place.
We show the whole band rather than the mean alone for that reason.

**What we are now entitled to say:** the shipped index is a **peak-canopy index with
temporal corrections** — not a season-long trajectory model. One scene gets the broad
ordering; the other four are what fix roughly a third of the attention list and what make
senescence exist at all. That is a smaller claim than "we tracked the crop through the
season", and it is the one the data supports.

**A latent fragility this found in the shipped code, which we are not fixing.** `derive_weights`
takes a Spearman correlation matrix. A part with **zero variance** makes its column NaN, and
the row sums propagate that NaN into **every** weight — so one dead part silently turns the
whole index into a constant 50. Thin date subsets produce exactly that (growth with no pair,
senescence with one late date), which is how it surfaced: a variant scored ρ = NaN. With the
delivered six dates no part is degenerate (minimum part sd = 1.08, all weights finite,
verified), **so the shipped run is unaffected** — but the failure mode is silent, which is the
dangerous kind. The guard lives in `p3_voi.build()`; `p3_build.py` is frozen and untouched.

The village total is invariant by construction and asserted, not assumed: the worst
within-crop area-weighted modifier mean deviates from 1.0 by **3.3 × 10⁻¹⁶** across every
variant.

---

### ★ 9.10 Would the same 97 farms be named if we re-flew the mission?

**Figure:** `p3_f8_speckle.png`

§9.8 asked whether the ranking is about the farm or its neighbourhood. §9.9 asked what each
scene bought. Neither asked the question a farmer would ask first:

> how much of my rank is the radar measuring my field, and how much is speckle?

This is **not** the ensemble spread already in §7. That resamples our *modelling* choices —
which features, which weights, which dates. This resamples the **measurement**: same crop,
same sensor, same day, a different realisation of speckle. It is the only error source here
we can compute from first principles rather than argue about, and it had never been
propagated into the ranking.

It bites harder here than it would elsewhere because **these parcels are tiny.** Median farm:
**69 pixels**; 159 farms have fewer than 20 on the peak-canopy date. The relative standard
error of a speckle mean over N independent looks is 1/√N, so the median farm's own brightness
is known to about **12%** before any question of whether the model is right.

**Method.** The mean of N independent single-look intensity samples is Gamma-distributed with
shape N, so each farm-date is perturbed by a multiplicative u ~ Gamma(k, 1/k) with k = npix ×
F, applied to the linear and dB means together. The index is then rebuilt **by the shipped
`p3_build.health_parts`**, not a reimplementation, and the attention list recomputed. 500
replicates at each of three noise levels, because the number of independent looks per pixel is
bracketed rather than known.

| looks per pixel | attention list retained | rank ρ |
|:--|--:|--:|
| F = 2 (optimistic) | 0.754 | 0.908 |
| **F = 1 (nominal)** | **0.686** [0.629, 0.732] | 0.855 |
| F = 0.5 (correlated pixels) | 0.616 | 0.786 |

Against a **chance floor of 10.0%** — the retention of a 97-farm list drawn at random from 966.

> **Of the 97 farms we name, 39 come back in ≥80% of re-flights and 30 in under half.**
> The list is far better than chance and about a third of the individual names are not stable.

### The control failed, and the failure is reported rather than deleted

The positive control as first written required retention among listed farms to rise with pixel
count. **It came back ρ = −0.008.** Under the rule this document follows, a test that fails its
own control is discarded — so the claim that the control was *mis-specified* had to be
demonstrated, not asserted.

It was. Retention among **already-listed** farms is governed by **margin** — how far below the
decile boundary a farm sits. A farm deep in the bottom returns whatever its size; a farm on
the boundary flips whatever its size. Measured: **ρ(retention, margin) = +0.921**, against
ρ(retention, npix) = −0.008. Size and margin are near-independent, so the size effect cannot
show up in that statistic.

The underlying claim — that speckle reaches the index in a **size-dependent** way — is then
tested directly, and it passes decisively:

| parcel size | mean index spread across re-flights |
|:--|--:|
| under 20 px | **12.19 points** |
| 20–50 px | 11.26 |
| 50–150 px | 7.24 |
| over 150 px | **4.10** |

**ρ(index spread, npix) = −0.622.** Both the failed control and the corrected one are reported,
and the run aborts if *either* the corrected control fails **or** the margin explanation fails —
so the mis-specification story cannot be assumed after the fact.

**Two other controls.** Zero noise must be an exact no-op: retention 1.000, ρ 1.0000 — and it
caught a real bug on first run, since `numpy`'s Gamma returns NaN at infinite shape rather than
collapsing onto 1.0, which made C1 report chance-level retention. The village total is
invariant and asserted **on every one of the 1500 replicates**, not once.

**The honest bound, and it is not small.** Only the *level* is perturbed, not the within-farm
CV feeding `uniform` — and `uniform` carries the **largest weight in the shipped index,
0.249**. A quarter of the index is noise-free by construction of this test, so every retention
above is an **upper** bound and true stability is worse. Modelling it would need the spatial
correlation length of speckle within a parcel, which we do not have.

**What we do with it.** `p3_speckle_farm.csv` carries a per-farm retention at all three noise
levels. We are **not** re-cutting the frozen list; we are stating that the attention list
should be read as a ranked list with a stability column, and that a 0.27 ha parcel and a
3.5 ha parcel do not deserve equal confidence even when they carry the same index. That is a
statement about the product's resolution, and no team can make it without propagating the
sensor's own noise model.

---

## 10. Reproducing this

```
py -3.12 src/common.py              # self-check: 6 scenes, duplicate-SLC trap, SF² assertion
py -3.12 src/p1_prep.py             # SLC → β⁰/σ⁰/γ⁰, geocoded, 2 m + 5 m grids
py -3.12 src/p1_calib.py            # the nesz_peak adjudication, all six scenes
py -3.12 src/p1_features.py         # 966 × 111 per-farm features, buffer ladder, coverage
py -3.12 src/p3_build.py            # anchors × modifier → submission + aggregation
py -3.12 src/p3_checks.py           # the 19-check defensibility battery
py -3.12 src/tests_regression.py    # 12 failure-mode assertions
py -3.12 src/p3_figures.py          # the nine figures; renders, then says to go and look
```

The ten post-freeze approaches of §9, none of which touch the deliverable:

```
py -3.12 -u src/p3_t2_wcm.py        # 9.1  WCM autopsy — identifiability
py -3.12 -u src/p3_t1_gai.py        # 9.2  SAFY's proxy, and the 6-day decay rate
py -3.12 -u src/p3_dawidskene.py    # 9.3  label fusion + the provenance control that voided it
py -3.12 -u src/p3_fusion.py        # 9.4  X-band + C-band, rejected on the held-out witness
py -3.12 -u src/p3_climatology.py   # 9.5  nine-year Sentinel-1 climatology
py -3.12 -u src/p3_harvest.py       # 9.6  harvest detection — failed its own controls
py -3.12 -u src/p3_representative.py # 9.7 Sokhda against 271 like-sized neighbours
py -3.12 -u src/p3_spatial.py       # 9.8  location: Moran's I, variogram, positive control
py -3.12 -u src/p3_edge.py          # 9.8  outline: core/ring split, matched-N random null
py -3.12 -u src/p3_voi.py           # 9.9  value of each acquisition
py -3.12 -u src/p3_speckle.py       # 9.10 re-flight stability of the attention list
```

Every one of these aborts rather than reports if its own control fails, and every one
re-verifies both submission checksums on the way out.

Dates are **scanned from the delivered data**, never hardcoded — Round 2 measured its own
portability debt at 20 of 33 files hardcoding acquisition dates. Every scene constant is read
from the vendor's `_extended.json`; nothing is transcribed.

**Deliverables:** `results/submission.csv` (966 rows) · `results/tables/p3_village_summary.csv` ·
`p3_zone_summary.csv` (46 zones) · `p3_farm_uncertainty.csv` · `results/figures/p3_f1..f9.png`
