import urllib
import csv

import xlrd

url = 'https://www.ons.gov.uk/file?' + \
      'uri=/peoplepopulationandcommunity/birthsdeathsandmarriages/' + \
      'livebirths/adhocs/10429babynames1996to2018englandandwales/' + \
      'adhocallbabynames1996to2018.xls'

opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0')
filename, headers = opener.retrieve(url, 'names.xls')

book = xlrd.open_workbook('names.xls')

sheet = {
    'M': book.sheet_by_name('Boys'),
    'F': book.sheet_by_name('Girls'),
}

# for sheet in [boy_sheet, girl_sheet]:
min_year = 1996
max_year = 2018
years = range(min_year, max_year + 1)
upper_index = (max_year - min_year) * 2 + 2
indexes = range(upper_index, 0, -2)
output = []

for sex in ['F', 'M']:
    rows = sheet[sex].get_rows()
    while True:
        row = next(rows)
        if row[0].value == 'Name':
            break

    totals = {}
    for row in rows:
        name = row[0].value
        if str(row[0]) == 'bool:1':
            # the name "TRUE" completely throws the excel parser
            name = 'TRUE'
        if name == '':
            break
        name = name.title()
        totals[name] = dict(zip(years, map(lambda x: row[x].value
                                           if row[x].value != ':'
                                           else 0.0, indexes)))

    year_totals = {year: sum([t[year]
                              for t in totals.values()])
                   for year in years}

    # percs = {name: {year: 100 * total / year_totals[year]
    #                 for year, total in t.items()
    #                 } for name, t in totals.items()}

    for name, data in totals.items():
        for year, total in data.items():
            output.append({
                'sex': sex,
                'year': year,
                'name': name,
                'pct': 100 * total / year_totals[year],
            })

with open('data/names_byyear_sub.tsv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['sex', 'year', 'name', 'pct'],
                            dialect='excel-tab')
    _ = writer.writeheader()
    for row in output:
        _ = writer.writerow(row)
