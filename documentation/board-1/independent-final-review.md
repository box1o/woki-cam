# independent final schematic check

Reviewed current KiCad-exported XML netlists for all four boards, connector CSV/JSON, physical DF40 footprints, compact converter review, USB migration proof and TI PMP22477 Rev C schematic page 2.

- All six stack connector instances contain exactly 100 physical contact roles, matching the allocation JSON and 100-row CSV. The functional pin ranges cover pins 1–100 without gaps or duplication.
- Every reserved CSI differential pair uses adjacent contacts on the same physical row, 0.4 mm apart. Rows alternate between successive pairs. Female/male footprint pin numbering agrees after board-side mirroring.
- **Correction required at review time:** CSI signals were present in `shared_reservations`, so boards 2 and 3 connected J1 to J2 on every CSI pair. This contradicts the stated board-2-top to board-3-bottom point-to-point policy and creates unused branches. Remove CSI from shared pass-through and leave endpoint reservations explicitly NC until FPGA/sensor circuitry exists.
- Ethernet, JTAG and UART have no higher-board pass-through connection. Shared I²C, SPI, camera control, GPIO, power-good, reset and VIO roles pass between board-2/3 connectors as intended. These reservations do not implement a master, pullups, level translation or endpoint circuitry.
- T502 pin 4 connects to CP. Pin 5 connects through R545 (3.90 Ω) to the D514 anode/bias/feedback network; D514 cathode supplies PRI_VCC. Pin 5 is **not** directly RTN. The original TI sheet-2 T2 pin 5 was CP and pin 4 fed R45/D14, so the Coilcraft 4↔5 remap preserves actual circuit topology. Corrected misleading prose in compact-poe-review.md; no circuit changes.
- R567 remains 0.05 Ω and R572 is 100 Ω. The documented minimum current limit estimate (4.46 A) is below the illustrative biased-inductance full-load peak (4.54 A). Therefore 35 W across all corners is not established. The existing prototype/thermal/loop qualification warning is required and appropriate.
- USB migration evidence records exactly the same 63 physical components and 75 physical connection groups. Current export uses native FT2232HL pin assignments: D−/D+ 7/8, OSCI/OSCO 2/3, MPSSE TCK/TDI/TDO/TMS 16/17/18/19, UART TX/RX 38/39, VREGOUT49 to VCORE12/37/64, VREGIN50 and VCCIO20/31/42/56 to USB_3V3. TEST13 is grounded. No pin-map inconsistency found.
- Full Board-1 ERC supplied by parent reports zero electrical violations under the saved project rule configuration. ERC does not establish analog stability, power capability, EMC, manufacturability or complete physical placement.

Independent evidence: `/tmp/independent-power.xml`, `/tmp/independent-board2.xml`, `/tmp/independent-board3.xml`, `/tmp/independent-board4.xml` and `/tmp/usb-native-net-comparison.json` during this review. Later parent corrections must regenerate the affected exports.

Final correction: CSI signal pass-through was removed from both middle-board connectors. Regenerated XML exports contain no connected CSI signal nets, all four schematic ERC reports show zero violations, and final PCB connector net comparison reports zero mismatches. See `stack-checks/` and `final-stack-net-verification.json`.

Final correction: CSI signal pass-through was removed from both middle-board connectors. Regenerated XML exports contain no connected CSI signal nets, all four schematic ERC reports show zero violations, and final PCB connector net comparison reports zero mismatches. See `stack-checks/` and `final-stack-net-verification.json`.

Display correction requested by user: each physical connector is now one single 100-pin schematic symbol, with no separate units or connector sheets. Board 1 physical pin-connection groups are unchanged; regenerated ERC is zero on all four schematics.

Final correction: CSI signal pass-through was removed from both middle-board connectors. Regenerated XML exports contain no connected CSI signal nets, all four schematic ERC reports show zero violations, and final PCB connector net comparison reports zero mismatches. See `stack-checks/` and `final-stack-net-verification.json`.
