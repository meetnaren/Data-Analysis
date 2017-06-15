from initialize import *

counties={}

def audit_counties(elem):
    for tag in elem.iter('tag'):
        if tag.attrib['k'].startswith('tiger:county'):
            counties[tag.attrib['v']]=counties.get(tag.attrib['v'],0)+1
    
for elem in get_element(OSM_FILE):
    audit_counties(elem)

pprint.pprint(counties)
