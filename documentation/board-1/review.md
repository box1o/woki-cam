# design review

The project uses a Bel 0826-1X1T-HS-F Gigabit, four-pair 100 W MagJack, TPS23730 Class 6 input/converter, Coilcraft POE51Q-12ED transformer, RTL8211F PHY and FT2232HL USB programmer/UART.

All four schematic roots pass ERC under the existing project rules. Renaming preserves every physical pin connection group. See `cleanup-verification.json` for current results and `components.csv` / `connections.csv` for the component and connection indexes.

Board 1 is an unfinished layout: 262 DRC violations and 499 unconnected items remain. The other three boards have no geometric DRC violations but still have unrouted connector signals. Existing outlines, mounting holes and connector positions are preserved.

35 W output remains a design target requiring prototype qualification. The adapted converter needs current-limit, startup, loop-stability, temperature, isolation and EMC verification; see `compact-poe-review.md`. ERC does not establish electrical performance or manufacturing readiness.

Models use original STEP geometry where available, downloaded WRL meshes where necessary, and installed KiCad generic package models for standard parts. No generated stand-in geometry is retained. Generic package models do not prove exact manufacturer dimensions. Model provenance is recorded in `model-download-sources.json`, `bel-hs-model-source.json` and `../../lib/3dmodels/manufacturer/index.csv`.

Obsolete reports, unused component datasheets and removed models are backed up outside the project in `/home/woki/dev/woki-schematic-backups/project-cleanup-20261121`.
