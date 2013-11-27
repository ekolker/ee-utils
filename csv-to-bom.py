# CSV to usable BOM

import csv, sys

bom_out = {}
foo = ""
line_number = 1
# key: everything except refdes --> list

def read_diptrace(filename):

    diptarce_bom = csv.reader(file(filename, "rU"), dialect = 'excel')

    line_number = 1

    for col in diptarce_bom:
        foo = ""
        if (col[0] in ("", "#")):
            continue

        # we're not in the header/footer, so let's do some work
        refdes      = col[1]
        value       = col[2]
        symbol      = col[3]
        pattern     = col[5]
        quantity    = col[6]
        datasheet   = col[7]
        digikey     = col[8]
        
        for char in refdes:
            if char.isalpha():
                foo += char

        # dictionary stuff
        key = foo+value+symbol+pattern+datasheet+digikey

        # columns in final bom:
        #   line #, Quantity, Value, Description, Manufacturer Part #, Manufacturer, Package Supplier, supplier PN, ,supplier link, Ref Des, 1, Quantity, , 100, (Total PPU), ,1000, (Total PPU)
        value = [line_number, 1, value, '', '']
        line_number = line_number + 1
        

        # bom_line = bom_out.set






def main(name, filename = "in.csv", target = "out.csv"):

    if (filename == ""):
        print "\nError, invalid file name\n"
        return
    
    print "\nAdapting source the file:\t", filename, \
            "\nTo a usable format here:\t", target

    read_diptrace(filename)


if __name__ == '__main__':
    main(*sys.argv)