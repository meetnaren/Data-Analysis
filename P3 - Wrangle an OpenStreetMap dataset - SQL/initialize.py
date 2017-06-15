#importing required modules - XML, CSV, SQLite and plotting
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import sqlite3
import string as s
import pandas as pd
import matplotlib.pyplot as plt
import plotly as pltly
from plotly.graph_objs import *

OSM_FILE='NYC_SAMPLE.OSM'
DATABASE='OpenStreetMap.db'
mapbox_access_token='pk.eyJ1IjoibWVldG5hcmVuIiwiYSI6ImNqM3htbWtrMjAwMXUyd3BteXlpb2lmOXkifQ.tOV33V0Iv2N_Lqw--qqUwg'

pltly.tools.set_credentials_file(username='meetnaren', api_key='02FpawrSfFQjW88Ry5UA')

# Helper functions for connecting to database, fetching elements from XML file
def connect_db():
    conn=sqlite3.connect(DATABASE)
    c=conn.cursor()
    return c

def execute_query(cursor, query):
    return pd.DataFrame(cursor.execute(query).fetchall())

def get_element(osm_file, tags=('node', 'way')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

# This code is from the case study
class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
