# Thesis Feedback
**Course**: ECON 397 — Undergraduate Honors Thesis  
**Original paper**: *Education Under Fire: Conflict Exposure and Educational Attainment in Northern Nigeria*
**Feedback date**: March 5, 2013  
**Status**: Reference document for upgraded thesis

> This document consolidates Dr. Goldberg's written feedback on the original thesis draft. It has been reorganized and cleaned for use as a standing reference during the upgrade. Time-specific action items have been converted into standing revision priorities. Data acquisition details have been moved to `data_acquisition.md`.

---

## Overall Assessment

This is a genuinely interesting piece of work. The research question matters, the two-dataset approach (NEDS + UCDP) is the right instinct, and pushing through to empirical results is harder than it looks. The revisions needed are not about saving a weak project — they are about making a good project excellent.

The goal of the revision is to make the paper represent your *ability*, not just your effort. That means tightening the econometrics, cleaning the writing, and being precise about what the analysis can and cannot establish.

> Graduate economics programs are looking for students who can both ask important questions and reason carefully about identification. This paper, with these revisions, can demonstrate both.

---

## Key Issues (Priority Order)

### 1. Identification Strategy — The Core Problem

**The fundamental problem**: Violence is not randomly assigned across LGAs. Communities that experience conflict tend to be poorer, more politically marginalized, more ethnically fractious, and more resource-constrained. Comparing children in violent LGAs to children in peaceful LGAs conflates the effect of violence with pre-existing disadvantage.

**The most damning evidence is in your own results**: The violence coefficients almost entirely flip sign when LGA fixed effects are added. The paper does not currently grapple with this, and it needs to.

**What the current approach gets right**: The age-at-exposure strategy — comparing children *within the same LGA* who were at different developmental stages when violence hit — is a legitimate and well-established identification approach. It is the same intuition as Almond's critical period work. The LGA fixed effects model is the correct implementation of this idea. Lean into it and defend it rather than treating both specifications as equally valid.

**Limitation to acknowledge explicitly**: Even within an LGA, children who were school-age during violence may differ from those who were too young or too old in ways other than violence exposure. This must be stated.

### 2. Results Interpretation — The Sign Reversal

The shift from OLS to LGA fixed effects in the `highest_enrolled` regression is not a minor adjustment — it is a fundamental change in direction. It must be addressed head-on. Possible explanations to discuss:

- **Survivorship bias**: Children who remained in school despite violence may be positively selected on unobserved characteristics (family wealth, motivation).
- **Measurement error**: If the UCDP data understates actual conflict exposure, coefficients may be attenuated or biased in unpredictable directions.
- **Compensatory responses**: Families in conflict areas may increase education investment as an insurance mechanism (consistent with some findings in the Ugandan LRA literature).

You do not need to resolve the ambiguity — but you must engage with it honestly. A paper that says "we cannot definitively establish causality but here is what the evidence suggests and why" is far stronger than one that reports inconsistent results without comment.

### 3. Writing Quality

The draft reads as a first pass in places. Specific issues to fix:

- **Broken sentence in Section III**: *"questions on the effectiveness of these investments prove very important to the political leaders and policy whether the population i and how to ensure the young are getting the most out of these investments have."* Rewrite from scratch.
- **Typo**: "Hey also found" → "He also found"
- **Informal phrasing to cut**: "I will go deeper into the literature a bit later in the paper" — just move into the literature review.
- **Results narrate numbers, not economics**: Don't just report what the coefficients are — tell the reader what they mean, why they are surprising or expected, and what they imply.

---

## Writing Guidance

Your natural voice — direct, curious, grounded in Nigerian context — is an asset. The goal is to polish and tighten it, not replace it with stiff academic prose.

**Lead with stakes, not mechanics.** The introduction sometimes buries the lede by jumping to methodology before the reader is emotionally invested. Let the human cost land first. One or two strong sentences about what was happening on the ground in Borno circa 2013 does more work than a paragraph of literature positioning.

