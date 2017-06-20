from initialize import *
from audit_zip_codes import *

def clean_zip_codes(elem):
    """This function cleans the zip code in the element by retaining only the first five numeric characters in the string.

    Args:
        elem (XML Element): The element with the zip code that needs to be cleaned

    Returns:
        elem (XML Element): The passed element with the cleaned zip code
    """
    for tag in elem.iter('tag'):
        keytext=tag.attrib['k']
        if keytext.startswith('addr:postcode') or keytext.startswith('tiger:zip'):
            zipcode=tag.attrib['v']
            clean_zipcode=re.findall(r'(\d{5})',zipcode)[0]
            if zipcode=='100014':
                clean_zipcode='10014'
            tag.set('v',clean_zipcode)
            if zipcode.startswith('0'):
                elem.set('add','False')
    return elem

zipcodes={}

for elem in get_element(OSM_FILE):
    elem=clean_zip_codes(elem)
    audit_zip_codes(elem)

pprint.pprint(zipcodes)
