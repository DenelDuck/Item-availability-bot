import requests

DEFAULT_FILE = "links.txt"

# create function
def main():
    links = getURLs(DEFAULT_FILE)
    if links == None:
        return
    
    checkLinks(links)
    


def getURLs(filename):
    # open file
    try:
        with open(filename, "r") as file:
            data = file.read()
            lines = data.split("\n")
            return lines
    # catch error if file does not exist
    except FileNotFoundError:
        print("File with filename %s not found" % filename)
        return None


def checkLinks(links):
    oosList= {"out of stock", "out-of-stock", "uitverkocht", "not available", "niet leverbaar"}
    for link in links:
        if link == "":
            continue
        print("Checking %s..." % link[:100])
        data = getDataFromWeb(link)
        if data == None:
            print("Did not receive content from %s..." % link[:100])
            continue
        oos = False
        for word in oosList:
            if word in data.lower():
                print("%s... is out of stock" % link[:100])
                oos = True
                break
        if not oos:
            print("%s... is in stock" % link[:100])
        
        

def getDataFromWeb(url):
    hdr = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    , 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    try:
        with requests.get(url, headers=hdr) as r:
            if r.status_code == 200:
                return r.text
            return None
    except:
        print("Could not open %s" % url[:100])
    

main()