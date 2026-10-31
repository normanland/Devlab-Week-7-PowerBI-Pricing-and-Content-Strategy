# Country happiness, five report editions
### Research note | 2015–2019

## The analytical frame

The five source files were combined into a country-year panel after their field names were aligned. The resulting dataset contains **782 observations**, **170 distinct country labels** and **141 countries with records in every year**. The balanced subset contains 705 country-year observations.

The balanced panel is the basis for the five-year country averages and the 2015-to-2019 endpoint comparison. This is important because an unbalanced average can reward a country simply for having fewer observed years.

The main outcome is `happiness_score`. The six candidate factors are GDP per capita, social support, healthy life expectancy, freedom, generosity and perceptions of corruption. The `dystopia_residual` field is not treated as a driver: it is a residual component of the report's score decomposition and is absent from the 2018 and 2019 files.

## Four findings on the drivers of happiness

### Economic capacity is the strongest cross-country correlate

Across the 141 countries in the balanced panel, the Pearson correlation between five-year mean GDP per capita and five-year mean happiness is **0.819**. This is the strongest association among the six factors.

The same relationship remains visible in each annual cross-section: GDP correlations range from **0.781 in 2015** to **0.812 in 2017**, and stand at **0.794 in 2019**. The consistency suggests that economic capacity is a durable marker of cross-country differences in reported happiness within this dataset.

This is not a causal estimate. It does not show how much an increase in GDP would change an individual country's score.

### Health and social support form a close second tier

Healthy life expectancy correlates with five-year mean happiness at **0.792**, while social support correlates at **0.781**. Both relationships remain strong in the 2019 cross-section: **0.780** for health and **0.777** for social support.

The three leading factors are therefore relatively close, rather than one factor explaining the entire pattern. The annual correlation heatmap shows that this upper tier remains stable from 2015 through 2019.

### Freedom and corruption perceptions have moderate associations

Freedom has a five-year country-mean correlation of **0.586**. The corruption measure has a lower positive correlation of **0.460**. In the 2019 cross-section, these values are **0.567** and **0.386**, respectively.

These values are meaningful but clearly below the associations observed for GDP, health and social support. The corruption field also changes its source label across editions—from `Trust (Government Corruption)` to `Perceptions of corruption`—so the standardized column should be read as a harmonized family of measures, not as proof that the underlying questionnaire and scale are identical in every year.

### Generosity is the weakest of the six factors

Generosity has a five-year country-mean correlation of **0.153** and a 2019 cross-sectional correlation of **0.076**. It is the weakest association in both views.

The 2019 outlier screen defines high generosity as the upper quartile (`≥ 0.248`) and low happiness as the lower quartile (`≤ 4.545`). Nine countries fall into both groups: Myanmar, Haiti, Kenya, Syria, Tanzania, Comoros, Gambia, Uganda and Sierra Leone.

The result does not imply that generosity is unimportant. It shows that the generosity score alone does not distinguish high-happiness countries particularly well in this cross-section.

## Country movement: stable leaders, uneven change

The highest five-year average scores belong to Denmark (**7.546**), Norway (**7.541**), Finland (**7.538**), Switzerland (**7.511**) and Iceland (**7.511**). Burundi has the lowest five-year average (**3.079**), followed by Syria (**3.292**) and Rwanda (**3.439**).

The largest endpoint gains from 2015 to 2019 are:

| Country | 2015 | 2019 | Change |
|---|---:|---:|---:|
| Benin | 3.340 | 4.883 | **+1.543** |
| Ivory Coast | 3.655 | 4.944 | **+1.289** |
| Togo | 2.839 | 4.085 | **+1.246** |
| Honduras | 4.788 | 5.860 | **+1.072** |
| Burkina Faso | 3.587 | 4.587 | **+1.000** |

The largest declines are:

