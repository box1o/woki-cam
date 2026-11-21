# active library sources

Custom libraries contain only symbols unavailable in the installed KiCad library or multi-unit layouts for the selected parts. Standard resistors, capacitors, inductors, diodes, MOSFETs, power symbols, FT2232HL, EEPROM, USB receptacle/protection, TPS62160 and logic use KiCad symbols. The AXC translator has two body styles for the same physical pinout.

## symbols and footprints

- **0826-1X1T-HS-F**: four functional units of one physical MagJack: Ethernet/magnetics, cable-side PoE, yellow LED and orange/green LED. Pin numbers and lands follow the Bel drawing in `../datasheets/bel-0826-1x1t-hs-f-drawing.pdf`; see `symbols/magjack-pinout.csv`. Magnetics are integrated. The jack front keepout still needs a PCB-level copper and mounting review.
- **RTL8211F-CG**: four functional symbol units, one physical QFN. Pin allocation follows its Realtek datasheet; the footprint adapts the standard KiCad package to the published dimensions.
- **TPS23730 converter**: adapted from the original [TI PMP22477 reference](https://www.ti.com/tool/PMP22477) CAD and schematic. The project omits adapter input, output selection and unused options. TPS23730, FDMS86252, FSV1060V and transformer remain custom symbols; standard passives replace the imported passive symbols. This is an adapted prototype circuit, not an unchanged or qualified TI reference design.
- **POE51Q-12ED**: custom transformer symbol and footprint follow the [Coilcraft POExxQ datasheet](https://www.coilcraft.com/getmedia/71a3c6d3-d040-4587-8bbd-dd1492f81afc/poexxq.pdf). The auxiliary polarity and pin numbering differ from the previous transformer. The 14.99 mm dimension is the inner land-edge gap, giving land centers at ±8.27 mm for 1.55 mm wide pads. Current limit, regulation, compensation and thermal operation require prototype qualification.
- **LPS4018-332MLB, FDMS86252, 744272251, FOD817DS and Panasonic FK lands**: retain the TI reference pad geometry. Reference-field placement and missing courtyards have been corrected. `lps4018` separately copies the installed standard KiCad footprint without changing its pad geometry; only its missing 3D association is replaced with original Coilcraft CAD. These two LPS4018 footprints intentionally retain their respective reference land patterns.
- **TPS23730 land**: TI RMT0045A; RTN/VSS exposed pads remain distinct. TPS25947 and TPS62160 lands follow the TI package drawings. TPS62160 thermal-via drills are adapted to 0.25 mm inside the existing 0.50 mm copper pads, giving 0.125 mm annular rings; the vias remain tented. DF40 male/female symbols each show all 100 pins in one unit; footprints retain the existing Hirose contact geometry.
- Supporting component datasheets are in `../datasheets/`. Generic KiCad symbols, footprints and package models follow the [KiCad library licence](https://www.kicad.org/libraries/license/).

## 3D models

All active models use lowercase `.step` filenames. Native manufacturer STEP geometry is reused unchanged. The two downloaded mesh models were converted to faceted STEP while preserving every source triangle and color group; no substitute geometry was created. Footprint transforms set position and orientation; the converted jack has its existing pose baked into the STEP coordinates.

- **Original manufacturer CAD**: Hirose DF40 male/female; TI RMT0045A, RPW0010A and DSG0008A; Coilcraft LPS4018 and POE51Q; Würth WE-SL5 family model assigned by Würth to 744272251. File hashes and source links are in `3dmodels/manufacturer/index.csv`. The Coilcraft LPS4018 model was extracted unchanged from its original PCB library. Downloads used the manufacturer's public Azure mirror where its main download endpoint rejected access.
- **RTL8211F**: existing [Protoflow C187932 model](https://www.protoflow.ai/library/parts/C187932/files/WQFN-40_L5.0-W5.0-P0.4-BL-EP.wrl), downloaded as WRL and converted to STEP (5,312 faces); third-party CAD, not verified Realtek-original CAD. The footprint applies a +90° Z rotation, verified against its pin-1 marker in the native KiCad renderer.
- **FDMS86252**: existing [KiCad Vishay PowerPAK SO-8 model](https://raw.githubusercontent.com/KiCad/kicad-packages3D/master/Package_SO.3dshapes/Vishay_PowerPAK_SO-8.step), compatible generic package representation; not original onsemi part CAD.
- **FOD817DS and Panasonic FK capacitors**: installed KiCad generic package models. Capacitor models are package approximations (10.5 mm model height versus 10.2 mm nominal part height), not exact manufacturer originals.
- **Other standard parts**: installed KiCad generic package models; these do not establish exact manufacturer body tolerances.
- **0826-1X1T-HS-F**: complete downloaded Bel/CADENAS mesh converted to STEP (33,817 faces) with visualization materials for the shell, plastic, contacts and lenses. The incomplete OEM STEP export is archived outside the project to prevent incorrect STEP substitution. Conversion and placement details are recorded in `../documentation/board-1/bel-hs-model-source.json`. Bare test pads need no solid model.

`3dmodels/model-coverage.csv` indexes the current physical Board 1 components and model associations. Source URLs and attribution are retained in `../documentation/board-1/model-download-sources.json`.

Unused custom symbol definitions and the obsolete LDT9055 footprint were archived outside the project at `/home/woki/dev/woki-schematic-backups/library-cleanup-20261121`. Existing PCB mounting holes remain intentional mechanical objects even though duplicate schematic hole symbols were removed. The current schematic export is `../documentation/board-1.pdf`.

`../documentation/board-1/component-register.csv` lists Board 1 references, symbols, footprints, front/back side and model provenance. Standard KiCad library identifiers keep their upstream spelling; project filenames and custom identifiers are lowercase.

Closed courtyards were added to six legacy footprint definitions (seven placed instances) using their existing fabrication/pad envelopes, with 0.25 mm clearance or 0.50 mm for canned capacitors, following [KiCad courtyard conventions](https://klc.kicad.org/footprint/f5/f5.3/). Pads, numbering and model geometry were preserved apart from the stated TPS62160 drill adaptation.
