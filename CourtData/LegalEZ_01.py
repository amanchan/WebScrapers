#-------------------------------------------------------------------------------
# Name:        DallasCityScraper
# Purpose:  To automate retrieval of data from website
#       http://dallascityhall.com/departments/sustainabledevelopment/buildinginspection/Pages/permit_reports2.aspx'
#       This site accepts a search string like 'Comcast' and takes you to page
#       http://licensing.copyright.gov/search/DisplayLegalName.jsp
#       From this page, user can select the actual company name and view
#       associated information (ID number, first community and state) on page
#       http://licensing.copyright.gov/search/SelectCommunity.jsp
#       From this page user select the community,
#       then click appropriate button to view either filing period or
#       associated communities information.
#       Get Filing Periods take you to page
#       http://licensing.copyright.gov/search/SelectFilingPeriod2.jsp
#       Get Associated communities takes you to page:
#       http://licensing.copyright.gov/search/DisplayAssociatedCommunities.jsp
#       You can go to the associated communities page given beow from
#       "Filing Periods" page as well
#       http://licensing.copyright.gov/search/DisplayAssociatedCommunities2.jsp
# Author:      AnilM
#
# Created:     06/02/2015
# Copyright:   (c) AnilM 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from __future__ import ( division, absolute_import, print_function, unicode_literals )

import sys, os, tempfile, logging

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse
import mechanize
import cookielib
from bs4 import BeautifulSoup
import html2text
import twill.commands
import re,sys
import argparse
import csv
import datetime
import time

def reopenSite(siteUrl):
    status = 0
    try:
        page = br.open(siteUrl)
    except (mechanize.HTTPError,mechanize.URLError) as e:
        time.sleep(25)
        status = 1

    if (status != 0):
        exit

    html = page.read()
    soup = BeautifulSoup(html)
#    print (soup)
    # Select the first (index zero) form
    br.select_form(nr=0)

    #disclaimerForm = soup.find("form", {"name":"main"})

    #control = br.form.find_control("disclaimer")
    #control.selected=True
    for i in range(0, len(br.find_control(type="checkbox").items)):
        if "modify" not in str(br.find_control(type="checkbox").items[i]):
            br.find_control(type="checkbox").items[i].selected =True
    control1 = br.form.find_control("text")
    control1.disabled=True
    br.submit()

    htmlnext = br.response().read()

    soup = BeautifulSoup(htmlnext)
    print (soup)
    pass

def openSite(siteUrl, destPath):
    status = 0
    try:
        page = br.open(siteUrl)
    except (mechanize.HTTPError,mechanize.URLError) as e:
        time.sleep(25)
        status = 1

    if (status != 0):
        exit

    html = page.read()
    soup = BeautifulSoup(html)
    print (soup)
    # Select the first (index zero) form
    br.select_form(nr=0)

    #disclaimerForm = soup.find("form", {"name":"main"})

    #control = br.form.find_control("disclaimer")
    #control.selected=True
    for i in range(0, len(br.find_control(type="checkbox").items)):
        if "modify" not in str(br.find_control(type="checkbox").items[i]):
            br.find_control(type="checkbox").items[i].selected =True
    control1 = br.form.find_control("text")
    control1.disabled=True
    br.submit()

    htmlnext = br.response().read()

    soup = BeautifulSoup(htmlnext)
    print (soup)
    date1 = datetime.date(2015, 3, 15)

    for num in range(1,375):
        try:
            br.select_form(nr=2)
            br.form['lastName'] = srchString
            br.form['site'] = ['CIVIL']
            br.form['courtSystem'] = ['C']
            br.form['partyType'] = ['DEF']
            d1 = date1.strftime("%m/%d/%Y")
            print (d1) ;
            date1 = date1 + datetime.timedelta(days=1)
            br.form['filingDate'] = d1
            br.submit()
            htmlnext = br.response().read()
            soup = BeautifulSoup(htmlnext)
        except :
            #outFile.close()
            #outFile = open(legalNameFile,'a');
            reopenSite(siteUrl)
            continue
        #print (soup)

# Find span for export <span class="export csv">CSV </span></a>|
# <div class="exportlinks">Export options:
        exportSpan = soup.find("div", {"class":"exportlinks"})
        #print (exportSpan)

        try:
            downLinks = exportSpan.findAll('a')
            link = downLinks[0]
            fileUrl = 'http://casesearch.courts.state.md.us'
            fileUrl += link['href']
            br.follow_link(text='CSV')
            csvdata = br.response().read()
            outFile.writelines( csvdata )
            response= br.back(2)
            htmlnext = response.read()
            #soup = BeautifulSoup(htmlnext)
            #print (soup)
        except :
            continue
    #print (soup)
    #download_or_extract(fileUrl, destPath )
    #outFile.close()
    pass


# --------------------------------------------------------------------------
# Main Start here.
# --------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--url', help='url help')
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
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0')]
br.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
#print parser.parse_args(['--name'])
mainSite = 'http://texasbar.com/'
#mainSite = 'http://casesearch.courts.state.md.us/casesearch/processDisclaimer.jis'
destPath = 'C:\\Users\\amanchanda\\Downloads\\Research\\Legal\\'

try:

    openSite(mainSite, destPath)
    outFile.close()
except (mechanize.HTTPError,mechanize.URLError) as e:
    outFile.close()
    exit ;
pass


