# =============================================================================
# 02_pretrends.R
# Parallel trends test: check that treated and control LGAs moved together
# before the Boko Haram insurgency intensified in 2009.
#
# Input:  data/processed/analysis_panel.csv
# Output: output/figures/fig_pretrends.pdf
#         output/tables/table_pretrends.tex
# =============================================================================

source(here::here("R", "config.R"))

# =============================================================================
# 1. Load
# =============================================================================
# panel <- read_csv(ANALYSIS_PANEL, show_col_types = FALSE)

# =============================================================================
# 2. Visual parallel trends check
# =============================================================================
# A simple graph showing outcome trends for treated and control groups,
# restricted to the pre-treatment period, is often the most convincing test.

# pre <- panel %>% filter(survey_year < TREATMENT_YEAR)

# trends_pre <- pre %>%
#   group_by(survey_year, treated) %>%
#   summarise(mean_attend = mean(attend, na.rm = TRUE), .groups = "drop") %>%
#   mutate(group = if_else(treated == 1, "Treated", "Control"))

# fig_pre <- ggplot(trends_pre, aes(x = survey_year, y = mean_attend,
#                                    colour = group, linetype = group)) +
#   geom_line(linewidth = 0.9) +
#   geom_point(size = 2.5) +
#   scale_colour_manual(values = c("Treated" = TREAT_COLOR, "Control" = CTRL_COLOR)) +
#   scale_y_continuous(labels = percent_format(accuracy = 1)) +
#   labs(title   = "Pre-Treatment Trends: School Attendance",
#        subtitle = "Parallel pre-trends support the DiD identifying assumption",
#        x = NULL, y = "Mean Attendance Rate") +
#   theme(legend.position = "bottom")

# save_fig(fig_pre, "fig_pretrends_visual")

# =============================================================================
# 3. Formal pre-trends test (regression-based)
# =============================================================================
# Regress the outcome on treated × year dummies for pre-treatment years.
# Under parallel trends, the coefficients on treated × year (pre) should be
# jointly zero.

# -- Restrict to pre-treatment period ----------------------------------------
# pre_formal <- panel %>%
#   filter(survey_year < TREATMENT_YEAR) %>%
#   mutate(year_fct = factor(survey_year))

# -- Run regression with LGA and year FE -------------------------------------
# The i() function in fixest creates interactions with a reference year.
# mod_pretrends <- feols(
#   attend ~ i(year_fct, treated, ref = "<reference year here>") |
#            lga + survey_year,
#   data    = pre_formal,
#   cluster = ~lga
# )

# summary(mod_pretrends)

# -- Test joint significance of pre-trend coefficients -----------------------
# wald(mod_pretrends, keep = "year_fct")   # p > 0.10 is reassuring

# -- Export table -------------------------------------------------------------
# modelsummary(
#   mod_pretrends,
#   title   = "Pre-Trends Test",
#   notes   = "Coefficients are treated × year interactions (pre-treatment only). Clustered SEs.",
#   output  = file.path(TABLES_DIR, "table_pretrends.tex")
# )

message("[TODO] Uncomment steps above once analysis_panel.csv is ready.")
