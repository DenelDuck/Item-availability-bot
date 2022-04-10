import requests

DEFAULT_FILE = "links.txt"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    print(f"{bcolors.HEADER}=========================================================={bcolors.ENDC}")
    links = getURLs(DEFAULT_FILE)
    if links == None:
        return
    checkLinks(links)
    print(f"{bcolors.HEADER}=========================================================={bcolors.ENDC}")
    
# TODO:
# Add keywords to check for on link
# Add periodically check
# Email when available

def getURLs(filename):
    # open file
    try:
        with open(filename, "r") as file:
            data = file.read()
            lines = data.split("\n")
            return lines
    # catch error if file does not exist
    except FileNotFoundError:
        print(f"{bcolors.FAIL}{bcolors.BOLD}File with filename {filename} not found")
        return None


def checkLinks(links):
    oosList= {"out of stock", "out-of-stock", "uitverkocht", "not available", "niet leverbaar"}
    for link in links:
        if link == "":
            continue
        shortlink = link[:80]
        print(f"{bcolors.OKGREEN}Checking {bcolors.BOLD}{shortlink}{bcolors.OKGREEN}...{bcolors.ENDC}")
        # get html from link
        data = getDataFromWeb(link)
        if data == None:
            print(f"{bcolors.FAIL}Did not receive content from {bcolors.BOLD}{shortlink}{bcolors.FAIL}...{bcolors.ENDC}")
            continue
        # check for keywords in html
        oos = False
        for word in oosList:
            if word in data.lower():
                print(f"{bcolors.OKGREEN}{shortlink}... {bcolors.FAIL}{bcolors.BOLD}is out of stock{bcolors.ENDC}")
                oos = True
                break
        if not oos:
            print(f"{bcolors.OKGREEN}{shortlink}... {bcolors.OKBLUE}{bcolors.BOLD}is in stock{bcolors.ENDC}")
        
        

def getDataFromWeb(url):
    hdr = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    , 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    try:
        with requests.get(url, headers=hdr) as r:
            if r.status_code == 200:
                return r.text
            return None
    except:
        print(f"{bcolors.WARNING}{bcolors.BOLD}Could not open {url}{bcolors.ENDC}")
        return None
    

main()