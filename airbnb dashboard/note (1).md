# Analytical Note
## Seattle Airbnb — Neighbourhood Pricing, Availability and Listing Characteristics

### 1. Purpose and analytical questions

This project examines the Seattle Airbnb listing market through four connected perspectives: neighbourhood-level price positioning, calendar availability patterns, listing characteristics and geographic concentration. The objective is to identify differences between areas and property types, show how asking prices and unavailable-night rates vary over time, and provide a transparent evidence base for exploratory investor comparisons.

The analysis is descriptive. It does not estimate causal effects, forecast returns or establish that an unavailable date represents a paid stay.

### 2. Scope and task alignment

The deliverable addresses the main analytical views requested for the Seattle Airbnb task:

| Task area | Implementation in this submission |
|---|---|
| Neighbourhood benchmarking | Median asking price, unavailable-night rate, neighbourhood comparison table and price-versus-rate quadrant. |
| Seasonality | Monthly weighted median published asking price and monthly unavailable-night rate. |
| Listing characteristics | Price distribution by room type, room-type availability comparison, instant-bookable comparison and review-count scatter plot. |
| Geographic comparison | Neighbourhood coordinate-centroid visualization and dynamic Top-N comparison. |
| Neighbourhood-level inspection | Selected-neighbourhood summary, room-type mix and monthly trend. |
| Scenario analysis | Price-change sensitivity control with the unavailable-night rate held constant. |
| Reproducibility | Python source code, input CSV files, exported PNG/SVG charts, derived metric tables and validation output. |

The implementation is presented as a Python and web-based alternative rather than a Tableau workbook. No Tableau workbook is used or included.

### 3. Data scope and structure

The supplied Seattle Airbnb source period contains 3,818 unique listings across 87 neighbourhoods. The original daily calendar contains 1,393,570 listing-date observations.

The reproducible Python workflow uses three prepared inputs:

| Input | Records | Analytical grain | Purpose |
|---|---:|---|---|
| `dim_listings.csv` | 3,818 | One row per listing | Listing attributes, asking price, room type, neighbourhood, reviews, coordinates and full-period summary measures. |
| `airbnb_monthly_fact.csv` | 49,634 | Listing × month | Monthly unavailable-night and total-calendar-night counts. |
| `airbnb_asking_price_frequency.csv` | 74,520 | Listing × month × asking price | Published asking-price frequency distribution, including the observation count used for weighted medians. |

`listing_id` is the listing-level key connecting the dimension and monthly facts. The monthly price-frequency input is aggregated using its explicit frequency weights. The final package retains these compact inputs to keep the Python workflow reproducible without carrying a second copy of the entire daily calendar table.

### 4. Data preparation and metric logic

#### 4.1 Unavailable dates

The key source definition is:

- `available = 'f'`: unavailable date;
- `available = 't'`: available date.

The prepared data represents unavailable dates through `is_booked_proxy` or the aggregated `unavailable_nights` fields. This is a **booked-night proxy only**. Unavailability can result from a reservation, owner use, maintenance or another host block. It must not be described as confirmed paid occupancy.

#### 4.2 Core measures

| Measure | Calculation | Grain / interpretation |
|---|---|---|
| Active Listings | Distinct count of `listing_id` | Counts each selected listing once. |
| Median Listing Price | Median of `listing_price` | Calculated at listing grain; daily repetition must not give a listing extra weight. |
| Unavailable Nights (Booked Proxy) | Sum of unavailable-night counts | Calendar dates marked unavailable. |
| Total Calendar Nights | Sum of calendar-night counts | Denominator for the unavailable-night rate. |
| Unavailable-Night Rate | Unavailable Nights ÷ Total Calendar Nights | Share of calendar observations marked unavailable. |
| Availability Rate | 1 − Unavailable-Night Rate | Complement of the unavailable-night rate; not a verified occupancy measure. |
| Monthly Median Published Asking Price | Weighted median of `published_asking_price`, weighted by `price_observation_count` | Represents published asking-price observations on available dates. |
| Estimated Revenue Potential | Listing asking price × unavailable nights | A simple proxy supplied for directional comparison, not realized revenue or profit. |

The monthly asking-price calculation uses the frequency counts when finding the median. Taking the median of the summary rows without those weights would give an incorrect result. The listing-level median similarly counts every listing once.

### 5. Validation results

The Python workflow was executed against the included input files. Its validation report records:

| Check | Result |
|---|---:|
| Unique listings | 3,818 |
| Neighbourhoods | 87 |
| Listing-month rows | 49,634 |
| Asking-price frequency rows | 74,520 |
| Unavailable nights (proxy) | 459,028 |
| Total calendar nights | 1,393,570 |
| Unavailable-night rate | 32.9390% |
| Availability rate | 67.0610% |
| Listing-level median asking price | $100.00 |
| Monthly fact totals reconcile with listing dimension | Yes |

The overall unavailable-night rate is calculated as 459,028 ÷ 1,393,570. The 67.0610% availability rate is its complement; it should not be relabelled as an occupancy rate.

### 6. Findings and interpretation

#### 6.1 Neighbourhood price variation

The overall listing-level median asking price is **$100**. The highest neighbourhood medians include:

