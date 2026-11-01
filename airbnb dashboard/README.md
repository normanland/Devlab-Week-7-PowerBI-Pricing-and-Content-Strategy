# Seattle Airbnb | Market Intelligence Dashboard

A Seattle Airbnb analytics project focused on neighbourhood pricing, listing characteristics, calendar availability patterns and investor-oriented comparisons.

The submission combines a reproducible Python visualization workflow with an interactive, AI-assisted web dashboard. It is designed to make the analytical results inspectable both as source code and as a browser-based presentation.

## Project at a glance

| Item | Scope |
|---|---:|
| Unique listings | 3,818 |
| Neighbourhoods | 87 |
| Source calendar observations | 1,393,570 |
| Listing-month records used by the Python workflow | 49,634 |
| Asking-price frequency records | 74,520 |
| Python-generated chart views | 10 |

## What is included

### Interactive web dashboard

Open `01_Web_Dashboard/Seattle_Airbnb_Interactive_Dashboard.html` in a modern browser. The dashboard is a standalone HTML file and does not require a database, web server or external JavaScript library.

It contains five views:

- **Neighbourhood Benchmark** — listing and price KPIs, neighbourhood price and unavailable-night-rate comparisons, a neighbourhood table and a price-versus-rate quadrant.
- **Seasonality** — monthly published asking-price and unavailable-night-rate trends.
- **Listing Characteristics** — price distribution by room type, unavailable-night rate by room type, instant-bookable comparison and review-count scatter plot.
- **Geographic Analysis** — neighbourhood concentration and a dynamic Top-N comparison.
- **Neighbourhood Detail** — selected-neighbourhood summary, room-type mix, monthly trend and a price-change sensitivity control.

Global controls cover neighbourhood, room type, price band, instant-bookable status and month range. Selecting a neighbourhood from the comparison table or charts updates the dashboard context. The dashboard also provides filtered CSV export.

### Python visualizations

`02_Python_Visualizations/generate_charts.py` independently calculates the core analytical views with pandas, NumPy and Matplotlib. It exports each chart in PNG and SVG formats.

The ten outputs are:

1. Median listing price by neighbourhood.
2. Unavailable-night rate by neighbourhood.
3. Neighbourhood price-versus-rate investment quadrant.
4. Monthly median published asking price.
5. Monthly unavailable-night rate.
6. Listing-price distribution by room type.
7. Unavailable-night rate by room type.
8. Instant-bookable comparison.
9. Reviews versus unavailable-night rate.
10. Seattle neighbourhood concentration using neighbourhood coordinate centroids.

The contact sheet is available at `02_Python_Visualizations/charts_overview.jpg`. Derived metric tables are stored in `02_Python_Visualizations/chart_data/`, and the validation output is `02_Python_Visualizations/validation_report.txt`.

## Run the Python project

1. Open the `02_Python_Visualizations` folder in Visual Studio Code.
2. Open the integrated terminal.
3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Generate the charts and derived tables:

   ```bash
   python generate_charts.py
   ```

The script reads the three CSV files from `data/` and writes the PNG/SVG charts, metric tables and validation report to their respective folders. The supplied `run_charts.bat` can also be used on Windows.

## Repository structure

```text
seattle airbnb dashboard/
├── Web Dashboard/
│   └── seattle airbnb dashboard.html
├── python visualizations/
│   ├── data/
│   │   ├── dim listings.csv
│   │   ├── airbnb monthly fact.csv
│   │   └── airbnb asking price frequency.csv
│   ├── charts/                 # 10 charts, PNG and SVG
│   ├── chart data/             # derived analytical tables
│   ├── generated charts.py
│   ├── requirements.txt
├── README.md
└── note.md
```

## Data files and analytical grain

The Python workflow uses three prepared CSV files:

- `dim_listings.csv` — one record per listing, including listing attributes and full-period summary metrics.
- `airbnb_monthly_fact.csv` — one record per listing and month, with unavailable-night and total-calendar-night counts.
- `airbnb_asking_price_frequency.csv` — published asking-price observations grouped by listing, month and price, with `price_observation_count` as the frequency weight.

The original calendar source contains 1,393,570 listing-date observations. The final submission keeps the compact listing-level and monthly inputs needed to reproduce the delivered analysis; it does not include a duplicate copy of the full daily calendar table.

## Metric definitions

- **Active Listings** = distinct listing count in the current filter context.
- **Median Listing Price** = median of listing-level asking prices, with each listing counted once.
- **Unavailable Nights (Booked Proxy)** = sum of unavailable calendar nights.
- **Unavailable-Night Rate** = unavailable nights divided by total calendar nights.
- **Availability Rate** = one minus the unavailable-night rate.
- **Monthly Median Published Asking Price** = frequency-weighted median of published asking-price observations, using `price_observation_count`.
- **Estimated Revenue Potential** = listing asking price multiplied by unavailable nights. This is a directional proxy, not realized revenue or profit.

## Tools and implementation

- **Python:** pandas, NumPy and Matplotlib for data loading, metric calculations, validation and ten exported chart views.
- **Web presentation:** HTML, CSS and JavaScript, with SVG-based browser chart rendering and interactive filters.
- **AI assistance:** used during the design and implementation of the web presentation and to support the dashboard development workflow.

This project was not built in Tableau. It is submitted as a Python visualization project with an AI-assisted web dashboard. The Python charts are reproducible outputs from `generate_charts.py`; the interactive charts inside the standalone HTML are rendered in the browser with JavaScript and SVG. The Python exports and the HTML dashboard are complementary presentations of the same analytical themes, not one shared chart-rendering engine.

## Important interpretation notes

The source field `available = 'f'` indicates that a calendar date is unavailable. It does not prove that the date was occupied by a confirmed, paid reservation; host-blocked dates may also be included. For that reason, this project uses **Unavailable-Night Rate** and **Booked Proxy** rather than claiming verified occupancy.

Published asking prices are not transaction prices. The estimated revenue metric is not a verified revenue measure. January 2016 has 28 days of source coverage per listing and January 2017 has only two; both should be treated as partial months in seasonal comparisons.

See [`note.md`](note.md) for the analytical rationale, findings and limitations.
