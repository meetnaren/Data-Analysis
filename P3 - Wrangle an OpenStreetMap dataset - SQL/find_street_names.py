from initialize import *

abbr_names = {
    "st":"Street",
    "ste":"Suite",
    "ave":"Avenue",
    "brg":"Bridge",
    "ct":"Court",
    "rd":"Road",
    "pl":"Place",
    "dr":"Drive",
    "sq":"Square",
    "ln":"Lane",
    "blvd":"Boulevard",
    "hwy":"Highway",
    "wy":"Way",
    "plz":"Plaza",
    "ctr":"Center",
    "n":"North",
    "w":"West",
    "s":"South",
    "e":"East"
    }

abbr_street_names={}

def find_abbr_street_names(elem):
    for tag in elem.iter('tag'):
        keytext=tag.attrib['k']
        if keytext.startswith('addr:street') or keytext.startswith('tiger:name_type'):
            words=tag.attrib['v'].split(' ')
            for word in words:
                word=word.translate(None,',.').lower()
                if word in abbr_names:
                    abbr_street_names[word]=abbr_street_names.get(word,0)+1
    return None

for elem in get_element(OSM_FILE):
    find_abbr_street_names(elem)

pprint.pprint(abbr_street_names)
