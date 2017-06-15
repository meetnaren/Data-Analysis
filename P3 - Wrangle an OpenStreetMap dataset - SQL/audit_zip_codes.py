from initialize import *

zipcodes={}

def audit_zip_codes(elem):
    for tag in elem.iter('tag'):
        keytext=tag.attrib['k']
        if keytext.startswith('addr:postcode') or keytext.startswith('tiger:zip'):
            if tag.attrib['v'][0]!='1' or len(tag.attrib['v'])!=5:
                zipcodes[tag.attrib['v']]=zipcodes.get(tag.attrib['v'],0)+1
    return None
    

for elem in get_element(OSM_FILE):
    audit_zip_codes(elem)
            
pprint.pprint(zipcodes)
