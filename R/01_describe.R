# =============================================================================
# 01_describe.R
# Summary statistics and descriptive figures.
#
# Input:  data/processed/analysis_panel.csv
# Output: output/tables/table_summary_stats.tex
#         output/figures/fig_outcomes_over_time.pdf
# =============================================================================

source(here::here("R", "config.R"))

# =============================================================================
# 1. Load
# =============================================================================
message("Loading analysis panel...")
# panel <- read_csv(ANALYSIS_PANEL, show_col_types = FALSE)
# message(glue("  Rows: {nrow(panel):,}  |  Columns: {ncol(panel)}"))

# =============================================================================
# 2. Summary statistics table
# =============================================================================
# modelsummary's datasummary_skim() gives a quick overview.
# For a publication-quality table, use datasummary().

# -- All variables at a glance ------------------------------------------------
# datasummary_skim(panel, output = "markdown")

# -- Formatted summary stats table -------------------------------------------
# Adjust the variable list to match your actual column names.
# summary_vars <- panel %>%
#   select(attend, years_educ,
#          n_events, n_fatalities, log_fatalities,
#          treated, post, male, urban, wealth_index)

# datasummary(
#   All(summary_vars) ~ N + Mean + SD + Min + Max,
#   data    = summary_vars,
#   title   = "Summary Statistics",
#   notes   = "Unit of observation: individual child. Source: DHS and ACLED.",
#   output  = file.path(TABLES_DIR, "table_summary_stats.tex")
# )
# message("  Saved table_summary_stats.tex")

# =============================================================================
# 3. Outcome trends over time (treated vs control)
# =============================================================================

# -- Collapse to year × treatment group means ---------------------------------
# trends <- panel %>%
#   group_by(survey_year, treated) %>%
#   summarise(
#     mean_attend    = mean(attend, na.rm = TRUE),
#     mean_years     = mean(years_educ, na.rm = TRUE),
#     .groups = "drop"
#   ) %>%
#   mutate(group = if_else(treated == 1, "Treated", "Control"))

# -- Plot: school attendance over time ----------------------------------------
# fig_attend <- ggplot(trends, aes(x = survey_year, y = mean_attend,
#                                  colour = group, linetype = group)) +
#   geom_line(linewidth = 0.9) +
#   geom_point(size = 2) +
#   geom_vline(xintercept = TREATMENT_YEAR, linetype = "dashed",
#              colour = "grey50", linewidth = 0.7) +
#   annotate("text", x = TREATMENT_YEAR + 0.1, y = Inf,
#            label = "Treatment\nyear", hjust = 0, vjust = 1.2,
#            size = 3, colour = "grey50") +
#   scale_colour_manual(values = c("Treated" = TREAT_COLOR, "Control" = CTRL_COLOR)) +
#   scale_y_continuous(labels = percent_format(accuracy = 1)) +
#   labs(title = "School Attendance Rate: Treated vs Control LGAs",
#        x = NULL, y = "Mean Attendance Rate") +
#   theme(legend.position = "bottom")
#
# save_fig(fig_attend, "fig_attendance_trends")

# -- Plot: years of schooling over time ----------------------------------------
# fig_years <- ggplot(trends, aes(x = survey_year, y = mean_years,
#                                 colour = group, linetype = group)) +
#   geom_line(linewidth = 0.9) +
#   geom_point(size = 2) +
#   geom_vline(xintercept = TREATMENT_YEAR, linetype = "dashed",
#              colour = "grey50", linewidth = 0.7) +
#   scale_colour_manual(values = c("Treated" = TREAT_COLOR, "Control" = CTRL_COLOR)) +
#   labs(title = "Mean Years of Schooling: Treated vs Control LGAs",
#        x = NULL, y = "Mean Years of Schooling") +
#   theme(legend.position = "bottom")
#
# save_fig(fig_years, "fig_years_educ_trends")

message("[TODO] Uncomment steps above once analysis_panel.csv is ready.")
