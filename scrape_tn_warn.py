import requests
import pandas as pd
from io import StringIO

URL = "https://www.tn.gov/content/tn/workforce/general-resources/major-publications0/major-publications-redirect/reports.html"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

print("Downloading Tennessee WARN page...")

response = requests.get(
    URL,
    headers=headers,
    timeout=30
)

response.raise_for_status()

print("Page downloaded successfully.")

tables = pd.read_html(StringIO(response.text))

print(f"Found {len(tables)} tables.")

# Find the table containing WARN data rather than assuming
# it will always be in the same position on the page.
warn_table = None

for table in tables:
    columns = [str(col).lower() for col in table.columns]

    if (
        any("company" in col for col in columns)
        and any("county" in col for col in columns)
        and any("affected" in col for col in columns)
    ):
        warn_table = table
        break

if warn_table is None:
    raise Exception("Could not find the Tennessee WARN table.")

warn_table = warn_table.dropna(how="all")
warn_table.to_csv("tn_warn.csv", index=False)

print(f"Saved {len(warn_table)} WARN records to tn_warn.csv")