**Sharpen your claims.** Watch for hedging that drains sentences of force — "it may be the case that" or "it seems as though" — where you actually have evidence to be confident. Be assertive where your data supports it. Reserve hedging for genuine uncertainty.

**Vary sentence rhythm deliberately.** You tend toward medium-length sentences throughout, creating a monotonous pace. Short sentences after longer analytical ones create emphasis. Read sections aloud — if you don't notice variation, add it.

**Transition deliberately between sections.** A single sentence like "Having established the historical context, I now turn to the data and estimation strategy" maintains narrative thread.

**Cut "this paper" and "I will show."** Replace "In this paper, I will show that conflict reduces enrollment" with the claim itself: "Boko Haram's insurgency significantly reduced educational attainment in Nigeria's Northeast — and the effects were not limited to areas of active fighting."

**Be specific about geography and people.** Instead of "conflict-affected areas," say "Borno, Yobe, and Adamawa states." Instead of "children," say "primary school-age children" or "girls in rural LGAs."

### Suggested Rewrite: Introduction (Opening Paragraph)

**Original:**
> *The purpose of this paper is to measure the effects of violence on educational attainment amongst school age children in Nigeria. I use survey data from the 2010 Nigeria Education Data Survey (NEDS) and combine this with violence data spanning the years 1999-2010 from the Uppsala Conflict Data Program (UCDP) to see whether experiencing violence has an effect on the number of years of education a student will attain and whether it increases the likelihood that a student will be enrolled in school.*

**Suggested revision:**
> *This paper estimates the effect of community-level violence exposure on two key educational outcomes for Nigerian children: school enrollment and years of schooling attained. Using child-level data from the 2010 Nigeria Education Data Survey (NEDS) linked to georeferenced conflict event data from the Uppsala Conflict Data Program (UCDP) spanning 1999 to 2010, I construct violence exposure indicators at the Local Government Area (LGA) level and assign each child a treatment status based on their age at the time of the first recorded conflict event in their community. The central question is whether children who experienced violence during developmentally sensitive periods — early childhood, primary school age, or adolescence — show systematically different educational trajectories than their peers who were not exposed.*

What changed: specifies the identification approach (age-at-exposure variation), names the unit of analysis (LGA), frames the question to signal methodological awareness, and removes the informal "to see whether" phrasing.

### Suggested Rewrite: Methodology Opening

**Suggested revision:**
> *The central empirical challenge in estimating the effect of violence on education is that conflict is not randomly distributed across communities. LGAs that experienced violence during the study period tend to differ from peaceful LGAs along multiple dimensions — they are generally poorer, more ethnically divided, and more politically unstable — and these underlying conditions independently predict lower educational attainment. A naive comparison of children in conflict-affected and peaceful LGAs would therefore conflate the effect of violence with the effect of pre-existing disadvantage. To address this, I exploit variation in the timing of violence onset relative to each child's age, comparing children within the same LGA who were at different developmental stages when conflict first occurred. The identifying assumption is that, conditional on LGA fixed effects, the timing of violence onset within the study period is uncorrelated with child-specific unobservables that affect educational outcomes. While this assumption cannot be tested directly, it is supported by the fact that the UCDP data covers a wide range of conflict types — including spontaneous inter-ethnic violence, political assassinations, and insurgent attacks — whose precise timing within a multi-year window is plausibly exogenous to household-level educational investment decisions. LGA fixed effects absorb all time-invariant community-level confounders, including pre-existing poverty levels, ethnic composition, and distance from educational centers.*

---

## Title Options

The original title ("No School Today, It's Raining Bullets!") is too informal for academic publication. Alternatives:

