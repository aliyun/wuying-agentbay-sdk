#!/usr/bin/env python3
"""
E-commerce Sales Data Generator

Generates synthetic e-commerce sales data for AgentBay demo purposes.
"""

import csv
import random
from datetime import datetime, timedelta


# Configuration
NUM_RECORDS = 5000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)


# Data pools
CATEGORIES = {
    "Electronics": ["Wireless Mouse", "Mechanical Keyboard", "USB-C Hub", "Webcam", "Bluetooth Headphones",
                   "Laptop Stand", "External SSD", "Power Bank", "HDMI Cable", "Phone Charger"],
    "Clothing": ["Cotton T-Shirt", "Denim Jeans", "Running Jacket", "Wool Sweater", "Canvas Sneakers",
                "Baseball Cap", "Winter Scarf", "Sport Socks", "Hoodie", "Cargo Pants"],
    "Home & Garden": ["Coffee Maker", "Vacuum Cleaner", "Air Purifier", "Desk Lamp", "Storage Bins",
                     "Kitchen Scale", "Cutting Board Set", "Plant Pot", "Door Mat", "Wall Clock"],
    "Books": ["Python Programming", "Data Science Handbook", "Business Strategy", "Fiction Novel", "Cookbook",
             "Self-Help Guide", "History Book", "Biography", "Travel Guide", "Children's Book"],
    "Sports": ["Yoga Mat", "Dumbbell Set", "Running Shoes", "Tennis Racket", "Resistance Bands",
              "Water Bottle", "Gym Bag", "Jump Rope", "Foam Roller", "Sports Watch"],
    "Toys": ["Building Blocks", "Board Game", "Action Figure", "Puzzle Set", "Remote Control Car",
            "Stuffed Animal", "Art Supply Kit", "Educational Toy", "Outdoor Play Set", "Card Game"]
}

BRANDS = {
    "Electronics": ["TechPro", "DigitalEdge", "ConnectPlus", "PowerTech", "SmartGear"],
    "Clothing": ["UrbanStyle", "FitWear", "ClassicThreads", "ActiveLife", "TrendSet"],
    "Home & Garden": ["HomeEssentials", "ComfortZone", "ModernLiving", "GardenPro", "CozyHome"],
    "Books": ["TechBooks", "ReadMore", "KnowledgePress", "PageTurner", "WisdomPublishing"],
    "Sports": ["AthleteX", "FitLife", "SportsPro", "ActiveGear", "PeakPerformance"],
    "Toys": ["PlayTime", "FunFactory", "KidJoy", "CreativePlay", "HappyToys"]
}

REGIONS = {
    "North America": ["New York", "Los Angeles", "Chicago", "Toronto", "San Francisco", "Boston", "Seattle"],
    "Europe": ["London", "Paris", "Berlin", "Amsterdam", "Madrid", "Rome", "Stockholm"],
    "Asia Pacific": ["Singapore", "Tokyo", "Sydney", "Hong Kong", "Seoul", "Bangkok", "Melbourne"],
    "Latin America": ["Mexico City", "São Paulo", "Buenos Aires", "Santiago", "Bogotá", "Lima"]
}

CUSTOMER_SEGMENTS = ["Premium", "Regular", "New"]
PAYMENT_METHODS = ["Credit Card", "PayPal", "Bank Transfer", "Digital Wallet"]
SHIPPING_METHODS = ["Standard", "Express", "Next Day"]

# Price ranges by category (min, max)
PRICE_RANGES = {
    "Electronics": (19.99, 299.99),
    "Clothing": (15.99, 149.99),
    "Home & Garden": (24.99, 399.99),
    "Books": (9.99, 59.99),
    "Sports": (14.99, 249.99),
    "Toys": (9.99, 89.99)
}


def generate_order_id(date: datetime, index: int) -> str:
    """Generate a unique order ID."""
    return f"ORD{date.strftime('%Y%m%d')}{index:04d}"


def generate_product_id(category: str, product_name: str) -> str:
    """Generate a consistent product ID based on category and name."""
    # Create a simple hash-like ID
    cat_code = category[:4].upper()
    name_hash = sum(ord(c) for c in product_name) % 1000
    return f"PROD{cat_code}{name_hash:03d}"


def generate_customer_id(num: int) -> str:
    """Generate a customer ID."""
    return f"CUST{num:04d}"


def random_date(start: datetime, end: datetime) -> datetime:
    """Generate a random date between start and end."""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