| Neighbourhood | Listings | Median asking price | Unavailable-night rate |
|---|---:|---:|---:|
| Briarcliff | 14 | $173.50 | 13.46% |
| Pioneer Square | 23 | $150.00 | 21.22% |
| Westlake | 17 | $150.00 | 38.89% |
| Southeast Magnolia | 17 | $150.00 | 18.36% |
| Industrial District | 6 | $150.00 | 14.38% |

The bottom of the neighbourhood price ranking includes Olympic Hills ($55.50 median; 16 listings), Rainier Beach ($60; 18 listings), South Beacon Hill ($60; 4 listings), Victory Heights ($65; 15 listings) and Bitter Lake ($65; 13 listings). Small neighbourhood samples should be interpreted cautiously; South Beacon Hill, for example, has only four listings in this dataset.

A high asking-price median does not automatically coincide with a high unavailable-night rate. Briarcliff has the highest median price among neighbourhoods but a relatively low unavailable-night rate. Westlake combines a high median price with a higher unavailable-night rate, illustrating why price and calendar status should be reviewed together rather than treated as interchangeable indicators.

#### 6.2 Neighbourhoods above both reference levels

Using the overall listing median ($100) and overall unavailable-night rate (32.94%) as descriptive reference points, several neighbourhoods sit above both thresholds. Examples with larger listing samples include Belltown (234 listings; $139 median; 37.57% unavailable-night rate), First Hill (108; $127; 40.89%), Lower Queen Anne (94; $119; 43.25%), East Queen Anne (82; $125; 40.08%) and Madrona (47; $125; 43.49%).

These areas are candidates for further investigation, not a ranked investment recommendation. Differences in listing mix, seasonality, host blocking and sample size can influence the observed rates.

#### 6.3 Room-type differences

| Room type | Listings | Median asking price | Unavailable-night rate |
|---|---:|---:|---:|
| Entire home/apt | 2,541 | $126 | 36.04% |
| Private room | 1,160 | $69 | 27.59% |
| Shared room | 117 | $40 | 18.60% |

Entire-home listings have the highest median asking price and the highest unavailable-night rate among the three room types. Shared rooms have both the lowest median price and the lowest unavailable-night rate. This describes the supplied sample; it does not establish that room type causes a difference in demand or returns.

#### 6.4 Monthly pattern

The weighted monthly median published asking price rises from $99 in January 2016 to a high of $115 in July 2016, then generally settles between $106 and $110 from September through December. The monthly unavailable-night rate is highest in January 2016 at 44.59% and reaches 37.29% in July; it declines to 26.44% in December 2016.

January requires special handling: the source contains 28 days per listing in January 2016 and only two days per listing in January 2017. These are partial-month observations and should not be compared with full months as if coverage were equal. The dashboard flags partial January coverage in its seasonality note.

#### 6.5 Instant-bookable comparison

Listings marked instant-bookable have a 32.64% unavailable-night rate (591 listings), compared with 32.99% among listings not marked instant-bookable (3,227 listings). The difference is small in this dataset. It should not be interpreted as evidence that instant booking has no effect or that it causes a change in availability; this is a descriptive comparison without controls for listing and host characteristics.

### 7. Visualization design and implementation

The project is delivered in two complementary forms:

1. **Python analytical charts.** `generate_charts.py` uses pandas, NumPy and Matplotlib to calculate and export ten chart views as PNG and SVG. The code and all three input CSVs are included so that the charts and validation report can be regenerated in Visual Studio Code.
2. **AI-assisted interactive web dashboard.** The web presentation was designed and assembled with AI assistance using HTML, CSS and JavaScript. It provides page navigation, shared filters, chart interactions, neighbourhood selection, Top-N control, a what-if price-change control and filtered CSV export.

The project was **not created in Tableau**. For technical clarity, the chart files in `02_Python_Visualizations/charts/` are generated by Python. The interactive charts inside `Seattle_Airbnb_Interactive_Dashboard.html` are rendered in the browser with JavaScript and SVG from embedded prepared data. The Python charts independently reproduce the same analytical themes; they are not the HTML dashboard's runtime rendering engine.

### 8. Limitations

- An unavailable calendar date is not proof of a confirmed reservation or a paid night.
- Asking prices are published prices, not completed transaction prices.
- Estimated revenue potential is a simple price-times-unavailable-night proxy. It is not revenue, contribution margin, net income or an investment return forecast.
- January 2016 and January 2017 have incomplete calendar coverage.
- Neighbourhood medians can be unstable where listing counts are low.
- The map-style Python chart plots neighbourhood coordinate centroids; it is not a street-level or parcel-level map.
- The price-change scenario holds the unavailable-night rate constant. It is a sensitivity illustration and does not model price elasticity, competitive response or demand changes.
- The supplied submission is a Python plus standalone-web implementation, not a native Tableau workbook or Power BI `.pbix` file.

### 9. Conclusion

The Seattle Airbnb sample shows substantial differences in asking prices and unavailable-night patterns across neighbourhoods and room types. The strongest analytical use of the dashboard is comparative: it helps shortlist areas for deeper research, inspect seasonal patterns and understand how listing attributes relate to the observed calendar. Any investment decision would require additional evidence, including verified reservations, realized nightly rates, operating costs, taxes, seasonality beyond the supplied period and host-level context.
