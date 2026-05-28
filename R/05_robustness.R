# =============================================================================
# 05_robustness.R
# Robustness checks for the main DiD results.
#
# Input:  data/processed/analysis_panel.csv
# Output: output/tables/table_robustness.tex
#
# Checks included:
#   (1) Alternative conflict measures (log, IHS, event count)
#   (2) Alternative treatment thresholds (median vs top quartile)
#   (3) Restrict to northern states only
#   (4) Drop LGAs near the border (possible spillovers)
# =============================================================================

source(here::here("R", "config.R"))

# =============================================================================
# 1. Load
# =============================================================================
# panel <- read_csv(ANALYSIS_PANEL, show_col_types = FALSE)

# =============================================================================
# 2. Baseline (replicate from 03_main_did.R for comparison)
# =============================================================================
# mod_baseline <- feols(
#   attend ~ treated_x_post + male + age + urban + wealth_index |
#            lga + survey_year,
#   data    = panel,
#   cluster = ~lga
# )

# =============================================================================
# 3. Alternative conflict measures
# =============================================================================
# -- IHS-transformed fatalities -----------------------------------------------
# panel <- panel %>%
#   mutate(
#     treated_ihs_x_post = ihs_fatalities * post,   # continuous treatment
#   )

# mod_ihs <- feols(
#   attend ~ treated_ihs_x_post + male + age + urban + wealth_index |
#            lga + survey_year,
#   data    = panel,
#   cluster = ~lga
# )

# -- Event count as treatment -------------------------------------------------
# panel <- panel %>%
#   mutate(treated_events_x_post = n_events * post)

# mod_events <- feols(
#   attend ~ treated_events_x_post + male + age + urban + wealth_index |
#            lga + survey_year,
#   data    = panel,
#   cluster = ~lga
# )

# =============================================================================
# 4. Restrict to northern states only
# =============================================================================
# NORTH_STATES defined in config.R
# panel_north <- panel %>% filter(state %in% NORTH_STATES)

# mod_north <- feols(
#   attend ~ treated_x_post + male + age + urban + wealth_index |
#            lga + survey_year,
#   data    = panel_north,
#   cluster = ~lga
# )

# =============================================================================
# 5. Export robustness table
# =============================================================================
# modelsummary(
#   list(
#     "Baseline"       = mod_baseline,
#     "IHS fatalities" = mod_ihs,
#     "Event count"    = mod_events,
#     "North only"     = mod_north
#   ),
#   coef_rename = c(
#     "treated_x_post"       = "Treated × Post (binary)",
#     "treated_ihs_x_post"   = "IHS Fatalities × Post",
#     "treated_events_x_post" = "Event Count × Post"
#   ),
#   stars   = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
#   title   = "Robustness Checks",
#   notes   = "Dep. var.: school attendance. Clustered SEs. LGA + year FE throughout.",
#   output  = file.path(TABLES_DIR, "table_robustness.tex")
# )
# message("Saved table_robustness.tex")

message("[TODO] Uncomment steps above once analysis_panel.csv is ready.")
