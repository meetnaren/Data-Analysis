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

def clean_cities(elem):
    for tag in elem.iter('tag'):
        if tag.attrib['k'].startswith('addr:city'):
            city=s.capwords(tag.attrib['v']) # this takes care of incorrect capitalization of words
            if city in city_mappings:
                city=city_mappings[city]
            tag.set('v',city)
            if tag.attrib['v'] in ['Hoboken', 'Jersey City']:
                elem.set('add','False')
    return elem
    
for elem in get_element(OSM_FILE):
    elem=clean_cities(elem)
    audit_cities(elem)
            
pprint.pprint(cities)