1. **"Education Under Fire: Conflict Exposure and Educational Attainment in Northern Nigeria"** — straightforward, field-standard, signals regional focus
2. **"Caught in the Crossfire: The Effect of the Boko Haram Insurgency on Educational Attainment in Northeast Nigeria"** — retains some energy while staying credible *(recommended for journal submission)*
3. **"When Bullets Replace Books: Boko Haram, Violent Conflict, and Human Capital Formation in Northern Nigeria"** — bridges original voice with academic framing *(recommended if preserving voice)*
4. **"The Cost of Conflict: Boko Haram and Educational Attainment Losses in Nigeria's Northeast"** — clean, policy-oriented
5. **"Fear, Flight, and Foregone Schooling: The Educational Impact of the Boko Haram Insurgency in Northeast Nigeria"** — captures mechanism and has memorable rhythm

---

## Structural Elements Missing from the Draft

### A. Summary Statistics Table — Non-Negotiable
Before any regression results, present a table with mean, standard deviation, and sample size for all key variables, broken down by violence exposure status (LGAs with violence vs. without).

**Suggested structure:**
- Rows: All outcome and control variables (`attend`, `highest_enrolled`, age, male, urban, wealth quintile, religion, distance to school, parental education)
- Columns: (1) Full sample mean/SD, (2) No-violence LGAs, (3) Violence LGAs, (4) Difference and p-value of t-test

This table immediately tells the reader whether your treatment and control groups are balanced on observables — directly relevant to the endogeneity discussion.

### B. Violence Descriptive Section
Before regression results, describe the violence data: how many LGAs experienced violence, what share of children are in the "treated" category, what types of violence dominate (state-based, non-state, one-sided), and the temporal distribution of events. A map or figure showing violence intensity by LGA would be particularly impactful.

### C. Mechanism Discussion
The paper establishes (or tries to establish) a statistical relationship but never asks *why* violence would affect schooling. Two main channels:

- **Supply-side**: Violence destroys or disrupts school infrastructure, kills or displaces teachers, makes travel to school dangerous
- **Demand-side**: Income shocks reduce household ability to pay; mortality/morbidity of household members changes returns to schooling; fear and trauma reduce academic engagement

Nigeria's Boko Haram insurgency — which explicitly targets schools as symbols of Western influence — is a particularly clear case of the supply-side channel. Your data may not allow distinguishing these mechanisms, but naming them shows analytical depth.

### D. Robustness Checks (Minimum Viable)
- Run the analysis on subsamples (northern states only, where violence is most concentrated)
- Use an alternative violence definition (deaths per capita rather than binary exposure)
- Check whether results hold if you drop LGAs with very few observations
- Add the F-statistic or joint significance test for the full set of violence indicators in each regression table

---

## More Credible Identification Strategies to Discuss

Full implementation is not required — add a section discussing what you would do with more data and be transparent about current limitations. This demonstrates methodological sophistication to graduate admissions committees.

### 1. Geographic Regression Discontinuity (Boundary Design)
Compare children in LGAs that experienced violence to children in adjacent peaceful LGAs along shared borders. Children living just inside a conflict-affected LGA and just across the border in a peaceful LGA are likely similar in most unobserved characteristics. A discrete jump in educational outcomes at the LGA boundary is strong evidence of a causal effect. Requires LGA boundary shapefiles (available from GADM or GRID3) and household GPS coordinates (available in DHS GPS files).

### 2. Cohort-Based Difference-in-Differences
Define "treated" LGAs as those experiencing violence onset during the study period, and "control" LGAs as those that never experienced violence. Compare educational outcomes of cohorts who were school-age during the violence versus older cohorts who had already completed schooling by the time violence began. If violence truly affects attainment, the treated cohort in violent LGAs should show larger declines relative to control LGAs than the older cohort does. This falsification test would significantly strengthen credibility.

### 3. Violence Intensity as Continuous Treatment
Rather than a binary indicator, use the number of deaths, number of events, or total conflict incidents as a continuous measure of intensity. This tests whether more intense violence has larger educational effects, consistent with a causal interpretation. Constructible from the UCDP data already in hand.

