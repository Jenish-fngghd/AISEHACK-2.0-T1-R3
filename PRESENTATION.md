# Sokhda kharif 2025 — 10-minute panel deck

**Ten slides, one claim each.** Round 2's measured lesson: the most persuasive devices in this
competition were a **decile-trend plot** and a **validation table whose rows state what they
*establish*, not what they measure**. Both are used below.

Timing: ~50 s per slide, leaving ~2 min for questions. **Slides 3, 6 and 8 are the ones to
protect if we run long.** Slides 4 and 9 can be cut to a sentence.

---

## Slide 1 — The answer, and why the column is not one thing

> **710 t over 447.5 ha. But the column holds three different kinds of object.**

**Figure:** `p3_f1_deliverable.png`

| crop | area | what the number *is* |
|:--|--:|:--|
| Cotton | 43% | a **FORECAST** — ~72% still on the plant at our last scene |
| Groundnut | 31% | a **MEASUREMENT** — yield determined in late October, inside our window |
| Rice · Maize · Bajra | 26% | a **RECONSTRUCTION** — season closed before Round 2's last date |

**Say:** "Every team here will show you one number per plot. Ours is three different things, and
we tell you which is which — because a forecast, a measurement and a reconstruction do not
deserve the same confidence."

---

## Slide 2 — What the two new dates actually bought

> **They landed exactly where Round 2 was blind: cotton and groundnut, 74% of the village.**

- Cotton picking runs **October to January**. Round 2 stopped on 13 October.
- Groundnut's yield is set at physiological maturity, **~135 days after sowing = late October**.
- **12 November is after the groundnut event and mid-way through the cotton one.** That
  asymmetry is the whole round.

**Say:** "Two acquisitions do not double our information. They arrive at the one moment that
separates a crop we can measure from a crop we must forecast."

---

## Slide 3 — ★ We found our own Round 2 calibration was wrong

> **β⁰ = SF²·|z|², not SF·|z|². And our own post-mortem's confirmation was on the wrong quantity.**

| quantity | mean vs vendor's declared noise floor | scenes **below** the floor |
|:--|--:|:--|
| **β⁰** | **+1.86 dB** | **0 / 6 — admissible** |
| σ⁰ | −1.08 dB | 6 / 6 — impossible |
| γ⁰ | −0.42 dB *(the smaller error!)* | 4 / 6 — impossible |

**The point:** a scene's darkest pixels cannot be quieter than the sensor's own noise. **Sign
beats magnitude.** γ⁰'s "better" 0.36 dB was bought by sitting *under* the floor.

Confirmed three independent ways — vendor metadata on six scenes, Capella's own reference code,
and a competitor's published γ⁰ agreeing with ours to **~1 dB**.

**Say:** "We audited ourselves and found we had been wrong for two rounds. Then we found our own
fix had been verified against the wrong number."

---

## Slide 4 — Is the right-looking scene even usable? *(cut to one line if short)*

> **Pre-registered kill criterion. Measured answer: yes, no correction needed.**

Per-target spread, look-reversed pair **1.81 dB** vs same-look control **1.90 dB** — ratio 0.94
against a 1.5 threshold. **Water — physically incapable of an orientation effect — spreads *more*
than built-up on the same pair.**

**Say:** "We asked a question nobody else asked, and the answer was 'it doesn't matter'. That is
still worth knowing, because we can now use the date without an apology."

---

## Slide 5 — ★ Our 29 October scene is inside a state-wide disaster

> **239 talukas. 33 districts. Over 10 lakh hectares damaged. Our satellite passed overhead on
> day six.**

- ERA5-Land at Sokhda: **81.2 mm over 26–28 October**, soil moisture 0.133 → **0.372**
- Our overpass sits on the wet peak
- **The rise is ordered by canopy**: cotton +0.49 dB (most canopy) → bajra +2.60 dB (bare)

Two consequences:
1. **No scalar removes it** — the term depends on canopy cover.
2. **It is a yield-loss mechanism, not just a radiometric one.** The crop itself changed.

**And it disqualified an inherited method:** Round 2 referenced every date to in-scene water.
29 October is the only date with **14.1 m/s wind** — that would have injected **+2.9 dB** of wind
roughening into a load-bearing date, in the direction that reads as canopy change.

### ★ And we can now corroborate all of this with nine years of radar, not a news report

**Figure:** `p3_f5_climatology.png`

Every Sentinel-1 scene over Sokhda in Jun–Sep, **every year 2016–2025, is on one track** — nine
years with no geometry confound. Each year measured twice: farm pixels, and non-farm pixels as a
control.

