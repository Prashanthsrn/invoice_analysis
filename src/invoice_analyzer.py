# src/process_invoices.py
import csv
import os
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
import argparse

class InvoiceAnalyzer:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir
        self.invoices = self.read_invoices()
        
    def read_invoices(self):
        try:
            invoices = []
            with open(self.input_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['Date'] = datetime.strptime(row['Date'], '%Y-%m-%d')
                    row['Invoice Amount'] = float(row['Invoice Amount'])
                    row['Tags'] = set(tag.strip() for tag in row['Tags'].split(','))
                    invoices.append(row)
            return invoices
        except FileNotFoundError:
            print(f"Error: Input file '{self.input_file}' not found.")
            exit(1)
        except Exception as e:
            print(f"Error reading input file: {str(e)}")
            exit(1)
    
    def get_week_start(self, date):
        return date - timedelta(days=date.weekday())
    
    def generate_report(self, percentile, tag_filter=None):
        weekly_data = defaultdict(list)
        
        for invoice in self.invoices:
            if tag_filter is None or all(tag in invoice['Tags'] for tag in tag_filter):
                week_start = self.get_week_start(invoice['Date'])
                weekly_data[week_start].append(invoice['Invoice Amount'])
        
        report = []
        for week_start, amounts in sorted(weekly_data.items()):
            if amounts:
                percentile_value = np.percentile(amounts, percentile)
                report.append({
                    'Week Start': week_start.strftime('%Y-%m-%d'),
                    f'{percentile}th Percentile': round(percentile_value, 2),
                    'Number of Invoices': len(amounts),
                    'Total Amount': round(sum(amounts), 2),
                    'Average Amount': round(np.mean(amounts), 2)
                })
        return report
    
    def save_report(self, report, filename):
        if not report:
            print(f"No data available for {filename}")
            return
            
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, filename)
        
        with open(output_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=report[0].keys())
            writer.writeheader()
            writer.writerows(report)
            
        print(f"Generated report: {output_path}")
    
    def get_available_tags(self):
        """Get all unique tags from the dataset"""
        all_tags = set()
        for invoice in self.invoices:
            all_tags.update(invoice['Tags'])
        return sorted(list(all_tags))
    
    def generate_all_reports(self, percentile, custom_tags=None):
        # Generate overall report
        print("\nGenerating overall report...")
        overall_report = self.generate_report(percentile)
        self.save_report(overall_report, f'overall_report_p{percentile}.csv')
        
        # Generate report for each individual tag
        available_tags = self.get_available_tags()
        print("\nGenerating individual tag reports...")
        for tag in available_tags:
            tag_report = self.generate_report(percentile, tag_filter={tag})
            self.save_report(tag_report, f'{tag}_report_p{percentile}.csv')
        
        # Generate report for discounted and UPI transactions
        print("\nGenerating combined tag report (discounted + UPI)...")
        discounted_upi_report = self.generate_report(percentile, tag_filter={'discounted', 'upi'})
        self.save_report(discounted_upi_report, f'discounted_upi_report_p{percentile}.csv')
        
        # Generate custom tag report if specified
        if custom_tags:
            print(f"\nGenerating custom tag report...")
            custom_report = self.generate_report(percentile, tag_filter=custom_tags)
            self.save_report(custom_report, f'custom_tag_report_p{percentile}.csv')

def main():
    parser = argparse.ArgumentParser(description='Process invoice data and generate reports')
    parser.add_argument('--percentile', type=float,
                      help='Percentile value (0-100)')
    parser.add_argument('--input', type=str, default='data/invoices.csv',
                      help='Input CSV file path')
    parser.add_argument('--output-dir', type=str, default='reports',
                      help='Output directory for reports')
    parser.add_argument('--tags', type=str, nargs='+',
                      help='Filter by specific tags (space separated)')
    parser.add_argument('--interactive', action='store_true',
                      help='Run in interactive mode')
    
    args = parser.parse_args()
    
    analyzer = InvoiceAnalyzer(args.input, args.output_dir)
    
    if args.interactive:
        # Interactive mode
        while True:
            try:
                percentile = float(input("\nEnter the percentile value (0-100): "))
                if 0 <= percentile <= 100:
                    break
                print("Error: Percentile must be between 0 and 100")
            except ValueError:
                print("Error: Please enter a valid number")
        
        # Show available tags and get custom tags
        available_tags = analyzer.get_available_tags()
        print("\nAvailable tags:", ", ".join(available_tags))
        tags_input = input("Enter tags to filter by (comma-separated), or press Enter to skip: ").strip()
        custom_tags = set(tag.strip() for tag in tags_input.split(',')) if tags_input else None
        
    else:
        # Direct input mode
        if args.percentile is None:
            print("Error: Please provide --percentile value or use --interactive mode")
            exit(1)
        if not 0 <= args.percentile <= 100:
            print("Error: Percentile must be between 0 and 100")
            exit(1)
        percentile = args.percentile
        custom_tags = set(args.tags) if args.tags else None
    
    # Generate reports
    analyzer.generate_all_reports(percentile, custom_tags)
    print("\nReport generation complete!")

if __name__ == "__main__":
    main()