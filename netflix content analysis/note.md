# Netflix Content Portfolio — Research Notes

## Executive reading

The supplied Netflix catalog contains 8,807 titles: 6,131 Movies (69.62%) and 2,676 TV Shows (30.38%). The catalog remains film-led, but the share of TV Shows is more visible in later addition years and among recent release-year cohorts.

The analysis separates three concepts that can easily be confused:

- **Release year:** when the title was originally released.
- **Addition year:** the year recorded in `date_added`.
- **Country credit:** a country associated with a title, not necessarily the only country involved in its production.

The difference matters. A release-year pivot describes the age and format profile of the catalog; an addition-year pivot describes when titles were recorded as entering Netflix.

## Five strategic findings

### A film-led base, with a stronger TV Show contribution in recent cohorts

Movies account for 69.62% of all catalog records. Before 2015, Movies make up 80.36% of titles with a valid addition date. The TV Show share among additions is 24.98% in 2018, 29.37% in 2019, 31.67% in 2020 and 33.71% in 2021.

The release-year view adds a second signal. TV Shows represent 25.68% of titles released in 2017, 33.13% in 2018, 38.54% in 2019, 45.75% in 2020 and 53.21% in 2021. The 2021 cohort is partial, so the final percentage is indicative rather than a full-year result.

**Strategic reading:** the catalog does not become TV Show-dominant overall, but the more recent cohorts contain a larger series component than the earlier catalog base.

### International reach is broad, while country format profiles differ

After splitting the multi-value `country` field, the leading country credits are:

| Country | Titles | Movies | TV Shows |
|---|---:|---:|---:|
| United States | 3,690 | 2,752 | 938 |
| India | 1,046 | 962 | 84 |
| United Kingdom | 806 | 534 | 272 |
| Canada | 445 | 319 | 126 |
| France | 393 | 303 | 90 |
| Japan | 318 | 119 | 199 |
| Spain | 232 | 171 | 61 |
| South Korea | 231 | 61 | 170 |
| Germany | 226 | 182 | 44 |
| Mexico | 169 | 111 | 58 |

The United States, India and the United Kingdom account for 55.31% of known country credits. The format split is not consistent across markets. India is strongly Movie-oriented (962 Movies versus 84 TV Shows), while Japan (119 versus 199) and South Korea (61 versus 170) have more TV Show credits than Movie credits.

**Strategic reading:** country presence alone does not describe the portfolio. The format mix within each country reveals distinct catalog profiles.

### Genre breadth exists, but the leading labels hold a large share of tagging

The top genre labels are:

| Genre | Title credits |
|---|---:|
| International Movies | 2,752 |
| Dramas | 2,427 |
| Comedies | 1,674 |
| International TV Shows | 1,351 |
| Documentaries | 869 |
| Action & Adventure | 859 |
| TV Dramas | 763 |
| Independent Movies | 756 |
| Children & Family Movies | 641 |
| Romantic Movies | 616 |
| TV Comedies | 581 |
| Thrillers | 577 |
| Crime TV Shows | 470 |
| Kids' TV | 451 |
| Docuseries | 395 |

There are 42 distinct genre labels and 19,323 title–genre associations. The leading three labels account for 35.47% of all associations; the leading five account for 46.95%.

**Strategic reading:** the catalog has a broad set of genre labels, but international films, drama and comedy are the main pillars of its tagging structure. These percentages describe metadata associations, not viewing share.

### Short series are the dominant TV Show format

| Season band | TV Shows | Share |
|---|---:|---:|
| 1 season | 1,793 | 67.00% |
| 2 seasons | 425 | 15.88% |
| 3 seasons | 199 | 7.44% |
| 4+ seasons | 259 | 9.68% |

Two-thirds of TV Shows have one season. Only 9.68% have four or more seasons.

**Strategic reading:** the catalog is weighted toward one-season series. This is consistent with a strong limited-run or short-series presence, but the dataset does not identify whether a series ended by design, was cancelled, or simply had no later season recorded.

### Mature ratings and a mid-year addition peak shape the catalog profile

TV-MA is the most frequent rating label, with 3,207 titles. It represents 42.8% of TV Shows and 33.6% of Movies when each format is normalized separately. TV-14 is second, with 2,160 titles. Film-specific labels are concentrated in Movies: the catalog records 797 R-rated Movies and only two R-rated TV Shows.

July is the most active addition month, with 827 titles. December follows with 813, then September with 770. October contains 760 additions and is not the peak month in this dataset.

**Strategic reading:** mature-audience labels are prominent in both formats, especially TV Shows. Addition activity is distributed across the year, with a July high point and a secondary December peak.

