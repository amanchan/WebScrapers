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

#page = ""


def openSite(siteUrl):
    status = 0
    try:
        page = br.open(siteUrl)
        return 0
    except (mechanize.HTTPError,mechanize.URLError) as e:
        time.sleep(35)
        print ("error")
        return 1
    pass

def processSite(page):
    html = page.read()
    soup = BeautifulSoup(html)
    print (soup)
    # Select the second form (by City)
    try:
        form = br.forms[2]
        print (form)
        form['PPlCityName'] = 'Plano'
        form['State'] = ['TX']
        form['County'] = ['43']
        form['Zip'] = '75024'
        response = urlopen(form.click()).read()
        print (response)

        #br.select_form(nr=2)
        #br.form['PPlCityName'] = 'Plano'
        #br.form['State'] = ['TX']
        #br.form['County'] = ['43']
        #br.form['Zip'] = '75024'
        #br.form['ShowPrinter'] = '1'
        #br.form['Find'] = '0'
        #br.form['Submitted'] = '1'
        #br.submit()

        htmlnext = br.response().read()
        soup = BeautifulSoup(htmlnext)
        print (soup)
        outFileWarn.write(htmlnext)
    except :
        outFileError.writelines("%s - process\n" )
        return 1
    return 0
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
#mainSite = 'https://www.texasbar.com/AM/Template.cfm?Section=Public_Home'
mainSite = 'https://www.texasbar.com/AM/Template.cfm?Section=Find_A_Lawyer&Template=/CustomSource/MemberDirectory/Search_Form_Client_Main.cfm'
destPath = 'C:\\Users\\amanchanda\\Downloads\\Research\\LegalEZ\\'

fNameFile1 = destPath + 'TX_ContactInfo.txt'
contactFile = open(fNameFile1,'w');
fNameFile2 = destPath +'TX_Summary.txt'
summaryFile = open(fNameFile2,'w');
fNameFile3 = destPath + 'TX_PracticeInfo.txt'
practiceFile = open(fNameFile2,'w');

fNameError = destPath  +'TX_error.txt'
outFileError = open(fNameError,'w');
fNameWarn = destPath  +'TX_warn.txt'
outFileWarn = open(fNameWarn,'w');

try:
    val1 = 1
    while val1 != 0:
        try:
            page = br.open(mainSite)
            val1 = processSite(page)
        except (mechanize.HTTPError,mechanize.URLError) as e:
            time.sleep(45)
            print ("error" + caseNumber)
    pass
except (mechanize.HTTPError,mechanize.URLError) as e:
    print("error")
pass


contactFile.close()
summaryFile.close()
practiceFile.close()
outFileWarn.close()
outFileError.close()

