# compact 35 W PoE options

Research date: 2026-11-21. Target remains at least 35 W operating output, Class 6, custom circuitry, existing USB JTAG/UART function. No component or schematic changes were made for this research.

**No verified low-cost catalogue transformer was found that provides the required power and materially reduces both the current transformer's PCB area and height.** Lower-power 10–25 W designs must not be substituted merely because their transformer looks smaller.

## what is already integrated

TPS23730 already integrates the PoE PD interface, hot-swap switch, startup and PWM controller. It still needs a power transformer and external switching MOSFET. MP8030 is a legitimate alternative Class 6 controller in a 5 × 6 mm QFN, but its integrated high-voltage FET is the **hot-swap FET**, not the main flyback power switch. It also retains a transformer and external switching power stage; replacing the controller alone does not solve the transformer's size. MPS advertises a one-piece price of $3.26 and $2.45 at ten units on the inspected page; these exclude magnetics, rectification, protection, delivery and tax. Stock/delivery dates on the cached page should be rechecked before purchase. [TPS23730](https://www.ti.com/product/TPS23730), [MP8030](https://www.monolithicpower.com/en/mp8030.html)

A more integrated example is TPS23758: it includes a 150 V switching MOSFET, but TI rates this family for **13 W Type 1**, so it cannot retain the present power requirement. MP8009 is an 802.3af/at solution; it is not a Class 6 replacement. [TPS23758](https://www.ti.com/product/TPS23758), [MP8009](https://www.monolithicpower.com/en/mp8009.html)

## genuine magnetic alternatives

| Option | Official mechanical/electrical facts | Fit against the request |
|---|---|---|
| Current Coilcraft POE51Q-12ED | Body 13 × 14.5 mm, lead span 17.7 mm, height 14 mm; 51 W series, 12 V / 3.9 A; 22.2 µH, ratio 1:0.5:0.5 | Already small in XY for this power. Original manufacturer STEP is already in the project. Prototype qualification remains necessary. |
| Bourns PLN060-ER20A12S planar | 22.5 × 21 mm maximum extent, 8 mm height; flyback 60 W, 12 V / 5 A, 21 µH, ratio 1:0.5:0.5, nominal 200 kHz | Height decreases about 43%, but XY area rises from approximately 257 to 473 mm², about 84% larger. **Does not satisfy both smaller area and smaller height.** Requires new footprint and circuit qualification. Exact original STEP was not verified. |
| LinkCom low-profile families | Manufacturer advertises EPD13.3 ≤10 mm height. This is a core/platform announcement, not an exact 35 W output part specification. | Not a qualified replacement. Require an exact ordering code, winding drawing, current/temperature rating, price and model before considering it. |

The dimensions above compare the current lead-envelope area with the alternative envelope, rather than comparing body dimensions against another part's land pattern. None of these power ratings by itself guarantees the assembled converter's output. [Coilcraft drawing](https://www.coilcraft.com/getmedia/71a3c6d3-d040-4587-8bbd-dd1492f81afc/poexxq.pdf), [Bourns planar drawing, pp. 1–2](https://www.bourns.com/docs/Product-Datasheets/PLN0xx-ER20.pdf), [LinkCom low-profile announcement](https://www.linkcom.com.tw/en/news.php?act=list&cid=1&page=5)

The current Coilcraft part lists **$3.48 at one piece** on its official product page. The page also shows a selected-configuration availability warning, so the listed price is not proof of immediately purchasable stock. [Official Coilcraft price](https://www.coilcraft.com/en-us/products/transformers/power-transformers/power-over-ethernet/poexxq/poe51q-12/)

The Bourns part's availability is a further obstacle for this prototype: the inspected distributor listing is not stocked and offers full-reel quantities rather than a practical few-piece purchase. Do not use an apparent $6 catalogue price as proof it can actually be bought singly. [Distributor availability](https://www.digikey.ee/en/products/detail/bourns-inc/PLN060-ER20A12S/22286776)

## official reference designs worth using

- **TI PMP22477:** existing Class 6 / isolated 12 V reference basis. It supports keeping the current integrated-controller approach. A different transformer still needs its own calculations and tests. [Design resources](https://www.ti.com/tool/PMP22477)
- **TI TIDA-050023:** genuine 42–57 V, 12 V / 4.25 A isolated design using TPS2373 plus LM51551-Q1. It is relevant to power and cost, but introduces two controller ICs and does not establish a smaller complete circuit. [Official design files](https://www.ti.com/tool/TIDA-050023)
- **MPS MP8030 reference support:** official material lists a 51 W / 12 V active-clamp forward design using an EP13 transformer. This proves an appropriate power-class reference exists, but adds a clamp/output-inductor power stage; EP13 does not establish a reduction in both dimensions. Request the precise BOM, transformer drawing and test report before committing to a redesign. [MPS reference-design summary](https://media.monolithicpower.cn/mps_cms_document/m/p/mps_dc_.pdf)
- **Skyworks Si34071:** official isolated 12 V / 6 A evaluation documentation exists. It is a useful high-power reference, but has a more elaborate forward stage and is not evidence for a simpler or smaller 35 W implementation. [UG478](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/user-guides/ug478-si34071-iso-12v6a-output-evb.pdf)

## can the transformer be removed?

A non-isolated buck converter can convert the PoE voltage to 12 V using an inductor. It still needs a compliant Class 6 PD interface, rectification, protection and power budgeting. It changes the isolation architecture: the camera/FPGA ground then belongs to the PoE power domain.

In this project the USB programmer, JTAG/UART interfaces and accessible ground are directly connected to secondary GND. Removing only the power transformer would connect that ground to the PoE power return. Preserving the USB function therefore requires a system-level isolation redesign, for example isolating all programmer signal crossings and supplying their two sides appropriately. This can recover magnetic power-stage volume but adds isolators, power domains, routing and qualification; a saving is not established. TI explicitly identifies exposed USB/ground as a reason to retain isolation. [TI PoE topology and isolation guidance](https://www.ti.com/video/6307067380112)

## actionable recommendation

Keep the current controller and power target until there is a documented replacement that solves **both** dimensions. First perform a realistic placement study with the transformer and jack on an externally facing board side, rather than inside the 3 mm interboard gap. If that cannot meet the enclosure envelope, obtain a manufacturer reference/quote for a lower-profile 35 W-plus transformer or reconsider the isolation architecture. Do not silently lower power, replace an isolated transformer with an ordinary inductor, or claim MP8030 removes the external switching stage. A final cost or dimension reduction is currently unproven.
