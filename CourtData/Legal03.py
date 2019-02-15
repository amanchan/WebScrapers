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
        infoType = 0

        outFile1.writelines("%s" % caseNumber);
        outFile2.writelines("%s" % caseNumber);
        outFile3.writelines("%s" % caseNumber);
        outFile4.writelines("%s" % caseNumber);
        outFile5.writelines("%s" % caseNumber);
        outFile11.writelines("%s" % caseNumber);
        for anh5 in all_tables:
            h6tag = anh5.find_all("h6")
            if len(h6tag) > 0:
                if h6tag[0].text == 'Attorney(s) for the Plaintiff':
                    outFile7.writelines("%s" % caseNumber);
                    infoType = 7
                elif h6tag[0].text == 'Attorney(s) for the Defendant':
                    outFile8.writelines("%s" % caseNumber);
                    infoType = 8
                elif h6tag[0].text == 'Attorney(s) for the Other':
                    outFile9.writelines("%s" % caseNumber);
                    infoType = 9
                elif h6tag[0].text == 'Attorney(s) for the Ward':
                    outFile9.writelines("%s" % caseNumber);
                    infoType = 16
                elif h6tag[0].text == 'Attorney(s) for the Interested Party':
                    outFile9.writelines("%s" % caseNumber);
                    infoType = 17
                elif h6tag[0].text == 'Attorney(s) for the Garnishee':
                    outFile9.writelines("%s" % caseNumber);
                    infoType = 18
                elif h6tag[0].text == 'Plaintiff Aliases':
                    outFile9.writelines("%s" % caseNumber);
                    infoType = 19
                elif h6tag[0].text == 'Defendant Aliases':
                    outFile9.writelines("%s" % caseNumber);
                    infoType = 20
                elif h6tag[0].text == 'Other Aliases':
                    outFile9.writelines("%s" % caseNumber);
                    infoType = 21
                else:
                    outFileWarn.writelines("%s" % caseNumber);
                    outFileWarn.writelines("|%s\n" % h6tag[0].text);
                continue
            if infoType == 6:
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    outFile6.writelines("%s" % caseNumber);
                    contents1 = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    contents2 = [re.sub(r'(\0x5f)+', "", x)for x in contents1]
                    contents3 = [re.sub(r'(\0x0a)+', "", x)for x in contents2]
                    contents4 = [re.sub(r'(\0x0d)+', "", x)for x in contents3]
                    contents = [re.sub(r'(\0xc2)+', "", x)for x in contents4]
                    try:
                        outFile6.writelines( "|\"%s\"" % item for item in contents )
                        outFile6.writelines("\n");
                        outFile11.writelines( "|\"%s\"" % item for item in contents )
                    except:
                        outFile6.writelines("\n");
                        outFileError.writelines("%s - process\n" % caseNumber)
                        continue

                 #continue
            elif infoType == 1:
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    contents = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    #outFile1.writelines("%s" % caseNumber);
                    outFile1.writelines( "|\"%s\"" % item for item in contents )
                    outFile11.writelines( "|\"%s\"" % item for item in contents )
            elif infoType == 2:
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    contents = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    #outFile2.writelines("%s" % caseNumber);
                    outFile2.writelines( "|\"%s\"" % item for item in contents )
                    outFile11.writelines( "|\"%s\"" % item for item in contents )
            elif infoType == 3:
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    contents = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    #outFile3.writelines("%s" % caseNumber);
                    outFile3.writelines( "|\"%s\"" % item for item in contents )
                    outFile11.writelines( "|\"%s\"" % item for item in contents )
            elif infoType == 4:
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    contents = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    #outFile3.writelines("%s" % caseNumber);
                    outFile4.writelines( "|\"%s\"" % item for item in contents )
                    outFile11.writelines( "|\"%s\"" % item for item in contents )
            elif infoType == 5:
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    contents = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    #outFile5.writelines("%s" % caseNumber);
                    outFile5.writelines( "|\"%s\"" % item for item in contents )
                    outFile11.writelines( "|\"%s\"" % item for item in contents )
            elif infoType == 7:
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    contents = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    outFile7.writelines( "|\"%s\"" % item for item in contents )
                    outFile11.writelines( "|\"%s\"" % item for item in contents )
            elif infoType == 8:
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    contents = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    outFile8.writelines( "|\"%s\"" % item for item in contents )
                    outFile11.writelines( "|\"%s\"" % item for item in contents )
            elif infoType == 9:
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    contents = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    outFile9.writelines( "|\"%s\"" % item for item in contents )
                    outFile11.writelines( "|\"%s\"" % item for item in contents )
            elif infoType == 10:
                spanTags = anh5.find_all("span")
                if len(spanTags) > 0:
                    contents = [re.sub(r'(\n)+', "", x.text)for x in spanTags]
                    outFile10.writelines( "|\"%s\"" % item for item in contents )
                    outFile11.writelines( "|\"%s\"" % item for item in contents )
            h5tag = anh5.find_all("h5")
            if len(h5tag) == 0:
                #h6tag = anh5.find_all("h6")
                #if len(h6tag) > 0:
                #    if h6tag[0].text == 'Attorney(s) for the Plaintiff':
                #        infoType = 3
                continue


            if h5tag[0].text == 'Case Information':
                infoType = 1
            elif h5tag[0].text == 'Plaintiff Information':
                infoType = 2
            elif h5tag[0].text == 'Defendant Information':
                infoType = 3
            elif h5tag[0].text == 'Other Party Information':
                infoType = 4
            elif h5tag[0].text == 'Issues Information':
                infoType = 5
            elif h5tag[0].text == 'Document Tracking':
                infoType = 6
            elif h5tag[0].text == 'Ward Information':
                infoType = 11
            elif h5tag[0].text == 'Interested Party Information':
                infoType = 12
            elif h5tag[0].text == 'Garnishee Information':
                infoType = 13
            elif h5tag[0].text == 'Court Scheduling Information':
                infoType = 14
            elif h5tag[0].text == 'Court Scheduling Information':
                infoType = 15
            else:
                infoType = 10
                outFile10.writelines("\n%s" % caseNumber);
                outFile10.writelines("|%s" % h5tag[0].text);
            pass
        outFile1.writelines("\n");
        outFile2.writelines("\n");
        outFile3.writelines("\n");
        outFile4.writelines("\n");
        outFile5.writelines("\n");
        outFile7.writelines("\n");
        outFile8.writelines("\n");
        outFile9.writelines("\n");
        outFile11.writelines("\n");
        #Get all H5's
        #<h5>Case Information</h5>
        #<h5>Plaintiff/Petitioner Information</h5>
        #<h5>Defendant/Respondent Information</h5>
        #<h5>Document Tracking</h5>
        #all_h5s = soup.find_all("h5")
        #print all of this
        #for anh5 in all_h5s:
        #    print (anh5)
        #    pass

        #docTrack_h5 = all_h5s[3]
        #ps1 = docTrack_h5.find_parent()
        #ps2 = docTrack_h5.find_siblings()
        #print(ps2[0])

        # data received for case
        # Issue Information
        # Document Tracking
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
destPath = 'C:\\Users\\amanchanda\\Downloads\\Research\\Legal\\Data_02262016'
caseNumber='102430FL'
courtId='15'

