#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
SERVICE="${2:-}"

if [[ -z "$ACTION" ]]; then
  echo "ERROR: acción obligatoria"
  exit 1
fi

if [[ "$ACTION" == "list" ]]; then
  systemctl list-units --type=service --all --no-pager --no-legend | awk '{print $1}' | while read -r service; do
    [[ -z "$service" ]] && continue
    state="$(systemctl is-active "$service" 2>/dev/null || true)"
    echo "${service}|${state}"
  done
  exit 0
fi

if [[ "$ACTION" == "start" || "$ACTION" == "stop" || "$ACTION" == "restart" ]]; then
  if [[ -z "$SERVICE" ]]; then
    echo "ERROR: servicio obligatorio"
    exit 1
  fi

  if [[ "$SERVICE" == *"/"* || "$SERVICE" == *";"* || "$SERVICE" == *"|"* || "$SERVICE" == *"&"* ]]; then
    echo "ERROR: nombre de servicio no permitido"
    exit 1
  fi

  sudo /usr/bin/systemctl "$ACTION" "$SERVICE"
  state="$(systemctl is-active "$SERVICE" 2>/dev/null || true)"
  echo "${SERVICE}|${state}"
  exit 0
fi

echo "ERROR: acción no válida"
exit 1
