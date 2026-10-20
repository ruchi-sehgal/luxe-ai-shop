from pathlib import Path

import openpyxl

from backend.database import db

XLSX_FILE = Path(__file__).parent / "bulk_upload.xlsx"


def parse_row(row: dict) -> dict:
    sizes = [s.strip() for s in (row["size"] or "").split(",") if s.strip()]
    colours = [c.strip() for c in (row["color"] or "").split(",") if c.strip()]
    return {
        "name": row["name"],
        "description": row["description"],
        "price": row["price"],
        "category": row["category"],
        "sizes": sizes,
        "colours": colours,
        "image_url": f"/images/{row['image']}",
    }


def main() -> None:
    wb = openpyxl.load_workbook(XLSX_FILE, data_only=True)
    ws = wb["Products"]
    rows = ws.iter_rows(values_only=True)
    headers = next(rows)

    products = [parse_row(dict(zip(headers, row))) for row in rows if row[0]]

    db.products.delete_many({})
    db.products.insert_many(products)
    print(f"Inserted {len(products)} products into '{db.name}'")


if __name__ == "__main__":
    main()