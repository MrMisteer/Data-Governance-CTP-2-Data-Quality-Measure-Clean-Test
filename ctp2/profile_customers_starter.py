"""CTP 2 - Exercise 1 STARTER: profile customers.csv with pandas.
Run from the 02_CTP2 folder:  python profile_customers_starter.py
Goal: measure at least 8 rules (2 per dimension) and copy the numbers into quality_scorecard_template.csv
"""
import pandas as pd

df = pd.read_csv("../shopfast-kit/data/customers.csv", dtype=str)   # dtype=str: keep the raw text (e.g. 01300)
n = len(df)
print("Rows:", n)
print(df.head())

# --- Completeness: how many empty values per column? ---
print("\nEmpty values per column:\n", df.isna().sum())
print("\n Number of rows", )
# --- Uniqueness: is customer_id unique? ---
print("\nDuplicated customer_id rows:", df["customer_id"].duplicated(keep=False).sum())

# TODO 1 (Uniqueness): normalise email (strip + lower case) and count people registered twice

df["email"] = df["email"].str.strip().str.lower()
counts = df["email"].value_counts()
print("\nDuplicated email rows:", counts[counts > 1].sum(), )


# TODO 2 (Validity): count emails that do not match the regex  ^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$   (hint: .str.match)

email_pattern = r'^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$'
is_valid = df['email'].str.match(email_pattern, na=False)
not_match = df[~is_valid]

print(f'Invalid email rows: {len(not_match)}')

# TODO 3 (Consistency): list the distinct values of country with value_counts() - how many spellings for 4 countries?
country_counts = df['country'].value_counts()
print(country_counts)

# TODO 4 (Consistency): count signup_date values that are NOT in the format YYYY-MM-DD
date_pattern = r'^\d{4}-\d{2}-\d{2}$'
is_valid_date = df['signup_date'].str.match(date_pattern, na=False)
not_match_date = df[~is_valid_date]
print(f'Invalid signup_date rows: {len(not_match_date)}')

# TODO 5 (Validity): loyalty_tier values outside bronze / silver / gold / platinum
valid_tiers = ['bronze', 'silver', 'gold', 'platinum']
not_match_tier = df[~df['loyalty_tier'].isin(valid_tiers)]
print(f'Invalid loyalty_tier rows: {len(not_match_tier)}')

# TODO 6 (Accuracy): birth dates in the future or before 1906 (convert the ISO ones with pd.to_datetime)
df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
future_births = df[df['birth_date'] > pd.Timestamp.now()]
old_births = df[df['birth_date'] < pd.Timestamp('1906-01-01')]
print(f'Future birth dates: {len(future_births)}')
print(f'Old birth dates: {len(old_births)}')

# TODO 7 (Validity): French postal codes that do not have 5 digits
french_postal_pattern = r'^[0-9]{5}$'
is_valid_postal = df['postal_code'].str.match(french_postal_pattern, na=False)
not_match_postal = df[~is_valid_postal]
print(f'Invalid French postal codes: {len(not_match_postal)}')

# Bonus: compute score_pct = 100 * (1 - failing_rows / n) for each rule
failing_rows = [
    len(not_match),
    len(not_match_date),
    len(not_match_tier),
    len(future_births),
    len(old_births),
    len(not_match_postal)
]
score_pct = [100 * (1 - failing / n) for failing in failing_rows]
round_score = [ round(s, 3) for s in score_pct]
print(f'Quality scores: {round_score}')