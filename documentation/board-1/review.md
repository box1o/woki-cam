# design review

The project uses a Bel 0826-1X1T-HS-F Gigabit, four-pair 100 W MagJack, TPS23730 Class 6 input/converter, Coilcraft POE51Q-12ED transformer, RTL8211F PHY and FT2232HL USB programmer/UART.

All four schematic roots pass strict ERC under the existing project rules. Renaming and presentation cleanup preserve every physical pin connection group. The four overview/stack sheets use A3; the Board 1 PDF has been regenerated and visually reviewed. See `cleanup-verification.json` for current results and `components.csv` / `connections.csv` for the component and connection indexes.

Board 1 is an unfinished layout: 20 DRC findings (19 errors and one warning), plus 499 unconnected items. Fifteen findings concern copper crossing the outline; four concern the specified USB connector hole clearance; one concerns a diode silkscreen crossing the edge. Many components remain staged outside the board. The other boards have no geometric DRC findings but remain unrouted. Existing outlines, mounting holes and aligned stack connectors are preserved. J2 clears H3; R543 clears its neighboring capacitor.

The PCB stack fit remains unvalidated: the nominal 3 mm connector separation does not accommodate the approximately 14 mm transformer and 15 mm jack where boards overlap. Tall-component placement and enclosure access require mechanical design.

35 W output remains a design target requiring prototype qualification. The adapted converter needs current-limit, startup, loop-stability, temperature, isolation and EMC verification; see `compact-poe-review.md`. ERC does not establish electrical performance or manufacturing readiness.

All active models use STEP: original manufacturer CAD where available, faceted conversions of the two downloaded meshes, and installed KiCad generic package models for standard parts. No generated stand-in geometry is retained. Generic package models do not prove exact manufacturer dimensions. Model provenance is recorded in `model-download-sources.json`, `bel-hs-model-source.json` and `../../lib/3dmodels/manufacturer/index.csv`.

Obsolete reports, unused component datasheets and removed models are backed up outside the project in `/home/woki/dev/woki-schematic-backups/project-cleanup-20261121`.

`component-register.csv` lists all 232 physical Board 1 objects (228 schematic components and four existing mounting holes), their side, symbol, footprint and model association.

Dense passive and small-package references are retained on the fabrication/assembly layer. Connector, debug and major-IC markings remain on silkscreen where space permits. `../board-1-assembly.pdf` provides front and mirrored-back views. Seven component instances now have closed courtyards; missing courtyards are checked. U301 uses two 0.25 mm tented thermal-via drills within the existing 0.50 mm copper pads.

Legacy instance paths in the USB, PHY-supply and Ethernet sheets were repaired. All four strict ERC checks pass and physical connection groups are unchanged.