### 4. Instrumental Variable (IV) Approach
An ideal IV predicts violence in an LGA but does not independently affect education. Rainfall shocks are the most common instrument for conflict in Sub-Saharan Africa (Ciccone 2011; Miguel et al. 2004): lower rainfall predicts higher conflict by reducing agricultural income and increasing the opportunity cost of peaceful activity. Rainfall data at the LGA-year level is available from CHIRPS. Ethnic fractionalization indices are another candidate. Describe this strategy even if you cannot implement it.

---

## Figures and Visualizations to Add

### Priority Figures
1. **Map of Nigeria — violence events by LGA, 1999–2010**: Plot each UCDP event as a point, colored by type and sized by fatalities. The single most impactful visual you can add — immediately shows where violence is concentrated and contextualizes the North-South educational disparities.
2. **Timeline of violence events, 1999–2010**: Bar chart or line graph of events and/or deaths per year. Illustrates that the study period spans meaningfully different conflict phases.
3. **Coefficient plot (forest plot)**: Point estimates and 95% confidence intervals for each violence coefficient across all four models. Makes the sign reversal between OLS and fixed effects immediately visible.
4. **Educational attainment by violence exposure and age cohort**: Bar chart showing mean years of schooling for exposed vs. unexposed children by age window. The descriptive analog to your regressions.

### Tables to Add or Improve
- **Table 1**: Summary statistics (see above)
- **Table 2**: Violence events by LGA and region — number of events, deaths, share of sample in affected LGAs
- **Tables 3–4**: Current regression tables, with an added row reporting the F-statistic or joint significance test for the violence indicators collectively

---

## Additional Data Sources

See `data_acquisition.md` for download instructions. Summary of advisor recommendations:

| Dataset | Recommended? | Notes |
|---|---|---|
| **ACLED** | ✅ High priority | Geocoded conflict events 1997–present; should replace or supplement UCDP as primary conflict measure |
| **Nigeria DHS (2008, 2013)** | ✅ High priority | Child-level enrollment data + GPS cluster coordinates for geographic analysis |
| **CHIRPS rainfall** | ✅ If pursuing IV | Available via Google Earth Engine; most common instrument for conflict in SSA |
| **DMSP-OLS Night Lights** | ⚠️ Secondary | Useful as proxy for local economic conditions; harmonization with VIIRS needed post-2013 |
| **UBEC school census** | ❌ Not recommended | No publicly available machine-readable dataset; access requires institutional contacts. Use NEDS/DHS education recode instead. |

---

## Revised Paper Outline

Structure appropriate for a master's-level economics paper targeting a development journal (e.g., *Journal of Development Economics*).

**Abstract** (~200 words)  
One sentence each: question, setting and why it matters, identification strategy, main finding, policy implication. Write last.

**I. Introduction** (~4–6 pages)  
Open with a concrete illustration of the conflict's educational disruption — a specific attack, a statistic about school closures — before the reader is in analytical mode. Lay out the research question precisely, explain why Nigeria's Northeast and Boko Haram are the right setting, preview the empirical strategy in plain language, state main findings and contribution. Close with a roadmap sentence. Avoid overloading with citations here — save depth for the review.

**II. Background and Historical Context** (~4–5 pages)  
Three components: (1) the Boko Haram insurgency — origins, escalation, geographic concentration, key events including the 2014 Chibok kidnapping and 2015 peak violence; (2) Nigeria's educational landscape, particularly the pre-existing North-South gap and the al-Majiri system, which demonstrates that educational disadvantage predates the conflict; (3) the specific mechanisms through which Boko Haram affected education — school destruction, teacher flight, student displacement, parental fear.

**III. Literature Review** (~5–7 pages)  
Organize thematically, not by paper. Suggested sub-sections: (a) the broader conflict and human capital literature; (b) gender-differential effects; (c) mechanisms; (d) Nigeria-specific evidence and your paper's position relative to Leone et al. (2019). End with a clear statement of your specific contribution.

