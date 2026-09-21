# Gurgaon Real Estate Price Analysis

Exploratory data analysis on ~19,500 property listings from Gurgaon, exploring
what drives price and rate-per-sqft across localities, builders, RERA status,
and configuration (BHK).

## Project structure

```
gurgaon-real-estate-analysis/
├── data/
│   ├── raw_data.csv            # Original scraped/exported listings
│   └── cleaned_dataset.csv     # Output of src/clean_data.py
├── src/
│   ├── clean_data.py           # Cleans raw_data.csv -> cleaned_dataset.csv
│   └── analysis.py             # Answers the analysis questions, saves charts
├── output/
│   ├── area_vs_price.png
│   ├── area_vs_rate_per_sqft.png
│   └── correlation_heatmap.png
├── requirements.txt
└── README.md
```

## How to run

```bash
pip install -r requirements.txt
python src/clean_data.py   # writes data/cleaned_dataset.csv
python src/analysis.py     # prints insights, writes charts to output/
```

## Data cleaning

Starting from the raw export, `clean_data.py`:

- Normalizes column names (lowercase, snake_case).
- Drops exact duplicate rows.
- Converts `price` and `rate_per_sqft` from comma-formatted strings to numeric.
- Lowercases and trims categorical fields (locality, builder, society, etc.).
- Maps `rera_approval` text to a boolean.
- Standardizes `status` so `'new'` and `'resale'` both become `'ready to move'`.
- Drops rows missing `bhk_count` or `price`, and keeps only 0–6 BHK listings
  as plausible values for this market.
- Fixes a handful of known `company_name` typos (e.g. `camelliaass` /
  `cameliaas` -> `camellias`) where the scraper had fallen back to a
  misspelled society name. A companion `find_fuzzy_duplicates()` check flags
  other near-identical spellings for manual review — it does not merge them
  automatically, since at a similarity threshold that catches real typos,
  genuinely different builder names (e.g. `right` vs `bright`) score just as
  high, and an automatic merge would silently corrupt distinct names.

This takes the dataset from ~19,500 raw rows to ~14,100 clean rows.

## Key insights

1. **Costliest flat:** a 6 BHK unit in DLF Camellias, Sector 42, at ~₹122.6 crore.
2. **Priciest locality by average price:** Baliawas.
3. **Priciest locality by rate/sqft:** Sector 42 (~₹56,400/sqft) — driven by
   ultra-luxury societies like DLF Camellias.
4. **Ready-to-move vs. under-construction:** ready-to-move flats are slightly
   more expensive on average, though the gap is small.
5. **RERA premium:** RERA-approved listings do *not* command a price premium
   in this dataset — non-approved listings actually average higher, likely
   because many older/luxury resale listings predate RERA requirements.
6. **Area vs. price / rate per sqft:** price does not scale linearly with
   area — very large plots and independent houses often have a *lower*
   rate per sqft than compact high-rise apartments, because land-heavy
   listings are priced more on absolute land value than on built-up rate.
7. **BHK vs. rate per sqft:** 6 BHK configurations command the highest
   average rate per sqft, reflecting the premium on large luxury homes.
8. **Property type:** villas are the most expensive property type by
   rate per sqft.
9. **Builders:** a small number of premium societies (Camellias, Tulip,
   Magnolias) dominate the top rate-per-sqft bracket.
10. **Correlation:** price correlates most with rate per sqft (0.62) and
    moderately with BHK count (0.32); raw area has a weak correlation with
    both price and rate per sqft, reinforcing that location and build quality
    matter more than size alone.

See `output/` for the supporting charts.

## Known limitations / next steps

- `company_name` still has a few unresolved near-duplicates flagged by
  `find_fuzzy_duplicates()` (e.g. `arayaa` vs `arayaaa`, `plotssss` vs
  `plotsss`) that haven't been manually confirmed as typos yet — check the
  console output of `clean_data.py` and extend `COMPANY_NAME_FIXES` as
  needed.
- No geocoding yet — locality-level insights are based on listing labels only.
- A Power BI dashboard on top of `cleaned_dataset.csv` is planned as a
  follow-up for interactive exploration.

## Tools

Python, pandas, seaborn, matplotlib.
