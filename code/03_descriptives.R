# =============================================================================
# 03_descriptives.R
# Summary statistics and schooling profiles by birth cohort and region.
#
# Input:  data/processed/analysis_war.csv
# Output: output/tables/table_summary_stats.tex
#         output/figures/fig_cohort_profiles.pdf / .png
# =============================================================================

source(here::here("code", "config.R"))

adults <- load_analysis()
main   <- filter(adults, main_sample == 1)
message(glue("Adults: {comma(nrow(adults))} | main sample: {comma(nrow(main))}"))

# =============================================================================
# 1. Summary statistics: the four cells of the difference-in-differences
#    (survey-weighted means, main sample)
# =============================================================================
summary_vars <- c(
  "Years of schooling" = "years_educ",
  "Completed primary"  = "completed_primary",
  "Male"               = "male",
  "Age at survey"      = "age",
  "Birth year"         = "birth_year"
)

cells <- main |>
  mutate(
    region = if_else(war_region == 1, "War region", "Rest of Nigeria"),
    cohort = if_else(school_age_war == 1, "School-age in war (1950-63)", "Before war (1935-49)")
  ) |>
  group_by(region, cohort) |>
  summarise(
    across(all_of(unname(summary_vars)), \(x) weighted.mean(x, weight)),
    People = n(),
    States = n_distinct(state),
    .groups = "drop"
  )

column_order <- c("War region: Before war (1935-49)", "War region: School-age in war (1950-63)",
                  "Rest of Nigeria: Before war (1935-49)", "Rest of Nigeria: School-age in war (1950-63)")

summary_table <- cells |>
  mutate(column = glue("{region}: {cohort}")) |>
  select(-region, -cohort) |>
  pivot_longer(-column, names_to = "variable") |>
  pivot_wider(names_from = column, values_from = value) |>
  mutate(
    variable = recode(variable, !!!setNames(names(summary_vars), summary_vars)),
    across(-variable, \(x) if_else(variable %in% c("People", "States", "Birth year"),
                                   comma(x, accuracy = 1, big.mark = ""), number(x, accuracy = 0.01)))
  ) |>
  select(Variable = variable, all_of(column_order))

datasummary_df(
  summary_table,
  title  = "Summary statistics by region and birth cohort (survey-weighted means)",
  notes  = glue("Adults in DHS 2003 and 2008 household rosters. War region: Abia, Anambra, Ebonyi, Enugu, Imo. ",
                "Rest of Nigeria excludes the partly exposed states (Akwa Ibom, Bayelsa, Cross River, Rivers, ",
                "Delta, Edo)."),
  output = file.path(TABLES_DIR, "table_summary_stats.tex")
)
print(summary_table)

# Raw difference-in-differences in years of schooling
raw <- cells |> select(region, cohort, years_educ) |> pivot_wider(names_from = cohort, values_from = years_educ)
raw_change <- raw[[3]] - raw[[2]]
message(glue("Raw DiD in years of schooling (war region change minus rest change): ",
             "{number(raw_change[raw$region == 'War region'] - raw_change[raw$region == 'Rest of Nigeria'], accuracy = 0.01)}"))

# =============================================================================
# 2. Schooling by 5-year birth cohort and region group
# =============================================================================
profiles <- adults |>
  group_by(cohort5, region_group) |>
  summarise(across(all_of(names(OUTCOMES)), \(x) weighted.mean(x, weight)), .groups = "drop") |>
  pivot_longer(all_of(names(OUTCOMES)), names_to = "outcome") |>
  mutate(
    outcome      = factor(OUTCOMES[outcome], levels = OUTCOMES),
    region_group = factor(region_group, levels = c("War region", "Partly exposed", "Rest of Nigeria"))
  )

fig_profiles <- ggplot(profiles, aes(cohort5 + 2, value, colour = region_group)) +
  annotate("rect", xmin = 1950, xmax = 1964, ymin = -Inf, ymax = Inf, fill = "grey85", alpha = 0.5) +
  geom_line(linewidth = 0.8) +
  geom_point(size = 2) +
  facet_wrap(~outcome, scales = "free_y") +
  scale_colour_manual(values = c("War region" = WAR_COLOR, "Partly exposed" = PART_COLOR,
                                 "Rest of Nigeria" = REST_COLOR)) +
  labs(
    x = "Year of birth (5-year cohorts)", y = NULL,
    title = "Completed schooling by birth cohort and region",
    subtitle = "Survey-weighted means; shaded: cohorts of school age during the 1967-70 war"
  )

save_fig(fig_profiles, "fig_cohort_profiles", width = 9, height = 4.5)
