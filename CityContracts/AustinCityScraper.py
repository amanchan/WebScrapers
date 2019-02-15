#-------------------------------------------------------------------------------
# Name:        AustinCityScraper
# Purpose:  To automate retrieval of data from website
#       http://www.austintexas.gov
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
import datetime;
from datetime import timedelta;

def processData(html, dataFile):
    soup = BeautifulSoup(html)
#    print (soup)
    dataTable = soup.find("table")
#    print (dataTable)

    for row in dataTable.findAll('tr')[1:]:
        dataLine = ""
        all_cols = [list_item for list_item in row.findAll('td')]
        for aCol in all_cols:
            abc = aCol.get_text()
            #if (abc != ""):
            if (dataLine != ""):
                abc = abc.replace("\n"," ")
                abc = abc.replace("\r"," ")
                dataLine += "|" + abc
                #if (abc == '2006-063576 DS'):
                #    print (abc)
            else:
                dataLine = abc
                #if (abc == '1995-006121 MP'):
                #    print (abc)
        if (dataLine != ""):
            dl = dataLine.replace("\xa0", "")
            dl1 = dl.encode('ascii','xmlcharrefreplace')

            try:
                #print (dl1)
                dataFile.write(dl1 + "\n")
            except :
                dataFile.close()
                return
    dataFile.close()

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

def openSite(siteUrl):
    status = 0
    try:
        page = br.open(siteUrl)
    except (mechanize.HTTPError,mechanize.URLError) as e:
        time.sleep(25)
        status = 1

    if (status != 0):
        exit
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
mainSite = 'http://www.austintexas.gov/oss_permits/index.cfm'
destPath = 'H:\\Research\\AustinCity_06022015\\'
dataFileName = os.path.join(destPath, "construction_permit_rep_11.txt")
header = "permit_number|sub_type|work_type|permit_location|date_issued|work_description|status|folder_owner|folder_owner_addrhouse|folder_owner_addrstreet" + \
"|folder_owner_addrstreettype|folder_owner_addrunittype|folder_owner_addrunit|folder_owner_addrcity|folder_owner_addrprovince|folder_owner_addrpostal" + \
"|folder_owner_phone|property_owner|property_owner_addrhouse|property_owner_addrstreet|property_owner_addrstreettype|property_owner_addrunittype" + \
"|property_owner_addrunit|property_owner_addrcity|property_owner_addrprovince|property_owner_addrpostal|property_owner_phone|total_existing_bldg_footage" + \
"|total_new_add_footage|total_valuation_remodel|total_job_valuation|remodel_repair_footage|number_of_units|usage_category|legal_description\n"

td1 = timedelta(days=7)
td2 = timedelta(days=8)
td = timedelta(days=556)
#td = timedelta(days=2171)
#td = timedelta(days=2979)
#td = timedelta(days=3787)
#td = timedelta(days=4595)
#td = timedelta(days=5403)
#td = timedelta(days=6211)
#td = timedelta(days=7019)
#td = timedelta(days=7827)
#td = timedelta(days=6654)
startDate = datetime.date.today() - td

dataFile = open(dataFileName,'a');
dataFile.write(header)
dataFile.close();
loopCount = 0
while (loopCount <= 100):

    loopCount += 1
    try:
        openSite(mainSite)
        # Select the first (index zero) form
        br.select_form(nr=0)
        # Set the for parameter to srchString
        endDate = startDate + td1
        sDate = startDate.strftime("%m/%d/%Y")
        eDate = endDate.strftime("%m/%d/%Y")
        br.form['sDate'] = sDate
        br.form['eDate'] = eDate
        print (startDate, endDate)
        # Submit the form to go to
        br.submit()
        downloadUrl = br.response()
        html = br.response().read()
#        print (html)
        dataFile = open(dataFileName,'a');
        processData(html, dataFile)
#        print (downloadUrl.geturl())
        startDate += td2

    except (mechanize.HTTPError,mechanize.URLError) as e:
        print ("Error: StartDate -" + sDate)
        exit ;


