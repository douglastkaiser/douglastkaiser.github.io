# November 17 lineup and Sporty/Fun audit

Checked 2026-11-17. Current cohort: **63 ranked configurations from 80 screened candidates**. This audit supersedes the maintenance-based score snapshots in earlier audits. `data.json` contains research inputs; `index.html` is generated.

## What changed

The optional sixth category is now Sporty/Fun (`sporty`, default 0). Five other priorities retain default weight 1. Upkeep and the repair reserve already existed in five-year Cost and remain counted exactly once. Every one of the original 57 complete dollar cost breakdowns was compared with the previous generator and is unchanged. Service caveats moved into Cost details; no former maintenance score is converted to dollars.

Fun uses fixed editorial ratings 1–5 minus three: +2 exceptional engagement, +1 clearly engaging, 0 ordinary/uncertain, −1 detached/cumbersome, −2 strongly utility-focused. GR86 manual and minivans are the user-provided +2/−2 anchors. Steering, chassis, agility and involvement lead; straight-line acceleration, manual transmission, badge and off-road ability alone do not earn +2. Evidence confidence does not add a bonus or penalty.

## Added configurations

| Configuration | MSRP | Destination | Est. OTD | Five-year cost | Cost / Eco / Trips / Comfort / Assist / Fun |
|---|---:|---:|---:|---:|---|
| Hyundai IONIQ 5 SEL AWD — 2026 SEL AWD, 19-inch wheels | $43,300 | $1,600 | $49,101.19 | $56,099.74 | −2 / +1 / 0 / 0 / +2 / 0 |
| Honda Civic Si Manual — 2026 Si 6MT FWD | $31,495 | $1,295 | $35,907.95 | $49,346.28 | 0 / −1 / 0 / 0 / 0 / +2 |
| Volkswagen ID.4 AWD — 2026 AWD Pro, 19-inch wheels | $48,995 | $1,475 | $55,139.07 | $60,196.77 | −2 / 0 / 0 / 0 / +1 / 0 |
| Toyota Tacoma — 2026 SR5 Double Cab 4WD 8AT, 5-ft bed | $40,905 | $1,745 | $46,742.18 | $59,453.85 | −2 / −2 / +1 / −1 / +1 / −1 |
| Mazda MX-5 Miata Manual — 2026 Sport soft top 6MT RWD | $30,730 | $1,315 | $35,100.37 | $49,745.81 | 0 / −2 / −1 / −1 / −2 / +2 |
| Toyota GR86 Manual — 2026 Base 6MT RWD | $31,400 | $1,295 | $35,804.97 | $53,971.30 | −1 / −2 / −1 / −1 / −1 / +2 |

All prices use published MSRP and destination with no assumed discount or conditional rebate. All selected builds meet the existing $60k OTD limit. The existing IONIQ 5 SE Standard Range RWD remains alongside SEL AWD.

Tacoma is SR5 Double Cab, 5-ft bed, 4WD, 8AT; EPA #50090 matches its 19/24/21 MPG and 2-mode Power/Normal transmission variant. A $80 annual pickup-weight allowance is charged in the initial registration and four renewals; exact registered unladen weight remains a dealer/DMV check. Open-bed gear needs securing and weather protection, and rear adult comfort is limited.

GR86 uses current Toyota MSRP $31,400 and current $1,295 car delivery reference; older articles quote lower amounts. No 2026 GR86 model was returned by the EPA API, so the selected 22-MPG manual manufacturer/specification reference is explicitly marked as a fallback. No automatic-transmission fuel economy or continuous lane centering is borrowed. Civic Si gets manual-specific ACC/LKAS without low-speed-follow or Traffic Jam Assist. Miata Sport gets no adaptive-cruise, lane-centering, Club suspension or Club differential credit.

The mountain assessment retains three adults plus long gear. Miata has only two seats and cannot meet this passenger requirement. GR86 rear seats and the fully folding rear seatback severely constrain the scenario. Low trip composites do not certify passenger/gear feasibility; the per-car explanations state these limitations explicitly.

### Ariya: screened, not ranked

