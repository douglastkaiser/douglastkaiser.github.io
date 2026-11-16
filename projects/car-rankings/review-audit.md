# Review and scoring audit — November 16, 2026

Baseline: `8ae55dc` on `main`. All 57 configurations and all 342 category results were reviewed. The cost calculation and lifecycle-anchor calculations were rerun; their raw inputs were retained. This report distinguishes source checks, qualitative judgments and unresolved measurements. It is not 57 new road tests or a claim that all 2026 trim prices, future resale values and insurance quotes were freshly verified.

## Research coverage

- Retrieved all **55 linked EPA vehicle API records** and checked model year, manufacturer, selected energy consumption and stored drivetrain reference. No energy discrepancy was found. Prius Plug-in Hybrid and RAV4 Plug-in Hybrid have no linked EPA record; a fresh 2026 Toyota model-menu lookup did not establish one. Their disclosed manufacturer/current-configuration estimates remain estimates.
- Retrieved current-model Edmunds review pages and their Comfort, Driving experience and In-cabin tech discussions for **56 configurations**, including the **2027** Bolt and Standard-specific Tesla pages. These pages can reuse earlier tests or test a different trim. Qualitative findings were reviewed; publisher numeric ratings were **not** converted into our scores because their class comparisons and tested builds differ.
- Sportage Plug-in Hybrid's Edmunds page had no scored review. The accessible Consumer Reports road-test excerpt was insufficient to establish an exact X-Line comfort advantage; its first three comfort inputs remain at the baseline. No paywalled rating was inferred.
- Rechecked selected assistance against current manufacturer material, including Kia matrices, Hyundai trim pages, Toyota/Subaru brochures, Mazda specifications, Ford equipment descriptions, Nissan specifications and VW instructions. Two omitted navigation-based-cruise capabilities and one omitted driver-monitoring capability were corrected, as detailed below. Feature presence is not an independent execution/safety rating.
- Historical lifecycle inputs remain traceable 2024 records/proxy means. The published table still lists Solterra 66 and Equinox EV FWD 52; that discrepancy was not invented by the ranking. These are **not current-model environmental measurements**. No arbitrary redesign, MPG or battery adjustment was added. Model-specific reliability remains unmeasured; all cars keep the shared disruption/service-access baselines.

The compact [evidence snapshot](evidence-audit.json) records every EPA result and review URL/status/scope. All 57 car dialogs now expose review sources, confidence, and four comfort rationales. Source `checked` dates were advanced only for newly retrieved review/EPA references and newly checked assistance sources; existing pricing sources retain their earlier dates.

## Rubric corrections applied consistently

**Cost and Eco retain the existing relative midpoint-percentile bands.** Every other category now uses fixed bands around the component rubric's 3/5 workable baseline:

| Weighted composite /5 | Score | Interpretation |
| --- | ---: | --- |
| Below 1.5 | −2 | Very constrained |
| 1.5 to below 2.5 | −1 | Constrained |
| 2.5 to below 3.5 | 0 | Workable or uncertain |
| 3.5 to below 4.5 | +1 | Useful capability |
| 4.5 or above | +2 | Strong capability |

These are editorial policy thresholds, not empirically calibrated quality cutoffs. They prevent a 3.2/5 comfort composite from becoming +1 merely because other cars have manual hatches, and stop many small feature differences turning into two-point tier swings. Adding an unrelated vehicle cannot change a capability score. Raw category ranks still order composites and share exact ties. Relative Cost/Eco bands can still change with the cohort.

**Comfort:** removed equipment/brand-based seat and control advantages. Used explicitly qualified model-level review evidence for noise, seat support, adult rear room, control reach and screen/gauge issues. A positive review of a different trim is not sufficient by itself to borrow its upgraded seat, adaptive damper or tire behavior. First three components retain 3/5 where transfer is weak. Negative and positive findings use the same standard; no blanket EV, luxury or Subaru adjustment was made. A powered gate still earns its existing 10% convenience credit, but cannot alone turn a baseline cabin positive.

**Assistance:** Seltos SX changes `[4,4,3] → [5,4,3]` for documented navigation-based curve cruise. Tucson PHEV SEL changes `[4,4,3] → [5,4,4]` for navigation-based curve cruise and Forward Attention Warning. Sportage PHEV X-Line stays `[4,4,3]`; its matrix reserves navigation-based cruise for Prestige. Other capability vectors remain, including Solterra's `[4,5,4]`. Renamed the third component **Driver supervision**: it describes equipment, not measured usability. Reviews identify execution concerns, but a common cross-system intervention/false-alert benchmark has not been established, so execution is not assigned invented numerical penalties.

**Trips:** reviewed all carrying/access/replenishment vectors and retained them as planning estimates. All route/gear-fit caveats remain explicit. A 288-mile EPA label, AWD, NACS connector or peak kW does not establish loaded winter-trip success. EV practicality remains provisionally 3/5; rapid liquid-fuel replenishment remains 5/5. Fixed bands reduce artificial separation of otherwise workable cars. This still does not replace a winter route/charger assessment.

