#!/usr/bin/env python3

import urllib.request
import xmltodict


def print_status(line, status, language):
    if language == "en":
        print("{0} line status: {1}"
              .format(line, status.encode('ascii', 'replace').decode('utf-8')))
    else:
        print("statut de la ligne {0}: {1}"
              .format(line, status.encode('ascii', 'replace').decode('utf-8')))


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
            if language == "en":
                print_status("green", i['msgAnglais'], language)
            else:
                print_status("verte", i['msgFrancais'], language)
        if line == "orange" and nline == "2" or line == "all" and nline == "2":
            if language == "en":
                print_status("orange", i['msgAnglais'], language)
            else:
                print_status("orange", i['msgFrancais'], language)

        if line == "yellow" and nline == "4" or line == "all" and nline == "4":
            if language == "en":
                print_status("yellow", i['msgAnglais'], language)
            else:
                print_status("jaune", i['msgFrancais'], language)

        if line == "blue" and nline == "5" or line == "all" and nline == "5":
            if language == "en":
                print_status("blue", i['msgAnglais'], language)
            else:
                print_status("bleu", i['msgFrancais'], language)
