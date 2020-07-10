import urllib.request


def download_xls(url, filename):
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'Mozilla/5.0')
    filename, headers = opener.retrieve(url, filename)
    return filename


url = 'https://www.ons.gov.uk/file?' + \
      'uri=/peoplepopulationandcommunity/birthsdeathsandmarriages/' + \
      'livebirths/adhocs/10429babynames1996to2018englandandwales/' + \
      'adhocallbabynames1996to2018.xls'
filename = 'names.xls'

historic_url = 'https://www.ons.gov.uk/file?' + \
               'uri=%2fpeoplepopulationandcommunity%2f' + \
               'birthsdeathsandmarriages%2flivebirths%2fdatasets%2f' + \
               'babynamesenglandandwalestop100babynameshistoricaldata%2f' + \
               '19041994/historicname_tcm77-254032.xls'
historic_filename = 'historic_names.xls'

download_xls(url, filename)
download_xls(historic_url, historic_filename)
