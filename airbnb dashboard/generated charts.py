from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHART_DIR = BASE_DIR / "charts"
CHART_DATA_DIR = BASE_DIR / "chart_data"

COLORS = {
    "background": "#0d1533",
    "panel": "#1b2650",
    "panel_alt": "#222f5a",
    "grid": "#34436f",
    "text": "#d9e3fb",
    "muted": "#9eafd2",
    "blue": "#89a9ff",
    "purple": "#b99af5",
    "teal": "#67dbc8",
    "coral": "#ff927e",
    "gold": "#f3c978",
}

ROOM_ORDER = ["Entire home/apt", "Private room", "Shared room"]
ROOM_LABELS = ["Entire home", "Private room", "Shared room"]


def load_data():
    required_files = [
        DATA_DIR / "dim_listings.csv",
        DATA_DIR / "airbnb_monthly_fact.csv",
        DATA_DIR / "airbnb_asking_price_frequency.csv",
    ]
    missing = [path.name for path in required_files if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing data files: " + ", ".join(missing) +
            ". Keep the supplied CSV files in the project's data/ folder."
        )

    listings = pd.read_csv(required_files[0])
    monthly = pd.read_csv(required_files[1])
    asking_prices = pd.read_csv(required_files[2])

    listing_columns = {
        "listing_id", "neighbourhood", "room_type", "listing_price",
        "price_band", "instant_bookable", "number_of_reviews",
        "latitude", "longitude", "unavailable_nights_total",
        "calendar_nights_total", "estimated_revenue_total",
    }
    monthly_columns = {
        "listing_id", "month", "unavailable_nights", "calendar_nights",
    }
    asking_columns = {
        "listing_id", "month", "published_asking_price", "price_observation_count",
    }

    for name, frame, expected in [
        ("dim_listings.csv", listings, listing_columns),
        ("airbnb_monthly_fact.csv", monthly, monthly_columns),
        ("airbnb_asking_price_frequency.csv", asking_prices, asking_columns),
    ]:
        absent = expected.difference(frame.columns)
        if absent:
            raise ValueError(f"{name} is missing required columns: {sorted(absent)}")

    if listings["listing_id"].duplicated().any():
        raise ValueError("dim_listings.csv must contain one row per listing_id.")

    monthly["month"] = pd.to_datetime(monthly["month"] + "-01")
    asking_prices["month"] = pd.to_datetime(asking_prices["month"] + "-01")
    return listings, monthly, asking_prices


def apply_dark_theme():
    plt.rcParams.update({
        "figure.facecolor": COLORS["background"],
        "axes.facecolor": COLORS["panel"],
        "axes.edgecolor": COLORS["panel"],
        "axes.labelcolor": COLORS["muted"],
        "text.color": COLORS["text"],
        "xtick.color": COLORS["muted"],
        "ytick.color": COLORS["muted"],
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titleweight": "bold",
        "axes.titlesize": 16,
        "savefig.facecolor": COLORS["background"],
    })


def style_axis(ax, *, xgrid=False, ygrid=True):
    ax.set_axisbelow(True)
    ax.grid(axis="x" if xgrid else "y", color=COLORS["grid"], linewidth=0.8, alpha=0.8)
    if xgrid and ygrid:
        ax.grid(axis="y", color=COLORS["grid"], linewidth=0.5, alpha=0.35)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0, pad=7)


def save_chart(fig, filename):
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    output_path = CHART_DIR / filename
    fig.savefig(output_path, dpi=200, bbox_inches="tight", pad_inches=0.25)
    fig.savefig(output_path.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def weighted_median(values, weights):
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=np.int64)
    valid = np.isfinite(values) & (weights > 0)
    values = values[valid]
    weights = weights[valid]
    if len(values) == 0:
        return np.nan

    order = np.argsort(values)
    values = values[order]
    weights = weights[order]
    cumulative = np.cumsum(weights)
    total = int(weights.sum())
    lower_position = (total - 1) // 2
    upper_position = total // 2
    lower_index = np.searchsorted(cumulative, lower_position + 1, side="left")
    upper_index = np.searchsorted(cumulative, upper_position + 1, side="left")
    return float((values[lower_index] + values[upper_index]) / 2)


