#!/usr/bin/env python
import argparse
import csv
import sys
from decimal import Decimal
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument(
    "csv_file", help="input .csv file", type=argparse.FileType("r", encoding="latin-1")
)
parser.add_argument("year", help="reporting year", type=int)
args = parser.parse_args()
reader = csv.reader(args.csv_file, delimiter="\t", quotechar='"')

header = True
default = lambda: Decimal("0")
data = defaultdict(default)
transfer_amount = Decimal("0")

for row in reader:
    if header:
        try:
            header = False
            month_column = row.index("Sale Month")
            artist_column = row.index("Artist")
            earnings_column = row.index("Earnings (USD)")
        except ValueError:
            print("Error finding correct data in .tsv file")
            sys.exit()
    else:
        artist = row[artist_column]
        earnings = row[earnings_column]
        month = row[month_column]

        year, _ = month.split("-")
        if int(year) == args.year:
            data[artist] += Decimal(earnings)

for k in sorted(data.keys()):
    print("{}\n    ${}\n".format(k, data[k]))
    transfer_amount += data[k]

print("Net Amount\n    ${}\n".format(transfer_amount))
