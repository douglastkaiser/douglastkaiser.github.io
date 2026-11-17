# Car rankings evidence and market-coverage audit

> Historical snapshot: the [November 17 lineup and Sporty/Fun audit](fun-lineup-audit.md) supersedes the lineup and maintenance-based scores below. Maintenance is now included only in Cost; Fun is the optional sixth axis.

**Latest:** [November 16 review and scoring audit](review-audit.md) supersedes the score/rank summaries below and the [November 15 scoring snapshot](scoring-audit.md). It covers all 57 configurations, all 342 category results, review evidence, the revised rubric and sensitivity checks.

Research checked November 14, 2026. Implementation baseline: `2518f55a1f9ca5958c674ad1a9365dc5bc67272e` (fetched and fast-forwarded from `main`). `data.json` contains research inputs; `index.html` is generated from the data and template. Prior audits and original screening decisions remain available in Git history.

## November 14 baseline findings

- **57 ranked configurations from 73 screened candidates**, including 12 additions. This is a representative market comparison, not an exhaustive inventory or sales-weighted sample.
- Body styles: 37 Crossover; 9 Hatchback; 3 Minivan; 2 Pickup; 6 Sedan. Powertrains: 10 EV; 18 Gas; 25 Hybrid; 4 PHEV.
- Tucson Plug-in Hybrid retains its published **2024 lifecycle anchor of 60/100**. Its relative Eco band moves **0 → +1** after correcting proxies and expanding the cohort. This is not a new environmental measurement or a manually selected promotion.
- RAV4 Hybrid Maintenance moves **−2 → 0**. Its old 3/5 disruption input was lower than the 4/5 given to established designs solely because it was redesigned. The revised comparison does not turn uncertainty into a failure-risk penalty.
- The audit also found same-model lifecycle records omitted in favor of unrelated comparisons. Model 3’s 67-point proxy becomes 55 using the historical RWD record; Model Y’s 65 becomes 57 using its model-family AWD record. Current efficiency alone cannot quantify an eight- or twelve-point lifecycle uplift.
- **20 historical anchors and 37 editorial proxies**, all numeric and included in rankings and Pareto comparisons. Counts in the page method are derived from the data. There are 55 exact model-year EPA records and two retained Toyota manufacturer references/conversions.
- All prices describe reference configurations. Local stock, transaction price, future resale, current-model failure rates, exact cold-weather range and actual gear fit remain unverified.

## November 15 trip consistency audit (before the general audit)

Reviewed all 57 selected configurations and all 171 trip-component inputs. Preserved the 40% carrying / 35% winter access / 25% trip practicality weights and full-cohort tier calculation. The issue was unsupported editorial inputs, not a percentile calculation bug.

Five EVs had a 4/5 trip-practicality input without a sourced loaded-winter route assessment. All ten EVs now share a provisional 3/5 replenishment baseline. EPA range and manufacturer charging claims remain context; neither establishes cold-weather usable range, arrival reserve, charger availability or stop duration. A future higher input requires explicit route evidence, and is not prohibited by powertrain. This is a planning assumption, not a measured equivalence between EVs.

Gas, hybrid and PHEV 5/5 inputs describe rapid liquid-fuel replenishment only. They do not establish better carrying, winter grip or overall trip performance. PHEV electric miles are not assumed to cover the mountain trip. A low-clearance sedan still loses carrying and access points. No EV-only roof-drag penalty or free winter-tire/roof-carrier equipment is assumed.

Carrying and winter inputs remain editorial estimates with their existing configuration evidence; no new physical fit tests, stopping-distance results or clearance measurements were performed. Every car now exposes all three component rationales and a review note. AWD, brand, model refresh and maximum folded-seat cargo volume cannot substitute for a route or three-adult gear-fit assessment. The updated validation rejects missing rationales and unsupported EV trip upgrades.

| Vehicle | Components: before → after | Trips band: before → after |
| --- | --- | --- |
| Subaru Solterra | [4, 4, 4] → [4, 4, 3] | +2 → +1 |
| Nissan LEAF | [3, 2, 4] → [3, 2, 3] | −1 → −2 |
| Tesla Model Y | [5, 2, 4] → [5, 2, 3] | 0 → 0 |
| Chevrolet Equinox EV | [4, 2, 4] → [4, 2, 3] | 0 → −1 |
| Tesla Model 3 | [2, 1, 4] → [2, 1, 3] | −2 → −2 |

Other vehicles retain their trip inputs and bands. Totals, order and Pareto comparisons are regenerated from the revised inputs. The November 14 rank table below is historical; the live page contains the current order. Other categories were not re-researched in this trip-specific follow-up.

## Eco re-evaluation

