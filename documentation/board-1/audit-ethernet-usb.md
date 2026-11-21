# Ethernet and USB independent datasheet audit

Reviewed 2026-11-21. Scope: live Board 1 hierarchical schematic exported with KiCad 10.0.8 to `/tmp/audit-eu.net`, manufacturer datasheets stored in `datasheets/`, and actual physical pin nets. Read-only circuit review; no schematic or PCB edits by this reviewer. This is schematic evidence, not proof of hardware operation.

## Findings requiring action

1. **USB crystal tolerance is not fully specified to meet FTDI.** Y101 identifies `ABM8-12.000MHZ-B2-T`. FT2232H section 6.3 specifies 12 MHz ±30 ppm. Abracon's ordering table makes B the temperature range, 2 the ±20 ppm initial tolerance, and the omitted frequency-stability option defaults to ±50 ppm. That cannot guarantee ±30 ppm across temperature, even before load error and aging. Select an explicitly tighter ordered variant, with initial tolerance, temperature stability, aging and PCB load error fitting the 30 ppm budget. A ±10 ppm initial / ±10 ppm stability variant leaves some margin; verify the exact manufacturer order code and availability. C105/C106 = 27 pF is an initial reference value, not a measured load qualification.

2. **EEPROM DO pullup is on the other side of the series resistor from the documented FTDI circuit.** Current U106.4 (DO) only joins R105.1. R105 = 2.2 kΩ correctly connects DO to U101.61 / U106.3 (DI), but R108 = 10 kΩ pulls up the DI/EEDATA side. FT2232H Table 3.4 explicitly calls for the DO pin to be pulled to VCC through 10 kΩ. Move R108's low terminal to U106.4 / R105.1 to match the documented interface. The current arrangement is not proven nonfunctional, but it does not reproduce the specified pullup topology and has different input-low loading.

## Boot and programming requirements

- U106 is **93LC46B-I/SN**, a 64 × 16-bit EEPROM. Its pins 6 and 7 are NC; leaving both NC is correct. The B suffix provides the required 16-bit organization without an ORG connection. The standard SOIC-8 footprint pins CS1, CLK2, DI3, DO4, VSS5, VCC8 match the manufacturer pinout.
- Blank or absent EEPROM boots **two UART channels**, default VID 0403 / PID 6010, bus-powered configuration and a 500 mA maximum-power descriptor. It does **not automatically boot a JTAG engine**.
- Manufacturing must program and verify an EEPROM profile with FT_PROG, preserving bus-powered operation, correct power budget and a unique serial number. Keep channel B available as UART; configure the host driver binding so the programming application can claim channel A and switch it into **MPSSE**. MPSSE JTAG mode is selected by host software, not a schematic wire or a fixed EEPROM “JTAG” choice. Select clock rate and JTAG transitions for the eventual FPGA. A stock VCP binding on A can prevent the JTAG application opening it.
- PWREN# goes low after USB configuration and high during suspend. It enables the translators through their active-low OE inputs; it does not indicate that the host has already configured MPSSE. Target-side TMS/TDI/UART idle pullups and TCK pulldown help establish initial states, but software must initialize channel A before active programming.

## Connections checked against datasheets

| Circuit | Observed implementation | Result / boundary |
|---|---|---|
| FT2232HL power | VREGIN50 and VCCIO20/31/42/56 on USB_3V3; VREGOUT49 drives VCORE12/37/64 with 10 µF plus bypass; VPHY4 and VPLL9 filtered from 3.3 V; all listed ground pins grounded; TEST13 grounded | Matches FTDI bus-powered architecture. LDO dissipation, USB suspend current, inrush and supply ramps need measurement. |
| FTDI USB | DM7 to Type-C A7/B7; DP8 to A6/B6; independent CC1/CC2 5.1 kΩ pull-downs; USBLC6-2SC6 channels 1/6 and 3/4, GND2 and VBUS5 | Pin polarities correct. Route USB as controlled differential pair through protection, no long branches. |
| JTAG | FTDI16/17/18/19 = TCK/TDI/TDO/TMS; outputs U104 A→B, return U105 B→A | Physical directions correct. Series output resistors 33 Ω are present. Final FPGA voltage/timing remains a requirement. |
| UART B | FTDI38 TX → U104 → target RX; target TX → U105 → FTDI39 RX | Correct. Target TX/RX naming is from FPGA perspective on the interboard interface. |
| AXC translators | PW package VCCA1=USB_3V3; VCCB16=VIO_TARGET; grounds8/9; U104 DIR2/3 high, U105 DIR2/3 low; OE14/15 driven by PWREN# with pullup | Matches TI truth table and PW pinout. TI supports partial power-down and either-rail-off isolation. VIO_TARGET must remain within 0.65–3.6 V; current PHY architecture requires 3.3 V. |
| RTL8211F MDI | MDIP/N pins1/2→jackR11/R10;4/5→R4/R5;6/7→R3/R2;9/10→R8/R9 | All four pair polarities match UDE drawing. Magnetics are integrated in the jack. |
| Jack PoE | R13/R14/R15/R16 go only to the cable-side PoE bridges; PHY center taps R12/R6/R1/R7 each have 100 nF to secondary GND | Power extraction and PHY-side center taps are separated correctly. Physical primary/secondary/chassis clearance still needs PCB implementation. |
| PHY power/core | 3.3 V pins11/29/40; switch pin30 via 2.2 µH L201 to core pins3/8/21/38, bypass100 nF and bulk4.7 µF; exposed pad41 GND; RSET39 has2.49 kΩ1% to GND | Matches RTL8211F switching-regulator variant, not RTL8211FD LDO variant. Thermal-pad copper/vias and short switch loop are essential. |
| PHY straps | PHYAD2/1 low, PHYAD0 high; PLLOFF low; TXDLY/RXDLY high; CFG_EXT high; CFG_LDO1/0 low | Address1, PLL remains active in ALDPS, 2 ns TX/RX delays, external3.3 V RGMII selected. FPGA must not add another2 ns at the same interface; FPGA strap-facing inputs must be high impedance during reset. |
| PHY LEDs | LED1 pin33 and LED2 pin34 are strapped low via4.7 kΩ and drive LEDs through510 Ω; relevant cathodes grounded | Correct active-high arrangement for low straps. Default indication is speed-specific100/1000 Mbps, not a universal all-speed link lamp. The two-terminal bicolor jack LED only displays the polarity actually driven; do not promise all available colors. |
| PHY reset | TLV803EA29 open-drain supervisor, approximately200 ms release delay; request pin joined with0 Ω | Adequate nominal startup reset duration versus10 ms requirement. External PHY_RESET_REQ_N must be open drain or high impedance; push-pull high would fight the supervisor. Respect at least100 ms complete power-off interval and verify power-up ramps. |
| PHY clock | 25 MHz Y201, CL20 pF,36 pF initial capacitors; grounded case pins2/4 | YXC family sheet supports50 Ω ESR at25 MHz and ±20 ppm initial / ±20 ppm thermal / ±3 ppm aging configurations, within the50 ppm total requirement only with remaining PCB/load error controlled. Family PDF is not an exact ordering-code certificate: confirm supplied X322525MSB4SI configuration and measure startup/frequency. |

