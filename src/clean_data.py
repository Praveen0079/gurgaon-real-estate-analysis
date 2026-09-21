"""
clean_data.py
-------------
Cleans the raw Gurgaon real estate listing data scraped/exported into
data/raw_data.csv and writes a tidy version to data/cleaned_dataset.csv.

Cleaning steps:
    1. Normalize column names (lowercase, strip, snake_case).
    2. Drop exact duplicate rows.
    3. Convert price and rate_per_sqft to numeric (strip commas).
    4. Lowercase + strip categorical text columns.
    5. Map rera_approval text to a boolean.
    6. Standardize status values ('new' / 'resale' -> 'ready to move').
    7. Drop rows missing bhk_count or price, and drop implausible
       BHK counts (keeping 0-6, per project scope).
"""

import difflib

import pandas as pd

RAW_PATH = "data/raw_data.csv"
CLEAN_PATH = "data/cleaned_dataset.csv"

# Known typos in company_name, found by manually reviewing the top
# rate-per-sqft companies. These all come from a batch of Golf Course Road
# listings where the scraper fell back to the (misspelled) society name
# instead of an actual builder name.
COMPANY_NAME_FIXES = {
    "camelliaass": "camellias",
    "cameliaas": "camellias",
    "magnoliaaa": "magnolias",
    "magnoliaass": "magnolias",
    "villasss": "villas",
}

CATEGORICAL_COLUMNS = [
    "status",
    "property_type",
    "builder_name",
    "locality",
    "socity",
    "company_name",
    "flat_type",
]

RERA_MAP = {
    "Approved by RERA": True,
    "Not approved by RERA": False,
}

STATUS_MAP = {
    "new": "ready to move",
    "resale": "ready to move",
}


def load_raw(path: str = RAW_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1. Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # 2. Drop duplicates
    df = df.drop_duplicates()

    # 3. Numeric cleaning
    df["price"] = df["price"].astype(str).str.replace(",", "").astype(int)
    df["rate_per_sqft"] = (
        df["rate_per_sqft"].astype(str).str.replace(",", "").astype(float)
    )

    # 4. Categorical cleaning
    for col in CATEGORICAL_COLUMNS:
        df[col] = df[col].str.strip().str.lower()

    # 4b. Fix known company_name typos (see COMPANY_NAME_FIXES above)
    df["company_name"] = df["company_name"].replace(COMPANY_NAME_FIXES)

    # 5. RERA approval -> boolean (mapped before any lowercasing, since the
    # raw text is title-case and isn't part of CATEGORICAL_COLUMNS)
    df["rera_approval"] = df["rera_approval"].str.strip().map(RERA_MAP)

    # 6. Standardize status categories
    df["status"] = df["status"].replace(STATUS_MAP)

    # 7. Outlier / missing-value handling
    df = df.dropna(subset=["bhk_count", "price"])
    df = df.query("0 <= bhk_count <= 6")

    return df


def find_fuzzy_duplicates(series: pd.Series, threshold: float = 0.9) -> dict:
    """
    Flags pairs of near-identical spellings (e.g. a typo with a repeated
    trailing letter) for manual review.

    This does NOT merge anything automatically: at this similarity
    threshold, genuinely different names (e.g. 'right' vs 'bright',
    'dharma' vs 'dhara') score just as high as real typos (e.g.
    'camelliaass' vs 'cameliaas'), so an automatic merge would silently
    corrupt distinct builder names. Use the output to extend
    COMPANY_NAME_FIXES by hand once you've confirmed a pair really is
    a typo.
    """
    counts = series.value_counts()
    canonical_names = []
    suggestions = {}
    for name in counts.index:  # most frequent spelling becomes canonical
        match = difflib.get_close_matches(name, canonical_names, n=1, cutoff=threshold)
        if match:
            suggestions[name] = match[0]
        else:
            canonical_names.append(name)
    return suggestions


def main():
    df = load_raw()
    df = clean(df)

    review = find_fuzzy_duplicates(df["company_name"])
    if review:
        print("Possible additional company_name typos - review before fixing:")
        for variant, looks_like in review.items():
            print(f"  {variant!r} looks similar to {looks_like!r}")

    df.to_csv(CLEAN_PATH, index=False)
    print(f"Cleaned {len(df)} rows -> {CLEAN_PATH}")
    print(df.head())


if __name__ == "__main__":
    main()