**IV. Data** (~4–5 pages)  
Describe each dataset: DHS Nigeria (2003, 2008, 2013, 2018 rounds), ACLED conflict events, and supplementary data (CHIRPS, nighttime lights). Explain variable construction — conflict exposure measure, educational outcome, controls. Present summary statistics table comparing treated and control LGAs. Flag data limitations honestly.

**V. Empirical Strategy** (~4–5 pages)  
Lay out the DiD design: treatment group (Northeast LGAs with high conflict exposure), control group (similar LGAs with low/no exposure), pre/post periods (pre-2009 cohorts vs. those school-age during the insurgency). Write out the regression equation and define every term. Discuss the parallel trends assumption explicitly — do you have evidence for it? How do you test it? Explain standard error clustering choice. Acknowledge threats to validity: selection into conflict exposure, displacement contaminating control groups, potential SUTVA violations.

**VI. Results** (~6–8 pages)  
Lead with main DiD estimates in a clean table. Follow with an event study figure showing dynamic treatment effects by year/cohort — essential for establishing pre-trend credibility. Then heterogeneity: results by gender, rural/urban, conflict intensity quartile. Each sub-analysis should have a brief motivating sentence for why the heterogeneity matters theoretically.

**VII. Robustness Checks** (~3–4 pages)  
At minimum: placebo tests using non-treated regions or pre-insurgency periods, alternative conflict exposure measures (fatalities vs. event counts, different radii), alternative control group definitions, and dropping states bordering the Northeast to address spillover concerns.

**VIII. Mechanisms** (~2–3 pages)  
Use ACLED data to look at school-specific attacks vs. general violence. If DHS data on child labor or household displacement is available, test whether conflict exposure predicts those outcomes. The goal is to move from "conflict reduces schooling" to "conflict reduces schooling *because* schools were destroyed and families fled."

**IX. Policy Implications and Discussion** (~2–3 pages)  
Translate findings into stakes: aggregate schooling years lost, lifetime earnings implications using Mincerian returns. Discuss interventions the evidence supports — cash transfers, school reconstruction, teacher incentive programs, IDP education support. Avoid overclaiming policy certainty from a single study.

**X. Conclusion** (~1–2 pages)  
Brief synthesis of what you found and why it matters. Acknowledge limitations. End with one or two sentences on future research directions.

**References** — Full bibliography in target journal style (AEA: author-date; JDE: numbered).

**Appendix** — Additional robustness tables, variable construction details, sample restriction sensitivity, technical derivations.

---

## Annotated Bibliography

### Core Empirical Comparators

**Akresh, R., & de Walque, D. (2011). Armed conflict and schooling: Evidence from the 1994 Rwandan genocide. *World Bank Policy Research Working Paper* 4606.**
- Their cohort-based DiD design (comparing children school-age during genocide vs. not) is the template for your identification strategy — internalize this fully
- Large negative effects concentrated in specific age/gender groups — demonstrates value of heterogeneity analysis
- Rwanda's ethnic targeting creates a clean natural experiment; your analog is geographic variation in Boko Haram intensity across LGAs
- Their robustness checks (placebo cohorts, spatial spillovers) are exactly the checks you should replicate

**Leone, T., Brown, L., Memon, A., & Bhatt, S. (2019). Education is Forbidden: The Effect of the Boko Haram Conflict on Education in North-East Nigeria. *Journal of Development Economics*, 141, 102365.**
- Your closest comparator paper — read it until you understand every specification and table
- They use Nigeria GHS Panel + ACLED at village level; your DHS approach covers more rounds and different populations — this is your differentiation
- Their finding (10 fatalities within 5km → ~1 pp enrollment drop) is your benchmark; discuss whether your estimates are consistent or diverge and why
- What they don't do: no explicit gender heterogeneity decomposition, no rainfall controls, limited discussion of displacement as a mechanism — these are your openings

