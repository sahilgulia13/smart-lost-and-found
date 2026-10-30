
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


OUTPUT_FILE = Path(__file__).parent / "lost_found_dataset.csv"

CATEGORIES = {
    "Electronics": ["Phone", "Laptop", "Earbuds", "Charger", "Tablet"],
    "Accessories": ["Wallet", "Watch", "Keychain", "Sunglasses", "Bag"],
    "Documents": ["ID Card", "Notebook", "Certificate", "Book", "Folder"],
    "Clothing": ["Jacket", "Hoodie", "Scarf", "Cap", "Umbrella"],
    "Other": ["Water Bottle", "Lunch Box", "Calculator", "Tiffin", "Bottle"]
}

BRANDS = [
    "Apple", "Samsung", "HP", "Dell", "Boat",
    "Sony", "Puma", "Nike", "Milton", "Unknown"
]

LOCATIONS = [
    "Library", "Canteen", "Main Gate", "Classroom",
    "Computer Lab", "Auditorium", "Sports Ground",
    "Parking Area", "Hostel", "Seminar Hall"
]

STATUSES = ["Active", "Claimed", "Returned"]


def generate_records(count=1000, seed=42):
    """Generate reproducible synthetic lost-and-found records."""
    random.seed(seed)
    records = []
    start_date = datetime(2026, 1, 1)

    for number in range(1, count + 1):
        category = random.choice(list(CATEGORIES.keys()))
        item_name = random.choice(CATEGORIES[category])
        report_type = random.choice(["Lost", "Found"])
        status = random.choices(
            STATUSES, weights=[75, 15, 10], k=1
        )[0]

        report_date = start_date + timedelta(
            days=random.randint(0, 300)
        )

        records.append({
            "item_id": f"LF{number:04d}",
            "report_type": report_type,
            "item_name": item_name,
            "category": category,
            "brand": random.choice(BRANDS),
            "color": random.choice([
                "Black", "White", "Blue", "Red",
                "Brown", "Grey", "Green", "Pink"
            ]),
            "location": random.choice(LOCATIONS),
            "description": (
                f"{random.choice(['Small', 'Medium', 'Large', ''])} "
                f"{random.choice(['personal', 'everyday', 'college', ''])} "
                f"{item_name.lower()}"
            ).strip(),
            "date_reported": report_date.strftime("%Y-%m-%d"),
            "contact": f"student{number:04d}@example.com",
            "status": status
        })

    return records


def save_records(records, output_file=OUTPUT_FILE):
    """Write records to a CSV file."""
    if not records:
        raise ValueError("Cannot save an empty dataset.")

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(records[0].keys())
        )
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    records = generate_records(1000)
    save_records(records)

    print(f"Dataset created: {OUTPUT_FILE}")
    print(f"Total records: {len(records)}")
    print("Sample record:")
    print(records[0])
