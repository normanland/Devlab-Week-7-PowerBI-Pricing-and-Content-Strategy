# The Happiness Panel
### Five years of country scores, shared drivers and divergent paths

A country-level study of the World Happiness Report from 2015 to 2019. The project brings five differently structured CSV files into one consistent panel, then examines the factors most closely associated with happiness, the countries that moved furthest, and the regional patterns visible in the source data.

The analysis is designed around one distinction: a relationship observed across countries is not the same as a change observed within a country over time.

## The question behind the numbers

Which national conditions move most closely with reported happiness? How stable are those relationships from one report year to another? And which countries experienced the largest score gains or losses between 2015 and 2019?

## Source and coverage

**Dataset:** [World Happiness Report — Kaggle](https://www.kaggle.com/datasets/unsdsn/world-happiness)

| File | Country records |
|---|---:|
| `2015.csv` | 158 |
| `2016.csv` | 157 |
| `2017.csv` | 155 |
| `2018.csv` | 156 |
| `2019.csv` | 156 |
| **Combined** | **782** |

The combined data contain 170 distinct country labels. A balanced comparison is possible for 141 countries represented in all five editions, producing 705 country-year observations. The 2015–2019 change analysis and the five-year country leaderboard use this balanced panel.

## How the analysis is built

### One schema, five source formats

The column names are standardized before concatenation. Examples include `Family` → `social_support`, `Economy (GDP per Capita)` → `gdp_per_capita`, and the later `Score` field → `happiness_score`.

The original values are retained. A field that does not exist in a source year remains missing; it is not reconstructed from another variable.

### A balanced country panel

Country averages and endpoint changes use only countries with a score in all five years. This avoids comparing a five-year average for one country with a one- or two-year average for another.

### Driver analysis

The primary Pearson correlations use each country's five-year mean score and five-year mean factor values. Annual correlations and the 2019 cross-section provide separate checks on whether the factor ranking is consistent.

Correlation is treated as association, not evidence that a factor causes a change in happiness.

### Regional context

The source files contain `Region` only in 2015 and 2016. The regional average comparison is therefore limited to those two editions. For the 2019 GDP–happiness scatter, the earlier country-to-region labels are carried forward where a country name matches; unmatched labels remain unclassified.

### Distribution and exceptions

The analysis also covers score dispersion by year, the top 20 country trajectories, country-level volatility, and a transparent generosity outlier screen based on 2019 quartiles.

## Findings at a glance

- **GDP per capita** has the strongest correlation with five-year mean happiness (`r = 0.819`), followed by healthy life expectancy (`r = 0.792`) and social support (`r = 0.781`).
- **Generosity** has a much weaker association (`r = 0.153`). Its 2019 relationship with happiness is weaker still (`r = 0.076`).
- **Denmark** has the highest five-year average score (`7.546`); **Burundi** has the lowest (`3.079`) among the 141-country balanced panel.
- **Benin** records the largest 2015–2019 gain (`+1.543` points), while **Venezuela** records the largest decline (`−2.103` points).
- In the editions with regional labels, **Australia and New Zealand** average `7.304` and **North America** `7.264`, but each group contains only two countries. Among larger regional groups, Western Europe averages `6.688`; Sub-Saharan Africa averages `4.170`.

The 2019 cross-section ranges from Finland (`7.769`) to South Sudan (`2.853`).

## Visual guide

The executed notebook contains ten static visualizations and one interactive Plotly explorer:

| Visual | Analytical purpose |
|---|---|
| Ranked correlation bars | Relative strength of the six happiness-factor associations |
| Top and bottom country panels | Persistent differences in five-year average scores |
| Riser/faller bars | Largest 2015–2019 endpoint changes |
| Regional average bars | Regional differences in the years with available labels |
| GDP–happiness scatter | 2019 relationship, colored by mapped region |
| Generosity outlier scatter | Countries in the high-generosity / low-happiness quadrant |
| Yearly violin plots | Shape and spread of scores across report editions |
| Top-20 country heatmap | Five-year score paths among the highest-scoring countries |
| Annual correlation heatmap | Stability of factor relationships from 2015 to 2019 |
| Volatility panels | Countries with the most variable and most stable scores |
| Animated Plotly scatter | Interactive year-by-year GDP and happiness comparison |

The Plotly chart is executed and embedded in the notebook output. Its year control, hover details and animation are available when the notebook is opened in a compatible Jupyter environment.

## Running the notebook

The data-loading cell reads the five CSV files from:

```text
C:\Users\anarrasulzada\Desktop\world happiness report data
```

The expected filenames are `2015.csv`, `2016.csv`, `2017.csv`, `2018.csv` and `2019.csv`. The same five source files are included in this project package.

Required libraries:

```bash
pip install pandas numpy matplotlib seaborn plotly jupyter
```

Open `World Happiness Panel Analysis.ipynb` in Jupyter Notebook or VS Code. The delivered notebook already contains executed outputs and charts.

## Project files

- `World Happiness Panel Analysis.ipynb` — complete analysis, tables, static charts and interactive chart
- `note.md` — research design, four driver insights, country movements and methodological boundaries
- `2015.csv` to `2019.csv` — source files used in the analysis

## Reading the results responsibly

The World Happiness Report scores are composite measures. The factor correlations are descriptive and do not isolate causal effects. Regional comparisons are limited by the availability of region labels, and the 2019 region mapping uses country labels from the 2015–2016 files. Small regional groups should not be interpreted as representative of a broad population.