# Open the file for reading.
with open('C:\\Users\\amanchanda\\Downloads\\Research\\Legal\\Data_02262016\\montCaseFile.txt', 'r') as infile:

    data = infile.read()  # Read the contents of the file into memory.

# Return a list of the lines, breaking at line boundaries.
my_list = data.splitlines()

fNameFile1 = destPath + courtId +'_CasesInfo.csv'
outFile1 = open(fNameFile1,'w');
fNameFile2 = destPath + courtId +'_PlaintiffInfo_Cases.csv'
outFile2 = open(fNameFile2,'w');
fNameFile3 = destPath + courtId +  '_Defendent_Cases.csv' #
outFile3 = open(fNameFile3,'w');
fNameFile4 = destPath + courtId + '_OtherParty_Cases.csv'
outFile4 = open(fNameFile4,'w');
fNameFile5 = destPath + courtId + 'IssueInfo_Cases.csv'
outFile5 = open(fNameFile5,'w');
fNameFile6 = destPath + courtId + 'TrackInfo_Cases.csv'
outFile6 = open(fNameFile6,'w');
fNameFile7 = destPath + courtId + '_AttPlaintiff.csv'
outFile7 = open(fNameFile7,'w');
fNameFile8 = destPath + courtId + '_AttDefParty.csv'
outFile8 = open(fNameFile8,'w');
fNameFile9 = destPath + courtId + '_AttOtherParty.csv'
outFile9 = open(fNameFile9,'w');
fNameFile10 = destPath + courtId + '_OtherInfo.csv'
outFile10 = open(fNameFile10,'w');
fNameFile11 = destPath + courtId + '_CaseDetail.csv'
outFile11 = open(fNameFile11,'w');

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

outFile1.close()
outFile2.close()
outFile3.close()
outFile4.close()
outFile5.close()
outFile6.close()
outFile7.close()
outFile8.close()
outFile9.close()
outFile10.close()
outFile11.close()
outFileWarn.close()
outFileError.close()

