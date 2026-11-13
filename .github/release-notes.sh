#!/usr/bin/env bash
set -euo pipefail

: "${RELEASE_TAG:?}" "${PACKAGE_NAME:?}" "${RELEASE_NOTES:?}"

mkdir -p build/release
url="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/releases/download/${RELEASE_TAG}"
prev="$(git describe --tags --abbrev=0 "${RELEASE_TAG}^" 2>/dev/null || true)"

{
  echo "## Downloads"
  echo
  echo "[Package](${url}/${PACKAGE_NAME}.zip) · [Schematic](${url}/woki-cam-schematic.pdf) · [3D collage](${url}/woki-cam-3d.png)"
  echo
  echo "Per-board outputs: \`power/\`, \`fpga_control/\`, \`camera/\`, \`ir_led/\` inside the zip."
  echo
  echo "## Preview"
  echo
  echo "<img src=\"${url}/woki-cam-3d.png\" alt=\"Board collage\" width=\"640\">"
  echo
  echo "## Changelog"
  echo
  if [[ -n "$prev" ]]; then
    git log --pretty=format:'- %s (`%h`)' "${prev}..HEAD"
  else
    git log --max-count=20 --pretty=format:'- %s (`%h`)'
  fi
  echo
} >"$RELEASE_NOTES"