**Chamarbagwala, R., & Morán, H. E. (2011). The human capital consequences of civil war: Evidence from Guatemala. *Journal of Development Economics*, 94(1), 41–61.**
- Shows conflict effects on education persist into adulthood as labor market penalties — motivates framing around long-run human capital losses, not just enrollment drops
- Use of census data (large N, retrospective education histories) is a methodological model for DHS birth cohort reconstruction
- Strong gender differential findings — girls lost more schooling — relevant to heterogeneity section

**Shemyakina, O. (2011). The effect of armed conflict on accumulation of schooling: Results from Tajikistan. *Journal of Development Economics*, 95(2), 186–200.**
- Finds conflict increased girls' enrollment relative to boys in some contexts because boys were conscripted — counterintuitive result that sharpens thinking on mechanisms
- Household-level substitution effects (labor demand shifts during conflict) worth discussing in mechanism section even if not tested directly
- Good example of testing pre-trend parallel assumption explicitly in a DiD setup

### Nigeria and Boko Haram Context

**Afzal, N. (2020). Education and Boko Haram in Nigeria. *Brookings Institution Center for Middle East Policy.***
- Best non-technical overview of the ideological relationship between Boko Haram and Western education — essential for introduction and historical context
- Documents al-Majiri system's pre-existing tensions with formal schooling in northern Nigeria — establishes that educational disadvantage predates Boko Haram
- Key statistics (600+ teachers killed, 1,400+ schools destroyed) to cite in motivation section

**Olashore, A., Akanni, O., Fela-Thomas, A., & Kinnear, J. (2016). Impact of the Boko Haram insurgency on the child's right to education in Nigeria. *African Human Rights Law Journal*, 16(1), 645–669.**
- Primary source for hard statistics on scale: 314 children killed 2012–14, 1,400 schools destroyed, 2.1 million IDPs (55% children)
- Use in introduction and context section to establish stakes

### Methodology and Theory

**Angrist, J. D., & Pischke, J. S. (2009). *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton University Press.**
- Chapter 5 is your DiD reference — every methodological decision should be traceable to the assumptions outlined here
- Parallel trends, the role of controls, clustering standard errors: understand these deeply enough to explain them to a skeptical reader
- Use "selection on observables vs. unobservables" framing to motivate identification strategy in the methods section

**Verwimp, P., Justino, P., & Brück, T. (2019). The microeconomics of violent conflict. *Journal of Development Economics*, 141, 102297.**
- Excellent methodological overview of the full conflict-development literature; situates your work in broader context
- Taxonomy of conflict effects (direct vs. indirect, short-run vs. long-run) gives a conceptual structure for your theoretical framework section

**Baez, J. E. (2011). Civil wars beyond their borders: The human capital and health consequences of hosting refugees. *Journal of Development Economics*, 96(2), 391–408.**
- Displacement and refugee flows as educational disruption mechanisms — relevant to discussion of the 2M+ IDPs generated by Boko Haram
- Argues that spillover effects on non-conflict LGAs that received IDPs are part of the story
- Motivates controlling for IDP inflows or doing a robustness check excluding LGAs that received large displaced populations

---

## Revision Priorities

Converted from the original time-specific work plan into standing priorities:

1. **Fix the writing first.** Eliminate incomplete sentences, casual phrasing, and typos throughout. Rewrite the broken Literature Review opening. Polish the introduction. Do not add new content until what exists is clean and defensible.

2. **Add missing structural elements.** Build the summary statistics table. Write a paragraph describing the violence data (number of LGAs, events, temporal distribution). Add a mechanisms paragraph. Draft the identification discussion with honest acknowledgment of limitations and brief descriptions of the RD and DiD alternatives.

3. **Rewrite the Results sections to be interpretive.** Explicitly address the sign reversal between OLS and fixed effects. Add the coefficient plot if possible; at minimum, add labels and discussion to the existing figures.

4. **Rewrite the Conclusion.** It is currently too thin and pivots too quickly to generic policy recommendations. The conclusion should: (a) summarize findings and identification strategy, (b) be honest about what results can and cannot establish causally, (c) connect findings to existing literature, and (d) suggest the next empirical step a researcher would take.