**Cost:** recalculated every 5-year scenario, including selected subscriptions, depreciation, taxes, registration and powertrain upkeep. No arithmetic or stored EPA discrepancy found. Published MSRP/destination, resale estimates, common insurance/repair reserves and local charging assumption are retained. Shared allowances can conceal real insurance/repair differences, and mixed historical-model versus segment depreciation proxies remain a material uncertainty; no new transaction/insurance quote was obtained.

**Eco:** all historical records and proxy means retain their existing values. Exact anchor selection and model-year transfer can materially affect results. Turning Eco off remains available; proxy confidence is visible without a hidden scoring penalty.

**Upkeep:** shared disruption/service-access baselines retained. EV routine-work advantage remains supported only at powertrain level. Under fixed bands EVs receive +1 rather than the previous +2; other powertrains remain 0. This is service effort, not a current-model reliability forecast, and starts off.

## Before/after scores — complete cohort

Unchanged cells show one value. Upkeep remains **0×** in the default total. `#` is default weighted rank, with equal totals ordered by lower five-year cost, then name.

Category results changed: cost: 0/57, eco: 0/57, mountain: 44/57, lux: 45/57, commute: 53/57, maintenance: 10/57; **152/342** in total. Changes include both reviewed inputs and the disclosed rubric conversion.

