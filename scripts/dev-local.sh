#!/usr/bin/env bash
# Pornește app devis + site static builduit (local).
# Usage:
#   ./scripts/dev-local.sh [ro|fr]     — build + serve (default: ro)
#   ./scripts/dev-local.sh stop        — oprește procesele pe 3100 și 8080
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP_DIR="$ROOT/../polistibrick-devis-app"
PORT_SITE="${PORT_SITE:-8080}"
PORT_DEVIS="${PORT_DEVIS:-3100}"

port_in_use() {
  lsof -i ":$1" -sTCP:LISTEN -t >/dev/null 2>&1
}

kill_port() {
  local pids
  pids=$(lsof -i ":$1" -sTCP:LISTEN -t 2>/dev/null || true)
  if [[ -n "$pids" ]]; then
    echo "→ Oprire port $1 (pid: $pids)…"
    kill $pids 2>/dev/null || true
    sleep 1
  fi
}

if [[ "${1:-}" == "stop" ]]; then
  kill_port "$PORT_DEVIS"
  kill_port "$PORT_SITE"
  echo "✓ Porturi eliberate ($PORT_DEVIS, $PORT_SITE)."
  exit 0
fi

COUNTRY="${1:-ro}"

if [[ ! -d "$APP_DIR" ]]; then
  echo "❌ Nu găsesc app devis: $APP_DIR"
  echo "   Așteptat sibling: polistibrick-devis-app/"
  exit 1
fi

echo "→ Build site ($COUNTRY)…"
python3 "$ROOT/build/build.py" "$COUNTRY"

DEVIS_PID=""
DEVIS_STARTED=0
SITE_PID=""
SITE_STARTED=0

cleanup() {
  echo ""
  if [[ "$DEVIS_STARTED" -eq 1 && -n "$DEVIS_PID" ]]; then
    echo "→ Oprire app devis (pid $DEVIS_PID)…"
    kill "$DEVIS_PID" 2>/dev/null || true
  fi
  if [[ "$SITE_STARTED" -eq 1 && -n "$SITE_PID" ]]; then
    echo "→ Oprire site (pid $SITE_PID)…"
    kill "$SITE_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

if port_in_use "$PORT_DEVIS"; then
  echo "⚠ Port $PORT_DEVIS ocupat — app devis rulează deja (OK, o folosim)."
else
  echo "→ Pornesc app devis (port $PORT_DEVIS)…"
  (cd "$APP_DIR" && npm run dev) &
  DEVIS_PID=$!
  DEVIS_STARTED=1
  sleep 2
fi

OFFER_PATH="oferta/"
[[ "$COUNTRY" == "fr" ]] && OFFER_PATH="devis/"

# Găsește port liber pentru site dacă e ocupat
SITE_REQUESTED=$PORT_SITE
while port_in_use "$PORT_SITE"; do
  if [[ "$PORT_SITE" -eq "$SITE_REQUESTED" ]]; then
    echo "⚠ Port $PORT_SITE ocupat — încerc alt port…"
  fi
  PORT_SITE=$((PORT_SITE + 1))
  if [[ "$PORT_SITE" -gt 8099 ]]; then
    echo "❌ Nu găsesc port liber pentru site ($SITE_REQUESTED–8099)."
    echo "   Rulează: ./scripts/dev-local.sh stop"
    exit 1
  fi
done

echo ""
echo "✓ Site:  http://localhost:$PORT_SITE/$OFFER_PATH"
echo "✓ Devis: http://localhost:$PORT_DEVIS"
echo "  Ctrl+C oprește doar ce a pornit acest script."
echo "  ./scripts/dev-local.sh stop  — eliberează porturile 3100 + 8080"
echo ""

cd "$ROOT/build/$COUNTRY"
python3 -m http.server "$PORT_SITE" &
SITE_PID=$!
SITE_STARTED=1
wait "$SITE_PID"
