# =============================================================================
# 03_main_did.R
# Main two-way fixed effects (TWFE) DiD estimation.
#
# Input:  data/processed/analysis_panel.csv
# Output: output/tables/table_main_did.tex
#
# Model: Y_ilt = alpha_l + gamma_t + beta*(Treated_l × Post_t) + X'delta + e_ilt
#   where l = LGA, t = survey year
#   alpha_l = LGA fixed effects
#   gamma_t = survey-year fixed effects
#   beta    = DiD estimator (the main coefficient of interest)
# =============================================================================

source(here::here("R", "config.R"))

# =============================================================================
# 1. Load
# =============================================================================
# panel <- read_csv(ANALYSIS_PANEL, show_col_types = FALSE)
# message(glue("Panel: {nrow(panel):,} observations"))

# =============================================================================
# 2. Main TWFE models
# =============================================================================
# fixest::feols() is the fastest and most flexible option for TWFE.
# The | lga + survey_year syntax absorbs both sets of fixed effects.
# cluster = ~lga clusters standard errors at the LGA level.

# -- Model 1: No controls (baseline) -----------------------------------------
# mod1 <- feols(
#   attend ~ treated_x_post | lga + survey_year,
#   data    = panel,
#   cluster = ~lga
# )

# -- Model 2: Add individual controls ----------------------------------------
# mod2 <- feols(
#   attend ~ treated_x_post + male + age + urban + wealth_index |
#            lga + survey_year,
#   data    = panel,
#   cluster = ~lga
# )

# -- Model 3: Years of schooling outcome -------------------------------------
# mod3 <- feols(
#   years_educ ~ treated_x_post + male + age + urban + wealth_index |
#                lga + survey_year,
#   data    = panel,
#   cluster = ~lga
# )

# =============================================================================
# 3. Inspect results
# =============================================================================
# etable(mod1, mod2, mod3)   # fixest's built-in table printer

# Quick coefficient check:
# coef(mod2)["treated_x_post"]   # DiD estimate
# confint(mod2)["treated_x_post",]  # 95% CI

# =============================================================================
# 4. Export table
# =============================================================================
# modelsummary(
#   list("Attendance (1)" = mod1,
#        "Attendance (2)" = mod2,
#        "Years Educ (3)" = mod3),
#   coef_rename  = c("treated_x_post" = "Treated × Post"),
#   coef_omit    = "^(?!treated_x_post)",  # show only the DiD coef + controls
#   gof_map      = c("nobs", "r.squared", "FE: lga", "FE: survey_year"),
#   stars        = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
#   title        = "Main DiD Estimates: Effect of Boko Haram Conflict on Education",
#   notes        = "Standard errors clustered at the LGA level. LGA and survey-year FE included.",
#   output       = file.path(TABLES_DIR, "table_main_did.tex")
# )
# message("Saved table_main_did.tex")

message("[TODO] Uncomment steps above once analysis_panel.csv is ready.")
