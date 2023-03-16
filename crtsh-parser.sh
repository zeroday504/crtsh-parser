#!/bin/bash

# Set the color variable
green='\033[0;32m'
red='\033[0;31m'
clear='\033[0m'

# ASCII Art
echo -e " __   __  ___   __           __        __   __   ___  __" 
echo -e "/  \` |__)  |   /__\` |__|    |__)  /\  |__) /__\` |__  |__)"
echo -e "\__, |  \  |  ..__/ |  |    |    /~~\ |  \ .__/ |___ | '\'"
echo -e "-------------------------------------------------------------"

# Usage instructions

function show_usage() {
	echo "Script designed to query and parse through crt.sh response 
data"
	echo "Usage: ./crtsh-parser.sh <keyword> <top-level-domain>"
	echo "Example: ./crtsh-parser.sh nabisco .com"
	echo 
"---------------------------------------------------------------"
	echo "Supports the following TLDs:"
	echo ".com"
	echo ".edu"
	echo ".org"
	echo ".net"
	echo ".xyz"
	echo ".gov"
	echo 
"---------------------------------------------------------------"
	echo "Currently does not support researching the following 
domains:"
	echo "sectigo.com"
	echo "*googleapis*"
	echo "*github*"
	echo 
"---------------------------------------------------------------"
	echo "Common exit code meanings:"
	echo "3: URL malformed"
	echo "6: Failed DNS resolution"
	echo "7: Failed to connect"
	echo "22: HTTP page not retrieved"
	echo "For other exit code meanings, please reference 
https://everything.curl.dev/usingcurl/returns"
	
return 0
}

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
	show_usage
else
	# Reaching out to crt.sh and grabbing response content
	echo -e "\n"
	echo -e "${green}Connecting to crt.sh and searching 
${red}$1$2${green}..."
	curl -s "https://crt.sh/?q=$1$2" > crtsh-content.txt

	# Parsing through web page content and removing working file
	echo -e "\n"
	echo -e "${green}Parsing web page content..."
	grep $2 crtsh-content.txt > crtsh-messy-urls.txt

	#Uniquely sorting URLs
	echo -e "\n"
	echo -e "${green}Sorting and identifying relevant URLs..."
	echo "Uniquely sorted URLs:" > crtsh-final-urls.txt
	echo "----------------------" >> crtsh-final-urls.txt

	grep -E -o 
'([a-zA-Z0-9])+\.([comeduorgnetxyzkv]){3}'\|'([a-zA-Z0-9])+\.([a-zA-Z0-9])+\.([comeduorgnetxyzkv]){3}'\|'([a-zA-Z0-9])+\.([a-zA-Z0-9])+\.([a-zA-Z0-9])+\.([comeduorgnetxyzkv]){3}' 
crtsh-messy-urls.txt | grep -v 'sectigo.com\|googleapis\|github'  | sort 
-u -f >> crtsh-final-urls.txt

	echo -e "\n"

	#Output to console and file cleanup
	cat crtsh-final-urls.txt
	echo "----------------------"
	echo -e "\n"
	echo -e "Number of unique URL's identified: ${red}$(grep $2 
crtsh-final-urls.txt | wc -l)"
	echo -e "\n"
	echo -e "${green}Final list of urls is stored in 
${red}crtsh-final-urls.txt ${green}in the current directory"
	echo 
"-----------------------------------------------------------------------------------------------------------"
	rm crtsh-messy-urls.txt
	rm crtsh-content.txt
fi

#Prompt asking if user wants to lookup status codes for each found 
subdomain
echo -e "\n"
echo -e "${clear}Would you like to retrieve the HTTP status codes for 
these subdomains? This can be a lengthy process depending on the number of 
subdomains being reached and potential timeouts (error code will display). 
(Y/N): "
read status_code_inquiry
echo -e "\n"

if [ $status_code_inquiry = "N" ] || [ $status_code_inquiry = "n" ]; then
	echo -e "${red}No status codes checked."
elif [ $status_code_inquiry = "Y" ] || [ $status_code_inquiry = "y" ]; 
then
	echo -e "${green}Performing status code checks..."
	echo -e "---------------------------------------------"
	echo -e "\n"
	for i in $(grep $2 crtsh-final-urls.txt)
	do
		#Gets HTTP status code and IP for each URL in the file
		response=$(curl -s -w "%{http_code}" $i)
		check=$?
		http_code=$(tail -n1 <<< "$response")
		echo -e "${green}$i: $http_code (Exit code: $check)"
		IP=$(host $i | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" 
| sed -z 's/\n/\t/g;s/\t$/\n/')
		echo -e "     ${clear}IP(s): $IP" 
		#If the code is a redirect, follow the redirect and grab 
the URL/IP
		if [ $http_code = "301" ]; then
			redirect=$(curl -Ls -o /dev/null -w 
%{url_effective} $i)
			echo -e "     ${clear}Redirected to: $redirect"
			cleanredir=$(echo ${redirect/%?/})
			redirIP=$(host $cleanredir | grep -E -o 
"([0-9]{1,3}[\.]){3}[0-9]{1,3}" | sed -z 's/\n/\t/g;s/\t$/\n/')
			#If the redirIP variable is empty, print that no 
IP was found, otherwise print the IP
			if [ -z "$redirIP" ]; then
				echo -e "     Redirect IP(s): No redirect 
IP found."
			else
				echo -e "     ${clear}Redirect IP(s): 
$redirIP"
			fi
		fi
	done
else
	echo -e "${red}Incorrect entry, assuming no."
fi
