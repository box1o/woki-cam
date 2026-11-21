# PCB, connector and major-part cost audit

Checked 2026-11-21. Read-only inspection of the four active PCB files, current stack XML netlists, project rules, model index and manufacturer/distributor documentation. No components, copper or circuit connections were changed by this audit.

## Result

The files are mechanically consistent connector-only templates, not completed electronic PCB layouts. All four have **zero tracks and zero zones**. Board 1 still lacks the 227 other schematic components on the PCB. A working, professional routed board and guaranteed 35 W output cannot be concluded from these files or from a clean geometric DRC.

| Check | Observed result |
|---|---|
| Outline | All four: eight Edge.Cuts primitives, nominal 60 × 60 mm centerline outline; KiCad bounding box includes the 0.1 mm stroke and reports 60.1 mm |
| Board thickness / copper | 1.6 mm, eight copper layers |
| Connector centers | All connectors at (80, 55) mm, orientation 0°, locked; 5 mm below the top outline centerline |
| Mounting holes | Existing four holes at (53,53), (107,53), (53,107), (107,107) mm, locked and retained |
| Stack arrangement | Board 1 female front; boards 2/3 male back + female front; board 4 male back |
| Contacts | Each physical connector has exactly 100 numbered contacts; all live PCB contact net assignments match the current exported schematic XML |
| Models on PCB | One model per connector; no invented model geometry |
| Copper / keepouts | No routing, copper zones or isolation rule areas |

Live evidence is recorded in `audit-pcb-live.json`. Earlier geometric DRC results in `pcb-stack-verification.json` report zero geometric violations but 53/128/128/50 unconnected items, respectively. These counts are expected for the incomplete templates and must not be presented as a fabrication pass.

## DF40 and future interface limits