## Footprint scope

FT2232HL LQFP64 10×10 /0.5 mm, AXC PWR TSSOP16 /0.65 mm, EEPROM SN SOIC8 /1.27 mm and RTL8211F QFN40 exposed-pad numbering were compared to their respective package pin tables. Jack R1–R16 / L1–L4 / shield labels match the maker's physical numbering. This does not substitute for checking the custom land geometry and board-level courtyards against the mechanical drawings. There is no routed electronics PCB in this review; connector-only board templates cannot establish impedance, fit, EMI, thermal performance or operational Ethernet/USB.

## Primary documents

- FTDI [FT2232H datasheet v2.9](https://www.ftdichip.cn/Support/Documents/DataSheets/ICs/DS_FT2232H.pdf): Tables3.1–3.4, section6.1, section6.3, sections7/7.1. Downloaded copy: `datasheets/ft2232h.pdf`. The alternate official ftdichip.com endpoint returned403 during this audit.
- Abracon [ABM8 datasheet](https://abracon.com/Resonators/ABM8.pdf): electrical specifications and order-code table, pages1–2.
- Microchip [93AA/LC/C46A/B/C datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/93AA46A-B-C-93LC46A-B-C-93C46A-B-C-1-Kbit-Microwire-Compatible-Serial-EEPROM-Data-Sheet-DS20001749.pdf): organization and package pinout.
- TI [SN74AXC4T245 datasheet](https://www.ti.com/lit/ds/symlink/sn74axc4t245.pdf): PW pinout, supply isolation and direction/OE truth table.
- Realtek RTL8211F(I)-CG / RTL8211FD(I)-CG maker datasheet Rev1.4, local `datasheets/rtl8211f.pdf`, distributed [via LCSC](https://datasheet.lcsc.com/datasheet/pdf/7023c5bb6713a670a415e3c449e0d974.pdf?productCode=C187932): sections6–10, particularly Tables10/11,53 and56. Public manufacturer-origin document; not an independently confirmed latest revision.
- UDE RT516062-00 RevA, local `datasheets/rt5-zz-0030.pdf`, distributed [via LCSC](https://datasheet.lcsc.com/datasheet/pdf/f47e1624b47c6daa046dab3e9174a7f8.pdf?productCode=C2934914): drawing page2 and electrical diagram page8 of the PDF; Gigabit/60 W labeling and720 mA continuous rating are maker statements, not system PoE qualification.
- YXC YSX321SL family sheet, local `datasheets/x322525msb4si.pdf`, visually inspected because PDF text extraction is disabled/empty. Family options require exact order confirmation.
- TI [TLV803E datasheet](https://www.ti.com/lit/ds/symlink/tlv803e.pdf): EA timeout200 ms typical,130–270 ms limits.

## Proposed correction selected with parent reviewer

Use **ABM8-12.000MHZ-12-B1U-T** in the same footprint. Abracon's primary ABM8 table decodes this as CL12 pF, B=-20°C to+70°C,1=±10 ppm initial tolerance,U=±10 ppm temperature stability (U valid for B range), with ±2 ppm first-year aging. This allocates22 ppm before loading errors, leaving8 ppm against FTDI's30 ppm requirement. Set C105/C106 initially to15 pF C0G: CL = 15/2 +4.5 pF assumed effective stray =12 pF. Measure and trim actual loading;4.5 pF is an assumption, not measured PCB data. At12 MHz the ABM8 family maximum ESR is120 Ω; FTDI does not publish an explicit maximum crystal ESR or oscillator negative-resistance value in this datasheet, so startup/drive-margin qualification remains necessary. Crystal pins1/3 and case-ground pins2/4 match the existing standard3225 footprint. Exact part listings were independently found at DigiKey, Mouser and Newark; stock and procurement price are handled in the separate cost review.

## applied corrections

The parent applied the reviewed changes on 2026-11-21: EEPROM DO-side 10 kΩ pullup; ABM8-12.000MHZ-12-B1U-T with initial 15 pF loads; output-breaker R601 = 953 Ω / 1%. Current Board 1 ERC is zero, all 228 footprint pin maps resolve, and all physical pin groups other than the intended R108 move are preserved. See `datasheet-fix-verification.json`. Prototype qualifications above remain open.
