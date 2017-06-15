def clean_counties(elem):
    for tag in elem.iter('tag'):
        if tag.attrib['k'].startswith('tiger:county') and tag.attrib['v']=='Hudson, NJ':
            elem.set('add','False')
    return elem