[Hirose's exact female product page](https://www.hirose.com/en/product/p/CL0684-4151-0-51) confirms 100 contacts, 0.4 mm pitch, **0.3 A/contact**, a **3 mm mating height**, and the intended DF40C-100DP-0.4V(51) male mate. The local `datasheets/df40.pdf` agrees. The previously cited DF40C-100DS page describes a different, 1.5 mm receptacle; it must not be used as the source for this stack height.

Fourteen contacts are allocated to +12V_STACK. At 35 W/12 V the ideal total is 2.92 A, or 0.208 A/contact with perfect sharing. The twelve dedicated adjacent return contacts carry 0.243 A each if they alone return that current; there are additional grounds in the signal region. This is plausible allocation, not a guaranteed aggregate rating. Layout must distribute current across the contacts, include sufficient copper/vias and be checked for temperature rise and connector wear. At 50 W, 4.17 A would nearly consume the ideal 14 × 0.3 A sum, leaving little sharing/temperature margin; do not claim this connector allocation guarantees 50 W.

Male and female lands intentionally have different row center distances. Matching contact numbers have the same X coordinates and occupy the same side of the connector center once the male is on B.Cu; the 0.185 mm land-row difference is not a mating-pin error. Do not move male pads to make their solder lands coincide with the female lands.

I²C/SPI/control reservations may pass through intermediate boards, but require a deliberate master, voltage and pullup/tri-state policy. RGMII/JTAG/UART belong to board 1 ↔ board 2. CSI-2 is a point-to-point reservation for board 2 ↔ board 3, not a multidrop bus; unused stubs must remain absent. A sensor/FPGA choice and actual controlled-impedance routing are still required before claiming MIPI compatibility.

The 3 mm gap is a hard packaging constraint. The roughly 14 mm transformer, tall capacitors and MagJack cannot occupy that interboard gap. Place these on the outward-facing side of board 1 or revise the mechanical stack. The present connector-only PCB does not establish that all electronics fit in 60 × 60 mm.

## Stackup and fabrication rules

An explicit, symmetric generic stackup exists: eight 35 µm copper layers and dielectric thicknesses **0.10 / 0.18 / 0.10 / 0.56 / 0.10 / 0.18 / 0.10 mm**, totaling 1.60 mm before solder-mask conventions. FR4 is assigned Er 4.5 and loss tangent 0.02. This is a template, not a fabricator-approved material stack. Copper finish is `None`, dielectric constraints are disabled, and layer functions/reference planes are not implemented in copper.

Only the Default routing class is defined (0.125 mm clearance/track settings). No dedicated PoE-primary/isolation, high-current power or USB/Ethernet/CSI impedance constraints are enforced. No isolation keepout is present. Before layout release, agree the actual stack/materials with the fabricator, calculate and constrain line geometries against that stack, assign continuous return planes, specify the isolation barrier including internal-layer copper/vias, and size power copper and thermal paths. Eight layers by themselves establish none of these properties. Creepage/clearance values must be selected from the actual isolation/safety requirements and component/reference-design guidance; the 0.125 mm Default rule is not an isolation design.

## 3D model status

The current coverage index has 228 physical references: 8 manufacturer-CAD associations, 204 generic KiCad package models, 1 downloaded third-party PHY model, 14 bare test pads and **1 missing model: RT5-ZZ-0030 MagJack**. Thus the project must not be described as having original manufacturer models for every component. The DF40 models are present, associated and have source/hash records in `lib/3dmodels/manufacturer/index.csv`. Generic package models help visualization but do not verify exact part fit or isolation. The jack model is still needed for a complete mechanical collision check; no replacement geometry was generated.

## Major-part price check

These are **indicative USD listings retrieved on the check date**, not a live purchasing quote. Distributor pages and search-index snapshots disagree on stock and sometimes price; direct pages can hide dynamic prices. Taxes, shipping, tariffs, PCB fabrication and assembly are excluded. Capacitors and resistors are excluded as requested. `audit-major-prices.csv` records quantity breaks, sourcing alternatives and availability limitations.

| Part | One-piece USD | Comment |
|---|---:|---|
| FT2232HL-REEL | 5.97 | [Mouser](https://www.mouser.com/en/ProductDetail/FTDI/FT2232HL-REEL?qs=D1%2FPMqvA100v7FHcEx164g%3D%3D); long lead time shown |
| TPS23730RMTR | 4.95 | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TPS23730RMTR/13280037) |
| RTL8211F-CG | 1.42 | [LCSC C187932](https://www.lcsc.com/product-detail/C187932.html); indexed listing |
| RT5-ZZ-0030 | 3.01 | [LCSC C2934914](https://www.lcsc.com/product-detail/C2934914.html); older indexed quote, current availability unconfirmed |
| POE51Q-12ED | 3.48 direct / 6.50 distributor | [Coilcraft](https://www.coilcraft.com/en-us/products/transformers/power-transformers/power-over-ethernet/poexxq/poe51q-12/), [Mouser](https://www.mouser.com/en/ProductDetail/Coilcraft/POE51Q-12ED?qs=bZr6mbWTK5n9wUyOO%252BFTXw%3D%3D) |
| TPS259474ARPWR | 1.95 | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TPS259474ARPWR/14124024); conflicting stock snapshots, newer says due 2026-12-14 |
| DF40 female on board 1 | 1.74 | [LCSC C424649](https://www.lcsc.com/product-image/C424649.html) |
| DF40 male on board 2 | 1.42 | [LCSC C531031](https://www.lcsc.com/product-detail/C531031.html); excluded from board-1 subtotal |

The **partial seven-line board-1 subtotal is $22.52**, or $25.54 if the transformer is purchased at the distributor price. The mating pair is about **$3.16** using the listed LCSC prices. All six stack connectors (three mating pairs) are about $9.49; each intermediate board has two connectors. These are not whole-board totals.

The original seven-line subtotal above is retained only to show its limited scope. The extended check below supersedes it for budget assessment. No substitutions were made.

## Extended component cost check

The price CSV now covers **24 priced BOM lines / 35 physical parts**. Their allocated low-quantity subtotal is **$46.43**, before capacitors, resistors, the eleven unpriced references below, PCB fabrication, assembly, shipping or taxes. Buying the listed minimum packs at the same price breaks would cost about **$48.99** for these lines. That pack calculation is conservative rather than an optimized cart: for example, buying ten STPS3H100U at $0.415 each costs less cash than eight at $0.67 each. The $45 target therefore is **not established by these quotes**; a purchasing cart and further sourcing work are required. It would be misleading to call the earlier $22.52 partial subtotal the board cost.

| Additional part | Qty on board | Listed unit USD | Allocated USD | Source / limitation |
|---|---:|---:|---:|---|
| SN74AXC4T245PWR | 2 | 0.3152 | 0.63 | [LCSC C2867798](https://www.lcsc.com/product-image/C2867798.html); MOQ 5 |
| TPS22918DBVR | 2 | 0.2942 | 0.59 | [LCSC C131941](https://www.lcsc.com/product-image/C131941.html); MOQ 5 |
| AP2112K-3.3TRG1 | 1 | 0.2800 | 0.28 | [DigiKey / Diodes Incorporated](https://www.digikey.com/en/products/detail/diodes-incorporated/AP2112K-3-3TRG1/4470746) |
| 93LC46B-I/SN | 1 | 0.3100 | 0.31 | [Mouser](https://www.mouser.com/en/ProductDetail/Microchip-Technology/93LC46B-I-SN?qs=g6BBfX6YTkmj0a6KI7j5ww%3D%3D) |
| TPS62160DSGR | 1 | 0.8884 | 0.89 | [LCSC C324077](https://www.lcsc.com/product-detail/C324077.html) |
| TLV803EA29DBZR | 1 | 0.4491 | 0.45 | [LCSC C1852114](https://www.lcsc.com/product-detail/C1852114.html) |
| TPD4E1B06DRLR | 2 | 0.9600 | 1.92 | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TPD4E1B06DRLR/5178574) |
| USBLC6-2SC6 | 1 | 0.1844 | 0.18 | [LCSC C7519 / STMicroelectronics](https://www.lcsc.com/product-detail/C7519.html); MOQ 5 |
| STPS3H100U | 8 | 0.6700 | 5.36 | [DigiKey](https://www.digikey.com/en/products/detail/stmicroelectronics/STPS3H100U/2236916) |
| FSV1060V | 1 | 1.9800 | 1.98 | [DigiKey via indexed distributor cross-list](https://www.digikey.com/en/products/detail/littelfuse-inc/DST560S/7347663) |
| FDMS86252 | 1 | 3.5400 | 3.54 | [DigiKey](https://www.digikey.com/en/products/detail/onsemi/FDMS86252/2410061) |
| FOD817DS | 2 | 0.4000 | 0.80 | [Mouser](https://www.mouser.com/en/ProductDetail/onsemi/FOD817DS?qs=32VJUWvZ7XYY8mAX6gBHJQ%3D%3D) |
| SN74LVC1G02DBVR | 1 | 0.1100 | 0.11 | [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC1G02DBVR/385714) |
| 744272251 | 1 | 3.3500 | 3.35 | [Mouser](https://www.mouser.com/en/ProductDetail/Wurth-Elektronik/744272251?qs=PGXP4M47uW5C6uyW1HsSRw%3D%3D) |
| XAL4020-222MEC | 1 | 2.2500 | 2.25 | [Coilcraft direct](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xal/xal40xx/xal4020-222/) |
| USB4105-GF-A | 1 | 0.8000 | 0.80 | [DigiKey](https://www.digikey.com/en/products/detail/gct/USB4105-GF-A/11198441) |
| ABM8-12.000MHZ-12-B1U-T | 1 | 0.4700 | 0.47 | [Mouser](https://www.mouser.com/en/ProductDetail/ABRACON/ABM8-12.000MHZ-12-B1U-T?qs=vLWxofP3U2wqlTvBlimfnA%3D%3D) |

Unknowns are explicitly blank in the CSV, **not zero**: L201, L507, Y201, D512–D515, Q505, F101, FB101 and FB102. Their omission prevents a complete BOM quote. L201 is currently specified as `LPS4018-222MR`, which lacks the complete packaging suffix; the [current manufacturer MRC page](https://www.coilcraft.com/en-us/products/power/shielded-inductors/ferrite-drum/lps/lps4018/lps4018-222/) requires a quote. L507's older `LPS4018-332MLB` uses the earlier termination version; [Coilcraft states](https://www.coilcraft.com/en-us/products/power/shielded-inductors/ferrite-drum/lps/lps4018/) the previous version is only available to current customers. The newer MRC version is a candidate to qualify, not an already-approved substitution. F101 and the ferrite beads lack exact manufacturer part numbers.

Sourcing materially affects cost: FT2232HL is listed around $5.97 at Mouser but $11.86 at LCSC. XAL4020-222MEC is listed at $2.25 by Coilcraft, while an LCSC cross-list showed substantially more. A single-supplier LCSC purchase is not automatically cheaper. Some exact TI parts show zero stock/backorder; quotes do not establish a buildable current purchasing basket.

TPD4E1B06DRLR is marked Active at DigiKey but LCSC's limited inventory page warns against new designs. This distributor flag alone does not establish manufacturer obsolescence. [Onsemi bulletin PB27308XA](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8899/PB27308XA.pdf) also lists FDMS86252 with FDMS86102LZ mapping; confirm the current lifecycle, change applicability and stock before releasing the BOM. No replacement has been silently applied.
