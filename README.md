
## Features
- Generate realistic test invoice data with configurable parameters
- Calculate percentile values for invoice amounts
- Weekly aggregation of invoice data
- Filter analysis based on transaction tags
- Support for both interactive and command-line modes
- Reporting with multiple metrics
- Flexible tag combinations for custom analysis

## Project Structure
```
invoice-analysis/
├── data/
│   └── invoices.csv
├── reports/
│   ├── overall_report_p75.csv
│   ├── cash_report_p75.csv
│   └── ...
├── src/
│   ├── __init__.py
│   ├── generate_test_data.py
│   └── process_invoices.py
├── requirements.txt
└── README.md
```

## Requirements
- Python 3.8 or higher
- NumPy
- pandas

## Installation
1. Clone the repository:
```bash
git clone 
cd invoice-analysis
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Generating Test Data

#### Interactive Mode:
```bash
python src/generate_test_data.py
```

#### Command Line Mode:
```bash
python src/generate_test_data.py --entries 1000 --output data/invoices.csv
```

Parameters:
- `--entries`: Number of invoices to generate
- `--output`: Output file path (default: data/invoices.csv)

### Processing Invoices

#### Interactive Mode:
```bash
python src/process_invoices.py --interactive
```

#### Command Line Mode:
```bash
python src/process_invoices.py --percentile 75 --input data/invoices.csv --output-dir reports
```

Parameters:
- `--percentile`: Percentile value (0-100)
- `--input`: Input CSV file path
- `--output-dir`: Output directory for reports
- `--tags`: Space-separated list of tags to filter by
- `--interactive`: Run in interactive mode

## Input Format

The input CSV file should have the following columns:
- `Date`: Transaction date (YYYY-MM-DD)
- `Invoice Amount`: Transaction amount (decimal number)
- `Tags`: Comma-separated list of tags

Available tags:
- `cash`
- `creditcard`
- `upi`
- `discounted`
- `loyaltycard`

## Output Reports

The system generates several CSV reports:
1. `overall_report_p{percentile}.csv`: Analysis of all transactions
2. Individual tag reports for each available tag
3. Combined tag reports (e.g., discounted + UPI)
4. Custom tag combination reports

Each report includes:
- Week Start
- Percentile Value
- Number of Invoices
- Total Amount
- Average Amount

## Examples

### Example Input
```csv
Date,Invoice Amount,Tags
2024-01-01,156.78,"cash, loyaltycard"
2024-01-02,789.45,"creditcard, discounted"
2024-01-03,234.56,"upi, discounted"
```

### Example Output
```csv
Week Start,75th Percentile,Number of Invoices,Total Amount,Average Amount
2024-01-01,789.45,3,1180.79,393.60
```

### Example Commands

1. Generate 1000 test invoices with specific output location:
```bash
python src/generate_test_data.py --entries 1000 --output data/test_invoices.csv
```

2. Analyze invoices for 90th percentile with custom tags:
```bash
python src/process_invoices.py --percentile 90 --tags cash discounted
```

3. Interactive analysis with custom input file:
```bash
python src/process_invoices.py --interactive --input data/custom_invoices.csv
```

## Assumptions

1. Data Structure:
   - Invoice amounts are positive numbers
   - Dates are in valid format (YYYY-MM-DD)
   - Tags are case-sensitive
   - Each invoice has at least one tag

2. Business Rules:
   - Weekly periods start on Monday
   - Amount ranges vary by payment method:
     * Cash: $20-500
     * Credit Card: $100-1000
     * UPI: $50-800

3. Tag Combinations:
   - Common combinations are weighted more heavily
   - Multiple tags per invoice are allowed
   - All tags are valid for analysis

4. Processing:
   - Percentile calculations use linear interpolation
   - Week aggregation includes partial weeks
   - Empty result sets are handled gracefully