def generate_sales_data(num_records: int) -> list:
    """Generate synthetic e-commerce sales data."""
    records = []
    order_counter = 1

    # Create a pool of customers
    num_customers = num_records // 3  # Average 3 orders per customer
    customer_ids = [generate_customer_id(i) for i in range(1, num_customers + 1)]

    # Assign segments to customers (with distribution)
    customer_segments = {}
    for cid in customer_ids:
        segment = random.choices(
            CUSTOMER_SEGMENTS,
            weights=[0.15, 0.60, 0.25],  # 15% Premium, 60% Regular, 25% New
            k=1
        )[0]
        customer_segments[cid] = segment

    for _ in range(num_records):
        # Select date
        order_date = random_date(START_DATE, END_DATE)

        # Select category and product
        category = random.choice(list(CATEGORIES.keys()))
        product_name = random.choice(CATEGORIES[category])
        brand = random.choice(BRANDS[category])

        # Generate IDs
        order_id = generate_order_id(order_date, order_counter)
        product_id = generate_product_id(category, product_name)
        customer_id = random.choice(customer_ids)

        # Pricing
        min_price, max_price = PRICE_RANGES[category]
        unit_price = round(random.uniform(min_price, max_price), 2)

        # Quantity (biased towards 1-3 items)
        quantity = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 15, 7, 3], k=1)[0]
        total_amount = round(unit_price * quantity, 2)

        # Customer segment
        segment = customer_segments[customer_id]

        # Region and city
        region = random.choice(list(REGIONS.keys()))
        city = random.choice(REGIONS[region])

        # Payment and shipping (Premium customers prefer faster shipping)
        payment_method = random.choice(PAYMENT_METHODS)
        if segment == "Premium":
            shipping_method = random.choices(
                SHIPPING_METHODS,
                weights=[0.2, 0.3, 0.5],
                k=1
            )[0]
        else:
            shipping_method = random.choices(
                SHIPPING_METHODS,
                weights=[0.6, 0.3, 0.1],
                k=1
            )[0]

        # Create record
        record = {
            "Date": order_date.strftime("%Y-%m-%d"),
            "OrderID": order_id,
            "ProductID": product_id,
            "ProductName": product_name,
            "Category": category,
            "Brand": brand,
            "UnitPrice": unit_price,
            "Quantity": quantity,
            "TotalAmount": total_amount,
            "CustomerID": customer_id,
            "CustomerSegment": segment,
            "Region": region,
            "City": city,
            "PaymentMethod": payment_method,
            "ShippingMethod": shipping_method
        }

        records.append(record)
        order_counter += 1

    # Sort by date
    records.sort(key=lambda x: x["Date"])

    return records


def save_to_csv(records: list, filename: str):
    """Save records to CSV file."""
    if not records:
        print("No records to save!")
        return

    fieldnames = list(records[0].keys())

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"✓ Generated {len(records)} records")
    print(f"✓ Saved to {filename}")


def print_statistics(records: list):
    """Print basic statistics about the generated data."""
    total_revenue = sum(r["TotalAmount"] for r in records)
    categories = {}
    segments = {}
    regions = {}

    for record in records:
        cat = record["Category"]
        categories[cat] = categories.get(cat, 0) + 1

        seg = record["CustomerSegment"]
        segments[seg] = segments.get(seg, 0) + 1

        reg = record["Region"]
        regions[reg] = regions.get(reg, 0) + 1

    print("\n" + "=" * 60)
    print("Dataset Statistics")
    print("=" * 60)
    print(f"Total Orders: {len(records)}")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Average Order Value: ${total_revenue/len(records):.2f}")
    print(f"\nDate Range: {records[0]['Date']} to {records[-1]['Date']}")

    print(f"\nOrders by Category:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(records) * 100
        print(f"  {cat}: {count} ({pct:.1f}%)")

    print(f"\nOrders by Customer Segment:")
    for seg, count in sorted(segments.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(records) * 100
        print(f"  {seg}: {count} ({pct:.1f}%)")

    print(f"\nOrders by Region:")
    for reg, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(records) * 100
        print(f"  {reg}: {count} ({pct:.1f}%)")
    print("=" * 60)


def main():
    """Main function."""
    import os

    print("Generating e-commerce sales data...")
    print(f"Target records: {NUM_RECORDS}")
    print(f"Date range: {START_DATE.date()} to {END_DATE.date()}")
    print()

    # Generate data
    records = generate_sales_data(NUM_RECORDS)

    # Save to file in ../data/ directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    output_file = os.path.join(data_dir, "ecommerce_sales.csv")

    save_to_csv(records, output_file)

    # Print statistics
    print_statistics(records)

    print(f"\n✓ Data generation complete!")
    print(f"✓ File ready for use: {output_file}")


if __name__ == "__main__":
    main()
