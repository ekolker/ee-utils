import requests, sys
from bs4 import BeautifulSoup
from types import NoneType

def output(BOM, invalids):
  for part in BOM.keys():
    print part, '\n', BOM[part], '\n'

  if (len(invalids) > 0):
    print "\nInvalid part numbers:"
    for i in invalids:
      print [i]
  print '\n\n'


def old_school_search(source, targets):
  start = source.find(targets[0])
  end = source.find(targets[1], start)
  entry = source[start + len(targets[0]):end]
  # we apparently don't actually like unicode
  return str(entry.replace('\xc2\xb5', 'u'))


def main(name, *args):

  if args == ():
    args = ["311-1.0KJRCT-ND", "SC1489-1-ND", "WM6699CT-ND", "WM5587CT-ND", "S9337-ND", "S5446-ND", "609-3322-ND"]
    # ["", \
    #  "ACML-0603-121-TCT-ND", \
    #  "2N7002DWA-7DICT-ND", \
    #  "296-21527-1-ND", \
    #  "LM2596S-3.3/NOPB-ND", \
    #  "296-29936-1-ND", \
    #  "1276-2154-1-ND", \
    #  "1276-1443-1-ND", \
    #  "1276-1116-1-ND", \
    #  "1276-2267-1-ND", \
    #  "1276-1173-1-ND", \
    #  "1276-2908-1-ND", \
    #  "SC1489-1-ND", \
    #  "609-3322-ND", \
    #  "311-1.0KJRCT-ND", \
    #  "490-5258-1-ND", \
    #  "587-3105-1-ND", \
    #  "MMBD914-FDICT-ND", \
    #  "296-9541-1-ND", \
    #  "1276-6378-1-ND", \
    #  "1276-1443-1-ND", \
    #  "PCE3951CT-ND", \
    #  "1276-1173-1-ND", \
    #  "PCE4440CT-ND", \
    #  "1276-2972-1-ND", \
    #  "1276-2908-1-ND", \
    #  "1276-2267-1-ND", \
    #  "1276-2154-1-ND", \
    #  "1276-1116-1-ND", \
    #  "B340A-FDICT-ND", \
    #  "568-6542-1-ND", \
    #  "475-1409-1-ND", \
    #  "475-2558-1-ND", \
    #  "62T0379", \
    #  "WM5587CT-ND", \
    #  "SC1489-1-ND", \
    #  "609-3322-ND", \
    #  "S5446-ND", \
    #  "WM6699CT-ND", \
    #  "S9337-ND", \
    #  "SRR6038-100YCT-ND", \
    #  "ACML-0603-121-TCT-ND", \
    #  ""]
     #['587-1722-1-ND']#'311-1.0KJRCT-ND']#, '2N7002DWA-7DICT-ND', 'dsig', '1276-1443-1-ND']
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
      Manufacturer = soup.find(itemprop="manufacturer").find(itemprop="name").contents[0].encode('ascii','ignore')
      DigiKeyPN = soup.find(id="reportpartnumber").contents[1].encode('ascii','ignore')
      ManufacturerPN = soup.find(class_="seohtag", itemprop='model').contents[0].encode('ascii','ignore')
      Description = soup.find(itemprop="description").contents[0].encode('ascii','ignore')

      Datasheets = []
      for link in soup.find_all(class_="lnkDatasheet"):
        # there could be more than one...
        Datasheets.append(link.get('href').encode('ascii','ignore'))

      Prices = dict()
      chart = soup.find('table', id='pricing').find_all('td')
      for index in range(len(chart)):
        if (index % 3 == 0):
          key = int(chart[index].contents[0].encode('ascii','ignore').replace(',', ''))
          val = float(chart[index + 1].contents[0].encode('ascii','ignore'))
          Prices.setdefault(key, val)
      
      Value = ""
      # do we have a passive?
      if (Description[0:3] in "RES CAP IND"):
        # 0 = R, 1 = C, 2 = L
        type_of_passive = "RESCAPIND".find(Description[0:3]) / 3
        # what we look for
        search_terms = {0 : "<tr><th align=right valign=top>Resistance</th><td>", \
          1 : "<tr><th align=right valign=top>Capacitance</th><td>", \
          2 : "<tr><th align=right valign=top>Inductance</th><td>"}
        search_term = search_terms.get(type_of_passive)
        Value = old_school_search(page_source, [search_term, "</td></tr>"])

      # go for packages...
      search_term = "<tr><th align=right valign=top>Package / Case</th><td>"
      Package = old_school_search(page_source, [search_term, "<"])

      # add 'em!
      BOM.setdefault(DigiKeyPN, [Description, DigiKeyPN, Manufacturer, ManufacturerPN, Datasheets, Prices, Value, Package])

  output(BOM, invalids)


if __name__ == '__main__':
    main(*sys.argv)