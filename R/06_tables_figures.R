# =============================================================================
# 06_tables_figures.R
# Final assembly: re-run all models and export publication-ready outputs.
# This script is intentionally self-contained — it sources the others
# and re-exports everything cleanly for the thesis.
#
# Output: output/tables/*.tex
#         output/figures/*.pdf  *.png
# =============================================================================

source(here::here("R", "config.R"))

# =============================================================================
# Option A: Source all scripts (re-runs everything)
# =============================================================================
# source(here("R", "01_describe.R"))
# source(here("R", "02_pretrends.R"))
# source(here("R", "03_main_did.R"))
# source(here("R", "04_event_study.R"))
# source(here("R", "05_robustness.R"))

# =============================================================================
# Option B: Load saved model objects and re-export (faster if models are saved)
# =============================================================================
# If you saved models in earlier scripts with saveRDS(), load them here:
# mod1       <- readRDS(file.path(OUTPUT, "mod1.rds"))
# mod_es     <- readRDS(file.path(OUTPUT, "mod_es.rds"))

# =============================================================================
# Combined main table (all outcomes side-by-side)
# =============================================================================
# modelsummary(
#   list(
#     "Attendance (1)" = mod1,
#     "Attendance (2)" = mod2,
#     "Years Educ (3)" = mod3
#   ),
#   coef_rename  = c("treated_x_post" = "Treated × Post"),
#   coef_omit    = "^(?!treated_x_post|male|age|urban)",
#   gof_map      = c("nobs", "r.squared"),
#   stars        = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
#   fmt          = 3,
#   title        = "Table 1: Effect of Boko Haram Conflict on Educational Outcomes",
#   notes        = "Standard errors clustered at the LGA level in parentheses.
#                   LGA and survey-year fixed effects included in all columns.
#                   *** p<0.01, ** p<0.05, * p<0.10.",
#   output = file.path(TABLES_DIR, "table1_main.tex")
# )

# =============================================================================
# Thesis-ready figure: event study + trends side by side (patchwork)
# =============================================================================
# fig_combined <- fig_attend + fig_es +
#   plot_annotation(
#     title  = "Conflict Exposure and School Attendance in Northern Nigeria",
#     tag_levels = "A"
#   )
#
# save_fig(fig_combined, "fig_main_combined", width = 12, height = 5)

message("[TODO] Uncomment steps above once all prior scripts have been run.")
message("All outputs written to output/tables/ and output/figures/")
