# src/generate_test_data.py
import csv
import random
from datetime import datetime, timedelta
import os
import argparse

def generate_test_data(num_entries, output_file):
    """Generate random invoice data and save to CSV."""
    tags = ['discounted', 'loyaltycard', 'upi', 'cash', 'creditcard']
    
    # Common tag combinations with their probabilities
    tag_combinations = [
        (["cash", "loyaltycard"], 0.15),
        (["creditcard", "discounted"], 0.15),
        (["upi", "discounted"], 0.15),
        (["cash"], 0.1),
        (["creditcard"], 0.1),
        (["upi"], 0.1),
        (["cash", "discounted", "loyaltycard"], 0.05),
        (["creditcard", "discounted", "loyaltycard"], 0.1),
        (["upi", "discounted", "loyaltycard"], 0.1)
    ]

    # Amount ranges for different payment types
    amount_ranges = {
        "cash": (20, 500),
        "creditcard": (100, 1000),
        "upi": (50, 800)
    }
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Invoice Amount', 'Tags'])
        
        start_date = datetime(2024, 1, 1)
        entries_per_day = max(1, num_entries // 90)  # Spread entries over ~90 days
        
        for i in range(num_entries):
            # Calculate date
            current_date = start_date + timedelta(days=i // entries_per_day)
            
            # Select random tag combination based on probabilities
            tags, _ = random.choices(tag_combinations, 
                weights=[p for _, p in tag_combinations])[0]
            
            # Determine amount range based on payment method
            payment_method = next(tag for tag in tags 
                if tag in amount_ranges.keys())
            min_amount, max_amount = amount_ranges[payment_method]
            
            # Generate amount with some randomness
            amount = round(random.uniform(min_amount, max_amount), 2)
            
            writer.writerow([
                current_date.strftime('%Y-%m-%d'),
                amount,
                ', '.join(tags)
            ])

    print(f"Generated {num_entries} invoices in {output_file}")

def get_num_entries():
    """Get number of entries from user input"""
    while True:
        try:
            num = int(input("Enter the number of invoices to generate: "))
            if num > 0:
                return num
            print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")

def main():
    parser = argparse.ArgumentParser(description='Generate test invoice data')
    parser.add_argument('--entries', type=int, help='Number of invoices to generate')
    parser.add_argument('--output', type=str, default='data/invoices.csv',
                      help='Output file path')
    
    args = parser.parse_args()
    
    # If entries not provided via command line, ask interactively
    num_entries = args.entries if args.entries is not None else get_num_entries()
    
    generate_test_data(num_entries, args.output)

if __name__ == "__main__":
    main()