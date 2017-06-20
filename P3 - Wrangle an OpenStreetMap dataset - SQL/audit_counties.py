from initialize import *

counties={}

def audit_counties(elem):
    """Find all the different counties in the XML file.

    Args:
        elem (XML Element): The element with the county name

    Returns:
        None
    """
    for tag in elem.iter('tag'):
        if tag.attrib['k'].startswith('tiger:county'):
            counties[tag.attrib['v']]=counties.get(tag.attrib['v'],0)+1
    return None
    
for elem in get_element(OSM_FILE):
    audit_counties(elem)

pprint.pprint(counties)
