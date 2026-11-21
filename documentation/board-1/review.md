# board 1 circuit draft

Open `../../boards/01-power/power.kicad_sch`. The current seven-page drawing is `../board-1-custom.pdf`; earlier PDFs are historical snapshots.

| function | implementation |
|---|---|
| Ethernet jack | 0826-1X1T-HS-F, integrated Gigabit magnetics and four-pair PoE taps |
| isolated 12 V | TPS23730 Class 6 flyback, Coilcraft POE51Q-12ED |
| local supplies | TPS62160 3.3 V regulator; TPS22918 PHY supply ramp |
| Ethernet PHY | RTL8211F-CG, 25 MHz crystal, protection and jack LEDs |
| stack protection | TPS259474A integrated circuit breaker |
| allocation check | two isolated PoE status signals and a NOR gate |
| PHY reset | TLV803EA29DBZR supervisor |
| programmer | USB-powered FT2232HL, EEPROM, JTAG/UART translators |

## stack connector

`connector-pinout.csv` defines all 100 contacts, revision 2. Each connector is one complete 100-pin symbol. Consecutive pin ranges cover power, system control, Ethernet, JTAG, UART/GPIO, I²C, SPI, CSI-2 and camera control. This replaces the previous pinout.

Shared controls and power pass through the middle boards. RGMII, MDIO, PHY control, JTAG and UART terminate at board 2. CSI-2 is reserved only between the FPGA and camera boards: no long branches through the full stack. Its five differential pairs use adjacent contacts on the same physical row, alternating rows between pairs.

Future interface endpoints remain explicitly unconnected until the FPGA, sensor and light drivers are selected. A named reservation is not a completed interface. Use one master and one pullup set for shared I²C; SPI slaves must release MISO when deselected. Interface levels depend on the selected devices.

VIO_TARGET is a 3.3 V interface supply/reference, not the main FPGA supply. Do not backfeed it. RGMII uses both PHY clock delays; do not add the same delays in the FPGA. The PHY reset request must be open drain. USB powers the programmer independently of PoE.

## verification

- All active schematics saved in KiCad 10 native format; Board 1 ERC reports zero violations without exclusions.
- 228 physical references, no DNP options. Standard KiCad symbols are used where appropriate.
- USB migration preserves all 63 physical components and 75 connection groups; local supply migration preserves its 20 physical components and pin connections.
- The converter is adapted from TI PMP22477. Its transformer and current-sense filtering changed; see `compact-poe-review.md` for assumptions and remaining qualification.
- Components, physical pin connections, test pads, connector allocation and model availability are indexed here and in `../../lib/3dmodels/model-coverage.csv`.

## remaining work

This is a reviewed schematic draft, not validated hardware. The 35 W output target needs prototype efficiency, thermal, current-limit, startup, transient and loop-stability tests. Class 6 requires a suitable four-pair PSE. The eFuse is a circuit breaker, not a constant-power limiter; nominal trip is about 3.50 A, with approximately 3.12–3.89 A tolerance.

Boards 2–4 remain connector-only mechanical templates. Board 1 now contains imported electronics with incomplete placement; existing holes, outline, layer stack and locked connectors are preserved. Electronic fit, routing, impedance, isolation spacing and thermal performance have not been validated. Tall parts cannot occupy the 3 mm inter-board gap.

Original manufacturer models are used where available; generic package and third-party models are identified separately. An exact 0826-1X1T-HS-F model is still unavailable. The complete BOM cost and LCSC stock are not confirmed, so the $45 target remains provisional.

## independent datasheet audit

See `audit-power.md`, `audit-ethernet-usb.md` and `audit-pcb-cost.md`. The reviewed fixes and connection-preservation evidence are in `datasheet-fix-verification.json`. USB clock load values remain initial; measure frequency and startup. Host software must select channel A MPSSE for JTAG; a blank EEPROM starts as UART.

Compact power research: `audit-compact-power-options.md`. No verified economical 35 W replacement improves both height and PCB area. Current transformer retained. The extended price audit covers 24 BOM lines / 35 physical parts at approximately $46.43, excluding caps/resistors, eleven unpriced references and PCB/assembly/shipping/taxes; the $45 total target is not established. See `audit-price-summary.json`.

Latest PCB cleanup: removed the duplicate imported J1, linked all stack footprints to their single-unit schematic symbols, removed unused eth library table entries, and separated R543 from H1. Live Board 1 DRC is recorded in `stack-checks/power-drc.json`; placement, silkscreen, two 0.2 mm thermal-hole constraints and USB footprint hole-clearance constraints remain unresolved. No routing is present. See `pcb-cleanup.json` and `jack-model-search.json`.
