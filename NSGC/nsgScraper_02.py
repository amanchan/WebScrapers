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
br = mechanize.Browser(factory=mechanize.RobustFactory())

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

mainSite = 'http://www.ncbi.nlm.nih.gov/clinvar'
mainSite='http://www.ncbi.nlm.nih.gov/portal/utils/file_backend.cgi?Db=clinvar&HistoryId=NCID_1_148836612_130.14.18.97_5555_1442170992_1632873268_0MetA0_S_HStore&QueryKey=1&Sort=Position&Filter=all&CompleteResultCount=3211&Mode=file&View=tabular&p$l=Email&portalSnapshot=%2Fprojects%2FClinVar%2Fclinvar_entrez_package%401.30&BaseUrl=&PortName=live&FileName='
br.open(mainSite)
html = br.response().read()
soup = BeautifulSoup(html)
print (soup)
forms = mechanize.ParseResponse(br.response(), backwards_compat=False)

#form = forms[0]
br.select_form(nr=0)

br.form['term'] = 'brca1[gene]' #tmp
br.submit()
response= br.response()
html = br.response().read()
soup = BeautifulSoup(html)
print (soup)
#forms = mechanize.ParseResponseEx(br.response(), backwards_compat=False)
pagination = soup.find('a', attrs={'id':'EntrezSystem2.PEntrez.clinVar.clinVar_Entrez_ResultsPanel.Entrez_Pager.Page'})
print (pagination)
#
#response = br.back(1)

br.select_form(nr=0)
br.form['term'] = 'brca1[gene]'
br.form['EntrezSystem2.PEntrez.clinVar.clinVar_Entrez_ResultsPanel.Entrez_DisplayBar.SendTo'] = ['File']
mycontrols = br.form.controls
for control in br.form.controls:
    if hasattr(control, 'name'):
        if control.name == 'EntrezSystem2.PEntrez.clinVar.clinVar_Entrez_ResultsPanel.Entrez_DisplayBar.SendToSubmit':
#    if hasattr(control, 'cmd'):
#        if control.Cmd == 'File': #'EntrezSystem2.PEntrez.clinVar.clinVar_Entrez_ResultsPanel.Entrez_Pager.Page':
            br.submit('EntrezSystem2.PEntrez.clinVar.clinVar_Entrez_ResultsPanel.Entrez_DisplayBar.SendToSubmit')
            break

#br.submit(name='EntrezSystem2.PEntrez.clinVar.clinVar_Entrez_ResultsPanel.Entrez_DisplayBar.SendToSubmit')
response= br.response()
html = br.response().read()
soup = BeautifulSoup(html)
print (soup)
#br.form['EntrezSystem2.PEntrez.clinVar.clinVar_Entrez_ResultsPanel.Entrez_Pager.CurrPage'] = '2' #tmp
for link in br.links():
#    if control.name == 'EntrezSystem2.PEntrez.clinVar.clinVar_Entrez_ResultsPanel.Entrez_Pager.cPage':
#        control.value = '2'
    if link.url == '#':
        if hasattr(link, 'text'):
            if link.text == 'Next >': #'EntrezSystem2.PEntrez.clinVar.clinVar_Entrez_ResultsPanel.Entrez_Pager.Page':
                response = br.follow_link(link)
                break
#br.form['EntrezSystem2.PEntrez.clinVar.clinVar_Entrez_ResultsPanel.Entrez_Pager.cPage'][0] = '2' #tmp

html = response.read()
soup = BeautifulSoup(html)
print (soup)

links = soup.find_all('a', href=True)
print (links[272])
br.follow_link(links[272])
br.follow_link(pagination)
html = br.response().read()
soup = BeautifulSoup(html)
print (soup)
target_url='#'
links = pagination.findall('a');
for link in links:
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


