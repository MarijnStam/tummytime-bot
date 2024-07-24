from time import gmtime, strftime

def timestamp():
    return strftime("%Y-%m-%dT%H:%M", gmtime())