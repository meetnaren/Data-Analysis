from initialize import *
from find_street_names import *

street_names={}
abbr_street_names={}

def clean_street_words(elem):
    for tag in elem.iter('tag'):
        keytext=tag.attrib['k']
        if keytext.startswith('addr:street') or keytext.startswith('tiger:name_type'):
            words=tag.attrib['v'].split(' ')
            cleaned_tag=' '.join(words)
            for word in words:
                # removing dots and commas, and converting to lowercase for comparison
                cleanword=word.translate(None,',.').lower()
                if cleanword in abbr_names:
                    words[words.index(word)]=abbr_names[cleanword]
                # There are some tags where the street name types are separated by a colon or semicolon like this:
                # 'Ave; St; Ave' or 'St; Plz; St'
                # the following lines of code are for fixing such cases
                elif cleanword[-1]==';' and cleanword[:-1] in abbr_names:
                    words[words.index(word)]=abbr_names[cleanword[:-1]]+';'
                elif cleanword[-1]==':' and cleanword[:-1] in abbr_names:
                    words[words.index(word)]=abbr_names[cleanword[:-1]]+':'
                cleaned_tag=' '.join(words)
            if cleaned_tag!=tag.attrib['v']:
                street_names[(tag.attrib['v'],cleaned_tag)]=street_names.get((tag.attrib['v'],cleaned_tag),0)+1
                tag.set('v',cleaned_tag)
    return elem

for elem in get_element(OSM_FILE):
    elem=clean_street_words(elem)
    find_abbr_street_names(elem)

pprint.pprint(street_names)
pprint.pprint(abbr_street_names)
