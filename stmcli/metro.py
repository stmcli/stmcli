#!/usr/bin/env python3

import urllib.request
import xmltodict


def metro_status(line, language):
    # Getting XML data
    URL = "http://www2.stm.info/1997/alertesmetro/esm.xml"
    metro_website = urllib.request.urlopen(URL)
    metro_info = metro_website.read()
    metro_website.close()

    xml_data = xmltodict.parse(metro_info)

    for i in xml_data['Root']['Ligne']:
        nline = i["NoLigne"]
        if line == "green" and nline == "1" or line == "all" and nline == "1":
            print("Green line status: {0}"
                  .format(i["msg{0}".format(language)]
                          .encode('ascii', 'replace').decode('utf-8')))

        if line == "orange" and nline == "2" or line == "all" and nline == "2":
            print("Orange line status: {0}"
                  .format(i["msg{0}".format(language)]
                          .encode('ascii', 'replace').decode('utf-8')))

        if line == "yellow" and nline == "4" or line == "all" and nline == "4":
            print("Yellow line status: {0}"
                  .format(i["msg{0}".format(language)]
                          .encode('ascii', 'replace').decode('utf-8')))

        if line == "blue" and nline == "5" or line == "all" and nline == "5":
            print("Blue line status: {0}"
                  .format(i["msg{0}".format(language)]
                          .encode('ascii', 'replace').decode('utf-8')))
