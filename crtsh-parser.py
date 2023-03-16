#!/bin/python3.10
from bs4 import BeautifulSoup
import requests
import sys
from colorama import Fore, Back, Style
import argparse

# ASCII Art
print(Fore.GREEN + " __   __  ___   __           __        __   __   ___  __") 
print("/  \ |__)  |   /__` |__|    |__)  /\  |__) /__` |__  |__)")
print("\__, |  \  |  ..__/ |  |    |    /~~\ |  \ .__/ |___ | \\")
print("-------------------------------------------------------------")

#Argument for help:
parser=argparse.ArgumentParser(
    description='''Reaches out to and queries crt.sh for a specific domain passed using -d flag.''')
parser.add_argument('-d', '--domain', type=str, help="domain for query", required=True)   
args=vars(parser.parse_args())


#Prompt for keyword
keyword = args['domain']

#Split keyword into keyword and TLD
split_query = keyword.split(".")
TLD = "." + split_query[1]

print(Fore.BLUE + "\nQuerying crt.sh for " + keyword + "...\n")

#GET request for URL
URL = "https://crt.sh/?q=" + keyword 
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")

header = soup.find_all("td")

#Create initial list of subdomains, more cleanup later on in code
sites = []

print(Fore.BLUE + "Cleaning up web page content...\n")

for lines in header:
	if lines.name == 'td':
		site = lines.text
		split_site=site.split("\n")
		for i in split_site:
			if TLD in i:
				sites.append(i)

#Create new list with cleaned up subdomains
print("\n")
print(Fore.WHITE + "Uniquely sorted subdomains identified:")
print("---------------------------------------")
sites = sorted(set(sites))
sites2 = []
for i in sites:
	if "*" not in i:
		if "Match" not in i:
			if "OU=" not in i:
				if "?" not in i:
					individual = i.split(TLD)
					for x in individual:
						addedTLD = x + TLD
						if addedTLD != TLD:
							sites2.append(addedTLD)

#Final sort and print of subdomains, creation and write to file
file = open("subdomains.txt",  "a")					
sites2 = sorted(set(sites2))
for x in sites2:
	print(x)
	file.write(x + "\n")
print("------------------------------------------------")
print(Fore.GREEN + "Total number of subdomains: " + str(len(sites2)))
print(Fore.BLUE + "Subdomains written to file subdomains.txt in current directory.")	
file.close()		
