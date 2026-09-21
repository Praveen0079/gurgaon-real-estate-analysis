def list_unique_dealers(df: pd.DataFrame) -> list:
    """Returns every property dealer/agent with no duplicates, sorted."""
    dealers = sorted(df["builder_name"].dropna().unique())
    print(f"Found {len(dealers)} unique property dealers.")

    review = find_fuzzy_duplicates(df["builder_name"])
    if review:
        print("Possible duplicate dealer spellings - review before merging:")
        for variant, looks_like in review.items():
            print(f"  {variant!r} looks similar to {looks_like!r}")

    return dealers
printf(review);
