# =============================================================================
# 04_event_study.R
# Event study: estimate year-by-year treatment effects to visualise dynamics
# and provide further evidence on parallel pre-trends.
#
# Input:  data/processed/analysis_panel.csv
# Output: output/figures/fig_event_study.pdf
# =============================================================================

source(here::here("R", "config.R"))

# =============================================================================
# 1. Load
# =============================================================================
# panel <- read_csv(ANALYSIS_PANEL, show_col_types = FALSE)

# =============================================================================
# 2. Event study regression
# =============================================================================
# The i() function in fixest creates dummies for each year interacted with
# treatment status. The reference year should be the year before treatment (t-1).

# -- Set reference year (year before treatment) --------------------------------
# REF_YEAR <- TREATMENT_YEAR - 1

# mod_es <- feols(
#   attend ~ i(survey_year, treated, ref = REF_YEAR) + male + age + urban |
#            lga + survey_year,
#   data    = panel,
#   cluster = ~lga
# )

# summary(mod_es)

# =============================================================================
# 3. Extract coefficients and CIs for plotting
# =============================================================================
# iplot() from fixest can do this automatically, but building it manually
# gives you more control over the final figure.

# es_coefs <- broom::tidy(mod_es, conf.int = TRUE) %>%
#   filter(str_detect(term, "survey_year::")) %>%
#   mutate(
#     year = as.integer(str_extract(term, "\\d{4}")),
#     pre  = year < TREATMENT_YEAR
#   ) %>%
#   # Add the reference year manually (coefficient = 0 by construction)
#   bind_rows(tibble(year = REF_YEAR, estimate = 0, conf.low = 0, conf.high = 0,
#                    pre = TRUE))

# =============================================================================
# 4. Plot
# =============================================================================
# fig_es <- ggplot(es_coefs, aes(x = year, y = estimate)) +
#   geom_hline(yintercept = 0, colour = "grey60", linetype = "dashed") +
#   geom_vline(xintercept = TREATMENT_YEAR - 0.5, colour = "grey60",
#              linetype = "dashed") +
#   geom_ribbon(aes(ymin = conf.low, ymax = conf.high), alpha = 0.15,
#               fill = TREAT_COLOR) +
#   geom_line(colour = TREAT_COLOR, linewidth = 0.9) +
#   geom_point(aes(shape = pre), colour = TREAT_COLOR, size = 2.5) +
#   scale_shape_manual(values = c("TRUE" = 16, "FALSE" = 17), guide = "none") +
#   annotate("text", x = TREATMENT_YEAR - 0.6, y = Inf,
#            label = "Pre-treatment", hjust = 1, vjust = 1.3,
#            size = 3, colour = "grey50") +
#   annotate("text", x = TREATMENT_YEAR + 0.6, y = Inf,
#            label = "Post-treatment", hjust = 0, vjust = 1.3,
#            size = 3, colour = "grey50") +
#   labs(
#     title    = "Event Study: Effect of Boko Haram Conflict on School Attendance",
#     subtitle = "Treated × year coefficients relative to year t-1 (95% CI shaded)",
#     x = NULL, y = "DiD Coefficient"
#   )
#
# save_fig(fig_es, "fig_event_study")

message("[TODO] Uncomment steps above once analysis_panel.csv is ready.")
