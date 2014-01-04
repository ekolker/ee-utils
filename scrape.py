import requests, sys, csv
from bs4 import BeautifulSoup
from types import NoneType


def export_BOM(BOM, filename = 'BOM'):
  out = open(filename + '.csv', "w")
  for part_number in BOM.keys():
    part = BOM[part_number][0]
    for attribute in part:
      out.write(attribute + ', ')
    out.write("\n")

  # out.write(json.dumps(course, ensure_ascii = False, indent = 4) + "\n")
  out.close()
  print '\nBOM exported to:\t./' + filename + '.csv\n\n'


def print_output(BOM, invalids):
  for part in BOM.keys():
    print part, '\n', BOM[part][0], '\n'
  if (len(invalids) > 0):
    print "\nInvalid part numbers:"
    for i in invalids:
      print [i]
  print '\n\n'


def old_school_search(source, targets):
  start = source.find(targets[0])
  if start == -1:
    return ""
  end = source.find(targets[1], start)
  entry = source[start + len(targets[0]):end]
  # we apparently don't actually like unicode
  return str(entry.replace('\xc2\xb5', 'u'))


def main(name, *args):

  if args == ():
    args = [ "", \
    # ["311-1.0KJRCT-ND", "SC1489-1-ND", "WM6699CT-ND", "WM5587CT-ND", "S9337-ND", "S5446-ND", "609-3322-ND"]
    # ["", \
     "ACML-0603-121-TCT-ND", \
     "2N7002DWA-7DICT-ND", \
     "296-21527-1-ND", \
     "LM2596S-3.3/NOPB-ND", \
     "296-29936-1-ND", \
     "1276-2154-1-ND", \
     "1276-1443-1-ND", \
     "1276-1116-1-ND", \
     "1276-2267-1-ND", \
     "1276-1173-1-ND", \
     "1276-2908-1-ND", \
     "SC1489-1-ND", \
     "609-3322-ND", \
     "311-1.0KJRCT-ND", \
     "490-5258-1-ND", \
     "587-3105-1-ND", \
     "MMBD914-FDICT-ND", \
     "296-9541-1-ND", \
     "1276-6378-1-ND", \
     "1276-1443-1-ND", \
     "PCE3951CT-ND", \
     "1276-1173-1-ND", \
     "PCE4440CT-ND", \
     "1276-2972-1-ND", \
     "1276-2908-1-ND", \
     "1276-2267-1-ND", \
     "1276-2154-1-ND", \
     "1276-1116-1-ND", \
     "B340A-FDICT-ND", \
     "568-6542-1-ND", \
     "475-1409-1-ND", \
     "475-2558-1-ND", \
     "62T0379", \
     "WM5587CT-ND", \
     "SC1489-1-ND", \
     "609-3322-ND", \
     "S5446-ND", \
     "WM6699CT-ND", \
     "S9337-ND", \
     "SRR6038-100YCT-ND", \
     "ACML-0603-121-TCT-ND", \
     ""]
     #['587-1722-1-ND']#'311-1.0KJRCT-ND']#, '2N7002DWA-7DICT-ND', 'dsig', '1276-1443-1-ND']
  print args, '\n'

  base_url = 'http://search.digikey.com/scripts/DkSearch/dksus.dll?Detail&name='

  # where we keep good parts and wrong numbers
  BOM = dict()
  invalids = []

  for argument_number in range(len(args)):
    debug = 'Fetching\t' + str(argument_number + 1) + '\tof\t' + str(len(args)) + '\tparts...'

    Source_Link = base_url + args[argument_number]
    r = requests.get(Source_Link)
    page_source = r.text.encode("utf8")

    # cut to the chase
    target = '<table class="product-details-table" '
    start_index = page_source.find(target)
    ingredients = page_source[start_index : len(page_source) - 26]

    soup = BeautifulSoup(ingredients)

    if type(soup.find(itemprop="manufacturer")) == NoneType:
      # skip invalid part numbers
      invalids.append(args[argument_number])
      print debug + '\tINVALID PN: ' + str([args[argument_number]])

    else:
      print debug
      Manufacturer = soup.find(itemprop="manufacturer").find(itemprop="name").contents[0].encode('ascii','ignore')
      DigiKeyPN = soup.find(id="reportpartnumber").contents[1].encode('ascii','ignore')
      ManufacturerPN = soup.find(class_="seohtag", itemprop='model').contents[0].encode('ascii','ignore')
      Description = soup.find(itemprop="description").contents[0].encode('ascii','ignore')
      Type = Description.split()[0]

      Datasheets = ""
      for link in soup.find_all(class_="lnkDatasheet"):
        # there could be more than one...
        Datasheets = Datasheets + link.get('href').encode('ascii','ignore') + " "
      Datasheets = Datasheets.strip()

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

      search_term = ">Package / Case</th><td>"
      Package = old_school_search(page_source, [search_term, "</td>"])

      # add 'em!
      BOM.setdefault(DigiKeyPN, [[Type, Value, Description, Package, Manufacturer, ManufacturerPN, Datasheets, Source_Link, DigiKeyPN], Prices])
      #Description, DigiKeyPN, Manufacturer, ManufacturerPN, Datasheets, Prices, Value, Package, Source_Link])

  print_output(BOM, invalids)

  export_BOM(BOM)


if __name__ == '__main__':
    main(*sys.argv)