| window | z(farm − non-farm) vs the 8-year norm | |
|:--|--:|:--|
| **Jun–Sep** growing season | **−0.16** | statistically **ordinary** |
| **Oct–Nov** after the rain | **−1.62** | farms darker than the landscape |

**The crop grew normally and was hit late.** That is the epistemic-object split (slide 1) falling
out of an independent nine-year record — and it turns our `adj_2025_26 = 1.00`, held for four
crops as an admitted assumption, into a village-specific measurement.

**The control did the work:** raw farm signal was z = +1.20, which reads as a good season — but
the non-farm control was **+1.39**. The whole landscape brightened on wet soil. Report the raw
number and we would have announced a good harvest from soil moisture.

---

## Slide 6 — ★ Two experiments, killed by their own controls

> **We designed both to be able to fail. Both did.**

| experiment | result | killed by |
|:--|:--|:--|
| Groundnut-lift signature | +0.11 dB, p = 0.42 | **control fired at 12× the effect** |
| Water Cloud Model | T² ordered beautifully… | **bajra T² = 1.53, CI [1.27, 1.90]** |
| Dawid-Skene label fusion | beat us 26.3% vs 11.2% | **3 of 6 teams''' labels are optical-informed** |
| X-band + C-band fusion | +0.35 partial ρ on cotton | **helps 13 Oct, hurts 12 Nov** |

**★ And the WCM turned out to be worse than wrong — it was incapable.** ρ(raw two-date
difference, T²) = **+1.000, exactly.** T² is a monotone relabelling of a number we already had:
one degree of freedom of data per crop against several free parameters. **Even if the physics had
passed, it would have added nothing.**

**The lift test's control fires because Round 2's labels were derived from these same
trajectories** — every naive label test on this stack is circular. **The WCM fails because a
canopy cannot amplify a soil signal.** Both point at the same unmodelled term: field position
and soil, comparable in size to canopy.

**Say:** "These are the two most interesting things we did, and neither is in the forecast. A
control that can fire is worth more than a result that cannot."

---

## Slide 7 — ★ The consistency check no other team can run

> **We are the only team with a Round 2 to contradict.**

**Figure:** `p3_f3_d1.png` — every expected ratio written down *before* the forecast existed.

| crop | ratio | expected | why |
|:--|--:|:--|:--|
| Rice · Maize | **1.04 · 1.00** | 0.8–1.3 | harvested before R2's last date — **must not move** |
| Cotton | **1.84** | 1.5–4.0 | final vs to-date, still picking |
| **Bajra** | **0.71** | 0.5–1.3 | **we corrected an anchor we had got wrong** |

**Say:** "The crops that must not move, don't. The crop that must rise, does. And bajra falls
because we found our own error."

---

## Slide 8 — ★ What did the SAR actually contribute? An honest number.

**Figure:** `p3_f2_uncertainty.png`

> **Through the modifier: nothing, by construction. Through the crop map: everything we own.**

**★ We had this wrong until we audited the sentence.** For two rounds we reported "the SAR
contributes zero to the village total". That is true of the **modifier** — and it is only one of
the two channels. Write the total out:

```
village total  =  SUM over crops of    anchor_c    x    area_c
                                      ----------       --------
                                      published        a SAR
                                      statistic        PRODUCT
```

The anchors are government yield statistics we did not produce. **The areas are decided entirely
by the crop map, and the crop map is made from these Capella trajectories** — that is exactly why
every naive label test on this stack is circular (slide 6). **So the SAR supplies one of the two
factors in the product.** It is worth 236.5 t of the interval; we had been reporting 0.0 t.

| source | 90% interval width on village production |
|:--|--:|
| the SAR **modifier** (8-member ensemble) | **0.0 t** |
| the SAR **crop map** — the other channel, see above | **236.5 t** |
| crop label — sampling **our own** posterior | 40.7 t |
| crop label — **5 other teams, same 966 farms** | **236.5 t** |
| **the anchor** — calibrated to the district's own history | **385.2 t** |

**★ Both our uncertainty terms were too narrow, and we only found out by going outside our own
model.** Sampling our own posterior measures our *confidence*, not our *accuracy* — it said the
label was worth 41 t; five independent labellings of the same farms say **237 t**. Our anchor
spread said groundnut was worth CV 0.15; that district's own yields move at **CV 0.49**.

*Reassuring half:* 4 of the 5 other teams land within **2.2%** of our 710 t (695.0–722.8 t). We
are not the outlier — Orion is, at 887 t.

**And one term is a bias, not a width.** Argmax over a diffuse posterior (69.4% of farms have no
class above p = 0.5) concentrates area into the classes that win most often — cotton −35 ha,
groundnut −37 ha — while the posterior spreads it into higher-anchor maize and bajra. Shipped
**710.0 t** vs posterior-mean **741.5 t**: **biased LOW by 31.5 t (4.4%), and we know the sign.**

**★ And a second bias, pointing the same way, that we went looking for.** The anchor is a
*Vadodara district* statistic applied to *one village* — the assumption underneath the largest
term on this table, and never once examined in three rounds. We cut the surrounding 22 km into
**271 blocks of Sokhda's own size**, cropland pixels only, and measured Sentinel-1 VH:

| 2017 | 2018 | 2019 | 2025 |
|:--|:--|:--|:--|
| +1.41 dB (92nd pct) | +1.85 dB (92nd) | +1.50 dB (85th) | +1.05 dB |

**Same sign every year — Sokhda is in the top 10–15% of its own landscape.** The control that
should have killed it: we measure Sokhda over *surveyed parcels* and its neighbours over
*classifier cropland*, and those masks disagree on **more than a third of the area** (11 153 vs
13 757 px, overlapping on 7 191). Re-measured with one definition on both sides: **+1.007 dB
against +1.051 — a 4% definition effect.** The masks disagree about the area and agree about
the radiometry.

**We are not applying it,** because VH differs by crop and we do not know the neighbours' crop
mix — "brighter" could mean "better" or could mean "more cotton". So it stands as a second,
independent reason to think **710 t is conservative rather than optimistic**, named rather than
corrected. A correction we cannot verify is worth less than a bias we can name.

So the SAR works on this problem through **three** channels, and only one of them is zero:
**the crop map** (236.5 t of the village total), **plots** (all of the within-crop spread,
validated at ρ ≈ 0.5 — but that is the same-day γ⁰ *feature*, not the composite index we ship,
which sits near ρ ≈ 0.09 against the same sensor), and **zones** (39.7 points of
hidden variation). The **modifier** is the zero — and it is zero *by construction*, because we
normalised it to mean 1.0 within crop, not because the radar failed.

**On confidence:** conformal prediction without labels guarantees **1 − α − β**, and β is our
label error rate, which we cannot bound. **So we publish the arithmetic instead of a number** —
a nominal 90% is really 60% at β = 0.30.

**Say:** "For two rounds we told people the radar contributed nothing to our village total. That
was our own sentence, and it was wrong — it described one channel out of three. The radar picks
the crop on every plot, and the crop is what the yield statistic gets multiplied by. What the
radar does *not* do is set the level. A published statistic does that, and it is the single
biggest thing we are unsure about."

---

## Slide 9 — ★ We are the most purely SAR-derived team here, and we can show it *(cut if short)*

**This slide used to claim the opposite of what it now says.** It read *"our labels survive the
test that dissolved a competitor's — ours 55%, their Tier-2 1%."* Applying that same metric
consistently to all six teams' shipped Round 2 labels killed the claim:

| team's labels | explains residual NDVI | survives | reads as |
|:--|--:|--:|:--|
| DeepThinkers · 8bit · CodingBits | 21.9% · 26.0% · 20.6% | 98% · 97% · 92% | optical-informed |
| Megalodon | 16.1% | 90% | mixed |
| Orion | 11.6% | 72% | SAR-like |
| **ours** | **11.2%** | **55%** | **SAR-like** |

**Computed like-for-like, we rank last.** The old comparison put our number, computed by us,
against Orion's self-reported figure for a *different* label set — not like-for-like.

**But the metric does not measure label quality.** It measures information *beyond the dominant
SAR axis* — and a labelling built with optical data gets that for free. So the ranking is a
provenance detector, not a quality ranking, and it says: **our labels are the least contaminated
by anything that is not radar.** In a SAR competition that is the more interesting fact.

**Say:** "We built this test to flatter ourselves, ran it properly across everyone, and came
last. Then we worked out what it actually measures — how much of your crop map did not come from
the radar. On that reading we are first, and we would rather show you the corrected version than
the one we liked."

---

## Slide 9a — ★ Ten things we built *after* we froze the forecast

> **The forecast was final before any of this ran. So none of it could make our number look
> better — it could only tell us something true.**

| what we asked | verdict |
|:--|:--|
| Can the Water Cloud Model be fixed and retried? | **killed** — unidentifiable; ρ(model, raw input) = 1.000 |
| Can SAFY's canopy proxy work on this stack? | **killed** — the signal decays a third in six days |
| Should we fuse six teams' crop labels? | **won, then voided** by our own provenance control |
| Does adding Sentinel-1 C-band improve the forecast? | **real information, rejected** — helped only on the date we looked at |
| Was 2025 an ordinary year at Sokhda? | ★ **survived** — nine-year climatology |
| Can we test our own harvest-timing claim? | **could not be run**, and §8 now says so |
| Is Sokhda typical of its district? | ★ **survived as a flag we did not apply** |
| Is the ranking the farm, its location, or its outline? | ★ **survived** — and it is the good news |
| What did each of the six acquisitions buy? | ★ **survived, and shrank our own claim** |
| Would the same 97 farms be named if we re-flew? | ★ **survived**, with a stability column |

**Four died to their own controls. One won and was then voided. One could not be run.** Nothing
here changed a shipped number, and the R2 and R3 submission checksums are verified before and
after every one of these runs.

**Say:** "We froze the forecast, then spent the rest of the round trying to break it. Six of the
ten failed. We are showing you the failures because that is the only reason to believe the four
that didn't."

---

## Slide 9b — ★ The three that changed what we say

**Figures:** `p3_f7_voi.png`, `p3_f8_speckle.png`, `p3_f6_spatial.png`, `p3_f9_edge.png`

**1. We were overselling the time series, and we measured it.** Leave each scene out and rebuild:
dropping **14 August** collapses the ranking (ρ **0.211**, 77 of 97 attention-list farms move) —
14 August *is* the index. Dropping 6 June moves **one farm**. One scene alone already reaches
ρ 0.857. The jump to 0.9993 comes at the *fourth* scene, and it is mechanical, not fitted:
senescence is a **slope**, so it does not exist until a second late date arrives. **So we are
entitled to say "a peak-canopy index with temporal corrections", not "a season-long trajectory
model", and we changed our own wording.** The time axis still does real work — shuffling the
calendar costs more (ρ 0.312) than deleting four of five scenes.

**2. A third of the names on our attention list would not survive a re-flight.** Same crop, same
day, different speckle: the median parcel is 69 pixels, so its brightness is known to 12% before
the model is even wrong. Rebuilding 500 times, **68.6% of the list returns** against a **10%**
chance floor — **39 of the 97 farms come back in ≥80% of re-flights, and 30 in under half.** So
we ship the list *with a stability column*. ★ Our positive control here **failed** (ρ = −0.008);
rather than delete it we had to prove it mis-specified (retention is driven by margin, ρ = +0.921)
before replacing it, and **both versions ship**.

**3. The ranking is about the field — not where it sits, and not how it is drawn.** Two ways our
per-farm list could have been an artefact, both tested: **location**, against a positive control
(incidence angle) whose structure runs clean off the edge of the village — **96% of the ranking is
field-scale**; and **outline**, since the median parcel is **45% boundary pixel** and 75 farms have
no interior at all. Dropping every boundary pixel moves the list **no more than dropping the same
number at random** (ρ 0.853 vs 0.857). And **ρ(index, parcel size) = −0.017** — across a 40× spread
in farm area, **our index does not punish you for having a small field.**

**Say:** "The first one made us shrink our own claim. The second means a farmer gets a name *and*
a number saying how much to trust it. The third is why we are willing to put individual names on a
list at all — and all three could have gone the other way."

---

## Slide 10 — What we got wrong

> **Nineteen items across this deck, §8 of the writeup and the research log.
> Twelve are our own errors. Here are four.**

1. **Our calibration was wrong for two rounds**, and our fix was verified against the wrong
   quantity.
2. **We nearly shipped a selection artefact** as a discovery — a clean 3.4 dB effect on both new
   dates, of which **+2.59 dB was the artefact**, caught by rebuilding out-of-sample.
3. **★ We padded our own uncertainty and called it measured.** Rice and maize carried an invented
   ±15% bracket sitting directly under a comment promising every entry was a real published
   number. Replacing it with the Gujarat state estimates **widened our interval from 170 to
   320 t**, once against real published values and again against the district's own history — reality was wider than the padding, on 26% of the village.
4. **Our bajra share is probably too high**: we assign 9.5%, Gujarat's actual 2025 sowing profile
   gives 2.9%. **If a share in our map is wrong, it is that one — and we costed it: +13.7 t,
   +1.9%.** Bajra's anchor sits near the village mean, so even our worst-suspected share error
   barely moves the total.

Plus: our total is biased low by 4.4% from argmax labelling (slide 8); coverage is crop-biased on
every date (29 cotton plots never observed); no clean reserved scene exists and we publish the
contamination ledger instead; 2 of 9 spatial hold-out checks fail on a feature that does not enter
the shipped index; and the one diagnosis on this list we got *wrong* — we blamed the argmax bias
on a normalisation artefact, tested it, and **the fix made the gap larger**.

**And one the figure caught, not the test.** Our variogram reported the positive control's range
as "~1400 m", computed as the first lag reaching 95% of a sill estimated from the far bins. Plotted,
that curve is **still climbing at the last lag** — there is no sill inside the village, so the
number was not a measurement. It now prints `>1400 m [still rising]`. Understating the control
weakens our own contrast, which is why the corrected version is the one we show. **Second round
running that the figure caught something every number passed.**

**A table of ours disagreed with its own figure.** Our parcel-size table (slide 9b) excluded the 75 farms with no interior pixel while the figure included them, so the table read 0.80 boundary fraction for small parcels where the truth is 1.00 — it understated exactly the population the test was about. The figure caught it, for the fourth time this round.

**A control of ours failed and we kept it in.** Our speckle positive control (slide 9b) came
back ρ = −0.008. We could have quietly rewritten it; instead we had to prove it was
mis-specified before replacing it, and both versions ship.

**And a silent failure mode in our own shipped code, found by an audit that was looking for
something else.** `derive_weights` reads a Spearman matrix; a zero-variance part makes its
column NaN and the row sums push that NaN into **every** weight — turning the whole index into
a constant 50 with no error raised. With the delivered six dates no part is degenerate (min
part sd 1.08, verified), **so nothing we shipped is affected** — but it fails silently, which
is the kind that gets you next time.

**Two more found in the last 48 hours, both against us.** Our slide-9 claim was self-flattering
and did not survive being computed consistently (see slide 9). And our writeup said plot level was
*validated at ρ ≈ 0.5* — that is the same-day γ⁰ **feature**, not the composite index we actually
ship, which sits near **ρ ≈ 0.09**. We had validated an input and reported it as validation of the
product. No test in the repo had ever put the shipped index against the witness.

**Close:** "Round 2 taught us that a submittable answer early beats a better answer late, and
that the figure is the check on the prose. This round we added a third: **a control that can fire
is worth more than a result that cannot.** Every number we showed you has one."

---

## Anticipated questions

| question | answer |
|:--|:--|
| *"Why is cotton only 0.73 t/ha?"* | **Lint**, ~34% of seed cotton. It leads on area, not tonnage. Confirmed against a primary source stating the same tonnage three ways (480 lb bales / 170 kg bales / MMT). |
| *"Your groundnut share is too high — it's a Saurashtra crop."* | Gujarat's **actual** 2025 sowing: groundnut **39.2%** of the five-crop area, surpassing cotton for the first time at 116.62% of normal. Our 30.8% is **23.2 pp** from that profile; the 16% reference is **60.5 pp** from it — and was derived from these same figures. |
| *"Isn't this just a statistic with a radar decoration?"* | Partly, at village level — and slide 8 quantifies exactly how much. At plot and zone level the SAR carries all the variation, validated against an independent same-day sensor. |
| *"What's your confidence interval?"* | **[598, 918] t at 90%**, dominated by the anchor. It got wider **twice** under audit: we had invented a ±15% bracket for rice and maize, and even after fixing that, three of five crops were still narrower than the district's own interannual spread. An interval that only ever narrows is not being tested. And the conformal guarantee is 1 − α − β with β unbounded — we show the arithmetic. |
| *"Is your estimate biased?"* | **Yes, low, by 31.5 t (4.4%), and we measured it.** Argmax labelling concentrates area into the classes that win most often; the posterior spreads it into higher-anchor crops. We report it rather than correct it, because the deliverable needs one label per farm. |
| *"Did you try anything beyond the six scenes?"* | **Ten things, after the forecast was frozen, none of which changed a shipped number** (slide 9a). Six died to their own controls or could not be run — Dawid-Skene label fusion, X+C fusion, the WCM autopsy, SAFY, and harvest detection. Of the survivors the cleanest is a **nine-year Sentinel-1 climatology** showing the 2025 growing season at Sokhda was ordinary (z = −0.16) while Oct–Nov was not (z = −1.62) — free, no credentials, via Planetary Computer. |
| *"Why not a proper crop growth model?"* | We gated SAFY on a test and it failed on **availability**: only 2 of 6 dates have a same-day optical partner, neither inside the June–September growth window. Process-based models need per-plot inputs we would have to invent. |
| *"How do we know your crop map is right?"* | We don't, and we say so — 69.4% of farms have no class above 0.5 probability, and we ship the full posterior. What we can show is slide 9: our labels survive a non-circular test that dissolved a competitor's. |