| Country | 2015 | 2019 | Change |
|---|---:|---:|---:|
| Venezuela | 6.810 | 4.707 | **−2.103** |
| Zambia | 5.129 | 4.107 | **−1.022** |
| Zimbabwe | 4.610 | 3.663 | **−0.947** |
| Haiti | 4.518 | 3.597 | **−0.921** |
| Malawi | 4.292 | 3.410 | **−0.882** |

Across the balanced panel, the mean score rises from **5.407 in 2015** to **5.485 in 2019**, an average country-level endpoint gain of **0.079 points**. This modest aggregate movement sits alongside much larger country-specific gains and declines.

Venezuela also has the highest five-year score standard deviation in the balanced panel (**0.898**). Belgium has the lowest (**0.018**). Score volatility is not a direct measure of political or economic instability, but it identifies countries whose reported happiness scores changed most sharply across the five editions.

## Regional contrasts, with a limited time window

The Region field is available in the 2015 and 2016 files, but not in the 2017–2019 files. Regional averages therefore cover only the two editions where the source provides a region label.

| Region | Mean score, 2015–2016 | Countries |
|---|---:|---:|
| Australia and New Zealand | 7.304 | 2 |
| North America | 7.264 | 2 |
| Western Europe | 6.688 | 21 |
| Latin America and Caribbean | 6.122 | 24 |
| Eastern Asia | 5.625 | 6 |
| Middle East and Northern Africa | 5.397 | 20 |
| Central and Eastern Europe | 5.352 | 29 |
| Southeastern Asia | 5.328 | 9 |
| Southern Asia | 4.572 | 7 |
| Sub-Saharan Africa | 4.170 | 44 |

Australia and New Zealand and North America have the highest averages, but each group contains only two countries. Among the larger groups, Western Europe has the highest average. Sub-Saharan Africa has the lowest regional average in this two-year view.

For the 2019 GDP–happiness scatter, country-to-region labels were carried forward from the 2015–2016 files. This lookup covers **152 of 156** country labels; Trinidad & Tobago, Northern Cyprus, North Macedonia and Gambia remain unclassified. The mapped region is a visualization aid, not a newly observed 2019 source field.

## Data treatment and comparability

| Item | Result | Treatment |
|---|---:|---|
| Source files | 5 | Combined after year-specific renaming |
| Country-year rows | 782 | Retained |
| Distinct country labels | 170 | Exact labels retained |
| Countries present in all five years | 141 | Balanced comparison panel |
| Duplicate country-year keys | 0 | No duplicate records found |
| Missing Region values | 467 | Expected: Region is absent in 2017–2019 |
| Missing Dystopia Residual values | 312 | Expected: field is absent in 2018–2019 |
| Missing corruption values | 1 | Pairwise-complete correlation calculation |

The five files use different column names and, in some editions, different labels for conceptually related fields. The analysis aligns these fields but does not rescale or manufacture missing values.

Country names are matched exactly after trimming surrounding spaces. No alias table was imposed, so a country label that changes between editions can reduce the balanced-panel count. This is preferable to silently merging labels without a documented identity rule.

The 2019 ranking runs from Finland (**7.769**) to South Sudan (**2.853**). These are annual endpoints; they should not be confused with the five-year country averages.

## What the numbers cannot establish

- Pearson correlation describes linear association, not causation.
- The happiness score is a composite index; the factor columns are components or related measures, not independent policy levers.
- Country-level patterns do not describe every person's experience within a country.
- The regional comparison is limited to 2015 and 2016 because later files do not provide Region.
- The 2019 region color in the scatter is inherited from earlier labels and has four unmatched countries.
- Small regional groups, especially Australia and New Zealand and North America, have limited country counts.
- The corruption variable's source label changes across editions, so year-to-year comparability deserves caution.

## Research summary

The five-year evidence points to a consistent hierarchy: economic capacity, health and social support have the strongest cross-country associations with happiness; freedom and corruption perceptions sit in a moderate tier; generosity has a weak linear relationship with the score. At the same time, country-level changes are far from uniform. A small increase in the balanced-panel average conceals substantial gains in some countries and steep declines in others.
