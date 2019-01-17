#!/usr/bin/python

from lxml import etree
import re
import json
import sys

# usage: python export-clipperz.py Clipperz_Export.html
# creates file 'import-for-bitwarden.json'

root = etree.parse(sys.argv[1], etree.HTMLParser())
# print(etree.tostring(root, pretty_print=True, method="html"))

htmlList = root.xpath('//ul')[0]
# print(etree.tostring(htmlList[0], pretty_print=True))

matcherUser = re.compile('login|username|benutzername', re.IGNORECASE)
matcherPassword = re.compile('passwor[td]', re.IGNORECASE)
matcherUrl = re.compile('link|web address|url', re.IGNORECASE)

export = {'items': [], 'folders': []}
for entry in htmlList:

    item = {
        'name': entry.xpath('.//h2')[0].text,
        'login': {'uris': []},
        'fields': [],
        'type': 1,
        'folderId': None,
        'organizationId': None,
        'favorite': False,
        'collectionIds': None

    }

    if len(entry.xpath('.//p')):
        comment = entry.xpath('.//p')[0].text
        item['notes'] = comment
    fields = entry.xpath('.//dl/*')
    # print("{}: {}".format(i, etree.tostring(entry)))
    listOfNameAndValues = list(zip(fields[::2], fields[1::2]))
    foundLogin = False
    foundPassword = False

    for pair in listOfNameAndValues:
        name = pair[0].text
        value = pair[1].text
        if name is None:
            continue
        if not foundLogin and matcherUser.match(name):
            item['login']['username'] = value
            foundLogin = True
        elif not foundPassword and matcherPassword.match(name):
            item['login']['password'] = value
            foundPassword = True
        elif matcherUrl.match(name):
            item['login']['uris'].append({'uri': value})
        else:
            item['fields'].append({'name': name, 'value': value, 'type': 1 if pair[1].get('class') == 'hidden' else 0})

    export['items'].append(item)

with open('import-for-bitwarden.json', 'w') as outfile:
    json.dump(export, outfile)
