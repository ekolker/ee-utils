from bs4 import BeautifulSoup
import requests, sys

# url = raw_input("Enter a website to extract the URL's from: "

def main(name):
  r = requests.get('http://www.digikey.com/product-detail/en/CBMF1608T470K/587-1722-1-ND/1008047')
  # http://www.digikey.com/product-detail/en/2N7002-7-F/2N7002-FDITR-ND/717681')
  # "http://search.digikey.com/scripts/DkSearch/dksus.dll?Detail&name=LM2596S-3.3/NOPB-ND")
  # "http://www.digikey.com/product-detail/en/PRTR5V0U4Y,125/568-6542-1-ND/2531829")
  # http://www.digikey.com/product-detail/en/CBMF1608T470K/587-1722-1-ND/1008047
  # http://www.digikey.com/product-detail/en/2N7002-7-F/2N7002-FDITR-ND/717681
   
  page_source = r.text.encode("utf8")

  # cut to the chase
  target = '<table class="product-details-table" '
  start_index = page_source.find(target)
  ingredients = page_source[start_index : len(page_source) - 26]

  soup = BeautifulSoup(ingredients)

  Manufacturer = soup.find(itemprop="manufacturer").find(itemprop="name").contents[0]
  DigiKeyPN = soup.find(id="reportpartnumber").contents[1]
  ManufacturerPN = soup.find(class_="seohtag", itemprop='model').contents[0]
  Description = soup.find(itemprop="description").contents[0]

  # details = soup.find(class_='attributes-table-main')

  Datasheets = []
  for link in soup.find_all(class_="lnkDatasheet"):
    Datasheets.append(link.get('href'))

  print [Manufacturer, ManufacturerPN, DigiKeyPN, Description, Datasheets], '\n'


  # print details























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