def calculate_metrics(listings, monthly, asking_prices):
    neighbourhood = (
        listings.groupby("neighbourhood", as_index=False)
        .agg(
            listing_count=("listing_id", "nunique"),
            median_price=("listing_price", "median"),
            unavailable_nights=("unavailable_nights_total", "sum"),
            calendar_nights=("calendar_nights_total", "sum"),
            estimated_revenue=("estimated_revenue_total", "sum"),
            latitude=("latitude", "mean"),
            longitude=("longitude", "mean"),
        )
    )
    neighbourhood["unavailable_rate"] = (
        neighbourhood["unavailable_nights"] / neighbourhood["calendar_nights"]
    )
    neighbourhood = neighbourhood.sort_values("median_price", ascending=False)

    room_type = (
        listings.groupby("room_type", as_index=False)
        .agg(
            listing_count=("listing_id", "nunique"),
            median_price=("listing_price", "median"),
            unavailable_nights=("unavailable_nights_total", "sum"),
            calendar_nights=("calendar_nights_total", "sum"),
        )
    )
    room_type["unavailable_rate"] = room_type["unavailable_nights"] / room_type["calendar_nights"]
    room_type["room_type"] = pd.Categorical(room_type["room_type"], ROOM_ORDER, ordered=True)
    room_type = room_type.sort_values("room_type")

    instant = (
        listings.groupby("instant_bookable", as_index=False)
        .agg(
            listing_count=("listing_id", "nunique"),
            median_price=("listing_price", "median"),
            unavailable_nights=("unavailable_nights_total", "sum"),
            calendar_nights=("calendar_nights_total", "sum"),
        )
    )
    instant["unavailable_rate"] = instant["unavailable_nights"] / instant["calendar_nights"]
    instant["instant_bookable"] = pd.Categorical(
        instant["instant_bookable"], ["Yes", "No"], ordered=True
    )
    instant = instant.sort_values("instant_bookable")

    monthly_rate = (
        monthly.groupby("month", as_index=False)
        .agg(
            unavailable_nights=("unavailable_nights", "sum"),
            calendar_nights=("calendar_nights", "sum"),
        )
    )
    monthly_rate["unavailable_rate"] = (
        monthly_rate["unavailable_nights"] / monthly_rate["calendar_nights"]
    )

    price_rows = []
    for month, group in asking_prices.groupby("month", sort=True):
        median_price = weighted_median(
            group["published_asking_price"], group["price_observation_count"]
        )
        price_rows.append({"month": month, "weighted_median_asking_price": median_price})
    monthly_price = pd.DataFrame(price_rows)
    monthly_metrics = monthly_rate.merge(monthly_price, on="month", how="outer").sort_values("month")

    listing_metrics = listings.copy()
    listing_metrics["unavailable_rate"] = (
        listing_metrics["unavailable_nights_total"] / listing_metrics["calendar_nights_total"]
    )

    return neighbourhood, room_type, instant, monthly_metrics, listing_metrics


