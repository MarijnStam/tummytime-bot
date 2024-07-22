from time import gmtime, strftime

def timestamp():
    return strftime("%d/%m/%Y %H:%M:%S", gmtime())