def clean_counties(elem):
    """Set add flag to False if the county is Hudson

    Args:
        elem (XML Element): The element with the county name

    Returns:
        elem (XML Element): The element with the flag set to False if the county is Hudson
    """
    for tag in elem.iter('tag'):
        if tag.attrib['k'].startswith('tiger:county') and tag.attrib['v']=='Hudson, NJ':
            elem.set('add','False')
    return elem
