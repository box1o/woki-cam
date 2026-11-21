# compact PoE converter review

T502 now uses **Coilcraft POE51Q-12ED** instead of LDT9055-51R. The new transformer has a 13 × 14.5 mm body, a maximum 17.7 mm lead span and 14 mm height. Its 22.2 µH primary and 1:0.5:0.5 winding ratio require prototype qualification; this is not a proven drop-in replacement.

The auxiliary terminals are reversed relative to LinkCom: **pin 4 is the dotted CP terminal; pin 5 feeds the auxiliary bias/feedback network through R545 (3.90 Ω)**. Pin 5 is not directly connected to RTN: R545 feeds D514 anode, C540, R546 and R548; D514 cathode supplies PRI_VCC. This preserves the original TI arrangement after swapping the transformer terminal numbers. Primary pins 1/3 and secondary pairs 9+10 / 6+7 retain their functions. The manufacturer footprint and original STEP model are used.

R572 changes from 1 kΩ to 100 Ω. This reduces additional current-sense slope compensation; the controller retains internal compensation and blanking. R567 remains 0.05 Ω, switching frequency remains approximately 250 kHz, and the initial PSR divider/compensation values remain unchanged. The auxiliary-to-secondary voltage ratio remains 1:1.

At a **35 W stack target plus 2 W local load**, assuming 87% efficiency and 35 V after the input bridge/hotswap, first-order peak primary current is approximately:

| Effective primary inductance | Estimated peak current |
|---|---:|
| 22.2 µH nominal | 4.23 A |
| 19.98 µH, −10% tolerance | 4.38 A |
| 18 µH, illustrative biased value | 4.54 A |

Coilcraft's 4.7 A saturation-current specification describes a 15% inductance reduction at 25°C. It is not a guaranteed hot-core operating limit. The current-sense change gives an estimated minimum trip threshold around 4.46 A before transient effects; startup, overload/hiccup, thermal behavior and loop gain must be measured.

Eight unpopulated options and their dead wiring were removed: C521, C522, C546, C549, R551, R563, R565 and R570. Unused TPS23730 TPL and SCDIS pins are explicitly marked unconnected. All remaining physical connection groups are preserved after accounting for the deliberate auxiliary pin swap.

**35 W is a target, not a hardware guarantee.** Verify output regulation, primary current, switch/rectifier overshoot, loop stability, temperatures, EMC and total Class 6 input-power allocation before manufacture.

Sources: [Coilcraft transformer drawing](https://www.coilcraft.com/getmedia/71a3c6d3-d040-4587-8bbd-dd1492f81afc/poexxq.pdf), [TI TPS23730 datasheet](https://www.ti.com/lit/ds/symlink/tps23730.pdf), sections 8.3.7.2–8.3.7.3.
