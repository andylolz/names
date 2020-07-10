from itertools import islice
import csv

import xlrd


def skip_headers(rows, header_row=0):
    return islice(rows, header_row, None)


def get_name(cell):
    name = cell.value
    if str(cell) == 'bool:1':
        # the name "TRUE" completely throws the excel parser
        name = 'TRUE'
    return name.title()


def val_from_cell(cell):
    if cell.value == ':':
        return 0.
    return cell.value


book = xlrd.open_workbook('names.xls')
sheet = {
    'M': book.sheet_by_name('Boys'),
    'F': book.sheet_by_name('Girls'),
}


min_year = 1996
max_year = 2018
years = range(max_year, min_year-1, -1)
header_row = ['Name'] + ['{} {}'.format(y, x)
                         for y in years
                         for x in ['Rank', 'Count']]
indexes = [idx for idx, x in enumerate(header_row) if 'Count' in x]

output = []

for sex in ['F', 'M']:
    rows = sheet[sex].get_rows()
    rows = skip_headers(rows, 6)
    counts = []
    for row in rows:
        if row[0].value == '':
            break
        counts.append({
            'name': get_name(row[0]),
            'count': sum([val_from_cell(row[i]) for i in indexes]),
        })
    total = sum(x['count'] for x in counts)
    for x in counts:
        output.append({
            'sex': sex,
            'name': x['name'],
            'abs': x['count'],
            'pct': 100 * x['count'] / total,
        })

fieldnames = ['sex', 'name', 'pct']
with open('data/names_sub.tsv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames,
                            dialect='excel-tab')
    _ = writer.writeheader()
    for row in output:
        _ = writer.writerow({k: v for k, v in row.items() if k in fieldnames})