The [published ACEEE table](https://www.greenercars.org/greenercars-ratings/) was downloaded and all 20 retained benchmark records matched on make/model, score, engine, drive, emissions certification, city/highway fields and weight class. The historical Tucson PHEV 60 and Sportage PHEV 61 records are valid. A historical anchor is not a measured current-year rating: trim, tires, certification and model-year changes remain explicit limitations.

All existing proxy records were resolved to specific published rows. Every proxy now stores the full source record, including engine, drivetrain, emissions, city/highway and weight, and validation rejects inconsistent scores or labels. Same-family, same-powertrain evidence takes precedence over a different model. A different powertrain within the family is not automatically a better anchor: for example, a gas-only 2024 CX-50 does not represent the new hybrid.

### Existing assessment changes

| Vehicle | Prior assessment | Revised assessment | Revised basis |
| --- | ---: | ---: | --- |
| Subaru Solterra | 64 | 66 | Subaru SOLTERRA AWD · Electric (Li-Ion) · AWD |
| Mazda CX-5 | 47 | 49 | MAZDA CX-5 4WD · 2.5L 4, auto stk 4wd · 4WD |
| Toyota RAV4 Hybrid | 59 | 57 | TOYOTA RAV4 HYBRID AWD · 2.5L 4, auto CVT Awd · AWD |
| Hyundai Tucson Hybrid | 56 | 53 | Hyundai Tucson Hybrid Blue · 1.6L 4, auto Awd · AWD |
| Hyundai Sonata Hybrid | 62 | 60 | Hyundai Sonata Hybrid · 2.0L 4, auto · FWD |
| Lexus UX 300h | 60 | 56 | LEXUS UX 250h · 2.0L 4, auto CVT · FWD |
| Tesla Model Y | 65 | 57 | Tesla Model Y Long Range AWD · Electric (Li-Ion) · AWD |
| Tesla Model 3 | 67 | 55 | Tesla Model 3 RWD · Electric (Li-Ion) · RWD |

Unchanged proxy estimates retain their named rationale and limitations. LEAF/Bolt comparisons now include both the 66-point small-battery LEAF and 62-point LEAF SV context; they do not claim a linear relationship between battery capacity and Green Score. There is no blending of European Green NCAP results, direct MPG/MPGe comparison, or calculated lifecycle score derived from the cost scenario.

PHEV ownership costs still assume **60% electric and 40% gasoline miles**. That is a disclosed cost scenario, not the utility factor used by ACEEE and not a recalculation of a historical Green Score. Regular charging affects real-world impacts, but a precise personal lifecycle prediction is not established here.

### Relative scale

Keep the full-cohort midpoint rule: `(strictly better + tied / 2) / cohort count`. Bands at 20/40/60/80% produce +2/+1/0/−1/−2; exact boundaries go toward zero, and equal values share ranks and bands. No quotas or forced band sizes. **Zero means middle of this comparison group, not zero environmental benefit.** Adding candidates can change bands without changing their assessments. The score legend, accessible row descriptions and Eco dialogs explain this. Dialogs show the assessment /100, source basis, shared category rank and band.

## Maintenance: evidence and confidence are separate

- Preserve 50% disruption, 30% routine effort, 20% service access, with Maintenance starting at 0×. Confidence descriptions and audit/generation notes never enter `value()`, tier assignment, totals or Pareto dominance.
- **Disruption: shared 3/5 for every vehicle.** No applicable current-model failure evidence was established. Remove both the old redesign penalty and the unsupported continuity bonus. Brand reputation can guide further research but is not a measured exact-build reliability result.
- **Routine effort: shared 3/5 for Gas, Hybrid and PHEV.** Comparable schedule/time evidence has not established a model-specific difference. Retain manufacturer schedule/severe-use cautions and remove the unsupported PHEV systems-complexity penalty. This deliberately also removes the old gas-versus-hybrid effort distinction rather than translating a dollar allowance into a time measurement.
- **EV routine effort: 5/5**, an editorial powertrain-level estimate supported by the [DOE scheduled-maintenance framework](https://www.energy.gov/cmei/vehicles/articles/fotw-1190-june-14-2021-battery-electric-vehicles-have-lower-scheduled). Engine oil, ignition and exhaust tasks are avoided, but tires, brakes, inspections, filters and fluids remain. This is not a source-provided exact-build effort score or maintenance schedule.
- **Service access: shared 3/5.** No local shop census or quantified model-specific delay evidence supports a difference.
- Every maintenance detail has three component rationales and a separately labeled confidence description. All combustion entries therefore share the current 0 band; EVs share +2. Empty intermediate bands are acceptable. Dollar upkeep and repair allowances remain in Cost unchanged.

## Representative market expansion

Added minivans and compact pickups plus larger family SUVs while preserving new-car, California and $60k estimated OTD constraints. Configurations use the least expensive documented grade with adaptive cruise and continuous lane centering found in this pass, not expensive power-door-driven upgrades. Every entry supplies six assessments, a selected energy record and source context; subjective components remain editorial estimates.

| Added vehicle | Selected configuration | Est. OTD | EPA combined MPG | Price/equipment references |
| --- | --- | ---: | ---: | --- |
| Ford Maverick Hybrid | Lariat AWD | $43,719.13 | 36 | [Ford Maverick Lariat 2026 equipment](https://www.ford.com/trucks/maverick/models/lariat/); [Ford 2026 Lariat AWD hybrid manufacturer label](https://www.windowsticker.forddirect.com/windowsticker.pdf?vin=3FTTW8S31TRB75802) |
| Kia Sorento Hybrid | EX FWD | $44,206.93 | 37 | [Kia Sorento Hybrid 2026 pricing](https://www.kiamedia.com/us/en/models/sorento-hev/2026/pricing); [Kia Sorento Hybrid 2026 equipment](https://www.kiamedia.com/us/en/models/sorento-hev/2026/features) |
| Toyota Sienna | LE FWD | $46,949.45 | 36 | [Toyota Sienna 2026 pricing and standard equipment](https://www.toyota.com/sienna/2026/features/); [Toyota current delivery/processing charges](https://www.toyota.com/gst/deals-incentives/financial-estimates-highlanderhybrid/?vehicles=highlanderhybrid) |
| Toyota Crown Signia | XLE AWD | $50,602.53 | 38 | [Toyota Crown Signia 2026 pricing and equipment](https://www.toyota.com/crownsignia/features/); [Toyota current delivery/processing charges](https://www.toyota.com/gst/deals-incentives/financial-estimates-highlanderhybrid/?vehicles=highlanderhybrid) |
| Toyota Highlander Hybrid | XLE AWD | $53,128.25 | 35 | [Toyota Highlander 2026 equipment and pricing](https://pressroom.toyota.com/2026-toyota-highlander-gets-standard-all-wheel-drive-across-the-lineup/); [Toyota current delivery/processing charges](https://www.toyota.com/gst/deals-incentives/financial-estimates-highlanderhybrid/?vehicles=highlanderhybrid) |
| Hyundai Santa Fe Hybrid | SE FWD | $41,621.59 | 36 | [Hyundai Santa Fe Hybrid SE 2026 pricing and equipment](https://www.hyundaiusa.com/us/en/vehicles/2026-santa-fe-hybrid/se); [Hyundai Santa Fe Hybrid 2026 manufacturer label](https://monroneylabels.com/cars/15246353-2026-hyundai-santa-fe-hybrid/window_sticker.pdf?cfl=3532684500) |
| Kia Carnival Hybrid | LXS FWD | $46,971.13 | 32 | [Kia Carnival Hybrid 2026 pricing](https://www.kiamedia.com/us/en/models/carnival-hev/2026/pricing); [Kia Carnival Hybrid 2026 equipment](https://www.kiamedia.com/us/en/models/carnival-hev/2026/features) |
| Subaru Outback | Premium AWD | $39,935.97 | 27 | [Subaru Outback 2026 manufacturer equipment comparison](https://www.subaru.com/services/vehicles/pdf/trimComparison/2026/OBK?hideBuildMsrp=false); [Subaru 2026 Outback pricing announcement](https://www.prnewswire.com/news-releases/subaru-announces-pricing-on-all-new-2026-outback-suv-302535958.html) |
| Hyundai Palisade | SE FWD | $44,911.53 | 21 | [Hyundai Palisade SE 2026 pricing and equipment](https://www.hyundaiusa.com/us/en/vehicles/2026-palisade/se); [Hyundai 2026 Palisade pricing and freight reference](https://www.kbb.com/car-news/hyundai-nails-down-2026-palisade-starting-prices/) |
| Hyundai Santa Cruz | XRT AWD | $46,987.39 | 20 | [Hyundai Santa Cruz XRT 2026 equipment and pricing](https://www.hyundaiusa.com/us/en/vehicles/2026-santa-cruz/xrt); [Santa Cruz 2026 freight reference](https://www.cars.com/articles/how-much-is-the-2026-hyundai-santa-cruz-518272/) |
| Honda Pilot | Sport FWD | $48,114.75 | 22 | [Honda Pilot September 2026 pricing](https://hondanews.com/en-US/honda-automobiles/releases/release-bb136e6e7af7ccb6b0336e10d8119451-2026-honda-pilot-pricing-and-epa-ratings-september); [Honda Pilot 2026 equipment](https://www.hondainfocenter.com/2026/Pilot/Feature-Guide/Specifications/) |
| Honda Odyssey | EX-L FWD | $48,439.95 | 22 | [Honda Odyssey 2026 pricing](https://hondanews.com/en-US/honda-automobiles/releases/release-6f8b202ddb1c7f26ecd92774bb031f99-2026-honda-odyssey-pricing-and-epa-ratings); [Honda Odyssey 2026 equipment](https://www.hondainfocenter.com/2026/Odyssey/Feature-Guide/Specifications/) |

Configuration checks: Maverick **Lariat HEV AWD EPA #50086 = 36 MPG**, not FWD or the generic AWD record. Its manufacturer label separates $38,090 base and $1,845 destination from optional paint/accessories; those unselected options are not charged. Santa Cruz uses the XRT turbo-AWD 20-MPG record, with navigation-based SCC and attention warning. Odyssey has speed-limited LKAS, not low-speed traffic-jam steering; Pilot has Traffic Jam Assist. Santa Fe SE does not borrow upper-grade navigation cruise. Carnival LXS receives no powered-liftgate credit. Larger cabins receive carrying estimates for three adults with unused rear seats folded, not a claim that skis fit from cargo volume alone.

No model-specific new-vehicle resale forecast was invented: additions use the existing historical hybrid/SUV segment assumptions or overall-market depreciation where a minivan/pickup-specific estimate was not established. Shipping is itemized once; source dates and price scope remain visible.

### Remaining coverage gaps

- **Ranger:** the checked US 2026 order guide lists ACC and lane keeping, but does not establish continuous centering for the proposed XLT package. Hold it out rather than equating corrective lane support with centering.
- **Pacifica PHEV:** an EPA 2026 record exists, but the manufacturer discontinued-model notice and remaining-stock uncertainty require an actual current assisted new build/quote before ranking. Not treated as universally unavailable.
- **Wagons:** no current assisted new US wagon under the OTD ceiling was established. V60 is explicitly screened. Subaru classifies 2026 Outback as an SUV, and Toyota markets Crown Signia as an SUV, so both remain crossovers in the existing body-style taxonomy. Older-model new wagon inventory requires a quote.
- The field still favors crossovers and efficient drivetrains; it does not represent every US model, equal body-style shares or local sales shares. Large trucks, true wagons, additional three-row EVs and near-duplicate trims are not automatically added to satisfy quotas.

## November 14 baseline ranks and score changes

Default weights remain 1× for the first five categories and 0× for Maintenance. These comparisons include both corrected evidence and cohort-expansion effects; existing prices and cost assumptions did not change.

| Rank | Vehicle | Prior rank | Total | Eco: prior → current band (assessment) | Maintenance: prior → current |
| ---: | --- | ---: | ---: | --- | --- |
| 1 | Toyota Camry Hybrid | 2 | +4 | +1 → +2 (63/100) | +1 → 0 |
| 2 | Honda CR-V Hybrid | 5 | +4 | 0 → +1 (58/100) | +1 → 0 |
| 3 | Subaru Forester Hybrid | 10 | +4 | −1 → 0 (55/100) | −2 → 0 |
| 4 | Toyota RAV4 Plug-in Hybrid | 1 | +4 | +2 → +2 (64/100) | −2 → 0 |
| 5 | Ford Maverick Hybrid | New | +4 | New: 0 (54/100) | New: 0 |
| 6 | Honda Civic Hybrid Hatchback | 9 | +3 | +1 → +2 (62/100) | −2 → 0 |
| 7 | Kia Niro Hybrid | 3 | +3 | +1 → +1 (61/100) | +1 → 0 |
| 8 | Kia Sorento Hybrid | New | +3 | New: −1 (52/100) | New: 0 |
| 9 | Kia Sportage Plug-in Hybrid | 4 | +3 | +1 → +1 (61/100) | −1 → 0 |
| 10 | Hyundai Tucson Plug-in Hybrid | 6 | +3 | 0 → +1 (60/100) | −1 → 0 |
| 11 | Toyota Sienna | New | +3 | New: 0 (55/100) | New: 0 |
| 12 | Hyundai IONIQ 5 | 12 | +3 | +1 → +2 (62/100) | +2 → +2 |
| 13 | Toyota Crown Signia | New | +3 | New: 0 (57/100) | New: 0 |
| 14 | Toyota Highlander Hybrid | New | +3 | New: 0 (54/100) | New: 0 |
| 15 | Toyota Prius | 8 | +2 | +2 → +2 (65/100) | +1 → 0 |
| 16 | Hyundai Elantra Hybrid | 15 | +2 | +1 → +2 (62/100) | +1 → 0 |
| 17 | Hyundai Santa Fe Hybrid | New | +2 | New: −1 (53/100) | New: 0 |
| 18 | Toyota bZ | 21 | +2 | +2 → +2 (66/100) | +2 → +2 |
| 19 | Subaru Solterra | 13 | +2 | +2 → +2 (66/100) | +2 → +2 |
| 20 | Mazda CX-5 | 14 | +2 | −2 → −1 (49/100) | −2 → 0 |
| 21 | Toyota Prius Plug-in Hybrid | 16 | +1 | +2 → +2 (71/100) | −1 → 0 |
| 22 | Toyota Corolla Cross Hybrid | 23 | +1 | 0 → +1 (60/100) | +1 → 0 |
| 23 | Kia Sportage Hybrid | 17 | +1 | −1 → 0 (56/100) | +1 → 0 |
| 24 | Toyota RAV4 Hybrid | 18 | +1 | 0 → 0 (57/100) | −2 → 0 |
| 25 | Hyundai Tucson Hybrid | 19 | +1 | −1 → −1 (53/100) | +1 → 0 |
| 26 | Honda Accord Hybrid | 26 | +1 | 0 → +1 (59/100) | +1 → 0 |
| 27 | Subaru Crosstrek Hybrid | 27 | +1 | 0 → 0 (57/100) | −2 → 0 |
| 28 | Mazda CX-50 Hybrid | 20 | +1 | −1 → 0 (56/100) | +1 → 0 |
| 29 | Nissan LEAF | 28 | +1 | +2 → +2 (64/100) | +2 → +2 |
| 30 | Kia Carnival Hybrid | New | +1 | New: −1 (53/100) | New: 0 |
| 31 | Subaru Outback | New | +1 | New: −1 (49/100) | New: 0 |
| 32 | Hyundai Palisade | New | +1 | New: −2 (42/100) | New: 0 |
| 33 | Toyota Corolla Hybrid | 30 | 0 | +1 → +2 (62/100) | +1 → 0 |
| 34 | Subaru Impreza | 24 | 0 | −1 → −1 (51/100) | −1 → 0 |
| 35 | Hyundai Sonata Hybrid | 25 | 0 | +1 → +1 (60/100) | +1 → 0 |
| 36 | Lexus UX 300h | 31 | 0 | 0 → 0 (56/100) | +1 → 0 |
| 37 | Nissan Rogue | 11 | 0 | −1 → −1 (52/100) | −1 → 0 |
| 38 | Lexus NX 350h | 22 | 0 | 0 → 0 (57/100) | +1 → 0 |
| 39 | Kia EV6 | 33 | 0 | +1 → +2 (63/100) | +2 → +2 |
| 40 | Tesla Model Y | 7 | 0 | +2 → 0 (57/100) | +2 → +2 |
| 41 | Hyundai Santa Cruz | New | 0 | New: −2 (42/100) | New: 0 |
| 42 | BMW X1 | 39 | −1 | −2 → −1 (49/100) | −1 → 0 |
| 43 | Honda Pilot | New | −1 | New: −2 (43/100) | New: 0 |
| 44 | Genesis GV70 | 29 | −1 | −2 → −2 (41/100) | −1 → 0 |
| 45 | Honda HR-V | 34 | −2 | −1 → −1 (50/100) | −1 → 0 |
| 46 | Chevrolet Bolt | 35 | −2 | +2 → +2 (65/100) | +2 → +2 |
| 47 | Kia K4 Hatchback | 36 | −2 | −1 → −1 (52/100) | −2 → 0 |
| 48 | Ford Mustang Mach-E | 42 | −2 | 0 → +1 (60/100) | +2 → +2 |
| 49 | Honda Odyssey | New | −2 | New: −2 (43/100) | New: 0 |
| 50 | Chevrolet Equinox EV | 43 | −3 | 0 → +1 (60/100) | +2 → +2 |
| 51 | Volkswagen Tiguan | 32 | −3 | −2 → −2 (48/100) | −1 → 0 |
| 52 | Mazda CX-30 | 37 | −3 | −2 → −2 (46/100) | −1 → 0 |
| 53 | Acura RDX | 40 | −3 | −2 → −2 (44/100) | −1 → 0 |
| 54 | Volkswagen Golf GTI | 41 | −4 | −2 → −1 (49/100) | −1 → 0 |
| 55 | Mazda3 Hatchback | 45 | −4 | −2 → −2 (48/100) | −1 → 0 |
| 56 | Tesla Model 3 | 38 | −4 | +2 → 0 (55/100) | +2 → +2 |
| 57 | Kia Seltos | 44 | −5 | −2 → −2 (47/100) | −1 → 0 |

## Screening ledger

Retained decisions from the earlier audit remain below alongside the new screening outcomes. The currently selected configuration in `data.json` supersedes older shorthand in a retained candidate name/reason.

| Candidate | Decision | Rationale / sources |
| --- | --- | --- |
| Lexus NX 350h | Retained / configuration re-audited | Standard FWD includes Lexus Safety System+ 3.0 and the standard power rear door; no Premium or hands-free-door option is selected. Rear space is adequate; long gear needs a verified carrier route. [Lexus NX pricing and equipment](https://pressroom.lexus.com/2026-lexus-nx-adds-grades-and-drivetrain/); [Lexus NX US model equipment](https://www.lexus.com/models/NX?trim=nxh-1) |
| Mazda CX-50 Hybrid | Retained / configuration re-audited | Estimated absent for the selected Hybrid Preferred: the available equipment description supports MRCC, while CTS continuous centering is not established for this grade. Best estimate is adaptive cruise with corrective lane support, so centering input remains 0/5. This is estimated fitment, not a verified absence. [Mazda CX-50 pricing and packaging](https://news.mazdausa.com/2025-09-16-2026-Mazda-CX-50-Pricing-and-Packaging) |
| Toyota RAV4 Hybrid | Retained / configuration re-audited | New generation, entry LE with Toyota Safety Sense 4.0. No power-door upgrade. Useful cabin and luggage area; FWD tires and clearance remain relevant for winter. [Toyota RAV4 pricing and equipment](https://pressroom.toyota.com/all-new-2026-toyota-rav4-takes-center-stage-in-whats-your-rav4-campaign/) |
| Lexus UX 300h | Retained / configuration re-audited | Base seats are power adjustable; ventilation and the powered rear door belong to higher grades. Tight rear seating and luggage room constrain three-adult trips. [Lexus UX pricing and equipment](https://pressroom.lexus.com/2026-lexus-ux-300h-a-powerful-hybrid-hatchback/) |
| BMW X3 | Held out: budget/equipment | The referenced $51,300 base + $3,450 Premium/assistance build exceeds $60k OTD after destination/tax/fees. A cheaper fully verified assisted build was not established; this is not a claim that every X3 is ineligible. [BMW X3 equipment](https://www.bmwusa.com/vehicles/x-series/x3/bmw-x3.html) |
| Mazda CX-30 | Retained / configuration re-audited | Turbo Premium Plus is the documented CTS grade; its turbo powertrain and 25-MPG EPA record replace the old non-turbo assumptions. Rear accommodation stays tight. [Mazda CX-30 pricing and packaging](https://news.mazdausa.com/2025-09-18-2026-Mazda-CX-30-Pricing-and-Packaging) |
| Kia Sportage Hybrid | Retained / configuration re-audited | LX now includes stop/go cruise and LFA2. Cloth/manual-seat equipment is less plush than SX-Prestige, but avoids paying for the old power-door constraint. [Kia sportage-hev 2026 pricing](https://www.kiamedia.com/us/en/models/sportage-hev/2026/pricing); [Kia sportage-hev equipment](https://www.kiamedia.com/us/en/models/sportage-hev/2026/features) |
| Mazda CX-5 | Retained / configuration re-audited | The all-new 2026 Premium Plus explicitly includes CTS with Lane Change Assist and a power rear gate. Large touchscreen controls and actual ride/noise need a test drive. [Mazda CX-5 pricing and packaging](https://news.mazdausa.com/2026-01-13-Mazda-Announces-Pricing-and-Packaging-for-All-New-2026-Mazda-CX-5) |
| Hyundai IONIQ 5 | Retained / configuration re-audited | Entry SE Standard Range has stop/go cruise and LFA. The 245-mile EPA range is not the long-range model. Spacious flat-floor cabin; manual rear gate at this trim. [Hyundai IONIQ 5 SE Standard Range](https://www.hyundaiusa.com/us/en/vehicles/2026-ioniq-5/se-standard-range) |
| Ford Mustang Mach-E | Retained / configuration re-audited | Select retains adaptive cruise with lane centering. Technology Package and paid BlueCruise are unselected and receive no hands-free credit. Standard battery has 260 EPA miles. [Ford Mach-E Select pricing](https://www.ford.com/suvs/mach-e/models/select/); [Ford 2026 Mach-E order guide](https://www.fromtheroad.ford.com/content/dam/fordmediasite/us/en/library/2026/order-guides/2026_Ford_Mustang_Mach-E_Order_Guide.pdf); [Ford Mach-E package changes](https://www.fromtheroad.ford.com/us/en/articles/2026/whats-new-2026-ford-mustang-mach-e.html) |
| Honda CR-V Hybrid | Retained / configuration re-audited | Entry Sport hybrid includes Honda Sensing and Traffic Jam Assist without Sport-L liftgate pricing. Roomy cabin and straightforward controls; selected cloth/manual-gate equipment matters. [Honda CR-V pricing](https://hondanews.com/en-US/honda-automobiles/releases/release-cf005034e20eb27505fd8e6bbb056d5c-2026-honda-cr-v-pricing-and-epa-ratings-3); [Honda CR-V features by trim](https://www.hondainfocenter.com/2026/CR-V/Feature-Guide/Features-by-Trim/) |
| Subaru Forester Hybrid | Retained / configuration re-audited | Revised entry hybrid price; EyeSight with lane centering, heated seats and standard powered rear gate. Useful roof/cargo packaging and 8.7-inch clearance; new hybrid longevity is uncertain, with confidence shown separately. [Subaru Forester revised pricing](https://www.subaru.com/about/company-news/subaru-focuses-consumer-affordability-excellent-value-updated-pricing.html) |
| Nissan Rogue Rock Creek | Retained / configuration re-audited | SV supplies ProPILOT and power liftgate without Rock Creek packaging. FWD is the cheaper reference build; its 32-MPG EPA record is not the Rock Creek AWD record. [Nissan Rogue 2026.5 pricing](https://usa.nissannews.com/en-US/releases/2026-nissan-rogue-pricing); [Nissan Rogue equipment table](https://usa.nissannews.com/en-US/releases/2026-nissan-rogue-specifications) |
| Nissan LEAF | Retained / configuration re-audited | Redesigned S+ includes hands-on ProPILOT and has 303 EPA miles. It is not the old CHAdeMO LEAF; Platinum wheels and power-door equipment are unselected. [Nissan LEAF specifications and pricing](https://www.nissanusa.com/vehicles/electric-cars/leaf/specs-trims.html); [Nissan LEAF equipment table](https://usa.nissannews.com/en-US/releases/2026-nissan-leaf-specifications) |
| Hyundai Tucson Hybrid | Retained / configuration re-audited | Entry SE FWD has SCC and LFA with 38 MPG. Do not inherit Limited AWD features, powered gate or the AWD energy record. [Hyundai tucson-hybrid 2026](https://www.hyundaiusa.com/us/en/vehicles/tucson-hybrid/compare-specs) |
| Subaru Solterra | Retained / configuration re-audited | 2026 battery/charging update and 288-mile EPA range replace predecessor assumptions. Standard assistance and AWD; Premium does not receive Limited powered-gate credit. [Subaru Solterra pricing and trims](https://www.subaru.com/vehicles/solterra/2026/specs-trim.html) |
| Toyota bZ | Retained / configuration re-audited | Entry XLE FWD uses the smaller battery and 236-mile EPA range; it is not FWD Plus or Limited AWD. Standard Toyota Safety Sense and powered rear door. [Toyota bZ year-specific specifications](https://www.toyota.com/bz/2026/features/mpg_other_price/2870/2880/) |
| Tesla Model Y | Retained / configuration re-audited | Cash price before savings/incentives. Paid FSD (Supervised) is selected and costed for five years; driver supervision is mandatory. Sparse physical controls constrain ergonomics. [Tesla Model Y cash configurator](https://www.tesla.com/modely/design); [Tesla FSD subscription pricing](https://www.tesla.com/current-offers) |
| Kia EV6 | Retained / configuration re-audited | Entry Light includes HDA and stop/go cruise. The standard-range 237-mile battery is selected; Wind AWD and its powered-hatch equipment are not borrowed. [Kia ev6 2026 pricing](https://www.kiamedia.com/us/en/models/ev6/2026/pricing); [Kia ev6 equipment](https://www.kiamedia.com/us/en/models/ev6/2026/features) |
| Acura RDX | Retained / configuration re-audited | Base RDX already has ACC, speed-limited LKAS and powered tailgate. No Technology-package price or acoustic-side-glass benefit is assumed. LKAS does not provide low-speed traffic-jam steering. [Acura RDX September pricing](https://acuranews.com/en-US/releases/release-2a30447979673882e0608a518f07df8f-2026-acura-rdx-pricing-and-epa-ratings-september); [Acura RDX equipment table](https://acuranews.com/en-US/releases/2026-acura-rdx-specifications-features) |
| BMW X2 | Curated replacement | Overlaps the X1 powertrain/price class with less carrying flexibility. X1 now includes a documented assistance package; no need to retain both. [BMW X2 equipment](https://www.bmwusa.com/vehicles/x-series/x2/bmw-x2-overview.html) |
| BMW X1 | Retained / configuration re-audited | A manufacturer label establishes the $500 Driving Assistance Plus selection; retailer equipment description confirms ACC with steering assistance. No Professional/Technology package benefits are credited. [BMW X1 manufacturer window sticker](https://assets-cdn.space.auto/ckfe1plb); [BMW retailer selected assistance package](https://www.bmwseattle.com/inventory/new-2026-bmw-x1-xdrive28i-awd-suv-wbx73ef08t5719016/) |
| Genesis GV70 | Retained / configuration re-audited | Base 2.5T has heated power seats, powered liftgate, SCC and HDA. Leather, ventilation and higher-trim benefits are not assumed. Premium gasoline is costed. [Genesis GV70 current 2026 pricing](https://www.genesis.com/us/en/offers/gv70/previous); [Genesis GV70 manufacturer equipment label](https://www.genesis.com/us/en/services/windowsticker?VIN=5NMMADTB0TH040165&vehicleModel=GV70) |
| BMW 430i Gran Coupe | Held out: configuration evidence | Original base build had no verified ACC/centering. Complete current assistance-package prerequisites and OTD not established; not labeled unavailable. [BMW 4 Series Gran Coupe equipment](https://www.bmwusa.com/vehicles/4-series/gran-coupe/overview.html) |
| Kia Niro Hybrid | Retained / configuration re-audited | EX is the first documented navigation-based SCC grade; LFA is standard. Its efficient wheel configuration uses the FE EPA record, not the old SX assumption. [Kia niro-hev 2026 pricing](https://www.kiamedia.com/us/en/models/niro-hev/2026/pricing); [Kia niro-hev equipment](https://www.kiamedia.com/us/en/models/niro-hev/2026/features) |
| Mitsubishi Outlander | Held out: model-year mismatch | Old 2.5L/2024 assumptions do not establish the current 2026 equipment/powertrain. Current exact assisted configuration and price need re-verification. [Mitsubishi Outlander trim equipment](https://www.mitsubishicars.com/cars-and-suvs/outlander/trims) |
| MINI Countryman S ALL4 | Removed by request | MINI replaced by lower-cost practical hatchbacks and hybrids; no claim that the model is unavailable. [MINI Countryman equipment](https://www.miniusa.com/model/countryman.html) |
| Volvo XC40 | Held out: configuration evidence | Old Core build lacked verified Pilot Assist; a complete current package/trim quote was not established. No claim that every XC40 is ineligible. [Volvo XC40 equipment](https://www.volvocars.com/us/cars/xc40/specifications/) |
| Mercedes-Benz GLA 250 | Held out: configuration evidence | Old base build lacked verified driving-assistance package. Current option prerequisites and total cost unresolved; do not rank an unverified build as an assisted option. [Mercedes-Benz GLA equipment](https://www.mbusa.com/en/vehicles/class/gla/suv) |
| Audi Q3 | Held out: model-year mismatch | Old S line/current-page generation mismatch; named 2026 assisted package and current price not established. Manufacturer rolling page now shows 2027. [Audi Q3 equipment](https://www.audiusa.com/en/models/q3/q3/) |
| Kia Seltos | Retained / configuration re-audited | SX is required for SCC/HDA. A powered liftgate requires an additional package that is not selected; useful AWD but ride/noise and compact back seat limit comfort. [Kia seltos 2026 pricing](https://www.kiamedia.com/us/en/models/seltos/2026/pricing); [Kia seltos equipment](https://www.kiamedia.com/us/en/models/seltos/2026/features) |
| Jeep Compass | Curated replacement | Old build relied on unselected assistance and ranked poorly on cost/comfort inputs. Broader manual-hatch and efficient sedan alternatives replace it; not declared unavailable. [Jeep Compass assistance equipment](https://www.jeep.com/compass/technology.html) |
| GMC Terrain | Curated replacement | AT4 was selected around the old liftgate/utility constraints; replace this overlapping gas crossover with broader body styles and EV options. No Super Cruise capability inferred. [GMC Terrain fleet specifications](https://www.gmfleet.com/content/dam/gmfleet/na/us/en/index/pdfs/suvs/02-pdfs/2026%20GMC%20Terrain.pdf) |
| Lincoln Corsair | California ineligible | Listed 2026 Premiere/Reserve cannot be purchased for California registration; OEM disclosure verified. [Ford Pro California availability](https://www.fordpro.com/en-us/fleet-vehicles/lincoln-corsair/) |
| Chevrolet Equinox | Curated replacement | Gas RS + liftgate package no longer needed for eligibility. Equinox EV adds a materially different powertrain/value choice; not a claim that gas Equinox is unavailable. [Chevrolet Equinox equipment](https://www.chevrolet.com/suvs/previous-year/equinox) |
| Volkswagen Tiguan | Retained / configuration re-audited | All-new Tiguan S has standard IQ.DRIVE/Travel Assist. The cheapest S FWD uses the distinct 29-MPG record; SE power-gate and 4MOTION features are unselected. [Volkswagen Tiguan 2026 configurator](https://www.vw.com/en/builder.html/__app/tiguan.app) |
| Honda Civic Hybrid Hatchback | Added | Added manual-hatch alternative. Sport Hybrid is the least expensive hybrid hatch, with ACC/LKAS/TJA. Low clearance and long-gear packaging constrain mountain use; no Touring equipment is borrowed. [Honda Civic hatchback September pricing](https://hondanews.com/en-US/honda-automobiles/releases/release-bb136e6e7af7ccb6b0336e10d81121d6-2026-honda-civic-hatchback-pricing-and-epa-ratings-september); [Honda Civic hatchback equipment](https://automobiles.honda.com/2026/civic-hatchback/specs-features-trim-comparison) |
| Toyota Prius | Added | Entry LE is the 57-MPG configuration with TSS 3.0 and a manual hatch. Rear headroom, low seating and clearance should be checked with the third adult. [Toyota Prius 2026 price and equipment](https://www.toyota.com/prius/2026/section/features/) |
| Toyota Prius Plug-in Hybrid | Added | SE has 44 EPA electric miles and TSS 3.0; the plug-in battery reduces luggage flexibility. The five-year scenario assumes regular nearby charging, not all-electric driving. [Toyota Prius Plug-in Hybrid 2026](https://www.toyota.com/priuspluginhybrid/2026/) |
| Toyota Corolla Hybrid | Added | Low-cost sedan with TSS 3.0 and 50 MPG. The conventional trunk and rear-adult space constrain three-person long-gear trips without excluding the car. [Toyota Corolla Hybrid 2026](https://www.toyota.com/corolla/2026/section/trims/) |
| Toyota Camry Hybrid | Added | Roomier hybrid sedan with small wheels, TSS 3.0 and 51 MPG. Trunk access is less flexible than a hatch; rear seats and ski pass-through need an actual fit check. [Toyota Camry 2026 pricing and specifications](https://www.toyota.com/camry/2026/features/mpg_other_price/2559/) |
| Honda Accord Hybrid | Added | Entry hybrid Sport includes Honda Sensing/TJA. Large rear seating area and trunk are useful, but low clearance and 19-inch wheels constrain ride/winter use. [Honda Accord September pricing](https://hondanews.com/en-US/honda-automobiles/releases/release-bb136e6e7af7ccb6b0336e10d810f9e5-2026-honda-accord-pricing-epa-ratings-september) |
| Hyundai Elantra Hybrid | Added | Current feature matrix restricts SCC to Limited despite LFA on every trim. Select Limited with its upgraded seats; do not mistake LFA-only availability for an adaptive-cruise package. Compact trunk access and low clearance limit long-gear use. [Hyundai Elantra Hybrid Limited](https://www.hyundaiusa.com/us/en/vehicles/elantra-hybrid/limited) |
| Hyundai Sonata Hybrid | Added | Blue supplies SCC/LFA without Limited pricing and returns 51 MPG. Smart trunk release is not a powered liftgate; rear-adult room is useful but roof/gear fit remains conditional. [Hyundai Sonata Hybrid Blue](https://www.hyundaiusa.com/us/en/vehicles/2026-sonata-hev/blue-hybrid) |
| Mazda3 Hatchback | Added | This is the documented CTS automatic hatch configuration. Turbo AWD has a 26-MPG EPA record; no power hatch. Rear space and low clearance constrain three-adult mountain trips. [Mazda3 pricing and packaging](https://news.mazdausa.com/2026-Mazda3) |
| Volkswagen Golf GTI | Added | S includes IQ.DRIVE/Travel Assist and automatic DSG. Supportive sport seats suit some drivers, but a firmer ride and low clearance are relevant comfort/winter tradeoffs. [Volkswagen Golf GTI standard IQ.DRIVE](https://www.vw.com/en/models/golf-gti.html) |
| Subaru Impreza | Added | Entry Sport has EyeSight with lane centering and AWD. Manual hatch is allowed; clearance is lower than Crosstrek despite the traction system. [Subaru Impreza 2026 specifications](https://www.subaru.com/services/vehicles/pdf/trimComparison/2026/IMP?hideBuildMsrp=false) |
| Subaru Crosstrek Hybrid | Added | New conventional hybrid, not the older plug-in Crosstrek. EyeSight, AWD and 8.7-inch clearance help winter access; actual rear/luggage fit is still conditional. [Subaru Crosstrek Hybrid 2026 specifications](https://www.subaru.com/services/vehicles/pdf/trimComparison/2026/CTK?hideBuildMsrp=false) |
| Toyota Corolla Cross Hybrid | Added | Entry hybrid S includes TSS 3.0 and AWD. Modest rear space and manual-gate equipment keep the price below an unnecessary liftgate upgrade. [Toyota Corolla Cross Hybrid 2026 specifications](https://www.toyota.com/corollacross/features/mpg_other_price/6312/) |
| Honda HR-V | Added | LX has Honda Sensing with ACC/LKAS, so EX-L is unnecessary for assistance. Modest 2.0L power and rear-seat/cargo fit need a loaded-trip check. [Honda HR-V 2026 pricing](https://hondanews.com/en-US/releases/release-cf005034e20eb27505fd8e6bbb055118-2026-honda-hr-v-pricing-and-epa-ratings-3) |
| Chevrolet Equinox EV | Added | Estimated absent for the selected base LT1: the available trim evidence supports ACC and corrective lane keeping. The manual describes optional Hands-On Steering Assist with connected-plan conditions; base-grade fitment/entitlement is not established. Best estimate is no continuous centering (0/5), rather than crediting an unselected option. This is estimated fitment, not a verified absence. [Chevrolet Equinox EV 2026](https://www.chevrolet.com/electric/previous-year/equinox-ev) |
| Chevrolet Bolt | Added | New 2027 Bolt is on sale with 262 EPA miles and standard ACC. Super Cruise needs extra packages; no centering credit or paid entitlement is inferred for base LT. [Chevrolet Bolt 2027 pricing and features](https://news.chevrolet.com/newsroom.detail.html/Pages/topic/us/en/2026/apr/0422-Chevrolet-Bolt.html) |
| Tesla Model 3 | Added | Cash price before savings/incentives. Five years of $99/month FSD (Supervised) are explicitly costed; driver supervision is mandatory. Conventional trunk and sparse controls affect utility/ergonomics. [Tesla Model 3 cash configurator](https://www.tesla.com/model3/design); [Tesla FSD subscription pricing](https://www.tesla.com/current-offers) |
| Hyundai Tucson Plug-in Hybrid | Added | SEL provides SCC/LFA, powered gate and 32 EPA electric miles. PHEV carries extra systems and the electric-mile split is a scenario assumption. [Hyundai tucson-plug-in-hybrid 2026](https://www.hyundaiusa.com/us/en/vehicles/tucson-plug-in-hybrid/compare-specs) |
| Kia Sportage Plug-in Hybrid | Added | Entry X-Line PHEV has SCC/LFA and powered gate, with 33 EPA electric miles. Not the more expensive X-Line Prestige equipment list. [Kia sportage-phev 2026 pricing](https://www.kiamedia.com/us/en/models/sportage-phev/2026/pricing); [Kia sportage-phev equipment](https://www.kiamedia.com/us/en/models/sportage-phev/2026/features) |
| Toyota RAV4 Plug-in Hybrid | Added | Redesigned SE plug-in offers 54 EPA electric miles, a standard power liftgate and TSS 4.0. Do not reuse the old RAV4 Prime environmental score or higher-grade charging/comfort equipment. [Toyota RAV4 Plug-in Hybrid 2026 specifications](https://www.toyota.com/rav4pluginhybrid/features/mpg_other_price/4544/4550/); [Toyota RAV4 SE manufacturer window sticker](https://www.andersontoyota.com/resrc/toyotawindowsticker/getByVIN/?vin=JTM7ERAV3TJ007411) |
| Kia K4 Hatchback | Added | Affordable manual-hatch alternative with standard stop/go SCC and LFA. EX 2.0L uses the 30-MPG EPA record, not the turbo model. [Kia k4-hatchback 2026 pricing](https://www.kiamedia.com/us/en/models/k4-hatchback/2026/pricing); [Kia k4-hatchback equipment](https://www.kiamedia.com/us/en/models/k4-hatchback/2026/features) |
| Hyundai IONIQ 6 | Held out: current new inventory needed | No regular 2026 US model in the checked EPA data; manufacturer-confirmed discontinuation reported by Edmunds. Remaining new 2025 stock requires an actual current quote; N is not a substitute configuration. [Current IONIQ 6 US availability](https://www.edmunds.com/car-news/2026-hyundai-ioniq-6-discontinued.html); [EPA downloadable vehicle data](https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip) |
| Toyota Sienna | Added: representative market expansion | Eight-seat hybrid minivan, power sliding doors and liftgate. Fold the third row and retain a second-row adult; long gear still needs an actual fit check. [Toyota Sienna 2026 pricing and standard equipment](https://www.toyota.com/sienna/2026/features/); [Toyota current delivery/processing charges](https://www.toyota.com/gst/deals-incentives/financial-estimates-highlanderhybrid/?vehicles=highlanderhybrid) |
| Honda Odyssey | Added: representative market expansion | Leather/heated front seats, sliding second row and folding third row provide a distinct people-and-gear option. LKAS is speed-limited and does not supply low-speed traffic-jam steering. [Honda Odyssey 2026 pricing](https://hondanews.com/en-US/honda-automobiles/releases/release-6f8b202ddb1c7f26ecd92774bb031f99-2026-honda-odyssey-pricing-and-epa-ratings); [Honda Odyssey 2026 equipment](https://www.hondainfocenter.com/2026/Odyssey/Feature-Guide/Specifications/) |
| Kia Carnival Hybrid | Added: representative market expansion | Hybrid minivan with power sliding doors and a manual rear liftgate at LXS. Three-row packaging adds useful interior carrying space without crediting EX/SX liftgate equipment. [Kia Carnival Hybrid 2026 pricing](https://www.kiamedia.com/us/en/models/carnival-hev/2026/pricing); [Kia Carnival Hybrid 2026 equipment](https://www.kiamedia.com/us/en/models/carnival-hev/2026/features) |
| Ford Maverick Hybrid | Added: representative market expansion | Compact hybrid pickup with heated front seats and a short open bed. AWD Lariat uses its own 36-MPG EPA record, not the 38-MPG FWD record. Weatherproof gear storage is extra. [Ford Maverick Lariat 2026 equipment](https://www.ford.com/trucks/maverick/models/lariat/); [Ford 2026 Lariat AWD hybrid manufacturer label](https://www.windowsticker.forddirect.com/windowsticker.pdf?vin=3FTTW8S31TRB75802) |
| Hyundai Santa Cruz | Added: representative market expansion | Turbo AWD compact pickup with XRT clearance/traction features, heated fronts and open-bed carrying flexibility. Rear accommodation is tighter than a minivan; test the third adult and gear. [Hyundai Santa Cruz XRT 2026 equipment and pricing](https://www.hyundaiusa.com/us/en/vehicles/2026-santa-cruz/xrt) |
| Subaru Outback | Added: representative market expansion | Redesigned 2.5L AWD SUV with 8.7-inch clearance, a long cargo area and power rear gate. It remains a useful wagon-like alternative but Subaru classifies it as an SUV. [Subaru Outback 2026 manufacturer equipment comparison](https://www.subaru.com/services/vehicles/pdf/trimComparison/2026/OBK?hideBuildMsrp=false); [Subaru 2026 Outback pricing announcement](https://www.prnewswire.com/news-releases/subaru-announces-pricing-on-all-new-2026-outback-suv-302535958.html) |
| Toyota Crown Signia | Added: representative market expansion | Two-row hybrid SUV with a long load area and heated/ventilated leather front seats. Wagon-like utility does not make it a manufacturer-classified wagon. No Advanced Technology package is selected. [Toyota Crown Signia 2026 pricing and equipment](https://www.toyota.com/crownsignia/features/); [Toyota current delivery/processing charges](https://www.toyota.com/gst/deals-incentives/financial-estimates-highlanderhybrid/?vehicles=highlanderhybrid) |
| Hyundai Santa Fe Hybrid | Added: representative market expansion | Entry three-row hybrid with cloth seats and a powered liftgate. SE receives ordinary SCC/LFA, not higher-grade navigation-based cruise or HDA2 lane changes. [Hyundai Santa Fe Hybrid SE 2026 pricing and equipment](https://www.hyundaiusa.com/us/en/vehicles/2026-santa-fe-hybrid/se); [Hyundai Santa Fe Hybrid 2026 manufacturer label](https://monroneylabels.com/cars/15246353-2026-hyundai-santa-fe-hybrid/window_sticker.pdf?cfl=3532684500) |
| Kia Sorento Hybrid | Added: representative market expansion | Three-row hybrid with heated fronts and a power tailgate. Keep the third row folded for three adults plus mountain gear; its smaller cabin does not receive minivan carrying credit. [Kia Sorento Hybrid 2026 pricing](https://www.kiamedia.com/us/en/models/sorento-hev/2026/pricing); [Kia Sorento Hybrid 2026 equipment](https://www.kiamedia.com/us/en/models/sorento-hev/2026/features) |
| Toyota Highlander Hybrid | Added: representative market expansion | Three-row AWD hybrid with heated front seats and powered liftgate. Third-row passenger use competes with luggage; the assessed mountain scenario retains one second-row adult. [Toyota Highlander 2026 equipment and pricing](https://pressroom.toyota.com/2026-toyota-highlander-gets-standard-all-wheel-drive-across-the-lineup/); [Toyota current delivery/processing charges](https://www.toyota.com/gst/deals-incentives/financial-estimates-highlanderhybrid/?vehicles=highlanderhybrid) |
| Honda Pilot | Added: representative market expansion | Three-row V6 SUV in entry Sport FWD trim. Cloth seats, power tailgate and Traffic Jam Assist are assessed; TrailSport AWD, tires and acoustic upgrades are unselected. [Honda Pilot September 2026 pricing](https://hondanews.com/en-US/honda-automobiles/releases/release-bb136e6e7af7ccb6b0336e10d8119451-2026-honda-pilot-pricing-and-epa-ratings-september); [Honda Pilot 2026 equipment](https://www.hondainfocenter.com/2026/Pilot/Feature-Guide/Specifications/) |
| Hyundai Palisade | Added: representative market expansion | Redesigned three-row V6 SUV with cloth seats and powered liftgate. SE includes navigation-based cruise and forward-attention warning; no HDA2 assisted lane change or Calligraphy comfort equipment is credited. [Hyundai Palisade SE 2026 pricing and equipment](https://www.hyundaiusa.com/us/en/vehicles/2026-palisade/se); [Hyundai 2026 Palisade pricing and freight reference](https://www.kbb.com/car-news/hyundai-nails-down-2026-palisade-starting-prices/) |
| Ford Ranger | Held out: evidence/eligibility unresolved | Held out: the checked 2026 US order guide establishes ACC and lane keeping, but not continuous lane centering in the proposed XLT package. Do not confuse corrective support with centering; no complete eligible assisted build established. [Ford Ranger 2026 order guide](https://www.fromtheroad.ford.com/content/dam/fordmediasite/us/en/library/2026/order-guides/2026_Ford_Ranger_Order_Guide.pdf) |
| Chrysler Pacifica Plug-in Hybrid | Held out: evidence/eligibility unresolved | Held out: discontinued-model notice and remaining-stock uncertainty. A 2026 EPA record alone does not establish an orderable new assisted configuration; a current local build/quote would be needed. [Chrysler Pacifica Hybrid discontinued-model notice](https://www.chrysler.com/crossbrand_us/common/bridge/chrysler/vhp.html?vehicle=pacifica_hybrid&year=2024) |
| Volvo V60 wagon | Held out: evidence/eligibility unresolved | Wagon coverage gap: no current assisted new US V60 build at or below $60k OTD was established. Outback and Crown Signia are manufacturer-classified SUVs, so neither is relabeled to fill the gap. Older-model new inventory needs an actual quote. [Volvo V60 wagon US model reference](https://www.volvocars.com/us/cars/v60-hybrid/) |

## Reproduction and validation

```sh
python3 -B scripts/test_car_rankings.py
python3 -B scripts/build_car_rankings.py --check
node --test scripts/test_car_rankings_pareto.js
python3 -B scripts/test_car_rankings_browser.py
```

Regression coverage includes tie/boundary/order invariance, shared canonical scores, evidence contracts, proxy source-record consistency, confidence-independent maintenance, RAV4/PHEV baselines, coverage/classification, selected energy records, dynamic cohort counts, cost arithmetic, real slider keyboard input, dialog contributions, Pareto graph counts checked against an independent Python dominance calculation, desktop/mobile layout, focus handling, legacy links and offline/no-JavaScript fallback. Browser screenshots are written outside the repository.
