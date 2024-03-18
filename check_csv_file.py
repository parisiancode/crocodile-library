"""
Module to check Handy file integration new features.
"""

import csv
import sys

filename = '../HandyLibrary.csv'
filenameToCompare = '../handy_result.csv'

with open(filename, encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    try:
        for row in csv_reader:
            if line_count == 0:
                # Print Columns Header
                print(row)
                line_count += 1
            else:
                # Print Processed Lines
                # print(row)
                line_count += 1
        print(f'Processed without errors {line_count} lines.')
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(
            filename, csv_reader.line_num, e))
