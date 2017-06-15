from initialize import *
from audit_zip_codes import *

def is_extension(zipcode):
    return zipcode.find('-')>-1

def is_state_code(zipcode):
    return zipcode[:2]=='NY'

def clean_zip_codes(elem):
    for tag in elem.iter('tag'):
        keytext=tag.attrib['k']
        if keytext.startswith('addr:postcode') or keytext.startswith('tiger:zip'):
            zipcode=tag.attrib['v']
            if is_extension(zipcode):
                zipcode=zipcode[:5]
            elif is_state_code(zipcode):
                zipcode=zipcode[3:8]
            elif zipcode=='100014':
                zipcode='10014'
            tag.set('v',zipcode)
            if zipcode.startswith('0'):
                elem.set('add','False')
    return elem
                
zipcodes={}

for elem in get_element(OSM_FILE):
    elem=clean_zip_codes(elem)
    audit_zip_codes(elem)

pprint.pprint(zipcodes)
