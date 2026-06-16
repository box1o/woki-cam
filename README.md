# Woki Cam

<p align="center">
  <img src="https://github.com/box1o/woki-cam/releases/latest/download/woki-cam-3d.png" alt="Woki Cam" width="720">
</p>

Modular Ethernet-powered infrared optical tracking camera. Four stacked PCBs detect retroreflective markers and send marker coordinates over Ethernet so a host can triangulate 3D positions from multiple cameras.

## Boards

| # | Directory | Role |
|---|-----------|------|
| 1 | `boards/01-power` | Power rails, Ethernet |
| 2 | `boards/02-fpga-control` | Artix-7 processing, STM32 control |
| 3 | `boards/03-camera` | Global-shutter sensor, M12 lens |
| 4 | `boards/04-ir-led` | Pulsed 850 nm illumination |

