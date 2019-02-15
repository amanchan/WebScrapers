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
from array import array
#page = ""


def openSite(siteUrl, destPath, caseNumber):
    status = 0
    try:
        page = br.open(siteUrl)
        return 0
    except (mechanize.HTTPError,mechanize.URLError) as e:
        time.sleep(35)
        print ("error" + caseNumber)
        return 1
    pass

def processSite(page, caseNumber):
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
    #print (soup)
    date1 = datetime.date(2015, 3, 15)

    try:
        br.select_form(nr=3)
        br.form['caseId'] = caseNumber
        br.form['locationCode'] = [courtId]
        br.submit()
        htmlnext = br.response().read()
        soup = BeautifulSoup(htmlnext)
        #print (soup)

        all_tables = soup.find_all("table")

        #mytable = all_tables[17]
        #print(mytable)
        #next1 = all_tables[18]
        #print(next1)
        historyFound = False
        infoType = -1

        i = 0
        for fname in my_files:
            outFile[i].writelines("%s" % caseNumber)
            i = i + 1
            if i > 10 :
                break;
        pass

        outFile[23].writelines("%s" % caseNumber);
        outFile[24].writelines("%s" % caseNumber);

        for anh5 in all_tables:
            h6tag = anh5.find_all("h6")
            if len(h6tag) > 0:
                if h6tag[0].text == 'Attorney(s) for the Plaintiff':
                    outFile[11].writelines("%s" % caseNumber);
                    infoType = 11
                elif h6tag[0].text == 'Attorney(s) for the Defendant':
                    outFile[12].writelines("%s" % caseNumber);
                    infoType = 12
                elif h6tag[0].text == 'Attorney(s) for the Other':
                    outFile[13].writelines("%s" % caseNumber);
                    infoType = 13
                elif h6tag[0].text == 'Attorney(s) for the Ward':
                    outFile[15].writelines("%s" % caseNumber);
                    infoType = 15
                elif h6tag[0].text == 'Attorney(s) for the Interested Party':
                    outFile[14].writelines("%s" % caseNumber);
                    infoType = 14
                elif h6tag[0].text == 'Attorney(s) for the Garnishee':
                    outFile[16].writelines("%s" % caseNumber);
                    infoType = 16
                elif h6tag[0].text == 'Plaintiff Aliases':
                    outFile[17].writelines("%s" % caseNumber);
                    infoType = 17
                elif h6tag[0].text == 'Defendant Aliases':
                    outFile[18].writelines("%s" % caseNumber);
                    infoType = 18
                elif h6tag[0].text == 'Other Aliases':
                    outFile[19].writelines("%s" % caseNumber);
                    infoType = 19
                elif h6tag[0].text == 'Interested Party Aliases':
                    outFile[20].writelines("%s" % caseNumber);
                    infoType = 20
                elif h6tag[0].text == 'Ward Aliases':
                    outFile[21].writelines("%s" % caseNumber);
                    infoType = 21
                elif h6tag[0].text == 'Debtor Aliases':
                    outFile[22].writelines("%s" % caseNumber);
                    infoType = 22

                else:
                    outFileWarn.writelines("%s" % caseNumber);
                    outFileWarn.writelines("|%s\n" % h6tag[0].text);
                continue
            if infoType == 23:
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    outFileTrack.writelines("%s" % caseNumber);
                    contents1 = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    contents2 = [re.sub(r'(\0x5f)+', "", x)for x in contents1]
                    contents3 = [re.sub(r'(\0x0a)+', "", x)for x in contents2]
                    contents4 = [re.sub(r'(\0x0d)+', "", x)for x in contents3]
                    contents = [re.sub(r'(\0xc2)+', "", x)for x in contents4]
                    try:
                        outFileTrack.writelines( "|\"%s\"" % item for item in contents )
                        outFileTrack.writelines("\n");
                        outFile[24].writelines( "|\"%s\"" % item for item in contents )
                        outFile[infoType].writelines( "|\"%s\"" % item for item in contents )
                    except:
                        outFileTrack.writelines("\n");
                        outFileError.writelines("%s - Tracking Data Error\n" % caseNumber)
                        continue

                 #continue
            elif (infoType >= 0 and infoType <= 22):
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    contents = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    #outFile1.writelines("%s" % caseNumber);
                    outFile[infoType].writelines( "|\"%s\"" % item for item in contents )
                    outFile[24].writelines( "|\"%s\"" % item for item in contents )

            h5tag = anh5.find_all("h5")
            if len(h5tag) == 0:
                #h6tag = anh5.find_all("h6")
                #if len(h6tag) > 0:
                #    if h6tag[0].text == 'Attorney(s) for the Plaintiff':
                #        infoType = 3
                continue


            if h5tag[0].text == 'Case Information':
                infoType = 0
            elif h5tag[0].text == 'Plaintiff Information':
                infoType = 1
            elif h5tag[0].text == 'Defendant Information':
                infoType = 2
            elif h5tag[0].text == 'Other Party Information':
                infoType = 3
            elif h5tag[0].text == 'Interested Party Information':
                infoType = 4
            elif h5tag[0].text == 'Ward Information':
                infoType = 5
            elif h5tag[0].text == 'Garnishee Information':
                infoType = 6
            elif h5tag[0].text == 'Court Scheduling Information':
                infoType = 7
            elif h5tag[0].text == 'Judgment Information':
                infoType = 8
            elif h5tag[0].text == 'Issues Information':
                infoType = 9
            elif h5tag[0].text == 'Document Tracking':
                infoType = 23

            else:
                infoType = 10
                outFile[10].writelines("\n%s" % caseNumber);
                outFile[10].writelines("|%s" % h5tag[0].text);
            pass
        i = 0
        for fname in my_files:
            outFile[i].writelines("\n")
            outFile[i].flush()
            i = i + 1

        pass

    except :
        print (caseNumber)
        outFileError.writelines("%s - process\n" % caseNumber)
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
mainSite = 'http://casesearch.courts.state.md.us/casesearch/'
#mainSite = 'http://casesearch.courts.state.md.us/casesearch/processDisclaimer.jis'
destPath = 'C:\\Users\\amanchanda\\Downloads\\Research\\Legal\\Data_022620116-2\\'
caseNumber='102430FL'
courtId='15'

