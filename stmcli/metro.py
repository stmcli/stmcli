import urllib.request
import xmltodict
from stmcli import data


def line_to_english(line):
    if line == "verte":
        return "green"
    elif line == "jaune":
        return "yellow"
    elif line == "bleu":
        return "blue"
    else:
        return line


def line_to_french(line):
    if line == "green":
        return "verte"
    elif line == "yellow":
        return "jaune"
    elif line == "blue":
        return "bleu"
    else:
        return line


def print_status(line, status, language):
    if language == "Anglais":
        status = ("{0} line status: {1}".format(line_to_english(line),
                                                status))
        print(data.strip_accents(status))

    else:
        status = ("statut de la ligne {0}: {1}".format(line_to_french(line),
                                                       status))
        print(data.strip_accents(status))


def metro_status(line, language):
    # Getting XML data
    URL = "http://www2.stm.info/1997/alertesmetro/esm.xml"
    metro_website = urllib.request.urlopen(URL)
    metro_info = metro_website.read()
    metro_website.close()
    xml_data = xmltodict.parse(metro_info)

    for i in xml_data['Root']['Ligne']:
        nline = i["NoLigne"]
        if (line == "green" and nline == "1" or line == "all" and nline == "1" or line == "verte" and nline == "1"):
            print_status("green", i['msg' + language], language)

        if line == "orange" and nline == "2" or line == "all" and nline == "2":
            print_status("orange", i['msg' + language], language)

        if line == "yellow" and nline == "4" or line == "all" and nline == "4" or line == "jaune" and nline == "4":
            print_status("yellow", i['msg' + language], language)

        if line == "blue" and nline == "5" or line == "all" and nline == "5" or line == "bleu" and nline == "5":
            print_status("blue", i['msg' + language], language)
