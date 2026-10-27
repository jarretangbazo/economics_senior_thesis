#!/usr/bin/env bash
# =============================================================================
# master.sh
# Runs the full pipeline end to end: Python notebooks (01–02), then R (03–05).
#
# Usage (from anywhere):
#   bash code/master.sh              # run everything
#   bash code/master.sh --python     # notebooks only
#   bash code/master.sh --r          # R scripts only
#
# Notebooks are executed in place, so their saved outputs reflect the latest run.
# Logs are saved to output/logs/run_YYYYMMDD_HHMMSS.log
# =============================================================================

set -euo pipefail   # stop on error, undefined vars, and pipe failures

# -----------------------------------------------------------------------------
# Configuration — paths are resolved from this script's location
# -----------------------------------------------------------------------------
CODE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$CODE_DIR")"
LOG_DIR="$PROJECT_ROOT/output/logs"

# Use the project virtualenv if it exists, otherwise whatever jupyter is on PATH
if [ -x "$PROJECT_ROOT/.venv/bin/jupyter" ]; then
  JUPYTER="$PROJECT_ROOT/.venv/bin/jupyter"
else
  JUPYTER="jupyter"
fi

mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/run_$(date +"%Y%m%d_%H%M%S").log"

# Send all output to the log file AND the terminal
exec > >(tee -a "$LOG_FILE") 2>&1

echo "============================================================"
echo " Education Under Fire — Pipeline"
echo " Started: $(date)"
echo " Log: $LOG_FILE"
echo "============================================================"

# -----------------------------------------------------------------------------
# Parse arguments
# -----------------------------------------------------------------------------
RUN_PYTHON=true
RUN_R=true

for arg in "$@"; do
  case $arg in
    --python) RUN_R=false ;;
    --r)      RUN_PYTHON=false ;;
    *) echo "Unknown argument: $arg"; exit 1 ;;
  esac
done

# -----------------------------------------------------------------------------
# Stage 1: Python notebooks
# -----------------------------------------------------------------------------
NOTEBOOKS=(
  "01_dhs_clean:Cleaning DHS adult data"
  "02_war_exposure:Building civil war exposure"
)

if [ "$RUN_PYTHON" = true ]; then
  echo ""
  echo "=== Stage 1: Python notebooks =================================="
  i=1
  for entry in "${NOTEBOOKS[@]}"; do
    nb="${entry%%:*}"
    echo "[$i/${#NOTEBOOKS[@]}] ${entry#*:}..."
    "$JUPYTER" nbconvert --to notebook --execute --inplace "$CODE_DIR/$nb.ipynb" --log-level=WARN
    i=$((i + 1))
  done

  if [ ! -f "$PROJECT_ROOT/data/processed/analysis_war.csv" ]; then
    echo "ERROR: analysis_war.csv not found. Python stage may have failed."
    exit 1
  fi
  echo "analysis_war.csv confirmed."
fi

# -----------------------------------------------------------------------------
# Stage 2: R
# Run from the project root so .Rprofile activates renv.
# -----------------------------------------------------------------------------
R_SCRIPTS=(
  "03_descriptives:Descriptive statistics"
  "04_main_results:Main estimates and event study"
  "05_robustness:Robustness, placebo and heterogeneity"
)

if [ "$RUN_R" = true ]; then
  echo ""
  echo "=== Stage 2: R ================================================="
  cd "$PROJECT_ROOT"
  i=1
  for entry in "${R_SCRIPTS[@]}"; do
    script="${entry%%:*}"
    echo "[$i/${#R_SCRIPTS[@]}] ${entry#*:}..."
    Rscript "code/$script.R"
    i=$((i + 1))
  done
fi

# -----------------------------------------------------------------------------
# Done
# -----------------------------------------------------------------------------
echo ""
echo "============================================================"
echo " Pipeline complete: $(date)"
echo " Outputs: $PROJECT_ROOT/output/"
echo " Log:     $LOG_FILE"
echo "============================================================"
