"""
analysis.py
-----------
Runs the exploratory analysis on data/cleaned_dataset.csv and answers a
fixed set of business questions about the Gurgaon real estate market.
Also saves three charts to output/.

Run clean_data.py first to generate data/cleaned_dataset.csv.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CLEAN_PATH = "data/cleaned_dataset.csv"
OUTPUT_DIR = "output"


def load_clean(path: str = CLEAN_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def costliest_flat(df: pd.DataFrame) -> None:
    """Q1: Which is the costliest flat?"""
    row = df.loc[df["price"].idxmax()]
    print(
        f"Q1. The costliest flat is a {row['bhk_count']:.0f} BHK "
        f"{row['property_type']} in {row['socity']} society, "
        f"{row['locality']}, priced at Rs. {row['price']:,}"
    )


def costliest_locality_by_price(df: pd.DataFrame) -> None:
    """Q2: Which locality has the highest average price?"""
    avg_price = df.groupby("locality")["price"].mean()
    locality = avg_price.idxmax()
    print(
        f"Q2. {locality} has the highest average price "
        f"(Rs. {avg_price.max():,.2f})"
    )


def costliest_locality_by_rate(df: pd.DataFrame) -> None:
    """Q3: Which locality has the highest rate per square foot?"""
    avg_rate = df.groupby("locality")["rate_per_sqft"].mean()
    locality = avg_rate.idxmax()
    print(
        f"Q3. {locality} has the highest average rate per sqft "
        f"(Rs. {avg_rate.max():,.2f})"
    )


def ready_vs_under_construction(df: pd.DataFrame) -> None:
    """Q4: Are ready-to-move flats pricier than under-construction ones?"""
    rtm = df[df["status"] == "ready to move"]["price"].mean()
    utc = df[df["status"] == "under construction"]["price"].mean()
    verdict = "Ready to move" if rtm > utc else "Under construction"
    print(
        f"Q4. {verdict} flats are more expensive on average "
        f"(ready to move: Rs. {rtm:,.2f} vs under construction: Rs. {utc:,.2f})"
    )


def rera_price_premium(df: pd.DataFrame) -> None:
    """Q5: Do RERA-approved properties command a price premium?"""
    approved = df[df["rera_approval"] == True]["price"].mean()
    not_approved = df[df["rera_approval"] == False]["price"].mean()
    if approved > not_approved:
        print(
            f"Q5. Yes, RERA-approved properties command a price premium "
            f"(Rs. {approved:,.2f} vs Rs. {not_approved:,.2f})"
        )
    else:
        print(
            f"Q5. No, RERA-approved properties don't command a price premium "
            f"(Rs. {approved:,.2f} vs Rs. {not_approved:,.2f})"
        )


def area_vs_price_plot(df: pd.DataFrame) -> None:
    """Q6: How does area (sqft) affect the price of flats?"""
    plt.figure()
    sns.scatterplot(x="area", y="price", data=df)
    plt.title("Area (sqft) vs Price")
    plt.xlabel("Area (sqft)")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/area_vs_price.png")
    plt.close()
    print(f"Q6. Saved scatter plot -> {OUTPUT_DIR}/area_vs_price.png")


def costliest_bhk(df: pd.DataFrame) -> None:
    """Q7: Which BHK configuration is the most expensive on average?"""
    avg_rate = df[df["bhk_count"] != 0].groupby("bhk_count")["rate_per_sqft"].mean()
    bhk = avg_rate.idxmax()
    print(
        f"Q7. {bhk:.0f} BHK configurations are the most expensive on "
        f"average (Rs. {avg_rate.max():,.2f} per sqft)"
    )


def costliest_property_type(df: pd.DataFrame) -> None:
    """Q8: Which property type (apartment, floor, plot) is costliest?"""
    avg_rate = df.groupby("flat_type")["rate_per_sqft"].mean()
    flat_type = avg_rate.idxmax()
    print(
        f"Q8. {flat_type} is the most expensive property type "
        f"(Rs. {avg_rate.max():,.2f} per sqft)"
    )


def top_companies_by_rate(df: pd.DataFrame, n: int = 5) -> None:
    """Q9: Do certain builders/companies consistently price higher?"""
    top = (
        df.groupby("company_name")["rate_per_sqft"]
        .mean()
        .sort_values(ascending=False)
        .head(n)
        .round(2)
    )
    print(f"Q9. Top {n} companies by average rate per sqft:")
    for company, rate in top.items():
        print(f"    {company}: Rs. {rate:,.2f}")


def correlation_heatmap(df: pd.DataFrame) -> None:
    """Bonus: correlation between price, area, rate_per_sqft and bhk_count."""
    cols = ["price", "area", "rate_per_sqft", "bhk_count"]
    plt.figure()
    sns.heatmap(df[cols].corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation: Price, Area, Rate/Sqft, BHK")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/correlation_heatmap.png")
    plt.close()
    print(f"Bonus. Saved correlation heatmap -> {OUTPUT_DIR}/correlation_heatmap.png")


def area_vs_rate_plot(df: pd.DataFrame) -> None:
    """Q10: Are larger homes always more expensive per square foot?"""
    plt.figure()
    sns.scatterplot(x="area", y="rate_per_sqft", data=df)
    plt.title("Area vs Rate per Sqft")
    plt.xlabel("Area (sqft)")
    plt.ylabel("Rate per Sqft")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/area_vs_rate_per_sqft.png")
    plt.close()
    print(f"Q10. Saved scatter plot -> {OUTPUT_DIR}/area_vs_rate_per_sqft.png")


def main():
    df = load_clean()

    costliest_flat(df)
    costliest_locality_by_price(df)
    costliest_locality_by_rate(df)
    ready_vs_under_construction(df)
    rera_price_premium(df)
    area_vs_price_plot(df)
    costliest_bhk(df)
    costliest_property_type(df)
    top_companies_by_rate(df)
    correlation_heatmap(df)
    area_vs_rate_plot(df)


if __name__ == "__main__":
    main()
