import math
import sys

def xfloor(data, div):
    i = float(data)
    a = i / int(div)
    b = str(a)
    if "." in b:
        c = str(b).split(".")
        d = c[1]
        e = int(d)
        if e < 50:
            f = math.floor(a)
            print "result =", f
            print "+ 1 =", f + 1
        else:
            f = math.floor(a)
            print "result =", f
    else:
        f = a
        print "result =", a
        
if __name__ == "__main__":
    if len(sys.argv) >  1:
        xfloor(sys.argv[1], sys.argv[2])
    else:
        print "\n"
        print "\t Usage:", "data divider\n"
        