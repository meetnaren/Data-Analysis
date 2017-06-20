from initialize import *
from audit_cities import *

city_mappings={
    'Blissville':'Long Island City',
    'Brooklyn, Ny':'Brooklyn',
    'Brooklyn, New York':'Brooklyn',
    'Manhattan Nyc':'New York',
    'New York City':'New York',
    'New York, Ny': 'New York',
    'York City':'New York',
    'Tribeca':'New York'
}

cities={}

def clean_cities(elem, mappings=city_mappings):
    """Clean city names in the element

    Args:
        elem (XML Element): The element with the city name that needs to be analyzed and cleaned. Unclean names and mappings are available in city_mappings
        mappings (dict)   : Dictionary mapping the unclean names to the correct names. Defaults to city_mappings

    Returns:
        elem (XML Element): The element with the city name that has been analyzed and cleaned
    """
    for tag in elem.iter('tag'):
        if tag.attrib['k'].startswith('addr:city'):
            city=s.capwords(tag.attrib['v']) # this takes care of incorrect capitalization of words
            if city in mappings:
                city=mappings[city]
            tag.set('v',city)
            if tag.attrib['v'] in ['Hoboken', 'Jersey City']:
                elem.set('add','False')
    return elem
    
for elem in get_element(OSM_FILE):
    elem=clean_cities(elem)
    audit_cities(elem)
            
pprint.pprint(cities)
