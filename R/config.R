# =============================================================================
# config.R
# Shared paths, constants, and package loader for the R pipeline.
# All other R scripts source this file at the top.
# =============================================================================

# -----------------------------------------------------------------------------
# Packages
# Install once with: install.packages(c("tidyverse", "fixest", ...))
# After that, renv::snapshot() locks the versions.
# -----------------------------------------------------------------------------
suppressPackageStartupMessages({
  library(tidyverse)       # data manipulation + ggplot2
  library(fixest)          # fast TWFE estimation with feols()
  library(modelsummary)    # regression tables → .tex / .docx
  library(haven)           # read .dta Stata files if needed in R
  library(here)            # project-relative file paths
  library(glue)            # string interpolation
  library(scales)          # axis formatting in ggplot2
  library(patchwork)       # combine multiple ggplots
})

# -----------------------------------------------------------------------------
# Project root — using here() so paths work on any machine
# here() finds the project root by looking for .Rproj or .here
# -----------------------------------------------------------------------------
ROOT       <- here()
DATA_RAW   <- file.path(ROOT, "data", "raw")
DATA_PROC  <- file.path(ROOT, "data", "processed")
OUTPUT     <- file.path(ROOT, "output")
TABLES_DIR <- file.path(OUTPUT, "tables")
FIGURES_DIR <- file.path(OUTPUT, "figures")
LOGS_DIR   <- file.path(OUTPUT, "logs")

# Create output dirs if they don't exist
for (d in c(TABLES_DIR, FIGURES_DIR, LOGS_DIR)) {
  dir.create(d, recursive = TRUE, showWarnings = FALSE)
}

# -----------------------------------------------------------------------------
# Handoff file from Python
# -----------------------------------------------------------------------------
ANALYSIS_PANEL <- file.path(DATA_PROC, "analysis_panel.csv")

# -----------------------------------------------------------------------------
# Study parameters — keep in sync with python/config.py
# -----------------------------------------------------------------------------
TREATMENT_YEAR  <- 2009

OUTCOME_VARS    <- c(
  "attend",           # binary: currently enrolled
  "years_educ"        # continuous: years of schooling
)

CONFLICT_MEASURES <- c(
  "n_events",
  "n_fatalities",
  "log_fatalities",
  "ihs_fatalities"
)

# -----------------------------------------------------------------------------
# ggplot2 theme — applied globally
# All figures will use this theme unless overridden.
# -----------------------------------------------------------------------------
theme_thesis <- function() {
  theme_minimal(base_size = 12, base_family = "serif") +
    theme(
      panel.grid.minor   = element_blank(),
      panel.grid.major.x = element_blank(),
      axis.line          = element_line(colour = "grey40"),
      axis.ticks         = element_line(colour = "grey40"),
      plot.title         = element_text(face = "bold", size = 13),
      plot.subtitle      = element_text(colour = "grey40", size = 10),
      legend.position    = "bottom",
      legend.title       = element_blank(),
      strip.text         = element_text(face = "bold"),
    )
}

theme_set(theme_thesis())

# Consistent color palette
MALE_COLOR   <- "#2166AC"
FEMALE_COLOR <- "#D6604D"
TREAT_COLOR  <- "#D6604D"
CTRL_COLOR   <- "#2166AC"

# -----------------------------------------------------------------------------
# Helper: save a ggplot as both PDF and PNG
# -----------------------------------------------------------------------------
save_fig <- function(plot, name, width = 7, height = 5) {
  ggsave(file.path(FIGURES_DIR, paste0(name, ".pdf")),
         plot, width = width, height = height)
  ggsave(file.path(FIGURES_DIR, paste0(name, ".png")),
         plot, width = width, height = height, dpi = 300)
  message(glue("  Saved {name}.pdf / {name}.png"))
}

message("config.R loaded")
