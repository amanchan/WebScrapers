#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      AManchanda
#
# Created:     31/08/2015
# Copyright:   (c) AManchanda 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import mechanize
import cookielib
from bs4 import BeautifulSoup
import html2text
import twill.commands
import re,sys
import argparse
import csv

def retrieveData(br, opt):
    br.select_form(nr=0)
    tmp=[]
    tmp.append(opt)

    br.form['cost'] = tmp
    br.form['crit'] = ['0']

    br.submit()

    html = br.response().read()
    soup = BeautifulSoup(html)
#    soup = soup.prettify(formatter=lambda s: s.replace(u'\xa0', '|'))

    print (soup)
    pass
###############################################################################
# Main Start here. Get the search string from command line
parser = argparse.ArgumentParser()
parser.add_argument('--url', help='url help')
parser.add_argument('--name', help='name help')
args = parser.parse_args()

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Search for Comcast
#print parser.parse_args(['--name'])
mainSite = 'http://nsgc.org/p/cm/ld/fid=164'
mainSite = 'http://nsgc.org'

br.open(mainSite)
target_url='p/cm/ld/fid=164'
for link in br.links():
    print(link)
    # Link(base_url='http://www.example.com/', url='http://www.rfc-editor.org/rfc/rfc2606.txt', text='RFC 2606', tag='a', attrs=[('href', 'http://www.rfc-editor.org/rfc/rfc2606.txt')])
    print(link.url)
    # http://www.rfc-editor.org/rfc/rfc2606.txt
    if link.url == target_url:
        print('match found')
        # match found
        break

br.follow_link(link)   # link still holds the last value it had in the loop
print(br.geturl())



# Select the first (index zero) form
#br.select_form(nr=0)
# Form with name 'form1' has a select list of options (Company names) to choose
forms = mechanize.ParseResponse(br.response(), backwards_compat=False)

#forms = mechanize.ParseString(html, 'form1')
form = forms[0]
control = form.controls[1]

stateNameOpts = [item.attrs['value'] for item in control.items]

print stateNameOpts
# Write data rows
for stateName in stateNameOpts:
#    print control
    if (stateName <> ''):
        retrieveData(br, stateName)
        response = br.back(1)
        html = response.read()


