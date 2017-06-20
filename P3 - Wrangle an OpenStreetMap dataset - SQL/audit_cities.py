from initialize import *

cities={}

def audit_cities(elem):
    """Find all city names in the XML file

    Args:
        elem (XML Element): The element with the city name

    Returns:
        None
    """
    for tag in elem.iter('tag'):
        if tag.attrib['k'].startswith('addr:city'):
            cities[tag.attrib['v']]=cities.get(tag.attrib['v'],0)+1
    
for elem in get_element(OSM_FILE):
    audit_cities(elem)

pprint.pprint(cities)
