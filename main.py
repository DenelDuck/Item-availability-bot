import email
from re import S
import requests
import json
import smtplib
from email.message import EmailMessage

DEFAULT_FILE = "links.txt"
KEYWORDSFILE = "static/keywords.json"
EMAILFILE = "email.txt"
IGNOREFILE = "ignore.txt"

# Color class for printing in terminal
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
    links = getLinks(DEFAULT_FILE)
    if links == None:
        return
    checkLinks(links)
    print(f"{bcolors.HEADER}=========================================================={bcolors.ENDC}")
    
# TODO:
# Add periodically check
# Join all links that are in stock in one email, instead of one email per link

def getLinks(filename):
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
    # Get keywords
    try:
        with open(KEYWORDSFILE, "r") as file:
            oosList = json.load(file)
    except FileNotFoundError:
        print(f"{bcolors.FAIL}{bcolors.BOLD}File with filename {KEYWORDSFILE} not found")
        return None
    # check every link in list
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
            # send email if not already sent by checking if it's present in ignore list
            try:
                if link not in open(IGNOREFILE, "r").read():
                    ignore(link)
                    sendEmail(link)
            except:
                print(f"{bcolors.WARNING}{bcolors.BOLD}Could not open {IGNOREFILE}, creating file{bcolors.ENDC}")
                ignore(link)
                sendEmail(link)


        
        
# get html from link
def getDataFromWeb(link):
    # use headers to avoid 403 error
    hdr = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    , 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    try:
        with requests.get(link, headers=hdr) as r:
            if r.status_code == 200:
                return r.text
            return None
    except:
        print(f"{bcolors.WARNING}{bcolors.BOLD}Could not open {link}{bcolors.ENDC}")
        return None
    

def sendEmail(link):
    # create email message
    msg = EmailMessage()
    msg['Subject'] = "Link is in stock!"
    # get email addresses and password from file for privacy reasons
    with open(EMAILFILE, 'r') as file:
        receiver = file.readline()
        sender = file.readline()
        password = file.readline()
        print(f"{bcolors.OKGREEN}Sending email to {bcolors.BOLD}{receiver}{bcolors.OKGREEN} from {bcolors.BOLD}{sender}{bcolors.OKGREEN}")
        msg['From'] = sender
        msg['To'] = receiver
    msg.set_content(f"{link}\nis in stock!")

    # send message via gmail server
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login(sender, password)
        s.sendmail(sender, receiver, msg.as_string())
        print(f"{bcolors.OKGREEN}Email sent to {bcolors.BOLD}{receiver}{bcolors.OKGREEN}")
        s.quit()
    except smtplib.SMTPException as e:
        print(f"{bcolors.WARNING}{bcolors.BOLD}Could not send email{bcolors.ENDC}")
        print(f"{bcolors.ENDC}e")


# append link to file, creates file if doesn't exist
def ignore(link):
    with open(IGNOREFILE, "a+") as file:
        file.write(link + "\n")


main()