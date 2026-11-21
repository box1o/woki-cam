"""Shared board inventory for exports, previews and GitHub Actions."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARDS = (
    {"board": "power", "directory": "01-power", "label": "01 Power"},
    {"board": "fpga-control", "directory": "02-fpga-control", "label": "02 FPGA"},
    {"board": "camera", "directory": "03-camera", "label": "03 Camera"},
    {"board": "ir-led", "directory": "04-ir-led", "label": "04 IR LED"},
)


def board_file(board: dict[str, str], extension: str) -> Path:
    return ROOT / "boards" / board["directory"] / f"{board['board']}.{extension}"


if __name__ == "__main__":
    print(
        json.dumps(
            {
                "include": [
                    {
                        "board": board["board"],
                        "pcb": str(board_file(board, "kicad_pcb").relative_to(ROOT)),
                        "sch": str(board_file(board, "kicad_sch").relative_to(ROOT)),
                    }
                    for board in BOARDS
                ]
            }
        )
    )