# Open the file for reading.
with open('C:\\Users\\amanchanda\\Downloads\\Research\\Legal\\Data_022620116-2\\montCaseFile2.txt', 'r') as infile:

    data = infile.read()  # Read the contents of the file into memory.

# Return a list of the lines, breaking at line boundaries.
my_list = data.splitlines()
outFile = []
my_files = ['CasesInfo',
'Plaintiff', 'Defendent', 'OtherParty', 'IntParty', 'Ward', 'Garnishee', 'Issue', 'ScheduleInfo',
'JudgementInfo', 'OtherOnfo',
#11
'AttyPlaintiff', 'AttyDefendent', 'AttyOtherParty', 'AttyIntParty', 'AttyWard', 'AttyGarnishee',
#17
'AliasPlaintiff', 'AliasDefendent', 'AliasOtherParty', 'AliasIntParty', 'AliasWard', 'AliasDebtor',
#23
'TrackingOne', 'CaseDetail']

for fname in my_files:
    fNameFile = destPath + courtId + fname + '.txt'
    handle = open(fNameFile,'w')
    outFile.append(handle);
    pass

fNameTrack = destPath + courtId +'_Tracking.csv'
outFileTrack = open(fNameTrack,'w');
fNameError = destPath + courtId +'_error.csv'
outFileError = open(fNameError,'w');
fNameWarn = destPath + courtId +'_warn.csv'
outFileWarn = open(fNameWarn,'w');
for caseNumber in my_list:
    try:
        val1 = 1
        while val1 != 0:
            try:
                page = br.open(mainSite)
                val1 = processSite(page, caseNumber)
            except (mechanize.HTTPError,mechanize.URLError) as e:
                time.sleep(45)
                print ("error" + caseNumber)
        #break;
    except (mechanize.HTTPError,mechanize.URLError) as e:
        break;
    pass


i = 0
for fname in my_files:
    outFile[i].close();
    i = i + 1
    pass
outFileTrack.close()
outFileWarn.close()
outFileError.close()

