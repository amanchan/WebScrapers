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
import time

def extract_site_data(url, filename, desc=None):
    try:
        page = br.open(url)
    except (mechanize.HTTPError,mechanize.URLError) as e:
        print ("Could not open: " + url)

    html = page.read()
    soup = BeautifulSoup(html)
#    print (soup)
    allTables = soup.findAll("table")
    dataTable = allTables[2]
#    print (dataTable)
    dataFileName = os.path.join(desc, filename + ".txt")
    dataFile = open(dataFileName,'a');
    for row in dataTable.findAll('tr')[1:]:
        dataLine = ""
        all_cols = [list_item for list_item in row.findAll('td')]
        for aCol in all_cols:
            abc = aCol.get_text()
            if (abc != ""):
                if (dataLine != ""):
                    dataLine += "|" + abc
                else:
                    dataLine = abc
        if (dataLine != ""):
            dl = dataLine.replace("\xa0", "")
            dl1 = dl.encode('ascii','xmlcharrefreplace')
            try:
                dataFile.write(dl1 + "\n")
            except :
                dataFile.close()
                return
    dataFile.close()

def download_or_extract(url, desc=None):
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)

    if not filename:
        filename = 'downloaded.file'
    if desc:
        filename = os.path.join(desc, filename)
        extn = filename.split(".")[-1]
        fname = filename.split(".")[0]
        if (extn != 'aspx'):
#            download_file(url, desc)
            pass
        else:
            extract_site_data(url, fname, desc)

def download_file(url, desc=None):
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    try:
        u = urllib2.urlopen(url)
    except (mechanize.HTTPError,mechanize.URLError) as e:
        print ("Could not open: " + url)
        return filename

    if not filename:
        filename = 'downloaded.file'
    if desc:
        filename = os.path.join(desc, filename)

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()
    return filename

def openSite(siteUrl, destPath):
    status = 0
    try:
        page = br.open(siteUrl)
    except (mechanize.HTTPError,mechanize.URLError) as e:
        fileCommunity.close()
        dataFile.close()
        time.sleep(25)
        status = 1

    if (status != 0):
        exit

    html = page.read()
    soup = BeautifulSoup(html)
    divContainingTable = soup.find("div", {"id":"mainContainer"})
    # Select the 3rd (index zero) table

#    soup = BeautifulSoup(divContainingTable)
#    print (divContainingTable)

# loop 1
# In Table 1 (2013 - 2015) download all files (Excel & pdf)
# loop 2
# In Table 2 (2013 - 2015) download all files (pdf and download data into CSV
# loop 3
# In Table 3 (2013 - 2015) download all files (pdf and download data into CSV

    allTables = divContainingTable.findAll("table")

    # For each row find tag <a to download file
    for tbl in allTables:
        for row in tbl.findAll('tr')[1:]:
            downLinks = row.findAll('a')
            for link in downLinks:
                fileUrl = 'http://dallascityhall.com'
                fileUrl += link['href']
                download_or_extract(fileUrl, destPath )
            #print fileUrl
    # end of loop to find file links
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
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#print parser.parse_args(['--name'])
mainSite = 'http://dallascityhall.com/departments/sustainabledevelopment/buildinginspection/Pages/permit_reports2.aspx'
destPath = 'H:\\Research\\DallasCity_06022015\\'


try:
    openSite(mainSite, destPath)
except (mechanize.HTTPError,mechanize.URLError) as e:
    exit ;