Nissan’s [US discontinuation notice](https://www.nissanusa.com/vehicles/discontinued/ariya.html) identifies 2025 as the final US model year. The California Engage e-4ORCE VIN lead JN8CF0BF6SM761659 redirected to general inventory on recheck; other leads were demo-site duplicates or used stock. No current new California build/quote was established. It remains a screened candidate, without an invented 2026 US build or a ranked stock claim. A current dealer listing/quote can establish eligibility later.

### Lifecycle and review limitations

ID.4 AWD Pro, IONIQ 5 long-range AWD, GR86 manual, Civic Si manual and Tacoma use explicitly transcribed 2024 same-family lifecycle anchors as proxies, without numerical adjustments. Battery, certification, model year and trim differences remain limitations. No same-model MX-5 record was located in the checked table: its clearly labeled low-confidence cross-model proxy is the GR86 manual anchor (43/100). This proxy does not reproduce measured Miata lifecycle performance and can materially affect its relative Eco band; its actual EPA 29 MPG is used separately for Cost.

Model-level review evidence may concern another trim, tire or year. Comfort/Fun assessments are editorial transfer judgments, not reproduced publisher ratings. IONIQ 5 SEL retains baseline ride/seating/ergonomics where XRT evidence does not transfer; no N performance credit. Upgraded driver-assistance tasks follow selected SEL HDA2 equipment only. No new EV trip-practicality upgrade is made without loaded winter range, reserve and charging-stop evidence.

## Cohort-driven changes for existing cars

Cost and Eco use full-cohort midpoint percentile bands. Their underlying values did not change for existing cars. Trips, Comfort and Assist also remain unchanged for every existing configuration. Fun is fixed, so adding/removing other cars cannot change it.

| Existing configuration | Cost before → after | Eco before → after | Default total before → after |
|---|---|---|---|
| Honda Civic Hybrid Hatchback | +2 → +2 | +1 → +2 | +4 → +5 |
| Toyota RAV4 Hybrid | +2 → +2 | 0 → +1 | +4 → +5 |
| Toyota RAV4 Plug-in Hybrid | 0 → +1 | +2 → +2 | +4 → +5 |
| Hyundai Elantra Hybrid | +2 → +2 | +1 → +2 | +3 → +4 |
| Kia Niro Hybrid | +1 → +2 | +1 → +1 | +3 → +4 |
| Toyota Corolla Hybrid | +2 → +2 | +1 → +2 | +2 → +3 |
| Hyundai Tucson Hybrid | +1 → +2 | −1 → −1 | +2 → +3 |
| Hyundai Santa Fe Hybrid | 0 → +1 | −1 → −1 | +2 → +3 |
| Hyundai IONIQ 5 | 0 → 0 | +1 → +2 | +2 → +3 |
| Toyota Crown Signia | −1 → −1 | 0 → +1 | +2 → +3 |
| Lexus NX 350h | −1 → 0 | 0 → +1 | 0 → +2 |
| Kia Carnival Hybrid | −1 → −1 | −1 → 0 | 0 → +1 |
| Tesla Model Y | −2 → −2 | 0 → +1 | 0 → +1 |
| Volkswagen Tiguan | −1 → 0 | −2 → −2 | −1 → 0 |
| Mazda CX-30 | −2 → −1 | −2 → −2 | −3 → −2 |

## Fun evidence for every configuration

Each source is model-level context; exact-trim applicability is qualified in the rationale. Ordinary/uncertain baselines do not assert measured poor handling.

| Configuration | Fun | Editorial rationale | Review context |
|---|---:|---|---|
| Acura RDX — Base SH-AWD | +1 | Responsive steering and the selected turbo powertrain support an engaging road-driving estimate. | [Edmunds 2026 Acura RDX review](https://www.edmunds.com/acura/rdx/2026/) |
| BMW X1 — xDrive28i + Driving Assistance Plus | +1 | Responsive cornering and compact proportions support an engaging crossover estimate; do not borrow M35i suspension or performance. | [Edmunds 2026 BMW X1 review](https://www.edmunds.com/bmw/x1/2026/) |
| Chevrolet Bolt — LT FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2027 Chevrolet Bolt review](https://www.edmunds.com/chevrolet/bolt/2027/) |
| Chevrolet Equinox EV — LT1 FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Chevrolet Equinox EV review](https://www.edmunds.com/chevrolet/equinox-ev/2026/) |
| Ford Maverick Hybrid — Lariat AWD | −1 | Selected hybrid pickup prioritizes cargo utility; no sport suspension or road-driving evidence supports a positive band. | [Edmunds 2026 Ford Maverick Hybrid review](https://www.edmunds.com/ford/maverick/2026/hybrid/) |
| Ford Mustang Mach-E — Select RWD Standard Range | +1 | Responsive chassis and steering support engagement; no GT or performance-package equipment is credited. | [Edmunds 2026 Ford Mustang Mach-E review](https://www.edmunds.com/ford/mustang-mach-e/2026/) |
| Genesis GV70 — 2.5T AWD Standard | +1 | Balanced chassis responses support engagement; no Sport Prestige suspension or higher-power engine is assumed. | [Edmunds 2026 Genesis GV70 review](https://www.edmunds.com/genesis/gv70/2026/) |
| Honda Accord Hybrid — Sport FWD | +1 | Balanced handling and responsive hybrid power delivery support an engaging sedan estimate; it is not assessed as a sports car. | [Edmunds 2026 Honda Accord Hybrid review](https://www.edmunds.com/honda/accord/2026/hybrid/) |
| Honda Civic Hybrid Hatchback — Sport Hybrid FWD | +1 | Responsive hatchback handling and the hybrid powertrain support everyday engagement; no Si chassis or manual transmission is borrowed. | [Edmunds 2026 Honda Civic Hybrid Hatchback review](https://www.edmunds.com/honda/civic/2026/hybrid/) |
| Honda Civic Si Manual — Si 6MT FWD | +2 | Nimble chassis, responsive steering, limited-slip differential and slick six-speed manual support +2 driver engagement despite modest acceleration. | [Road-test context: civicsi](https://www.edmunds.com/honda/civic/2026/si/) |
| Honda CR-V Hybrid — Sport FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Honda CR-V Hybrid review](https://www.edmunds.com/honda/cr-v/2026/hybrid/) |
| Honda HR-V — LX FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Honda HR-V review](https://www.edmunds.com/honda/hr-v/2026/) |
| Honda Odyssey — EX-L FWD | −2 | Minivan utility anchor: passenger and cargo priorities, size and comfort-oriented responses place this configuration at −2 for sporty driving. This does not reduce its carrying or comfort assessment. | [Edmunds 2026 Honda Odyssey review](https://www.edmunds.com/honda/odyssey/2026/) |
| Honda Pilot — Sport FWD | −1 | Large family SUV proportions prioritize carrying over agility; no TrailSport capability is counted as road-driving fun. | [Edmunds 2026 Honda Pilot review](https://www.edmunds.com/honda/pilot/2026/) |
| Hyundai Elantra Hybrid — Limited FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Hyundai Elantra Hybrid review](https://www.edmunds.com/hyundai/elantra-hybrid/2026/) |
| Hyundai IONIQ 5 — SE Standard Range RWD | 0 | Roomy comfort-oriented SE Standard Range RWD; do not borrow the N chassis or dual-motor acceleration. | [Edmunds 2026 Hyundai IONIQ 5 review](https://www.edmunds.com/hyundai/ioniq-5/2026/) |
| Hyundai IONIQ 5 SEL AWD — SEL AWD, 19-inch wheels | 0 | Dual-motor response alone does not establish sporty feedback; retain neutral engagement for the comfort-oriented SEL, without borrowing IONIQ 5 N chassis hardware. | [Edmunds 2026 Hyundai IONIQ 5 review](https://www.edmunds.com/hyundai/ioniq-5/2026/) |
| Hyundai Palisade — SE FWD | −1 | Large comfort-oriented three-row configuration prioritizes passenger utility over road feedback. | [Edmunds 2026 Hyundai Palisade review](https://www.edmunds.com/hyundai/palisade/2026/) |
| Hyundai Santa Cruz — XRT AWD | 0 | Compact pickup can feel carlike, but selected XRT off-road hardware and turbo speed alone do not establish a positive engagement band. | [Edmunds 2026 Hyundai Santa Cruz review](https://www.edmunds.com/hyundai/santa-cruz/2026/) |
| Hyundai Santa Fe Hybrid — SE FWD | −1 | Tall three-row family packaging prioritizes utility over agile road-driving responses. | [Edmunds 2026 Hyundai Santa Fe Hybrid review](https://www.edmunds.com/hyundai/santa-fe/2026/hybrid/) |
| Hyundai Sonata Hybrid — Blue FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Hyundai Sonata Hybrid review](https://www.edmunds.com/hyundai/sonata/2026/hybrid/) |
| Hyundai Tucson Hybrid — SE FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Hyundai Tucson Hybrid review](https://www.edmunds.com/hyundai/tucson/2026/hybrid/) |
| Hyundai Tucson Plug-in Hybrid — SEL AWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Hyundai Tucson Plug-in Hybrid review](https://www.edmunds.com/hyundai/tucson-plug-in-hybrid/2026/) |
| Kia Carnival Hybrid — LXS FWD | −2 | Minivan utility anchor: passenger and cargo priorities, size and comfort-oriented responses place this configuration at −2 for sporty driving. This does not reduce its carrying or comfort assessment. | [Edmunds 2026 Kia Carnival Hybrid review](https://www.edmunds.com/kia/carnival-hybrid/2026/) |
| Kia EV6 — Light Standard Range RWD | +1 | Composed cornering and responsive power delivery support engagement; no GT equipment or AWD performance is borrowed. | [Edmunds 2026 Kia EV6 review](https://www.edmunds.com/kia/ev6/2026/) |
| Kia K4 Hatchback — EX FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Kia K4 Hatchback review](https://www.edmunds.com/kia/k4/2026/hatchback/) |
| Kia Niro Hybrid — EX FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Kia Niro Hybrid review](https://www.edmunds.com/kia/niro/2026/) |
| Kia Seltos — SX AWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Kia Seltos review](https://www.edmunds.com/kia/seltos/2026/) |
| Kia Sorento Hybrid — EX FWD | −1 | Three-row utility-oriented hybrid configuration emphasizes family transport over driver involvement. | [Edmunds 2026 Kia Sorento Hybrid review](https://www.edmunds.com/kia/sorento-hybrid/2026/) |
| Kia Sportage Hybrid — LX FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Kia Sportage Hybrid review](https://www.edmunds.com/kia/sportage-hybrid/2026/) |
| Kia Sportage Plug-in Hybrid — X-Line AWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Consumer Reports 2026 Kia Sportage Plug-in Hybrid review](https://www.consumerreports.org/cars/kia/sportage-plug-in-hybrid/2026/road-test-report/) |
| Lexus NX 350h — Standard FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Lexus NX 350h review](https://www.edmunds.com/lexus/nx/2026/) |
| Lexus UX 300h — Base FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Lexus UX 300h review](https://www.edmunds.com/lexus/ux/2026/) |
| Mazda CX-30 — 2.5 Turbo Premium Plus AWD | +1 | Responsive steering and compact proportions support involvement; turbo acceleration alone is not the reason for the positive rating. | [Edmunds 2026 Mazda CX-30 review](https://www.edmunds.com/mazda/cx-30/2026/) |
| Mazda CX-5 — 2.5 S Premium Plus AWD | 0 | Redesigned selected build lacks a sufficiently transferable engagement comparison; retain neutral rather than borrowing predecessor handling praise. | [Edmunds 2026 Mazda CX-5 review](https://www.edmunds.com/mazda/cx-5/2026/) |
| Mazda CX-50 Hybrid — Preferred eAWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Mazda CX-50 Hybrid review](https://www.edmunds.com/mazda/cx-50/2026/hybrid/) |
| Mazda MX-5 Miata Manual — Sport soft top 6MT RWD | +2 | Light rear-drive roadster, precise steering and direct manual interaction support +2; Sport does not borrow Club limited-slip differential or Bilstein equipment. | [Road-test context: miata](https://www.edmunds.com/mazda/mx-5-miata/2026/) |
| Mazda3 Hatchback — 2.5 Turbo Premium Plus AWD | +1 | Responsive steering and a compact chassis support engagement; the selected turbo automatic is not a manual hot hatch. | [Edmunds 2026 Mazda3 Hatchback review](https://www.edmunds.com/mazda/3/2026/hatchback/) |
| Nissan LEAF — S+ FWD, 18-inch steel wheels | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Nissan LEAF review](https://www.edmunds.com/nissan/leaf/2026/) |
| Nissan Rogue — 2026.5 SV FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Nissan Rogue review](https://www.edmunds.com/nissan/rogue/2026/) |
| Subaru Crosstrek Hybrid — Sport Hybrid AWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Subaru Crosstrek Hybrid review](https://www.edmunds.com/subaru/crosstrek/2026/hybrid/) |
| Subaru Forester Hybrid — Premium Hybrid AWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Subaru Forester Hybrid review](https://www.edmunds.com/subaru/forester/2026/hybrid/) |
| Subaru Impreza — Sport AWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Subaru Impreza review](https://www.edmunds.com/subaru/impreza/2026/) |
| Subaru Outback — Premium AWD | −1 | Tall utility-oriented packaging and body motions constrain paved-road engagement; winter access is scored separately. | [Edmunds 2026 Subaru Outback review](https://www.edmunds.com/subaru/outback/2026/) |
| Subaru Solterra — Premium AWD, 18-inch wheels | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Subaru Solterra review](https://www.edmunds.com/subaru/solterra/2026/) |
| Tesla Model 3 — Standard RWD + FSD subscription | +1 | Low sedan proportions and responsive handling support engagement; FSD is unrelated to Fun and acceleration alone earns no extra tier. | [Edmunds 2026 Tesla Model 3 review](https://www.edmunds.com/tesla/model-3/2026/standard/) |
| Tesla Model Y — Standard RWD, 18-inch wheels + FSD subscription | 0 | Selected Standard RWD evidence does not establish exceptional feedback or agility; no Performance chassis is borrowed. | [Edmunds 2026 Tesla Model Y review](https://www.edmunds.com/tesla/model-y/2026/standard/) |
| Toyota bZ — XLE FWD, 57.7-kWh battery | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Toyota bZ review](https://www.edmunds.com/toyota/bz/2026/) |
| Toyota Camry Hybrid — LE FWD | 0 | Efficient everyday hybrid sedan; current evidence does not establish sports-car feedback for the selected entry configuration. | [Edmunds 2026 Toyota Camry Hybrid review](https://www.edmunds.com/toyota/camry/2026/) |
| Toyota Corolla Cross Hybrid — S AWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Toyota Corolla Cross Hybrid review](https://www.edmunds.com/toyota/corolla-cross-hybrid/2026/) |
| Toyota Corolla Hybrid — LE FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Toyota Corolla Hybrid review](https://www.edmunds.com/toyota/corolla-hybrid/2026/) |
| Toyota Crown Signia — XLE AWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Toyota Crown Signia review](https://www.edmunds.com/toyota/crown-signia/2026/) |
| Toyota GR86 Manual — Base 6MT RWD | +2 | Light rear-drive coupe with precise steering, balanced handling and a direct six-speed manual: the user’s +2 engagement anchor. No Premium tires, Brembo brakes or SACHS dampers assumed. | [Road-test context: gr86](https://www.edmunds.com/toyota/gr86/2026/) |
| Toyota Highlander Hybrid — XLE AWD | −1 | Three-row family packaging and comfort-oriented responses constrain agility and feedback. | [Edmunds 2026 Toyota Highlander Hybrid review](https://www.edmunds.com/toyota/highlander-hybrid/2026/) |
| Toyota Prius — LE FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Toyota Prius review](https://www.edmunds.com/toyota/prius/2026/) |
| Toyota Prius Plug-in Hybrid — SE FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Toyota Prius Plug-in Hybrid review](https://www.edmunds.com/toyota/prius-plug-in-hybrid/2026/) |
| Toyota RAV4 Hybrid — LE FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Toyota RAV4 Hybrid review](https://www.edmunds.com/toyota/rav4/2026/) |
| Toyota RAV4 Plug-in Hybrid — SE AWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Toyota RAV4 Plug-in Hybrid review](https://www.edmunds.com/toyota/rav4-plug-in-hybrid/2026/) |
| Toyota Sienna — LE FWD | −2 | Minivan utility anchor: passenger and cargo priorities, size and comfort-oriented responses place this configuration at −2 for sporty driving. This does not reduce its carrying or comfort assessment. | [Edmunds 2026 Toyota Sienna review](https://www.edmunds.com/toyota/sienna/2026/) |
| Toyota Tacoma — SR5 Double Cab 4WD 8AT, 5-ft bed | −1 | Road-driving agility and feedback are constrained by midsize-truck proportions and utility suspension. Off-road access is valuable but is assessed under Trips, not road-driving Fun. | [Road-test context: tacoma](https://www.edmunds.com/toyota/tacoma/2026/) |
| Volkswagen Golf GTI — S DSG FWD | +2 | Sport-tuned hatchback chassis and responsive DSG powertrain support exceptional engagement without requiring a manual. | [Edmunds 2026 Volkswagen Golf GTI review](https://www.edmunds.com/volkswagen/golf-gti/2026/) |
| Volkswagen ID.4 AWD — AWD Pro, 19-inch wheels | 0 | Comfort-oriented crossover handling; dual-motor acceleration does not establish exceptional feedback. Retain ordinary engagement. | [Road-test context: id4](https://www.edmunds.com/volkswagen/id4/2026/) |
| Volkswagen Tiguan — S FWD | 0 | Selected everyday configuration has no established exceptional steering/chassis engagement in the cited model-level context; retain the ordinary/uncertain baseline. Powertrain type, badge and acceleration alone do not change it. | [Edmunds 2026 Volkswagen Tiguan review](https://www.edmunds.com/volkswagen/tiguan/2026/) |

## Validation

- Python arithmetic, input/evidence contracts, Fun anchors, cohort independence, lineup and generation tests.
- JavaScript allocation, sorting and Pareto tests, including all category activation masks.
- Offline browser tests: sliders, totals, sorting, reset, Pareto, desktop/mobile, dialogs/focus, and no-JavaScript fallback.
- Generator `--check` and `git diff --check`.
- All 57 previous cost breakdowns compared exactly; no original dollar inputs changed.
