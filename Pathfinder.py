#!/usr/bin/env python3
import requests, os
from html.parser import HTMLParser
import urllib3
from PathfinderFunctions import change_crawler_session, soup_function, get_file
from bs4 import Tag

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

path_to_download_tag = 'r=true'
exts = ['.zip','.epub']
url_download_list = {}
url_login = 'https://paizo.com/cgi-bin/WebObjects/Store.woa/wa/DirectAction/signIn?path=paizo'
url_account_files = 'https://paizo.com/paizo/account/assets'
data = {'e': 'EMAIL', 'zzz': 'PASSWORD'}

session = requests.Session()
holder = change_crawler_session(url_login, data, url_account_files, session)
soup = soup_function(holder)

found = 0
for link in soup.find_all('a'):
    if link.get('href') is not None and path_to_download_tag in link.get('href'):
        found+=1
        data = link.parent.parent.get_text().replace(u'\xa0', u' ').split('\n')
        if data[9] != '':
            name = data[7]+" - "+data[9]
        else:
            name = data[7]
        # Remove duplicate whitespace
        name = " ".join(name.split())
        url_download_list[name] = link

if found == 0:
    print("No download links found?")
    print(soup)
    exit(1)
        
for name in url_download_list:
    print("== File:",name)    
    if not os.path.exists(os.path.join("PaizoLibrary",name)):
        print("Not in library, trying to find download link")
        link = url_download_list[name]
        new_holder = session.get(link.get('href'))
        soup_var = soup_function(new_holder)
        ok = False
        for inner_link in soup_var.find_all('a'):
            if get_file(inner_link, exts, session, name):
                ok = True
        if not ok:
            print("*********** No download link found? *************")
    else:
        print("Already in library, skipping")
            
