# =============================================================================
# 04_main_results.R
# Main difference-in-differences estimates and the cohort event study.
#
#   y_isc = b * WarRegion_s x SchoolAgeDuringWar_c + state FE + birth-year FE
#           + survey-wave FE + male + e_isc
#
# Columns per outcome: (1) binary exposure, (2) adds war-region-specific
# linear cohort trends, (3) intensity: number of war years at school age.
# Inference: SEs clustered by state and a permutation test that re-assigns the
# war region to random sets of 5 states (only 5 states are treated, so
# clustered SEs alone are unreliable).
#
# Input:  data/processed/analysis_war.csv
# Output: output/tables/table_main_results.tex
#         output/tables/table_event_study.tex
#         output/figures/fig_event_study.pdf / .png
#         output/figures/fig_permutation.pdf / .png
# =============================================================================

source(here::here("code", "config.R"))

adults <- load_analysis()
main   <- filter(adults, main_sample == 1) |>
  mutate(war_x_trend = war_region * (birth_year - 1950))

# =============================================================================
# 1. Main table
# =============================================================================
specs <- list()
for (y in names(OUTCOMES)) {
  specs[[glue("{OUTCOMES[[y]]}: binary")]] <- list(y = y, cohort = "school_age_war",   term = "war_x_cohort", trend = FALSE)
  specs[[glue("{OUTCOMES[[y]]}: trend")]]  <- list(y = y, cohort = "school_age_war",   term = "war_x_cohort", trend = TRUE)
  specs[[glue("{OUTCOMES[[y]]}: years")]]  <- list(y = y, cohort = "war_school_years", term = "war_x_years",  trend = FALSE)
}

models <- map(specs, \(s) {
  rhs <- glue("{s$term} + {CONTROLS}{if (s$trend) ' + war_x_trend' else ''}")
  feols(reg_formula(s$y, rhs), data = main, cluster = CLUSTER)
})
numbered <- set_names(models, glue("({seq_along(models)})"))

message(glue("Running permutation tests ({N_PERM} draws per column)..."))
perms <- map(specs, \(s) permutation_test(main, s$y, "war_region", s$cohort, region_trend = s$trend))

extra_rows <- tibble(
  term = c("Permutation p-value", "War-region cohort trend", "Treated states", "States"),
  !!!set_names(map(seq_along(specs), \(i) c(
    number(perms[[i]]$p_value, accuracy = 0.001),
    if_else(specs[[i]]$trend, "Yes", "No"),
    "5",
    as.character(n_distinct(main$state))
  )), names(numbered))
)

modelsummary(
  numbered,
  coef_map = COEF_LABELS[c("war_x_cohort", "war_x_years")],
  gof_map  = GOF_MAP,
  add_rows = extra_rows,
  stars    = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  title    = "Effect of the Nigerian Civil War on completed schooling",
  notes    = glue("Columns 1-3: years of schooling; 4-6: completed primary. Adults born 1935-1963 in DHS 2003 and ",
                  "2008; partly exposed states excluded. State, birth-year and survey-wave FE and a sex control. ",
                  "SEs clustered by state in parentheses (stars use these). Permutation p-value: share of {N_PERM} ",
                  "random 5-state placebo regions with an estimate at least as large in absolute value."),
  output   = file.path(TABLES_DIR, "table_main_results.tex")
)
modelsummary(numbered, coef_map = COEF_LABELS[c("war_x_cohort", "war_x_years")], gof_map = GOF_MAP,
             add_rows = extra_rows, output = "markdown") |> print()

# Permutation distribution for the headline column
perm_plot_data <- tibble(placebo = perms[[1]]$placebo)
fig_perm <- ggplot(perm_plot_data, aes(placebo)) +
  geom_histogram(bins = 40, fill = "grey70", colour = "white") +
  geom_vline(xintercept = perms[[1]]$estimate, colour = WAR_COLOR, linewidth = 1) +
  labs(
    x = "Estimate for a random 5-state placebo region", y = "Count",
    title = "Permutation test: years of schooling",
    subtitle = glue("Red line: actual war region (p = {number(perms[[1]]$p_value, accuracy = 0.001)})")
  )
save_fig(fig_perm, "fig_permutation", width = 7, height = 4)

# =============================================================================
# 2. Cohort event study: war-region gap by 5-year birth cohort, relative to
#    the 1945-49 cohort (the last to finish school before the war).
#    All cohorts 1935-1975; partly exposed states excluded.
# =============================================================================
es_data <- filter(adults, partly_exposed == 0)

es_models <- map(names(OUTCOMES), \(y) {
  feols(reg_formula(y, glue("i(cohort5, war_region, ref = {REF_COHORT}) + {CONTROLS}")),
        data = es_data, cluster = CLUSTER)
}) |>
  set_names(OUTCOMES)

modelsummary(
  es_models,
  coef_rename = \(x) str_replace(x, "cohort5::(\\d{4}):war_region", "War region × born \\1-"),
  gof_map  = GOF_MAP,
  stars    = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  title    = glue("Cohort event study: war-region schooling gap by birth cohort (reference: born {REF_COHORT}-{REF_COHORT + 4})"),
  notes    = "State, birth-year and survey-wave FE and a sex control. SEs clustered by state.",
  output   = file.path(TABLES_DIR, "table_event_study.tex")
)

es_coefs <- imap_dfr(es_models, \(m, outcome) {
  ct <- coeftable(m)
  ct <- ct[grepl("^cohort5::", rownames(ct)), , drop = FALSE]
  tibble(
    outcome  = factor(outcome, levels = OUTCOMES),
    cohort   = as.integer(str_extract(rownames(ct), "\\d{4}")),
    estimate = ct[, "Estimate"],
    se       = ct[, "Std. Error"]
  ) |>
    add_row(outcome = outcome, cohort = REF_COHORT, estimate = 0, se = 0)
}) |>
  mutate(
    ci_low  = estimate - qt(0.975, n_distinct(es_data$state) - 1) * se,
    ci_high = estimate + qt(0.975, n_distinct(es_data$state) - 1) * se
  )

fig_es <- ggplot(es_coefs, aes(cohort + 2, estimate)) +
  annotate("rect", xmin = 1950, xmax = 1964, ymin = -Inf, ymax = Inf, fill = "grey85", alpha = 0.5) +
  geom_hline(yintercept = 0, colour = "grey50") +
  geom_errorbar(aes(ymin = ci_low, ymax = ci_high), width = 1.2, colour = WAR_COLOR) +
  geom_point(size = 2.5, colour = WAR_COLOR) +
  facet_wrap(~outcome, scales = "free_y") +
  labs(
    x = "Year of birth (5-year cohorts)", y = glue("War-region gap relative to born {REF_COHORT}-{REF_COHORT + 4}"),
    title = "Cohort event study: the Nigerian Civil War and schooling",
    subtitle = "Shaded: cohorts of school age during the war. 95% CIs, SEs clustered by state"
  )

save_fig(fig_es, "fig_event_study", width = 9, height = 4.5)
