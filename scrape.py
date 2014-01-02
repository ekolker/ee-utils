import requests, sys
from bs4 import BeautifulSoup
from types import NoneType

def output(BOM, invalids):
  for part in BOM.keys():
    print part, '\n', BOM[part], '\n'

  if (len(invalids) > 0):
    print "\nInvalid part numbers:"
    for i in invalids:
      print i
  print '\n\n'


def main(name, *args):

  if args == ():
    args = ['587-1722-1-ND']#'311-1.0KJRCT-ND']#, '2N7002DWA-7DICT-ND', 'dsig', '1276-1443-1-ND']
  print args, '\n'

  base_url = 'http://search.digikey.com/scripts/DkSearch/dksus.dll?Detail&name='

  # where we keep good parts and wrong numbers
  BOM = dict()
  invalids = []

  for argument_number in range(len(args)):
    debug = 'Fetching\t' + str(argument_number + 1) + '\tof\t' + str(len(args)) + '\tparts...'

    r = requests.get(base_url + args[argument_number])
    page_source = r.text.encode("utf8")

    # cut to the chase
    target = '<table class="product-details-table" '
    start_index = page_source.find(target)
    ingredients = page_source[start_index : len(page_source) - 26]

    soup = BeautifulSoup(ingredients)

    if type(soup.find(itemprop="manufacturer")) == NoneType:
      # skip invalid part numbers
      invalids.append(args[argument_number])
      print debug + '\tINVALID PN: ' + args[argument_number]

    else:
      print debug
      Manufacturer = soup.find(itemprop="manufacturer").find(itemprop="name").contents[0]
      DigiKeyPN = soup.find(id="reportpartnumber").contents[1]
      ManufacturerPN = soup.find(class_="seohtag", itemprop='model').contents[0]
      Description = soup.find(itemprop="description").contents[0]
      Datasheets = []
      for link in soup.find_all(class_="lnkDatasheet"):
        # there could be more than one...
        Datasheets.append(link.get('href'))


      # price_chart = soup.find_all('tr')[3]
      # k = soup.find('table', class_='product-additional-info').contents[0].contents[0].find('table')
      # print k, '\n\n'

      chart = soup.find('table', id='pricing').find_all('td')
      Prices = dict()
      last = 0

      for index in range(len(chart)):
        if (index % 3 == 0):
          last = int(chart[index].contents[0].encode('ascii','ignore').replace(',', ''))
          Prices.setdefault(last, '')
        if (index % 3 == 1):
          Prices[last] = float(chart[index].contents[0].encode('ascii','ignore'))

      # print Prices

  



      # add 'em!
      BOM.setdefault(DigiKeyPN, [Description, DigiKeyPN, Manufacturer, ManufacturerPN, Datasheets])

    

  # output(BOM, invalids)

  























  # start = 0
  # key_words = ['Digi-Key Part Number', 'Manufacturer', 'Manufacturer Part Number', 'Description', 'Package']#, 'Datasheet']
  # start_words = ['content="sku:', 'itemprop="name">', 'itemprop="model">', 'itemprop="description">', '<tr><th align=right valign=top>Supplier Device Package</th><td>']#, '<a class="lnkDatasheet" href="']
  # end_words = ['" />', '</span>', '</h1></td></tr>', '</td></tr>', '</td></tr>']#, '" target="_blank"']
  # data = []

  # for i in range(len(key_words)):
  #   start = 0
  #   while (page_source.find(key_words[i], start) > 0):
  #     data.append('')
  #     start = page_source.find(key_words[i], start)
  #     start = page_source.find(start_words[i], start)
  #     end = page_source.find(end_words[i], start)
  #     data[i] = data[i] + (page_source[start+len(start_words[i]):end] + ' ')

  # # any_left = 1
  # # datasheets = ''
  # # while (page_source.find(search_term) > 0):
  # #   search_term = '<a class="lnkDatasheet" href="'
  # #   start = page_source.find(search_term)
  # #   end = page_source.find('</td></tr>', start)

  # # do we have a passive?
  # if (data[3][0:3] in "RES CAP IND"):
  #   # value
  #   # 0 = R, 1 = C, 2 = L
  #   type_of_passive = "RESCAPIND".find(data[3][0:3]) / 3
  #   # what we look for
  #   search_terms = {0 :'<tr><th align=right valign=top>Resistance</th><td>', \
  #     1 : '<tr><th align=right valign=top>Capacitance</th><td>', \
  #     2 : '<tr><th align=right valign=top>Inductance</th><td>'}
  #   search_term = search_terms.get(type_of_passive)
  #   start = page_source.find(search_term)
  #   end = page_source.find('</td></tr>', start)
  #   entry = page_source[start + len(search_term):end]
  #   # we apparently don't like unicode
  #   entry = entry.replace('\xc2\xb5', 'u')

  #   key_words.append('Value')
  #   data.append(entry)




  #   # print value
  #   # start = page_source.find(key_words[i])
  #   # start = page_source.find(start_words[i], start)
  #   # end = page_source.find(end_words[i], start)
  #   # data.append(page_source[start+len(start_words[i]):end])

  # # print data
  # print page_source



if __name__ == '__main__':
    main(*sys.argv)