def chart_neighbourhood_price(neighbourhood):
    data = neighbourhood.nlargest(12, "median_price").sort_values("median_price")
    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    bars = ax.barh(data["neighbourhood"], data["median_price"], color=COLORS["blue"], height=0.66)
    style_axis(ax, xgrid=True, ygrid=False)
    ax.set_title("Median Listing Price by Neighbourhood", loc="left", pad=18)
    ax.set_xlabel("Median asking price (USD)")
    ax.set_xlim(0, data["median_price"].max() * 1.18)
    ax.xaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
    for bar, value in zip(bars, data["median_price"]):
        ax.text(value + 2, bar.get_y() + bar.get_height() / 2, f"${value:,.0f}",
                va="center", ha="left", color=COLORS["text"], fontsize=9)
    fig.text(0.01, 0.01, "Listing-level median; each listing is counted once.", color=COLORS["muted"], fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save_chart(fig, "01_neighbourhood_median_price.png")


def chart_neighbourhood_rate(neighbourhood):
    data = neighbourhood.nlargest(12, "unavailable_rate").sort_values("unavailable_rate")
    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    bars = ax.barh(data["neighbourhood"], data["unavailable_rate"] * 100,
                   color=COLORS["coral"], height=0.66)
    style_axis(ax, xgrid=True, ygrid=False)
    ax.set_title("Unavailable-Night Rate by Neighbourhood", loc="left", pad=18)
    ax.set_xlabel("Unavailable nights / total calendar nights")
    ax.set_xlim(0, max(45, data["unavailable_rate"].max() * 120))
    ax.xaxis.set_major_formatter(lambda value, _: f"{value:.0f}%")
    for bar, value in zip(bars, data["unavailable_rate"] * 100):
        ax.text(value + 0.6, bar.get_y() + bar.get_height() / 2, f"{value:.1f}%",
                va="center", ha="left", color=COLORS["text"], fontsize=9)
    fig.text(0.01, 0.01, "Unavailable dates are a booked-night proxy, not confirmed paid reservations.",
             color=COLORS["muted"], fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save_chart(fig, "02_neighbourhood_unavailable_rate.png")


def chart_investment_quadrant(neighbourhood):
    data = neighbourhood[neighbourhood["listing_count"] >= 2].copy()
    median_price = data["median_price"].median()
    median_rate = data["unavailable_rate"].median()
    sizes = 25 + np.sqrt(data["listing_count"]) * 23
    high = (data["median_price"] >= median_price) & (data["unavailable_rate"] >= median_rate)
    colors = np.where(high, COLORS["teal"], COLORS["blue"])

    fig, ax = plt.subplots(figsize=(12.5, 7.4))
    ax.scatter(data["median_price"], data["unavailable_rate"] * 100,
               s=sizes, c=colors, alpha=0.78, edgecolors="#d5e2ff", linewidths=0.6)
    ax.axvline(median_price, color=COLORS["muted"], linestyle=(0, (4, 4)), linewidth=1.2)
    ax.axhline(median_rate * 100, color=COLORS["muted"], linestyle=(0, (4, 4)), linewidth=1.2)
    style_axis(ax, xgrid=True, ygrid=True)
    ax.set_title("Neighbourhood Comparison · Price vs Unavailable-Night Rate", loc="left", pad=18)
    ax.set_xlabel("Median listing price (USD)")
    ax.set_ylabel("Unavailable-night rate")
    ax.xaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
    ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0f}%")

    label_candidates = data[high].nlargest(8, "listing_count")
    for _, row in label_candidates.iterrows():
        ax.annotate(row["neighbourhood"], (row["median_price"], row["unavailable_rate"] * 100),
                    xytext=(6, 6), textcoords="offset points", fontsize=8, color=COLORS["text"])
    ax.text(0.98, 0.98, f"Median price: ${median_price:,.0f}\nMedian rate: {median_rate:.1%}",
            transform=ax.transAxes, ha="right", va="top", color=COLORS["muted"], fontsize=9,
            bbox={"boxstyle": "round,pad=0.5", "facecolor": COLORS["panel_alt"], "edgecolor": "none"})
    fig.text(0.01, 0.01, "Bubble size represents listing count. Dashed lines mark neighbourhood medians.",
             color=COLORS["muted"], fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save_chart(fig, "03_investment_quadrant.png")


def chart_monthly_price(monthly_metrics):
    data = monthly_metrics.dropna(subset=["weighted_median_asking_price"]).copy()
    fig, ax = plt.subplots(figsize=(12.5, 6.6))
    ax.plot(data["month"], data["weighted_median_asking_price"], color=COLORS["purple"],
            linewidth=2.8, marker="o", markersize=6)
    ax.fill_between(data["month"], data["weighted_median_asking_price"],
                    data["weighted_median_asking_price"].min() - 5,
                    color=COLORS["purple"], alpha=0.10)
    style_axis(ax, xgrid=False, ygrid=True)
    ax.set_title("Monthly Median Published Asking Price", loc="left", pad=18)
    ax.set_ylabel("Weighted median asking price (USD)")
    ax.yaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
    ax.set_xticks(data["month"])
    ax.set_xticklabels(data["month"].dt.strftime("%b '%y"), rotation=0)
    if not data.empty and data["month"].max().month == 1 and data["month"].max().year == 2017:
        last = data.iloc[-1]
        ax.annotate("Jan 2017: partial month\n(2 calendar days)",
                    (last["month"], last["weighted_median_asking_price"]),
                    xytext=(-105, 30), textcoords="offset points", fontsize=8,
                    color=COLORS["gold"], arrowprops={"arrowstyle": "->", "color": COLORS["gold"]})
    fig.text(0.01, 0.01, "Median is weighted by the number of daily asking-price observations per listing and month.",
             color=COLORS["muted"], fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save_chart(fig, "04_monthly_median_asking_price.png")


def chart_monthly_rate(monthly_metrics):
    data = monthly_metrics.dropna(subset=["unavailable_rate"]).copy()
    fig, ax = plt.subplots(figsize=(12.5, 6.6))
    ax.plot(data["month"], data["unavailable_rate"] * 100, color=COLORS["teal"],
            linewidth=2.8, marker="o", markersize=6)
    ax.fill_between(data["month"], data["unavailable_rate"] * 100, 0,
                    color=COLORS["teal"], alpha=0.09)
    style_axis(ax, xgrid=False, ygrid=True)
    ax.set_title("Monthly Unavailable-Night Rate", loc="left", pad=18)
    ax.set_ylabel("Unavailable nights / calendar nights")
    ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0f}%")
    ax.set_ylim(bottom=0)
    ax.set_xticks(data["month"])
    ax.set_xticklabels(data["month"].dt.strftime("%b '%y"), rotation=0)
    fig.text(0.01, 0.01, "Unavailable dates may include host-blocked nights; this is not confirmed occupancy.",
             color=COLORS["muted"], fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save_chart(fig, "05_monthly_unavailable_rate.png")


def chart_room_type_boxplot(listings):
    data = [listings.loc[listings["room_type"] == room, "listing_price"].dropna().to_numpy()
            for room in ROOM_ORDER]
    stats = []
    for label, values in zip(ROOM_LABELS, data):
        stats.append({
            "label": label,
            "whislo": float(np.quantile(values, 0.10)),
            "q1": float(np.quantile(values, 0.25)),
            "med": float(np.quantile(values, 0.50)),
            "q3": float(np.quantile(values, 0.75)),
            "whishi": float(np.quantile(values, 0.90)),
            "fliers": [],
        })

    fig, ax = plt.subplots(figsize=(11.5, 6.8))
    artists = ax.bxp(stats, showfliers=False, patch_artist=True, widths=0.48,
                     medianprops={"color": COLORS["teal"], "linewidth": 2.6},
                     whiskerprops={"color": COLORS["blue"], "linewidth": 1.8},
                     capprops={"color": COLORS["blue"], "linewidth": 1.8},
                     boxprops={"edgecolor": COLORS["blue"], "linewidth": 1.4})
    for patch, color in zip(artists["boxes"], [COLORS["blue"], COLORS["purple"], COLORS["coral"]]):
        patch.set_facecolor(color)
        patch.set_alpha(0.52)
    style_axis(ax, xgrid=False, ygrid=True)
    ax.set_title("Listing Price Distribution by Room Type", loc="left", pad=18)
    ax.set_ylabel("Listing asking price (USD)")
    ax.yaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
    ax.set_ylim(0, min(650, max(250, float(listings["listing_price"].quantile(0.95) * 1.2))))
    fig.text(0.01, 0.01, "Boxes show the 25th–75th percentiles; whiskers show the 10th–90th percentiles.",
             color=COLORS["muted"], fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save_chart(fig, "06_listing_price_distribution_by_room_type.png")


def chart_room_type_rate(room_type):
    data = room_type.copy()
    labels = data["room_type"].astype(str).replace({
        "Entire home/apt": "Entire home", "Private room": "Private room", "Shared room": "Shared room"
    })
    order = np.argsort(data["unavailable_rate"].to_numpy())
    data = data.iloc[order]
    labels = labels.iloc[order]
    fig, ax = plt.subplots(figsize=(11.5, 5.8))
    bars = ax.barh(labels, data["unavailable_rate"] * 100,
                   color=[COLORS["coral"], COLORS["purple"], COLORS["teal"]], height=0.58)
    style_axis(ax, xgrid=True, ygrid=False)
    ax.set_title("Unavailable-Night Rate by Room Type", loc="left", pad=18)
    ax.set_xlabel("Unavailable nights / calendar nights")
    ax.xaxis.set_major_formatter(lambda value, _: f"{value:.0f}%")
    ax.set_xlim(0, max(45, data["unavailable_rate"].max() * 120))
    for bar, value in zip(bars, data["unavailable_rate"] * 100):
        ax.text(value + 0.7, bar.get_y() + bar.get_height() / 2, f"{value:.1f}%",
                va="center", color=COLORS["text"], fontsize=10)
    fig.text(0.01, 0.01, "Descriptive comparison; unavailable dates are not necessarily paid bookings.",
             color=COLORS["muted"], fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save_chart(fig, "07_unavailable_rate_by_room_type.png")


def chart_instant_bookable(instant):
    data = instant.set_index("instant_bookable").reindex(["Yes", "No"]).reset_index()
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.8))
    fig.suptitle("Instant Bookable Comparison", x=0.04, ha="left", y=0.98,
                 fontsize=16, fontweight="bold", color=COLORS["text"])

    axes[0].bar(data["instant_bookable"], data["median_price"],
                color=[COLORS["purple"], COLORS["blue"]], width=0.55)
    axes[0].set_title("Median listing price", loc="left", pad=14, fontsize=12)
    axes[0].set_ylabel("USD")
    axes[0].yaxis.set_major_formatter(lambda value, _: f"${value:,.0f}")
    axes[0].set_ylim(0, data["median_price"].max() * 1.3)
    for i, value in enumerate(data["median_price"]):
        axes[0].text(i, value + data["median_price"].max() * 0.035, f"${value:,.0f}",
                     ha="center", color=COLORS["text"], fontsize=10)
    style_axis(axes[0], xgrid=False, ygrid=True)

    rate_values = data["unavailable_rate"] * 100
    axes[1].bar(data["instant_bookable"], rate_values,
                color=[COLORS["teal"], COLORS["coral"]], width=0.55)
    axes[1].set_title("Unavailable-night rate", loc="left", pad=14, fontsize=12)
    axes[1].set_ylabel("Percent")
    axes[1].yaxis.set_major_formatter(lambda value, _: f"{value:.0f}%")
    axes[1].set_ylim(0, max(45, rate_values.max() * 1.3))
    for i, value in enumerate(rate_values):
        axes[1].text(i, value + 1, f"{value:.1f}%", ha="center", color=COLORS["text"], fontsize=10)
    style_axis(axes[1], xgrid=False, ygrid=True)

    fig.text(0.04, 0.01, "Median price is listing-weighted; unavailable-night rate is calculated from calendar totals.",
             color=COLORS["muted"], fontsize=9)
    fig.tight_layout(rect=(0.02, 0.05, 1, 0.92))
    save_chart(fig, "08_instant_bookable_comparison.png")


def chart_reviews_scatter(listings):
    data = listings[listings["number_of_reviews"] >= 0].copy()
    fig, ax = plt.subplots(figsize=(12.5, 6.8))
    ax.scatter(data["number_of_reviews"], data["unavailable_rate"] * 100,
               s=24, color=COLORS["blue"], alpha=0.42, edgecolors="none")
    style_axis(ax, xgrid=True, ygrid=True)
    ax.set_title("Number of Reviews vs Unavailable-Night Rate", loc="left", pad=18)
    ax.set_xlabel("Number of reviews")
    ax.set_ylabel("Unavailable-night rate")
    ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0f}%")
    ax.set_xlim(left=0)
    ax.set_ylim(0, 105)
    fig.text(0.01, 0.01, "Each point represents one listing. The relationship is descriptive, not causal.",
             color=COLORS["muted"], fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save_chart(fig, "09_reviews_vs_unavailable_rate.png")


def chart_neighbourhood_map(neighbourhood):
    data = neighbourhood.dropna(subset=["latitude", "longitude"]).copy()
    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    scatter = ax.scatter(
        data["longitude"], data["latitude"],
        s=24 + np.sqrt(data["listing_count"]) * 25,
        c=data["median_price"], cmap="plasma", alpha=0.82,
        edgecolors="#d5e2ff", linewidths=0.55,
    )
    style_axis(ax, xgrid=True, ygrid=True)
    ax.set_title("Seattle Listing Concentration by Neighbourhood", loc="left", pad=18)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_xlim(-122.48, -122.23)
    ax.set_ylim(47.48, 47.75)
    ax.set_aspect("equal", adjustable="box")
    colourbar = fig.colorbar(scatter, ax=ax, pad=0.02)
    colourbar.set_label("Median listing price (USD)", color=COLORS["muted"])
    colourbar.ax.yaxis.set_tick_params(color=COLORS["muted"])
    plt.setp(colourbar.ax.get_yticklabels(), color=COLORS["muted"])
    fig.text(0.01, 0.01, "Each point is a neighbourhood centroid; bubble size represents listing count. No basemap is used.",
             color=COLORS["muted"], fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save_chart(fig, "10_seattle_neighbourhood_concentration.png")


def export_chart_data(neighbourhood, room_type, instant, monthly_metrics, listing_metrics):
    CHART_DATA_DIR.mkdir(parents=True, exist_ok=True)
    neighbourhood.to_csv(CHART_DATA_DIR / "neighbourhood_metrics.csv", index=False)
    room_type.assign(room_type=room_type["room_type"].astype(str)).to_csv(
        CHART_DATA_DIR / "room_type_metrics.csv", index=False
    )
    instant.assign(instant_bookable=instant["instant_bookable"].astype(str)).to_csv(
        CHART_DATA_DIR / "instant_bookable_metrics.csv", index=False
    )
    monthly_metrics.assign(month=monthly_metrics["month"].dt.strftime("%Y-%m")).to_csv(
        CHART_DATA_DIR / "monthly_metrics.csv", index=False
    )
    listing_metrics.to_csv(CHART_DATA_DIR / "listing_level_metrics.csv", index=False)


def write_validation_report(listings, monthly, asking_prices, neighbourhood, room_type, monthly_metrics):
    unavailable = int(listings["unavailable_nights_total"].sum())
    calendar_nights = int(listings["calendar_nights_total"].sum())
    unavailable_rate = unavailable / calendar_nights
    median_price = float(listings["listing_price"].median())
    monthly_unavailable = int(monthly["unavailable_nights"].sum())
    monthly_calendar = int(monthly["calendar_nights"].sum())
    january_2017_days = int(
        monthly.loc[monthly["month"] == pd.Timestamp("2017-01-01"), "calendar_nights"].sum()
        / max(listings["listing_id"].nunique(), 1)
    )

    rows = [
        "SEATTLE AIRBNB — PYTHON CHART VALIDATION",
        "=" * 48,
        f"Unique listings: {listings['listing_id'].nunique():,}",
        f"Neighbourhoods: {listings['neighbourhood'].nunique():,}",
        f"Monthly fact rows: {len(monthly):,}",
        f"Asking-price frequency rows: {len(asking_prices):,}",
        f"Unavailable nights (proxy): {unavailable:,}",
        f"Total calendar nights: {calendar_nights:,}",
        f"Unavailable-night rate: {unavailable_rate:.4%}",
        f"Availability rate: {1 - unavailable_rate:.4%}",
        f"Median listing price (listing grain): ${median_price:,.2f}",
        f"Monthly fact totals match listing dimension: {monthly_unavailable == unavailable and monthly_calendar == calendar_nights}",
        f"January 2017 calendar span per listing (approx.): {january_2017_days} day(s)",
        "",
        "Interpretation: available='f' is represented as unavailable_nights / booked proxy.",
        "It is not proof of paid reservations or realized revenue.",
        "Monthly median asking prices use price_observation_count as frequency weights.",
        "Listing median price is calculated once per listing, not from repeated daily rows.",
    ]
    (BASE_DIR / "validation_report.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")


def main():
    apply_dark_theme()
    listings, monthly, asking_prices = load_data()
    neighbourhood, room_type, instant, monthly_metrics, listing_metrics = calculate_metrics(
        listings, monthly, asking_prices
    )

    export_chart_data(neighbourhood, room_type, instant, monthly_metrics, listing_metrics)
    chart_neighbourhood_price(neighbourhood)
    chart_neighbourhood_rate(neighbourhood)
    chart_investment_quadrant(neighbourhood)
    chart_monthly_price(monthly_metrics)
    chart_monthly_rate(monthly_metrics)
    chart_room_type_boxplot(listings)
    chart_room_type_rate(room_type)
    chart_instant_bookable(instant)
    chart_reviews_scatter(listing_metrics)
    chart_neighbourhood_map(neighbourhood)
    write_validation_report(listings, monthly, asking_prices, neighbourhood, room_type, monthly_metrics)

    print("Python chart generation completed.")
    print(f"Charts: {CHART_DIR}")
    print(f"Chart data: {CHART_DATA_DIR}")
    print(f"Validation: {BASE_DIR / 'validation_report.txt'}")
    print(f"Listings: {listings['listing_id'].nunique():,}")
    print(f"Median listing price: ${listings['listing_price'].median():,.0f}")
    print(f"Unavailable-night rate: {listings['unavailable_nights_total'].sum() / listings['calendar_nights_total'].sum():.2%}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Chart generation failed: {error}", file=sys.stderr)
        raise
