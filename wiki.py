from pyquery import PyQuery as pq
from lxml import etree
import wikipedia as wiki
import re
import sys

#input is spider name
name = "mouse spider"

def get_image(name):

    page = wiki.page(name).html()

    d = pq(page)
    table = d('table.infobox img')

    if len(table) == 0:
    	print('Unable to find the table element')

    else:
        print('https:' + table.attr['src'])

get_image(name)