## Addition-year detail

The yearly pivot uses `date_added`, not `release_year`.

| Year added | Movies | TV Shows | Total | TV Show share |
|---|---:|---:|---:|---:|
| 2015 | 56 | 26 | 82 | 31.71% |
| 2016 | 253 | 176 | 429 | 41.03% |
| 2017 | 839 | 349 | 1,188 | 29.38% |
| 2018 | 1,237 | 412 | 1,649 | 24.98% |
| 2019 | 1,424 | 592 | 2,016 | 29.37% |
| 2020 | 1,284 | 595 | 1,879 | 31.67% |
| 2021 | 993 | 505 | 1,498 | 33.71% |

2019 is the highest-volume addition year in the extract. The 2021 count covers additions through 25 September 2021 and is not directly comparable with complete calendar years.

The small counts in 2008–2014 should not be treated as evidence of Netflix's total historical acquisition volume. They describe only the records and dates represented in this particular catalog file.

## Release-to-addition lag by country

The calculation is:

`release-to-addition gap = year_added − release_year`

A larger positive result means the title was added further after its recorded release year. The country table below is restricted to countries with at least ten distinct title credits.

| Country | Title credits | Mean gap | Median gap |
|---|---:|---:|---:|
| Hong Kong | 105 | 13.75 years | 8 years |
| Poland | 41 | 10.88 years | 1 year |
| Egypt | 117 | 10.78 years | 6 years |
| Lebanon | 31 | 10.19 years | 3 years |
| India | 1,046 | 6.69 years | 3 years |

Hong Kong has the highest mean gap among countries meeting the minimum-count threshold. Poland's mean is high while its median is only one year, suggesting that a smaller number of older titles pull the average upward. The median is therefore an important companion to the mean.

Fourteen distinct titles have a negative gap, meaning the recorded addition year is earlier than the release year. These records are retained rather than silently removed; they may reflect pre-release catalog timing or metadata inconsistencies.

## Director profiles

The five directors with the highest distinct title counts are:

| Director | Distinct titles | Main genre pattern |
|---|---:|---|
| Rajiv Chilaka | 22 | Children & Family Movies |
| Jan Suter | 21 | Stand-Up Comedy |
| Raúl Campos | 19 | Stand-Up Comedy |
| Suhas Kadav | 16 | Children & Family Movies, Comedies and Music & Musicals |
| Marcus Raboy | 16 | Stand-Up Comedy |

A title with multiple directors is credited to each listed director. Genre associations can also overlap, so the sum of a director's genre counts may exceed the director's distinct title count.

## Data quality and treatment

| Field | Missing or adjusted records | Treatment |
|---|---:|---|
| `director` | 2,634 missing | Replaced with `Unknown` |
| `cast` | 825 missing | Replaced with `Unknown` |
| `country` | 831 missing | Replaced with `Unknown` |
| `date_added` | 10 missing | Excluded from date-based analysis |
| `rating` | 4 missing | Classified as `Unknown` |
| `rating` | 3 runtime-like values | Classified as `Unknown` |

The three malformed rating values contain runtime text such as `66 min`, `74 min` and `84 min`. They are not valid rating categories. The cleaned rating analysis therefore contains seven `Unknown` records.

The original dataset has 8,807 rows and 12 columns. The `date_added` field parses successfully for 8,797 records. The country field contains multiple country credits per title, and `listed_in` contains multiple genre labels per title.

## Methodological boundaries

- Country and genre counts are multi-label counts. Their totals are not expected to equal 8,807.
- The top-country comparison uses distinct title IDs within each country and content type.
- The rating chart uses percentages within each content type. Movie and TV rating systems are not identical classification scales.
- `date_added` is treated as the recorded catalog addition date, not proof of the date of contract signature or licensing approval.
- The 2021 addition-year record ends on 25 September 2021.
- The dataset contains no viewing hours, revenue, subscription conversion, licensing costs or audience retention. Strategy interpretations remain descriptive rather than causal.

## Analytical conclusion

The catalog has a stable Movie majority, but later addition and release cohorts show a stronger TV Show presence. International representation is substantial, although country portfolios differ sharply in their format mix. Genre tagging is concentrated in International Movies, Dramas and Comedies, while the TV Show catalog is heavily weighted toward one-season titles. TV-MA and TV-14 dominate the rating structure, and July is the strongest addition month in the supplied snapshot.

The most defensible strategic interpretation is a broad, international catalog built on a film-heavy foundation, with a more visible series component in recent cohorts and a large concentration of short-run TV content.
