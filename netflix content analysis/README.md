# Netflix Content Portfolio Analysis

## A catalog strategy study

This project examines the composition and evolution of the Netflix Movies and TV Shows catalog. The analysis focuses on the balance between Movies and TV Shows, the countries represented in the catalog, the concentration of genre labels, series length, content ratings and the timing of catalog additions.

The work uses the real **Netflix Movies and TV Shows** dataset published by Shivam Bansal on Kaggle. Its 8,807 records cover 6,131 Movies and 2,676 TV Shows across 12 source columns.

## What the analysis reveals

- **A film-led catalog with a growing series contribution.** Movies account for 69.62% of all records. The TV Show share of titles added in 2021 is 33.71%, compared with 24.98% in 2018.
- **2019 is the busiest addition year in this extract.** It contains 2,016 additions, followed by 1,879 in 2020. The 2021 record ends on 25 September, so it is not a full-year comparison.
- **International Movies, Dramas and Comedies lead genre tagging.** Together they represent 35.47% of all title–genre associations. The top five genre labels represent 46.95%.
- **Country contributions are highly concentrated.** The United States, India and the United Kingdom lead the exploded country credits. Their combined share is 55.31% of known country credits.
- **One-season series dominate the TV Show catalog.** A total of 1,793 TV Shows, or 67.00%, have one season.
- **TV-MA is the most common content rating.** It appears on 3,207 titles and represents 42.8% of TV Shows and 33.6% of Movies after within-format normalization.
- **July is the strongest addition month.** The catalog contains 827 July additions, ahead of December (813) and September (770).

These results describe the supplied catalog snapshot. They are not direct measures of viewing hours, subscriber demand, licensing spend or commercial performance.

## Analytical scope

### Catalog composition
- Movie and TV Show counts and percentage shares.
- Addition-year growth from 2008 through 2021.
- A year-added × content-type pivot with row-normalized percentages.
- A separate release-year × content-type pivot, distinguishing a title's release cohort from its catalog addition year.

### Multi-value fields
- `listed_in` is split and exploded into title–genre records.
- `country` is split and exploded into title–country credits.
- `director` is split and exploded into individual director credits.
- Country and genre counts are based on distinct title IDs within each category. A title can appear in more than one category.

### Portfolio depth
- TV Show season bands: one, two, three and four or more seasons.
- Rating distribution by content type, normalized within each format.
- Monthly addition patterns.
- Release-to-addition lag by country, with both mean and median values.
- The five most frequently credited directors and their genre profiles.
- Concentration of the leading genre labels.

## Visual portfolio

The notebook contains seven purpose-built visualizations:

1. Interactive 100% stacked chart of Movie and TV Show share by addition year, with annual title totals.
2. Horizontal ranking of the 15 most frequent genre labels.
3. Grouped comparison of Movie and TV Show credits across the top 10 countries.
4. TV Show season distribution with title counts and percentages.
5. Monthly catalog additions.
6. Heatmap of rating shares within Movies and TV Shows.
7. Heatmap of genre signatures for the five most prolific directors.

## Dataset and methodology notes

- Source: [Netflix Movies and TV Shows — Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows).
- `date_added` is parsed into `year_added` and `month_added`. Ten records have no usable addition date and are excluded only from date-based calculations.
- Missing `director`, `cast` and `country` values are represented as `Unknown`.
- Four rating values are missing. Three additional records contain runtime text in the rating field; all seven are classified as `Unknown` for rating analysis.
- The country field contains multiple country credits. Country counts therefore sum to more than the number of titles.
- Genre counts are title–genre associations rather than mutually exclusive title counts.
- The 2021 addition data ends on 25 September 2021.
- The release-to-addition gap is calculated as `year_added − release_year`. Negative values are retained and flagged as chronology exceptions rather than silently removed.
- Film and television rating systems are not identical. The rating heatmap compares the labels as recorded, normalized within each content type.

## Project files

| File | Purpose |
|---|---|
| `Netflix Content Portfolio Analysis.ipynb` | Complete analysis, tables, narrative context and seven visualizations |
| `netflix_titles.csv` | Source dataset used by the notebook |
| `note.md` | Detailed findings, strategic interpretation and analytical caveats |
| `README.md` | Project overview and reproduction notes |

## Local execution

The notebook first checks the requested Windows Desktop location:

```python
Path(r"C:\Users\anarrasulzada\Desktop\netflix_titles.csv")
```

If that file is not present, it uses `netflix_titles.csv` from the notebook's working directory. The supplied project folder already contains a copy of the dataset.

The notebook uses Python with pandas, matplotlib, seaborn and Plotly. A typical environment setup is:

```bash
pip install pandas matplotlib seaborn plotly jupyter
```

Open `Netflix Content Portfolio Analysis.ipynb` in Jupyter Notebook or VS Code. The dataset file remains beside the notebook as a portable fallback.

## Interpretation

The strongest signal is not a simple replacement of Movies by TV Shows. Movies remain the larger catalog segment, while the TV Show share becomes more substantial in recent addition years and among recent release cohorts. Country and genre credits show a broad international footprint, but the distribution is not uniform: some countries are strongly film-oriented, while Japan and South Korea have a larger TV Show component. The high one-season share and the prominence of TV-MA indicate a catalog with substantial short-run and mature-audience content, although the dataset alone cannot establish why those choices were made.
