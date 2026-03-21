"""
Process NCES Public and Private school datasets into a unified JSON file.

Reads both CSVs, filters to valid continental US records, and outputs
a compact JSON with standardized fields.
"""

import csv
import json
import sys
from datetime import date
from pathlib import Path

# Columns we need (by name, so column order differences don't matter)
REQUIRED_COLUMNS = {
    "NAME", "CITY", "STATE", "LATITUDE", "LONGITUDE",
    "TYPE", "ENROLLMENT", "LEVEL_", "COUNTYFIPS",
}

# Continental US states (exclude HI, AK, territories)
CONTINENTAL_US_STATES = frozenset({
    "AL", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
    "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA",
    "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA",
    "WV", "WI", "WY", "DC",
})

# Continental US bounding box (rough validation)
LAT_MIN, LAT_MAX = 24.0, 50.0
LNG_MIN, LNG_MAX = -125.0, -66.0

DATA_DIR = Path("/Users/yahelraviv/documents/data_raw/schools")
OUTPUT_PATH = Path("/tmp/TheHeatMarket/data/schools.json")

SOURCE_FILES = [
    ("public", DATA_DIR / "Public_Schools.csv"),
    ("private", DATA_DIR / "Private_Schools.csv"),
]


def parse_float(value: str) -> float | None:
    """Safely parse a float, returning None on failure."""
    try:
        result = float(value)
        return result
    except (ValueError, TypeError):
        return None


def parse_int(value: str) -> int | None:
    """Safely parse an integer, returning None on failure."""
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def is_valid_continental_coords(lat: float, lng: float) -> bool:
    """Check if coordinates fall within continental US bounding box."""
    return LAT_MIN <= lat <= LAT_MAX and LNG_MIN <= lng <= LNG_MAX


def normalize_level(raw_level: str) -> str:
    """Normalize the LEVEL_ field to a clean string."""
    level = raw_level.strip().title() if raw_level else ""
    # Some common normalizations
    level_map = {
        # Text labels (public schools)
        "Elem": "Elementary",
        "High": "High",
        "Middle": "Middle",
        "Prekindergarten": "Prekindergarten",
        "Not Reported": "",
        "Not Available": "",
        "Not Applicable": "",
        "N/A": "",
        "Other": "Other",
        # Numeric codes (private schools: 1=Elem, 2=Middle, 3=High)
        "1": "Elementary",
        "2": "Middle",
        "3": "High",
    }
    return level_map.get(level, level)


def process_csv(file_path: Path, source_label: str) -> tuple[list[dict], dict]:
    """
    Process a single school CSV file.

    Returns a tuple of (records, stats) where stats contains
    counts for total, skipped, and included records.
    """
    records = []
    stats = {
        "total": 0,
        "skipped_no_coords": 0,
        "skipped_invalid_coords": 0,
        "skipped_non_continental": 0,
        "skipped_no_state": 0,
        "included": 0,
    }

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # Validate that required columns exist
        headers = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - headers
        if missing:
            print(f"  WARNING: Missing columns in {file_path.name}: {missing}")
            print(f"  Available columns: {sorted(headers)}")
            return records, stats

        for row in reader:
            stats["total"] += 1

            state = (row.get("STATE") or "").strip().upper()
            if not state:
                stats["skipped_no_state"] += 1
                continue

            if state not in CONTINENTAL_US_STATES:
                stats["skipped_non_continental"] += 1
                continue

            lat = parse_float(row.get("LATITUDE", ""))
            lng = parse_float(row.get("LONGITUDE", ""))

            if lat is None or lng is None:
                stats["skipped_no_coords"] += 1
                continue

            if not is_valid_continental_coords(lat, lng):
                stats["skipped_invalid_coords"] += 1
                continue

            enrollment = parse_int(row.get("ENROLLMENT", ""))
            level = normalize_level(row.get("LEVEL_", ""))
            county_fips = (row.get("COUNTYFIPS") or "").strip()
            name = (row.get("NAME") or "").strip()
            city = (row.get("CITY") or "").strip()

            if not name:
                continue

            record = {
                "name": name,
                "city": city,
                "state": state,
                "lat": round(lat, 4),
                "lng": round(lng, 4),
                "type": "school",
                "enrollment": enrollment,
                "level": level,
                "county_fips": county_fips,
            }

            records.append(record)
            stats["included"] += 1

    return records, stats


def main() -> None:
    """Process all school CSV files and write combined JSON output."""
    all_records: list[dict] = []
    total_stats: dict[str, int] = {}

    for source_label, file_path in SOURCE_FILES:
        print(f"Processing {source_label}: {file_path.name}")

        if not file_path.exists():
            print(f"  ERROR: File not found: {file_path}")
            continue

        records, stats = process_csv(file_path, source_label)
        all_records.extend(records)

        print(f"  Total rows: {stats['total']:,}")
        print(f"  Skipped (no state): {stats['skipped_no_state']:,}")
        print(f"  Skipped (non-continental): {stats['skipped_non_continental']:,}")
        print(f"  Skipped (no coords): {stats['skipped_no_coords']:,}")
        print(f"  Skipped (invalid coords): {stats['skipped_invalid_coords']:,}")
        print(f"  Included: {stats['included']:,}")

        for key, val in stats.items():
            total_stats[key] = total_stats.get(key, 0) + val

    print(f"\n--- Combined Results ---")
    print(f"Total records processed: {total_stats.get('total', 0):,}")
    print(f"Total included: {len(all_records):,}")

    # Sort by state, then city, then name for deterministic output
    all_records.sort(key=lambda r: (r["state"], r["city"], r["name"]))

    output = {
        "schools": all_records,
        "meta": {
            "count": len(all_records),
            "source": "NCES 2024-25",
            "generated": str(date.today()),
        },
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, separators=(",", ":"))

    file_size_mb = OUTPUT_PATH.stat().st_size / (1024 * 1024)
    print(f"\nOutput written to: {OUTPUT_PATH}")
    print(f"File size: {file_size_mb:.1f} MB")
    print(f"Final school count: {len(all_records):,}")


if __name__ == "__main__":
    main()
