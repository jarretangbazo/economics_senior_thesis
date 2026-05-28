#!/usr/bin/env bash
# =============================================================================
# master.sh
# Master script: runs the full Python to R pipeline end to end.
#
# Usage:
#   bash master.sh              # run everything
#   bash master.sh --python     # Python stage only
#   bash master.sh --r          # R stage only
#
# Logs are saved to output/logs/run_YYYYMMDD_HHMMSS.log
# =============================================================================

set -euo pipefail   # stop on error, undefined vars, and pipe failures

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
PROJECT_ROOT="$HOME/Projects/economics_senior_thesis"
PYTHON_DIR="$PROJECT_ROOT/python"
R_DIR="$PROJECT_ROOT/R"
LOG_DIR="$PROJECT_ROOT/output/logs"

mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/run_${TIMESTAMP}.log"

# Redirect all output to log file AND terminal
exec > >(tee -a "$LOG_FILE") 2>&1

echo "============================================================"
echo " Education Under Fire — Full Pipeline"
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
# Stage 1: Python
# -----------------------------------------------------------------------------
if [ "$RUN_PYTHON" = true ]; then
  echo ""
  echo "=== Stage 1: Python pipeline ==================================="
  cd "$PYTHON_DIR"

  echo "[1/5] Cleaning ACLED data..."
  python 01_acled_clean.py

  echo "[2/5] Cleaning DHS data..."
  python 02_dhs_clean.py

  echo "[3/5] Geospatial merge..."
  python 03_geospatial_merge.py

  echo "[4/5] Building conflict exposure measures..."
  python 04_conflict_exposure.py

  echo "[5/5] Assembling analysis panel..."
  python 05_panel_merge.py

  PANEL="$PROJECT_ROOT/data/processed/analysis_panel.csv"
  if [ ! -f "$PANEL" ]; then
    echo "ERROR: analysis_panel.csv not found. Python pipeline may have failed."
    exit 1
  fi
  echo "analysis_panel.csv confirmed."
  cd "$PROJECT_ROOT"
fi

# -----------------------------------------------------------------------------
# Stage 2: R
# -----------------------------------------------------------------------------
if [ "$RUN_R" = true ]; then
  echo ""
  echo "=== Stage 2: R pipeline ========================================"
  cd "$R_DIR"

  echo "[1/6] Descriptive statistics..."
  Rscript 01_describe.R

  echo "[2/6] Pre-trends check..."
  Rscript 02_pretrends.R

  echo "[3/6] Main DiD estimation..."
  Rscript 03_main_did.R

  echo "[4/6] Event study..."
  Rscript 04_event_study.R

  echo "[5/6] Robustness checks..."
  Rscript 05_robustness.R

  echo "[6/6] Exporting tables and figures..."
  Rscript 06_tables_figures.R

  cd "$PROJECT_ROOT"
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
