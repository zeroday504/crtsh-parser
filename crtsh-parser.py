#!/bin/python3.10
from bs4 import BeautifulSoup
import bs4
import requests
import sys
from colorama import Fore, Back, Style
import argparse
from urllib3.exceptions import InsecureRequestWarning
import socket
import time

start_time = time.time()

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

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

while page.status_code != 200:
	print (Fore.RED + "Connection error, retrying...")
	page = requests.get(URL)
	time.sleep(5)

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
print("------------------------------------------------")
sites = sorted(set(sites))
sites2 = []
for i in sites:
	if not any(invalid in i for invalid in ("*", "Match", "OU=", "?")):
		individual = i.split(TLD)
		for x in individual:
			addedTLD = x + TLD
			if addedTLD != TLD:
				str(sites2.append(addedTLD))
if not sites2:
	print (Fore.RED + "No unique subdomains were identified for " + Fore.WHITE + keyword)
	print ("\nTime elapsed: " + str(round((time.time() - start_time), 2)) + " seconds.")
	
else:

	#Final sort and print of subdomains, creation and write to file
	file = open("subdomains.txt",  "w")					
	sites2 = sorted(set(sites2))
	for x in sites2:
		print(x)
		file.write(x + "\n")

	print("------------------------------------------------")
	print(Fore.GREEN + "Total number of subdomains: " + str(len(sites2)))
	print(Fore.BLUE + "Subdomains written to file subdomains.txt in current directory.\n")	
	file.close()	


	#Status Code Check
	Status_Code_Check = input(Fore.WHITE + "Would you like to perform a status code check against these subdomains? This may be time consuming depending on the number of subdomains found. ")
	if Status_Code_Check == "Y" or Status_Code_Check == "y":
		print (Fore.GREEN + "\nChecking subdomains...\n")
		
		session = requests.Session()
		session.verify = False
		
		headers = {
	    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'DNT': '1',
	    'Connection': 'keep-alive',
	    'Upgrade-Insecure-Requests': '1',
	    'Sec-Fetch-Dest': 'document',
	    'Sec-Fetch-Mode': 'navigate',
	    'Sec-Fetch-Site': 'none',
	    'Sec-Fetch-User': '?1',
	}
		file = open("live_subdomains.txt", "w")
		for url in sites2:
			try:
				long_url = 'https://' + url
				r = requests.get(long_url, timeout=7, allow_redirects=True, verify=False)
				
				if r.status_code == 200:
					html = bs4.BeautifulSoup(r.text, features="lxml")
					print (Fore.GREEN + url + ' ' + 'Status code: ' + str(r.status_code) )
					print ('	' + html.title.text)
					print ("	IP: " + socket.gethostbyname(url) + '\n')
					file.write(url + "\n")
				else: 
					print (Fore.PURPLE + url + ' ' + str(r.status_code))
			except:
				print (Fore.RED + url + ' FAILED\n')
				continue
				
		print (Fore.WHITE + "\nSubdomain HTTP status code check has completed.")
		print ("\nTime elapsed: " + str(round((time.time() - start_time), 2)) + " seconds.")
		print ("\nLive subdomains have been written to live_subdomains.txt in current directory")
	elif Status_Code_Check == "N" or Status_Code_Check == "n":
		print("\n" + Fore.RED + "Status code check not performed. Terminating program.")
		print ("\nTime elapsed: " + str(round((time.time() - start_time), 2)) + " seconds.")
	else:
		print("\n" + Fore.RED + "Invalid entry, terminating program.")
		print ("\nTime elapsed: " + str(round((time.time() - start_time), 2)) + " seconds.")

