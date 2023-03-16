# crtsh-parser
Tool used to query crt.sh and scrape subdomains from resulting webpage, storing them in a parsable and pipeable output file

![image](https://user-images.githubusercontent.com/84281259/225765171-2f33c078-0777-4e6b-8d6a-6f6ff9b20c80.png)

# crtsh-parser.sh
Usage: `./crtsh-parser.sh <keyword> <top-level domain>`

Example: `./crtsh-parser.sh nabisco .com`

![image](https://user-images.githubusercontent.com/84281259/225756585-bd18be13-4b72-4306-910e-d4e300b9acdb.png)

crtsh-parser.sh will save the output to a file named crtsh-final-urls.txt in the current directory

### HTTP Status Code Checker
crtsh-parser.sh will prompt and ask if you'd like to check the HTTP status codes of each subdomain, expediting enumeration and allowing you to find live sites rather than manually visiting them or having to pivot to another tool to do so.

During this enumeration, crtsh-parser.sh will also gather the IP addresses of the sites as well as the IP addresses of any redirects that take place, allowing the user to cross-reference with their scoping documents and identify subdomains that are within testing scope.


# crtsh-parser.py
Usage: `python3.10 crtsh-parser.py -d <domain>`

Example: `python3.10 crtsh-parser.py -d nabisco.com`

<img width="523" alt="image" src="https://user-images.githubusercontent.com/84281259/225760026-ca792b18-c2d1-4cff-ae32-d77ab77b8f29.png">

crtsh-parser.py does not current support HTTP status code checks or IP lookups, this will be implemented in later versions.

### Installation
`git clone https://github.com/zeroday504/crtsh-parser.git`

#### Python Version Installation Requirements
`python3.10 -m pip install -r requirements.txt`

#### Shell Version Installation Requirements
`chmod +x ./crtsh-parser.sh`
