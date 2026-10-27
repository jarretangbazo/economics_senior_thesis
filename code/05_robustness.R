# =============================================================================
# 05_robustness.R
# Robustness of the main estimate (main table, columns 1 and 4), a placebo
# war, and men vs women. Every row reports the clustered SE and a
# permutation p-value.
#
# Input:  data/processed/analysis_war.csv
# Output: output/tables/table_robustness.tex
# =============================================================================

source(here::here("code", "config.R"))

adults <- load_analysis()
main   <- filter(adults, main_sample == 1)

samples <- list(
  main        = main,
  wider       = filter(adults, birth_year <= 1963),       # partly exposed states join the war region
  no_heaping  = filter(main, age_heaped == 0),
  wave_2003   = filter(main, survey_year == 2003),
  wave_2008   = filter(main, survey_year == 2008),
  pre_war     = filter(main, birth_year <= 1949),         # placebo: fake 1957-59 war, older cohorts only
  women       = filter(main, male == 0),
  men         = filter(main, male == 1)
)

robustness_specs <- tribble(
  ~section,           ~spec,                                     ~sample,      ~region,            ~cohort,              ~weighted,
  "Specification",    "Baseline",                                "main",       "war_region",       "school_age_war",     FALSE,
  "Specification",    "Wider war region (former Eastern Region and Mid-West)", "wider", "wider_war_region", "school_age_war", FALSE,
  "Specification",    "Drop ages ending in 0 or 5",              "no_heaping", "war_region",       "school_age_war",     FALSE,
  "Specification",    "DHS 2003 only",                           "wave_2003",  "war_region",       "school_age_war",     FALSE,
  "Specification",    "DHS 2008 only",                           "wave_2008",  "war_region",       "school_age_war",     FALSE,
  "Specification",    "Survey weights",                          "main",       "war_region",       "school_age_war",     TRUE,
  "Placebo",          "Fake war in 1957-59 (born 1935-49 only)", "pre_war",    "war_region",       "school_age_placebo", FALSE,
  "Heterogeneity",    "Women",                                   "women",      "war_region",       "school_age_war",     FALSE,
  "Heterogeneity",    "Men",                                     "men",        "war_region",       "school_age_war",     FALSE
)

message(glue("Running {nrow(robustness_specs) * length(OUTCOMES)} specifications with {N_PERM} permutations each..."))

robustness <- pmap_dfr(robustness_specs, \(section, spec, sample, region, cohort, weighted) {
  d <- mutate(samples[[sample]], treat = .data[[region]] * .data[[cohort]])
  w <- if (weighted) ~weight else NULL
  # Single-wave samples cannot include survey-wave FE; single-sex samples drop the sex control
  fe  <- if (n_distinct(d$survey_year) == 1) "state + birth_year" else FE
  rhs <- if (n_distinct(d$male) == 1) "1" else CONTROLS

  map_dfr(names(OUTCOMES), \(y) {
    m  <- feols(reg_formula(y, glue("treat + {rhs}"), fe), data = d, cluster = CLUSTER, weights = w)
    ct <- coeftable(m)
    perm <- permutation_test(d, y, region, cohort, rhs_extra = rhs, fe = fe, weights = w)
    tibble(section = section, spec = spec, outcome = OUTCOMES[[y]],
           estimate = ct["treat", "Estimate"], se = ct["treat", "Std. Error"], p = ct["treat", "Pr(>|t|)"],
           p_perm = perm$p_value, n = nobs(m))
  })
})

fmt_est <- function(estimate, se, p) {
  stars <- case_when(p < 0.01 ~ "***", p < 0.05 ~ "**", p < 0.1 ~ "*", TRUE ~ "")
  glue("{number(estimate, accuracy = 0.001)}{stars} ({number(se, accuracy = 0.001)})")
}

robustness_table <- robustness |>
  mutate(cell = fmt_est(estimate, se, p), p_perm = number(p_perm, accuracy = 0.001)) |>
  select(Section = section, Specification = spec, outcome, cell, p_perm) |>
  pivot_wider(names_from = outcome, values_from = c(cell, p_perm), names_glue = "{outcome} {.value}") |>
  rename_with(\(n) str_replace(n, " cell$", "")) |>
  rename_with(\(n) str_replace(n, " p_perm$", ": permutation p")) |>
  select(Section, Specification, starts_with("Years"), starts_with("Completed"))

datasummary_df(
  robustness_table,
  title  = "Robustness, placebo and heterogeneity",
  notes  = glue("War region × school-age-during-war coefficient (SE clustered by state) and permutation p-value ",
                "({N_PERM} random placebo regions of the same size). Each row changes one element of the ",
                "baseline (main table, columns 1 and 4). * p<0.1, ** p<0.05, *** p<0.01 (clustered SEs)."),
  output = file.path(TABLES_DIR, "table_robustness.tex")
)
print(robustness_table, width = Inf)
