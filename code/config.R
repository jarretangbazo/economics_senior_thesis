# =============================================================================
# config.R
# Shared paths, constants, helpers and package loader for the R scripts (03–05).
# Every R script sources this file at the top.
# =============================================================================

# -----------------------------------------------------------------------------
# Packages (versions locked in renv.lock; restore with renv::restore())
# -----------------------------------------------------------------------------
suppressPackageStartupMessages({
  library(tidyverse)       # data manipulation + ggplot2
  library(fixest)          # fixed effects regressions with feols()
  library(modelsummary)    # regression tables -> .tex
  library(here)            # project-relative file paths
  library(glue)            # string interpolation
  library(scales)          # axis formatting in ggplot2
})

# -----------------------------------------------------------------------------
# Paths — here() finds the project root from the .Rproj file or .git folder
# -----------------------------------------------------------------------------
ROOT        <- here()
DATA_PROC   <- file.path(ROOT, "data", "processed")
OUTPUT      <- file.path(ROOT, "output")
TABLES_DIR  <- file.path(OUTPUT, "tables")
FIGURES_DIR <- file.path(OUTPUT, "figures")

for (d in c(TABLES_DIR, FIGURES_DIR)) {
  dir.create(d, recursive = TRUE, showWarnings = FALSE)
}

# Write plain numbers in .tex tables (no siunitx \num{} wrappers)
options(modelsummary_format_numeric_latex = "plain")

# Handoff file from the Python notebooks
ANALYSIS_FILE <- file.path(DATA_PROC, "analysis_war.csv")

# -----------------------------------------------------------------------------
# Study parameters — keep in sync with code/config.py
# -----------------------------------------------------------------------------
WAR_YEARS <- 1967:1969
REF_COHORT <- 1945                # last 5-year cohort that finished school before the war

OUTCOMES <- c(
  years_educ        = "Years of schooling",
  completed_primary = "Completed primary"
)

# Baseline specification: state, birth-year and survey-wave FE, sex control,
# SEs clustered by state. Inference also uses a permutation test, because
# only 5 states are treated.
CONTROLS <- "male"
FE       <- "state + birth_year + survey_year"
CLUSTER  <- ~state
N_PERM   <- 1000                  # permutation draws

COEF_LABELS <- c(
  war_x_cohort   = "War region × School-age during war",
  war_x_years    = "War region × War years at school age",
  wider_x_cohort = "Wider war region × School-age during war"
)

GOF_MAP <- tribble(
  ~raw,        ~clean,        ~fmt,
  "nobs",      "Observations", 0,
  "r.squared", "R²",           3
)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
load_analysis <- function() {
  read_csv(ANALYSIS_FILE, show_col_types = FALSE)
}

# Build "y ~ rhs | fe" from strings
reg_formula <- function(y, rhs, fe = FE) {
  as.formula(glue("{y} ~ {rhs} | {fe}"))
}

# Permutation test for a "region x cohort" coefficient.
# Re-assigns the treated region to random sets of states of the same size,
# re-estimates, and reports the share of placebo estimates at least as large
# in absolute value as the real one.
#   region_var:   0/1 column marking the treated states
#   cohort_var:   0/1 or count column marking exposed cohorts
#   region_trend: also give the (real or placebo) region its own linear cohort trend
permutation_test <- function(data, y, region_var, cohort_var, rhs_extra = CONTROLS,
                             fe = FE, region_trend = FALSE, weights = NULL, n = N_PERM, seed = 1967) {
  treated_states <- unique(data$state[data[[region_var]] == 1])
  all_states     <- unique(data$state)

  estimate <- function(fake_states) {
    d <- mutate(data,
                perm_region = as.integer(state %in% fake_states),
                perm_x      = perm_region * .data[[cohort_var]],
                perm_trend  = perm_region * (birth_year - 1950))
    rhs <- glue("perm_x + {rhs_extra}{if (region_trend) ' + perm_trend' else ''}")
    coef(feols(reg_formula(y, rhs, fe), data = d, weights = weights, notes = FALSE))[["perm_x"]]
  }

  actual  <- estimate(treated_states)
  placebo <- withr::with_seed(seed, map_dbl(seq_len(n), \(i) estimate(sample(all_states, length(treated_states)))))

  list(
    estimate = actual,
    p_value  = (1 + sum(abs(placebo) >= abs(actual))) / (1 + n),
    placebo  = placebo
  )
}

# -----------------------------------------------------------------------------
# ggplot2 theme — applied globally
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
      strip.text         = element_text(face = "bold")
    )
}

theme_set(theme_thesis())

WAR_COLOR   <- "#B2182B"
PART_COLOR  <- "#F4A582"
REST_COLOR  <- "#2166AC"

# Save a ggplot as both PDF and PNG
save_fig <- function(plot, name, width = 7, height = 5) {
  ggsave(file.path(FIGURES_DIR, paste0(name, ".pdf")), plot, width = width, height = height)
  ggsave(file.path(FIGURES_DIR, paste0(name, ".png")), plot, width = width, height = height, dpi = 300)
  message(glue("  Saved {name}.pdf / {name}.png"))
}

message("config.R loaded")