| New # | Vehicle | Old # | Cost | Eco | Trips | Comfort | Assist | Upkeep | Total |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | Toyota Camry Hybrid | 6 | +2 | +2 | −1 → 0 | 0 → +1 | 0 → +1 | 0 | +3 → +6 |
| 2 | Honda CR-V Hybrid | 2 | +1 | +1 | +2 → +1 | 0 → +1 | 0 → +1 | 0 | +4 → +5 |
| 3 | Subaru Forester Hybrid | 3 | +1 | 0 | +2 | +1 | 0 → +1 | 0 | +4 → +5 |
| 4 | Toyota Prius | 20 | +2 | +2 | −1 → 0 | −2 → −1 | 0 → +1 | 0 | +1 → +4 |
| 5 | Honda Civic Hybrid Hatchback | 15 | +2 | +1 | −1 → 0 | 0 | 0 → +1 | 0 | +2 → +4 |
| 6 | Toyota Corolla Cross Hybrid | 7 | +2 | +1 | 0 → +1 | 0 → −1 | 0 → +1 | 0 | +3 → +4 |
| 7 | Kia Sportage Hybrid | 28 | +2 | 0 | 0 → +1 | −2 → 0 | 0 → +1 | 0 | 0 → +4 |
| 8 | Toyota RAV4 Hybrid | 29 | +2 | 0 | 0 → +1 | −2 → 0 | 0 → +1 | 0 | 0 → +4 |
| 9 | Subaru Crosstrek Hybrid | 23 | +1 | +1 | +1 | −2 → 0 | 0 → +1 | 0 | +1 → +4 |
| 10 | Toyota RAV4 Plug-in Hybrid | 4 | 0 | +2 | +1 | +1 → 0 | 0 → +1 | 0 | +4 |
| 11 | Hyundai Tucson Plug-in Hybrid | 11 | 0 | +1 | +1 | +1 | 0 → +1 | 0 | +3 → +4 |
| 12 | Hyundai Elantra Hybrid | 21 | +2 | +1 | −2 → −1 | 0 | 0 → +1 | 0 | +1 → +3 |
| 13 | Toyota Prius Plug-in Hybrid | 27 | +2 | +2 | −2 → −1 | −2 → −1 | 0 → +1 | 0 | 0 → +3 |
| 14 | Subaru Impreza | 38 | +2 | −1 | 0 → +1 | −2 → 0 | 0 → +1 | 0 | −1 → +3 |
| 15 | Kia Niro Hybrid | 8 | +1 | +1 | −1 → 0 | 0 | +2 → +1 | 0 | +3 |
| 16 | Hyundai Sonata Hybrid | 39 | +1 | +1 | −1 → 0 | −2 → 0 | 0 → +1 | 0 | −1 → +3 |
| 17 | Honda Accord Hybrid | 22 | +1 | +1 | −1 → 0 | 0 | 0 → +1 | 0 | +1 → +3 |
| 18 | Nissan LEAF | 40 | +1 | +2 | −2 → 0 | −2 → −1 | 0 → +1 | +2 → +1 | −1 → +3 |
| 19 | Kia Sportage Plug-in Hybrid | 10 | 0 | +1 | +1 | +1 → 0 | 0 → +1 | 0 | +3 |
| 20 | Toyota bZ | 17 | 0 | +2 | −1 → 0 | +1 → 0 | 0 → +1 | +2 → +1 | +2 → +3 |
| 21 | Subaru Solterra | 1 | −1 | +2 | +1 | +1 → 0 | +2 → +1 | +2 → +1 | +5 → +3 |
| 22 | Toyota Corolla Hybrid | 19 | +2 | +1 | −2 → −1 | 0 → −1 | 0 → +1 | 0 | +1 → +2 |
| 23 | Hyundai Tucson Hybrid | 30 | +1 | −1 | +2 → +1 | −2 → 0 | 0 → +1 | 0 | 0 → +2 |
| 24 | Hyundai Santa Fe Hybrid | 16 | 0 | −1 | +2 → +1 | +1 | 0 → +1 | 0 | +2 |
| 25 | Kia Sorento Hybrid | 9 | 0 | −1 | 0 → +1 | +2 → +1 | +2 → +1 | 0 | +3 → +2 |
| 26 | Ford Maverick Hybrid | 5 | 0 | 0 | +1 | +1 → 0 | +2 → +1 | 0 | +4 → +2 |
| 27 | Toyota Sienna | 12 | 0 | 0 | +2 → +1 | +1 → 0 | 0 → +1 | 0 | +3 → +2 |
| 28 | Hyundai IONIQ 5 | 33 | 0 | +1 | −1 → 0 | −2 → 0 | +2 → +1 | +2 → +1 | 0 → +2 |
| 29 | Toyota Crown Signia | 13 | −1 | 0 | +2 → +1 | +2 → +1 | 0 → +1 | 0 | +3 → +2 |
| 30 | Kia EV6 | 41 | −1 | +2 | −2 → 0 | −2 → 0 | +2 → +1 | +2 → +1 | −1 → +2 |
| 31 | Subaru Outback | 25 | −1 | −1 | +2 | +1 | 0 → +1 | 0 | +1 → +2 |
| 32 | Ford Mustang Mach-E | 47 | −1 | +2 | −1 → 0 | −2 → 0 | 0 → +1 | +2 → +1 | −2 → +2 |
| 33 | Honda HR-V | 45 | +2 | −1 | −1 → 0 | 0 | −2 → 0 | 0 | −2 → +1 |
| 34 | Chevrolet Bolt | 49 | +1 | +2 | −2 → 0 | −2 → −1 | −2 → −1 | +2 → +1 | −3 → +1 |
| 35 | Kia K4 Hatchback | 50 | +1 | −1 | −1 → 0 | −2 → 0 | 0 → +1 | 0 | −3 → +1 |
| 36 | Mazda CX-50 Hybrid | 24 | +1 | 0 | +1 | +1 → 0 | −2 → −1 | 0 | +1 |
| 37 | Lexus UX 300h | 31 | +1 | 0 | −2 → 0 | +1 → −1 | 0 → +1 | 0 | 0 → +1 |
| 38 | Nissan Rogue | 32 | 0 | −1 | 0 → +1 | +1 → 0 | 0 → +1 | 0 | 0 → +1 |
| 39 | Toyota Highlander Hybrid | 14 | −1 | 0 | +2 → +1 | +2 → 0 | 0 → +1 | 0 | +3 → +1 |
| 40 | Lexus NX 350h | 34 | −1 | 0 | −1 → 0 | +2 → 0 | 0 → +1 | 0 | 0 |
| 41 | Kia Carnival Hybrid | 35 | −1 | −1 | +2 → +1 | −2 → 0 | +2 → +1 | 0 | 0 |
| 42 | Tesla Model Y | 36 | −2 | 0 | 0 | 0 | +2 | +2 → +1 | 0 |
| 43 | Volkswagen Tiguan | 53 | −1 | −2 | 0 → +1 | −2 → 0 | +1 | 0 | −4 → −1 |
| 44 | Volkswagen Golf GTI | 46 | −1 | −1 | −1 → 0 | 0 | +1 | 0 | −2 → −1 |
| 45 | Tesla Model 3 | 55 | −2 | 0 | −2 → −1 | −2 → 0 | +2 | +2 → +1 | −4 → −1 |
| 46 | Mazda CX-5 | 18 | −2 | −1 | +1 | +2 → 0 | +2 → +1 | 0 | +2 → −1 |
| 47 | BMW X1 | 42 | −2 | −1 | 0 → +1 | +2 → 0 | 0 → +1 | 0 | −1 |
| 48 | Hyundai Palisade | 26 | −2 | −2 | +2 → +1 | +1 | +2 → +1 | 0 | +1 → −1 |
| 49 | Genesis GV70 | 44 | −2 | −2 | +1 | +2 → +1 | 0 → +1 | 0 | −1 |
| 50 | Chevrolet Equinox EV | 57 | 0 | −1 | −1 → 0 | −2 → 0 | −2 → −1 | +2 → +1 | −6 → −2 |
| 51 | Kia Seltos | 56 | −1 | −2 | 0 → +1 | −2 → −1 | 0 → +1 | 0 | −5 → −2 |
| 52 | Mazda3 Hatchback | 54 | −1 | −2 | −2 → 0 | +1 → 0 | 0 → +1 | 0 | −4 → −2 |
| 53 | Honda Odyssey | 48 | −2 | −2 | +2 → +1 | +2 → +1 | −2 → 0 | 0 | −2 |
| 54 | Honda Pilot | 43 | −2 | −2 | +2 → +1 | +1 → 0 | 0 → +1 | 0 | −1 → −2 |
| 55 | Mazda CX-30 | 51 | −2 | −2 | −1 → 0 | +2 → 0 | 0 → +1 | 0 | −3 |
| 56 | Hyundai Santa Cruz | 37 | −2 | −2 | +2 → +1 | 0 → −1 | +2 → +1 | 0 | 0 → −3 |
| 57 | Acura RDX | 52 | −2 | −2 | +1 | +2 → 0 | −2 → 0 | 0 | −3 |

