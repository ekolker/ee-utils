# CSV to usable BOM

import csv, sys

bom_out = {}
# key: everything except refdes --> list

def read_diptrace(filename):

    diptarce_bom = csv.reader(file(filename, "rU"), dialect = 'excel')

    for col in diptarce_bom:
        if (col[0] in ("", "#")):
            continue

        # we're not in the header/footer, so let's do some work
        ref_des     = col[1]
        value       = col[2]
        symbol      = col[3]
        pattern     = col[5]
        quantity    = col[6]
        datasheet   = col[7]
        digikey     = col[8]

        # bom_line = bom_out.setdefault(\
        #       value+symbol+pattern+datasheet+digikey, {})
        
        print value+symbol+pattern+datasheet+digikey




def main(name, filename = "", target = "out.csv"):

    if (filename == ""):
        print "\nError, invalid file name\n"
        return
    
    print "\nAdapting source the file:\t", filename, \
            "\nTo a usable format here:\t", target

    read_diptrace(filename)


if __name__ == '__main__':
    main(*sys.argv)