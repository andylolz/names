import csv
from itertools import islice

import xlrd


def skip_headers(rows, header_row=0):
    return islice(rows, header_row, None)


def val_from_cell(cell):
    if cell.value == ':':
        return 0.
    return cell.value


book = xlrd.open_workbook('historic_names.xls')
sheet = {
    'M': book.sheet_by_name('Boys'),
    'F': book.sheet_by_name('Girls'),
}
header_row = [
    'rank', '1904', '1914', '1924', '1934', '1944', '1954',
    '1964', '1974', '1984', '1994']

output = []
for sex in ['M', 'F']:
    rows = sheet[sex].get_rows()
    rows = skip_headers(rows, 5)
    data = map(lambda row: dict(zip(header_row, map(val_from_cell, row))), rows)
    for idx, row in enumerate(data):
        if row['rank'] == '':
            break
        for year in header_row[1:]:
            output.append({
                'sex': sex,
                'decade': year[:3] + '0',
                'name': row[year].title(),
                'pct': 100 * (100 - idx) / 5050,
            })

fieldnames = ['sex', 'decade', 'name', 'pct']
with open('data/names_bydecade_sub.tsv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames,
                            dialect='excel-tab')
    _ = writer.writeheader()
    for row in output:
        _ = writer.writerow({k: v for k, v in row.items() if k in fieldnames})