## Comfort inputs and per-car research decisions

Vectors show `[Ride/noise, Seating, Controls, Power liftgate]`, each 0–5, before and after. These are qualitative editorial judgments, not published test scores. The linked source is model-level context; the selected trim remains the configuration in `data.json`.

| Vehicle / selected build | Inputs before → after | Review decision and source |
| --- | --- | --- |
| Lexus NX 350h · 2026 Standard FWD | [3, 4, 4, 5] → [3, 3, 2, 5] | Some tire hum remains despite low wind noise. Ordinary seat baseline; tested F Sport seats are not this Standard grade. Multifunction steering buttons and shifter caused usability problems. [Review](https://www.edmunds.com/lexus/nx/2026/). |
| Lexus UX 300h · 2026 Base FWD | [3, 4, 4, 0] → [2, 2, 3, 0] | Engine noise under acceleration interrupts refinement. Restricted adult rear accommodation offsets praised upgraded front seats. Retain the workable controls baseline; no measured advantage established. [Review](https://www.edmunds.com/lexus/ux/2026/). |
| Mazda CX-50 Hybrid · 2026 Preferred eAWD | [3, 3, 4, 5] → [3, 3, 3, 5] | Firm ride trades against reasonable highway noise isolation. Comfortable fronts but a flatter rear bench; no premium-seat credit. Physical climate controls help, but rotary menus and screen reach are drawbacks. [Review](https://www.edmunds.com/mazda/cx-50/2026/hybrid/). |
| Toyota RAV4 Hybrid · 2026 LE FWD | [3, 3, 3, 0] → [3, 2, 4, 0] | No comparable selected-wheel ride/noise advantage established. Review reports firm padding becoming tiring on longer drives. Large, reachable controls mix physical and digital functions effectively. [Review](https://www.edmunds.com/toyota/rav4/2026/). |
| Mazda CX-30 · 2026 2.5 Turbo Premium Plus AWD | [3, 4, 4, 5] → [4, 2, 3, 5] | Review praises bump absorption and a quiet highway cabin. Rear seats and low roof constrain an adult passenger. Retain baseline rather than treating a rotary controller as universally superior. [Review](https://www.edmunds.com/mazda/cx-30/2026/). |
| Kia Sportage Hybrid · 2026 LX FWD | [3, 3, 3, 0] → [4, 3, 3, 0] | Review reports a compliant ride and mild highway noise. Roomy second row; upper-grade tested seat equipment is not credited to LX. LX controls differ from navigation-equipped review cars; retain baseline. [Review](https://www.edmunds.com/kia/sportage-hybrid/2026/). |
| Mazda CX-5 · 2026 2.5 S Premium Plus AWD | [3, 4, 3, 5] → [4, 3, 2, 5] | Review finds the redesigned cabin quiet at highway speeds. Roomy rear accommodation; seat cushioning could improve on long drives. Touchscreen climate functions and unreliable touch-sensitive steering buttons distract. [Review](https://www.edmunds.com/mazda/cx-5/2026/). |
| Hyundai IONIQ 5 · 2026 SE Standard Range RWD | [3, 3, 3, 0] → [3, 3, 3, 0] | Positive XRT test is context; different tires prevent a selected-build upgrade. No upgraded tested-seat benefit is borrowed by SE Standard Range. Retain workable baseline for selected controls. [Review](https://www.edmunds.com/hyundai/ioniq-5/2026/). |
| Ford Mustang Mach-E · 2026 Select RWD Standard Range | [3, 3, 3, 0] → [3, 3, 3, 0] | Quiet highway cabin does not by itself establish combined ride superiority. Front adjustability has limits; adult rear space is useful. Climate controls are reported easy to use; retain combined baseline. [Review](https://www.edmunds.com/ford/mustang-mach-e/2026/). |
| Honda CR-V Hybrid · 2026 Sport FWD | [3, 3, 4, 0] → [4, 4, 4, 0] | Review identifies ride quality as a particular strength. Comfortable front seating and generous rear legroom support three adults. Reachable physical climate controls are praised for use without looking. [Review](https://www.edmunds.com/honda/cr-v/2026/hybrid/). |
| Subaru Forester Hybrid · 2026 Premium Hybrid AWD | [3, 3, 3, 5] → [4, 4, 3, 5] | Hybrid review finds improved noise/vibration and acceptable road noise. Well-padded fronts, generous headroom and easy entry support adults. Readable screen and simple switches coexist with digital climate controls. [Review](https://www.edmunds.com/subaru/forester/2026/hybrid/). |
| Nissan Rogue · 2026 2026.5 SV FWD | [3, 3, 4, 5] → [2, 3, 4, 5] | Review reports noticeable traffic and road noise at speed. Soft seats help long drives; rear legroom and headrests impose caveats. Simple physical climate controls avoid excessive screen dependence. [Review](https://www.edmunds.com/nissan/rogue/2026/). |
| Nissan LEAF · 2026 S+ FWD, 18-inch steel wheels | [3, 3, 3, 0] → [2, 3, 3, 0] | Review reports prominent wind noise. Supportive fronts and adequate legroom; small rear openings impose limits. Mostly simple controls; window and single-zone climate limitations remain. [Review](https://www.edmunds.com/nissan/leaf/2026/). |
| Hyundai Tucson Hybrid · 2026 SE FWD | [3, 3, 3, 0] → [4, 3, 3, 0] | Review reports limited exterior noise apart from some wind noise. Limited test seats are not borrowed by the entry SE. Retain selected-grade controls baseline. [Review](https://www.edmunds.com/hyundai/tucson/2026/hybrid/). |
| Subaru Solterra · 2026 Premium AWD, 18-inch wheels | [3, 3, 3, 5] → [3, 2, 2, 5] | Quiet cabin is balanced against firm-ride observations in other reviews. Review identifies insufficient front cushioning and thigh support for longer drives. Steering-wheel obstruction and a cluttered instrument display impair usability. [Review](https://www.edmunds.com/subaru/solterra/2026/). |
| Toyota bZ · 2026 XLE FWD, 57.7-kWh battery | [3, 3, 3, 5] → [3, 2, 2, 5] | No exact small-battery XLE ride/noise comparison established. XLE-family review identifies insufficient front cushioning on long drives. Gauge display placement requires an awkward wheel position for some drivers. [Review](https://www.edmunds.com/toyota/bz/2026/). |
| Tesla Model Y · 2026 Standard RWD, 18-inch wheels + FSD subscription | [3, 3, 2, 5] → [3, 2, 2, 5] | Premium-model refinement is not borrowed by the Standard. Standard-specific seats are less comfortable than Premium; room remains generous. Screen-based seat and air-vent adjustments are reported distracting. [Review](https://www.edmunds.com/tesla/model-y/2026/standard/). |
| Kia EV6 · 2026 Light Standard Range RWD | [3, 3, 3, 0] → [3, 3, 2, 0] | GT-Line test ride is context rather than a Light Standard Range measurement. Do not borrow GT-Line seat equipment; rear entry/headroom remain constraints. Dual-purpose touch panel requires switching between climate and media controls. [Review](https://www.edmunds.com/kia/ev6/2026/). |
| Acura RDX · 2026 Base SH-AWD | [3, 4, 3, 5] → [3, 3, 2, 5] | Do not borrow A-Spec Advance adaptive-damper behavior. Do not borrow the upgraded tested seat adjustment package. Touchpad interface is reported harder to use than a touchscreen. [Review](https://www.edmunds.com/acura/rdx/2026/). |
| BMW X1 · 2026 xDrive28i + Driving Assistance Plus | [3, 4, 3, 5] → [3, 3, 2, 5] | Selected non-M-Sport ride/noise comparison remains incomplete. Do not borrow M Sport seat support; retain ordinary-seat baseline. Screen-based climate adjustment is reported distracting. [Review](https://www.edmunds.com/bmw/x1/2026/). |
| Genesis GV70 · 2026 2.5T AWD Standard | [3, 4, 4, 5] → [4, 3, 3, 5] | Four-cylinder review praises bump absorption; some road/engine noise remains. Do not borrow massaging/ventilated tested seats by Standard. Controls are mostly intuitive but display reach and similar rotary knobs need care. [Review](https://www.edmunds.com/genesis/gv70/2026/). |
| Kia Niro Hybrid · 2026 EX FWD | [3, 3, 4, 0] → [3, 3, 2, 0] | No clear selected-build combined ride/noise advantage established. Useful upright packaging and rear headroom support the baseline. Switchable climate/media panel requires attention away from the road. [Review](https://www.edmunds.com/kia/niro/2026/). |
| Kia Seltos · 2026 SX AWD | [3, 3, 3, 0] → [2, 2, 3, 0] | Review reports considerable road noise. Front thigh support is limited on long drives despite useful rear space. Simple, practical layout retains baseline. [Review](https://www.edmunds.com/kia/seltos/2026/). |
| Volkswagen Tiguan · 2026 S FWD | [3, 3, 3, 0] → [4, 3, 3, 0] | Review praises ride comfort and a quiet cabin. Do not borrow SEL massage/ventilation by the S. Interface is reported straightforward; retain baseline without top-screen credit. [Review](https://www.edmunds.com/volkswagen/tiguan/2026/). |
| Honda Civic Hybrid Hatchback · 2026 Sport Hybrid FWD | [3, 3, 4, 0] → [3, 3, 4, 0] | Balanced but taut ride and some road noise retain baseline. Rear legroom is useful but the sloping roof constrains taller passengers. Physical climate controls and clear menus are praised. [Review](https://www.edmunds.com/honda/civic/2026/hybrid/). |
| Toyota Prius · 2026 LE FWD | [3, 3, 3, 0] → [2, 2, 2, 0] | Review reports excessive tire, wind and acceleration noise. Rear headroom and low entry constrain adult comfort. Instrument cluster is cluttered and obstructed by the steering wheel for many drivers. [Review](https://www.edmunds.com/toyota/prius/2026/). |
| Toyota Prius Plug-in Hybrid · 2026 SE FWD | [3, 3, 3, 0] → [2, 2, 2, 0] | Review reports substantial tire, wind and engine noise. Restricted rear headroom and small door openings constrain adults. Instrument display placement and clutter impair otherwise usable controls. [Review](https://www.edmunds.com/toyota/prius-plug-in-hybrid/2026/). |
| Toyota Corolla Hybrid · 2026 LE FWD | [3, 3, 4, 0] → [2, 3, 3, 0] | Engine noise is intrusive on acceleration or climbs. Supportive seats retain baseline, with restricted rear space. Simple climate controls coexist with fragmented settings menus. [Review](https://www.edmunds.com/toyota/corolla-hybrid/2026/). |
| Toyota Camry Hybrid · 2026 LE FWD | [3, 3, 4, 0] → [4, 4, 4, 0] | Quiet cruising cabin; engine noise under hard acceleration remains a caveat. Supportive seats and useful adult space in both rows support longer trips. Physical switches and knobs make common functions accessible. [Review](https://www.edmunds.com/toyota/camry/2026/). |
| Honda Accord Hybrid · 2026 Sport FWD | [3, 3, 4, 0] → [4, 3, 4, 0] | Review reports effective noise insulation in ordinary driving. Some testers wanted more cushion padding and legroom. Large physical buttons and knobs simplify common tasks. [Review](https://www.edmunds.com/honda/accord/2026/hybrid/). |
| Hyundai Elantra Hybrid · 2026 Limited FWD | [3, 4, 3, 0] → [2, 3, 4, 0] | Review identifies substantial wind/road noise versus class leaders. Supportive Limited fronts balance a flatter, tighter rear seat. Physical buttons, knobs and switches are praised for ease of use. [Review](https://www.edmunds.com/hyundai/elantra-hybrid/2026/). |
| Hyundai Sonata Hybrid · 2026 Blue FWD | [3, 3, 3, 0] → [2, 3, 4, 0] | Review identifies above-average road and wind noise. Firm front padding limits longer-trip comfort; rear space is useful. Center controls are intuitive and easy to reach. [Review](https://www.edmunds.com/hyundai/sonata/2026/hybrid/). |
| Mazda3 Hatchback · 2026 2.5 Turbo Premium Plus AWD | [3, 4, 4, 0] → [4, 2, 4, 0] | Review reports good engine and road-noise isolation. Cramped adult rear accommodation limits the three-adult scenario. Reachable physical climate buttons and major controls are praised. [Review](https://www.edmunds.com/mazda/3/2026/hatchback/). |
| Volkswagen Golf GTI · 2026 S DSG FWD | [3, 4, 3, 0] → [3, 3, 2, 0] | Performance/comfort balance retains baseline; selected-damper superiority unverified. Supportive seats retain baseline without higher-trim equipment credit. Capacitive temperature controls are reported difficult to use while driving. [Review](https://www.edmunds.com/volkswagen/golf-gti/2026/). |
| Subaru Impreza · 2026 Sport AWD | [3, 3, 3, 0] → [4, 3, 3, 0] | Review identifies a comfortable ride; RS test is a model-level proxy. Roomy rear accommodation; selected Sport seat support remains provisional. Large physical switches help, but screen-dependent functions remain. [Review](https://www.edmunds.com/subaru/impreza/2026/). |
| Subaru Crosstrek Hybrid · 2026 Sport Hybrid AWD | [3, 3, 3, 0] → [3, 3, 3, 0] | Smooth operation retains baseline without Wilderness ride/traction credit. Sport-specific seat support remains provisional; useful headroom is documented. Tactile buttons help, but slow screen operation limits an upgrade. [Review](https://www.edmunds.com/subaru/crosstrek/2026/hybrid/). |
| Toyota Corolla Cross Hybrid · 2026 S AWD | [3, 3, 4, 0] → [3, 2, 3, 0] | No selected-wheel combined ride/noise advantage established. Rear legroom is reported among the tightest in its class. Physical climate controls help, but steering-wheel grouping requires learning. [Review](https://www.edmunds.com/toyota/corolla-cross-hybrid/2026/). |
| Honda HR-V · 2026 LX FWD | [3, 3, 4, 0] → [3, 2, 4, 0] | Decent noise isolation retains baseline. Review reports unusually stiff front cushions without adjustable lumbar. Straightforward menus and physical steering/climate controls are praised. [Review](https://www.edmunds.com/honda/hr-v/2026/). |
| Chevrolet Equinox EV · 2026 LT1 FWD | [3, 3, 2, 0] → [4, 2, 4, 0] | Review reports little highway wind or road noise. Flat, firm seats lack support despite plentiful passenger room. Physical climate buttons are praised; phone-platform preference is not a penalty. [Review](https://www.edmunds.com/chevrolet/equinox-ev/2026/). |
| Chevrolet Bolt · 2027 LT FWD | [3, 3, 3, 0] → [3, 2, 3, 0] | New 2027 model retains baseline; old Bolt ride evidence is not substituted. New-model review reports flat, unsupportive front and rear seats. Physical climate controls help; headlights and other functions use the screen. [Review](https://www.edmunds.com/chevrolet/bolt/2027/). |
| Tesla Model 3 · 2026 Standard RWD + FSD subscription | [3, 3, 2, 0] → [3, 3, 2, 0] | Do not borrow Premium refinement by the Standard. Standard-specific support is acceptable but rear seats are low. Restored turn-signal stalk helps, but screen-based vents/climate remain distracting. [Review](https://www.edmunds.com/tesla/model-3/2026/standard/). |
| Hyundai Tucson Plug-in Hybrid · 2026 SEL AWD | [3, 3, 3, 5] → [3, 4, 3, 5] | Selected-wheel ride/noise comparison remains incomplete. Supportive fronts and reclining rear seats with long cushions support adults. Restored climate knobs help, but touch functions remain complicated. [Review](https://www.edmunds.com/hyundai/tucson-plug-in-hybrid/2026/). |
| Kia Sportage Plug-in Hybrid · 2026 X-Line AWD | [3, 3, 3, 5] → [3, 3, 3, 5] | Accessible review excerpt does not establish selected-build ride/noise superiority. Retain ordinary seating baseline; do not borrow Prestige equipment. Retain baseline for X-Line controls rather than borrowing a higher-grade interface. [Review](https://www.consumerreports.org/cars/kia/sportage-plug-in-hybrid/2026/road-test-report/). |
| Toyota RAV4 Plug-in Hybrid · 2026 SE AWD | [3, 3, 3, 5] → [3, 2, 4, 5] | No selected SE wheel/ride-noise comparison established. Review reports firm padding tiring on longer drives. Large, reachable physical/digital controls are praised. [Review](https://www.edmunds.com/toyota/rav4-plug-in-hybrid/2026/). |
| Kia K4 Hatchback · 2026 EX FWD | [3, 3, 3, 0] → [3, 4, 3, 0] | Firm ride balances comfortable seats; no noise advantage established. Roomy adult rear seat and supportive padding are praised. Physical controls help, but steering-wheel obstruction affects the climate display. [Review](https://www.edmunds.com/kia/k4/2026/hatchback/). |
| Toyota Sienna · 2026 LE FWD | [3, 3, 3, 5] → [2, 3, 3, 5] | Review reports pronounced engine/CVT drone under power. Do not borrow optional ottomans or luxury seating by LE. Retain baseline for LE rather than borrowing higher-grade convenience equipment. [Review](https://www.edmunds.com/toyota/sienna/2026/). |
| Honda Odyssey · 2026 EX-L FWD | [3, 4, 4, 5] → [4, 4, 3, 5] | Review reports unobtrusive wind and road noise. Comfortable front and second-row seats support three adults. No measured selected-grade control advantage established; retain baseline. [Review](https://www.edmunds.com/honda/odyssey/2026/). |
| Kia Carnival Hybrid · 2026 LXS FWD | [3, 3, 3, 0] → [3, 3, 2, 0] | Selected LXS ride/noise comparison remains incomplete. Useful front comfort; do not borrow optional lounge seats. Touch-sensitive climate controls are reported cumbersome while moving. [Review](https://www.edmunds.com/kia/carnival-hybrid/2026/). |
| Ford Maverick Hybrid · 2026 Lariat AWD | [3, 4, 4, 0] → [3, 3, 3, 0] | Quiet cruising balances engine coarseness under load. Firm support balances limited rear legroom and seat/steering adjustment. Simple controls retain baseline; no premium-brand or equipment bonus. [Review](https://www.edmunds.com/ford/maverick/2026/hybrid/). |
| Hyundai Santa Cruz · 2026 XRT AWD | [3, 3, 4, 0] → [3, 2, 3, 0] | Smooth ride balances noticeable wind and road noise. Upright, cramped rear seating constrains the third adult. Review control description may predate the refresh; retain current-build baseline. [Review](https://www.edmunds.com/hyundai/santa-cruz/2026/). |
| Subaru Outback · 2026 Premium AWD | [3, 3, 4, 5] → [4, 4, 4, 5] | Review praises ride over rough urban surfaces; Touring XT is a proxy. Supportive seats, generous space and easy entry support adults. Restored physical climate buttons and knobs materially improve usability. [Review](https://www.edmunds.com/subaru/outback/2026/). |
| Toyota Crown Signia · 2026 XLE AWD | [3, 4, 4, 5] → [3, 4, 4, 5] | Highway road noise and hybrid noise limit a refinement upgrade. Cushioned, supportive fronts and usable adult rear room are documented. Simple radio and climate controls are reported easy to reach. [Review](https://www.edmunds.com/toyota/crown-signia/2026/). |
| Hyundai Santa Fe Hybrid · 2026 SE FWD | [3, 3, 3, 5] → [4, 3, 4, 5] | Review reports a quiet cabin with little wind noise. Retain SE seat baseline; do not borrow tested upgraded upholstery/support. Dedicated climate interface and physical controls are praised. [Review](https://www.edmunds.com/hyundai/santa-fe/2026/hybrid/). |
| Kia Sorento Hybrid · 2026 EX FWD | [3, 4, 3, 5] → [4, 3, 3, 5] | Review reports useful noise insulation and controlled bump response. EX bench differs from tested upper-grade captain chairs; retain baseline. Retain baseline without an unverified selected-grade control advantage. [Review](https://www.edmunds.com/kia/sorento-hybrid/2026/). |
| Toyota Highlander Hybrid · 2026 XLE AWD | [3, 4, 4, 5] → [2, 4, 3, 5] | Review reports substantial highway road noise and coarse full-throttle engine sound. Comfortable first two rows suit three adults; third row remains restricted. Intuitive controls balance limited steering adjustment and awkward armrests. [Review](https://www.edmunds.com/toyota/highlander-hybrid/2026/). |
| Honda Pilot · 2026 Sport FWD | [3, 3, 4, 5] → [3, 3, 4, 5] | Generally low noise is balanced against quieter competitors. Soft, supportive seats have limited adjustability; retain Sport baseline. Physical controls keep common tasks accessible outside the screen. [Review](https://www.edmunds.com/honda/pilot/2026/). |
| Hyundai Palisade · 2026 SE FWD | [3, 3, 3, 5] → [4, 3, 4, 5] | Review reports a very quiet highway cabin. Do not borrow powered third-row or higher-grade seats by SE. Mixed physical knobs and digital controls are reported intuitive. [Review](https://www.edmunds.com/hyundai/palisade/2026/). |

## Sensitivity, not confidence weighting

The following scenarios retain the other categories at 1× and leave Upkeep off. They are checks of the ranking's dependence on assumptions, not alternative recommendations or hidden penalties. In the comfort-baseline scenario every vehicle's first three comfort components are set to 3/5 while keeping its selected gate.

| Scenario | First three cars | Solterra rank / total |
| --- | --- | --- |
| Default | Toyota Camry Hybrid, Honda CR-V Hybrid, Subaru Forester Hybrid | 21 / +3 |
| Eco off | Subaru Forester Hybrid, Toyota Camry Hybrid, Kia Sportage Hybrid | 37 / +1 |
| Comfort off | Toyota Prius, Toyota Camry Hybrid, Toyota Corolla Cross Hybrid | 22 / +3 |
| All comfort review estimates set to baseline | Toyota Prius, Toyota Camry Hybrid, Toyota Corolla Cross Hybrid | 22 / +3 |

## Sorting behavior and validation

All nine columns (#, Vehicle, Total and six categories) have keyboard-accessible buttons on desktop and mobile. Numeric score columns first sort descending; Vehicle and # first sort ascending. Repeating the active column reverses direction. Category sorting uses the displayed, unweighted category score; ties use weighted total descending, lower estimated five-year cost, then name. Weighted rank numbers, leader, details and Pareto calculations are independent of display sort. Slider changes retain the chosen column; Reset restores default weights and Total descending. JavaScript-free fallback remains default Total descending with working detail links.

Validation covers fixed-band boundaries, cohort independence, all-car evidence coverage, stored EPA energy consistency, selected-assistance corrections, sorting in both directions, ties, default/reset behavior, live weight changes, mobile headers, keyboard interaction, offline behavior and shared Pareto/detail scores. The verification results are reported with the code change; none of these checks validate unknown future resale, personal seat fit or loaded winter performance.
